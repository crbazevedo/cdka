# CDKA Proof Engine v3 — From repaired memory to recurrent physical policies

**Research status:** exact finite-family results, known analytical tools, originality unestablished. This document complements rather than overwrites prior notebooks. It advances issue #9 from a precommitted repair schedule to observation-contingent physical repair and an explicit recurrent action/resource loop.

## Strategic thesis

The next claim must quantify over **one implementable policy** that simultaneously preserves task-relevant distinctions, actuator authority and the physical capacity to repeat the process. Separate witnesses for sensing, actuation and repair are not a joint design. Conversely, studying a single fixed repair mode misses information carried by the choice of mode itself.

The object is therefore the *policy-constrained set of unnormalized viable trajectory laws*, not a universal scalar intelligence score.

## Backward chain of proof obligations

1. **Required behavior:** guarantee survival over a horizon and explicitly declare whether the guarantee is mean, worst-context, chance-constrained, or zero-error.
2. **Shared policy:** the same physical mechanism must handle all contexts; no hidden W, no forgotten history, no free persistent seed.
3. **Complete cut:** specify which M, Z, resources and clock values can be read at every step.
4. **Controlled channels:** derive `K_pi` from physical kernels and actual observation-dependent actions. Do not use `sup_a delta(K^a)` as a feedback bound.
5. **Unnormalized dynamics:** propagate failure mass. Perfect information conditional on survival is not a survival guarantee.
6. **Recursion:** solve occupancy-design DP or observation-consistent invariant synthesis; compare to a fully informed relaxation.
7. **Constructive attainment:** provide a physical prescription and resource cycle attaining the bound, not only an upper bound.
8. **Adversarial changes:** add a writable durable bit, an independent persistent seed, or a direct observation, and verify whether the proposed impossibility disappears.
9. **Novelty audit:** map every theorem to its strongest antecedent before labeling it original.

## Executed layer and discoveries

| Result | Instrument / proof | What it reveals | What it enables |
|---|---|---|---|
| Policy-aware contraction envelope | Convexity of TV; maxima at row vertices | Erasing fixed modes can form an information-preserving closed loop | Exact bounded channel oracle and geometric certificates |
| Live-mass terminal value | Positive measures; `max(x,y)` identity | One bit among survivors can coexist with near-total failure | Safety-correct recursion and diagnostics |
| Physical occupancy recursion | Matrix products, prescriptions, induction | Offline planning state must not be handed to runtime controller | Exact bounded-controller design oracle |
| Recurrent repair frontier | Binary decoder dichotomy, products, Pareto order | Mean survival may optimize by abandoning a context | Objective audit; robust rather than merely mean design |
| Fresh versus persistent randomness | Physical memory accounting, mixture argument | A durable independent random bit can change the robust feasible set | Adversarial tests against implicit free memory |
| Zero-error recurrence | Support graphs, greatest invariant set, Boolean implications | Per-context safe policies do not necessarily share a common implementation | SAT/MILP certificates and minimal unsatisfiable cores |
| Noise/horizon collapse | Derivatives and infinite products | Error budget must shrink with required lifetime | Quantitative requirements for physically sustained repair fidelity |

## Tactics: keep analysis tools separated

### A. Algebra of channels (one step)

Use convex row sets and total variation; compute exact envelopes by enumerating extreme actions. Distinguish information transport from information acquisition. Resource-coupled prescription constraints may break rectangularity, so the row envelope becomes a relaxation.

### B. Algebra of organization (multiple steps)

Use sub-stochastic positive kernels over `(W,C)` and observation-consistent prescriptions. Derive value functions as upper envelopes of linear forms. Use exact occupancy recursion for bounded horizons and support invariants for stationary zero-error safety. The optimizer's occupancy is not an agent's hidden memory.

### C. Optimization geometry

Work with **per-context viability vectors** before selecting a scalar criterion. Compute deterministic Pareto points, then distinguish behaviorally attainable points from mixtures that require extra physical state. An average-optimal solution can sacrifice a whole class of contexts.

### D. Calculus and asymptotics

For the proven renewal model `V_robust=(1-p)^n`, use sensitivity `-n(1-p)^(n-1)`, the exact tolerance `p≤1-(1-alpha)^(1/n)`, and `np→tau` collapse. For varying error probabilities, use infinite-product criteria. For a later physical model replace p by a derived finite-time failure law, not an arbitrary quasipotential approximation.

