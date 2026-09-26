---
doc_id: PHL-REQ-001
title: PotholeLog requirements
project: PotholeLog
doc_type: Requirements
version: "0.2"
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
---

# PotholeLog requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish, and will be checked by calculation at TRL 3 and by field data later. The status column gives the concept's position today: "met by design" means the chosen parts and architecture meet the target on paper; "unverified" means only data from a vehicle can show it.

Table 1. Requirements.

| ID | Requirement | Target | Status at TRL 2 | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Detect potholes and severe defects in the wheel path | 80 % or more of defects at least 50 mm deep and 300 mm long found within 3 passes | Unverified | Detection model on logged data against a surveyed defect list |
| R2 | Keep false reports low | 10 % or fewer of reported defect clusters (2 or more passes) are not real defects | Unverified; Pothole Patrol reported over 90 % real after clustering | Field check of reported clusters |
| R3 | Report roughness per road segment | One roughness value per 100 m segment per pass, calibrated per vehicle to an IRI estimate; r² of 0.8 or better against reference IRI on calibration sections | Unverified; needs reference sections from a partner | Calibration runs following World Bank Technical Paper 46 |
| R4 | Locate defects | Defect cluster within 10 m of its true position (95 %) and on the correct street | At risk in dense urban canyons | GNSS logs against surveyed points |
| R5 | Work across normal fleet speeds | Roughness valid from 20 to 80 km/h; defect detection from 10 to 80 km/h | Partly met; segments driven below 20 km/h give no roughness value | Speed-banded calibration |
| R6 | Sample fast enough | 3-axis acceleration at 400 Hz or more, range ±8 g or more; GNSS position at 5 Hz or more | Met by design (400 Hz, ±16 g, 10 Hz GNSS) | Datasheets and firmware configuration |
| R7 | Store data on the vehicle | 30 days or more of raw data and summaries without upload | Met by design (about 5 months on 32 GB, estimate) | Storage calculation |
| R8 | Get data off the vehicle | Summaries uploaded automatically within 24 h, with no driver or staff action | Met by design (depot Wi-Fi); real-time upload not provided | Design review |
| R9 | Run from vehicle power | 9 to 36 V DC input (12 V and 24 V systems); reverse-polarity protected; transient levels of ISO 16750-2 as a target; under 1 W running; no draw with ignition off | Met by design except transient levels, which are unverified | Power budget; later bench test |
| R10 | Shut down cleanly | Files closed without corruption when power is cut at any time | Met by design (about 9 s hold-up, estimate) | Hold-up calculation |
| R11 | Survive the vehicle environment | Operating -20 to +70 °C; enclosure IP65; no loosening under vehicle vibration | Enclosure met by design; temperature and vibration unverified | Component ratings; later vibration test |
| R12 | Install quickly and safely | 30 min or less by a fleet mechanic; no cutting or welding of structural members; bracket first natural frequency above 150 Hz | Install time and bracket stiffness unverified | Design review; TRL 3 calculation of plate stiffness |
| R13 | Protect privacy | No camera or microphone; published data limited to road-segment roughness and defect locations, with no vehicle tracks, timestamps or driver identity; no driver scoring | Met by design | Design review; data schema review |
| R14 | Open outputs | CSV and GeoJSON outputs that CityTwin and common GIS tools can read | Met by design (format proposed, awaiting Amish) | Sample export |
| R15 | Low cost and buildable | Parts $70 or less per unit; off-the-shelf modules; no custom PCB | Met, with $1 margin (about $69, indicative) | Priced BOM |
| R16 | Fit the fleet types in the pitch | Buses and refuse trucks; bicycles | **Not met for bicycles**: the concept needs vehicle power and a rigid floor; a bicycle needs its own battery and mount | Design review |

## Requirements not met or at risk

- **R16 (bicycles) not met.** The concept runs from vehicle power. A bicycle variant needs a battery, a charger and a rider-independent mount, and cyclist body motion would need its own calibration. Proposed, awaiting Amish: treat bicycles as a later variant.
- **R3 and R1 unverified.** Both depend on field data and a calibration partner with reference IRI sections.
- **R4 at risk.** Single-frequency GNSS in streets lined with tall buildings can be several meters to tens of meters off. Clustering over many passes helps, but this is unproven.
- **R5 partly met.** Stop-and-go traffic leaves some segments without a roughness value on a given pass.
- **R15 margin is thin.** Any cellular option (about $20 to $30 more for a module, plus a data plan) would exceed the $70 budget.

## Assumptions

- Host vehicles run about 200 km a day (estimate for an urban bus or refuse truck) and return to a depot with Wi-Fi each night.
- The logger is mounted on the sprung mass (floor or body structure), not the axle; the suspension filters the input, which calibration corrects.
- 100 m segments match common practice for network roughness reporting; defects are reported as point events.
- A partner agency can provide reference IRI on a few calibration sections, or allow a rod-and-level survey of them.
