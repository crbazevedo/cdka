# E-trace-v11 — Reproducible mechanism inspection

**Baseline commit:** 5f4f6e05f4a83f253c4a9657e282f78acabfb509. The existing physical model and continuation library are imported, not overwritten.

## Executed scope

- Two complete stopped trace trees at p=1/10: 492 paths each, 984 total.
- Exact fractions for original source mass, channel, physical transitions and endpoint events.
- 60 raw physical state/action rows checked against both existing macro and micro kernels.
- 25 complete trace/value comparisons over five noise values and five program witnesses.
- 51 rational points for the harmful-route identity.
- 576 polynomial coefficient checks for continuation-weighted error distance.
- Equal-two-epoch / unequal-three-epoch witness; fixed-policy mediator decomposition; extreme-prior policy-switch falsifier.
- Hidden-state nonleakage, update collision, no continuation after failure and cross-world coupling ambiguity.
- 12 scientific Python tests, one catalog integrity test and six browser-kernel tests.

## Commands

```bash
python -m unittest discover -s tests -p 'test_trace*.py' -v
node --test tests/trace-lab.test.mjs
python -m experiments.trace_sweep --out trace-output --web docs/lab/trace-data.json
python -m http.server 8000 --directory docs
```

The generator exports JSONL with exact weights and stable trace IDs, plus summary and SHA-256 manifest. The Pages workflow generates the same browser dataset from committed source before upload; the large trace file need not be hand-maintained.

## Visual checks

Local Chromium rendering via self-contained HTML at desktop 1440x1100 and mobile 390x844: three SVG figures, trace filters, evaluator toggle, pagination and analytic noise slider. No JavaScript exceptions or horizontal document overflow. Dataset p remains explicitly fixed while the analytic noise slider varies. This is offline byte rendering, not independent public-site navigation.

## Scientific provenance

The trace law is exactly projected to earlier outcome laws. Stops name first failed predicates, not unique actual causes. Expected policy contrasts do not imply a particular individual-level counterfactual coupling. Proof obligations and scholarly antecedents are recorded in T4.L.
