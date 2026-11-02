# Counterfactual Dynamics of Knowledge and Agency (CDKA)

**Research program · Started 2026-11-01 · Status: exploratory / pre-theorem**

**Question:** Under what conditions can a physical organization acquire, use, and preserve distinctions about the consequences of its own interventions, enabling operational knowledge, control, and autonomy without presupposing teleology?

CDKA investigates the coevolution of physical trajectory distributions, actionable counterfactual distinctions, and the physical organization sustaining sensing, memory, intervention, and repair. The objective is not a universal entropy/agency score; it is a precise set of definitions, impossibility results, sufficient conditions, counterexamples, and reproducible experiments.

**Scientific discipline:** Known results and rediscoveries must be explicitly distinguished from new proven theorems. No novelty or general account of agency has yet been established.

## Interactive research atlas

[Open the published atlas](https://crbazevedo.github.io/cdka/) · [T3.C: interactive causal-cut experiment](https://crbazevedo.github.io/cdka/lab/causal_cut.html) · [Open the atlas source](docs/index.html) · [Read seven mini knowledge articles](docs/articles) · [Simulator methodology](docs/lab/README.md)

To run the interactive site locally: `python3 -m http.server 8000 --directory docs` and open `http://localhost:8000/`. The CDKA atlas was successfully deployed to **[GitHub Pages](https://crbazevedo.github.io/cdka/)** on 2026-11-01. The [Pages workflow run](https://github.com/crbazevedo/cdka/actions/runs/41349166262) confirms deployment; browser-based external smoke checks remain a separate QA step.

## Current research gate — v7 hidden organizational health

**[Interactive T4.H / T3.G research lab](https://crbazevedo.github.io/cdka/lab/diagnosis.html)** · [Proof of diagnosis decision threshold](docs/results/T4H-hidden-health-diagnosis.md) · [Program-implementation cost](docs/results/T3G-physical-selector-cost.md) · [Proof Engine v7](docs/strategy/proof-engine-v7.md).

The new model conceals the corrector's health from runtime policy, prices a noisy diagnostic and a physically implementable conditional selector, and retains the **same** v6 physical action/failure kernel. With a fair prior and sufficient budget, diagnosis improves one-step survival only below the exact effective-error threshold `6402641323/32975801023 ≈ 19.42%`. With B=3 and d=c=1, even a perfect diagnostic cannot fund the contingent `refresh` action; with B=4 the survival gain is 2.561 percentage points. These are scoped decision-theoretic results, not original agency theorems.

The [research option ledger](registry/research-options.md) preserves 37 research paths and 18 rejected shortcuts; R11 and R14 remain the only active proof branches.

## Mathematical proof program

[Proof Engine — strategy and proof gates](docs/strategy/proof-engine-v1.md) · [Minimal mathematical instrument index](docs/strategy/instrument-index.md) · [Finite-time action derivation](docs/results/T2-time-constrained-action.md) · [Critical scaling proof](docs/results/T2-critical-collapse-proof.md) · [Restricted causal authority](docs/results/T3-causal-authority-gap.md) · [Recursive viability quotient](docs/results/T4-controlled-lumpability.md)

The new classical variational and information instruments have independent standard-library Python checks in `cdka/variational.py` and `tests/test_variational.py`. They are not claims of original CDKA theorems.

## Navigate

- [Current research state](STATUS.md)
- [Research program (Portuguese, v1.0)](docs/program/research-program-v1.0.md)
- [Operational ontology](docs/ontology.md)
- [Prior art and novelty register](docs/prior-art.md)
- [Baseline B1: minimum decision code](docs/results/B1-set-cover.md)
- [Candidate T1: informational threshold without a dynamical bifurcation](docs/results/T1-threshold.md)
- [Candidate T2: stochastic action barriers and bits](docs/results/T2-barrier-to-bits.md)
- [Hypothesis register](registry/hypotheses.md)
- [Experiment protocol](docs/experiments/E0-threshold.md)
- [Archived research notebooks](docs/corpus/)

## Finite causal-cut counterexample (T3.C / T4.B)

- [Read the research result and proof](docs/results/T3C-temporal-causal-cut.md).
- [Counterexample-synthesis strategy and ranked structural classes](docs/strategy/finite-counterexample-synthesis-v1.md).
- [Mini knowledge article](docs/articles/T3C.md) and [interactive simulator](docs/lab/causal_cut.html).
- Exact rational finite-policy checks: `python -m unittest tests.test_causal_cut -v`.
- Independent reproduction: `python -m experiments.causal_cut_sweep`.

The result is **not** a new theorem of agency. It exhibits the failure of marginal information/actuation/repair feasibility to guarantee a common physical policy, and shows how physical actuator configuration can bypass a narrowly specified memory bottleneck.

## Reproduce the first result

Requires Python 3.11+; standard library only for the baseline checks.

```bash
python -m unittest discover -s tests -v
python -m experiments.threshold_sweep
```

The initial result is a **teaching/verification lemma**, not a claim of originality: a smoothly parameterized, globally stable system can exhibit discontinuous changes in the minimum information required for robust action selection.

## Knowledge article workflow

The canonical content is maintained in `docs/lab/articles.mjs` and generates the seven Markdown miniarticles. Use `npm run articles:write` after edits; `npm test` checks that all articles, mathematical kernels and SVG renders remain synchronized and reproducible. New research results should follow [the article/visualization contract](docs/lab/ARTICLE_STANDARD.md).

## Research principles

1. Separate possibility, predictability, influence, action sufficiency, counterfactual knowledge, control, viability, and autonomy.
2. Specify system boundaries, horizons, intervention authority, observability, physical budgets, and risks.
3. Derive and test the simplest falsifiable proposition first; write down failure cases.
4. Preserve provenance and record negative results and novelty audits.
5. Treat organizational self-maintenance as a hypothesis to test, not a goal postulated in physics.

The [issues](../../issues) track proof obligations, experiments, and novelty checks.
