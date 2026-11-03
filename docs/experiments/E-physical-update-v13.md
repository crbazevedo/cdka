# E-physical-update-v13 — exact continuation-update synthesis

**2026-11-03.** Same v6 plant; explicit SERVICE-first task slice. All state and terminal event parameters remain fixed. Gate capacity is separate from plant energy/resource tokens.

## Reproduce

```sh
python -m unittest discover -s tests -p 'test_physical_update*.py' -v
python -m experiments.physical_update_sweep --write --check
node --test tests/physical-update-lab.test.mjs
python -m http.server 8000 --directory docs
```

## Evidence

14 scientific Python tests plus one catalog/methodology test; six JavaScript tests. Exhaustive gates are checked on all eight readable input rows. An unquotiented netlist oracle agrees through three gates. 24 raw microstate calculations agree with the weighted-interface model. 1092 direct probability evaluations agree with polynomial values. 2814 rational/quadratic interval inequalities certify the optimal frontier for all old-memory errors p∈[0,1/2], with the common affine output channel extending the result to q∈[0,1/2].

The largest search has 64 encoders and 91 realizable truth functions. The signal-set generation has 1,6,33,182,1098 distinct residual construction states through depths 0..4. These are actual small-family counts, not claims of general circuit-synthesis efficiency.

The result includes actual minimal networks (two and four NAND gates) and a false-generalization witness: a wire and two NAND inversions are noiselessly equivalent but respond differently to internal gate flips.

## Local UI validation

The generated standalone HTML was loaded by local Chromium at desktop 1440×1100 and mobile 390×844. Both views rendered two SVGs and eight readable truth-table rows. Three controls were changed and restored; no JavaScript exceptions or document overflow occurred. This is local-byte browser validation, not independent external navigation to the public Pages site.

## Source/provenance

`cdka/physical_update.py`, `tests/test_physical_update.py`, `tests/test_physical_update_catalog.py`, `experiments/physical_update_sweep.py`, `docs/lab/physical-update-core.mjs`. Existing kernel git blob: d2b9ccc2253b326af5d494b6d14c5dac6666105c. The local archived copy differs in comments/formatting; the committed module imports the repository's canonical kernel, whose numeric reference values and raw/macro equality are independently tested.
