"""PotholeLog prototype build plan pictures (PHL-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/PHL-DWG-101 to 104        making sketches for the made and drilled components
    docs/05-build-plan/plate-holes.png     hole positions on the mounting plate
    docs/05-build-plan/box-holes.png       hole positions on the enclosure floor and end wall
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, zcyl, zhex, box, corners, _fuse  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
REPO = "github.com/BoujeeEnjinia1701/potholelog"
D = derived(P)
C = build_components(P)
S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"plate": "#A8A29E", "base": "#4B5563", "lid": "#14B8A6", "gland": "#1F2937", "lead": "#374151",
       "standoffs": "#B45309", "imu": "#C2410C", "carrier": "#94A3B8", "mstand": "#E5E7EB", "conv": "#2563EB",
       "cap": "#7C3AED", "ctrl": "#065F46", "sd": "#DC2626", "gnss": "#D4A017", "tape": "#F9FAFB",
       "screw": "#111827", "bolt": "#6B7280", "board": "#D6C7A1", "vent": "#64748B", "status": "#059669",
       "label": "#0F766E"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


# ----------------------------------------------------------------- bench test board and M6 hardware
BOARD_T = 18.0


def bench_board():
    """Plywood offcut standing in for the vehicle floor during the first checks (not in the BOM)."""
    brd = box(0, 0, -BOARD_T / 2, 220, 160, BOARD_T)
    for x, y in corners(*P["hole_pitch"]):
        brd = brd - zcyl(x, y, -BOARD_T / 2, 3.3, BOARD_T + 2)
    return brd


def m6_shanks():
    hx, hy = P["hole_pitch"]
    return _fuse([zcyl(x, y, (P["plate"][2] - BOARD_T - 10) / 2, 3.0, P["plate"][2] + BOARD_T + 10) for x, y in corners(hx, hy)])


def m6_nuts():
    hx, hy = P["hole_pitch"]
    return _fuse([zcyl(x, y, -BOARD_T - 0.8, 6.0, 1.6) + zhex(x, y, -BOARD_T - 1.6 - 3.0, 10.0, 6.0) for x, y in corners(hx, hy)])


def m6_through():
    """M6 bolt shanks through plate and board, with washers and nyloc nuts under the board."""
    hx, hy = P["hole_pitch"]
    out = []
    for x, y in corners(hx, hy):
        out.append(zcyl(x, y, (P["plate"][2] - BOARD_T - 10) / 2, 3.0, P["plate"][2] + BOARD_T + 10)
                   + zcyl(x, y, -BOARD_T - 0.8, 6.0, 1.6) + zhex(x, y, -BOARD_T - 1.6 - 3.0, 10.0, 6.0))
    return _fuse(out)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "plate": part("Mounting plate", C["plate"].shape, COL["plate"]),
        "base": part("Enclosure base, drilled", C["base"].shape, COL["base"]),
        "gland": part("Cable gland and locknut", C["gland"].shape, COL["gland"]),
        "vent": part("Breather vent and locknut", C["vent"].shape, COL["vent"]),
        "standoffs": part("Hex standoffs M4 (4)", C["standoffs"].shape, COL["standoffs"]),
        "imu": part("IMU and two M3 screws", S("imu", "imu_screws"), COL["imu"]),
        "carrier": part("Carrier plate and its M4 screws", S("carrier", "carrier_screws"), COL["carrier"]),
        "mstand": part("Nylon standoffs (8)", C["module_standoffs"].shape, "#9CA3AF"),
        "conv": part("DC-DC converter", C["converter"].shape, COL["conv"]),
        "cap": part("Hold-up supercapacitor", C["supercap"].shape, COL["cap"]),
        "ctrl": part("Controller with microSD card", S("controller", "sd"), COL["ctrl"]),
        "lead": part("Fused lead", C["lead"].shape, COL["lead"]),
        "gnss": part("GNSS module and foam tape", S("gnss", "tape"), COL["gnss"]),
        "status": part("Light pipes, LEDs and their lead", S("light_pipes", "lp_nuts", "leds", "led_wires"), COL["status"]),
        "label": part("Nameplate label", C["label"].shape, COL["label"]),
        "lid": part("Lid and four lid screws", S("lid", "lid_screws"), COL["lid"]),
        "bolts": part("M6 bolts and washers (4)", C["fixings"].shape, COL["bolt"]),
    }


ORDER = ["plate", "base", "gland", "vent", "standoffs", "imu", "carrier", "mstand", "conv", "cap", "ctrl", "lead", "status", "label",
         "gnss", "lid", "bolts"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"plate": (0, 0, 0), "base": (0, 0, 70), "gland": (-110, 0, 70), "standoffs": (0, 0, 150),
           "imu": (0, 0, 175), "carrier": (0, 0, 205), "mstand": (0, 0, 230), "conv": (60, 0, 260),
           "cap": (50, -70, 240), "ctrl": (-50, 0, 285), "lead": (-150, 0, 40), "gnss": (0, 0, 330),
           "lid": (0, 0, 410), "bolts": (0, 0, 35), "vent": (90, 0, 70), "status": (0, -40, 470),
           "label": (0, 0, 455)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "PotholeLog prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the gland end is at the back left",
                       elev=22, azim=-55, size=(10, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    M = made()
    base = dict(project="PotholeLog", date=DATE)
    out = []
    out.append(bv.component_sheet(
        Part("Mounting plate", C["plate"].shape, COL["plate"]), [M["base"], M["bolts"]],
        dwg_no="PHL-DWG-101", title="PotholeLog mounting plate: making sketch", material="Aluminium sheet 4 mm, 5052",
        notes=["Blank 160 x 110 mm, 4 mm aluminium. Square the edges, deburr,",
               "  round the corners to about 2 mm. Measure every hole from the",
               "  plate's centre lines; the hole layout picture repeats them.",
               "Corner holes: four 6.6 mm (M6 clearance), 70 mm each side along the",
               "  length and 45 mm each side across (140 x 90 mm apart).",
               "Box standoff holes: four M4 tapped, drill 3.3 mm and tap,",
               "  40 mm each side along and 20 mm each side across (80 x 40 apart).",
               "IMU holes: two M3 tapped, drill 2.5 mm and tap, 7 mm each side of",
               "  the cross centre line, 5 mm to the right of the long centre line.",
               "Better: drill the IMU and standoff holes through the box floor",
               "  with the box clamped on the plate, then open the floor holes.",
               "Fit: the box floor sits flat on the top face; nothing may stick out",
               "  below the plate, so the standoffs and screws stop inside it.",
               "Check: every tapped hole takes its screw by hand."],
        inset_view=(30, -55), **base))
    out.append(bv.component_sheet(
        Part("Enclosure base", C["base"].shape, COL["base"]), [M["plate"], M["standoffs"], M["gland"]],
        dwg_no="PHL-DWG-102", title="PotholeLog enclosure base: drilling sketch", material="Bought IP65 polycarbonate box 120 x 90 x 55 mm",
        notes=["Bought box with four moulded corner pillars for the lid screws.",
               "Floor, measured from its centre, front is away from the gland:",
               "  four 4.5 mm holes 40 mm each side along, 20 mm each side across;",
               "  two 3.5 mm holes 7 mm each side of centre, 5 mm to the right.",
               "  The floor holes must match the plate's tapped holes: drill",
               "  them through the plate's holes with the box clamped on it.",
               "Rear end wall: one 16.2 mm hole for the M16 gland, 10 mm left",
               "  of centre, its centre 20 mm up from the box's underside.",
               "Front end wall: one 12.2 mm hole for the M12 breather vent,",
               "  on the centre line, its centre 30 mm up from the underside.",
               "Tape the faces, pilot 3 mm at low speed with wood behind, open",
               "  out with a step drill. No solvents: polycarbonate crazes.",
               "Fit: the floor sits flat on the plate; a ring of neutral-cure",
               "  silicone round each floor hole underneath seals it.",
               "Check: no crack runs from any hole under a bright lamp."],
        inset_view=(30, -130), **base))
    (lx0, ly0), (lx1, _) = P["light_pipe_xy"]
    out.append(bv.component_sheet(
        Part("Enclosure lid", C["lid"].shape, COL["lid"]), [M["status"], M["label"], M["gnss"]],
        dwg_no="PHL-DWG-104", title="PotholeLog enclosure lid: drilling sketch", material="Lid of the bought IP65 box (opaque)",
        notes=["Lid of the bought box, opaque, with its gasket and corner pillars.",
               f"Two {P['light_pipe'][0]:g} mm holes for the sealed light pipes, measured",
               f"  from the lid's centre: {abs(lx0):g} and {abs(lx1):g} mm toward the rear (gland)",
               f"  end, both {abs(ly0):g} mm to the right of the long centre line.",
               "  Rear hole: power light; front hole: logging light.",
               "Tape the top, pilot 3 mm with wood behind, open out with a",
               "  step drill; check the size against the light pipe's datasheet.",
               "Keep 25 mm round the GNSS module's patch free of labels and metal.",
               f"Nameplate label {P['label'][0]:g} x {P['label'][1]:g} mm, centred {P['label_xy'][0]:g} mm forward,",
               "  arrow pointing forward, on the cleaned lid top.",
               "Fit: each pipe's O-ring under its flange outside, nut inside.",
               "Check: no crack from either hole; the nuts clear the pillars."],
        inset_view=(35, -55), **base))
    out.append(bv.component_sheet(
        Part("Module carrier plate", C["carrier"].shape, COL["carrier"]), [M["base"], M["standoffs"], M["imu"], M["plate"]],
        dwg_no="PHL-DWG-103", title="PotholeLog module carrier plate: making sketch", material="Aluminium sheet 1.5 mm, 5052",
        notes=["Blank 92 x 76 mm, 1.5 mm aluminium; deburr all edges.",
               "Window 30 x 30 mm over the IMU, centred 5 mm right of centre:",
               "  drill 6 mm in each corner, cut between with a piercing saw, file.",
               "Fixing holes: four 4.5 mm, 80 x 40 mm apart, matching the plate.",
               "Module holes: 3.2 mm; mark them through each module (about",
               "  23 x 33 mm for the converter, 45 x 19 mm for the controller).",
               "Tie slots: two 2 x 3 mm, 15.5 mm forward of centre, 24 and",
               "  32 mm right of centre, for the supercapacitor's cable tie.",
               "Fit: sits on the four hex standoffs 8 mm above the box floor,",
               "  held by four M4 x 6 screws; 1.5 mm clear of the walls and",
               "  pillars, 4.5 mm clear of the gland locknut.",
               "Check: drops onto the standoffs without touching a wall."],
        inset_view=(35, -55), **base))
    return out


# ----------------------------------------------------------------- hole layouts (matplotlib, from PARAMS)
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []
    OUT.mkdir(parents=True, exist_ok=True)

    def foot(fig):
        fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
        fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")

    # mounting plate, seen from above, front (+X) to the right
    pl, pw, _ = P["plate"]
    hx, hy = P["hole_pitch"]
    sx, sy = P["box_screw_pitch"]
    ix, iy = P["imu_xy"]
    dx = P["imu_screw_dx"]
    fig = plt.figure(figsize=(11, 7.4), dpi=150)
    ax = fig.add_axes([0.04, 0.1, 0.62, 0.78]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(FancyBboxPatch((-pl / 2 + 2, -pw / 2 + 2), pl - 4, pw - 4, boxstyle="round,pad=2", fc="#F5F5F4", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-P["box"][0] / 2, -P["box"][1] / 2), *P["box"], fc="none", ec=MUT, lw=0.7, ls="--"))
    ax.text(-P["box"][0] / 2 + 2, P["box"][1] / 2 - 3, "box outline", fontsize=7, color=MUT, va="top")
    ax.plot([-pl / 2 - 3, pl / 2 + 3], [0, 0], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.plot([0, 0], [-pw / 2 - 3, pw / 2 + 3], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    holes = [(x, y, P["hole_d"], "6.6") for x, y in corners(hx, hy)] + \
            [(x, y, 3.3, "M4") for x, y in corners(sx, sy)] + [(ix - dx, iy, 2.5, "M3"), (ix + dx, iy, 2.5, "M3")]
    for x, y, d, _ in holes:
        ax.add_patch(plt.Circle((x, y), d / 2, fc="white", ec=INK, lw=1))
        ax.plot([x - d / 2 - 2, x + d / 2 + 2], [y, y], color=MUT, lw=0.4); ax.plot([x, x], [y - d / 2 - 2, y + d / 2 + 2], color=MUT, lw=0.4)
    for i, x in enumerate(sorted({abs(h[0]) for h in holes})):
        ax.plot([x, x], [-pw / 2, -pw / 2 - 6 - 7 * (i % 2)], color=AC, lw=0.4, ls=":")
        ax.text(x, -pw / 2 - 7 - 7 * (i % 2), f"{x:g}", ha="center", va="top", fontsize=8, color=AC)
    for i, y in enumerate(sorted({h[1] for h in holes})):
        ax.plot([pl / 2, pl / 2 + 5 + 10 * (i % 2)], [y, y], color=AC, lw=0.4, ls=":")
        ax.text(pl / 2 + 6 + 10 * (i % 2), y, f"{y:+g}", ha="left", va="center", fontsize=8, color=AC)
    ax.text(0, -pw / 2 - 24, "along the plate from the cross centre line, mm (same each way)", ha="center", fontsize=8, color=MUT)
    ax.text(pl / 2 + 6, -pw / 2 + 2, "across, mm\n(+ is left)", ha="left", va="center", fontsize=8, color=MUT)
    ax.annotate("", xy=(pl / 2 - 6, pw / 2 + 8), xytext=(pl / 2 - 30, pw / 2 + 8), arrowprops=dict(arrowstyle="-|>", color=AC))
    ax.text(pl / 2 - 32, pw / 2 + 8, "front of the vehicle", ha="right", va="center", fontsize=8, color=AC)
    ax.set_xlim(-pl / 2 - 6, pl / 2 + 52); ax.set_ylim(-pw / 2 - 30, pw / 2 + 14)
    fig.text(0.03, 0.965, "Mounting plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Seen from above, gland end on the left. Full size figures in mm from the plate's centre lines, taken from the model.",
             fontsize=8.5, color=MUT, va="top")
    key = ["Corner holes 6.6 mm (4): M6 bolts", "  into the vehicle, 140 x 90 apart", "",
           "M4 tapped (4), drill 3.3 mm:", "  box hex standoffs, 80 x 40 apart", "",
           "M3 tapped (2), drill 2.5 mm:", "  IMU screws, 14 apart, 5 mm right", "",
           "Tap only as deep as the plate:", "  nothing may stick out below it."]
    fig.text(0.70, 0.82, "What each hole is", fontsize=9.5, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.70, 0.78 - i * 0.034, t, fontsize=8.5, color=INK, va="top")
    foot(fig)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "plate-holes.png")

    # enclosure: floor from inside (above) and the rear end wall from outside
    bl, bw = P["box"]
    gy, gz = P["gland_yz"]
    fig = plt.figure(figsize=(12, 6.4), dpi=150)
    ax = fig.add_axes([0.03, 0.12, 0.56, 0.72]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-bl / 2, -bw / 2), bl, bw, fc="#F3F4F6", ec=INK, lw=1.2))
    pr = P["pillar"]
    for x, y in corners(2 * pr[0], 2 * pr[1]):
        ax.add_patch(plt.Circle((x, y), pr[2], fc="#E5E7EB", ec=MUT, lw=0.6))
    ax.text(pr[0], pr[1] - pr[2] - 1.5, "pillar", ha="center", va="top", fontsize=6.5, color=MUT)
    ax.plot([-bl / 2, bl / 2], [0, 0], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax.plot([0, 0], [-bw / 2, bw / 2], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    fl = [(x, y, 4.5) for x, y in corners(sx, sy)] + [(ix - dx, iy, 3.5), (ix + dx, iy, 3.5)]
    for x, y, d in fl:
        ax.add_patch(plt.Circle((x, y), d / 2, fc="white", ec=INK, lw=1))
    for x, y, d in fl[:4]:
        ax.text(x, y + (5 if y > 0 else -5), f"4.5 at {x:+g}, {y:+g}", ha="center", va="bottom" if y > 0 else "top", fontsize=7.5, color=INK)
    ax.text(0, iy - 5, f"3.5 at {-dx:g} and {dx:+g}, {iy:+g}", ha="center", va="top", fontsize=7.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.15", fc="#F3F4F6", ec="none"))
    ax.add_patch(Rectangle((-bl / 2 - 3, gy - 8), 3, 16, fc=COL["gland"], ec="none"))
    ax.add_patch(Rectangle((bl / 2, P["vent_yz"][0] - P["vent"][0] / 2), 3, P["vent"][0], fc=COL["vent"], ec="none"))
    ax.text(bl / 2 + 4, P["vent_yz"][0] + 8, "vent hole\n(end wall)", ha="left", va="bottom", fontsize=7, color=MUT)
    ax.text(-bl / 2 - 4, gy + 10, "gland hole\n(end wall)", ha="right", va="bottom", fontsize=7, color=MUT)
    ax.annotate("", xy=(bl / 2 + 2, -bw / 2 - 7), xytext=(bl / 2 - 24, -bw / 2 - 7), arrowprops=dict(arrowstyle="-|>", color=AC))
    ax.text(bl / 2 - 26, -bw / 2 - 7, "front", ha="right", va="center", fontsize=8, color=AC)
    ax.set_xlim(-bl / 2 - 22, bl / 2 + 22); ax.set_ylim(-bw / 2 - 12, bw / 2 + 6)
    ax.text(-bl / 2, bw / 2 + 3, "Floor, seen from inside (from above). x along, y across (+ is left), mm from the centre",
            fontsize=8, color=MUT, va="bottom")
    ax2 = fig.add_axes([0.63, 0.27, 0.34, 0.55]); ax2.set_aspect("equal"); ax2.set_axis_off()
    hb = P["base_h"]
    ax2.add_patch(Rectangle((-bw / 2, 0), bw, hb, fc="#F3F4F6", ec=INK, lw=1.2))
    ax2.plot([0, 0], [-2, hb + 2], color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    ax2.text(1, hb - 3, "centre", fontsize=7, color=MUT, va="top")
    xg = -gy        # seen from outside the rear end, left of the vehicle (+Y) is on the right
    ax2.add_patch(plt.Circle((xg, gz), 8.1, fc="white", ec=INK, lw=1))
    ax2.add_patch(plt.Circle((xg, gz), 11, fc="none", ec=MUT, lw=0.6, ls="--"))
    ax2.plot([xg, xg], [0, gz - 12], color=AC, lw=0.4, ls=":"); ax2.text(xg + 1.5, 4, f"{gz:g} up", fontsize=8, color=AC)
    ax2.plot([0, 0], [hb, hb + 4], color=MUT, lw=0.5); ax2.plot([xg, xg], [gz + 12, hb + 4], color=AC, lw=0.4, ls=":")
    ax2.text(xg / 2, hb + 5, f"{gy:g}", ha="center", fontsize=8, color=AC)
    ax2.text(0, -4, "Rear end wall, seen from outside. 16.2 mm hole for the M16 gland;\ndashed: the gland's outside flange. Up from the box's underside.",
             ha="center", va="top", fontsize=7.5, color=MUT)
    ax2.set_xlim(-bw / 2 - 4, bw / 2 + 4); ax2.set_ylim(-14, hb + 10)
    # front end wall, seen from outside: left of the vehicle (+Y) is on the left
    vy, vz = P["vent_yz"]
    ax3 = fig.add_axes([0.63, 0.02, 0.34, 0.2]); ax3.set_axis_off()
    ax3.text(0.0, 0.95, f"Front end wall, seen from outside: one {P['vent'][0]:g} mm hole for the M12 breather vent,", fontsize=7.5, color=MUT, va="top", transform=ax3.transAxes)
    ax3.text(0.0, 0.72, f"on the centre line ({vy:g} across), its centre {vz:g} mm up from the box's underside.", fontsize=7.5, color=MUT, va="top", transform=ax3.transAxes)
    fig.text(0.03, 0.965, "Enclosure base: drilling layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Drill the floor holes through the plate's holes with the box clamped on the plate, so they line up; then open them to size.",
             fontsize=8.5, color=MUT, va="top")
    foot(fig)
    fig.savefig(OUT / "box-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "box-holes.png")
    return res


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def joints():
    out = []
    sx, sy = P["box_screw_pitch"]
    xs, ys = sx / 2, sy / 2
    # 01 box fixing stack, cut through a standoff's axis
    b_ = (xs - 14, xs + 14, ys - 14, ys, -2, 24)
    out.append(bv.joint([
        part("Mounting plate (M4 tapped)", win(C["plate"].shape, *b_), COL["plate"]),
        part("Box floor", win(C["base"].shape, *b_), COL["base"]),
        part("Hex standoff, male end in the plate", win(C["standoffs"].shape, *b_), COL["standoffs"]),
        part("Carrier plate", win(C["carrier"].shape, *b_), COL["carrier"]),
        part("M4 x 6 screw", win(C["carrier_screws"].shape, *b_), COL["screw"])],
        OUT / "joint-01.png", "Joint 1: box fixing stack (cut through one standoff)",
        subtitle="The standoff clamps the box floor to the plate; the carrier screws into its top", elev=14, azim=70, size=(8, 6)))
    # 02 IMU on the floor, cut through the screw axis
    ix, iy = P["imu_xy"]
    b_ = (ix - 14, ix + 14, iy - 14, iy, -2, 18)
    out.append(bv.joint([
        part("Mounting plate (M3 tapped)", win(C["plate"].shape, *b_), COL["plate"]),
        part("Box floor", win(C["base"].shape, *b_), COL["base"]),
        part("IMU breakout", win(C["imu"].shape, *b_), COL["imu"]),
        part("M3 x 8 screw", win(C["imu_screws"].shape, *b_), COL["screw"]),
        part("Carrier plate (window edge)", win(C["carrier"].shape, *b_), COL["carrier"])],
        OUT / "joint-02.png", "Joint 2: IMU clamped to the plate (cut through both screws)",
        subtitle="Two M3 screws pass through the box floor into the plate; the carrier's window leaves it clear",
        elev=16, azim=70, size=(8, 6)))
    # 03 gland through the rear end wall, cut on its axis
    gy, gz = P["gland_yz"]
    zg = P["plate"][2] + gz
    b_ = (-90, -40, gy - 25, gy, 0, 46)
    out.append(bv.joint([
        part("Box end wall", win(C["base"].shape, *b_), "#CBD5E1"),
        part("Gland body, locknut inside", win(C["gland"].shape, *b_), COL["gland"]),
        part("Fused lead", win(C["lead"].shape, *b_), "#78716C"),
        part("Carrier plate", win(C["carrier"].shape, *b_), COL["carrier"]),
        part("Mounting plate", win(C["plate"].shape, *b_), COL["plate"])],
        OUT / "joint-03.png", "Joint 3: cable gland in the rear end wall (cut on its axis)",
        subtitle=f"Seal outside, locknut inside; the carrier stops 4.5 mm short of the nut. Gland centre {zg - P['plate'][2]:g} mm up",
        elev=14, azim=-62, size=(8, 6)))
    # 04 lid screw into a corner pillar, cut on the screw axis
    px, py, pr = P["pillar"]
    b_ = (px - 15, px + 6, py - 15, py, 30, 64)
    out.append(bv.joint([
        part("Base corner pillar", win(C["base"].shape, *b_), COL["base"]),
        part("Lid with its pillar", win(C["lid"].shape, *b_), COL["lid"]),
        part("Lid screw", win(C["lid_screws"].shape, *b_), COL["screw"])],
        OUT / "joint-04.png", "Joint 4: lid screw into a corner pillar (cut on the screw)",
        subtitle="The lid gasket seals the joint; the screws come with the box", elev=14, azim=70, size=(8, 6)))
    # 05 GNSS under the lid
    gx, gy2 = P["gnss_xy"]
    b_ = (gx - 22, gx + 22, gy2 - 22, gy2, 42, 62)
    out.append(bv.joint([
        part("Lid (top and wall)", win(C["lid"].shape, *b_), COL["lid"]),
        part("Foam tape pad, 1 mm", win(C["tape"].shape, *b_), "#E5E7EB"),
        part("GNSS module, antenna up", win(C["gnss"].shape, *b_), COL["gnss"])],
        OUT / "joint-05.png", "Joint 5: GNSS module under the lid (cut through its centre)",
        subtitle="A 22 x 22 mm pad of acrylic foam tape holds it flat against the inside of the lid top",
        elev=-10, azim=-75, size=(8, 6)))
    # 06 M6 bolt beside the box, on the bench board
    hx, hy = P["hole_pitch"]
    b_ = (hx / 2 - 22, hx / 2 + 10, hy / 2 - 18, hy / 2, -30, 40)
    out.append(bv.joint([
        part("Bench board (stands in for the vehicle floor)", win(bench_board(), *b_), COL["board"]),
        part("Mounting plate", win(C["plate"].shape, *b_), COL["plate"]),
        part("Box end wall", win(C["base"].shape, *b_), COL["base"]),
        part("M6 bolt and washer", win(C["fixings"].shape + m6_through(), *b_), COL["bolt"])],
        OUT / "joint-06.png", "Joint 6: M6 corner bolt beside the box (cut through the bolt)",
        subtitle="4 mm between washer and box wall: use a ring spanner on the head, nyloc nut underneath",
        elev=10, azim=-80, size=(8, 6)))
    # 07 light pipe in the lid, cut on its axis
    lx, ly = P["light_pipe_xy"][0]
    b_ = (lx - 7, lx + 5.5, ly - 12, ly, 36, 62)
    out.append(bv.joint([
        part("Lid top", win(C["lid"].shape, *b_), COL["lid"]),
        part("Light pipe, flange and O-ring outside", win(C["light_pipes"].shape, *b_), COL["status"]),
        part("Nut inside the lid", win(C["lp_nuts"].shape, *b_), COL["screw"]),
        part("5 mm LED in the pipe's socket", win(C["leds"].shape, *b_), "#FBBF24"),
        part("LED lead to the controller", win(C["led_wires"].shape, *b_), "#B91C1C")],
        OUT / "joint-07.png", "Joint 7: status light pipe in the lid (cut on its axis)",
        subtitle="Sealed under its flange outside, nut inside; the LED plugs into the back of the pipe",
        elev=14, azim=70, size=(8, 6)))
    # 08 breather vent in the front end wall, cut on its axis
    vy, vz = P["vent_yz"]
    bl = P["box"][0]
    b_ = (bl / 2 - 16, bl / 2 + 12, vy - 16, vy, 2, 46)
    out.append(bv.joint([
        part("Box front end wall (light grey)", win(C["base"].shape, *b_), "#CBD5E1"),
        part("Breather vent (dark): cap outside, nut inside", win(C["vent"].shape, *b_), COL["vent"]),
        part("DC-DC converter (nearest module)", win(C["converter"].shape, *b_), COL["conv"]),
        part("Carrier plate", win(C["carrier"].shape, *b_), COL["carrier"])],
        OUT / "joint-08.png", "Joint 8: breather vent in the front end wall (cut on its axis)",
        subtitle=f"Cap and O-ring outside, locknut inside; the nut stays 8.5 mm clear of the converter. Centre {vz:g} mm up",
        elev=10, azim=-82, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    st(1, [M["base"]], [mv(M["gland"], (-70, 0, 0)), mv(M["vent"], (60, 0, 0))], "cable gland and breather vent into the end walls",
       "Gland in the rear wall, vent in the front wall: seals outside, locknuts inside. Leave the gland's dome nut loose for now",
       elev=22, azim=-120, label_done=True)
    st(2, [M["plate"]], [mv(part("Enclosure base with gland and vent", S("base", "gland", "vent"), COL["base"]), (0, 0, 70)),
                         mv(M["standoffs"], (0, 0, 150))], "box onto the plate with four hex standoffs",
       "Silicone ring round each floor hole underneath; standoffs through the floor into the plate, firm by hand plus a quarter turn",
       elev=28, azim=-55, label_done=True)
    done2 = [M["plate"], part("Enclosure base", S("base", "gland", "vent", "standoffs"), COL["base"])]
    st(3, done2, [mv(M["imu"], (0, 0, 70))], "IMU onto the box floor",
       "Arrow on the board pointing forward; two M3 x 8 screws through the floor into the plate, snug",
       elev=45, azim=-55, label_done=False)
    st(4, [part("Carrier plate", C["carrier"].shape, COL["carrier"])],
       [mv(M["mstand"], (0, 0, 25)), mv(M["conv"], (0, 0, 70)), mv(M["cap"], (0, 0, 55)), mv(M["ctrl"], (0, 0, 70))],
       "modules onto the carrier plate (on the bench)",
       "Nylon standoffs screwed up from below; modules on top with M3 screws; supercapacitor tied through its slots",
       elev=35, azim=-55, label_done=False)
    done3 = done2 + [M["imu"]]
    carrier_set = part("Carrier with modules", S("carrier", "module_standoffs", "converter", "supercap", "controller", "sd", "carrier_screws"), COL["carrier"])
    st(5, done3, [mv(carrier_set, (0, 0, 90))], "carrier into the box",
       "Feed the IMU lead up through the window; four M4 x 6 screws into the standoff tops",
       elev=35, azim=-55, label_done=False)
    inside = part("Carrier with modules", S("carrier", "module_standoffs", "converter", "supercap", "controller", "sd", "carrier_screws"), COL["carrier"])
    st(6, done3 + [inside], [mv(M["lead"], (-90, 0, 0))], "fused lead through the gland and wired",
       "Through the gland to the converter's input terminals; tighten the dome nut on the lead",
       elev=28, azim=-140, label_done=False)
    st(7, [part("Lid", S("lid", "lid_screws"), COL["lid"])],
       [mv(part("Light pipes", C["light_pipes"].shape, COL["status"]), (0, 0, 35)),
        mv(part("Nuts and LEDs, from inside", S("lp_nuts", "leds"), COL["screw"]), (0, 0, -35)),
        mv(M["label"], (0, 0, 25))],
       "light pipes and nameplate onto the lid",
       "Pipes in from outside, O-rings under the flanges, nuts inside; LEDs into the pipes' sockets; label arrow forward",
       elev=30, azim=-55, label_done=True)
    lid_flip = part("Lid with light pipes, upside down", S("lid", "lid_screws", "light_pipes", "lp_nuts", "leds", "label"), COL["lid"])
    st(8, [lid_flip], [mv(part("GNSS module on its foam tape", S("gnss", "tape"), COL["gnss"]), (0, 0, -45))],
       "GNSS module under the lid", "Seen from below. Clean the lid with isopropyl alcohol; press the module on for 30 s, antenna toward the lid",
       elev=-40, azim=-55, label_done=True)
    done7 = done3 + [inside, M["lead"]]
    st(9, done7, [mv(part("Lid with light pipes, LEDs and GNSS module", S("lid", "lid_screws", "gnss", "tape", "light_pipes", "lp_nuts", "leds", "led_wires", "label"), COL["lid"]), (0, 0, 70))], "close the lid",
       "Plug the GNSS and light pipe leads into the controller; gasket clean, no wire across it; four lid screws in a cross pattern",
       elev=25, azim=-55, label_done=False)
    closed = done7 + [part("Lid", S("lid", "light_pipes", "label"), COL["lid"])]
    st(10, closed, [mv(part("M6 bolts and washers, from above", C["fixings"].shape + m6_shanks(), COL["bolt"]), (0, 0, 60)),
                   mv(part("Washers and nyloc nuts, from below", m6_nuts(), COL["screw"]), (0, 0, -45))],
       "onto the bench board for the first checks",
       "Four M6 bolts through plate and board, nyloc nuts underneath; ring spanner on the heads",
       context=[part("Bench board", bench_board(), COL["board"])], elev=12, azim=-55, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "PotholeLog prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper wire; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((25, 12), 92, 49, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(26.5, 59.8, "Inside the box", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    blk(2, 40, 15, 15, "Vehicle fuse box", "ignition-switched\ncircuit, fuse tap\nwith 2 A fuse", "#374151")
    blk(30, 40, 16, 15, "DC-DC converter", "9 to 60 V in,\n5 V out; TVS and\nreverse diode", "#2563EB")
    blk(52, 44, 14, 11, "Blocking diode", "Schottky, on\nthe 5 V output", "#7C3AED")
    blk(52, 24, 16, 13, "Supercapacitor", "1 F 5.5 V; 10 ohm\ncharge resistor with\na diode across it", "#7C3AED")
    blk(74, 36, 18, 19, "Controller", "ESP32-S3 board,\nmicroSD card in its\nslot, 5 V in,\n3.3 V out", "#065F46")
    blk(99, 44, 16, 11, "GNSS module", "under the lid;\nplug-in lead", "#D4A017")
    blk(99, 24, 16, 13, "IMU breakout", "on the box floor,\nunder the carrier\nwindow", "#C2410C")
    blk(28, 18, 18, 11, "Supply sense", "two resistors,\n10 k and 20 k", "#6B7280")
    blk(99, 13, 16, 8.5, "Status LEDs (2)", "in the lid's light pipes", "#059669")
    # power path
    wire([(17, 47.5), (30, 47.5)], RED); lab(17.8, 52.6, "2 m lead, 0.75 mm²,\nthrough the gland", RED)
    wire([(17, 43), (30, 43)], BLK); lab(17.8, 41, "ground core", BLK)
    wire([(46, 49.5), (52, 49.5)], RED); lab(49, 52.5, "5 V, 0.5 mm²", RED, "center")
    wire([(66, 49.5), (74, 49.5)], RED); lab(70, 52.5, "0.5 mm²", RED, "center")
    wire([(70, 49.5), (70, 37)], RED); lab(70.6, 40.5, "hold-up\nnode", RED)
    wire([(68, 30.5), (70, 30.5), (70, 37)], RED)
    wire([(38, 40), (38, 29)], GRY, 1.2); lab(38.6, 34.5, "from the 5 V output,\nbefore the diode", GRY)
    wire([(46, 21), (78, 21), (78, 36)], GRY, 1.2); lab(52, 18.8, "to a controller input pin, 0.25 mm²", GRY)
    # signals
    wire([(92, 50), (99, 50)], BLU); lab(95.5, 57.3, "3.3 V, GND, TX, RX,\nPPS; 0.25 mm²", BLU, "center")
    wire([(92, 40), (95, 40), (95, 30.5), (99, 30.5)], BLU); lab(94.4, 32.5, "I2C, 3.3 V,\nGND; 0.25 mm²", BLU, "right")
    wire([(88, 36), (88, 17), (99, 17)], BLU); lab(93.5, 20, "2 outputs,\nGND; 0.25 mm²", BLU, "center")
    ax.text(27, 9.6, "Safety: wire the lead with the vehicle battery isolated, or to a bench supply with a 2 A fuse. Do not short the supercapacitor's terminals.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(27, 6.2, "Red: power. Black: ground. Blue: signal. Grey: sensing. The controller starts a clean shutdown when the supply sense stays low for about 2 s.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
