# CDKA — Research State

**Snapshot:** 2026-11-01 · **Active gate:** G1 analytic foundations → G2 endogenous capability constraints. **Original theorem claims:** none verified.

This is the operational source of truth. Historical notebooks under [docs/corpus](docs/corpus) remain preserved separately. Re-deriving a classical theorem in CDKA's language is not, by itself, an original contribution.

## Working scientific chain

Physical organization and available interventions → realizable trajectory laws → finite-time failure action → safe-action compatibility → information needed for choices → future organization/repair. See [Proof Engine v1.0](docs/strategy/proof-engine-v1.md) and [minimum instrument index](docs/strategy/instrument-index.md).

## Demonstrated and checked — known theoretical instruments

- **B1:** fixed-size zero-error decision code equals minimum safe-action set cover; exhaustive 512 binary 3×3 relations checked against independent partition enumeration.
- **T1:** information threshold without a physical attractor bifurcation; time-horizon and actuator-repertoire variants. [Proof](docs/results/T1-threshold.md).
- **T1.B:** under average binary Hamming risk δ, Shannon mutual information required is \(1-h_2(\delta)\) rather than a universal hard 1-bit requirement. [Explanation](docs/results/T1-soft-information.md).
- **T2.A:** exact *finite-time* Freidlin–Wentzell action for a quartic gradient by Euler–Lagrange first integral and scalar quadrature. \(\Delta U=0.25\) at u=0, \(J_1\approx0.393877\). An OU reachability Gramian provides an independent exact benchmark. [Derivation](docs/results/T2-time-constrained-action.md).
- **T2.B:** saddle-node barrier \(\Delta U\sim[4/(3\,3^{1/4})]\delta^{3/2}\), while fixed-deadline action \(J_T\sim\delta/(\sqrt3 T)\); critical nonuniformity cautions against blind Eyring–Kramers extrapolation. [Proof](docs/results/T2-saddle-node-scaling.md).
- **T2.C:** normalized action-collapse for fixed positive scaled time \(\tau=3^{1/4}T\sqrt\delta\), via 1D implicit-quadrature continuity; numerical convergence verified. [Proof](docs/results/T2-critical-collapse-proof.md). This is a classical-model result; prior-art novelty not established.
- **T3.A:** exact restricted-actuator KL gap: physically realizable intervention cost can strictly exceed the universal binary-event data-processing bound. [Proof](docs/results/T3-causal-authority-gap.md). This is a known informational phenomenon.
- **T4.A:** controlled lumpability supplies a sufficient condition for a compressed representation to preserve recursive viability DP. One-step action sufficiency does not guarantee horizon sufficiency. [Proof](docs/results/T4-controlled-lumpability.md). Known principle.
- **Reproducibility:** \`cdka/finite.py\`, \`cdka/variational.py\`, \`tests/test_finite.py\`, \`tests/test_variational.py\`, GitHub Actions.

## Knowledge Atlas

- Seven miniarticles B1 and T1–T6 with seven interactive mathematical visualizations at https://crbazevedo.github.io/cdka/.
- The atlas explains research status, physical limits, numerical assumptions, and next questions. [Article and visual contract](docs/lab/ARTICLE_STANDARD.md).
- Public deployment and CI have succeeded; external browser/mobile QA is tracked by [issue #8](https://github.com/crbazevedo/cdka/issues/8).

## Unresolved / potentially original

1. **T2→information:** build the *time-constrained physical* compatibility relation \(R_{T,c}(w,a)\) from bistable rates, including observation and action constraints. Show code threshold surfaces and exact boundary behavior; a plain FW+set-cover composition is NOT novelty.
2. **T3 joint authority and resources:** prove or refute a **nonseparable** feasibility bound for sensing, acting, and sustaining the mechanisms that supply those capacities. Compare to constrained KL control and dual control.
3. **T4 recursive knowledge:** incorporate endogenous deterioration/recovery of sensors, memory and actuators; contrast minimal one-shot code with implementable recursive information states and existing POMDP/viability theorems.
4. **T5 causal autonomy:** specify identifiable mechanism interventions and constitutive viability criteria robust to external replay and boundary choice.
5. **T6 evolutionary extension:** replicator-mediated memory of selected mechanisms remains deferred pending a demonstrated causal regulatory role.

## Immediate tactical gate

**G1.1:** use analytic \(J_T(w,a)\) to construct explicit safe-action matrices for the left and right metastable wells; determine time/risk code thresholds, including \(J_T=c\) ambiguity and small-noise conditions. Produce a proof, counterexamples, and a diagram.

**G2.1:** construct the smallest finite model with endogenously variable observation and actuation plus repair; enumerate actual admissible policies and contrast joint feasibility with separately sufficient information/action budgets. A successful counterexample or impossibility proof is a better contribution than a large simulation.

**Scientific rule:** Code passing tests verifies implementations on test cases, not general theorems or scientific novelty. Record the latter separately.
