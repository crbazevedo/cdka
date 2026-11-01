# CDKA — Knowledge Article & Visualization Contract v1

Every scientific result, counterexample or live hypothesis in CDKA must have an accessible article and a reproducible visualization. The **scientific claim is primary**, the graphic is an instrument for understanding and refutation.

## Required article structure

1. **Question:** one specific problem, stated without using technical jargon as a substitute for meaning.
2. **Scientific status:** established prior result, proved illustration, corollary, conjecture, exploratory model, or falsified hypothesis.
3. **Motivation:** why the problem matters beyond mathematical elegance and which distinction it resolves.
4. **Minimum definitions:** variables, units, system boundary, horizon, permitted interventions, observations, resources and failure condition.
5. **Central formula:** fully specified hypotheses and quantifiers; separate theorem statement from the example model.
6. **Concrete example:** smallest nontrivial case, with at least one numerical or exact hand-checkable result.
7. **Insight:** what becomes visible, including a negative control or counterexample.
8. **CDKA role:** what this result connects in the program's causal → informational → organizational structure.
9. **Next proof obligation:** what a positive result makes possible, and what would falsify it.
10. **Limits/prior art:** state what is known and what does not follow from the visualization.
11. **Simulation:** controls and an invariant, discontinuity, geometry or asymptotic law to observe.
12. **Reproducibility:** pure model kernel, deterministic tests or declared stochastic seeds, corresponding source locations.

## Figure design principles

**Reveal mechanism, not just a trend.** Prefer diagrams of feasible sets, phase portraits, separatrices, optimal policies, value surfaces, asymptotic rates and counterfactual interventions. Generic dashboard metrics should be secondary.

**Controlled comparisons.** Keep everything but the named intervention fixed. If selecting a variable changes the model class, explicitly warn the reader.

**Honest boundaries.** Mark risk cutoffs, infeasible regions, singular cases and finite-size limitations. Do not interpolate across mathematical discontinuities in ways that imply a physical bifurcation.

**Causal relevance.** Correlation and observational equivalence must not be shown as evidence of internal agency; explicitly compare ablations and external replay.

**Numerical stability.** Check asymptotics independently; use log scales or log-odds coordinates where direct probabilities approach machine precision.

**Accessibility and visual language.** Use an off-white field, dark ink, moss-green main trajectory, muted ochre alternatives and warm rust exceptions; axes carry units and descriptions. Charts have accessible labels and text equivalents. No font downloads or tracking.

**Reader loop.** A user should be able to vary a parameter, predict a qualitative change, observe the figure, read a precise explanation and find the relevant proof or counterexample in under a minute.

## Required implementation gates

- A canonical markdown article under `docs/articles/ID.md`.
- Registered scientific status and hypothesis identifier in `registry/hypotheses.md`.
- Model code under `docs/lab/core.mjs`, presentation under `docs/lab/app.mjs` and a route in `docs/lab/articles.mjs`.
- Tests for boundary values, invariants, negative controls and a smoke render.
- Explicit statement of what result the simulator **does not** prove.
- A prior-art audit before using the phrase "novel theorem".

## Provenance / limitation

The seven current articles are generated from common content objects in `docs/lab/articles.mjs`; their Markdown counterparts are maintained in `docs/articles/`. Keep both in sync when editing. A future improvement is a content generation step that eliminates duplication.
