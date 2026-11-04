# v15 reproduction and limits

2026-11-04. Generate certificate before JS checks:

```sh
python -m unittest discover -s tests -p 'test_boundary*.py' -v
python -m experiments.boundary_voting_sweep --write --check
node --test tests/boundary-voting-lab.test.mjs
```

Exact oracles:17 scientific tests + catalog;192 raw/quotient rows;384 pairs of updates;2048 gate-mask/input checks;2560 small-module independent raw fault executions;128 stored traces. The topology formula is checked by polynomial coefficients; the fixed-fixture maintenance comparison is certified on the whole success interval by its affine endpoints.

The lab uses floating projections of the generated Fraction certificate. Its sliders compare a declared six-project portfolio, not all gate circuits. The default portfolio uses the same physical task as v14. The16-state register grammar is a separate exact composition experiment, not an unannounced expansion of the plant.

Offline Playwright/Chromium checks: desktop1440×1100 and mobile390×844; six table rows, three tabs and three manipulated controls; two SVGs; no JS exceptions or horizontal document overflow. Screenshots and logs are in the local additive package. This is not independent live-public-site navigation.
