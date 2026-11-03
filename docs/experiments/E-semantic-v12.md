# E-semantic-v12 — exact semantic compilation and interface-change tests

**Contract:** same v6 physical kernel; current runtime health hidden. Models and historical ledgers are not replaced.

## Reproduction

```sh
python -m unittest discover -s tests -p 'test_semantic*.py' -v
python -m experiments.semantic_sweep --write
python -m experiments.semantic_sweep --check
node --test tests/semantic-lab.test.mjs
python -m http.server 8000 --directory docs
```

The JSON certificate is generated from committed code rather than edited by hand. GitHub Actions generates it before JavaScript tests and Pages upload.

## Verified locally

17 scientific Python tests plus one research-memory test and seven JavaScript tests. Exact independent comparisons include 85 command words on the 80-state physical plant, all 64 previous two-step plans, 1,488 words across 48 rational systems, five factorized models from 2 to 128 states, and 12 full-rank chain sizes. All closure, quotient and defect certificates use exact Fraction arithmetic.

The full physical command family has rank 20, 20 state-signature classes and 81 candidate vector evaluations. HOLD-only has rank 4 and five evaluations. Repertoire-dependent signatures do not expose hidden health to the runtime controller.

## Visual and interaction QA

The generated standalone HTML was rendered using local-byte Playwright/Chromium `set_content`, at 1440×1100 and 390×844. Three SVGs, three panels and four controls were exercised. No JS exceptions or document overflow occurred. These checks are offline and do not constitute independent navigation to the deployed public URL.

## Negative controls retained

One-step equality versus composite distinction; feedback invalidating blind equivalence; rank two versus 17 distinguishable states; a trace-equivalent pair with no Markov quotient; full-rank delayed-failure chains; nontransitive action compatibility. No claim of universal combinatorial collapse follows.
