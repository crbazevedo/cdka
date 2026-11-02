# CDKA — Research State

**Active gate:** G2/G3 — physically funded reconfiguration, fault support and complete-controller viability. **Current increment:** Proof Engine v5, T3.F / T4.E–F. **Originality:** none established beyond scoped model-specific derivations with classical tools.

[Proof Engine v5](docs/strategy/proof-engine-v5.md) · [Miniarticle](docs/articles/T3F-T4F.md) · [Interactive laboratory](docs/lab/reconfiguration.html) · [Verification](docs/experiments/E-reconfiguration-v5.md) · [v5 result register](registry/v5-results.md).

The prior operational snapshot is preserved byte-for-byte at [status-before-v5](docs/corpus/status-before-proof-engine-v5.md) and in the immutable [pre-v5 root STATUS](https://github.com/crbazevedo/cdka/blob/b8a3b75ddd6d33a793be4c475abeced337fe9e54/STATUS.md). Earlier proof notes, notebooks and laboratories remain intact.

## Demonstrated in v5

1. **Joint noise matters.** XOR cascade failure is a+b-2t under the full Frechet interval. Perfectly correlated errors can cancel in a cascade but defeat majority redundancy. Local error marginals alone do not determine the task's failure law. [T3.F](docs/results/T3F-dependence-and-error-topology.md).
2. **Correction versus rarity.** Three-bit repetition with an ideal majority/rewrite mechanism and at most one upset per epoch yields a non-killing logical support. Independent positive bit noise reintroduces fatal masks, so finite-life improvement does not imply infinite survival. This is classical coding under explicit fault assumptions, not a physically perfect corrector theorem.
3. **Complete-controller support theorem.** For a fixed finite physical policy, infinite survival equals the probability of reaching a closed non-killing support before failure. Positive survival does not require initial membership in that support. Exact rational linear systems provide values. [T4.E](docs/results/T4E-recoverable-faults-and-support.md).
4. **Repairable redundancy.** A two-component damage/repair kernel has exact mean lifetime [d(3-2d)+r(1-d)]/{d^2[(2-d)-r(1-d)]}. At d=.01,r=1 this is 10,198 epochs, yet infinite survival is zero. Its spectral radius and support are independently checked.
5. **Switching falsifies mode-wise no-go.** A=[[0,1],[0,0]], B=[[0,0],[1,0]] are each nilpotent, but AB preserves a state. A realizable switching mechanism/clock must be part of the architecture; averaging or analyzing only fixed modes misses the closed-loop support.
6. **Financed reconfiguration.** A finite reservoir funds reliability during operation or pays to install a new architecture. Resource arrives only after a correct intervention. Bellman optimization and an exact monotone-resource DAG characterize finite and indefinite values. [T4.F](docs/results/T4F-financed-reconfiguration.md).
7. **Earliest is not optimal in the example.** With C=K=8,h=5,s=.9 and a truly safe new support, the optimal old effort sequence is 0,3,4 then install: survival 489177/1310720=0.373212432861328125, compared to .3515625 for the earliest installation route. This is exact within the symmetric, context-blind budget macro-library, not universal over all controllers.
8. **Min-plus instrument.** Negative log success turns installation reachability into an additive shortest-path problem. A rare-failure action exponent is not the same as negative log success. The finite-to-infinite certificate is 0<=V_n-R<=q_C^n when the upgraded support is safe.

## Verification

20 new Python tests, with exact Fraction arithmetic: 165 joint error laws; 42 damage/repair configurations; 435 finite-horizon comparisons against independent path enumeration; complete stationary-policy enumeration for small finite reservoirs; explicit support, switching and resource-prefix falsifiers. Eight JS tests mirror the mathematical browser kernels.

Offline Chromium at 1440x1050 and 390x844 rendered and exercised the generated standalone laboratory, with no JavaScript exceptions or horizontal overflow. Those are local-byte checks, not public-site navigation. CI and Pages status are reported separately by GitHub Actions after this commit.

Files: `cdka/reconfiguration.py`, `tests/test_reconfiguration.py`, `experiments/reconfiguration_sweep.py`, `tests/reconfiguration.test.mjs`, three proof notes, a miniarticle and `docs/lab/reconfiguration.html`.

## Retained foundations

[Main result register](registry/hypotheses.md) · [v4 results](registry/v4-results.md) · [Proof Engine v4](docs/strategy/proof-engine-v4.md) · [T3.E implementability](docs/results/T3E-implementable-prescriptions.md) · [T4.D produced fidelity](docs/results/T4D-produced-fidelity-budgets.md) · [T4.C physical recurrence](docs/results/T4C-recursive-physical-viability.md) · [T3.D policy-aware cuts](docs/results/T3D-policy-aware-cuts.md) · [T2 physical action](docs/results/T2-time-constrained-action.md).

## Next proof gates

**R5.1:** model the fallible corrector and its own maintenance, rather than placing an ideal external supervisor inside the supposedly autonomous organization.

**R5.2:** identify the minimum cost of creating a reachable, knowledge-compatible recurrent component under a single physically implementable policy; compare to consumption POMDPs, FSC synthesis and energy games.

**R5.3:** allow the hidden world to change and charge for new information; preserving a static bit is not maintaining correct knowledge of a changing environment.

**R5.4:** seek a compositional certificate connecting action-compatibility supports, implementability and resource-causal upkeep that is not merely a restatement of a standard whole-system POMDP calculation.

All claims remain relative to initial state, error support/correlations, observations, controller memory/clock/randomness, feasible interventions, resource law, horizon and viability criterion. General spontaneous agency or intention is not established.
