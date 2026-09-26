---
doc_id: PHL-REQ-001
title: PotholeLog requirements
project: PotholeLog
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from PHL-CAL-001; R16 redefined per PHL-DDR-001 (D1); R8, R13 and R14 rest on adopted choices
---

# PotholeLog requirements

These requirements are checked by calculation in PHL-CAL-001 v0.1. Targets are unchanged from v0.2 except R16, which is redefined for this build under PHL-DDR-001 (D1, adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review). The status column gives the result on paper: "met on paper" means a calculation shows the target is met under the stated assumptions; "met by design" means the chosen parts and architecture meet it; "not verifiable at TRL 3" means only data from a vehicle can show it.

Table 1. Requirements.

| ID | Requirement | Target | Status at TRL 3 (PHL-CAL-001) | Verification (later) |
| --- | --- | --- | --- | --- |
| R1 | Detect potholes and severe defects in the wheel path | 80 % or more of defects at least 50 mm deep and 300 mm long found within 3 passes | At risk: a bus tyre drops only 22 mm into a 300 mm pothole; detectable up to about 20 km/h on IRI 4 roads and 50 km/h on IRI 2 roads | Detection model on logged data against a surveyed defect list |
| R2 | Keep false reports low | 10 % or fewer of reported defect clusters (2 or more passes) are not real defects | Not verifiable at TRL 3; Pothole Patrol reported over 90 % real after clustering | Field check of reported clusters |
| R3 | Report roughness per road segment | One roughness value per 100 m segment per pass, calibrated per vehicle to an IRI estimate; r² of 0.8 or better against reference IRI on calibration sections | Not verifiable at TRL 3; synthetic calibration gives r² 0.93 from one pass and 0.99 from five | Calibration runs following World Bank Technical Paper 46 |
| R4 | Locate defects | Defect cluster within 10 m of its true position (95 %) and on the correct street | At risk: 2.3 m suburban, 18.2 m in dense urban streets (10-pass cluster) | GNSS logs against surveyed points |
| R5 | Work across normal fleet speeds | Roughness valid from 20 to 80 km/h; defect detection from 10 to 80 km/h | **Not met** for defect detection at 30 km/h and above on fair roads; roughness signal is 12 times sensor noise at 20 km/h | Speed-banded calibration |
| R6 | Sample fast enough | 3-axis acceleration at 400 Hz or more, range ±8 g or more; GNSS position at 5 Hz or more | Met by design (400 Hz, ±16 g, 10 Hz GNSS with PPS; floor peak 0.14 g) | Datasheets and firmware configuration |
| R7 | Store data on the vehicle | 30 days or more of raw data and summaries without upload | Met on paper (133 to 160 days on 32 GB) | Storage calculation |
| R8 | Get data off the vehicle | Summaries uploaded automatically within 24 h, with no driver or staff action | Met on paper for vehicles in daily service (112 kB in about 8 s over depot Wi-Fi, with the ignition on) | Design review |
| R9 | Run from vehicle power | 9 to 36 V DC input (12 V and 24 V systems); reverse-polarity protected; transient levels of ISO 16750-2 as a target; under 1 W running; no draw with ignition off | **Not met** for transients on 24 V vehicles (58 V suppressed load dump against a 36 V converter); running power 0.54 W met | Power budget; later bench test |
| R10 | Shut down cleanly | Files closed without corruption when power is cut at any time | Met on paper (7.0 s hold-up at end of life; 1 s needed) | Hold-up calculation |
| R11 | Survive the vehicle environment | Operating -20 to +70 °C; enclosure IP65; no loosening under vehicle vibration | At risk: about 72 °C inside at +70 °C needs 85 °C part grades; vibration not verifiable | Component ratings; later vibration test |
| R12 | Install quickly and safely | 30 min or less by a fleet mechanic; no cutting or welding of structural members; bracket first natural frequency above 150 Hz | At risk: 30 min task estimate at the limit; plate first mode 186 Hz met on paper | Design review |
| R13 | Protect privacy | No camera or microphone; published data limited to road-segment roughness and defect locations, with no vehicle tracks, timestamps or driver identity; no driver scoring | Met by design (privacy rule D7) | Design review; data schema review |
| R14 | Open outputs | CSV and GeoJSON outputs that CityTwin and common GIS tools can read | Met by design (format D6); the CityTwin ingest path is still open | Sample export |
| R15 | Low cost and buildable | Parts $70 or less per unit; off-the-shelf modules; no custom PCB | Met on paper ($69.00, $1 margin) | Priced BOM |
| R16 | Fit the fleet types in this build | Buses and refuse trucks; a bicycle variant is deferred to a later step (PHL-DDR-001, D1) | Met by design for buses and refuse trucks; bicycles are not served by this build | Design review |

## Requirements not met or at risk

- **R5 not met.** The R1 reference pothole is largely bridged by a bus tyre, so its floor signal falls below ordinary road vibration at 30 km/h and above on fair roads (PHL-CAL-001, section C). Longer potholes (600 mm) are detectable at all speeds. Options are in `docs/REVIEW.md`, awaiting Amish; the target is unchanged.
- **R9 not met for transients.** A 24 V suppressed load dump (58 V) exceeds the 36 V converter input. A 60 V converter, about $2 more, is proposed and awaiting Amish because it would take the cost to $71.
- **R1 at risk.** Detection depends on passes at low speed; only field data can show whether 80 % within 3 passes is reached.
- **R4 at risk** in dense urban streets, where GNSS errors repeat between passes.
- **R11 and R12 at risk.** Part temperature grades, vibration loosening and the 30 min installation are all at their limits.
- **R2 and R3 not verifiable at TRL 3.** Both need field data and a calibration partner with reference IRI sections.
- **R15 margin is thin.** The converter fix or any cellular option would exceed the $70 budget.
- **Bicycles.** The pitch still names bikes, but this build serves buses and refuse trucks only (R16 as redefined).

## Assumptions

- Host vehicles run about 200 km a day (estimate for an urban bus or refuse truck), return to a depot with Wi-Fi each night and spend at least about 10 s with the ignition on within its coverage.
- The logger is mounted on the sprung mass (floor or body structure), not the axle; the suspension filters the input, which calibration corrects.
- 100 m segments match common practice for network roughness reporting; defects are reported as point events.
- A partner agency can provide reference IRI on a few calibration sections, or allow a rod-and-level survey of them.
