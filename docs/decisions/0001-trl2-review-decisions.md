---
doc_id: PHL-DDR-001
title: PotholeLog TRL 2 review decisions
project: PotholeLog
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 work and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations for items D1 to D7 are adopted for TRL 3 work pending Amish's review; item O1 remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", seven of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Under that instruction, each item that carries a recommendation is adopted as recommended for TRL 3 work and stays open for his review. The item without a specific recommendation stays open. Nothing in this record is a decision by Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in PHL-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted as recommended.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Bicycles in the pitch | Option (a): keep the pitch and treat a bicycle variant (own battery, handlebar or seat-post mount) as a later step. The pitch and problem lines in `project.yaml` and `README.md` are unchanged, because no rewording was recommended. R16 is redefined for this build as buses and refuse trucks, with the bicycle variant deferred. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Upload route | Depot Wi-Fi first; LTE-M cellular as an optional add-on, costed separately. No budget change was recommended; `budget_usd` stays at $70. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Mount location | Sprung-mass floor mount above the rear axle, not an axle mount. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Controller | ESP32-S3 board with Wi-Fi and a microSD slot. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | IMU and GNSS classes | LSM6DSO-class IMU and u-blox M10-class GNSS, to be confirmed against datasheets. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Segment length and output format | 100 m segments plus point events, in CSV and GeoJSON following the CityTwin open data export. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | Privacy rule | Publish only road-segment roughness and defect clusters; keep vehicle tracks and timestamps on the operator's server; no driver scoring. To be agreed with any fleet partner and its drivers. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First pilot partner and city. The TRL 2 note described the kind of partner needed (a city road department with a bus or refuse fleet that can provide reference IRI sections, possibly found through the Helpful Engineering network) but named no partner, city or preference. No choice is made here. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields change. No new budget, pitch or problem wording was recommended, so `budget_usd` stays at $70 and the pitch still names bikes.
- PHL-PRB-001, PHL-PRC-001 and PHL-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed"; they are adopted as recommended for TRL 3, open for Amish's review. R16 is redefined (D1); R8, R13 and R14 now rest on adopted choices rather than proposals.
- The TRL 3 calculations (PHL-CAL-001) raise two new items that this record does not decide: the converter input rating for 24 V vehicles (R9), which would take the parts cost to $71 against the $70 budget, and the defect-detection speed band or reference defect (R1, R5). They are listed in `docs/REVIEW.md` as "Proposed, awaiting Amish".
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
