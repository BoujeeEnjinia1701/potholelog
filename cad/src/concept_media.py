"""PotholeLog concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X points forward along the vehicle, Y across it, Z up; the vehicle floor is
at Z = 0 and the road surface 1150 mm below it. The logger is a small box bolted to the vehicle floor above the rear axle, so the hero
render uses a grey context scene (road with a pothole, wheel, axle, suspension and a floor
section) instead of the 1.75 m person.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

# ---------------- logger, local frame: origin at the floor surface, box centered on it ----------------
BOX_L, BOX_W = 120.0, 90.0       # stock IP65 box footprint, X by Y
BASE_H, LID_H, WALL = 43.0, 12.0, 2.5
PLATE_L, PLATE_W, PLATE_T = 160.0, 110.0, 4.0

# The logger is modeled at the origin (the kit's cutaway cutter is centered at Z = 0); the grey
# context scene is shifted instead so the floor top meets the plate. Floor top is 1150 mm above
# the road; the logger sits above the axle, inboard of the wheel.
FLOOR_Z = 1150.0


def at(shape):
    """Logger parts stay in the local frame."""
    return shape


def hollow_box(l, w, h, wall, open_top=True):
    outer = Box(l, w, h)
    inner = Pos(0, 0, wall if open_top else -wall) * Box(l - 2 * wall, w - 2 * wall, h)
    return outer - inner


z0 = PLATE_T                                       # plate sits on the floor, box sits on the plate
plate = Pos(0, 0, PLATE_T / 2) * Box(PLATE_L, PLATE_W, PLATE_T)
base = Pos(0, 0, z0 + BASE_H / 2) * hollow_box(BOX_L, BOX_W, BASE_H, WALL, open_top=True)
lid = Pos(0, 0, z0 + BASE_H + LID_H / 2) * hollow_box(BOX_L, BOX_W, LID_H, WALL, open_top=False)
fl = z0 + WALL                                     # inside floor of the box
imu = Pos(0, -5, fl + 2.0) * Box(20, 20, 4)
controller = Pos(-31, 22, fl + 10.0) * Box(52, 26, 9) + Pos(-31, 22, fl + 2.75) * Box(40, 6, 5.5)   # board on a standoff rail
power = Pos(31, 22, fl + 7.0) * Box(40, 30, 14)
supercap = Pos(2.5, 24, fl + 10.0) * Cylinder(8, 20)
gnss = Pos(-25, 20, z0 + BASE_H + LID_H - WALL - 4.0) * Box(28, 28, 8)                   # under the lid top
gland = Pos(-BOX_L / 2 - 9, 10, z0 + 20) * Rot(0, 90, 0) * Cylinder(10, 18)
lead = Pos(-BOX_L / 2 - 18 - 75, 10, 3.5) * Rot(0, 90, 0) * Cylinder(3.5, 150) \
    + Pos(-BOX_L / 2 - 20, 10, (3.5 + z0 + 20) / 2) * Cylinder(3.5, z0 + 20 - 3.5)
cable = gland + lead

parts = [
    Part("Mounting plate, aluminum", at(plate), "#9CA3AF", 1, (0, 0, 0)),
    Part("Enclosure base, IP65", at(base), "#374151", 2, (0, 0, 45)),
    Part("Enclosure lid with gasket", at(lid), "#14B8A6", 3, (0, 0, 270)),
    Part("DC-DC converter and protection", at(power), "#2563EB", 4, (0, 0, 120)),
    Part("Hold-up supercapacitor", at(supercap), "#7C3AED", 5, (0, 0, 140)),
    Part("Controller, Wi-Fi, microSD", at(controller), "#065F46", 6, (0, 0, 160)),
    Part("6-axis IMU", at(imu), "#C2410C", 7, (0, 0, 90)),
    Part("GNSS module and patch antenna", at(gnss), "#D4A017", 8, (0, 0, 175)),
    Part("Cable gland and fused lead", at(cable), "#1F2937", 9, (-40, 0, 45)),
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
    key_figures=["3-axis acceleration at 400 Hz, GNSS at 10 Hz",
                 "100 m roughness segments plus pothole events",
                 "Box about 120 x 90 x 59 mm, about 0.4 kg (estimate)",
                 "About 0.7 W from a 12 or 24 V supply (estimate)",
                 "About $69 in parts (indicative)"],
    date="2026-09-25", scale_figure=False, context=context, cut_exclude=("Cable gland and fused lead",),
    flow={"title": "data flow (estimates; road data only, no images or audio)", "unit": "",
          "stages": [("Road surface", "potholes, roughness"),
                     ("Wheel, suspension", "filter the input"),
                     ("Logger on floor", "400 Hz accel + GNSS"),
                     ("On-board summary", "100 m segments"),
                     ("Depot Wi-Fi upload", "0.1 MB/day (est.)"),
                     ("Open road map", "CSV, GeoJSON")]},
)
