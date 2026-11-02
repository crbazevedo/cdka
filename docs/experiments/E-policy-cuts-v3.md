# E-policy-cuts-v3 — Verification and reproducibility record

## Scope

Exact finite-family derivations in T3.D and T4.C. Code uses Python standard library and `fractions.Fraction`; browser display uses native HTML/CSS/SVG/JavaScript. No claim of original agency theory or an exhaustive literature search.

## Executed independent checks

| Check | Execution / result |
|---|---|
| Python new module suite | 18 tests passing in the isolated local increment |
| Channel-envelope oracle | 729 three-input/two-action binary-output rational architectures, compared with exhaustive deterministic prescriptions |
| Local randomized controller inequalities | 1,875 rational one-cycle laws checked against sum/product bounds |
| Finite-horizon design | Unnormalized occupancy recursion agrees with independent products of per-context cycle profiles |
| Recurrence | Exact support-invariant enumeration distinguishes per-context feasibility from a shared policy |
| JavaScript new kernels | 8 tests passing, including 625 probability-grid channel cases |
| Offline desktop browser | Chromium 1440×1000; three SVGs; no JS error; no horizontal overflow; controls verified |
| Offline mobile browser | Chromium 390×844; three SVGs; no JS error; no horizontal overflow; controls verified |

Browser validation rendered the generated HTML/JS bytes using `page.set_content`, without external navigation. It verifies this artifact's rendering and interactions, **not** public-site delivery or GitHub Pages status. Repository-wide CI and deployment must be checked independently after commit.

## Reproduce the mathematical checks

```bash
python -m unittest discover -s tests -p 'test_policy_cuts.py' -v
python -m experiments.policy_cuts_sweep
node --test tests/policy-cuts.test.mjs
```

To regenerate the exact report:

```bash
python -m experiments.policy_cuts_sweep --output docs/lab/policy-cuts-data.json
```

Local site, from the repository root:

```bash
python3 -m http.server 8000 --directory docs
```

Open `/lab/policy_cuts.html` on that server. The JavaScript modules require HTTP hosting unless bundled for offline rendering. No third-party dependencies are needed by the page.

## Hand-checkable certificates

For repair error p=1/10:

| Cycles | Robust survival | Mean optimum |
|---:|---:|---:|
| 1 | 9/10 | 9/10 |
| 3 | 729/1000 | 729/1000 |
| 6 | 531441/1000000 | 531441/1000000 |
| 7 | 4782969/10000000 | 1/2 |
| 10 | 3486784401/10000000000 | 1/2 |

Each world separately has a stationary controller with zero failure; with p>0 no single controller gives zero-error recurrence for both in the specified architecture. The fully observed relaxation returns 1, revealing why access to hidden W is not an innocuous optimization shortcut.

## Numerical caution

Exact tests use rational probabilities. Smooth browser curves display the proven algebra and may interpolate the horizon for visual continuity; operational cycles are integer. The action-barrier extension is explicitly a surrogate until a physical finite-noise repair law and uniform bounds are established.
