# BOM notes

- Items 1 to 11 match the numbered callouts in `media/exploded.png` and the parts in `cad/src/model.py`. The microSD card (10) sits in the controller's slot and the fixings (11) are shown as bolt heads and washers.
- Every line is priced. Prices are indicative single-unit USD prices for concept costing, not quotes. Supplier types are given where no single supplier is preferred.
- Total: $69.00 against the $70 `budget_usd` in `project.yaml`, a margin of $1.00 (PHL-CAL-001, J1).
- PHL-CAL-001 (F4, F5) shows that the 36 V converter input is exceeded by a suppressed load dump on 24 V vehicles. A 60 V-rated converter is about $2 more and would bring the total to $71.00, over the budget. This change is proposed and awaiting Amish; the BOM still carries the 36 V part.
- The depot Wi-Fi version is costed. A cellular option (LTE-M module and antenna, about $20 to $30 more, plus a data plan) is an optional add-on, costed separately and not included.
- The controller, IMU and GNSS choices are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction and remain open for his review (PHL-DDR-001).
