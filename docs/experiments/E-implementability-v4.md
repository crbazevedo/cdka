# E-v4 — Verification of implementability and funded fidelity

## Local checks actually executed

- 14 new Python unittest tests passed, standard library only for the shipped model. They include 3,675 exact-rational selector/decoder/noise laws, 125 constructive erasure-interface triples, a separate two-cycle randomized-law enumeration, finite-grid DP vs independent weak compositions, derivative finite differences, tangent-envelope upper certificates, budget inversion, n log n scaling and harvesting prefix conservation.
- 6 JavaScript kernel tests passed in Node: curvature/tangency constants, complementarity, scarce-budget theorem, global grid values below the envelope, resource conservation/rate convergence, and contrast-limited per-cycle viability.
- Chromium rendered the generated standalone bytes using set_content at desktop 1440x1100 and mobile 390x844. Five SVGs rendered; every slider and both presets were exercised. No pageerror, NaN or horizontal overflow. These were offline artifact checks, not public-site navigation.
- The theorem on continuous optimization is proved analytically only in its declared regimes. The DP is globally optimal on its integer resource grid, not a continuum optimality claim.
- Exponential effort/noise laws are assumptions; no energy-in-joules calibration was tested.

## Reproduce in repository

```bash
python -m unittest discover -s tests -v
python -m experiments.implementability_sweep
node --test tests/implementability.test.mjs
python3 -m http.server 8000 --directory docs
```

Navigate to `/lab/implementability.html` on the local server. The GitHub workflow runs the mathematical tests and source syntax checks after the commit; its result must be checked separately rather than inferred from local success.

## Numerical certificates

- r_inflection = 1.06959999347914.
- r_tangent = 1.96872832139036.
- For n=4,R=1: best = 0.0721761326091; uniform = 0.0660238920016.
- For target beta=.9: R_min(10)=91.0586754244, R_min(100)=1371.1074656280, R_min(1000)=18316.2452088886.

Evidence files and standalone offline laboratory accompany the downloadable v4 package; screenshots are not proofs of mathematical validity.
