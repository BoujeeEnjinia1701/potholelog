"""PotholeLog parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    potholelog-assembly.step / .stl   plate, enclosure, modules, gland, lead stub and fixings
    mounting-plate.step / .stl        the 4 mm aluminum plate with its fixing holes
    enclosure.step / .stl             enclosure base and lid with the parts inside

Axes: X forward along the vehicle, Y across it, Z up. The vehicle floor (or the top of the
crossmember or seat rail the plate bolts to) is Z = 0 and the logger is centered on X = Y = 0.
Main dimensions and interfaces only: plate and hole pattern, stock enclosure envelope, module
positions, IMU on the enclosure floor, GNSS under the lid, gland and lead exit. Not fabrication
detail; not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py (PHL-CAL-001) and the
drawing PHL-DWG-001 (cad/src/sheets.py).
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 mounting plate, aluminum 5052, 4 x M6 clearance holes on a rectangular pattern
    "plate": (160.0, 110.0, 4.0), "hole_pitch": (140.0, 90.0), "hole_d": 6.6,
    # 2, 3 stock IP65 enclosure (outer footprint, base height, lid height, wall)
    "box": (120.0, 90.0), "base_h": 43.0, "lid_h": 12.0, "wall": 2.5,
    "box_screw_pitch": (100.0, 70.0),   # 4 x M4 through the box floor into the plate (tapped)
    # modules inside (x, y, z sizes) and positions (x, y) relative to the box center
    "imu": (20.0, 20.0, 4.0), "imu_xy": (0.0, -5.0),          # 7, screwed to the box floor on the centerline
    "controller": (52.0, 26.0, 9.0), "controller_xy": (-31.0, 22.0), "standoff": 6.0,   # 6
    "converter": (40.0, 30.0, 14.0), "converter_xy": (31.0, 22.0),                     # 4
    "supercap": (8.0, 20.0), "supercap_xy": (2.5, 24.0),                                # 5, radius and height
    "gnss": (28.0, 28.0, 8.0), "gnss_xy": (-25.0, 20.0),                                # 8, under the lid top
    "sd": (15.0, 11.0, 1.0),                                                            # 10, in the controller slot
    # 9 cable gland on the -X end wall and the lead stub (the full 2 m lead is not modeled)
    "gland": (10.0, 18.0), "gland_yz": (10.0, 20.0), "lead_d": 7.0, "lead_stub": 120.0,
    # 11 fixings: M6 bolts, washers and locking nuts (heads shown)
    "bolt_head": (10.0, 4.0), "washer": (12.0, 1.6),
}


def derived(p=PARAMS):
    """Dimensions and volumes the calc note and drawing quote, computed from PARAMS."""
    pl, pw, pt = p["plate"]
    bl, bw = p["box"]
    return {
        "overall_h": pt + p["base_h"] + p["lid_h"],
        "box_h": p["base_h"] + p["lid_h"],
        "box_floor_z": pt + p["wall"],
        "imu_z": pt + p["wall"] + p["imu"][2] / 2,                     # IMU center height above the floor
        "gland_out": bl / 2 + p["gland"][1],                           # gland tip from the box center, -X
        "plate_vol_mm3": pl * pw * pt - 4 * 3.14159265 * (p["hole_d"] / 2) ** 2 * pt,
        "edge_margin": ((pl - p["hole_pitch"][0]) / 2, (pw - p["hole_pitch"][1]) / 2),
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


def hollow(cx, cy, cz, l, w, h, wall, open_top=True):
    inner_z = cz + (wall if open_top else -wall)
    return box(cx, cy, cz, l, w, h) - box(cx, cy, inner_z, l - 2 * wall, w - 2 * wall, h)


def build_parts(p=PARAMS):
    """Return {key: solid} for BOM items 1 to 11."""
    pl, pw, pt = p["plate"]
    bl, bw = p["box"]
    t = p["wall"]
    hx, hy = p["hole_pitch"]
    sx, sy = p["box_screw_pitch"]
    D = derived(p)
    parts = {}

    # 1 Mounting plate with 4 x M6 clearance holes and 4 x M4 tapped holes for the box
    plate = box(0, 0, pt / 2, pl, pw, pt)
    for ix in (-1, 1):
        for iy in (-1, 1):
            plate = plate - zcyl(ix * hx / 2, iy * hy / 2, pt / 2, p["hole_d"] / 2, pt + 2)
            plate = plate - zcyl(ix * sx / 2, iy * sy / 2, pt / 2, 1.7, pt + 2)
    parts["plate"] = plate

    # 2 Enclosure base (open top) and 3 lid (open bottom)
    z0 = pt
    parts["base"] = hollow(0, 0, z0 + p["base_h"] / 2, bl, bw, p["base_h"], t, open_top=True)
    parts["lid"] = hollow(0, 0, z0 + p["base_h"] + p["lid_h"] / 2, bl, bw, p["lid_h"], t, open_top=False)

    fl = D["box_floor_z"]
    # 4 DC-DC converter (9 to 60 V in, PHL-DDR-002) and protection board; same envelope as the 36 V module
    cx, cy = p["converter_xy"]; w, d, h = p["converter"]
    parts["converter"] = box(cx, cy, fl + h / 2, w, d, h)
    # 5 Hold-up supercapacitor (radial can, standing)
    sx_, sy_ = p["supercap_xy"]; r, h = p["supercap"]
    parts["supercap"] = zcyl(sx_, sy_, fl + h / 2, r, h)
    # 6 Controller board on a standoff rail
    cx, cy = p["controller_xy"]; w, d, h = p["controller"]; so = p["standoff"]
    parts["controller"] = box(cx, cy, fl + so + h / 2, w, d, h) + box(cx, cy, fl + so / 2, w - 12, 6, so)
    # 10 microSD card in the controller's slot (end of the board)
    cw, cd, ch = p["sd"]
    parts["sd"] = box(cx - w / 2 + cw / 2 - 3, cy, fl + so - ch / 2, cw, cd, ch)
    # 7 IMU screwed flat to the enclosure floor
    ix_, iy_ = p["imu_xy"]; w, d, h = p["imu"]
    parts["imu"] = box(ix_, iy_, fl + h / 2, w, d, h)
    # 8 GNSS module with patch antenna under the lid top
    gx, gy = p["gnss_xy"]; w, d, h = p["gnss"]
    lid_top_in = z0 + p["base_h"] + p["lid_h"] - t
    parts["gnss"] = box(gx, gy, lid_top_in - h / 2, w, d, h)
    # 9 Cable gland on the -X end wall and a stub of the fused lead dropping to the floor
    gr, gl = p["gland"]; gy_, gz_ = p["gland_yz"]
    lr = p["lead_d"] / 2
    gland = xcyl(-bl / 2 - gl / 2, gy_, z0 + gz_, gr, gl)
    xe = -bl / 2 - gl - lr
    drop = zcyl(xe, gy_, (z0 + gz_ + lr + pt + lr) / 2, lr, z0 + gz_ - pt)
    run = xcyl(xe - p["lead_stub"] / 2, gy_, pt + lr, lr, p["lead_stub"])
    elbow = box(-bl / 2 - gl - lr / 2, gy_, z0 + gz_, lr + 0.5, 2 * lr, 2 * lr)
    parts["lead"] = gland + drop + run + elbow
    # 11 Fixings: M6 bolt heads and washers on the plate (nuts are below the floor, not shown)
    bh_d, bh_h = p["bolt_head"]; wd, wt = p["washer"]
    fix = None
    for ix in (-1, 1):
        for iy in (-1, 1):
            f = zcyl(ix * hx / 2, iy * hy / 2, pt + wt / 2, wd / 2, wt) + zcyl(ix * hx / 2, iy * hy / 2, pt + wt + bh_h / 2, bh_d / 2, bh_h)
            fix = f if fix is None else fix + f
    parts["fixings"] = fix
    return parts


BOM_ORDER = [("plate", 1), ("base", 2), ("lid", 3), ("converter", 4), ("supercap", 5), ("controller", 6),
             ("imu", 7), ("gnss", 8), ("lead", 9), ("sd", 10), ("fixings", 11)]


def assembly(p=PARAMS):
    b = _b()
    return b.Compound(children=list(build_parts(p).values()))


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {
        "potholelog-assembly": [P[k] for k, _ in BOM_ORDER],
        "mounting-plate": [P["plate"]],
        "enclosure": [P[k] for k in ("base", "lid", "converter", "supercap", "controller", "sd", "imu", "gnss")],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print("volumes (cm3): " + ", ".join(f"{k} {P[k].volume / 1000:.1f}" for k, _ in BOM_ORDER))
    print(f"overall height {D['overall_h']:.0f} mm on the floor; IMU center {D['imu_z']:.1f} mm above it; "
          f"plate edge margin to hole centers {D['edge_margin'][0]:.0f} x {D['edge_margin'][1]:.0f} mm")
