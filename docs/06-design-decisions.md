---
doc_id: PHL-DEC-001
title: PotholeLog design decisions register
project: PotholeLog
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# PotholeLog design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | First pilot partner and city, and who provides reference IRI sections | A city road department with a bus or refuse fleet; the Helpful Engineering network could help find one | None yet | Not the bench build; needed before any vehicle fitting | PHL-DDR-001, O1; PHL-DDR-002 |
| 2 | Clear window in the lid over the GNSS antenna (shown in the product renders) | (a) renders only; (b) choose a stock box with a clear lid | Keep it for the renders only, or (b) if a visible antenna is wanted; reception is fine through either | Lid part (BOM line 2) | REVIEW 2026-09-26, item 1 |
| 3 | Two status light pipes (power and logging) in the lid | (a) adopt; (b) leave out | (a): a driver can see the logger is running, for well under $1 | Two holes in the lid, two LEDs and wires; a lid change to the build plan | REVIEW 2026-09-26, item 2 |
| 4 | Pressure-equalising breather vent on the front end wall | (a) adopt, about $2 to $3; (b) leave out | (a), to limit condensation in a sealed box that heats and cools daily; it would take the estimated cost about $1 to $2 over the value-engineering target | One more hole in the box and one bought part | REVIEW 2026-09-26, item 3 |
| 5 | Nameplate label with a forward arrow | (a) adopt as a printed label; (b) leave out | (a): it tells the installer which way the IMU axes face | A label on the lid; no change to the parts inside | REVIEW 2026-09-26, item 4 |
| 6 | How CityTwin receives the operator's daily segment files, and whether a daily publication date fits R13 | (a) CityTwin fetches from the operator's server; (b) the operator passes them on by another route | None yet; to agree with CityTwin | Not the build; data path only | PHL-DDR-002, cross-repo actions |
| 7 | How the six floor holes are sealed against the plate | (a) a ring of neutral-cure silicone round each hole, as planned; (b) a 1 mm closed-cell foam gasket sheet between box and plate | (a) for the prototype; spray-test at TRL 4 before choosing for a pilot | Step 2 of the build plan | PHL-DDR-003, A1 |
| 8 | How the GNSS module is held under the lid | (a) acrylic foam tape, as planned; (b) a small printed clip screwed to two lid pillars | (a); check adhesion after the TRL 4 heat soak | Step 7 of the build plan | PHL-DDR-003, A2 |
| 9 | Spanner room at the M6 corner bolts (4 mm washer to box; 2 mm for a 10 mm socket) | (a) keep the plate and bolt the logger down as a unit with a ring spanner, as planned; (b) lengthen the plate to 180 mm with the M6 holes 160 mm apart | (a) for the prototype; review after a TRL 4 trial fitting | Mounting plate and step 9 | PHL-DDR-003, A3; PHL-CAL-001 [I4] |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The box: 120 x 90 x 55 mm outside, 2.5 mm walls, a flat floor and four moulded corner pillars about 10 mm across | The standoff pattern, carrier size and clearances are set by them | PHL-DDR-003, P1, P7 |
| 2 | The converter's size (about 30 x 40 mm) and its four mounting holes; its 60 V input rating on the datasheet | The carrier's module holes are marked from it; safety stop S3 | PHL-DDR-003, P2; PHL-DDR-002, N1 |
| 3 | The ESP32-S3 board is no larger than about 52 x 26 mm and its microSD slot can be reached with the lid off | Many ESP32-S3 boards are longer; a longer board needs the layout rechecked | PHL-DDR-003, P3 |
| 4 | The IMU breakout: about 20 x 20 mm, two mounting holes, a side-entry plug, and the noise figure the calculations assume | The floor and plate IMU holes and the 3.4 mm clearance under the carrier | PHL-DDR-003, P5; PHL-CAL-001 |
| 5 | The GNSS module: no larger than 28 x 28 mm, a timing-pulse output, and a plug-in lead long enough to set the lid aside | The lid layout and the wiring | PHL-DDR-003, P6 |
| 6 | The hex standoffs' male thread is 6 mm or shorter | A longer thread would stick out under the plate | PHL-DDR-003, P1 |
| 7 | The M6 bolt length for the vehicle's floor or crossmember | It depends on the structure at the chosen fixing points | PHL-PRC-001 |

## Value engineering

Value-engineering target: USD 75 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 74.00 (USD 1.00 under the target). Main cost drivers and savings worth trying:

- The largest lines are the GNSS module (USD 15), the controller (USD 10), the 60 V converter with its protection (USD 9) and the enclosure (USD 8); the plate, IMU and memory card are USD 6 each.
- Making the design constructable added the carrier plate (USD 2.00) and the box fixing kit (USD 1.50) and moved USD 0.50 of hardware out of line 11: from USD 71.00 to USD 74.00.
- Savings worth trying: cut the plate and carrier from offcuts; a 16 GB card still holds about 66 to 80 days of raw data against the 30 days needed (about USD 2 less); GNSS modules of the same class vary widely in price; buying the standoffs, screws and lead parts in packs lowers the per-unit hardware cost.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: bicycles a later variant; depot Wi-Fi first; floor mount above the rear axle; ESP32-S3; LSM6DSO and M10 classes; 100 m segments in CSV and GeoJSON; publish road-level results only | Amish: "i accept all your recommendations, go with them across all repos." | PHL-DDR-001, PHL-DDR-002 |
| 2026-09-25 | N1: a 60 V-rated converter, with `budget_usd` raised from $70 to $75 | Amish, same instruction | PHL-DDR-002 |
| 2026-09-25 | N2: R5 defect-detection range 10 to 30 km/h with repeat slow passes; 300 mm reference defect kept | Amish, same instruction | PHL-DDR-002 |
| 2026-10-01 | Design for construction: hex standoffs, carrier plate, module layout, gland locknut, IMU screwed into the plate, GNSS on foam tape, modelled lid pillars | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("fix the design assumptions to match and be physically feasible as you draw the illustrations"); open for his review | PHL-DDR-003 |
