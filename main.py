from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import traceback
from compute import compute_traverse
from pdf_generator import draw_survey_plan

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class TraversePoint(BaseModel):
    station: str
    bearing: str
    distance: float

class SurveyInfo(BaseModel):
    surveyor_name: str
    client_name: str
    plot_address: str
    locality: str
    file_no: str
    purpose: Optional[str] = "Certificate of Occupancy"
    scale: Optional[str] = "1:500"
    survey_date: str
    state: Optional[str] = "Oyo State"
    lga: Optional[str] = ""

class GeneratePlanRequest(BaseModel):
    survey_info: SurveyInfo
    traverse_points: List[TraversePoint]

@app.get("/")
def root():
    return {"service": "SurveyPlan Pro API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-plan")
def generate_plan(request: GeneratePlanRequest):
    try:
        points = [p.dict() for p in request.traverse_points]
        result = compute_traverse(points)
        info = request.survey_info.dict()
        pdf_bytes = draw_survey_plan(info, result)
        filename = f"SurveyPlan_{info['file_no'].replace('/', '-')}.pdf"
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))code=500, detail=str(e))
