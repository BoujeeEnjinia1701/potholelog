---
doc_id: PHL-CAL-001
title: PotholeLog sizing calculations
project: PotholeLog
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (vehicle and road model, roughness signal and calibration, pothole detection, location, storage and upload, power and transients, hold-up, environment, plate stiffness, installation, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# PotholeLog sizing calculations

On paper, PotholeLog meets eight of its sixteen requirements (four by calculation, four by design), has six at risk, cannot show two at TRL 3 and misses none. Version 0.2 applies Amish's 2026-09-25 decisions (PHL-DDR-002). Version 0.1 found two misses. First, a bus tyre largely bridges the R1 reference pothole (50 mm deep, 300 mm long), so a floor-mounted logger sees it clearly only at low speed: in the quarter-car model the impact stands above ordinary road vibration up to about 20 km/h on a fair road (IRI 4) and about 50 km/h on a good one (IRI 2), and not at 80 km/h. R5's defect-detection range is now restated as 10 to 30 km/h, relying on repeat slow passes near stops and junctions; it is met on good roads and misses by a hair (margin 0.97) at 30 km/h on fair ones, so R5 moves from not met to at risk, and R1 stays at risk. Second, the 9 to 36 V converter was exceeded by a suppressed load dump on a 24 V vehicle. The BOM now carries a 60 V-rated converter, which clears the 58 V load dump and the 58.1 V TVS clamp by 1.9 V; the TVS pulse energy is unverified, so R9 moves from not met to at risk. The parts cost rises from $69.00 to $71.00 against a budget raised from $70 to $75. The roughness function itself looks sound: the signal is 12 times the sensor noise at 20 km/h on a smooth road, and a synthetic calibration against IRI gives r² of 0.93 from one pass and 0.99 from five. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C2], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They are not a survey method, an automotive electrical approval or a mounting approval. Outputs must not drive contract acceptance or safety decisions without validation against a calibrated reference. See PHL-PRC-001, Safety.

## Scope and method

The note checks every requirement in PHL-REQ-001 v0.4 against the design in PHL-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part volumes, so the plate, hole pattern, enclosure and masses used here are the ones in the STEP files and in drawing PHL-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The vehicle is a linear quarter-car model of one side of a 12 m city bus's rear axle: sprung body, unsprung axle and twin tyres. Random road profiles follow the ISO 8608 spectral shape and are solved in the frequency domain; their IRI comes from the standard golden-car model at 80 km/h, following World Bank Technical Paper 46. A single pothole is enveloped by a rigid tyre circle and solved in the time domain. The logger reads the body's vertical acceleration at the floor centerline above the axle.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Vehicle | Per side: sprung mass 4,500 kg (3,500 empty to 5,250 laden), unsprung 500 kg; body frequency 1.2 Hz with 20 % damping (air suspension); twin tyres 1.8 MN/m; tyre radius 0.52 m; wheelbase 6 m | Typical 12 m city bus; to confirm with the pilot fleet |
| Road | ISO 8608 displacement spectrum with slope 2 (1.8 to 2.2 for the calibration study), 0.01 to 10 cycles/m, 250 mm moving average as the tyre patch | ISO 8608 shape; the classes are mapped to IRI in [A2] |
| Logger position | Floor centerline above the axle sees half of a one-sided input (bounce only) and 0.87 of the single-track random input (left and right tracks correlated at 0.5) | Assumed; roll and pitch are not modeled |
| Sensor | 400 Hz output, ±16 g, noise about 100 µg/√Hz; roughness metric band 0.5 to 20 Hz | LSM6DSO class; to confirm from the datasheet |
| Detection | A pothole is detected when its floor peak exceeds the level that ordinary roughness crosses once per km (Rice formula, Gaussian roughness); lateral wander σ 250 mm; twin-tyre width 0.6 m | Assumed; real roads have joints, covers and bumps that are not Gaussian |
| Location | M10-class GNSS, open-sky CEP 1.5 m; σ 3 m per axis suburban, 10 m in dense urban streets with errors 0.5 correlated between passes; PPS time-stamping to 10 ms | Class figures; urban values assumed |
| Data | 6 axes x 16 bit at 400 Hz; 40 B GNSS record at 10 Hz; 8 B time stamp per 100 samples; 10 to 12 h of driving and 200 km a day; 500 events a day; 32 GB card with 94 % usable | As at TRL 2, with the record layout now defined |
| Power | 3.3 V loads 91 mA (ESP32-S3 60 mA at 240 MHz with radio off, board 10 mA, GNSS 10 mA, card 10 mA average, IMU 1 mA); linear regulator on the board from 5 V; 85 % converter efficiency; Wi-Fi adds 150 mA while uploading | Typical module figures; to confirm by measurement later |
| Transients | Suppressed load dump of 35 V (12 V systems) and 58 V (24 V systems), as understood from ISO 16750-2 test B | To confirm from the standard |
| Hold-up | 1 F, 5.0 V rail less a 0.3 V diode, regulator dropout floor 3.6 V; capacitance 70 % at end of life and at -20 °C; 1 s to flush and close files | Typical supercapacitor data; worst-case card write latency |
| Structure | Aluminum E = 70 GPa; plate on four corner bolts with nothing beneath, half the width effective; 20 g crash pulse, M6 property class 8.8 | Conservative screening values, not a vehicle-code check |

