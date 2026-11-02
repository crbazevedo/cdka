# E7 — Hidden health and physically costed diagnosis: verification record

**Scientific status:** known Bayes/POMDP instruments specialized to the v6 physical corrector; original novelty unestablished.

- **Python:** `tests/test_hidden_health.py` independently enumerates 162 hidden-health/diagnostic/drift/budget/syndrome combinations, checks twelve categories, and cross-checks two-stage observation-consistent prescriptions. Rational values are exact using `fractions.Fraction`.
- **JavaScript:** `tests/diagnosis.test.mjs` checks six invariant groups and mirrors the default v6 physical payoff rows. Plotting uses floating-point numbers for visualization only.
- **Catalog:** the updated `tests/test_research_options.py` verifies 37 branches, 18 rejected shortcuts, exactly two active branches, valid fallback IDs and browser/source consistency.
- **Generated fixtures:** `experiments/hidden_health_sweep.py` regenerates `docs/lab/diagnosis-fixtures.json` and prints the critical rational thresholds and horizon reference values.
- **Browser:** local Chromium `page.set_content` of `diagnosis_standalone.html` rendered three SVGs in desktop (1440×980) and mobile (390×844), exercised four presets, and found neither JavaScript exceptions nor horizontal overflow. External public-site navigation was **not** tested.

| Exact certificate | Result |
|---|---|
| No health diagnosis, k=0, B=4, fair prior | 0.883319376 |
| Perfect paid diagnosis, d=c=1, B=4 | 0.908929941292 |
| Accuracy threshold | 6402641323/32975801023 ≈ 0.194161813341 |
| B=3, perfect diagnosis but insufficient remaining action resource | zero gain |
| η=.05, ν=.1, age=1 vs age=2 | useful (effective error .14) vs no gain (.212) |
| ζ=.05, perfect diagnostic otherwise | zero net gain |
| Health-hidden vs health-visible relaxation, n=1,2,3 | strict gaps 0.0256106, 0.0421315, 0.0621612 |

**Reproduce** from repo root (requires v6 `cdka/composition.py`):

```bash
python -m unittest discover -s tests -v
python -m experiments.hidden_health_sweep
node --test tests/diagnosis.test.mjs
```

**Scientific limitations:** (i) only two hidden health states and the v6 finite physical kernel; (ii) integer tokens not calibrated joules; (iii) fixed paid program library; (iv) the horizon DP without diagnosis is observation-memoryless with declared stage clock, *not* an unconstrained belief-POMDP; (v) no mathematically new general control theorem is claimed.
