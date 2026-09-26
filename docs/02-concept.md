---
doc_id: PHL-PRC-001
title: PotholeLog design precis
project: PotholeLog
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# PotholeLog design precis

## Summary

PotholeLog is a sealed box, about 120 x 90 x 59 mm, bolted to the floor of a bus or refuse truck above the rear axle. It records how the vehicle shakes and where it is, turns each 100 m of road into a roughness value and flags sharp impacts as possible potholes, then uploads a small daily file over depot Wi-Fi. Averaged over many passes and calibrated per vehicle, the data gives a city a weekly map of road condition on every street its fleet drives. First-order numbers suggest off-the-shelf modules meet the sampling, storage and power needs for about $69 in parts, just inside the $70 budget. Detection accuracy and calibration to IRI are unverified until field data exist.

![PotholeLog on a vehicle floor above the rear axle, with a wheel, suspension and a road with a pothole for scale](../media/hero.png)

Figure 1. Concept massing model. The logger is the small dark box on the floor section; the grey scene is for scale.

## How it works

1. **Sense.** A 6-axis IMU rigidly fixed to the enclosure floor samples acceleration at 400 Hz. A GNSS module under the lid logs position and speed at 10 Hz.
2. **Log raw data.** Raw samples go to a microSD card as a rolling buffer, so any detection can be re-run later with a better algorithm.
3. **Summarize on board.** For every 100 m traveled, the controller computes a roughness value from the vertical acceleration (for example, band-limited RMS normalized for speed), and records the segment's start and end, speed and the number of samples. Sharp vertical impacts above a threshold are stored as defect events with position, speed and peak size.
4. **Upload.** When the vehicle is back at the depot and the ignition is switched off or on, the controller joins the depot Wi-Fi and uploads the day's summaries to the fleet's server.
5. **Calibrate and aggregate.** On the server, each vehicle's raw roughness is converted to an IRI estimate using a calibration equation found on reference sections, in the way World Bank Technical Paper 46 describes for response-type systems ([Sayers et al., 1986](https://documents1.worldbank.org/curated/en/851131468160775725/pdf/multi-page.pdf)). Events from several passes and vehicles are clustered; a cluster seen on repeated passes becomes a reported defect, as in Pothole Patrol ([Eriksson et al., 2008](https://doi.org/10.1145/1378600.1378605)).
6. **Publish.** The city publishes a map of segment roughness and defect clusters as CSV and GeoJSON, for its own GIS and for CityTwin. Vehicle tracks and timestamps stay on the operator's server.

![Data flow from road surface to open road map](../media/flow.png)

Figure 2. Data flow. Values are estimates.

## Main components

Table 1. Main components. Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Mounting plate | 160 x 110 x 4 mm aluminum, 4 x M6 | Bolts to existing floor or seat-rail fixings; rigid so the IMU sees the vehicle, not the bracket |
| 2 | Enclosure base | Stock IP65 ABS or polycarbonate box, 120 x 90 mm | IMU screwed directly to its floor |
| 3 | Enclosure lid | Supplied with the box, with gasket | GNSS antenna under the lid; plastic lid keeps sky view through vehicle windows |
| 4 | DC-DC converter and protection | 9 to 36 V in, 5 V 1 A out; TVS diode, reverse-polarity diode, input fuse | Covers 12 V and 24 V vehicles |
| 5 | Hold-up supercapacitor | 1 F, 5.5 V | Keeps the controller alive long enough to close files when power drops |
| 6 | Controller | ESP32-S3 board with Wi-Fi and microSD slot | Proposed, awaiting Amish (alternatives below) |
| 7 | IMU | 6-axis, LSM6DSO class, ±16 g, 400 Hz or more | Gyroscope helps separate body roll and pitch from vertical motion |
| 8 | GNSS module | u-blox M10 class with patch antenna, 10 Hz | Multi-constellation |
| 9 | Cable gland and fused lead | M16 gland, 2 m lead, inline 2 A fuse | Wired to an ignition-switched fused circuit |

![Exploded view with BOM callouts](../media/exploded.png)

Figure 3. Exploded view with numbered callouts matching the BOM.

![Section through the enclosure](../media/cutaway.png)

Figure 4. Cutaway. The IMU sits on the enclosure floor, the controller and converter beside it, and the GNSS module under the lid.

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

Table 2. First-order numbers.

