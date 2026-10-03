---
doc_id: PHL-DDR-003
title: PotholeLog design for construction
project: PotholeLog
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'A1 to A3 accepted by Amish on 2026-10-02 as recommended; Tables 1 and 2 still open for review'
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Tables 1 and 2 accepted by Amish on 2026-10-02"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This covers the changes P1 to P7 in Table 1 and the knock-on changes in Table 2, made under Amish's 2026-09-30 instruction to make the design physically buildable, and is recorded in the design decisions register (PHL-DEC-001). The questions in Table 3 (A1 to A3) were accepted by Amish as recommended earlier the same day: "i approve your recommendations for all 555 open decisions." They are recorded in the register too.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of PHL-DDR-002 showed what PotholeLog does, but checking it with build123d (overlaps, contacts and clearances between every pair of parts) found modules that overlapped one another or a fixing, parts with no fixing at all, and stock-box features that were not modelled and would have clashed.

The changes keep what the logger does: the same 160 x 110 x 4 mm plate and M6 pattern, the same 120 x 90 x 55 mm stock box, the same modules and electrical design, the IMU on the box floor on the centre line, the GNSS under the plastic lid, the gland and lead on the rear end wall, and the same mounting place on the vehicle floor. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 48 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must not touch are apart by at least the stated clearance, and nothing reaches below the plate's underside. All 48 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The box was held by four M4 screws through its floor on a 100 x 70 mm pattern. Two of the screw heads lay under the converter, which sat directly on the floor, and all four fell where a stock box has its moulded corner pillars for the lid screws. | The box is held by four M4 male-female hex standoffs (7 mm across flats, 8 mm body, 6 mm male thread) on an 80 x 40 mm pattern. The male end passes through a 4.5 mm hole in the floor into an M4 tapped hole in the plate and clamps the floor down; a ring of neutral-cure silicone round each hole under the floor seals it. | One part both holds the box down and carries the modules (P2). The 6 mm thread stops 0.5 mm short of the plate's underside, so the plate still sits flat. The new pattern is clear of the corner pillars, the IMU and the gland. |
| P2 | The converter, supercapacitor and controller had no fixings: the converter and supercapacitor stood on the floor, and the controller on a "standoff rail" that was not a part. | A module carrier plate (92 x 76 x 1.5 mm aluminium, new BOM line 12) sits on the four hex standoffs, 8 mm above the floor, held by four M4 x 6 screws. The converter and controller stand on 6 mm M3 nylon standoffs on it; the supercapacitor stands on it, held by a cable tie through two slots. A 30 x 30 mm window over the IMU leaves the IMU and its lead clear. | Bought modules are made to be screwed to a plate on standoffs. A flat aluminium sheet is cut and drilled with the same tools as the mounting plate. The carrier stays 1.5 mm clear of the walls and pillars and 4.5 mm clear of the gland locknut. |
| P3 | The supercapacitor overlapped the controller by 0.5 mm, and the controller's end touched the inside of the end wall where the gland's locknut goes. | The converter is turned 90 degrees (30 x 40 mm footprint) and placed at the front left; the controller moved 19 mm forward, onto the carrier, at the rear left; the supercapacitor sits at the front right, beside the window. Every module is at least 2 mm from the next and 7.5 mm or more from the gland locknut. | The box size is unchanged; only the layout inside it moved. |
| P4 | The gland was a cylinder against the outside of the end wall, with no hole and no locknut inside. | A 16.2 mm hole in the rear end wall, 10 mm left of centre and 20 mm up from the box's underside (where the concept had the gland); the M16 gland body outside with its seal, and its locknut inside. | This is how a gland is fitted; the locknut needs the inside room that P3 makes. |
| P5 | The IMU was "screwed to the box floor" with no fixing shown; a screw into 2.5 mm of plastic alone would hold poorly and let the floor flex under the sensor. | Two M3 x 8 screws pass through the IMU board and 3.5 mm holes in the box floor into M3 tapped holes in the plate, clamping the board, floor and plate together. Silicone seals the two floor holes. | The IMU stays on the box floor, on the centre line, where the concept put it, and is now clamped to the aluminium plate the vehicle shakes, which keeps the measurement path stiff. The screws stop 0.1 mm short of the plate's underside. |
| P6 | The GNSS module floated under the lid with no fixing. | A 22 x 22 mm pad of 1 mm acrylic foam tape holds it under the lid top, antenna up; a plug-in lead joins it to the controller so the lid can be set aside. | No hole in the lid, so the seal and the sky view through the plastic lid are unchanged. |
| P7 | The stock box's corner pillars and lid screws were not modelled. | Four moulded corner pillars in the base and lid and four lid screws are modelled as on a stock IP65 box; every part inside is checked clear of them. | They exist on the box that will be bought, and they set where the box fixings and carrier can go. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Plate | Hole pattern: four M4 tapped holes on 80 x 40 mm (were on 100 x 70 mm) and two new M3 tapped holes 14 mm apart for the IMU. Size, thickness and M6 pattern unchanged. | P1, P5 |
| Mass | Logger 0.43 kg (was 0.37 kg); 0.57 kg with the lead and fixings (was 0.51 kg) [H2]. | Carrier 24 g, standoffs, screws and tape 21 g, and the box's pillars. |
| Plate stiffness | First mode 168 Hz (was 186 Hz) on the conservative half-width model [I1]; R12's 150 Hz is still met on paper. | More mass rides on the plate. |
| Crash loads | 21 N per M6 bolt (was 18 N) and 46 N on the four hex standoffs (was 34 N on the box screws) at 20 g [H3]. | Mass. |
| Cost | BOM line 12 (carrier, $2.00) and line 13 (box fixing kit, $1.50) added; line 11 repriced from $3.00 to $2.50 because its M4 screws and M3 standoffs moved to line 13. Estimated cost $74.00, $1.00 under the unchanged $75 value-engineering target (`budget_usd`) [J1]. | Parts added for construction. |
| Drawing | PHL-DWG-001 Rev P3; making sketches PHL-DWG-101 to 103 added. | Follows the model. |
| Documents | PHL-CAL-001 v0.3, PHL-PRC-001 v0.5, PHL-REQ-001 v0.5: mass, stiffness, crash and cost figures; R15 restated against the value-engineering target. No requirement changed status. | Follows the model. |
| Unchanged | Power, hold-up, storage, upload, detection, location and self-heating results; overall height 59 mm; box and plate size. | No change touches them. |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | How the four standoff holes and two IMU holes in the box floor are sealed against the plate. | (a) a ring of neutral-cure silicone round each hole under the floor, as modelled; (b) a 1 mm closed-cell foam gasket sheet between the box and the plate. | (a) for the prototype; spray-test at TRL 4 before choosing for a pilot. Accepted 2026-10-02; the foam gasket is the fallback if the spray test leaks. |
| A2 | The GNSS module is held by foam tape, which ages in a hot cabin. | (a) acrylic foam tape, as modelled; (b) a small printed clip screwed to two lid pillars. | (a); check adhesion after the TRL 4 heat soak. Accepted 2026-10-02; the printed clip is the fallback if the tape lets go. |
| A3 | Spanner room at the M6 bolts is 4 mm between washer and box wall (2 mm for a 10 mm socket), so the logger is bolted down as a unit with a ring spanner. | (a) keep the plate and use a ring spanner, as planned; (b) lengthen the plate to 180 mm with the M6 holes 160 mm apart, for socket room (plate mass and first mode change). | (a) for the prototype; review after a TRL 4 trial fitting. Accepted 2026-10-02 (a longer plate would lower the 168 Hz first mode toward R12's 150 Hz limit). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan PHL-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: 0 not met, 6 at risk, 2 not verifiable at TRL 3, 4 met on paper, 4 met by design (PHL-CAL-001 v0.3).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept's internal layout (converter beside the controller on the floor, no carrier plate). The outside of the logger is unchanged, so the hero render is still true; the exploded and detail renders need updating on Amish's Mac, where Blender is.
- With A1 to A3 accepted, the build plan stands as written: silicone rings round the floor holes, the GNSS module on foam tape and the logger bolted down as a unit with a ring spanner.
- The enclosure, converter, controller, IMU and GNSS parts are chosen at TRL 4; their sizes and hole positions must be checked then, and the carrier holes marked from the parts bought.
