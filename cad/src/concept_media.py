"""PotholeLog concept media (TRL 3, constructable design PHL-DDR-003), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the logger parts from cad/src/model.py (PARAMS), adds a grey context scene (road with a
pothole, wheel, axle, suspension and a floor section) for scale, and renders the media set with
.kit/concept.py. Parts are colored and numbered to match bom/bom.csv. Figures on the sheet and in
the flow diagram come from docs/04-calcs/sizing.py (PHL-CAL-001). Not for fabrication.

Coordinates in mm. X points forward along the vehicle, Y across it, Z up; the vehicle floor is
at Z = 0 and the road surface 1150 mm below it. The logger is a small box bolted to the vehicle
floor above the rear axle, so the hero render uses the grey context scene instead of the 1.75 m
person.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import PARAMS as P, build_parts  # noqa: E402


def cut_at_imu_plane(parts, keep="+Y"):
    """Like concept.cutaway_parts, but cut on the plane Y = IMU center, so the IMU on the box
    floor shows in section (the kit cuts at the mean Y of the parts, about 10 mm behind the IMU,
    which removes it). The kit is unchanged."""
    big = 4000.0
    cutter = Pos(0, P["imu_xy"][1] + big / 2, 0) * Box(big, big, big)
    out = []
    for p in parts:
        s = p.shape & cutter
        if s.volume > 1e-6:
            out.append(Part(p.name, s, p.color, p.bom, p.explode, p.alpha))
    return out


concept.cutaway_parts = cut_at_imu_plane

# The logger is modeled at the origin (the kit's cutaway cutter is centered at Z = 0); the grey
# context scene is shifted instead so the floor top meets the plate. Floor top is 1150 mm above
# the road; the logger sits above the axle, inboard of the wheel.
FLOOR_Z = 1150.0

m = build_parts()
parts = [
    Part("Mounting plate, aluminum", m["plate"], "#9CA3AF", 1, (0, 0, 0)),
    Part("Enclosure base, IP65", m["base"], "#374151", 2, (0, 0, 45)),
    Part("Enclosure lid with gasket", m["lid"], "#14B8A6", 3, (0, 0, 270)),
    Part("DC-DC converter and protection", m["converter"], "#2563EB", 4, (40, 0, 120)),
    Part("Hold-up supercapacitor", m["supercap"], "#7C3AED", 5, (0, 30, 150)),
    Part("Controller, Wi-Fi, microSD slot", m["controller"], "#065F46", 6, (-40, 0, 150)),
    Part("6-axis IMU", m["imu"], "#C2410C", 7, (0, -190, 60)),
    Part("GNSS module and patch antenna", m["gnss"], "#D4A017", 8, (0, 0, 205)),
    Part("Cable gland and fused lead", m["lead"], "#1F2937", 9, (-45, 0, 45)),
    Part("microSD card, 32 GB", m["sd"], "#DC2626", 10, (-110, 0, 150)),
    Part("M6 bolts, washers, locking nuts", m["fixings"], "#6B7280", 11, (0, 0, 20)),
    Part("Module carrier plate", m["carrier"], "#94A3B8", 12, (0, 0, 95)),
    Part("Hex standoffs, screws, foam tape", m["kit"], "#111827", 13, (0, 0, 75)),
    Part("Status light pipes and LEDs", m["status"], "#34D399", 14, (0, 0, 335)),
    Part("Breather vent, M12", m["vent"], "#AEB4BC", 15, (70, 0, 45)),
    Part("Nameplate label", m["label"], "#0F766E", 16, (0, 0, 290)),
]

# ---------------- grey context: road with a pothole, wheel, axle, suspension, floor ----------------
# Scene coordinates put the logger at Y = 0; CTX then drops the scene so the floor top is at Z = 0.
GREY = "#C8CDD3"
TYRE_R, TYRE_W = 520.0, 290.0      # bus or truck tyre, about 1.04 m diameter
WHEEL_Y = 480.0                    # wheel outboard (far side from the viewer), logger inboard
road = Pos(150, 180, -60) * Box(1700, 1250, 120)
pothole = Pos(640, WHEEL_Y, -35) * (Cylinder(200, 70) + Pos(110, -40, 0) * Cylinder(130, 70))
road = road - pothole
tyre = Pos(0, WHEEL_Y, TYRE_R) * Rot(90, 0, 0) * (Cylinder(TYRE_R, TYRE_W) - Cylinder(300, TYRE_W + 2))
rim = Pos(0, WHEEL_Y, TYRE_R) * Rot(90, 0, 0) * Cylinder(300, TYRE_W - 60)
axle = Pos(0, 110, TYRE_R) * Rot(90, 0, 0) * Cylinder(55, 740)
spring_h = FLOOR_Z - 20 - (TYRE_R + 55)
springs = Pos(0, -160, TYRE_R + 55 + spring_h / 2) * Box(150, 110, spring_h) \
    + Pos(0, 250, TYRE_R + 55 + spring_h / 2) * Box(150, 110, spring_h)
floor = Pos(0, 170, FLOOR_Z - 10) * Box(900, 1100, 20)
CTX = Pos(0, 0, -FLOOR_Z)
context = [Part("Road with pothole", CTX * road, "#A8AEB6"),
           Part("Wheel, axle, suspension and floor section", CTX * (tyre + rim + axle + springs + floor), GREY)]

render_all(
    parts, project="PotholeLog", title="Fleet road roughness logger concept", dwg_no="PHL-DWG-010",
    key_figures=["Acceleration 400 Hz, GNSS 10 Hz with PPS",
                 "100 m roughness segments plus pothole events",
                 "Box 120 x 90 x 55 mm on a 160 x 110 mm plate; 0.44 kg",
                 "0.54 W from a 12 or 24 V supply (60 V-rated input); 7 s hold-up",
                 "$77.50 in parts (indicative); value-engineering target $75"],
    date="2026-10-02", scale_figure=False, context=context,
    cut_exclude=("Cable gland and fused lead", "M6 bolts, washers, locking nuts"),
    flow={"title": "data flow (values from PHL-CAL-001; road data only, no images or audio)", "unit": "",
          "stages": [("Road surface", "potholes, roughness"),
                     ("Wheel, suspension", "filter the input"),
                     ("Logger on floor", "5.2 kB/s raw to card"),
                     ("On-board summary", "100 m segments"),
                     ("Depot Wi-Fi upload", "112 kB/day, about 8 s"),
                     ("Open road map", "CSV, GeoJSON")]},
)
