# Counterfactual Dynamics of Knowledge and Agency (CDKA)

**Research program · Started 2026-11-01 · Status: exploratory / pre-theorem**

**Question:** Under what conditions can a physical organization acquire, use, and preserve distinctions about the consequences of its own interventions, enabling operational knowledge, control, and autonomy without presupposing teleology?

CDKA investigates the coevolution of physical trajectory distributions, actionable counterfactual distinctions, and the physical organization sustaining sensing, memory, intervention, and repair. The objective is not a universal entropy/agency score; it is a precise set of definitions, impossibility results, sufficient conditions, counterexamples, and reproducible experiments.

**Scientific discipline:** Known results and rediscoveries must be explicitly distinguished from new proven theorems. No novelty or general account of agency has yet been established.

## Interactive research atlas

[Open the atlas source](docs/index.html) · [Read seven mini knowledge articles](docs/articles) · [Simulator methodology](docs/lab/README.md)

To run the interactive site locally: `python3 -m http.server 8000 --directory docs` and open `http://localhost:8000/`. The Pages workflow is committed, but the live site URL must be confirmed after GitHub Pages is enabled and deployment succeeds.

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

## Reproduce the first result

Requires Python 3.11+; standard library only for the baseline checks.

```bash
python -m unittest discover -s tests -v
python -m experiments.threshold_sweep
```

The initial result is a **teaching/verification lemma**, not a claim of originality: a smoothly parameterized, globally stable system can exhibit discontinuous changes in the minimum information required for robust action selection.

## Research principles

1. Separate possibility, predictability, influence, action sufficiency, counterfactual knowledge, control, viability, and autonomy.
2. Specify system boundaries, horizons, intervention authority, observability, physical budgets, and risks.
3. Derive and test the simplest falsifiable proposition first; write down failure cases.
4. Preserve provenance and record negative results and novelty audits.
5. Treat organizational self-maintenance as a hypothesis to test, not a goal postulated in physics.

The [issues](../../issues) track proof obligations, experiments, and novelty checks.