## A. Road and vehicle model

- **Vehicle.** The bus corner has a 1.2 Hz body mode (256 kN/m, 13.6 kN·s/m) and a 10.2 Hz wheel-hop mode [A1].
- **Road classes on the IRI scale.** ISO 8608 classes A, B, C and D come out at 2.17, 4.35, 8.69 and 17.38 m/km [A2]. IRI scales with the square root of the spectrum level, so IRI 2, 4 and 6 m/km correspond to Gd(n₀) of 13.6, 54.2 and 122.0 x 10⁻⁶ m³ [A3]. In this note "IRI 2" stands for a good urban road and "IRI 4" for a fair one.

## B. Roughness signal and calibration (R3, R5)

- **Noise.** The IMU's noise over the 0.5 to 20 Hz band is 4.3 mm/s² RMS, and one count at ±16 g is 4.8 mm/s² [B1].
- **Signal.** The floor RMS acceleration in that band rises with IRI and with speed [B2]:

*Table 2. Floor RMS acceleration in the 0.5 to 20 Hz band, m/s² [B2].*

| IRI | 10 km/h | 20 km/h | 30 km/h | 50 km/h | 80 km/h |
| --- | --- | --- | --- | --- | --- |
| 1 m/km | 0.031 | 0.051 | 0.066 | 0.089 | 0.114 |
| 2 m/km | 0.062 | 0.102 | 0.133 | 0.178 | 0.228 |
| 4 m/km | 0.123 | 0.204 | 0.266 | 0.356 | 0.456 |
| 6 m/km | 0.185 | 0.306 | 0.398 | 0.533 | 0.684 |

- **Low speed.** On a smooth road (IRI 1) the signal is 7 times the noise at 10 km/h and 12 times at 20 km/h [B3]. The 20 km/h floor of the roughness range in R5 is supported; the sensor is not the limit.
- **Speed.** At IRI 2 the RMS at 80 km/h is 2.23 times the 20 km/h value; even normalized by the square root of speed it varies 1.31 to 1 over 10 to 80 km/h [B4]. The metric must be calibrated per speed band, as TRL 2 assumed.
- **Scatter.** A 100 m segment at 50 km/h holds 7.2 s of data. With an effective bandwidth of 3.33 Hz, one RMS estimate scatters by 14 %, falling to 6 % averaged over five passes [B5].
- **Calibration.** For 40 synthetic sections from IRI 1 to 8 m/km with spectral slopes from 1.8 to 2.2, a straight-line fit of IRI on floor RMS gives r² of 0.998 with expected values, 0.934 from one pass and 0.992 from five passes, with a slope of 11.1 m/km per m/s² [B6]. This supports the response-type method and the R3 target of r² 0.8, but only a calibration on real reference sections can verify R3.
- **Load.** From empty to laden, the floor RMS changes from 1.07 to 0.96 of its mid-load value with air suspension, and from 1.22 to 0.89 with steel springs [B7]. Buses with air suspension need no load correction beyond this ±7 %; refuse trucks on steel springs need a load flag or calibration by load state.

