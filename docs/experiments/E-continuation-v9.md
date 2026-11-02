# E9 — Continuation-interface proof and verification record

**Date:** 2026-11-02. **Baseline:** `b0176b3d6fbdded67caad1cbe5cb4ae4521a5d1a`.

## Model integrity

The physical kernel is the existing v6 `cdka/composition.py`, git blob `d2b9ccc2253b326af5d494b6d14c5dac6666105c`. Initial syndrome, balance, costs and failure event remain fixed. Only the initial diagnostic encoding and decision horizon vary. No hidden health, designer posterior or unrecorded diagnostic is passed to runtime. Three diagnostic code states do not mean three bits or three total controller states.

## Exact checks executed locally

- 16 scientific Python tests plus one historical-catalog test: 17 passing.
- All 64 complete two-epoch plans evaluated for two initial hidden-health states, independently using raw cell-bit masks (128 coordinate comparisons).
- Rational upper-hull intersections; each active plan dominates every competitor at both endpoints of its interval, certifying the continuous interval. An additional 201-point grid checks implementation only.
- Exhaustive labeled encoders for capacities 1,2,3 on four diagnostic laws: 144 encoding comparisons against the canonical partition solver.
- Common-maximizer zero-loss equivalence, unnormalized Bellman residual decomposition, physically impossible memory updates, durable-diagnostic bypass, restricted decoder library and zero-mass controls.
- Immutable base-ledger and v8-addendum Git blob hashes; 37 branches, 23 distinct rejected claims, R11/R14 only active.
- 8 JavaScript tests against exact rational fixtures. `python -m experiments.continuation_sweep --check` verifies generated browser data byte-for-byte.

The v8 addendum read from its prior additive archive had different whitespace from the canonical repository blob. The v9 test records the canonical blob `c691c0fa249e14ad7a6aa11fee57bdb5b9a4ad71`; the old repository file is not modified. This is a provenance correction, not a research change.

## Local browser verification

Chromium rendered the generated standalone HTML at 1440×1100 and 390×844. Three SVGs, four controls and three presets were exercised; no JavaScript exceptions or horizontal overflow. The initial number formatter incorrectly stripped integer trailing zeroes and was corrected before the final render (100 must remain 100%). Screenshots and the report are in the downloadable evidence package.

Browser checks used `set_content` on exact generated local bytes. They do NOT establish public-site navigation. GitHub CI/Pages outcomes are recorded separately after commit; no future successful run is assumed in this note.

## Reproduce in a checkout

```sh
python -m unittest discover -s tests -p 'test_continuation*.py' -v
python -m experiments.continuation_sweep
python -m experiments.continuation_sweep --check
node --test tests/continuation.test.mjs
python -m http.server 8000 --directory docs
# browser: http://localhost:8000/lab/continuation.html
```

## Interpretation limit

Tests verify implementations and witnesses. Generality comes from the written assumptions/proofs, and originality requires a separate audit. Value-directed POMDP compression and approximate information states are direct predecessors. The measured third-code improvement is 0.0281117058 percentage point; no physical value-for-cost claim follows.