| Quantity | Estimate | Basis and assumptions | Requirement |
| --- | --- | --- | --- |
| Sample spacing on the road | about 35 mm | 400 Hz at 50 km/h (13.9 m/s) | R6 |
| Samples across a 300 mm pothole | about 9 at 50 km/h, about 4 at 80 km/h | Length divided by sample spacing | R1, margin thin at high speed |
| GNSS fix spacing | about 1.4 m | 10 Hz at 50 km/h | R4 |
| Raw data rate | about 5.2 kB/s | 6 axes x 2 bytes x 400 Hz, plus about 0.4 kB/s of GNSS records | |
| Raw data per day | about 190 MB | 10 h of driving | |
| Raw storage on a 32 GB card | about 5 months | Rolling buffer | R7 met |
| Summaries per day | about 0.1 MB | 200 km a day, 2,000 segments at 48 bytes, plus up to about 500 events at 32 bytes | R8 met |
| Running power | about 0.7 W | Controller about 0.35 W with Wi-Fi off, GNSS about 0.1 W, IMU and card about 0.1 W, converter at about 85 % efficiency | R9 met |
| Supply current | about 60 mA at 12 V, about 30 mA at 24 V | From running power | |
| Hold-up time | about 9 s | 1 F from 5.0 V to 3.5 V gives about 6 J; at 0.7 W | R10 met; closing files needs under 1 s |
| Size | 120 x 90 x 59 mm on a 160 x 110 mm plate | Stock enclosure | |
| Mass | about 0.4 kg | Plate about 0.19 kg, box about 0.11 kg, electronics and lead about 0.1 kg | |
| Parts cost | about $69 | Indicative prices, see `bom/bom.csv` | R15 met with $1 margin |

## Key design choices

All choices below are proposed, awaiting Amish.

- **Sprung-mass mount on the floor, not on the axle.** The floor is clean, dry and easy to reach, and the GNSS can see the sky through the windows. The axle would give a stronger, less filtered signal but sees large shocks, water and stones. Calibration per vehicle corrects for the suspension.
- **Depot Wi-Fi upload, not cellular.** It keeps parts cost within $70 and avoids data plans. Cellular (for example an LTE-M module) would give same-day data but adds about $20 to $30 per unit and a monthly fee.
- **Raw data kept on the card.** Storage is cheap, and raw data lets the detection method improve without new hardware.
- **Summaries and events, not tracks, leave the vehicle's operator.** Only road-level results are published (R13).
- **Controller.** ESP32-S3 (Wi-Fi, low cost, wide community) is proposed. Alternatives: an RP2040 board with a separate Wi-Fi module, or an nRF52 board with a phone or gateway for upload.
- **Built on existing lab work where it fits.** Outputs are proposed to follow the CityTwin open data export so PotholeLog segments can appear on the CityTwin map; CityTwin is built on TwinKit. PotholeLog does not use FieldNode, because it runs from vehicle power rather than solar and uploads at the depot rather than over LoRaWAN.

## Safety

> **Safety:** PotholeLog is fitted to vehicles that carry passengers and operate in traffic.
>
> - **Secure mounting.** A loose box can become a projectile in a crash or hard stop. Bolt the plate through with M6 bolts and locking nuts at existing fixing points, never with adhesive or magnets alone. Do not cut, drill or weld chassis members or safety-critical structure; follow the fleet operator's and vehicle maker's rules for body fittings.
> - **Vehicle electrics.** Connect only to a fused, ignition-switched circuit through the inline fuse, with the battery isolated during installation. Route the lead away from moving parts, hot surfaces and sharp edges, and protect it where it passes through panels. A short on a 24 V vehicle supply can start a fire.
> - **Working on vehicles.** Install only with the vehicle parked, secured and switched off. Never work under a vehicle supported only by a jack.
> - **Driver distraction.** The logger has no controls or display and must not be handled while the vehicle is moving.
> - **Sharp edges.** Deburr the aluminum plate.
> - **Supercapacitor.** It stays charged for a short time after power is removed; do not short its terminals.
> - **Data.** Vehicle location data can reveal where drivers are and when. Keep tracks on the operator's server under the operator's data policy, inform drivers and unions before a pilot, and publish only road-level results.
>
> This is a research prototype. It is not certified to automotive electrical or EMC standards, and its outputs must not be used for contract acceptance or safety decisions without validation against a calibrated reference.

## Open questions for TRL 3

- Which roughness metric from sprung-mass acceleration correlates best with IRI across speed bands, and how many calibration sections does each vehicle need?
- What event threshold and clustering rule meet R1 and R2 together?
- How far off is GNSS in the partner city's densest streets, and is map matching needed for R4?
- Is the 4 mm aluminum plate stiff enough on a typical bus floor to keep the first natural frequency above 150 Hz (R12)?
- Which host fleet and city for a first pilot, and who provides reference IRI?
- Should a bicycle variant be developed, and if so with what battery and mount (R16)?

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
