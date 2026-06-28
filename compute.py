import math
import re

def parse_bearing(bearing_str):
    raw = bearing_str.strip().upper()
    pattern = r"([NS])\s*(\d+(?:\.\d+)?)[°\s']*(\d+(?:\.\d+)?)?\s*[°'\s]*([EW])"
    match = re.match(pattern, raw)
    if not match:
        return None
    ns, deg_str, min_str, ew = match.groups()
    degrees = float(deg_str)
    minutes = float(min_str) if min_str else 0.0
    angle = degrees + minutes / 60.0
    if ns == "N" and ew == "E": azimuth = angle
    elif ns == "S" and ew == "E": azimuth = 180.0 - angle
    elif ns == "S" and ew == "W": azimuth = 180.0 + angle
    elif ns == "N" and ew == "W": azimuth = 360.0 - angle
    else: return None
    return round(azimuth, 6)

def compute_traverse(points):
    rows = []
    coords = [{"station": points[0]["station"], "easting": 0.0, "northing": 0.0}]
    easting, northing = 0.0, 0.0
    sum_dep, sum_lat = 0.0, 0.0
    total_distance = 0.0
    for pt in points:
        distance = float(pt.get("distance", 0))
        azimuth = parse_bearing(pt.get("bearing", ""))
        if azimuth is not None:
            dep = distance * math.sin(math.radians(azimuth))
            lat = distance * math.cos(math.radians(azimuth))
        else:
            dep, lat = 0.0, 0.0
        easting += dep
        northing += lat
        sum_dep += dep
        sum_lat += lat
        total_distance += distance
        coords.append({"station": pt["station"], "easting": round(easting,4), "northing": round(northing,4)})
        rows.append({"station": pt["station"], "bearing": pt.get("bearing",""), "distance": round(distance,4), "departure": round(dep,4), "latitude": round(lat,4), "easting": round(easting,4), "northing": round(northing,4)})
    closure = math.sqrt(sum_dep**2 + sum_lat**2)
    precision = f"1:{round(total_distance/closure)}" if closure > 0.001 else "1:inf"
    n = len(coords)
    area = abs(sum(coords[i]["easting"]*coords[(i+1)%n]["northing"] - coords[(i+1)%n]["easting"]*coords[i]["northing"] for i in range(n)) / 2)
    return {"rows": rows, "coordinates": coords, "total_departure": round(sum_dep,4), "total_latitude": round(sum_lat,4), "closure_error_m": round(closure,4), "precision_ratio": precision, "perimeter_m": round(total_distance,4), "area_sqm": round(area,4), "area_ha": round(area/10000,6)}