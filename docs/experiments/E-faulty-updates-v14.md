# E-faulty-updates-v14 — exact noisy NAND synthesis

The same v13 task is used; only internal independent gate flips are added. Physical node IDs preserve duplicate gates and fanout. All numbers are reproducible by

```sh
python -m unittest discover -s tests -p 'test_faulty*.py' -v
python -m experiments.faulty_update_sweep --write --check
node --test tests/faulty-update-lab.test.mjs
```

15 scientific Python tests plus one additive-ledger test; seven JavaScript tests.12,395 rooted netlists,611 conditional channel/cost classes,39,104 encoding/channel programs,8,854 exact polynomial interval comparisons,3,120 independent scalar bit executions and128 complete conditional gate-fault traces.

The continuous optimum certificate is specifically p=.01, gamma∈[0,.01], capacity<=4, before re-comparing the common q-latch with bypass. Other browser points are complete-library floating-point exploration, reproducible with exact rational Python synthesis.

Offline Chromium rendered desktop1440×1100 and mobile390×844. Two SVGs and16 conditional trace rows were checked; four range inputs and one trace selector were exercised and restored. No page exceptions or horizontal document overflow occurred. These are local generated-byte tests, not live-public-site navigation. CI and Pages status are recorded separately after commit.
