"""PotholeLog general arrangement sheet PHL-DWG-001, Rev P2 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/PHL-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is PHL-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"
DWG = "PHL-DWG-001"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]
    tw, th = dims["top"]
    rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="PotholeLog", title="General arrangement", dwg_no=DWG, rev="P2",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Al 5052 plate; stock IP65 box; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Supply note: 60 V converter (PHL-DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    pl, pw, pt = P["plate"]
    bl, bw = P["box"]
    hx, hy = P["hole_pitch"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zf = Z(0)
    L.append(f'<line x1="{X(bb.min.X):.2f}" y1="{zf:.2f}" x2="{X(pl / 2) + 12:.2f}" y2="{zf:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(X(bb.min.X) + 4, zf + 5.5, "VEHICLE FLOOR OR RAIL", 2.0, 600, MUTED, "start"))
    xr = X(pl / 2) + 5
    L += [ext(X(bl / 2), Z(D["overall_h"]), xr + 1, Z(D["overall_h"]))]
    L += [ext(X(pl / 2), Z(pt), xr + 1, Z(pt))]
    L += dim_v(xr, Z(D["overall_h"]), Z(pt), f"{D['box_h']:.0f} BOX", side=1)
    L += leader(X(0), Z(D["imu_z"]), X(0) + 4, Z(-26), f"IMU ON BOX FLOOR, CENTER {D['imu_z']:.1f} ABOVE FLOOR")
    L += leader(X(-bl / 2 - P["gland"][1] / 2), Z(pt + P["gland_yz"][1] + P["gland"][0]), X(-bl / 2) - 12,
                Z(D["overall_h"] + 18), "M16 GLAND, FUSED LEAD TO IGNITION FEED", "end")
    L += leader(X(P["gnss_xy"][0]), Z(D["overall_h"] - P["wall"] - 2), X(P["gnss_xy"][0]) + 10, Z(D["overall_h"] + 18),
                "GNSS UNDER LID, SKY VIEW UP")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    yt = Yt(pw / 2) - 6
    yt -= 7
    L += [ext(Xt(-hx / 2), Yt(hy / 2), Xt(-hx / 2), yt - 1), ext(Xt(hx / 2), Yt(hy / 2), Xt(hx / 2), yt - 1)]
    L += dim_h(Xt(-hx / 2), Xt(hx / 2), yt, f"{hx:.0f}")
    yt2 = yt - 6
    L += [ext(Xt(-pl / 2), Yt(pw / 2), Xt(-pl / 2), yt2 - 1), ext(Xt(pl / 2), Yt(pw / 2), Xt(pl / 2), yt2 - 1)]
    L += dim_h(Xt(-pl / 2), Xt(pl / 2), yt2, f"{pl:.0f}")
    xt = Xt(pl / 2) + 5
    L += [ext(Xt(hx / 2), Yt(hy / 2), xt + 1, Yt(hy / 2)), ext(Xt(hx / 2), Yt(-hy / 2), xt + 1, Yt(-hy / 2))]
    L += dim_v(xt, Yt(hy / 2), Yt(-hy / 2), f"{hy:.0f}", side=1)
    L += leader(Xt(-hx / 2), Yt(-hy / 2), Xt(-pl / 2) - 6, Yt(-pw / 2) + 5,
                f"4 x {P['hole_d']} THRU FOR M6, LOCKING NUTS", "end")
    L.append(_t(Xt(pl / 2) + 20, Yt(0) + 1, "FORWARD +X", 2.0, 600, MUTED, "start"))

    # right view (from +X): +Y to the right, Z up
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    zr = D["overall_h"] + 10
    L += [ext(Yr(-bw / 2), Zr(D["overall_h"]) - 1, Yr(-bw / 2), Zr(zr) - 1), ext(Yr(bw / 2), Zr(D["overall_h"]) - 1, Yr(bw / 2), Zr(zr) - 1)]
    L += dim_h(Yr(-bw / 2), Yr(bw / 2), Zr(zr), f"{bw:.0f}")

    s._layers += L
    s.add_svg(views["iso"], 276, 34, 140, 98, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Plate Al 5052 {pl:.0f} x {pw:.0f} x {pt:.0f}; 4 x M6 on {hx:.0f} x {hy:.0f}",
        f"Stock IP65 box {bl:.0f} x {bw:.0f} x {D['box_h']:.0f}; 4 x M4 to plate on {P['box_screw_pitch'][0]:.0f} x {P['box_screw_pitch'][1]:.0f}",
        f"Overall height {D['overall_h']:.0f} on the floor; logger about 0.37 kg",
        "Bolt at existing floor, seat-rail or crossmember fixings",
        "Plate first mode about 186 Hz on corner bolts (PHL-CAL-001)",
        "IMU screwed flat to the box floor; X axis forward",
        "GNSS under the plastic lid; keep metal off the lid",
        "Supply 9 to 36 V, converter rated 60 V; fused 2 A, ignition switched; 0.54 W",
        "Third-angle; front view from -Y; X forward along the vehicle",
    ], x=276, y=158, width=140)
    out = s.save(ROOT / "cad" / "drawings" / DWG)
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
