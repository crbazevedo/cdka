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
- **T2.D:** rigorous, causally consistent left/right initial-state comparison under the same fixed failure event and horizon, with 0/1/infeasible decision-code regions at \(T=3\). Thresholds \(c\approx0.269641\) and \(c\approx0.460201\) are numerically verified under strict small-noise margins. [Proof and counterfactual protocol](docs/results/T2-causal-information-phases.md).
- **T3.B:** log-sum-exp yields the reliability exponent \(\min\{J_{\rm good},J_{\rm bad}+\kappa\}\). Sensors may all approach one bit of mutual information while retaining different catastrophic-error exponents. Shared sensing/actuation budget optimum is obtained by equality of two branches in a **fixed causal frame**, with small-budget ratio \(\gamma/(\gamma+2q_T)\). [Derivation](docs/results/T3-fixed-frame-reliability-allocation.md). Not yet endogenous maintenance.
- **T2.C:** normalized action-collapse for fixed positive scaled time \(\tau=3^{1/4}T\sqrt\delta\), via 1D implicit-quadrature continuity; numerical convergence verified. [Proof](docs/results/T2-critical-collapse-proof.md). This is a classical-model result; prior-art novelty not established.
- **T3.A:** exact restricted-actuator KL gap: physically realizable intervention cost can strictly exceed the universal binary-event data-processing bound. [Proof](docs/results/T3-causal-authority-gap.md). This is a known informational phenomenon.
- **T4.A:** controlled lumpability supplies a sufficient condition for a compressed representation to preserve recursive viability DP. One-step action sufficiency does not guarantee horizon sufficiency. [Proof](docs/results/T4-controlled-lumpability.md). Known principle.
- **Reproducibility:** \`cdka/finite.py\`, \`cdka/variational.py\`, \`tests/test_finite.py\`, \`tests/test_variational.py\`, GitHub Actions.

## New finite capability-cut result — T3.C / T4.B

- **Causal-cut obstruction:** a perfect initial sensor and an actionable repaired actuator need not compose into a viable physically implemented policy when a mandatory repair destroys the only usable information channel. Base model: two equiprobable states, mutually incompatible actions, one repair resource; full physical repair but optimal decision success 1/2.
- **Generalized support criterion:** exact zero-error decoder exists iff every reachable terminal physical signal is compatible with at least one common safe action over all states producing that signal. The correct cut includes **M, Z, R, physical traces** — not only an explicit memory register.
- **Binary decision bound:** optimal success is `(1+TV(P(C|W=0),P(C|W=1)))/2` for equal priors and fully available terminal actions.
- **Resource-horizon exact formula:** with B tokens and n mandatory repairs, protected repair cost 2 rather than 1, sensor error η, erasure probability ρ and environment flip probability ν, exact viability equals `[1+(1−2η)(1−2ν)^n(1−ρ)^(n−min(n,B−n))]/2` for B≥n, or 0 for B<n. Protection schedules are precommitted and cannot signal world state.
- **Adversarial bypass:** an observable actuator mode Z carrying the earlier reading restores decision information despite volatile M being erased. No theorem may infer lost knowledge by examining M alone.
- Exact Fraction arithmetic, independent terminal decoder enumeration, all two-bit deterministic sensor/reset map enumeration, 378 parameter cases, and resource schedule enumeration in `cdka/causal_cut.py`, `tests/test_causal_cut.py`.
- [Complete proof and limitations](docs/results/T3C-temporal-causal-cut.md) · [synthesis strategy](docs/strategy/finite-counterexample-synthesis-v1.md) · [miniarticle](docs/articles/T3C.md) · [interactive experiment](docs/lab/causal_cut.html). **Not original**: binary Bayes testing, Dobrushin contraction, Blackwell, finite-state POMDPs.
  
- **Corte de ordem superior:** três contextos com conjuntos de ações {a,b}, {b,c}, {a,c} passam em todos os testes de compatibilidade aos pares, mas não admitem nenhuma ação universal após a memória ser colapsada. Sucesso ótimo para prior uniforme = 2/3. Verificado por `higher_order_compatibility_obstruction()`; antecedente combinatório conhecido.

- **Contraexemplo adversarial de sinalização por reparo:** cada canal de reparo com modo fixo possui coeficiente de contração TV=0, mas selecionar adaptativamente o modo `a=m` cria um canal fechado de coeficiente 1. Enumeradas as quatro políticas binárias; resultado conhecido da informação transmitida por ações, relevante para uma futura formulação dinâmica do corte causal.

## Knowledge Atlas

- Seven canonical miniarticles B1 and T1–T6, plus the standalone T3.C causal-cut miniarticle and interactive experiment, at https://crbazevedo.github.io/cdka/.
- The atlas explains research status, physical limits, numerical assumptions, and next questions. [Article and visual contract](docs/lab/ARTICLE_STANDARD.md).
- Public deployment and CI have succeeded; external browser/mobile QA is tracked by [issue #8](https://github.com/crbazevedo/cdka/issues/8).

## Unresolved / potentially original

1. **T2→information:** build the *time-constrained physical* compatibility relation \(R_{T,c}(w,a)\) from bistable rates, including observation and action constraints. Show code threshold surfaces and exact boundary behavior; a plain FW+set-cover composition is NOT novelty.
2. **T3 joint authority and resources:** prove or refute a **nonseparable** feasibility bound for sensing, acting, and sustaining the mechanisms that supply those capacities. Compare to constrained KL control and dual control.
3. **T4 recursive knowledge:** incorporate endogenous deterioration/recovery of sensors, memory and actuators; contrast minimal one-shot code with implementable recursive information states and existing POMDP/viability theorems.
4. **T5 causal autonomy:** specify identifiable mechanism interventions and constitutive viability criteria robust to external replay and boundary choice.
5. **T6 evolutionary extension:** replicator-mediated memory of selected mechanisms remains deferred pending a demonstrated causal regulatory role.

## Immediate tactical gate

**G1.1:** the fixed-frame T2.D model now yields strict small-noise 0/1/infeasible regimes. Next: finite-noise prefactor checks, risk smoothing, and event-consistent stochastic simulation. Continue to use analytic \(J_T(w,a)\) to construct explicit safe-action matrices for the left and right metastable wells; determine time/risk code thresholds, including \(J_T=c\) ambiguity and small-noise conditions. Produce a proof, counterexamples, and a diagram.

**G2.1:** T3.B now supplies a fixed-frame *externally allocated* sensing/actuation budget with a unique max-min optimum. Next: endogenize and repair resources. Construct the smallest finite model with endogenously variable observation and actuation plus repair; enumerate actual admissible policies and contrast joint feasibility with separately sufficient information/action budgets. A successful counterexample or impossibility proof is a better contribution than a large simulation.

**Scientific rule:** Code passing tests verifies implementations on test cases, not general theorems or scientific novelty. Record the latter separately.
