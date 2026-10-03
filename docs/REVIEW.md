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

Update 2026-09-25: items 1 to 7 are now "Decided by Amish, 2026-09-25: go with recommendation" (PHL-DDR-001, PHL-DDR-002). Item 8 stays "Proposed, awaiting Amish".

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

## Session 2026-09-25: TRL 3

Amish asked on 2026-09-25 for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so each item with a recommendation is adopted as recommended for TRL 3 under that instruction and remains open for his review. This session ran `/advance-trl3` and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (PHL-DDR-001 v0.1, status proposed): items D1 to D7 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; O1 (first pilot partner and city) left as "Proposed, awaiting Amish".
- `docs/04-calcs/01-sizing.md` (PHL-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: a quarter-car model of a bus rear corner on ISO 8608 road profiles with golden-car IRI; roughness signal, noise, speed and load effects and a synthetic calibration; pothole detection with tyre enveloping; location error; storage, upload, power, transients and hold-up; self-heating, mass and fixings; plate stiffness and installation time; cost. The script imports the model's parameters and part volumes and reads the BOM and `project.yaml`; every number in the note is printed by it (runs in about 10 s).
- `cad/src/model.py`: parametric build123d model (plate with hole patterns, stock enclosure base and lid, converter, supercapacitor, controller with microSD card, IMU on the box floor, GNSS under the lid, gland and lead stub, M6 fixings). Exports `cad/step/` and `cad/stl/` for `potholelog-assembly`, `mounting-plate` and `enclosure`.
- `cad/src/sheets.py` and `cad/drawings/PHL-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:2, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". PHL-DWG-001 was free because the concept blueprint is PHL-DWG-010.
- `bom/bom.csv` (11 lines, all priced with a supplier or supplier type, $69.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. The exploded view now has callouts 1 to 11 matching the BOM. Temporary `media/_views*` folders were removed.
- PHL-PRB-001, PHL-PRC-001 and PHL-REQ-001 revised to v0.3; `README.md` (TRL 3, key numbers, links) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design details specified by the calculations, within the adopted choices: GNSS with a PPS output to time-stamp IMU samples; uploads run with the ignition on (the hold-up cannot power Wi-Fi); shutdown starts only after about 2 s of low input so cranking dips are ridden through; front and rear axle impacts are paired; part grades of 85 °C for the controller module and card and 70 °C or more for the supercapacitor; the plate is bolted down before the box is fitted, because socket clearance is about 2 mm. The TRL 2 power estimate falls from 0.7 W to 0.54 W.

### Requirement status (PHL-CAL-001, Table 5)

2 not met, 4 at risk, 2 not verifiable at TRL 3, 4 met on paper, 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R5 Speed range | **Not met** | Reference pothole (50 x 300 mm) margin 0.97 at 30 km/h, 0.54 at 50 km/h and 0.30 at 80 km/h on an IRI 4 road; a bus tyre drops only 22 mm into it |
| R9 Vehicle power | **Not met** (transients) | 24 V suppressed load dump 58 V against a 36 V converter; running power 0.54 W is met |
| R1 Detection | At risk | Margin above 1 up to about 20 km/h (IRI 4) and 50 km/h (IRI 2); 93 % of passes hit the pothole |
| R4 Location | At risk | 95 % radius 2.3 m suburban, 18.2 m dense urban after 10 passes |
| R11 Environment | At risk | About 72 °C inside at +70 °C; part grades and vibration loosening |
| R12 Installation | At risk | 30 min task estimate at the limit; plate mode 186 Hz met |
| R2, R3 | Not verifiable at TRL 3 | Synthetic calibration r² 0.93 from one pass, 0.99 from five |
| R7, R8, R10, R15 | Met on paper | 133 to 160 days on 32 GB; 112 kB uploaded in about 8 s; 7.0 s hold-up; $69.00 of $70 |
| R6, R13, R14, R16 | Met by design | 400 Hz, ±16 g, peak 0.14 g; privacy rule; CSV and GeoJSON; buses and refuse trucks |

Key numbers: 5.23 kB/s raw; 0.37 kg (0.51 kg with lead and fixings); load changes the roughness signal by ±7 % with air suspension and up to 22 % with steel springs.

### Decisions recorded (PHL-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation (previously adopted as recommended for TRL 3, open for his review): D1 keep the pitch and treat bicycles as a later variant (R16 redefined to buses and refuse trucks for this build); D2 depot Wi-Fi first, cellular as a separately costed add-on; D3 floor mount above the rear axle; D4 ESP32-S3; D5 LSM6DSO-class IMU and M10-class GNSS; D6 100 m segments and point events in CSV and GeoJSON after the CityTwin export; D7 publish road-level results only, no driver scoring. No new budget and no pitch or problem rewording were recommended, so `budget_usd` stays at $70 and the pitch still names bikes.

### Still awaiting Amish

Update 2026-09-25: items 2 and 3 are now "Decided by Amish, 2026-09-25: go with recommendation" (PHL-DDR-002, N1 and N2). Item 1 stays "Proposed, awaiting Amish".

1. **O1, first pilot partner and city.** No partner, city or preference was named at TRL 2; none is chosen here.
2. **New, converter input for 24 V vehicles (R9).** Options: (a) a 60 V-rated converter, about $2 more, $71.00 in parts, $1 over budget; (b) keep the 36 V part and limit the build to 12 V vehicles, which excludes most buses; (c) add a surge-stopper front end, more robust and more costly. Recommendation: (a), with `budget_usd` raised to about $75 to restore a small margin. Not applied: the BOM still carries the 36 V part and `budget_usd` is unchanged at $70.
3. **New, defect-detection target (R1, R5).** Options: (a) keep the targets and accept R5 as not met; (b) limit the R5 defect-detection range to 10 to 30 km/h and rely on repeat slow passes near stops and junctions; (c) change the R1 reference defect to one at least 600 mm long, which is detectable at all speeds (margin 1.67 at 80 km/h on IRI 4). Recommendation: (b), keeping the 300 mm reference, because it matches how buses drive in town. Not applied.

Suggestions only, not in the repo: map matching to street centerlines for R4 in dense streets; a load flag for steel-sprung refuse trucks; testing the gyroscope's roll rate as a second detection channel for one-sided potholes.

### Cross-repo consistency

- PotholeLog uses no FieldNode, CellGuard, MotionCore, ThermaCart or CalRig component. It relates to TwinKit only through CityTwin's open data export (D6).
- CityTwin's review (session 2026-09-25, /populate) lists the PotholeLog upload path as undefined (its R1 at risk) and recommends one-way publishing, with the gateway accepting no inbound connections. PotholeLog uploads to the fleet operator's server, so CityTwin would need to fetch the operator's daily segment files, or the operator would pass them on by another route. This is not a conflict, but the path must be agreed between the two repos; no change was made to CityTwin.
- CityTwin plans to publish PotholeLog data "per road segment and per day". PotholeLog's R13 excludes timestamps from published data. A publication date for a daily aggregate is compatible with R13 as long as pass times are not published; to confirm when the interface is agreed.

### Safety concerns

- The 36 V converter in the BOM is not rated for a 24 V load dump. Until item 2 is decided it must not be fitted to a 24 V vehicle; the precis and README say so.
- A loose box is a projectile: crash loads are small (18 N per M6 bolt at 20 g), but loosening under years of vibration is untested. Locking nuts and bolting to structure, not thin floor panels, stay mandatory.
- False reassurance: small potholes can be missed at speed (R5), so a clean map is not proof of a sound road. Outputs remain uncertified and must not drive contract acceptance or safety decisions.
- Location data can reveal drivers' movements; the privacy rule (D7) still needs agreement with the fleet partner and its drivers.
- Working under and around vehicles and on vehicle electrics during installation, as at TRL 2.

### Gaps and notes

- The quarter-car model is linear, uses a rigid tyre circle and ignores pitch, roll and body flexing; ISO 8608 roads are Gaussian and lack joints and covers. The ISO 16750-2 levels, the IMU noise figure and the GNSS accuracy classes are stated as assumptions to confirm from the documents; they were not fetched this session.
- Citations: no unchecked citations remain in the docs. The figures left out at TRL 2 (AAA damage costs, the UK ALARM survey, India pothole deaths) were not re-attempted; WebSearch was unavailable.
- The kit's cutaway cuts at the mean Y of the parts, which removed the IMU; `cad/src/concept_media.py` swaps in a cut on the IMU's plane (a project-side wrapper; the kit is unchanged). The logger stays at the origin and the grey context scene is shifted, as at TRL 2.
- In the hero render the logger is small beside the wheel and floor, which is its true scale.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold only) is present, untouched and not extended. No test, build, firmware or PCB material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on items 1 to 3 above and on D1 to D7. For the record only, TRL 4 would need: a bench build of the logger; a lab test report (TST, `environment: lab`) covering IMU noise and timing against PPS, power and hold-up with power cuts, and ISO 16750-2 transients on the chosen converter; and build log entries. Drive data over surveyed defects and reference IRI sections would follow at TRL 5. None of this has been started.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25, in chat: "i accept all your recommendations, go with them across all repos." This session applied that decision at TRL 3 and recorded it in `docs/decisions/0002-recommendations-accepted.md` (PHL-DDR-002 v0.1).

### Decisions applied

Nine items are now "Decided by Amish, 2026-09-25: go with recommendation".

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D1 to D7 | Bicycles later, depot Wi-Fi, floor mount, ESP32-S3, LSM6DSO and M10 classes, 100 m segments in CSV and GeoJSON, privacy rule | Adopted as recommended for TRL 3, open for review | Decided; wording updated in PHL-DDR-001 v0.2, PHL-PRB-001, PHL-PRC-001, `bom/bom.csv`, `bom/bom-notes.md` and `README.md` |
| N1 | 60 V-rated converter; budget raised | 9 to 36 V converter, $7.00; parts $69.00; `budget_usd` $70; R9 not met | 9 to 60 V converter, $9.00; parts $71.00; `budget_usd` $75 (margin $4.00); R9 at risk (1.9 V over the 58.1 V TVS clamp; TVS pulse energy untested) |
| N2 | R5 defect-detection range restated, 300 mm reference kept | 10 to 80 km/h; not met (margin 0.30 at 80 km/h on IRI 4) | 10 to 30 km/h with repeat slow passes; at risk (lowest margin 1.94 on IRI 2, 0.97 at 30 km/h on IRI 4, 1.17 allowing 10 crossings per km) |

What changed in the repo:

- `project.yaml`: `budget_usd` 70 to 75; DDR-002 added to the TRL evidence. Pitch and problem unchanged (no rewording was recommended). `trl: 3` and `trl_target: 3` unchanged.
- `bom/bom.csv` item 4 and `bom/bom-notes.md`: 60 V converter, $71.00 total.
- `docs/03-requirements.md` (PHL-REQ-001 v0.4): R5 target and status, R9 status, R15 target ($75) and status.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (PHL-CAL-001 v0.2): converter rating 60 V in F4 and F5, cost in J1 and J2, new line K2 for the 10 to 30 km/h band; Table 5 and the summary updated. The script was re-run and the note matches its output.
- `docs/02-concept.md` (PHL-PRC-001 v0.4), `docs/01-problem.md` (PHL-PRB-001 v0.4): decisions, converter, detection band, budget and safety text.
- `cad/src/model.py`: converter comment only (same 40 x 30 x 14 mm envelope); STEP and STL re-exported.
- `cad/drawings/PHL-DWG-001`: supply note now states the 60 V converter; Rev P1 to P2.
- `cad/src/concept_media.py`: blueprint key figures ($71 of $75, 60 V-rated input); all media re-rendered and inspected; `media/_views*` removed.
- `README.md`: budget, concept numbers, components, safety, a new "What sparked the idea" (the 1982 International Road Roughness Experiment in Brasília, World Bank Technical Paper 45), and removal of the earlier text about how the idea was assembled.
- All PDFs in `docs/pdf/` rebuilt; generated files regenerated so that none shows the old personal domain.

### Requirement status (PHL-CAL-001 v0.2)

0 not met, 6 at risk, 2 not verifiable at TRL 3, 4 met on paper, 4 met by design (before: 2 not met, 4 at risk).

| ID | Status | Key number |
| --- | --- | --- |
| R5 Speed range | At risk | Defect band 10 to 30 km/h: margin 0.97 at 30 km/h on IRI 4 |
| R9 Vehicle power | At risk | 60 V converter against 58 V load dump and 58.1 V TVS clamp; TVS energy untested |
| R1 Detection | At risk | Margin above 1 up to about 20 km/h (IRI 4) and 50 km/h (IRI 2) |
| R4 Location | At risk | 18.2 m in dense urban streets (10 passes) |
| R11 Environment | At risk | About 72 °C inside at +70 °C |
| R12 Installation | At risk | 30 min at the limit |
| R2, R3 | Not verifiable at TRL 3 | Synthetic r² 0.93 (one pass), 0.99 (five) |
| R7, R8, R10, R15 | Met on paper | 133 to 160 days; 112 kB in 8 s; 7.0 s hold-up; $71.00 of $75 |
| R6, R13, R14, R16 | Met by design | 400 Hz, ±16 g; privacy rule; CSV and GeoJSON; buses and refuse trucks |

### Still awaiting Amish

1. **O1, first pilot partner and city, and who provides reference IRI.** No recommendation was made, so no choice is made here.

Suggestions only, unchanged and not decisions: map matching for R4, a load flag for steel-sprung refuse trucks, and the gyroscope roll rate as a second detection channel.

### Cross-repo actions

- **CityTwin:** agree the ingest path for PotholeLog's daily segment files (CityTwin fetches from the operator's server, or the operator passes them on), and confirm that a daily publication date is compatible with PotholeLog R13. Not edited from this repo.

### Safety

- The 60 V converter clears the 24 V load dump by only 1.9 V over the TVS clamp, and the TVS pulse energy is untested; converters rated below 60 V must not be fitted to 24 V vehicles. The precis and README say so.
- A clean map is still not proof of a sound road: small potholes are sought only on slow passes.
- Other concerns are as in the TRL 3 session.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold because they are TRL 4 work: a bench test of the converter and TVS against ISO 16750-2 load dump pulses (N1), and field data on slow-pass detection rates (N2). No build, test, firmware, PCB or purchasing work was started.

## Session 2026-09-26: sources strengthened

README "By country or region" rows without a citation were replaced or rewritten so each states only what a verified primary source supports. All kept links (FHWA HM-64, DfT, WHO, World Bank Technical Papers 45 and 46) were re-fetched and still support their claims.

| Row | Old source | New source |
| --- | --- | --- |
| India and South Asia, now India | None (uncited claims on two-wheelers and monsoon damage) | Press Information Bureau, Lok Sabha reply of 16 December 2021: pothole-related accidents 4,775 (2019) and 3,564 (2020) |
| Latin America, now Brazil | None | Confederação Nacional do Transporte, Pesquisa CNT de Rodovias 2025: pavement fair, poor or very poor on 56.5 % of 114,197 km |
| Canada and northern Europe, now Canada | None (uncited freeze-thaw claim) | Statistics Canada, Core Public Infrastructure Survey (The Daily, 24 May 2022): 13 % of roads poor or very poor in 2020 |

- What sparked the idea: the World Bank Technical Paper 45 source was kept (primary); "England" corrected to "the United Kingdom" to match the paper's list of participating countries.
- India pothole death counts were again not used; only the accident counts in the PIB release could be verified.
- No controlled document changed; `docs/01-problem.md` did not cite a weak source.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added `cad/src/product_model.py`, an appearance model for photoreal renders, and pointed the README hero at `media/render-hero.png` with a link to `media/render-exploded.png` (both produced later by the render pipeline).

What `product_model.py` adds, reusing `PARAMS`, `derived()` and `build_parts()` from `cad/src/model.py` with every main dimension and interface unchanged (plate, hole patterns, 120 x 90 x 55 mm box, module positions, gland position and lead path):

- Mounting plate with rounded corners and edge rounds; hex M6 bolt heads and washers (item 11).
- Enclosure base and lid with corner and edge fillets, a lid-to-base parting line, lid gasket, corner screw pillars and stainless lid screws, as on a stock IP65 box.
- M16 cable gland with hex body, locknut and knurled dome cap; the fused lead swept from the gland down to the floor, with a P-clip.
- Internals with credible detail: converter board with inductor, capacitors, TVS and terminal block; sleeved supercapacitor; controller PCB with ESP32-S3 module shield, USB-C, headers and microSD slot; IMU breakout with spacers and screws; GNSS PCB with ceramic patch antenna.
- Context: a compact section of painted steel vehicle floor with two crossmembers under the fixings.
- `TITLE` and three `RENDER_VIEWS`: hero (front left, with the floor), exploded (front right) and detail (front right, without the floor).

Where the appearance model differs from `model.py` (none of these change a main dimension or interface):

1. **Clear window in the lid over the GNSS patch antenna.** The BOM lid is opaque. Proposed, awaiting Amish. Recommendation: keep it for the renders only, or choose a stock box with a clear lid if Amish wants a visible antenna; GNSS reception is fine through either.
2. **Two status light pipes (power and logging) in the lid.** Not in the BOM or the firmware sketch. Proposed, awaiting Amish. Recommendation: adopt; a driver can see at a glance that the logger is running, at a cost of well under $1.
3. **Breather vent on the +X end wall.** Not in the BOM. Proposed, awaiting Amish. Recommendation: adopt a pressure-equalizing vent (about $2 to $3) to limit condensation in a sealed box that heats and cools daily; this would use about half of the $4 margin left in the $75 budget, so Amish decides.
4. **Teal nameplate with a forward arrow.** Not in the BOM. Proposed, awaiting Amish. Recommendation: adopt as a printed label; the arrow tells the installer which way the IMU axes face.
5. **Lead P-clip and floor and crossmember context.** Context only; the clip counts under item 11 hardware. No decision needed.

This is appearance only. No tolerances, fabrication detail, PCB layout or purchasing work was added. `trl` stays 3, and TRL 4 remains on hold by Amish's instruction. Previews were checked with the kit renderer; the photoreal renders are left to the orchestrator. No git commands were run in this session, by instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, constructable design and build plan

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept in a separate design decisions register. Under his 2026-09-30 instruction to make the design physically buildable ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."), this session made the PotholeLog design constructable and wrote the build plan. No git commands were run, by instruction.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- `cad/src/model.py`: constructable design with 48 build123d constructability checks (`python cad/src/model.py --check`), all passing. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (PHL-DDR-003 v0.1, Draft): every change, with the reason; three questions "Proposed, awaiting Amish" (A1 to A3).
- `bom/bom.csv`: line 12 (module carrier plate, $2.00) and line 13 (box fixing kit, $1.50) added; lines 1, 2, 4, 5, 7, 8 and 11 respecified; line 11 repriced to $2.50. Estimated cost $74.00.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (PHL-CAL-001 v0.3): mass, crash loads, plate stiffness and cost re-run; cost written against the value-engineering target.
- `docs/02-concept.md` (PHL-PRC-001 v0.5), `docs/03-requirements.md` (PHL-REQ-001 v0.5), `docs/01-problem.md` (PHL-PRB-001 v0.5): figures and value-engineering wording.
- `cad/drawings/PHL-DWG-001` Rev P3 (`cad/src/sheets.py`); concept media regenerated (`cad/src/concept_media.py`: hero, blueprint, exploded with callouts 1 to 13, cutaway, flow, model.glb).
- `cad/src/build_plan_media.py`: overview, making sketches PHL-DWG-101 (mounting plate), 102 (enclosure base drilling) and 103 (module carrier plate), plate and box hole layouts, six joint close-ups, nine assembly step pictures and a block wiring diagram. Every picture was inspected; `drawing.py --check-text` is clean.
- `docs/05-build-plan.md` (PHL-BLD-001 v0.1) and `docs/06-design-decisions.md` (PHL-DEC-001 v0.1). `project.yaml`: `design_state: constructable`, both new documents and PHL-DDR-003 in `trl_evidence`; `budget_usd` unchanged. README: links line, "Building the prototype" section, value-engineering wording.
- `cad/src/product_model.py`: one key renamed so it still builds (controller standoff height); its appearance is otherwise unchanged.

### Design changes made for construction (PHL-DDR-003)

1. The box is held to the plate by four M4 male-female hex standoffs on 80 x 40 mm, through the floor into tapped holes in the plate (was four screws on 100 x 70 mm, two of them under the converter and all four on the box's corner pillars).
2. A 92 x 76 x 1.5 mm aluminium carrier plate on the standoffs holds the converter and controller on nylon standoffs and the supercapacitor with a cable tie; a window leaves the IMU clear (the modules had no fixings).
3. The converter is turned 90 degrees and the modules rearranged so nothing overlaps (the supercapacitor overlapped the controller by 0.5 mm).
4. The gland has a 16.2 mm hole in the rear end wall and a locknut inside, with 4.5 mm or more to the carrier and modules.
5. The IMU is held by two M3 screws through the box floor into the plate, so it is clamped to the aluminium.
6. The GNSS module is held under the lid by a pad of acrylic foam tape, with a plug-in lead.
7. The stock box's corner pillars and lid screws are modelled and every part is clear of them.
8. The floor holes are sealed with a ring of neutral-cure silicone under the box.

Knock-on: logger 0.43 kg (was 0.37 kg), 0.57 kg with lead and fixings; plate first mode 168 Hz (was 186 Hz; R12's 150 Hz still met on paper); estimated cost $74.00, $1.00 under the $75 value-engineering target. Requirement status unchanged: 0 not met, 6 at risk, 2 not verifiable, 4 met on paper, 4 met by design.

### Proposed, awaiting Amish

All open items are in `docs/06-design-decisions.md`: O1 pilot partner; the four appearance items of 2026-09-26 (clear lid window, light pipes, breather vent, nameplate); the CityTwin ingest path; and PHL-DDR-003 A1 (floor hole sealing), A2 (GNSS fixing) and A3 (spanner room at the M6 bolts).

### Stale media (made on Amish's Mac)

The outside of the logger is unchanged, so `media/render-hero.png`, `media/card.png` and `media/social-preview.png` are still true. `media/render-exploded.png` and `media/render-detail.png` show the concept's internal layout (no carrier plate, converter on the floor) and are stale; `cad/src/product_model.py` needs the carrier and new layout before they are re-rendered.

### Safety

- The build plan keeps bench power to a fused, current-limited supply and leaves vehicle fitting outside the plan, with safety stops before first power, before tests above 30 V and before any vehicle fitting.
- Concerns from earlier sessions stand: the 1.9 V margin over the TVS clamp, projectile risk if bolted to thin panels, and location privacy.

### Recommended next step

Amish reviews PHL-DDR-003 and the register. TRL 4 (building to this plan and testing) remains on hold by his instruction.

## Session 2026-10-02: open-decision recommendations approved

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation for every open decision in the design decisions register. 9 decisions were recorded: each moved to Decisions made, dated 2026-10-02, with the approved recommendation and its record. trl stays 3; no build or test work was done, and the CAD model, BOM quantities and prices, and pictures were not changed.

### Documents changed

- `docs/06-design-decisions.md` (PHL-DEC-001 v0.2): the nine open decisions moved to Decisions made; Open decisions now reads none; value engineering notes the light pipes and vent take the estimate about USD 2 to 3 over the target
- `docs/decisions/0003-design-for-construction.md` (PHL-DDR-003 v0.2): A1 to A3 accepted with their fallbacks; Tables 1 and 2 stayed open for review (no register item asked for them) until Amish accepted them later on 2026-10-02 (see the next session)
- `docs/decisions/0001-trl2-review-decisions.md` (PHL-DDR-001 v0.3): O1 (first pilot partner) decided
- `docs/decisions/0002-recommendations-accepted.md` (PHL-DDR-002 v0.2): O1 decided; CityTwin ingest path decided
- `docs/03-requirements.md` (PHL-REQ-001 v0.6): R13 restated (dates published only when pooled, never pass times); R14 ingest path decided; R15 notes the cost of the light pipes and vent; no status changed
- `docs/04-calcs/01-sizing.md` (PHL-CAL-001 v0.4): requirement table wording for R13 and R14; no result changed
- `docs/02-concept.md` (PHL-PRC-001 v0.6): lid light pipes and nameplate, breather vent, clear window renders only, CityTwin path and pooled dates, first pilot partner
- `docs/01-problem.md` (PHL-PRB-001 v0.6): first pilot partner stated
- `bom/bom-notes.md`: adopted lid details and vent noted, not yet in the BOM; no quantity or price changed
- PDFs regenerated with `python3 .kit/render.py`; superseded PDF versions removed by the render.

### Follow-up actions to carry approved decisions into the design

1. Decision 3 (model): Add two sealed light pipe holes in the lid and the two status LEDs with their wires to `cad/src/model.py` and its checks
2. Decision 4 (model): Add the breather vent hole in the front end wall to `cad/src/model.py` and check its clearance to the modules
3. Decision 3 (bom): Add the light pipes and LEDs, the breather vent and the nameplate label to `bom/bom.csv` and price them
4. Decision 3 (calcs): Re-run `sizing.py` for the new total and update R15 in PHL-CAL-001 and PHL-REQ-001 (about USD 2 to 3 over the target)
5. Decision 3 (drawings): Update the general arrangement PHL-DWG-001 and the lid and box making sketches with the light pipe and vent holes
6. Decision 3 (pictures): Regenerate the build plan pictures and text for the lid, box drilling and wiring steps with the light pipes, vent and label
7. Decision 2 (pictures): Keep the clear lid window in the product renders only; check that `cad/src/product_model.py` marks it as a render detail
8. Decision 6 (docs): Agree the segment file fetch and pooled-date rule with CityTwin's item 6 so the formats match, and write the pooling rule into the server export

### Points found in the review

- There was no open item to accept PHL-DDR-003, yet the register listed it under Decisions made as "open for his review"; the recommendation was to accept. Amish accepted it later on 2026-10-02 (see the next session).
- Item 6 is already decided on the CityTwin side (CTW-DDR-001, D11, outbound pull); decide it together with CityTwin's item 6 so the formats match.
- Items 3 and 4 together take the estimate to about $2 to $3 over the $75 target; the register states only the vent's effect.

## Session 2026-10-02: design-for-construction changes accepted

Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This accepts the design-for-construction changes in Tables 1 and 2 of PHL-DDR-003 (P1 to P7 and their knock-on changes), which were left open for his review when the open decisions were decided earlier the same day. No other item is decided by it. trl stays 3; no build or test work was done, and the model, BOM, calculations and pictures are unchanged.

### Documents changed

- `docs/decisions/0003-design-for-construction.md` (PHL-DDR-003 v0.3, status Draft): status line now "accepted" with Amish's words.
- `docs/06-design-decisions.md` (PHL-DEC-001 v0.3): Decisions made row added, dated 2026-10-02; the 2026-10-01 row no longer calls the changes open for review.
- `docs/05-build-plan.md` (PHL-BLD-001 v0.2): section 2 says PHL-DDR-003 is accepted.
- PDFs regenerated.

### Recommended next step

No change: the follow-up actions of the previous session stand. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: approved follow-ups carried out

Amish, 2026-10-02: "497 follow-up actions that need CAD, drawing, picture, BOM or calculation work ... APPROVED CHANGES, COMPLETE THESE", and "Photoreal renders are out of date in most repos ... COMPLETE THESE". This session carried the decisions of 2026-10-02 into the design. trl stays 3; no build or test work was done; `budget_usd` is unchanged. No git commands were run, by instruction.

### Follow-ups (from the list of the open-decision session above)

1. Done. Light pipes and LEDs in the model: `cad/src/model.py` has two 6.4 mm sealed holes in the lid (30 mm right of centre, 40 and 30 mm toward the rear), two panel-mount light pipes with inside nuts, a 5 mm LED in each and their wire pair routed under the GNSS module to the controller (BOM line 14). Checks added for the seal, nuts, pillars, GNSS, LEDs and wire clearances.
2. Done. Breather vent in the model: a 12.2 mm hole in the front end wall on the centre line, 30 mm up, with an M12 vent and inside locknut (BOM line 15); the nut is 8.5 mm clear of the converter, 3.8 mm clear of the lid and 12.2 mm clear of the carrier. The nameplate label is modelled on the lid top (BOM line 16). 68 of 68 constructability checks pass (was 48); STEP and STL re-exported.
3. Done. `bom/bom.csv`: lines 14 (light pipes, LEDs and lead, $1.00), 15 (breather vent, $2.00) and 16 (nameplate label, $0.50) added with a price basis each; lines 2 and 3 respecified for the new holes. `bom/bom-notes.md` updated (total, mass, basis).
4. Done. `docs/04-calcs/sizing.py` re-run: logger 0.44 kg, 0.58 kg with lead and fixings [H2]; 22 N per M6 bolt at 20 g [H3]; plate first mode 168 Hz, unchanged [I1]; cost $77.50 [J1]. PHL-CAL-001 v0.5, PHL-REQ-001 v0.7 and PHL-DEC-001 v0.4 updated. Value-engineering target: USD 75. Estimated cost of the constructable design: USD 77.50 (USD 2.50 over the target).
5. Done. General arrangement PHL-DWG-001 Rev P4 (vent, light pipe holes and nameplate called out; notes updated). Making sketch PHL-DWG-102 adds the front wall vent hole; new lid drilling sketch PHL-DWG-104 (P1).
6. Done. Build plan pictures regenerated: overview (17 components), box hole layout (vent hole and front wall note), new joints 7 (light pipe in the lid) and 8 (vent in the front wall), step 1 (gland and vent), new step 7 (light pipes and nameplate onto the lid), steps 8 to 10 renumbered, wiring (status LEDs). `docs/05-build-plan.md` PHL-BLD-001 v0.3: section 1, 3.2, new 3.8 (lid drilling), 3.5.1 wiring, bought parts, steps, first checks and sources.
7. Done. `cad/src/product_model.py` marks the clear GNSS window as a render detail only (the build lid is opaque) and takes the light pipe, vent and nameplate sizes and positions from `model.py`. Its internals were also brought to the constructable design: carrier plate on the hex standoffs, modules on nylon standoffs, IMU on two screws, status LEDs and lead.
8. Partly done. The pooling rule is written into the server export description in PHL-PRC-001 v0.7 ("Server export: segment files and the pooling rule"): a date per segment, day only, only when at least two vehicles or at least three separate days are pooled; pass times, vehicle identifiers, tracks and speeds never exported. The three-day reading of "several days" is Proposed, awaiting Amish, to be matched with CityTwin. Agreeing the format with CityTwin's item 6 is not done here: cross-repo (see below). No server code was written (TRL 4 software).

Also changed: concept media regenerated (`cad/src/concept_media.py`: hero, blueprint key figures 0.44 kg and $77.50, exploded with callouts 1 to 16, cutaway, flow, model.glb); README cost figures; PHL-PRB-001 v0.7 cost line. `python3 .kit/drawing.py --check-text` is clean.

### Requirement status change

- R15 (low cost): met on paper to **not met**, $77.50 against the $75 value-engineering target ($2.50 over). Counts now: 1 not met, 6 at risk, 2 not verifiable at TRL 3, 3 met on paper, 4 met by design. The register lists savings (offcut plates, a 16 GB card) that could close the gap.

### Cross-repo actions

- CityTwin: match its item 6 (segment file fetch and pooled-date rule) to the PotholeLog export: daily CSV and GeoJSON files fetched over HTTPS, a day-only date per segment only when at least two vehicles or at least three days are pooled, no pass times. Field names to agree.

### Render scenes

`cad/src/product_model.py` exported with `.kit/export_views.py` to `/home/claude/renders/potholelog` (hero, exploded, detail: one .npz and .json each, plus `potholelog__jobs.json`). Photoreal renders, `media/card.png` and `media/social-preview.png` are to be made on Amish's Mac; until then `media/render-*.png` show the concept layout and no carrier plate.

### Proposed, awaiting Amish

- The "several days" in the pooling rule read as three or more separate days.
- R15 is over the target; whether to take the savings in the register or accept the overrun is Amish's call (`budget_usd` left at $75).

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