## C. Pothole detection (R1, R2, R5, R6)

- **The tyre bridges the hole.** A 1,040 mm tyre can drop only 22.1 mm into a 300 mm long pothole, however deep it is, and the loaded tyre's contact patch is about 337 mm long [C1]. A bus sees the R1 reference pothole as a 22 mm dip.
- **Floor peak against background.** The floor peak from the reference pothole falls with speed while ordinary road vibration rises:

*Table 3. Reference pothole (50 mm deep, 300 mm long) against a threshold that ordinary roughness crosses once per km [C2], [K1].*

| Speed | Floor peak | Threshold, IRI 2 | Margin, IRI 2 | Threshold, IRI 4 | Margin, IRI 4 |
| --- | --- | --- | --- | --- | --- |
| 10 km/h | 1.35 m/s² (0.138 g) | 0.24 m/s² | 5.64 | 0.48 m/s² | 2.82 |
| 20 km/h | 1.20 m/s² | 0.40 m/s² | 3.03 | 0.79 m/s² | 1.51 |
| 30 km/h | 0.98 m/s² | 0.51 m/s² | 1.94 | 1.01 m/s² | **0.97** |
| 50 km/h | 0.71 m/s² | 0.66 m/s² | 1.07 | 1.32 m/s² | **0.54** |
| 80 km/h | 0.48 m/s² | 0.82 m/s² | **0.59** | 1.64 m/s² | **0.30** |

Margins below 1 (bold) mean the pothole is lost in ordinary road vibration.

- **Relaxing the threshold does not rescue high speed.** Allowing 10 background crossings per km, which clustering over repeat passes could tolerate, raises the IRI 4 margins only to 1.17 at 30 km/h and 0.66 at 50 km/h [C2b]. A band-pass detector tuned to the wheel-hop band gave similar margins in a side check, so the limit is physical, not the choice of filter.
- **Longer potholes are found at all speeds.** A 50 mm deep pothole 600 mm long lets the tyre reach the bottom and gives margins of 5.28 at 10 km/h, 2.63 at 50 km/h and 1.67 at 80 km/h on an IRI 4 road [C2c].
- **Wheel path.** The twin tyres hit a 300 mm pothole centered in the wheel path on 93 % of passes, and on at least one of three passes 99.96 % of the time [C3]. The limit is detection per hit, not the chance of a hit.
- **R1 is at risk and R5 is not met.** In urban service a bus often passes a spot at 20 km/h or less, near stops and junctions, and R1 allows three passes, so R1 may still be met on streets with low speeds; it cannot be shown without field data. The original R5 defect-detection range of 10 to 80 km/h was not met for the reference pothole at 30 km/h and above on fair roads, or at 80 km/h on good ones. Under PHL-DDR-002 (N2) the range is restated as 10 to 30 km/h. Across that band the lowest margin is 1.94 on IRI 2 roads and 0.97 at 30 km/h on IRI 4 roads, or 1.17 allowing 10 background crossings per km [K2]. R5 is at risk rather than not met.
- **Range and sampling (R6).** The floor peak is at most 0.14 g, far inside ±16 g. An axle mount would see about 9 g in this linear model, 65 times more, with water and stones [C4], which supports the floor mount (D3). Sampling at 400 Hz keeps 99 % or more of the floor peak; samples are 35 mm apart at 50 km/h and 56 mm at 80 km/h, giving 9 and 5 samples across the pothole [C5].
- **Two axles.** The front and rear axle impacts arrive 0.72 s apart at 30 km/h and 0.43 s at 50 km/h [C6]. Pairing them confirms an event and fixes which axle hit it.
- **R2 cannot be shown at TRL 3.** Joints, drain covers and speed bumps are not Gaussian roughness, and they are the likely false reports. Only a field check of reported clusters can verify R2.

