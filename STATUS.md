# CDKA — Research State

**Snapshot:** 2026-11-01 · **Stage:** M0/M1 bootstrap · **Scientific status:** exploratory, no original theorem established.

This file is the operational source of truth. Historical notes are preserved verbatim under `docs/corpus/`; claims in those notes may not yet have undergone a complete prior-art audit.

## Completed and reproducible

- Repository created and the pre-existing v0.1/v0.2 notebooks and v1.0 program archived.
- Ontology distinguishes possibility, prediction, influence, informed control, action sufficiency, counterfactual knowledge, viability, and operational autonomy.
- **B1 (known baseline):** exact finite-state action-code cardinality is minimum set cover; worst-case fixed-width bits = ceil(log2 k). Not Shannon mutual information.
- **T1 (elementary example):** for the globally stable ODE `dx/dt=-x+lambda*w+u`, `w,u∈{-1,+1}`, `x(0)=0`, safety `|x(t)|≤1.5` for all t≥0, minimum decision-code cardinality is 1 (λ≤0.5), 2 (0.5<λ≤2.5), or infeasible (λ>2.5). Thus decision-memory thresholds need not coincide with attractor bifurcations.
- - **E0.1:** finite decision horizon shifts T1 thresholds by `B_T=(3/2)/(1-exp(-T))`; adding a neutral action can lower required memory. Verified by three new tests.\n- Independent finite checks compare set-cover enumeration with partition enumeration over **all 512 binary 3-world × 3-action relations**.
- B1/T1 are not claimed as original scientific contributions.

## In preparation, not established

- **T2:** relation between large-deviation failure barriers and the action-compatibility cover; basic finite corollary drafted, novelty requires dynamic extensions.
- **T3:** joint feasibility frontier for information, trajectory intervention, and organization-maintenance budgets.
- **T4:** recursively sufficient information when sensing, action authority, resources and repair evolve.
- **T5:** causal criteria to distinguish internal autonomy from external replay.
- **T6:** replicator dynamics as functional distributed memory, conditional on earlier gates.

## Blocking questions

1. Can any extension of T1/T2 escape straightforward composition of known viability, rate-distortion and large-deviation results?
2. Which structural constraints make the information/control/repair feasibility region nonseparable?
3. Can organizational boundaries and maintenance criteria be operationally specified without presupposing an externally assigned purpose?
4. Which causal interventions identify self-maintenance beyond observationally matched external replay?

## Next research gate — M0/M1

- Audit prior art and maintain exact claim-to-source mapping.
- Formalize observation-limited and horizon-dependent action sufficiency.
- Identify a small model with shared sensing/actuation/repair resources for T3 and search for a nontrivial lower bound.
- Ensure the deterministic examples and negative controls remain reproducible.

**Evidence rule:** Passing numerical tests supports implementation correctness on tested cases; it does not prove general theorems or novelty.
