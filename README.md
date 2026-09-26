# PotholeLog

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $70 USD · **Difficulty:** 2 of 5

A vehicle-mounted road roughness logger for buses, garbage trucks or bikes that records vibration with location to map potholes and rough roads as the fleet drives its routes.

![PotholeLog concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

Fleets already cover the road network every week, and a small sensor turns routine trips into a road survey. PotholeLog is a sealed box bolted to the floor of a bus or refuse truck above the rear axle. It logs vertical acceleration at 400 Hz with GNSS position, reports a roughness value for every 100 m of road and flags sharp impacts as possible potholes. Many passes by many vehicles are averaged, and each vehicle is calibrated on a few reference sections to give an estimate on the International Roughness Index (IRI) scale, following the method the World Bank set out for response-type roughness meters ([Technical Paper 46](https://documents1.worldbank.org/curated/en/851131468160775725/pdf/multi-page.pdf)).

It is open and garage-buildable because the agencies with the least survey money most need the data, and the parts are ordinary: an ESP32 board, an IMU breakout, a GNSS module, a vehicle DC-DC converter and a stock IP65 box, for about $69. Open firmware and an open data format let a city check how its road map was made and let others improve the detection method on the same raw data.

## Burning platform

Many road networks carry a large share of rough pavement. In the United States in 2023, about 25 % of the reported mileage of urban "other principal arterials" had an IRI above 170 in/mi (2.7 m/km), the level treated as poor (computed from [FHWA Highway Statistics, table HM-64](https://www.fhwa.dot.gov/policyinformation/statistics/2023/hm64.cfm)). In England, local authorities rated 17 % of their unclassified roads as needing maintenance to be considered in the year to March 2025 ([Department for Transport](https://www.gov.uk/government/statistics/road-conditions-in-england-to-march-2025)). Yet most local streets are surveyed rarely, so repairs follow complaints.

The stakes go beyond vehicle damage. Road crashes kill about 1.16 million people a year, 92 % of them in low- and middle-income countries, and more than half of those killed are pedestrians, cyclists and motorcyclists ([WHO](https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries)), the road users most exposed to potholes and broken surfaces. The same WHO fact sheet estimates that crashes cost most countries 3 % of gross domestic product.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal road maintenance | Weekly roughness and pothole map from the city's own fleet to plan patching and resurfacing |
| Public transit | Buses log the corridors they use most, and the agency can show where rough roads affect ride comfort and wear |
| Waste collection | Refuse trucks reach nearly every residential street on a weekly cycle, covering the roads surveys visit least |
| Road agencies and development programs | Low-cost condition data for network planning where survey vans are unaffordable |
| Fleet maintenance | Relate suspension and tyre wear to the roughness of each vehicle's routes |
| Universities and civic tech groups | Open raw data for research on detection methods and road equity |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | About a quarter of urban principal arterial mileage rated above the poor IRI level in 2023 ([FHWA HM-64](https://www.fhwa.dot.gov/policyinformation/statistics/2023/hm64.cfm)); cities have large bus and refuse fleets to host loggers |
| England and the United Kingdom | 17 % of local unclassified roads needed maintenance to be considered in 2024/25 ([DfT](https://www.gov.uk/government/statistics/road-conditions-in-england-to-march-2025)); councils already publish condition data |
| Sub-Saharan Africa | Road traffic death rates are highest in the WHO African Region ([WHO](https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries)); minibus fleets cover dense networks where survey budgets are small |
| India and South Asia | Fast-growing cities with heavy two-wheeler traffic and monsoon damage to road surfaces; municipal bus and waste fleets are large |
| Latin America | Municipal bus networks run on streets that are rarely surveyed; open data supports public accountability for repairs |
| Canada and northern Europe | Freeze-thaw cycles open potholes quickly in spring, so weekly data matters more than annual surveys |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. The real-world precedent was the MIT Pothole Patrol, which put accelerometers and GPS on 7 Boston taxis and found that over 90 % of the potholes it reported after clustering were real road anomalies needing repair ([Eriksson et al., 2008](https://doi.org/10.1145/1378600.1378605)); PotholeLog aims to make that approach cheap, open and calibrated.

## Problem

Road surveys are expensive and infrequent, so repairs follow complaints rather than condition. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A vehicle-mounted road roughness logger for buses, garbage trucks or bikes that records vibration with location to map potholes and rough roads as the fleet drives its routes. The first concept targets buses and refuse trucks on vehicle power, with summaries uploaded over depot Wi-Fi; a bicycle variant would need its own battery and mount and is proposed as a later step, awaiting Amish. First-order estimates: about 0.7 W, about 0.1 MB of summaries a day, about 5 months of raw data on a 32 GB card and about $69 in parts. Detection accuracy and calibration are unverified until field data exist.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md)

## Key components

- 6-axis IMU (LSM6DSO class) fixed to the enclosure floor
- GNSS module with patch antenna (u-blox M10 class)
- ESP32-S3 controller with Wi-Fi and microSD storage
- 9 to 36 V vehicle DC-DC converter with fuse, TVS and reverse-polarity protection, plus a hold-up supercapacitor
- Stock IP65 enclosure on an aluminum mounting plate

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Bolt the mounting plate through at existing fixing points so nothing can detach in a crash or hard stop, and never cut or weld structural members. Wire only to a fused, ignition-switched circuit with the battery isolated during installation, and route the lead away from moving parts and sharp edges. Never interact with the device while driving. Location data can reveal drivers' movements: publish only road-level results. This is a research prototype, not certified to automotive standards. See [docs/02-concept.md](docs/02-concept.md#safety).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (PHL-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `PHL-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
