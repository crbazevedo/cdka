# CDKA T3/T4 — Finite counterexample synthesis strategy v1

**Objective:** exhibit *marginally feasible but jointly unrealizable* sensing, actuation and repair in a finite organization, and determine the minimal structural obstruction. No originality claim is attached to elementary counterexamples.

## Reverse engineering: start from a desired failure

1. **Target counterfactual:** there exists at least one admissible physical action per world and a working actuator after repair, but *no single nonanticipative physically implementable policy* can select appropriate actions for all worlds.
2. **Disjoint decisions:** choose at least two worlds with incompatible acceptable-action sets; otherwise an unconditional safe action defeats any epistemic no-go.
3. **Marginal witnesses:** establish a physically realizable early observation that distinguishes those worlds, a post-repair actuator capable of both commands with an oracle, and an adequate repair resource budget.
4. **Force a causal bottleneck:** the information must cross a compulsory physical transition (repair, mode switch, deadline or channel interference). It is not enough merely to impose a cost.
5. **Rule out unmodeled bypasses:** policy actions, timing, register values, actuator configurations, resources, environment and durable history can all encode information. Define the **complete physical predecision cut** C.
6. **Certify impossibility:** zero-error support intersection is empty, or quantitative Bayes/TV reliability is below the required threshold.
7. **Demonstrate restoration:** add a physically permitted durable bit, a post-repair sensor, or a compatible safe action. If feasibility cannot be restored, the example may be physically impossible rather than information-limited.
8. **Test and audit:** enumerate all feasible finite-state policies, compare with analytical certificates, and map the result to established theory.

## Ranked candidate structural classes

| Rank | Class | Smallest obstruction | Analysis tool | Falsifier / bypass |
|---|---|---|---|---|
| **A1** | Repair destroys task-relevant physical memory | 2 worlds, 2 incompatible actions, volatile binary bit, compulsory repair | TV/Bayes, finite-state synthesis, memory-channel support | Persistent Z/M bit or post-repair sensing |
| **A2** | State changes after last observation | Binary world flips during repair; no later observation | Markov composition, correlation contraction, belief propagation | Fresh sensing restores correctness |
| **A3** | Mode or deadline noncommutativity | Sensing and acting available, but cannot be sequenced before irreversible deadline | Time-expanded graph, temporal logic, timed automata | Swap deadlines or add storage |
| **B1** | Shared physical resource makes repair + sensing + actuation incompatible | Competing finite resource assignments, each feasible separately | Knapsack / resource-constrained MDP, Pareto frontier | Increase budget or replace substrate |
| **B2** | Action changes future observation authority | Repair/actuation damages sensor or creates new signal | POMDP, dual control, information patterns | Add state-feedback or persistence |
| **B3** | Hidden damage makes repair choice ambiguous | Controller cannot distinguish multiple physical failure modes | Belief DP, viability, Blackwell order | Repair universally valid for all hidden modes |
| **C1** | Multi-attractor repair under rare noise | Action barrier reshapes both failure risk and information accessibility | Freidlin–Wentzell, min-plus exponents, constrained viability | Different causal initial/failure frame |
| **C2** | Distributed memory through actuator/organization | Apparent loss in M but Z or X physically retains a bit | Full causal-cut model, Witsenhausen-style signaling | Omitting action-generated memory (invalid) |

A1 is the first *positive* counterexample because it is exact, independently enumerable, physically interpretable and refutable. C2 is its mandatory adversarial test: it exposes whether our state representation is complete.

## Higher-order compatibility class — a second verified witness

For three worlds with safe-action sets {a,b}, {b,c}, {a,c}, every pair is compatible, while no action is valid for the triple. A compulsory repair maps the entire three-world support to one final memory symbol. Pairwise tests all pass, but no zero-error controller exists; with equal prior the maximal success probability is 2/3.

This construction is a distinct **higher-order hypergraph incompatibility** mechanism, not simply the binary all-or-nothing memory case. It motivates testing full intersections rather than pairwise overlaps. The exact oracle is `higher_order_compatibility_obstruction()` in `cdka/causal_cut.py`.


## Separate analysis instruments (do not conflate them)