## D. Location (R4)

*Table 4. 95 % location radius [D1].*

| Setting | σ per axis | One pass | 10-pass cluster |
| --- | --- | --- | --- |
| Open sky | 1.3 m | 3.1 m | 1.0 m |
| Suburban | 3.0 m | 7.3 m | 2.3 m |
| Dense urban | 10.0 m | 24.5 m | 18.2 m (errors correlated) |

- **Timing.** With PPS, a 10 ms IMU-to-GNSS error is 0.22 m at 80 km/h; using message times alone, 100 ms is 2.2 m. Fixes are 2.2 m apart at 10 Hz and 80 km/h [D2]. BOM item 8 now calls for a PPS output.
- **Axle.** An event attributed to the wrong axle is misplaced by the 6 m wheelbase [D3]; axle pairing (section C) removes this.
- **R4 is at risk.** The 10 m target is met in open and suburban streets but not in dense urban streets, where multipath errors repeat from pass to pass and do not average out. Map matching to the street centerline is the likely fix and is a later software task.

## E. Storage and upload (R7, R8)

- **Raw data.** 5.23 kB/s, or 188 MB per 10 h day and 226 MB per 12 h day [E1]. A 32 GB card holds 160 days at 10 h or 133 days at 12 h [E2], far beyond the 30 days of R7. Over five years the card is written 14 times over (412 GB) [E3], well within a high-endurance card's rating. **R7 is met on paper.**
- **Summaries.** A 48 B segment record and a 32 B event record give 112 kB a day for 200 km and 500 events [E4]. The pass time is kept only in the operator's copy (R13).
- **Upload.** At 2 Mbit/s effective at the edge of depot coverage the upload takes 8.4 s, most of it connecting; a day of raw data would take 13 min, so raw data stays on the card [E5]. The hold-up capacitor can power Wi-Fi for only 2.3 s [G3], so the upload runs while the ignition is on: on arrival at the depot or at the next start. **R8 is met on paper** for vehicles in daily service that spend at least about 10 s with the ignition on within depot Wi-Fi.

## F. Power and transients (R9)

- **Running power.** The 3.3 V loads draw 91 mA, which is 0.45 W at 5 V through the board's linear regulator and 0.54 W from the vehicle [F1]: 45 mA at 12 V, 22 mA at 24 V and 59 mA at 9 V, well within the 2 A fuse [F2]. Uploading raises this to 1.42 W for about 8 s a day; a 10 h day uses 5.4 Wh [F3]. The running target of under 1 W is met; the brief upload peak exceeds it. With an ignition-switched feed there is no draw with the ignition off. The TRL 2 estimate of 0.7 W was conservative and is revised to 0.54 W.
- **Transients.** Under PHL-DDR-002 (N1) the converter is rated 60 V (v0.1 used a 36 V part). Normal 12 V (9 to 16 V) and 24 V (18 to 32 V) supplies and both suppressed load dumps, 35 V on 12 V systems and 58 V on 24 V systems, are within the 60 V input [F4]. The SMBJ36A-class TVS clamps at up to 58.1 V, which the 60 V converter clears by 1.9 V [F5]. The TVS conducts during a 24 V load dump, and a pulse lasting hundreds of milliseconds may overheat it; only a bench test can show that it survives. **The transient part of R9 is at risk** for 24 V vehicles, rather than not met. A surge-stopper front end remains the fuller fix and was not chosen.

## G. Hold-up (R10)

