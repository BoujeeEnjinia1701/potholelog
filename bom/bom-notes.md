# BOM notes

- Items 1 to 11 match the numbered callouts in `media/exploded.png` and the parts in `cad/src/model.py`. The microSD card (10) sits in the controller's slot and the fixings (11) are shown as bolt heads and washers.
- Every line is priced. Prices are indicative single-unit USD prices for concept costing, not quotes. Supplier types are given where no single supplier is preferred.
- Total: $71.00 against the $75 `budget_usd` in `project.yaml`, a margin of $4.00 (PHL-CAL-001, J1). The budget was raised from $70 under PHL-DDR-002 (N1).
- PHL-CAL-001 v0.1 (F4, F5) showed that a 36 V converter input is exceeded by a suppressed load dump on 24 V vehicles. Item 4 is now a 60 V-rated converter, about $2 more ($7.00 to $9.00), decided by Amish on 2026-09-25 (PHL-DDR-002, N1). The TVS pulse energy during a load dump still needs a bench test (TRL 4, on hold).
- The depot Wi-Fi version is costed. A cellular option (LTE-M module and antenna, about $20 to $30 more, plus a data plan) is an optional add-on, costed separately and not included.
- The controller, IMU and GNSS choices were decided by Amish on 2026-09-25 (PHL-DDR-001, D4 and D5).
