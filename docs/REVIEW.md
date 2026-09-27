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
