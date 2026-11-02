# E10 — Exact joint coding, template caps and paid implementation

**Scope:** v6 plant and v9 sensor/continuation law remain unchanged; two diagnostic bit errors precede the first action. No claim that initial transport solves recurrent memory maintenance.

## Exact checks

- Canonical git blob hashes of `composition.py` and `continuation_interfaces.py`.
- Every small joint program: 64 encoders × 81 decoders after a proved library reduction.
- 486 distinct integer-coefficient polynomials and 1,458 exact interval dominance checks, using quadratic-radical signs and rational interior vertices.
- Independent decoder enumeration at four rational errors; no reuse of the portfolio optimizer.
- Full 64-plan library vs the three-plan hull under one/two-slot constraints on three code/noise fixtures.
- Noiseless equality and noisy inequality under arbitrary symbol relabeling; XOR translations as positive symmetries.
- Complete raw three-cell transition oracle for the physical value of the selected code.
- Installation/resource conservation, invalid input checks, and an unequal-program-cost counterexample to inappropriate pruning.
- Mutual information comparison against survival without changing the prior or physical task.

14 Python tests plus one immutable-ledger test; seven JavaScript tests including 101 browser-synthesis/envelope comparisons. Browser arithmetic is floating point; analytical claims come from the exact Python certificate, not the plot.

## Browser inspection

Offline Chromium rendered the standalone bytes at 1440×1100 and 390×844. Four range controls, two zoom buttons and reset were exercised. Two accessible SVG figures, no JavaScript errors and no horizontal overflow. This is local rendering, not independently observed public-site navigation. Exact browser report and screenshots are in the downloadable evidence bundle.

## Reproduction

```bash
python -m unittest discover -s tests -p 'test_joint_compilation.py' -v
python -m experiments.joint_compilation_sweep
node --test tests/joint-compilation.test.mjs
```

`python -m experiments.joint_compilation_sweep --write` regenerates the exact certificate and floating browser data from the physical kernel.
