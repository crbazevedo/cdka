# CDKA — Atlas de Resultados (microsite)

**Entry point:** [../index.html](../index.html). This interactive atlas complements the canonical [mini articles](../articles) and [proof notes](../results).

## Seven interactive results

| ID | Data visualization | Variables | Scientific status |
|---|---|---|---|
| B1 | Exact set-cover network and higher-order compatibility | Toggle state-action matrix and presets | Known baseline |
| T1 | Horizon–coupling regime map, trajectories | Coupling, horizon, additional neutral action | Proven teaching example |
| T2 | Exact Gaussian risk table and effective large-deviation exponent | Noise, reliability, state/action | Conditional asymptotic corollary |
| T3 | Three-budget allocation simplex and optimal frontier | Budget, reliability target, sensing and repair costs | Illustrative optimization model |
| T4 | DP policy map and survival-vs-horizon curves | Horizon, sensor health, repair tokens, sensor accuracy | Dynamic programming baseline |
| T5 | Observationally matched trajectories and causal divergence | Shock intensity, feedback gain, time | Causal feedback illustration |
| T6 | Replicator phase portrait, vector field and basins | Frequencies, environment, selection and relaxation | Known identity, open interpretation |

The site is implemented using native browser HTML/CSS/SVG and ES modules. No analytics, cookies, tracking, third-party fonts, JavaScript libraries or external graph services are required.

## Local execution

From the repository root:

```bash
python3 -m http.server 8000 --directory docs
# Then open http://localhost:8000/
node --test tests/visual-lab.test.mjs tests/atlas-render.test.mjs
```

A local HTTP server is needed for ES module imports; opening `docs/index.html` directly with `file://` may fail due to browser module restrictions.

## GitHub Pages deployment

A Pages workflow is configured in `.github/workflows/pages.yml` to upload the `docs/` directory. GitHub Pages has been enabled with **Source: GitHub Actions**. The [initial Pages deployment](https://github.com/crbazevedo/cdka/actions/runs/41349166262) succeeded on 2026-11-01. Deployments now run automatically when `docs/**` changes on `main`.

Pages URL reported by GitHub after successful deployment: https://crbazevedo.github.io/cdka/

## Review

- Illustrative models are not proofs of universal agency, nor evidence of a novel theorem.
- All simulator kernels are tested in Node and the finite baseline is cross-checked with an independent exhaustive oracle.
- See [claim status](../../registry/hypotheses.md), [prior art](../prior-art.md), [research state](../../STATUS.md).
