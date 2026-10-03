---
doc_id: PHL-DEC-001
title: PotholeLog design decisions register
project: PotholeLog
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Amish approved the recommendations for all nine open decisions on 2026-10-02 (PHL-DDR-003 A1 to A3 accepted); moved to decisions made; value engineering notes the effect of the light pipes and vent'
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Design for construction (PHL-DDR-003, Tables 1 and 2) accepted by Amish on 2026-10-02; the 2026-10-01 row no longer says open for review"
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Value engineering: the light pipes and LEDs, breather vent and nameplate label are now BOM lines 14 to 16; estimate USD 77.50, USD 2.50 over the target"
  - version: "0.5"
    date: '2026-10-03'
    author: Amish Chadha
    change: "Amish accepted the cost overrun against the value-engineering target on 2026-10-03; row added to decisions made; value engineering section updated"
---

# PotholeLog design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

Value-engineering target: USD 75 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 77.50 (USD 2.50 over the target). Main cost drivers and savings worth trying:

Amish accepted this overrun on 2026-10-03: the estimated cost of USD 77.50 against the USD 75 target (USD 2.50 over), accepting the USD 2.50 overrun on R15. Amish: "Cost over target - i accept all the cost variations and overruns". It stays reported against the target as an accepted overrun, and the savings below remain worth trying.

- The largest lines are the GNSS module (USD 15), the controller (USD 10), the 60 V converter with its protection (USD 9) and the enclosure (USD 8); the plate, IMU and memory card are USD 6 each.
- Making the design constructable added the carrier plate (USD 2.00) and the box fixing kit (USD 1.50) and moved USD 0.50 of hardware out of line 11: from USD 71.00 to USD 74.00.
- Adopted on 2026-10-02 and now in the BOM: the two status light pipes with their LEDs and lead (line 14, USD 1.00), the breather vent (line 15, USD 2.00) and the nameplate label (line 16, USD 0.50). Together they take the estimate from USD 74.00 to USD 77.50, USD 2.50 over the target.
- Savings worth trying: cut the plate and carrier from offcuts; a 16 GB card still holds about 66 to 80 days of raw data against the 30 days needed (about USD 2 less), which with offcut plates would close most of the gap; GNSS modules of the same class vary widely in price; buying the standoffs, screws and lead parts in packs lowers the per-unit hardware cost.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: bicycles a later variant; depot Wi-Fi first; floor mount above the rear axle; ESP32-S3; LSM6DSO and M10 classes; 100 m segments in CSV and GeoJSON; publish road-level results only | Amish: "i accept all your recommendations, go with them across all repos." | PHL-DDR-001, PHL-DDR-002 |
| 2026-09-25 | N1: a 60 V-rated converter, with `budget_usd` raised from $70 to $75 | Amish, same instruction | PHL-DDR-002 |
| 2026-09-25 | N2: R5 defect-detection range 10 to 30 km/h with repeat slow passes; 300 mm reference defect kept | Amish, same instruction | PHL-DDR-002 |
| 2026-10-01 | Design for construction: hex standoffs, carrier plate, module layout, gland locknut, IMU screwed into the plate, GNSS on foam tape, modelled lid pillars | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("fix the design assumptions to match and be physically feasible as you draw the illustrations"); the changes themselves were accepted on 2026-10-02 (below) | PHL-DDR-003 |
| 2026-10-02 | First pilot partner (first candidate to approach): a Dallas-Fort Worth area city with its own bus or refuse fleet, with TxDOT pavement management roughness data on state roads in that city as the reference IRI sections | Amish: "i approve your recommendations for all 555 open decisions." | PHL-DDR-001, O1; PHL-DDR-002 |
| 2026-10-02 | Clear lid window over the GNSS antenna shown in the renders only (option a); the build keeps the opaque lid | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 1 |
| 2026-10-02 | Two sealed status light pipes in the lid, for power and logging, adopted (option a); the two lid holes are sealed like the others | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 2 |
| 2026-10-02 | Pressure-equalizing breather vent on the front end wall adopted (option a) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 3 |
| 2026-10-02 | Printed nameplate label with a forward arrow adopted (option a) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 4 |
| 2026-10-02 | Segment files to CityTwin: CityTwin fetches the daily segment files from the operator's server (option a, matching CityTwin's outbound pull, CTW-DDR-001 D11); a date per segment may be published but never pass times, and only once at least two vehicles or several days are pooled | Amish: "i approve your recommendations for all 555 open decisions." | PHL-DDR-002, cross-repo actions |
| 2026-10-02 | Floor holes sealed with a ring of neutral-cure silicone round each hole for the prototype (option a), spray-tested at TRL 4 before a pilot; the foam gasket is the fallback if the spray test leaks | Amish: "i approve your recommendations for all 555 open decisions." | PHL-DDR-003, A1 |
| 2026-10-02 | GNSS module held by acrylic foam tape (option a), with adhesion checked after the TRL 4 heat soak; the printed clip is the fallback if the tape lets go | Amish: "i approve your recommendations for all 555 open decisions." | PHL-DDR-003, A2 |
| 2026-10-02 | Keep the 160 mm plate and bolt the logger down as a unit with a ring spanner for the prototype (option a); review after a TRL 4 trial fitting | Amish: "i approve your recommendations for all 555 open decisions." | PHL-DDR-003, A3; PHL-CAL-001 [I4] |
| 2026-10-02 | Design for construction accepted: the changes in Tables 1 and 2 (P1 to P7 and their knock-on changes), as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [PHL-DDR-003](decisions/0003-design-for-construction.md), Tables 1 and 2 |
| 2026-10-03 | Cost overrun accepted: the estimated cost of USD 77.50 against the USD 75 target (USD 2.50 over), accepting the USD 2.50 overrun on R15 | Amish: "Cost over target - i accept all the cost variations and overruns" | [REVIEW.md](REVIEW.md), session 2026-10-03 |