- **Hold-up time.** 1 F from 4.7 V to 3.6 V stores 4.57 J, which lasts 10.0 s new and 7.0 s at 70 % capacitance; closing files needs about 1 s, a factor of 7 [G1]. The TRL 2 estimate of about 9 s stands for a new capacitor. **R10 is met on paper.** The controller should start shutdown only after about 2 s of low input, so engine cranking dips are ridden through rather than logged as a stop.
- **Charging.** Through 10 Ω the capacitor reaches 95 % in 30 s; the 0.5 A charge peak is within the 1 A converter [G2].

## H. Environment and fixings (R11)

- **Self-heating.** 0.54 W over 339 cm² of box raises the inside by 2.0 K, so at +70 °C ambient the parts see about 72 °C [H1]. The GNSS, IMU, converter and a high-endurance card are commonly rated to 85 °C, but many supercapacitors are rated to 70 °C and some ESP32-S3 module variants (those with octal PSRAM) are rated to 65 °C. BOM items 5, 6 and 10 now state the grades needed. Parked in the sun with the ignition off, the logger sees only storage temperature.
- **Mass.** The plate is 187 g, the polycarbonate enclosure 126 g, the modules 46 g and the gland 12 g: 0.37 kg for the logger, 0.51 kg with the 2 m lead and fixings [H2]. The TRL 2 estimate of 0.4 kg stands.
- **Fixings.** A 20 g crash pulse puts 73 N on the plate, 18 N per M6 bolt against about 9.6 kN of shear capacity, and 34 N on the four M4 box screws [H3]. Strength is not a concern; loosening under long-term vibration is, and only a test can show that locking nuts suffice.
- **R11 is at risk:** the temperature margin depends on part grades, and vibration and loosening cannot be verified at TRL 3.

## I. Plate stiffness and installation (R12)

- **Stiffness.** Spanning 140 mm between corner bolts with nothing beneath, on half its width, the 4 mm plate has a stiffness of 359 kN/m under a moving mass of 263 g and a first mode of 186 Hz; on full-width supports it is 263 Hz [I1]. A 3.5 mm plate would just reach 150 Hz on the conservative model [I2]. The bracket part of R12 is met on paper. The mode sits near the 200 Hz Nyquist limit, so the IMU's internal low-pass filter should be set well below 200 Hz. A thin floor panel has its own lower modes, so the plate should bolt to a crossmember, seat rail or other stiff structure.
- **Installation time.** The tasks add up to 30 min, exactly the R12 limit [I3]. Tool clearance around the bolts is tight: the hole centers are 10 mm beyond the box end walls, leaving about 2 mm for a 10 mm socket [I4], so the plate should be bolted down before the box is fitted. **R12 is at risk** on installation time.

## J. Cost (R15)

The BOM has 11 lines totaling $71.00 against the $75 `budget_usd`, a margin of $4.00 [J1]. The 60 V converter added about $2 (from $69.00) and the budget was raised from $70 to $75 under PHL-DDR-002 (N1). **R15 is met on paper.** The LTE-M option would bring the cost to $91 to $101 [J2], over budget; it is not in the BOM.

## K. Results against every requirement

