# Review note: PotholeLog

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (PHL-PRB-001 v0.2): problem with cited figures (FHWA, DfT, WHO), users and context, prior work (Pothole Patrol, World Bank response-type roughness meters, smartphone apps), constraints, out of scope, safety pointer; co-design checklist kept.
- `docs/03-requirements.md` (PHL-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, status against the concept, verification route and assumptions.
- `docs/02-concept.md` (PHL-PRC-001 v0.2): how it works, numbered components, first-order numbers with assumptions, design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the logger (plate, IP65 box and lid, converter, supercapacitor, controller, IMU, GNSS, cable gland and lead), each part with a BOM number. Because the logger is small, the hero uses a grey context scene (road with a pothole, wheel, axle, suspension and floor section) instead of the 1.75 m figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` (callouts 1 to 9), `cutaway.png`, `flow.png` (data flow, estimates labeled). All images were inspected; temporary `media/_views*` folders were removed.
- `bom/bom.csv`: 11 lines with indicative prices, rows 1 to 9 matching the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, where it could be used (by industry and by region), what sparked the idea, and updated concept, components and safety sections.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still match the cited figures.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Sampling | 400 Hz acceleration (about 35 mm spacing at 50 km/h), 10 Hz GNSS | R6 met by design |
| Raw storage | about 190 MB a day; about 5 months on 32 GB | R7 met by design |
| Upload | about 0.1 MB of summaries a day over depot Wi-Fi | R8 met by design; no real-time data |
| Power | about 0.7 W, about 60 mA at 12 V | R9 met by design |
| Hold-up after power loss | about 9 s (1 F supercapacitor) | R10 met by design |
| Size and mass | 120 x 90 x 59 mm box on a 160 x 110 mm plate; about 0.4 kg | |
| Parts cost | about $69 against a $70 budget | R15 met, $1 margin |

Requirements not met or at risk:

- **R16 not met for bicycles.** The pitch names bikes, but this concept needs vehicle power and a rigid floor.
- **R1, R2 and R3 unverified.** Detection rate, false reports and correlation with IRI need field data and reference sections.
- **R4 at risk** in dense urban streets, where GNSS error can be large.
- **R5 partly met.** Segments driven below 20 km/h give no roughness value on that pass.
- **R9 transient immunity, R11 temperature and vibration, and R12 install time and plate stiffness are unverified.**
- **R15 margin is thin.** Any cellular option would exceed the $70 budget.

### Proposed, awaiting Amish

1. **Bicycles in the pitch.** Options: (a) keep the pitch and treat a bicycle variant (own battery, handlebar or seat-post mount) as a later step; (b) drop bikes from the pitch; (c) design both now. Recommendation: (a). `project.yaml` is unchanged.
2. **Upload route.** Options: depot Wi-Fi (in budget, next-day data) or LTE-M cellular (about $20 to $30 more per unit plus a data plan, same-day data, over budget). Recommendation: depot Wi-Fi first, with cellular as an optional add-on costed separately. No budget change is proposed.
3. **Mount location.** Sprung-mass floor mount above the rear axle (recommended) or an axle mount (stronger signal, harsher environment).
4. **Controller.** ESP32-S3 (recommended), an RP2040 board with Wi-Fi, or an nRF52 board.
5. **IMU and GNSS classes.** LSM6DSO-class IMU and u-blox M10-class GNSS (recommended), to be confirmed against datasheets at TRL 3.
6. **Segment length and output format.** 100 m segments plus point events, in CSV and GeoJSON following the CityTwin open data export (recommended).
7. **Privacy rule.** Publish only road-segment roughness and defect clusters; keep vehicle tracks and timestamps on the operator's server; no driver scoring (recommended, and should be agreed with any fleet partner and its drivers).
8. **First pilot partner.** A city road department with a bus or refuse fleet that can provide reference IRI sections; the Helpful Engineering network could help find one.

### Safety concerns

- Mounting on passenger vehicles: a loose box is a projectile hazard; through-bolting at existing fixings only.
- Vehicle electrics: fused, ignition-switched supply; a short on a 24 V system can cause a fire. Transient immunity is unverified.
- Working under or around vehicles during installation.
- Driver distraction: no controls or display.
- Location data can reveal drivers' movements; this is the main non-physical risk and needs a data agreement with the operator.
- Outputs are not a certified survey and must not drive contract acceptance or safety decisions without validation.

### Problems and notes

- The kit's cutaway cutter is centered at Z = 0, so the logger is modeled at the origin and the context scene is shifted down to meet it. This does not affect the media.
- In the hero render the logger is small relative to the wheel and floor, which is the true scale; the exploded view and cutaway show it clearly.
- WebSearch was unavailable. Sources were verified by fetching pages directly. Figures that could not be verified (for example AAA pothole damage costs, the UK ALARM survey and India pothole death counts) were left out.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the sampling, power, hold-up and plate stiffness by calculation, define the roughness metric and calibration method, and produce the parametric model and drawing sheet.