### E. Verification

Analytical proof → independently structured exact oracle → full-state relaxation → adversarial architecture change → browser visualization. Finite exact tests do not prove a general theorem or its novelty.

## Operational deliverables completed in this increment

- `cdka/policy_cuts.py`: exact channel, live-mass, occupancy-design, stationary invariant, and regenerative control tools.
- `tests/test_policy_cuts.py`: independent tests including 729 channel architectures and 1,875 randomized local laws.
- `experiments/policy_cuts_sweep.py`: exact data export and independent certificates.
- `docs/results/T3D-policy-aware-cuts.md`: complete assumptions and proofs for the channel and live-mass layer.
- `docs/results/T4C-recursive-physical-viability.md`: physical state machine, recursive solver, Pareto/robust/mean laws, durable-seed counterexample, recurrence certificates and asymptotics.
- `docs/articles/T3D.md`, `docs/articles/T4C.md`: short pedagogical articles.
- `docs/lab/policy_cuts.html`: a minimal interactive instrument for attainable channel rows, viable profiles and long-horizon reliability.

## Next prioritized reformulations

### R1 — Physically constrained prescription sets

Current exact channel envelopes permit independent choices per physical observation. Real circuits and shared resources may couple those choices. Replace the rectangular set by a finite implementability relation `Phi(Z,R)` and derive sharp bounds from its vertex/constraint structure. Find the smallest case where the unconstrained row envelope is strictly optimistic although every individual row action is feasible.

**Candidates:** finite Boolean circuits with limited persistent modes; costly rewiring; repair actions that share a substrate; read-only versus writable protected memory.

**Analysis:** 0–1 programming, support hypergraphs, transportation of posterior distinctions, controlled bisimulation. Prove either an exact decomposition or an irreducible coupling certificate.

### R2 — Fidelity is produced, not freely scheduled

Give the organization a finite resource/health state and let repair error depend on its action and current resource. Environmental interaction replenishes some, but not necessarily all, of what repair consumes. Derive a stationary viable information/energy cycle or prove its absence. Do not insert a summable `p_t` sequence unless a physical mechanism can generate it.

**Initial theorem target:** under an explicit positive error floor at every reachable repair cycle, no robust indefinite survival of both incompatible contexts is possible in a stated class. Then characterize the minimal sensing/redundancy/reconfiguration operation that breaks the obstruction.

### R3 — Compensating sensing and information generation

Allow new observations after repairs. Then `W→C→C'` need not hold; contraction-only analyses are inapplicable. Decompose the step into information-preserving transport, controlled physical transition, and an acquisition channel with a stated resource cost. Check data-processing and likelihood-ratio recursions rather than assuming information is conserved.

### R4 — Higher-order incompatibility and variable environments

Move beyond a static binary world. Use B1's action-compatibility hypergraph and full support intersections. Explore when an organizational change merges contexts that were pairwise compatible but jointly incompatible. Control the hidden state's transitions and the physical memory substrate in the same kernel.

## A useful boundary on the research claim

We now have a **working proof-and-synthesis apparatus**, plus explicit failures of several plausible simplifications. We do not yet have a theorem establishing spontaneous agency or a generally new control law. The genuine opportunity is a compositional theorem for viable, physically implementable information architectures with endogenous upkeep—not republishing occupancy MDPs under another name.

## Targeted return to least action

A useful next model is a repair-writing operation implemented by a bistable degree of freedom, with a common initial distribution, common deadline and fixed error event across candidate interventions. Derive its actual `p(error)` or a controlled asymptotic bound. Insert that physical fidelity into the already proved recurrent formula, without inserting free memory, clocks or random seeds.

Under the explicit exponential surrogate `p=exp(-J_rep/epsilon)`, the horizon constraint is `J_rep ≥ -epsilon log(1-(1-alpha)^(1/n))`, asymptotically logarithmic in n. This sets a concrete proof target: can an endogenously resource-limited organization supply the required increasing action barrier, or does physical saturation imply a maximum reliable operational lifetime? Large-deviation prefactors and joint limits are the immediate technical danger, not a reason to equate action with energy.