**Logical / algebraic**
- Relation R(w,a), compatibility hypergraph and Dowker complex.
- Boolean semiring for zero-error reachability; AND-OR condition for available action and common observation.
- Integer programming and SAT/SMT for finite controller synthesis, minimal obstruction search and unsatisfiable cores.

**Probabilistic / informational**
- Complete terminal channel K(C|W), binary Bayes risk = (1−TV)/2.
- Blackwell garbling and Dobrushin coefficient for memory degradation.
- Data processing and Fano for higher-arity approximate identification; zero-error support tests for hard guarantees.

**Control / time**
- Finite-state controller with explicit physical memory updates and restricted feedback.
- Viability DP and belief-state updates; nonanticipativity and intervention timing.
- Time-expanded causal graph: detect information lost at a cut **before** action availability.

**Organization / resources**
- State-dependent sensors, actuator authority, repair transitions, resource ledger and durability.
- Distinguish no actuator from wrong choice of actuator.
- Include physically visible repair mode, resource count and actuator status as potential memory.

**Physical dynamics (after finite core works)**
- Finite-time Freidlin–Wentzell action, metastable transitions and deadline-specific risks.
- Min-plus log-sum-exp competition between sensor failure and physical escape.
- Do not replace a fixed-frame physical failure event with an action-dependent equilibrium.

**Methodology**
- Direct proof → independent exhaustive oracle → negative controls → prior art.
- Use exact Fractions for finite models, not Monte Carlo.
- Hold causal world, state initialization, deadline and viability event fixed when comparing intervention policies.

## Minimal generator design

Base cardinalities:
- |W|=2, |A|=2, |M|=2 (the deterministic hard-reset case).
- Three physically ordered phases: observe → mandatory repair → terminal act.
- One binary actuator health mode and a one-token resource ledger.
- Sensor functions on {0,1}: exactly two injective maps.
- Repair-memory functions on {0,1}: exactly two noninjective maps.
- Thus 4 elementary deterministic minimal obstructions within this parameterized family.

Extend M to {0,1,⊥} for probabilistic erasure, and allow:
- BSC sensing error η;
- erasure rho in each compulsory unprotected repair;
- environment flip nu during repair;
- n required repairs and B resource tokens;
- optional precommitted per-repair protection, each costing an extra token;
- an explicitly modeled alternative durable physical channel Z.

## Exact proposed experiment grid

1. Enumerate all binary deterministic sensors and repair-memory maps, classify by information capacity and maximum viability.
2. Calculate exact terminal joint P(W_final,M_final) and optimize decoder by independent exhaustive enumeration.
3. Compare the optimum to the TV equality and the analytical horizon/resource law.
4. Enumerate all nonadaptive repair-protection schedules; verify resource threshold and monotonicity in budget within this architecture.
5. Introduce an actuator-configuration bit Z=W and confirm that the memory-only impossibility vanishes.
6. Introduce the universal action U=safe for both contexts and confirm the zero-error support criterion reports no need to distinguish W.
7. Repeat against a new sensor after repair to establish that the obstruction is fundamentally about *when* information becomes available.

## What would count as a genuine theorem beyond the baseline?

A result that characterizes an **architecture-relative, recursively updated causal cut** when organization and repair policies themselves create/destroy/restore physical information channels, with rigorous necessity and sufficiency (or a strict lower bound) and novelty compared to constrained POMDP/team-control theory.

A promising but unproved direction is a state-dependent cut capacity \(\eta_t(C_t,Z_t,R_t)\) coupled to a viable organization kernel, yielding a *joint viability-information frontier* not captured by static pairwise sensor/actuator/repair bounds. Any such statement must survive C2 (physical side-channel memory).

## Hard falsification criteria

- With a universal safe action, a claimed epistemic impossibility must disappear.
- With a durable and readable physical state containing W, a hard-reset no-go must disappear.
- If the controller can freely remember its own action choices, a model claiming perfect erasure while leaving those choices accessible is invalid.
- If post-repair re-observation is available, no inference may pretend information was irreversibly lost.
- If a correctly specified POMDP already yields the same exact theorem, call the result an application, not an original theory.
