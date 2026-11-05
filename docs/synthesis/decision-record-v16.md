# Decision record — CDKA v16, 2026-11-05

## What was retained

The v15 six-NAND topology, healthy/degraded error calibrations, explicit hidden maintenance outcome, joint noise dependence and rule that no failure trajectory receives resources. Historical ledger entries are not edited.

## What was changed, deliberately

A new recurrent task replaces the former one-shot terminal comparison. The same physical bank makes a maintenance choice, may be restored, performs work, earns resources on success, writes a noisy diagnostic and ages. Its performance numbers must not be compared directly with v15's two-stage survival benchmark.

## Why this was the next move

The previous program had separate certified pieces but not one recurrent process closing their operational dependencies. Adding more gates or a different noise family would not answer that missing question.

## Hypotheses set before the policy ranking

H1: a diagnosis-based stationary program can outperform both no maintenance and always-maintain in the fixed finite library.
H2: repeated noisy diagnostic writing induces a compact stochastic interface even though physical-state histories are large.
H3: the loop can remain pathwise resource-feasible while still having zero infinite-horizon survival under a uniform fatal task error.

All three held in the declared fixture; H2/H3 have algebraic proofs under explicit assumptions. H1 is an exact finite-library comparison at eight cycles, not a generic theorem about condition-based maintenance.

## What changed our understanding

Maintenance is not merely a resource benefit: on a healthy bank it adds procedural risk without improving the task channel. A stale report and a currently false report can have different physical routes. Even uninformative report cells do not eliminate state-dependence caused by a hidden faulty circuit itself. This separates knowledge in the representation from causal adaptation due to embodiment.

## What was not solved

The resource guard/routing and sensor calibration are not self-maintained. The16-program library has no arbitrary history recall or clock-dependent switching. Acquisition and basic operation share an explicit common token bundle; a different library could save diagnosis costs for blind programs. Full economic hardware optimality, thermodynamic closure, general agency and indefinite survival are not claimed.

## Next decision criterion

Do not add another component before testing whether an acquisition/retention choice preserves common stochastic emission. If not, retain the smallest physically meaningful dependence exposed by the counterexample. Keep the simple raw oracle and charge construction/certification cost separately from the reduced query cost.
