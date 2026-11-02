# Verification record — CDKA diagnostic transport v8

## Scope

Generated local package and repository additions for T4.I/T3.H. Classical Bayes/FSC tools; tests do not establish novelty or prove a general autonomy statement.

## Exact calculations

- 18 Python research tests; 486 sensor/repair/selector/driver parameter evaluations against independent joint-state propagation and all eight terminal decoders.
- 80 nonzero correlated live-mass fixtures verify the general decision-margin identity without independent H/S assumptions.
- 125 three-signal margin fixtures compare the sign encoder with all binary encoders and decoders.
- Nested v7 physical event, resource reservation, hidden-selector repair, correlation, action-generated memory bypass, time expiry and nonrecursive compression counterexamples are tested.
- One separate catalog test preserves the exact v7 base blob and checks v8 fallback links/counts.

## Browser mathematics

Eight Node tests compare floats against Fraction-generated budget/expiry fixtures, nested v7 values, fault semantics, monotonic physical upgrades and invalid contracts. `node --test tests/transport.test.mjs`.

## Offline browser QA

Chromium rendered the generated standalone HTML bytes using Playwright set_content, at 1440×1100 and 390×844. Four SVGs were rendered; nine controls and reset were exercised. No JavaScript exceptions or horizontal overflow were observed. These are offline checks; a GitHub Pages deployment result is not a substitute for external live browser testing.

The standalone and screenshots are retained in the conversation additive ZIP. Online source is `docs/lab/diagnostic_transport.html` plus `transport-core.mjs` and `transport-app.mjs`.

## Reproduction

```bash
python -m unittest discover -s tests -p 'test_diagnostic_transport.py' -v
python -m unittest discover -s tests -p 'test_transport_catalog.py' -v
python -m experiments.diagnostic_transport_sweep
node --test tests/transport.test.mjs
python -m http.server 8000 --directory docs
```

The scientific tests import the original v6 physical kernel from `cdka/composition.py`; the additive package is meant to be applied to an existing CDKA checkout, not treated as an unrelated complete repository.