*Table 5. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Work across normal fleet speeds | Roughness signal 12 x noise at 20 km/h; lowest defect margin in 10 to 30 km/h 1.94 on IRI 2 and 0.97 on IRI 4 [K2] | Roughness 20 to 80 km/h; defects 10 to 30 km/h (PHL-DDR-002, N2) | At risk (30 km/h on fair roads) |
| R9 | Run from vehicle power | 0.54 W running, 1.42 W for 8 s uploading; 24 V suppressed load dump 58 V and TVS clamp 58.1 V against a 60 V converter [F4], [F5] | 9 to 36 V, under 1 W, ISO 16750-2 transient levels | At risk (1.9 V margin; TVS pulse energy unverified) |
| R1 | Detect potholes | Margin above 1 up to 20 km/h on IRI 4 and 50 km/h on IRI 2; 93 % of passes hit | 80 % found within 3 passes | At risk; field data needed |
| R4 | Locate defects | 95 % radius 2.3 m suburban, 18.2 m dense urban (10 passes) | 10 m, correct street | At risk |
| R11 | Survive the vehicle environment | About 72 °C inside at +70 °C; crash factor 531 | -20 to +70 °C, IP65, no loosening | At risk (part grades; vibration unverifiable) |
| R12 | Install quickly and safely | 30 min; plate first mode 186 Hz | 30 min; above 150 Hz | At risk (install time at the limit) |
| R2 | Keep false reports low | Not computable from Gaussian roughness | 10 % or fewer false clusters | Not verifiable at TRL 3 |
| R3 | Report roughness per segment | Synthetic r² 0.93 from one pass, 0.99 from five | r² 0.8 against reference IRI | Not verifiable at TRL 3 (supported on paper) |
| R7 | Store data on the vehicle | 133 to 160 days on 32 GB | 30 days | Met on paper |
| R8 | Get data off the vehicle | 112 kB in 8.4 s with the ignition on in depot Wi-Fi | Within 24 h, no staff action | Met on paper (vehicles in daily service) |
| R10 | Shut down cleanly | 7.0 s hold-up at end of life, 1 s needed | No corruption on power loss | Met on paper |
| R15 | Low cost and buildable | $71.00 | $75 (PHL-DDR-002, N1) | Met on paper ($4 margin) |
| R6 | Sample fast enough | 400 Hz, ±16 g, 10 Hz GNSS; peak 0.14 g | 400 Hz, ±8 g, 5 Hz | Met by design |
| R13 | Protect privacy | No camera or microphone; pass times kept by the operator only | Road-level data only | Met by design |
| R14 | Open outputs | CSV and GeoJSON per the CityTwin export (D6) | Readable by CityTwin and GIS | Met by design (CityTwin ingest path still open) |
| R16 | Fit the fleet types in this build | Buses and refuse trucks on 9 to 36 V power (D1) | Buses and refuse trucks; bicycles deferred | Met by design (bicycle variant deferred) |

Counts: 0 not met, 6 at risk, 2 not verifiable at TRL 3, 4 met on paper, 4 met by design (v0.1: 2 not met, 4 at risk).

## Checks against the TRL 2 figures

*Table 6. TRL 2 figures checked.*

| TRL 2 claim (PHL-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| About 35 mm sample spacing at 50 km/h | 35 mm [C5] | Stands |
| About 9 samples across a 300 mm pothole at 50 km/h, about 4 at 80 km/h | 9 and 5 [C5] | Precis updated (5) |
| Raw data about 5.2 kB/s, 190 MB a day | 5.23 kB/s, 188 MB per 10 h day [E1] | Stands |
| About 5 months on 32 GB | 160 days at 10 h, 133 days at 12 h [E2] | Stands |
| About 0.1 MB of summaries a day | 112 kB [E4] | Stands |
| About 0.7 W, about 60 mA at 12 V | 0.54 W, 45 mA at 12 V [F1], [F2] | Precis updated |
| About 9 s hold-up | 10.0 s new, 7.0 s at end of life [G1] | Precis updated |
| About 0.4 kg | 0.37 kg; 0.51 kg with lead and fixings [H2] | Stands |
| About $69 | $71.00 with the 60 V converter [J1] | Updated under PHL-DDR-002 |
| 9 to 36 V input covers 12 V and 24 V vehicles | Not for 24 V load dump with the 36 V part; within 60 V [F4] | 60 V converter decided (PHL-DDR-002, N1) |
| Detection margin "thin at high speed" | Lost at 30 km/h and above (IRI 4) or 80 km/h (IRI 2) for the reference pothole [K1] | R5 range restated as 10 to 30 km/h (PHL-DDR-002, N2); at risk |
