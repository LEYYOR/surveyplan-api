import math
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

BLACK = colors.black
WHITE = colors.white

def draw_beacon(c, px, py, size=2.5):
    s = size * mm
    # Square
    c.setStrokeColor(BLACK); c.setLineWidth(0.5)
    c.rect(px-s, py-s, s*2, s*2, fill=0, stroke=1)
    # Circle inside
    c.circle(px, py, s*0.7, fill=0, stroke=1)
    # Cross lines extending out
    c.setLineWidth(0.4)
    c.line(px, py+s, px, py+s*2.2)
    c.line(px, py-s, px, py-s*2.2)
    c.line(px-s, py, px-s*2.2, py)
    c.line(px+s, py, px+s*2.2, py)

def draw_survey_plan(info, result):
    buf = io.BytesIO()
    W, H = A4
    c = canvas.Canvas(buf, pagesize=A4)

    # === OUTER BORDER ===
    c.setStrokeColor(BLACK); c.setLineWidth(3)
    c.rect(8*mm, 8*mm, W-16*mm, H-16*mm)
    c.setLineWidth(1)
    c.rect(11*mm, 11*mm, W-22*mm, H-22*mm)

    # === TITLE BLOCK (top) ===
    ty = H - 14*mm
    c.setFont("Helvetica", 7); c.setFillColor(BLACK)
    c.drawCentredString(W/2, ty, "PLAN SHEWING PROPERTY OF")
    ty -= 5*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, ty, info.get("client_name","").upper())
    ty -= 5*mm
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(W/2, ty, "AT " + info.get("plot_address","").upper())
    ty -= 4*mm
    c.drawCentredString(W/2, ty, info.get("locality","").upper())
    ty -= 4*mm
    c.drawCentredString(W/2, ty, info.get("state","").upper())
    ty -= 5*mm
    c.setFont("Helvetica", 7)
    c.drawCentredString(W/2, ty, "SCALE  :  " + info.get("scale","1:1000"))
    ty -= 3*mm
    c.setLineWidth(2)
    c.line(W/2-20*mm, ty, W/2+20*mm, ty)
    c.setLineWidth(1)
    c.line(W/2-20*mm, ty-2*mm, W/2-20*mm, ty)
    c.line(W/2, ty-2*mm, W/2, ty)
    c.line(W/2+20*mm, ty-2*mm, W/2+20*mm, ty)
    ty -= 5*mm
    c.setFont("Helvetica", 7)
    c.drawCentredString(W/2, ty, "ORIGIN : U.T.M (ZONE 31)")
    ty -= 4*mm
    area_sqm = result["area_sqm"]
    area_ha = result["area_ha"]
    acres = round(area_ha * 2.471, 3)
    c.drawCentredString(W/2, ty, f"AREA : {area_sqm} SQ.METRES ({area_ha} HECTS / {acres} ACRES)")
    ty -= 3*mm

    # === SKETCH AREA ===
    sketch_top = ty - 1*mm
    sketch_bot = 48*mm
    sketch_h = sketch_top - sketch_bot
    sketch_x = 13*mm
    sketch_w = W - 26*mm
    c.setStrokeColor(BLACK); c.setLineWidth(0.5)
    c.rect(sketch_x, sketch_bot, sketch_w, sketch_h)

    _draw_main_sketch(c, result, info, sketch_x, sketch_bot, sketch_w, sketch_h)

    # === FIRM DETAILS inside sketch - bottom left ===
    fy = sketch_bot + 36*mm
    c.setFont("Helvetica-Bold", 6); c.setFillColor(BLACK)
    c.drawString(sketch_x + 2*mm, fy, info.get("surveyor_name","").upper())
    office = info.get("office_address","")
    office_lines = [l.strip() for l in office.split(",") if l.strip()]
    fy -= 4*mm
    c.setFont("Helvetica", 5.5)
    for line in office_lines[:6]:
        c.drawString(sketch_x + 2*mm, fy, line)
        fy -= 3.5*mm
    if info.get("email",""):
        c.drawString(sketch_x + 2*mm, fy, "E-MAIL :- " + info.get("email",""))
        fy -= 3.5*mm
    if info.get("phone",""):
        c.drawString(sketch_x + 2*mm, fy, "PHONE NO :- " + info.get("phone",""))

    # === BOTTOM BLOCK ===
    bot_y = sketch_bot
    c.setLineWidth(1); c.setStrokeColor(BLACK)
    c.line(13*mm, bot_y, W-13*mm, bot_y)
    col2_x = W/2 - 20*mm
    col3_x = W/2 + 20*mm
    c.setLineWidth(0.5)
    c.line(col2_x, 14*mm, col2_x, bot_y)
    c.line(col3_x, 14*mm, col3_x, bot_y)
    c.line(13*mm, 14*mm, W-13*mm, 14*mm)

    # PLAN NO
    c.setFont("Helvetica-Bold", 9); c.setFillColor(BLACK)
    c.drawString(15*mm, bot_y - 8*mm, "PLAN")
    c.drawRightString(col2_x - 2*mm, bot_y - 8*mm, "NO")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(15*mm, 17*mm, info.get("file_no","").replace("/", " / "))

    # Seal
    cx_seal = (col2_x + col3_x) / 2
    cy_seal = bot_y - 17*mm
    c.setStrokeColor(BLACK); c.setLineWidth(1)
    c.circle(cx_seal, cy_seal, 12*mm, fill=0, stroke=1)
    c.circle(cx_seal, cy_seal, 10*mm, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 5); c.setFillColor(BLACK)
    c.drawCentredString(cx_seal, cy_seal+3*mm, "OFFICIAL SEAL")
    c.setFont("Helvetica", 5)
    c.drawCentredString(cx_seal, cy_seal, "REG. NO.")

    # Certification
    cert_x = col3_x + 2*mm
    cert_y = bot_y - 5*mm
    c.setFont("Helvetica", 6); c.setFillColor(BLACK)
    c.drawString(cert_x, cert_y, "Certified True Copy of Original")
    cert_y -= 4*mm
    c.drawString(cert_x, cert_y, "Plan made by me")
    cert_y -= 9*mm
    c.setLineWidth(0.5)
    c.line(cert_x, cert_y, W-14*mm, cert_y)
    cert_y -= 4*mm
    c.setFont("Helvetica-Bold", 7)
    c.drawString(cert_x, cert_y, info.get("surveyor_name","")[:28])
    cert_y -= 4*mm
    c.setFont("Helvetica", 6)
    c.drawString(cert_x, cert_y, "(FNIS)")
    cert_y -= 4*mm
    c.drawString(cert_x, cert_y, "SURVEYOR")
    cert_y -= 4*mm
    c.drawString(cert_x, cert_y, info.get("survey_date",""))

    c.setFont("Helvetica", 5.5); c.setFillColor(HexColor("#888888"))
    c.drawCentredString(W/2, 11*mm, "Generated by SurveyPlan Pro")
    c.save(); buf.seek(0)
    return buf.read()


