"""PotholeLog parametric model (build123d), TRL 3, constructable design (PHL-DDR-003).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    potholelog-assembly.step / .stl   plate, enclosure, carrier, modules, gland, lead stub and fixings
    mounting-plate.step / .stl        the 4 mm aluminium plate with its fixing and tapped holes
    enclosure.step / .stl             enclosure base and lid with everything inside
and prints the constructability checks (python cad/src/model.py --check prints them only).

Axes: X forward along the vehicle, Y across it, Z up. The vehicle floor (or the top of the
crossmember or seat rail the plate bolts to) is Z = 0 and the logger is centred on X = Y = 0.

Revised 2026-10-01 under Amish's 2026-09-30 instruction to make the design physically
buildable (PHL-DDR-003, "Design for construction"). Every component is now a shape that can be
cut, drilled or bought, and every joint has a fixing:
    the box is held to the plate by four M4 male-female hex standoffs whose male ends pass
    through the box floor into tapped holes in the plate (no screw head under a module);
    the converter, supercapacitor and controller sit on an aluminium carrier plate screwed to
    the tops of those standoffs, with a window over the IMU;
    the IMU is held by two M3 screws through the box floor into the plate, so it is clamped
    to the aluminium, not to the plastic floor alone;
    the stock box's corner lid-screw pillars and lid screws are modelled, and every module is
    placed clear of them, of the gland's inside locknut and of each other;
    the GNSS module is held under the lid by a pad of acrylic foam tape;
    the converter is turned 90 degrees so that it no longer clashes with the supercapacitor.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (PHL-CAL-001), the drawing PHL-DWG-001 (cad/src/sheets.py), the
concept media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 mounting plate, aluminium 5052, 4 x M6 clearance holes on a rectangular pattern
    "plate": (160.0, 110.0, 4.0), "hole_pitch": (140.0, 90.0), "hole_d": 6.6,
    # 2, 3 stock IP65 enclosure (outer footprint, base height, lid height, wall)
    "box": (120.0, 90.0), "base_h": 43.0, "lid_h": 12.0, "wall": 2.5,
    #   corner lid-screw pillars moulded in the box (centre x, y and radius), lid screw M4
    "pillar": (52.5, 37.5, 5.0),
    # 12 box fixing: 4 x M4 male-female hex standoffs, through the box floor into the plate
    "box_screw_pitch": (80.0, 40.0), "standoff": (7.0, 8.0, 6.0),   # across flats, body, male thread
    # 12 module carrier: aluminium sheet (L x W x t), window over the IMU (L x W)
    "carrier": (92.0, 76.0, 1.5), "carrier_window": (30.0, 30.0),
    # modules (x, y, z sizes) and positions (x, y) relative to the box centre
    "imu": (20.0, 20.0, 1.6), "imu_xy": (0.0, -5.0), "imu_screw_dx": 7.0,      # 7, on the box floor
    "controller": (52.0, 26.0, 9.0), "controller_xy": (-12.0, 24.0), "standoff_ctrl": 6.0,   # 6
    "converter": (30.0, 40.0, 14.0), "converter_xy": (31.0, 17.0), "standoff_conv": 6.0,     # 4
    "supercap": (8.0, 20.0), "supercap_xy": (26.0, -26.0),                                   # 5, radius, height
    "gnss": (28.0, 28.0, 8.0), "gnss_xy": (-25.0, 20.0), "tape": 1.0,                        # 8, under the lid top
    "sd": (15.0, 11.0, 1.0),                                                                 # 10, in the controller slot
    # 9 cable gland on the -X end wall (body radius, length outside; y, z of centre) and lead stub
    "gland": (10.0, 18.0), "gland_yz": (10.0, 20.0), "gland_nut": (12.0, 5.0), "lead_d": 7.0, "lead_stub": 120.0,
    # 11 fixings: M6 bolts, washers and locking nuts (heads shown)
    "bolt_head": (10.0, 4.0), "washer": (12.0, 1.6),
}


@dataclass
class Comp:
    """One component: a single made or bought piece, or a matched set of fixings."""
    name: str
    shape: object
    bom: int | None
    kind: str          # "made", "bought" or "fixing"


def derived(p=PARAMS):
    """Dimensions and volumes the calc note and drawing quote, computed from PARAMS."""
    pl, pw, pt = p["plate"]
    bl, bw = p["box"]
    fl = pt + p["wall"]
    so = p["standoff"]
    ct = p["carrier"][2]
    return {
        "overall_h": pt + p["base_h"] + p["lid_h"],
        "box_h": p["base_h"] + p["lid_h"],
        "box_floor_z": fl,
        "imu_z": fl + p["imu"][2] / 2,                                 # IMU board centre height above the floor
        "gland_out": bl / 2 + p["gland"][1],                           # gland tip from the box centre, -X
        "plate_vol_mm3": pl * pw * pt - 4 * math.pi * (p["hole_d"] / 2) ** 2 * pt,
        "edge_margin": ((pl - p["hole_pitch"][0]) / 2, (pw - p["hole_pitch"][1]) / 2),
        "carrier_z": fl + so[1],                                       # underside of the carrier
        "carrier_top": fl + so[1] + ct,
        "base_top": pt + p["base_h"],
        "lid_top_in": pt + p["base_h"] + p["lid_h"] - p["wall"],
    }


def _b():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def zcyl(x, y, z, r, h):
    b = _b()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def xcyl(x, y, z, r, h):
    b = _b()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)


def zhex(x, y, z, af, h):
    """Hex prism, axis Z, across flats af, centred at z."""
    b = _b()
    return b.Pos(x, y, z) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=h / 2, both=True)


def xhex(x, y, z, af, h):
    b = _b()
    return b.Pos(x, y, z) * b.Rot(0, 90, 0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=h / 2, both=True)


def hollow(cx, cy, cz, l, w, h, wall, open_top=True):
    inner_z = cz + (wall if open_top else -wall)
    return box(cx, cy, cz, l, w, h) - box(cx, cy, inner_z, l - 2 * wall, w - 2 * wall, h)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def corners(px, py):
    return [(ix * px / 2, iy * py / 2) for ix in (-1, 1) for iy in (-1, 1)]


def module_feet(cx, cy, w, d, inset=3.5):
    return [(cx + ix * (w / 2 - inset), cy + iy * (d / 2 - inset)) for ix in (-1, 1) for iy in (-1, 1)]


def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name."""
    b = _b()
    D = derived(p)
    pl, pw, pt = p["plate"]
    bl, bw = p["box"]
    t = p["wall"]
    hx, hy = p["hole_pitch"]
    fl = D["box_floor_z"]
    so_af, so_body, so_male = p["standoff"]
    st_xy = corners(*p["box_screw_pitch"])
    ix0, iy0 = p["imu_xy"]
    imu_scr = [(ix0 - p["imu_screw_dx"], iy0), (ix0 + p["imu_screw_dx"], iy0)]
    px, py, pr = p["pillar"]
    pil_xy = corners(2 * px, 2 * py)
    C = {}

    def add(key, name, shape, bom, kind):
        C[key] = Comp(name, shape, bom, kind)

    # 1 Mounting plate: 4 x 6.6 clearance (M6), 4 x M4 tapped (standoffs), 2 x M3 tapped (IMU)
    plate = box(0, 0, pt / 2, pl, pw, pt)
    for x, y in corners(hx, hy):
        plate = plate - zcyl(x, y, pt / 2, p["hole_d"] / 2, pt + 2)
    for x, y in st_xy:
        plate = plate - zcyl(x, y, pt / 2, 2.0, pt + 2)
    for x, y in imu_scr:
        plate = plate - zcyl(x, y, pt / 2, 1.5, pt + 2)
    add("plate", "Mounting plate", plate, 1, "made")

    # 2 Enclosure base (bought, drilled): open top, corner pillars, floor and wall holes
    z0 = pt
    base = hollow(0, 0, z0 + p["base_h"] / 2, bl, bw, p["base_h"], t, open_top=True)
    hb = p["base_h"] - t
    for x, y in pil_xy:
        pil = zcyl(x, y, fl + hb / 2, pr, hb) & box(0, 0, fl + hb / 2, bl - 0.01, bw - 0.01, hb)
        base = base + pil - zcyl(x, y, fl + hb / 2 + 2, 1.7, hb)
    for x, y in st_xy:
        base = base - zcyl(x, y, z0 + t / 2, 2.25, t + 2)
    for x, y in imu_scr:
        base = base - zcyl(x, y, z0 + t / 2, 1.75, t + 2)
    gy, gz = p["gland_yz"]
    base = base - xcyl(-bl / 2 + t / 2, gy, z0 + gz, 8.0, t + 2)
    add("base", "Enclosure base, drilled", base, 2, "bought")

    # 3 Lid with its pillars, and 4 lid screws (bought with the box)
    lid_z0 = D["base_top"]
    lid = hollow(0, 0, lid_z0 + p["lid_h"] / 2, bl, bw, p["lid_h"], t, open_top=False)
    hl = p["lid_h"] - t
    screws = []
    for x, y in pil_xy:
        lp = zcyl(x, y, lid_z0 + hl / 2, pr, hl) & box(0, 0, lid_z0 + hl / 2, bl - 0.01, bw - 0.01, hl)
        lid = lid + lp - zcyl(x, y, lid_z0 + p["lid_h"] / 2, 2.2, p["lid_h"] + 2)
        top = lid_z0 + p["lid_h"]
        screws.append(zcyl(x, y, top + 1.4, 3.5, 2.8) + zcyl(x, y, top - 9, 1.7, 18))
    add("lid", "Lid with gasket", lid, 3, "bought")
    add("lid_screws", "Lid screws (4, with the box)", _fuse(screws), 3, "fixing")

    # 12 Hex standoffs: male thread through the floor into the plate, body on the floor
    sos = []
    for x, y in st_xy:
        s = zhex(x, y, fl + so_body / 2, so_af, so_body) - zcyl(x, y, fl + so_body - 2.5, 2.0, 5.01)
        s = s + zcyl(x, y, fl - so_male / 2, 2.0, so_male)
        sos.append(s)
    add("standoffs", "Hex standoffs M4 (4)", _fuse(sos), 13, "fixing")

    # 7 IMU breakout on the box floor, held by two M3 screws into the plate
    w, d, h = p["imu"]
    imu = box(ix0, iy0, fl + h / 2, w, d, h) + box(ix0, iy0 + 2, fl + h + 1.0, 6, 6, 2.0) \
        + box(ix0, iy0 + d / 2 - 2.5, fl + h + 1.5, 7, 5, 3.0)
    for x, y in imu_scr:
        imu = imu - zcyl(x, y, fl + h / 2, 1.6, h + 2)
    add("imu", "IMU breakout", imu, 7, "bought")
    isc = []
    for x, y in imu_scr:
        isc.append(zcyl(x, y, fl + h + 1.0, 2.75, 2.0) + zcyl(x, y, fl + h - 4.0, 1.5, 8.0))
    add("imu_screws", "M3 x 8 screws (2)", _fuse(isc), 13, "fixing")

    # 12 Carrier plate on the standoffs, window over the IMU, two tie slots by the supercapacitor
    cl, cw, ct = p["carrier"]
    cz = D["carrier_z"]
    car = box(0, 0, cz + ct / 2, cl, cw, ct) - box(ix0, iy0, cz + ct / 2, *p["carrier_window"], ct + 2)
    for x, y in st_xy:
        car = car - zcyl(x, y, cz + ct / 2, 2.25, ct + 2)
    for key in ("converter", "controller"):          # 3.2 mm holes for the modules' nylon standoffs
        (mx, my), (mw, md, _) = p[f"{key}_xy"], p[key]
        for x, y in module_feet(mx, my, mw, md):
            car = car - zcyl(x, y, cz + ct / 2, 1.6, ct + 2)
    sx_, sy_ = p["supercap_xy"]
    for dy in (-6.0, 2.0):
        car = car - box(sx_ - p["supercap"][0] - 2.5, sy_ + dy, cz + ct / 2, 2.0, 3.0, ct + 2)
    add("carrier", "Module carrier plate", car, 12, "made")
    cs = []
    ctop = D["carrier_top"]
    for x, y in st_xy:
        cs.append(zcyl(x, y, ctop + 1.4, 3.5, 2.8) + zcyl(x, y, ctop - 3.0, 2.0, 6.0))
    add("carrier_screws", "M4 x 6 screws (4)", _fuse(cs), 13, "fixing")

    # 4 converter, 6 controller on M3 nylon standoffs; 5 supercapacitor standing on the carrier
    feet = []
    cx, cy = p["converter_xy"]; w, d, h = p["converter"]; hs = p["standoff_conv"]
    add("converter", "DC-DC converter and protection", box(cx, cy, ctop + hs + h / 2, w, d, h), 4, "bought")
    feet += [zcyl(x, y, ctop + hs / 2, 2.5, hs) for x, y in module_feet(cx, cy, w, d)]
    cx, cy = p["controller_xy"]; w, d, h = p["controller"]; hs = p["standoff_ctrl"]
    ctrl_z = ctop + hs
    add("controller", "Controller", box(cx, cy, ctrl_z + h / 2, w, d, h), 6, "bought")
    feet += [zcyl(x, y, ctop + hs / 2, 2.5, hs) for x, y in module_feet(cx, cy, w, d)]
    add("module_standoffs", "M3 nylon standoffs (8)", _fuse(feet), 13, "fixing")
    cw_, cd_, ch_ = p["sd"]
    add("sd", "microSD card", box(cx - w / 2 + cw_ / 2 - 3, cy, ctrl_z - ch_ / 2, cw_, cd_, ch_), 10, "bought")
    r, h = p["supercap"]
    add("supercap", "Hold-up supercapacitor", zcyl(sx_, sy_, ctop + h / 2, r, h), 5, "bought")

    # 8 GNSS module under the lid top on a foam tape pad
    gx, gy_ = p["gnss_xy"]; w, d, h = p["gnss"]
    lti = D["lid_top_in"]
    add("tape", "Foam tape pad", box(gx, gy_, lti - p["tape"] / 2, 22, 22, p["tape"]), 13, "fixing")
    add("gnss", "GNSS module", box(gx, gy_, lti - p["tape"] - h / 2, w, d, h), 8, "bought")

    # 9 Cable gland: body outside, thread through the wall, locknut inside; lead stub
    gr, gl = p["gland"]
    nr, nt = p["gland_nut"]
    zg = z0 + gz
    gland = xcyl(-bl / 2 - gl / 2, gy, zg, gr, gl) + xcyl(-bl / 2 + t / 2, gy, zg, 8.0, t) \
        + xhex(-bl / 2 + t + nt / 2, gy, zg, 2 * nr * math.sqrt(3) / 2, nt) \
        + xcyl(-bl / 2 + t + nt + 1.0, gy, zg, 8.0, 2.0)
    add("gland", "Cable gland M16", gland, 9, "bought")
    lr = p["lead_d"] / 2
    xe = -bl / 2 - gl - lr
    drop = zcyl(xe, gy, (zg + lr + pt + lr) / 2, lr, zg - pt)
    run = xcyl(xe - p["lead_stub"] / 2, gy, pt + lr, lr, p["lead_stub"])
    elbow = box(-bl / 2 - gl - lr / 2, gy, zg, lr + 0.5, 2 * lr, 2 * lr)
    add("lead", "Fused lead", drop + run + elbow, 9, "bought")

    # 11 M6 bolt heads and washers on the plate (nuts are below the floor, not shown)
    bh_d, bh_h = p["bolt_head"]; wd, wt = p["washer"]
    fix = [zcyl(x, y, pt + wt / 2, wd / 2, wt) + zhex(x, y, pt + wt + bh_h / 2, bh_d, bh_h) for x, y in corners(hx, hy)]
    add("fixings", "M6 bolts and washers (4)", _fuse(fix), 11, "fixing")
    return C


