"""PotholeLog product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted aluminum mounting plate with hex M6
bolts and washers; the stock IP65 enclosure with rounded corners, a lid-to-base parting line,
stainless lid screws in corner pockets, a clear window in the lid over the GNSS patch antenna,
two lit status light pipes, a raised teal nameplate with a forward arrow (the IMU axis is
referenced to the vehicle), and a breather vent on the +X end wall; the M16 cable gland with a
knurled dome cap and the fused lead swept down to the floor and held by a P-clip. Inside: the
DC-DC converter with its inductor and terminal block, the hold-up supercapacitor, the controller
board on its standoff rail with the microSD card, the IMU breakout on the floor and the GNSS
module with its ceramic patch. Context is a compact section of vehicle floor with a crossmember
below it.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py.
Axes as model.py: X forward along the vehicle, Y across it, Z up; the vehicle floor is Z = 0
and the logger is centered on X = Y = 0. Front of the render is -Y.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Circle, Cylinder, FilletPolyline, Plane, Polygon, Pos,
                       RectangleRounded, RegularPolygon, Rot, extrude, fillet, sweep)
from model import PARAMS, derived, build_parts

TITLE = "PotholeLog: vehicle-mounted road roughness and pothole logger"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -130,
     "note": "Product render from the front left and above (about 30 deg elevation); logger bolted to a "
             "section of vehicle floor, cable gland and fused lead at left, GNSS window and status "
             "lights in the lid"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): lid with window, "
             "screws and nameplate; GNSS module; controller, microSD card, supercapacitor and DC-DC "
             "converter; IMU on the base floor; base; mounting plate and M6 fixings; gland and lead at left"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 34, "az": -40,
     "note": "Detail view from the front right and above (about 34 deg elevation) without the vehicle: "
             "nameplate with forward arrow, lit status lights, GNSS window and breather vent on the "
             "forward end"},
]

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_BASE = "#3A4049"         # dark grey stock enclosure base
C_LID = "#E4E7EB"          # light grey lid
C_PLATE = "#B9BEC5"        # 5052 aluminum
C_STEEL = "#C4C9D0"        # zinc-plated fixings, stainless screws
C_BLACK = "#1C1F24"
C_RUBBER = "#23272D"
C_WHITE = "#F4F5F6"
C_WINDOW = "#DCEBF5"
C_PCB = "#1A1D21"
C_PCB_BLUE = "#1E3A8A"
C_PCB_PURPLE = "#4C1D95"
C_PCB_GREEN = "#166534"
C_CHIP = "#111827"
C_SHIELD = "#AEB4BC"
C_CERAMIC = "#D8CBB0"
C_GOLD = "#C9A227"
C_LED_PWR = "#34D399"
C_LED_LOG = "#2DD4BF"
C_FLOOR = "#8A9098"        # painted steel floor section
C_RAIL = "#6B7179"

# Appearance-only detail sizes (mm)
PLATE_R = 8.0              # plate corner radius in plan
BOX_R = 6.0                # enclosure corner radius in plan
SEAM = 0.8                 # edge round each side of the lid-to-base parting line
LID_SCREW_XY = [(sx * 52.0, sy * 37.0) for sx in (-1, 1) for sy in (-1, 1)]
WIN_XY, WIN_SIZE, WIN_R = (-25.0, 20.0), (40.0, 38.0), 4.0
LED_XY = [(-44.0, -30.0), (-34.0, -30.0)]
LABEL_XY, LABEL_SIZE = (26.0, -2.0), (54.0, 34.0)
FLOOR_X, FLOOR_Y, FLOOR_T = (-204.0, 98.0), (-82.0, 82.0), 5.0


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _xrod(x0, x1, y, z, r):
    """Cylinder along X from x0 to x1."""
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def _hex_z(x, y, z0, af, h):
    """Hexagon prism on Z (across flats af) from z0 up by h, top edges chamfered by a fillet."""
    hx = Pos(x, y, z0) * extrude(RegularPolygon(af / 2, 6, major_radius=False), amount=h)
    return _fillet_try(hx, _top_edges(hx), [0.6, 0.4, 0.2])


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _plate(P):
    pl, pw, pt = P["plate"]
    hx, hy = P["hole_pitch"]
    sx, sy = P["box_screw_pitch"]
    plate = _prism(pl, pw, PLATE_R, 0.0, pt)
    plate = _fillet_try(plate, _top_edges(plate), [0.8, 0.5, 0.3])
    for ix in (-1, 1):
        for iy in (-1, 1):
            plate -= Pos(ix * hx / 2, iy * hy / 2, pt / 2) * Cylinder(P["hole_d"] / 2, pt + 2)
            plate -= Pos(ix * sx / 2, iy * sy / 2, pt / 2) * Cylinder(1.7, pt + 2)
    return plate


def _base(P, D):
    bl, bw = P["box"]
    t, pt, bh = P["wall"], P["plate"][2], P["base_h"]
    base = _prism(bl, bw, BOX_R, pt, bh)
    base = _fillet_try(base, _bottom_edges(base), [2.0, 1.2, 0.6])
    base = _fillet_try(base, _top_edges(base), [SEAM, 0.5])
    base -= _prism(bl - 2 * t, bw - 2 * t, BOX_R - t, D["box_floor_z"], bh)
    # lid screw pillars in the inside corners (stock box)
    for (x, y) in LID_SCREW_XY:
        pil = Pos(x, y, D["box_floor_z"]) * extrude(Circle(4.0), amount=pt + bh - D["box_floor_z"] - 0.5)
        pil -= Pos(x, y, pt + bh - 6) * Cylinder(1.6, 14)
        base += pil
    # gland bore on the -X end wall, as model.py
    gy, gz = P["gland_yz"]
    base -= _xrod(-bl / 2 - 2, -bl / 2 + t + 2, gy, pt + gz, 8.1)
    # breather vent bore on the +X end wall (proposed, see docs/REVIEW.md)
    base -= _xrod(bl / 2 - t - 2, bl / 2 + 2, 0.0, pt + 30.0, 6.2)
    return base


def _lid(P, D):
    bl, bw = P["box"]
    t, pt, bh, lh = P["wall"], P["plate"][2], P["base_h"], P["lid_h"]
    z0, top = pt + bh, pt + bh + lh
    lid = _prism(bl, bw, BOX_R, z0, lh)
    lid = _fillet_try(lid, _top_edges(lid), [3.0, 2.0, 1.2])
    lid = _fillet_try(lid, _bottom_edges(lid), [SEAM, 0.5])
    lid -= _prism(bl - 2 * t, bw - 2 * t, BOX_R - t, z0 - 1, lh + 1 - t)
    # corner screw pockets and clearance holes
    for (x, y) in LID_SCREW_XY:
        lid -= Pos(x, y, top - 1.25) * Cylinder(4.2, 2.6)
        lid -= Pos(x, y, top - lh / 2) * Cylinder(1.8, lh + 2)
        lid += Pos(x, y, z0 + (lh - t) / 2) * (Cylinder(4.0, lh - t) - Cylinder(1.8, lh))
    # GNSS window: seat pocket and through opening
    wx, wy = WIN_XY
    lid -= _prism(WIN_SIZE[0] + 4, WIN_SIZE[1] + 4, WIN_R + 2, top - 1.0, 2.0, x=wx, y=wy)
    lid -= _prism(WIN_SIZE[0], WIN_SIZE[1], WIN_R, top - t - 1, t + 2, x=wx, y=wy)
    # light pipe holes
    for (x, y) in LED_XY:
        lid -= Pos(x, y, top - lh / 2) * Cylinder(2.1, lh + 2)
    # shallow nameplate recess
    lx, ly = LABEL_XY
    lid -= _prism(LABEL_SIZE[0] + 1, LABEL_SIZE[1] + 1, 3.5, top - 0.3, 1.0, x=lx, y=ly)
    return lid


def _gland_and_lead(P):
    bl = P["box"][0]
    pt = P["plate"][2]
    gr, gl = P["gland"]
    gy, gz = P["gland_yz"]
    z = pt + gz
    x_wall = -bl / 2
    lr = P["lead_d"] / 2
    # locknut inside the wall, hex body outside, knurled dome cap, seal nose; overall length gl
    hexb = Pos(x_wall, gy, z) * Rot(0, -90, 0) * extrude(RegularPolygon(9.0, 6, major_radius=False), amount=5.5)
    hexb = _fillet_try(hexb, hexb.edges().filter_by(Axis.X, reverse=True), [0.5, 0.3])
    nut = Pos(x_wall + P["wall"], gy, z) * Rot(0, 90, 0) * extrude(RegularPolygon(9.0, 6, major_radius=False), amount=3.5)
    cap = _xrod(x_wall - 5.5, x_wall - 15.0, gy, z, gr - 1.0)
    cap = _fillet_try(cap, cap.edges(), [2.0, 1.2, 0.6])
    for k in range(12):
        a = 360.0 * k / 12
        cap -= Pos(0, gy, z) * Rot(a, 0, 0) * Pos(x_wall - 10.0, 0, gr - 1.0) * Box(5.0, 1.0, 1.0)
    nose = _xrod(x_wall - 14.5, x_wall - gl, gy, z, lr + 1.2)
    nose = _fillet_try(nose, nose.edges().sort_by(Axis.X)[:1], [0.8, 0.5])
    gland = hexb + nut + cap + nose
    # fused lead: along -X out of the gland, bend down, run aft along the floor (model.py path)
    xe = x_wall - gl - lr
    zr = pt + lr
    pts = [(x_wall - gl + 1.0, gy, z), (xe - 6.0, gy, z), (xe - 6.0, gy, zr), (xe - P["lead_stub"], gy, zr)]
    path = FilletPolyline(*pts, radius=9.0)
    lead = sweep(Plane(origin=pts[0], z_dir=(-1, 0, 0)) * Circle(lr), path=path)
    return gland, lead, xe


def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    pl, pw, pt = P["plate"]
    bl, bw = P["box"]
    t, bh, lh = P["wall"], P["base_h"], P["lid_h"]
    fl = D["box_floor_z"]
    top = pt + bh + lh
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- 1 mounting plate and 11 fixings
    add("Mounting plate (aluminum 5052)", _plate(P), C_PLATE, "metal", 1, "shell", (0, 0, 0))
    hx, hy = P["hole_pitch"]
    bh_d, bh_h = P["bolt_head"]
    wd, wt = P["washer"]
    washers, bolts = [], []
    for ix in (-1, 1):
        for iy in (-1, 1):
            x, y = ix * hx / 2, iy * hy / 2
            w = Pos(x, y, pt + wt / 2) * (Cylinder(wd / 2, wt) - Cylinder(3.3, wt + 1))
            washers.append(_fillet_try(w, _top_edges(w).filter_by(lambda e: e.radius > 5), [0.4, 0.2]))
            b = _hex_z(x, y, pt + wt, bh_d, bh_h)
            b += Pos(x, y, pt + wt + bh_h + 0.3) * Cylinder(2.6, 0.6)   # thread end proud of the head
            bolts.append(b)
    add("M6 washers", _union(washers), C_STEEL, "metal", 11, "shell", (0, 0, 30))
    add("M6 hex bolts", _union(bolts), C_STEEL, "metal", 11, "shell", (0, 0, 55))

    # ---- 2 enclosure base, 3 lid
    add("Enclosure base (IP65)", _base(P, D), C_BASE, "plastic", 2, "shell", (0, 0, 20))
    add("Enclosure lid", _lid(P, D), C_LID, "plastic", 3, "shell", (0, 0, 210))
    gasket = _prism(bl - 2 * t - 0.4, bw - 2 * t - 0.4, BOX_R - t, pt + bh - 1.0, 1.0) - \
        _prism(bl - 2 * t - 4.0, bw - 2 * t - 4.0, BOX_R - t - 1.8, pt + bh - 2.0, 3.0)
    for (x, y) in LID_SCREW_XY:
        gasket -= Pos(x, y, pt + bh) * Cylinder(4.3, 4.0)
    add("Lid gasket", gasket, C_BLACK, "rubber", 3, "shell", (0, 0, 182))
    screws = []
    for (x, y) in LID_SCREW_XY:
        s = Pos(x, y, top - 2.5) * Cylinder(3.6, 1.8)
        s = _fillet_try(s, _top_edges(s), [0.8, 0.5])
        s -= Pos(x, y, top - 1.2) * Box(4.6, 0.8, 1.2)
        s -= Pos(x, y, top - 1.2) * Box(0.8, 4.6, 1.2)
        screws.append(s)
    add("Lid screws (stainless)", _union(screws), C_STEEL, "metal", 2, "shell", (0, 0, 246))
    wx, wy = WIN_XY
    window = _prism(WIN_SIZE[0] + 3.6, WIN_SIZE[1] + 3.6, WIN_R + 1.8, top - 1.0, 0.9, x=wx, y=wy)
    add("GNSS window (polycarbonate)", window, C_WINDOW, "clear", 3, "shell", (0, 0, 226))
    # nameplate: teal plate, white forward arrow and three text bars
    lx, ly = LABEL_XY
    plate_lab = _prism(LABEL_SIZE[0], LABEL_SIZE[1], 3.0, top - 0.3, 0.5, x=lx, y=ly)
    add("Nameplate", plate_lab, C_ACCENT, "plastic", None, "shell", (0, 0, 238))
    zlab = top + 0.2
    arrow = Pos(lx - 4, ly + 7.5, zlab) * extrude(
        Polygon((-18, -2), (6, -2), (6, -5.5), (15, 0), (6, 5.5), (6, 2), (-18, 2), align=None), amount=0.25)
    bars = _union([Pos(lx - 7.0 + dx, ly - 6.0 - 5.0 * k, zlab) * extrude(RectangleRounded(ln, 2.0, 0.9), amount=0.25)
                   for k, (ln, dx) in enumerate([(36.0, 5.0), (26.0, 0.0), (18.0, -4.0)])])
    add("Nameplate marking", arrow + bars, C_WHITE, "plastic", None, "shell", (0, 0, 238))
    # light pipes with dark bezels
    bez, pipes = [], []
    for (x, y) in LED_XY:
        b = Pos(x, y, top + 0.4) * (Cylinder(3.4, 0.8) - Cylinder(2.1, 1.0))
        bez.append(_fillet_try(b, _top_edges(b), [0.3, 0.2]))
        p = Pos(x, y, top - lh / 2 + 0.35) * Cylinder(2.0, lh + 0.7)
        pipes.append(_fillet_try(p, _top_edges(p), [0.6, 0.4]))
    add("Light pipe bezels", _union(bez), C_BLACK, "plastic", None, "shell", (0, 0, 246))
    add("Status light, power (lit)", pipes[0], C_LED_PWR, "emissive", None, "shell", (0, 0, 246))
    add("Status light, logging (lit)", pipes[1], C_LED_LOG, "emissive", None, "shell", (0, 0, 246))
    # breather vent on the +X end wall
    vz = pt + 30.0
    vent = _xrod(bl / 2, bl / 2 + 4.0, 0.0, vz, 7.0)
    vent = _fillet_try(vent, vent.edges().sort_by(Axis.X)[-1:], [1.5, 1.0, 0.5])
    vent += _xrod(bl / 2 - t - 2.0, bl / 2 + 0.1, 0.0, vz, 6.0)
    for k in range(3):
        vent -= Pos(bl / 2 + 3.2, 0.0, vz - 3.0 + 3.0 * k) * Box(2.0, 8.0, 0.9)
    add("Breather vent", vent, C_SHIELD, "plastic", None, "shell", (45, 0, 20))

    # ---- 9 gland and lead
    gland, lead, xe = _gland_and_lead(P)
    add("M16 cable gland", gland, C_RUBBER, "plastic", 9, "shell", (-35, 0, 20))
    add("Fused lead (2 m, stub shown)", lead, C_BLACK, "rubber", 9, "shell", (-55, 0, 20))
    lr = P["lead_d"] / 2
    cx = xe - 70.0
    gy = P["gland_yz"][0]
    clip = Pos(cx, gy, pt + lr) * Rot(0, 90, 0) * (Cylinder(lr + 1.2, 8.0) - Cylinder(lr, 9.0))
    clip += Pos(cx, gy - lr - 6.0, 0.6) * Box(8.0, 12.0, 1.2)
    clip += Pos(cx, gy - lr - 0.6, (pt + lr) / 2 + 0.3) * Box(8.0, 1.2, pt + lr - 0.6)
    add("Lead P-clip", clip, C_STEEL, "metal", 11, "context", (0, 0, 0))

    # ---- internals on the base floor
    # 7 IMU breakout (purple PCB, chip, header row)
    ix_, iy_ = P["imu_xy"]
    iw, idp, ih = P["imu"]
    imu = _prism(iw, idp, 1.5, fl + 2.0, 1.6, x=ix_, y=iy_)
    for sx in (-1, 1):
        for sy in (-1, 1):
            imu -= Pos(ix_ + sx * 7.0, iy_ + sy * 7.0, fl + 2.8) * Cylinder(1.3, 3.0)
    add("6-axis IMU breakout", imu, C_PCB_PURPLE, "plastic", 7, "internal", (0, 0, 55))
    ic = Pos(ix_, iy_, fl + 3.6 + 0.45) * Box(3.0, 2.5, 0.9)
    ic += Pos(ix_, iy_ - 7.0, fl + 3.6 + 1.25) * Box(12.0, 2.5, 2.5)
    ic += _union([Pos(ix_ + sx * 7.0, iy_ + sy * 7.0, fl + 1.0) * Cylinder(2.2, 2.0) for sx in (-1, 1) for sy in (-1, 1)])
    add("IMU chip, header and spacers", ic, C_CHIP, "plastic", 7, "internal", (0, 0, 55))
    ss = _union([Pos(ix_ + sx * 7.0, iy_ + sy * 7.0, fl + 3.6 + 0.6) * Cylinder(2.2, 1.2) for sx in (-1, 1) for sy in (-1, 1)])
    add("IMU screws", ss, C_STEEL, "metal", 11, "internal", (0, 0, 55))

    # 4 DC-DC converter and protection (blue PCB, inductor, capacitors, terminal block)
    cx_, cy_ = P["converter_xy"]
    cw, cd, ch = P["converter"]
    conv = _prism(cw, cd, 1.2, fl + 2.0, 1.6, x=cx_, y=cy_)
    add("DC-DC converter board", conv, C_PCB_BLUE, "plastic", 4, "internal", (0, 0, 90))
    cz = fl + 3.6
    ind = Pos(cx_ - 4, cy_ + 3, cz + 4.0) * Box(12.0, 12.0, 8.0)
    ind = _fillet_try(ind, ind.edges().filter_by(Axis.Z), [2.0, 1.0])
    caps_ = Pos(cx_ + 10, cy_ + 8, cz + 5.0) * Cylinder(4.0, 10.0)
    caps_ += Pos(cx_ + 10, cy_ - 2, cz + 4.0) * Cylinder(3.2, 8.0)
    caps_ = _fillet_try(caps_, [e for e in caps_.edges() if e.center().Z > cz + 7.5], [0.6, 0.3])
    tvs = Pos(cx_ - 10, cy_ - 9, cz + 1.0) * Box(5.0, 3.6, 2.0)
    add("Converter inductor and TVS", ind + tvs, C_CHIP, "plastic", 4, "internal", (0, 0, 90))
    add("Converter capacitors", caps_, C_SHIELD, "metal", 4, "internal", (0, 0, 90))
    term = Pos(cx_ - cw / 2 + 4.0, cy_ - 2, cz + 5.0) * Box(7.0, 14.0, 10.0)
    for k in (-1, 1):
        term -= Pos(cx_ - cw / 2 + 4.0, cy_ - 2 + k * 3.5, cz + 10.0) * Cylinder(1.4, 3.0)
    add("Converter terminal block", term, C_ACCENT, "plastic", 4, "internal", (0, 0, 90))
    stand = _union([Pos(cx_ + sx * (cw / 2 - 3), cy_ + sy * (cd / 2 - 3), fl + 1.0) * Cylinder(2.0, 2.0)
                    for sx in (-1, 1) for sy in (-1, 1)])
    add("Converter spacers", stand, C_STEEL, "metal", 11, "internal", (0, 0, 90))

    # 5 hold-up supercapacitor (sleeved can)
    sx_, sy_ = P["supercap_xy"]
    sr, sh = P["supercap"]
    can = Pos(sx_, sy_, fl + sh / 2) * Cylinder(sr, sh)
    can = _fillet_try(can, _top_edges(can), [0.8, 0.5])
    can -= Pos(sx_, sy_, fl + sh - 2.5) * (Cylinder(sr + 1, 0.6) - Cylinder(sr - 0.4, 1.0))
    add("Hold-up supercapacitor", can, "#1F2A44", "painted", 5, "internal", (0, 0, 90))
    cap_top = Pos(sx_, sy_, fl + sh + 0.05) * Cylinder(sr - 1.5, 0.1)
    add("Supercapacitor top disc", cap_top, C_STEEL, "metal", 5, "internal", (0, 0, 90))

    # 6 controller on a standoff rail, with ESP32-S3 module shield, USB-C and 10 microSD card
    kx, ky = P["controller_xy"]
    kw, kd, kh = P["controller"]
    so = P["standoff_ctrl"]   # controller standoff height (PHL-DDR-003)
    rail = Pos(kx, ky, fl + so / 2) * Box(kw - 12, 6, so)
    rail = _fillet_try(rail, rail.edges().filter_by(Axis.X), [1.0, 0.5])
    add("Controller standoff rail", rail, "#4B5563", "plastic", 6, "internal", (0, 0, 112))
    kz = fl + so
    pcb = _prism(kw, kd, 1.5, kz, 1.6, x=kx, y=ky)
    add("Controller PCB (ESP32-S3)", pcb, C_PCB, "plastic", 6, "internal", (0, 0, 118))
    shield = Pos(kx + 8, ky, kz + 1.6 + 1.6) * Box(18.0, 16.0, 3.2)
    shield = _fillet_try(shield, _top_edges(shield), [0.4, 0.2])
    usbc = Pos(kx + kw / 2 - 3.5, ky, kz + 1.6 + 1.6) * Box(7.0, 9.0, 3.2)
    add("ESP32-S3 module shield and USB-C", shield + usbc, C_SHIELD, "metal", 6, "internal", (0, 0, 118))
    ant = Pos(kx + 21, ky, kz + 1.6 + 0.4) * Box(8.0, 16.0, 0.8)
    hdr = Pos(kx - 4, ky + kd / 2 - 1.6, kz + 1.6 + kh / 2 - 1.0) * Box(30.0, 2.5, kh - 3.6)
    hdr += Pos(kx - 4, ky - kd / 2 + 1.6, kz + 1.6 + kh / 2 - 1.0) * Box(30.0, 2.5, kh - 3.6)
    add("Controller headers and antenna", ant + hdr, C_CHIP, "plastic", 6, "internal", (0, 0, 118))
    sdw, sdd, sdh = P["sd"]
    slot = Pos(kx - kw / 2 + sdw / 2 - 1.0, ky, kz - 1.0) * Box(sdw + 2.0, sdd + 2.0, 2.0)
    add("microSD slot", slot, C_SHIELD, "metal", 6, "internal", (0, 0, 118))
    add("microSD card (32 GB)", m["sd"], "#B91C1C", "plastic", 10, "internal", (-40, 0, 118))

    # 8 GNSS module with ceramic patch antenna, under the lid top (seen through the window)
    gx, gy2 = P["gnss_xy"]
    gw, gd, gh = P["gnss"]
    lid_in = top - t
    gpcb = _prism(gw, gd, 1.0, lid_in - gh, 1.6, x=gx, y=gy2)
    add("GNSS module PCB", gpcb, C_PCB_GREEN, "plastic", 8, "internal", (0, 0, 150))
    gshield = Pos(gx, gy2 - 6, lid_in - gh - 1.2) * Box(14.0, 12.0, 2.4)
    add("GNSS receiver shield", gshield, C_SHIELD, "metal", 8, "internal", (0, 0, 150))
    patch = _prism(25.0, 25.0, 0.8, lid_in - gh + 1.6, gh - 1.6 - 0.3, x=gx, y=gy2)
    patch = _fillet_try(patch, _top_edges(patch), [0.6, 0.3])
    add("GNSS ceramic patch antenna", patch, C_CERAMIC, "plastic", 8, "internal", (0, 0, 150))
    elec = _prism(17.0, 17.0, 0.4, lid_in - 0.3, 0.25, x=gx, y=gy2)
    elec += Pos(gx + 3.0, gy2 + 3.0, lid_in - 0.05) * Cylinder(1.0, 0.2)
    add("Patch electrode", elec, C_GOLD, "metal", 8, "internal", (0, 0, 150))

    # ---- context: compact section of vehicle floor with a crossmember under the fixings
    x0, x1 = FLOOR_X
    y0, y1 = FLOOR_Y
    floor = Pos((x0 + x1) / 2, (y0 + y1) / 2, -FLOOR_T / 2) * Box(x1 - x0, y1 - y0, FLOOR_T)
    floor = _fillet_try(floor, floor.edges().filter_by(Axis.Z), [3.0, 1.5])
    add("Vehicle floor section (painted steel)", floor, C_FLOOR, "painted", None, "context", (0, 0, 0))
    rail_h = 32.0
    xm = Pos(hx / 2, 0, -FLOOR_T - rail_h / 2) * Box(40.0, y1 - y0 - 20, rail_h)
    xm -= Pos(hx / 2, 0, -FLOOR_T - rail_h / 2) * Box(34.0, y1 - y0, rail_h - 6)
    xm2 = Pos(-hx, 0, 0) * xm
    add("Crossmembers", xm + xm2, C_RAIL, "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:7.2f} cm3")