def _draw_main_sketch(c, result, info, sx, sy, sw, sh):
    coords = result["coordinates"]
    rows = result["rows"]
    if len(coords) < 2: return
    es = [p["easting"] for p in coords]
    ns = [p["northing"] for p in coords]
    mine, maxe = min(es), max(es)
    minn, maxn = min(ns), max(ns)
    re_ = max(maxe - mine, 1)
    rn = max(maxn - minn, 1)
   pad_left = 14*mm
pad_right = 14*mm
pad_top = 14*mm
pad_bottom = 45*mm
usable_w = sw - pad_left - pad_right
usable_h = sh - pad_top - pad_bottom
scale = min(usable_w/re_, usable_h/rn)
   def tx(e): return sx + pad_left + (e - mine) * scale
def ty(n): return sy + pad_bottom + (n - minn) * scale
    # North arrow
    ax, ay = sx+sw-10*mm, sy+sh-8*mm
    c.setStrokeColor(BLACK); c.setFillColor(BLACK); c.setLineWidth(1)
    c.line(ax, ay-8*mm, ax, ay)
    p = c.beginPath()
    p.moveTo(ax, ay); p.lineTo(ax-2*mm, ay-5*mm); p.lineTo(ax+2*mm, ay-5*mm); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8); c.drawCentredString(ax, ay+2*mm, "N")

    # Origin coordinates
    origin_n = info.get("origin_n","")
    origin_e = info.get("origin_e","")
    if origin_n and origin_e:
        c.setFont("Helvetica", 5.5); c.setFillColor(BLACK)
        c.drawRightString(sx+sw-2*mm, sy+sh-20*mm, origin_n+"mN")
        c.drawRightString(sx+sw-2*mm, sy+sh-25*mm, origin_e+"mE")

    # Polygon lines with bearing and distance labels
    c.setStrokeColor(BLACK); c.setLineWidth(1.2)
    for i, row in enumerate(rows):
        p1 = coords[i]
        p2 = coords[i+1] if i+1 < len(coords) else coords[0]
        x1, y1 = tx(p1["easting"]), ty(p1["northing"])
        x2, y2 = tx(p2["easting"]), ty(p2["northing"])
        c.line(x1, y1, x2, y2)
        mx, my = (x1+x2)/2, (y1+y2)/2
        angle = math.degrees(math.atan2(y2-y1, x2-x1))
        c.saveState()
        c.translate(mx, my)
        c.rotate(angle if -90 < angle < 90 else angle+180)
        c.setFont("Helvetica-Bold", 5.5); c.setFillColor(BLACK)
        c.drawCentredString(0, 2.5*mm, row["bearing"])
        c.setFont("Helvetica", 5)
        c.drawCentredString(0, -3*mm, f"{row['distance']:.3f}m")
        c.restoreState()

    # Beacon markers and labels
    beacons = info.get("beacons","").split(",") if info.get("beacons","") else []
    for i, pt in enumerate(coords):
        px, py = tx(pt["easting"]), ty(pt["northing"])
        # Draw beacon symbol — square + circle + cross
        draw_beacon(c, px, py, size=2.0)
        ox = 3*mm if px < sx+sw/2 else -12*mm
        oy = 4*mm if py < sy+sh/2 else -6*mm
        beacon = beacons[i].strip() if i < len(beacons) else f"EL{5540+i:04d}HQ"
        c.setFont("Helvetica", 5); c.setFillColor(BLACK)
        c.drawString(px+ox, py+oy, "SC/OY")
        c.drawString(px+ox, py+oy-3.5*mm, beacon)
        c.setFont("Helvetica-Bold", 6)
        c.drawString(px-4*mm, py-6*mm, pt["station"])