BOM_GROUPS = {  # build_parts key: (BOM line, component keys)
    "plate": (1, ["plate"]), "base": (2, ["base"]), "lid": (3, ["lid", "lid_screws"]),
    "converter": (4, ["converter"]), "supercap": (5, ["supercap"]), "controller": (6, ["controller"]),
    "imu": (7, ["imu"]), "gnss": (8, ["gnss"]), "lead": (9, ["gland", "lead"]),
    "sd": (10, ["sd"]), "fixings": (11, ["fixings"]), "carrier": (12, ["carrier"]),
    "kit": (13, ["standoffs", "carrier_screws", "imu_screws", "module_standoffs", "tape"]),
}
BOM_ORDER = [(k, v[0]) for k, v in BOM_GROUPS.items()]


def build_parts(p=PARAMS):
    """Return {key: solid} for BOM items 1 to 13, grouped as BOM_GROUPS says."""
    C = build_components(p)
    return {k: _fuse([C[c].shape for c in keys]) for k, (_, keys) in BOM_GROUPS.items()}


def assembly(p=PARAMS):
    b = _b()
    return b.Compound(children=list(build_parts(p).values()))


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or keep a clearance. Returns (description, overlap mm3, gap mm,
    expectation, ok) rows; expectation is 'touch' or a minimum clearance in mm."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-3 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    box_ = S("base") + S("lid")
    chk("Box floor on the plate", S("base"), S("plate"), "touch")
    chk("Hex standoffs on the box floor, threads in the plate", S("standoffs"), S("base"), "touch")
    chk("Hex standoff threads in the tapped plate holes", S("standoffs"), S("plate"), "touch")
    chk("IMU flat on the box floor", S("imu"), S("base"), "touch")
    chk("IMU screws on the IMU", S("imu_screws"), S("imu"), "touch")
    chk("IMU screws in the tapped plate holes", S("imu_screws"), S("plate"), "touch")
    chk("IMU clear of the hex standoffs", S("imu"), S("standoffs"), 5.0)
    chk("Carrier on the hex standoffs", S("carrier"), S("standoffs"), "touch")
    chk("Carrier screws on the carrier", S("carrier_screws"), S("carrier"), "touch")
    chk("Carrier screws in the standoffs", S("carrier_screws"), S("standoffs"), "touch")
    chk("Carrier clear of the box walls and pillars", S("carrier"), S("base"), 1.0)
    chk("Carrier clear of the IMU and its screws (window)", S("carrier"), S("imu") + S("imu_screws"), 2.0)
    chk("Carrier clear of the gland locknut", S("carrier"), S("gland"), 2.0)
    chk("Module standoffs on the carrier", S("module_standoffs"), S("carrier"), "touch")
    chk("Converter on its standoffs", S("converter"), S("module_standoffs"), "touch")
    chk("Controller on its standoffs", S("controller"), S("module_standoffs"), "touch")
    chk("Supercapacitor standing on the carrier", S("supercap"), S("carrier"), "touch")
    chk("microSD card in the controller", S("sd"), S("controller"), "touch")
    mods = ["converter", "controller", "supercap"]
    for i, a in enumerate(mods):
        for b_ in mods[i + 1:]:
            chk(f"{C[a].name} clear of {C[b_].name}", S(a), S(b_), 2.0)
        chk(f"{C[a].name} clear of the box walls and pillars", S(a), S("base"), 1.0)
        chk(f"{C[a].name} clear of the carrier screw heads", S(a), S("carrier_screws"), 1.0)
        chk(f"{C[a].name} clear of the gland locknut", S(a), S("gland"), 3.0)
        chk(f"{C[a].name} clear of the GNSS module", S(a), S("gnss"), 5.0)
    chk("Supercapacitor clear of the module standoffs", S("supercap"), S("module_standoffs"), 1.0)
    chk("microSD card clear of the gland locknut", S("sd"), S("gland"), 2.0)
    chk("Gland in the end wall", S("gland"), S("base"), "touch")
    chk("Gland clear of the lid", S("gland"), S("lid"), 2.0)
    chk("Lid on the base", S("lid"), S("base"), "touch")
    chk("Lid screws on the lid", S("lid_screws"), S("lid"), "touch")
    chk("Lid screws clear of the GNSS module", S("lid_screws"), S("gnss"), 2.0)
    chk("Foam tape on the lid", S("tape"), S("lid"), "touch")
    chk("GNSS module on the foam tape", S("gnss"), S("tape"), "touch")
    chk("GNSS module 1 mm under the lid (tape gap), clear of the pillars", S("gnss"), S("lid"), 1.0)
    chk("GNSS module clear of the base", S("gnss"), S("base"), 0.4)
    chk("M6 washers on the plate", S("fixings"), S("plate"), "touch")
    chk("M6 bolt heads clear of the box (spanner room)", S("fixings"), box_, 3.0)
    chk("Lead clear of the plate and M6 fixings", S("lead"), S("plate") + S("fixings"), 1.0)
    low = min(C[k].shape.bounding_box().min.Z for k in C if k != "lead")
    rows.append(("Nothing below the plate's underside (it sits flat)", 0.0, low, 0.0, low >= -1e-6))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {
        "potholelog-assembly": [P[k] for k, _ in BOM_ORDER],
        "mounting-plate": [P["plate"]],
        "enclosure": [P[k] for k in ("base", "lid", "carrier", "kit", "converter", "supercap", "controller", "sd", "imu", "gnss")],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print("volumes (cm3): " + ", ".join(f"{k} {P[k].volume / 1000:.1f}" for k, _ in BOM_ORDER))
    print(f"overall height {D['overall_h']:.0f} mm on the floor; IMU board centre {D['imu_z']:.1f} mm above it; "
          f"carrier {D['carrier_z']:.1f} to {D['carrier_top']:.1f} mm; "
          f"plate edge margin to hole centres {D['edge_margin'][0]:.0f} x {D['edge_margin'][1]:.0f} mm")
    print_checks()
