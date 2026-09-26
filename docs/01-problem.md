---
doc_id: PHL-PRB-001
title: PotholeLog problem statement
project: PotholeLog
doc_type: Problem statement
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work with sources)
---

# PotholeLog problem statement

Road surveys are expensive and infrequent, so repairs follow complaints rather than condition. Most cities and road agencies already run vehicles over every street each week, but those trips produce no record of the road surface. A low-cost logger on those vehicles could turn routine driving into a continuous, repeatable condition survey.

## The problem

Road condition data is collected in two main ways today, and both leave gaps.

- **Survey vehicles and profilers.** Agencies measure roughness with instrumented vans or profilers and report it as the International Roughness Index (IRI), a standard scale the World Bank set out in 1986 ([Sayers, Gillespie and Paterson, World Bank Technical Paper 46](https://documents1.worldbank.org/curated/en/851131468160775725/pdf/multi-page.pdf)). These surveys are accurate but are usually repeated only every year or several years, and local streets are surveyed least often.
- **Complaints and patrols.** Potholes on local streets are mostly found by residents reporting them or by inspectors on foot or in a car. This favors busy and vocal neighborhoods and misses defects on routes that few people report.

The size of the gap is large even in well-funded networks. In the United States, about 25 % of the reported mileage of urban "other principal arterials" had an IRI above 170 in/mi (2.7 m/km) in 2023, the level the Federal Highway Administration treats as poor (computed from [FHWA Highway Statistics 2023, table HM-64](https://www.fhwa.dot.gov/policyinformation/statistics/2023/hm64.cfm)). In England, local authorities rated 17 % of their unclassified roads, the small residential and rural roads, as needing maintenance to be considered in the year to March 2025 ([DfT, Road conditions in England to March 2025](https://www.gov.uk/government/statistics/road-conditions-in-england-to-march-2025)).

Poor surfaces also matter for safety. About 1.16 million people die each year in road traffic crashes, 92 % of them in low- and middle-income countries, and more than half are pedestrians, cyclists and motorcyclists ([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries)). Road surface is only one factor in those crashes, but it weighs most on two-wheelers, and it is the factor that condition data helps a maintenance team act on.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| City or county road maintenance team | A map of where roads are rough and where new potholes appear, updated weekly, to plan patching and resurfacing | Small engineering team, limited survey budget, existing asset or GIS system |
| Fleet operator (transit agency, refuse contractor, municipal fleet) | A device that installs in minutes, needs no driver action and does not track drivers | Vehicles return to a depot daily; maintenance staff install and service devices |
| Drivers | No distraction, no performance monitoring | The device is out of sight and has no controls |
| Residents and cyclist groups | Evidence that repairs follow measured condition, not only complaints | Open data published by the city |
| Road agencies in low- and middle-income countries | Network condition data where survey vans are unaffordable | Mixed paved and unpaved roads, minibuses and trucks, intermittent connectivity |

Operating context assumed for the concept:

- Host vehicles are city buses, refuse trucks and similar fleet vehicles on fixed or repeated routes. They run about 8 to 12 h a day at 0 to 80 km/h and return to a depot each night (assumption).
- The logger is bolted to a rigid point of the vehicle floor or structure above the rear axle and wired to the ignition-switched 12 V or 24 V supply.
- Each street is driven many times a month by one or more vehicles, so results can be averaged over passes and vehicles.
- The vehicle filters the road input through its tyres and suspension, and each vehicle responds differently, so the raw signal must be calibrated per vehicle before it can be compared with IRI.

## Prior work

- **Pothole Patrol (MIT, 2008).** Accelerometers and GPS on 7 taxis in Boston. A simple classifier misidentified good road as potholes less than 0.2 % of the time, and after clustering over 90 % of reported potholes contained road anomalies needing repair ([Eriksson et al., MobiSys 2008](https://doi.org/10.1145/1378600.1378605)). This is the closest precedent and shows the approach works on fleet vehicles.
- **Response-type roughness measuring systems.** The World Bank IRI guidelines describe instruments that measure a vehicle's response to the road and convert it to IRI with a calibration equation found experimentally for that specific vehicle ([World Bank Technical Paper 46](https://documents1.worldbank.org/curated/en/851131468160775725/pdf/multi-page.pdf)). PotholeLog follows the same principle with a cheaper sensor.
- **Smartphone apps.** Several cities and development agencies have used phone apps to log bumps and roughness. Phones are cheap but move in their mounts, change between trips and depend on a volunteer; a fixed, calibrated logger avoids those problems.

## Constraints

- Garage-buildable prototype, about $70 USD in parts per unit (`project.yaml`).
- Off-the-shelf modules only; no custom PCB for the first build.
- Installs on a fleet vehicle without cutting or welding structural members and without the driver doing anything.
- Road data only: no camera, no microphone, and no driver behavior scoring.
- Open hardware (CERN-OHL-S-2.0) and open software (MIT), with outputs in open formats (CSV, GeoJSON).

## Out of scope

- Replacing a calibrated profiler for pavement design or contract acceptance.
- Measuring crack type, rutting depth or skid resistance.
- Real-time alerts to drivers.

> **Safety:** The logger is installed on vehicles that operate in traffic and are connected to a vehicle electrical system. Mounting, wiring and fusing must follow the fleet operator's procedures. See the precis (PHL-PRC-001) for the full safety section.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
