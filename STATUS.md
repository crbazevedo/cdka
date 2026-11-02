# CDKA — Research State

**Snapshot:** 2026-11-01 · **Active gate:** G4 — hidden health (R11) + physically costed whole-program implementation (R14). **Novelty:** no general original theorem or proof of autonomous agency established. This snapshot supersedes the [v6 status](docs/corpus/status-before-v7.md) without modifying its original mathematical records.

## Latest executed increment — Proof Engine v7

[Proof Engine v7](docs/strategy/proof-engine-v7.md) · [Research-option catalog (37 branches, 18 rejected)](registry/research-options.md) · [T4.H proof](docs/results/T4H-hidden-health-diagnosis.md) · [T3.G implementation proof](docs/results/T3G-physical-selector-cost.md) · [Interactive laboratory](https://crbazevedo.github.io/cdka/lab/diagnosis.html) · [Verification record](docs/experiments/E-hidden-health-v7.md).

1. **Health is not a free observation:** the v6 quotient `(k,h,b)` remains mathematically exact but the runtime interface becomes only `(k,b)` plus explicitly purchased diagnostic memory. The health-visible Bellman value is now an upper bound, not an implementable policy.
2. **Exact paid diagnosis:** one-step Bayes decision over the original v6 physical kernel with fixed initial state/failure/deadline, health changing with probability ν during a common interval, sensor BSC error η, and a diagnostic failure probability ζ. Joint cost d+c is charged before terminal action. No outcome-dependent budget sidechannel exists.
3. **Decision relevance threshold:** for the fair-prior two-action default, effective error `e=η+ν−2ην` gives improvement `ΔV=0.5 max(0,g−e(g+ℓ))` when affordable and ζ=0. The exact critical error is `6402641323/32975801023 ≈ 0.194161813341`.
4. **Physical program threshold:** with d=c=1 and refresh cost 2, B=3 yields no gain despite perfect diagnosis; B=4 allows a contingent `refresh/hold` controller and increases survival from 0.883319376 to 0.908929941292.
5. **Timing and procedure risk:** sensor error and health drift compose into the effective diagnostic error; old information can be correct about the past yet useless to current action. Procedure failure ζ=.05 eliminates the net benefit of a perfect diagnostic in the default fixture.
6. **Multi-epoch restricted control:** a stage-clock/(k,b) observation-memoryless physical policy reaches 0.883319376, 0.809177960770, 0.738694271130 for horizons 1,2,3, strictly below the health-visible relaxations 0.908929941292, 0.851309438183, 0.800855445804. These are *not* the values of a general belief-based POMDP or a paid diagnostic at every epoch.
7. **Reproducibility:** 12 new Python tests, 6 new JavaScript kernel tests, 162 independent physical diagnosis/decoder cases, an independent two-step policy oracle, exact Fraction arithmetic, and local Chromium desktop/mobile SVG and controls verification (not external public-site browser navigation).

All results use known Bayesian value-of-information, Blackwell/data processing, finite-state controller and inspection-maintenance POMDP instruments; novelty remains unestablished.

## Research memory and dead-end management

**Canonical:** [registry/research-options.json](registry/research-options.json), 37 branches (32 v6 plus five v7 additions) and 18 rejected shortcuts (14 v6 plus four v7). Every branch has hypothesis, evidence, minimal test, reactivation trigger, fallback links, acceptance gate and novelty status. Exactly R11 and R14 are marked active; all previous routes including oscillators, replicators, topological and physical-action calibration remain preserved.

A failed result is classified before redirecting: theorem contradiction, implementation bug, missing physical state/channel, known antecedent, numerical limitation, or vacuous bound. Do not expand two toy models in succession without a new mathematical separation or a predecessor audit.

## Next independent proof gates

**G4.B — R11:** allow health observations to be written into finite physical memory that must survive an intervening repair. Diagnose, act, service and reobserve with a physically limited controller; test whether the designer's posterior can be implemented by a finite register and declare all resource and sidechannel costs.

**G4.C — R14:** make the conditional selector a degrading and repairable physical component. Compare at least two circuit libraries with different program-installation and recurrent upkeep costs, and derive a necessary/sufficient implementation certificate or strict physical value gap.

**G5 — Conditional:** if G4.B/C produce nontrivial joint constraints not exhausted by standard POMDP/FSC methods, seek a compositional viability theorem across sensor, selector, corrector and resource processes, with a physically realizable policy witness and adversarial alternatives.

**Scientific rule:** passing tests demonstrates implementation correctness on tested cases, not mathematical novelty. Any general theorem requires explicit hypotheses, proof, a counterexample search and an independent antecedent audit.

## Retained foundations

All v1–v6 notebooks, proofs, and laboratories remain at their prior paths, including [T4.G compositional contracts](docs/results/T4G-compositional-contracts.md), [T4.F funded reconfiguration](docs/results/T4F-financed-reconfiguration.md), and [T2 physical action](docs/results/T2-time-constrained-action.md). The existing seven canonical atlas articles are unchanged; T4.H is an additional standalone knowledge article.
