import math

def draw_survey_svg(info, result):
    W = 794
    H = 1123
    coords = result["coordinates"]
    rows = result["rows"]

    es = [p["easting"] for p in coords]
    ns = [p["northing"] for p in coords]
    mine = min(es)
    maxe = max(es)
    minn = min(ns)
    maxn = max(ns)
    re_ = maxe - mine
    if re_ < 1:
        re_ = 1
    rn = maxn - minn
    if rn < 1:
        rn = 1

    sketch_x = 40
    sketch_y = 260
    sketch_w = 714
    sketch_h = 600
    pad = 50
    scale_x = (sketch_w - 2 * pad) / re_
    scale_y = (sketch_h - 2 * pad) / rn
    scale = min(scale_x, scale_y)

    def tx(e):
        return sketch_x + pad + (e - mine) * scale

    def ty(n):
        return sketch_y + sketch_h - pad - (n - minn) * scale

    parts = []
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="' + str(W) + '" height="' + str(H) + '" viewBox="0 0 ' + str(W) + ' ' + str(H) + '">')
    parts.append('<rect width="100%" height="100%" fill="white"/>')
    parts.append('<rect x="10" y="10" width="' + str(W-20) + '" height="' + str(H-20) + '" fill="none" stroke="black" stroke-width="3"/>')
    parts.append('<rect x="14" y="14" width="' + str(W-28) + '" height="' + str(H-28) + '" fill="none" stroke="black" stroke-width="1"/>')

    cy = 35
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="9">PLAN SHEWING PROPERTY OF</text>')
    cy = cy + 18
    client_name = str(info.get("client_name","")).upper()
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold">' + client_name + '</text>')
    cy = cy + 16
    plot_addr = str(info.get("plot_address","")).upper()
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="10" font-weight="bold">AT ' + plot_addr + '</text>')
    cy = cy + 14
    locality = str(info.get("locality","")).upper()
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="10" font-weight="bold">' + locality + '</text>')
    cy = cy + 14
    state = str(info.get("state","")).upper()
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="10" font-weight="bold">' + state + '</text>')
    cy = cy + 14
    scale_txt = str(info.get("scale","1:1000"))
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="9">SCALE : ' + scale_txt + '</text>')
    cy = cy + 12
    parts.append('<line x1="' + str(W//2-80) + '" y1="' + str(cy) + '" x2="' + str(W//2+80) + '" y2="' + str(cy) + '" stroke="black" stroke-width="2"/>')
    cy = cy + 14
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="9">ORIGIN : U.T.M (ZONE 31)</text>')
    cy = cy + 13
    area_sqm = result.get("area_sqm", 0)
    area_ha = result.get("area_ha", 0)
    acres = round(area_ha * 2.471, 3)
    area_txt = "AREA : " + str(area_sqm) + " SQ.METRES (" + str(area_ha) + " HECTS / " + str(acres) + " ACRES)"
    parts.append('<text x="' + str(W//2) + '" y="' + str(cy) + '" text-anchor="middle" font-family="Arial" font-size="9">' + area_txt + '</text>')

    parts.append('<rect x="' + str(sketch_x) + '" y="' + str(sketch_y) + '" width="' + str(sketch_w) + '" height="' + str(sketch_h) + '" fill="white" stroke="black" stroke-width="1"/>')

    ax = sketch_x + sketch_w - 30
    ay = sketch_y + 30
    parts.append('<line x1="' + str(ax) + '" y1="' + str(ay+25) + '" x2="' + str(ax) + '" y2="' + str(ay) + '" stroke="black" stroke-width="1.5"/>')
    parts.append('<polygon points="' + str(ax) + ',' + str(ay) + ' ' + str(ax-6) + ',' + str(ay+15) + ' ' + str(ax+6) + ',' + str(ay+15) + '" fill="black"/>')
    parts.append('<text x="' + str(ax) + '" y="' + str(ay-5) + '" text-anchor="middle" font-family="Arial" font-size="11" font-weight="bold">N</text>')

    for i in range(len(rows)):
        row = rows[i]
        p1 = coords[i]
        if i + 1 < len(coords):
            p2 = coords[i+1]
        else:
            p2 = coords[0]
        x1 = tx(p1["easting"])
        y1 = ty(p1["northing"])
        x2 = tx(p2["easting"])
        y2 = ty(p2["northing"])
        parts.append('<line x1="' + str(round(x1,1)) + '" y1="' + str(round(y1,1)) + '" x2="' + str(round(x2,1)) + '" y2="' + str(round(y2,1)) + '" stroke="black" stroke-width="1.5"/>')
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        angle = math.degrees(math.atan2(y1 - y2, x2 - x1))
        bearing_txt = str(row.get("bearing",""))
        dist_txt = str(round(row.get("distance",0), 3)) + "m"
        transform = 'rotate(' + str(round(-angle,1)) + ',' + str(round(mx,1)) + ',' + str(round(my,1)) + ')'
        parts.append('<text x="' + str(round(mx,1)) + '" y="' + str(round(my,1)) + '" text-anchor="middle" font-family="Arial" font-size="8" font-weight="bold" transform="' + transform + '">' + bearing_txt + '</text>')
        transform2 = 'rotate(' + str(round(-angle,1)) + ',' + str(round(mx,1)) + ',' + str(round(my+10,1)) + ')'
        parts.append('<text x="' + str(round(mx,1)) + '" y="' + str(round(my+10,1)) + '" text-anchor="middle" font-family="Arial" font-size="7" transform="' + transform2 + '">' + dist_txt + '</text>')

    beacons_str = info.get("beacons","")
    if beacons_str:
        beacons = beacons_str.split(",")
    else:
        beacons = []

    for i in range(len(coords)):
        pt = coords[i]
        px = tx(pt["easting"])
        py = ty(pt["northing"])
        if i < len(beacons):
            beacon = beacons[i].strip()
        else:
            beacon = "EL" + str(5540+i) + "HQ"
        parts.append('<circle cx="' + str(round(px,1)) + '" cy="' + str(round(py,1)) + '" r="4" fill="black"/>')
        if px < sketch_x + sketch_w/2:
            ox = 8
        else:
            ox = -45
        if py > sketch_y + sketch_h/2:
            oy = -8
        else:
            oy = 15
        parts.append('<text x="' + str(round(px+ox,1)) + '" y="' + str(round(py+oy,1)) + '" font-family="Arial" font-size="7">SC/OY</text>')
        parts.append('<text x="' + str(round(px+ox,1)) + '" y="' + str(round(py+oy+9,1)) + '" font-family="Arial" font-size="7">' + beacon + '</text>')
        parts.append('<text x="' + str(round(px-8,1)) + '" y="' + str(round(py+20,1)) + '" font-family="Arial" font-size="9" font-weight="bold">' + str(pt["station"]) + '</text>')

    bot_y = sketch_y + sketch_h + 5
    col2_x = W//2 - 80
    col3_x = W//2 + 80
    parts.append('<line x1="20" y1="' + str(bot_y) + '" x2="' + str(W-20) + '" y2="' + str(bot_y) + '" stroke="black" stroke-width="1"/>')
    parts.append('<line x1="' + str(col2_x) + '" y1="' + str(bot_y) + '" x2="' + str(col2_x) + '" y2="' + str(H-20) + '" stroke="black" stroke-width="0.5"/>')
    parts.append('<line x1="' + str(col3_x) + '" y1="' + str(bot_y) + '" x2="' + str(col3_x) + '" y2="' + str(H-20) + '" stroke="black" stroke-width="0.5"/>')

    fy = bot_y + 18
    surveyor_name = str(info.get("surveyor_name","")).upper()
    parts.append('<text x="25" y="' + str(fy) + '" font-family="Arial" font-size="9" font-weight="bold">' + surveyor_name + '</text>')
    fy = fy + 13
    office = info.get("office_address","")
    office_lines = office.split(",")
    count = 0
    for line in office_lines:
        if count >= 6:
            break
        line_clean = line.strip()
        if line_clean:
            parts.append('<text x="25" y="' + str(fy) + '" font-family="Arial" font-size="8">' + line_clean + '</text>')
            fy = fy + 11
            count = count + 1

    email = info.get("email","")
    if email:
        parts.append('<text x="25" y="' + str(fy) + '" font-family="Arial" font-size="8">E-MAIL :- ' + email + '</text>')
        fy = fy + 11

    phone = info.get("phone","")
    if phone:
        parts.append('<text x="25" y="' + str(fy) + '" font-family="Arial" font-size="8">PHONE NO :- ' + phone + '</text>')

    file_no = str(info.get("file_no","")).replace("/", " / ")
    parts.append('<text x="25" y="' + str(H-25) + '" font-family="Arial" font-size="11" font-weight="bold">' + file_no + '</text>')

    cx_seal = (col2_x + col3_x) // 2
    cy_seal = bot_y + 60
    parts.append('<circle cx="' + str(cx_seal) + '" cy="' + str(cy_seal) + '" r="45" fill="none" stroke="black" stroke-width="1.5"/>')
    parts.append('<circle cx="' + str(cx_seal) + '" cy="' + str(cy_seal) + '" r="38" fill="none" stroke="black" stroke-width="1"/>')
    parts.append('<text x="' + str(cx_seal) + '" y="' + str(cy_seal) + '" text-anchor="middle" font-family="Arial" font-size="8" font-weight="bold">OFFICIAL SEAL</text>')

    cx = col3_x + 10
    cy2 = bot_y + 18
    parts.append('<text x="' + str(cx) + '" y="' + str(cy2) + '" font-family="Arial" font-size="8">Certified True Copy of Original</text>')
    cy2 = cy2 + 12
    parts.append('<text x="' + str(cx) + '" y="' + str(cy2) + '" font-family="Arial" font-size="8">Plan made by me</text>')
    cy2 = cy2 + 35
    parts.append('<line x1="' + str(cx) + '" y1="' + str(cy2) + '" x2="' + str(W-25) + '" y2="' + str(cy2) + '" stroke="black" stroke-width="0.8"/>')
    cy2 = cy2 + 14
    parts.append('<text x="' + str(cx) + '" y="' + str(cy2) + '" font-family="Arial" font-size="9" font-weight="bold">' + surveyor_name[:30] + '</text>')
    cy2 = cy2 + 13
    parts.append('<text x="' + str(cx) + '" y="' + str(cy2) + '" font-family="Arial" font-size="8">(FNIS)</text>')
    cy2 = cy2 + 12
    parts.append('<text x="' + str(cx) + '" y="' + str(cy2) + '" font-family="Arial" font-size="8">SURVEYOR</text>')
    cy2 = cy2 + 12
    survey_date = str(info.get("survey_date",""))
    parts.append('<text x="' + str(cx) + '" y="' + str(cy2) + '" font-family="Arial" font-size="8">' + survey_date + '</text>')

    parts.append('</svg>')
    return "\n".join(parts)
