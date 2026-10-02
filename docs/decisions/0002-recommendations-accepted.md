---
doc_id: PHL-DDR-002
title: PotholeLog recommendations accepted
project: PotholeLog
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'O1 (first pilot partner) and the CityTwin ingest path decided by Amish on 2026-10-02'
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Items D1 to D7, N1 and N2 are "Decided by Amish, 2026-09-25: go with recommendation". Item O1 was decided by Amish on 2026-10-02 (PHL-DEC-001).

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item in `docs/REVIEW.md` and PHL-DDR-001 that was awaiting him and carried a recommendation is therefore decided as recommended. Where a recommendation offered several options, the recommended option is the decision. Items with no recommendation stay open. TRL 4 remains on hold by Amish's instruction, so nothing here authorizes building, testing or purchasing.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Bicycles in the pitch | Keep the pitch; a bicycle variant (own battery, handlebar or seat-post mount) is a later step | Status wording only; R16 already served buses and refuse trucks; pitch unchanged |
| D2 | Upload route | Depot Wi-Fi first; LTE-M cellular as an optional add-on, costed separately | Status wording only |
| D3 | Mount location | Sprung-mass floor mount above the rear axle | Status wording only |
| D4 | Controller | ESP32-S3 board with Wi-Fi and microSD slot | Status wording in PHL-PRC-001 and `bom/bom.csv` |
| D5 | IMU and GNSS classes | LSM6DSO-class IMU and u-blox M10-class GNSS, to confirm against datasheets | Status wording in `bom/bom.csv` |
| D6 | Segment length and output format | 100 m segments plus point events, in CSV and GeoJSON following the CityTwin open data export | Status wording only; CityTwin ingest path listed as a cross-repo action |
| D7 | Privacy rule | Publish only road-segment roughness and defect clusters; tracks and timestamps stay with the operator; no driver scoring | Status wording in PHL-PRB-001 |
| N1 | Converter input for 24 V vehicles (R9) | Option (a): a 60 V-rated converter, with `budget_usd` raised to $75 | `bom/bom.csv` item 4 from 9 to 36 V at $7.00 to 9 to 60 V at $9.00; parts cost $69.00 to $71.00; `budget_usd` $70 to $75 (margin $1.00 to $4.00); R15 target $70 to $75; R9 from not met to at risk (1.9 V margin over the TVS clamp, TVS pulse energy unverified); PHL-DWG-001 supply note, Rev P1 to P2; blueprint key figures; PHL-CAL-001 F4, F5, J1, J2 |
| N2 | Defect-detection target (R1, R5) | Option (b): limit the R5 defect-detection range to 10 to 30 km/h and rely on repeat slow passes near stops and junctions, keeping the 300 mm reference defect | R5 target restated in PHL-REQ-001 (was 10 to 80 km/h); R5 from not met to at risk (lowest margin 1.94 on IRI 2 and 0.97 at 30 km/h on IRI 4; new line K2 in PHL-CAL-001); PHL-PRC-001 and PHL-PRB-001 updated |

No design change altered geometry: the 60 V converter keeps the 40 x 30 x 14 mm envelope in `cad/src/model.py`. STEP, STL, the drawing and the concept media were regenerated.

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First pilot partner and city, and who provides reference IRI | No recommendation was made then. Decided by Amish, 2026-10-02 (PHL-DEC-001): first candidate to approach a Dallas-Fort Worth area city with its own bus or refuse fleet, with TxDOT pavement management roughness data on state roads in that city as the reference IRI sections |

## Cross-repo actions

- **CityTwin ingest path (D6, R14).** CityTwin's gateway accepts no inbound connections, and PotholeLog uploads to the fleet operator's server. The two repos must agree whether CityTwin fetches the operator's daily segment files or the operator passes them on by another route, and confirm that a daily publication date is compatible with R13. Recorded here; CityTwin is not edited. Decided 2026-10-02 (PHL-DEC-001): CityTwin fetches the daily segment files from the operator's server (option a, matching CityTwin's outbound pull, CTW-DDR-001 D11); a date per segment may be published but never pass times, and only once at least two vehicles or several days are pooled.

## Consequences

- Requirement status (PHL-CAL-001 v0.2): 0 not met, 6 at risk (R1, R4, R5, R9, R11, R12), 2 not verifiable at TRL 3 (R2, R3), 4 met on paper (R7, R8, R10, R15), 4 met by design (R6, R13, R14, R16). Before: 2 not met, 4 at risk.
- Decided but on hold because they are TRL 4 work: a bench test of the TVS and converter against ISO 16750-2 load dump pulses (N1), and field data on slow-pass detection rates (N2).
- `trl: 3` and `trl_target: 3` are unchanged.
- PHL-PRB-001, PHL-PRC-001 and PHL-REQ-001 are revised to v0.4; PHL-CAL-001 and PHL-DDR-001 to v0.2.
