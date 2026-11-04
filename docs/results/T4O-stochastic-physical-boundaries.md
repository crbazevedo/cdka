# T4.O / T3.K — Noisy physical boundaries, shared faults and executable continuation value

**2026-11-03 · CDKA v14.** Contribution: exact joint synthesis of noisy physical encodings and gate-level implementations for the unchanged SERVICE-first continuation task; an extension-safe stochastic interface contract; a certified topology separation, continuous optimality interval and last-port bound. Established probabilistic-circuit tools enable these adaptations. Priority is evaluated per precise result, separately from correctness, usefulness and fertility.

## 1. Frozen physical and hardware contract

The v6/v13 task is unchanged: three equiprobable diagnostic outcomes with healthy probabilities .01/.5/.99, first action SERVICE, identical physical transitions, resources, failure and deadline. After successful SERVICE, three tokens remain; HOLD and REFRESH are affordable even when commanded by error. The fixed REFRESH bypass has value V_ref=.8091779607700227... and does not use the new update circuit.

The diagnostic is encoded in two cells corrupted independently with probability p. The controller reads only the received word and actual syndrome k. Every installed NAND has a unique physical node identity and fresh independent output flip gamma. A common final latch flips independently with probability q. Fanout reuses the SAME noisy signal; it is not an independent sample. The last output bit alone reaches the command interface. Gate capacity is at most four; initial encoder, wires, constants, readable syndrome and actuator interface remain common primitives. Gamma is a calibrated probability, not a physical energy law. This is a finite single update, not recurrent gate maintenance.

## 2. Why a joint boundary is necessary

Two parent signals U,V each equal one with probability 1-gamma. Shared fanout has U=V; separate parents have independent errors. Their marginals coincide, but P(U=V=1) is respectively 1-gamma and (1-gamma)^2. A fresh noisy NAND, ideally outputting zero, has errors

    e_shared=2 gamma(1-gamma),
    e_separate=gamma+(1-2 gamma)(2 gamma-gamma^2).

At gamma=.1: .18 versus .252. The witnesses have two/three gates: a mechanism comparison, not same-cost optimality.

### Joint-boundary continuation lemma

Two partial implementations with the same accessible ports, admissible extension grammar, residual cost interface and future noise contract are interchangeable for every common continuation if their COMPLETE conditional boundary laws P_A(S|x)=P_B(S|x) agree for every readable input x, and each next operation is a common kernel on S with fresh noise independent conditional on S.

**Proof:** equal measures have equal pushforwards under a common kernel; apply induction. Equal cost/interfaces preserve legal contexts. QED.

For approximate boundaries, TV contracts through each common extension; bounded conditional kernel discrepancies admit the usual coupling bound 1-product_t(1-delta_t). This is an established probability instrument with the physical interface made explicit.

Marginals alone are insufficient. A persistent environmental variable controlling later correlated faults must also be included (or replaced by a sufficient noise state). Full joint law is sufficient, not asserted minimal for every bounded task. Terminal output laws cannot be used as prefix signatures when internal ports remain readable.

## 3. Complete synthesis without ideal-prefix pruning

The old ideal truth-set quotient is not reused. We enumerate causal rooted DAGs with duplicate gates and shared fanout. NAND commutativity sorts input pairs. Only gates not ancestral to the terminal output are removable: they cannot affect it under independent faults, and cost extra installation.

For d gates, N[x,k] counts k-fault masks producing output1 on readable input x:

    P(output1|x)=sum_k N[x,k] gamma^k (1-gamma)^(d-k).

Complete equal-cost circuits with equal conditional output polynomials may be merged for the terminal task. Their future internal-port contexts are not being merged.

| Gates | Rooted netlists | Complete output-channel classes |
|---:|---:|---:|
|0|5|5|
|1|15|8|
|2|90|24|
|3|855|97|
|4|11,430|477|

Total: 12,395 netlists, 611 cost-indexed terminal channels. With 64 encoders there are 39,104 programs. For a fixed circuit, source-codeword choices separate only because the unchanged encoder library is equally priced and row-independent. An independent64-encoder oracle verifies this shortcut; a coupled encoder-cost model would require new synthesis.

## 4. Same function, code and gate count; different physical value

Both four-NAND networks compute g=k OR NOT(m0 AND m1).

Parallel:

    n0=NAND(1,k)
    n1=NAND(m0,m1)
    n2=NAND(1,n1)
    out=NAND(n0,n2)

Sequential:

    n0=NAND(1,k)
    n1=NAND(m0,n0)
    n2=NAND(1,n1)
    out=NAND(m1,n2)

At encoding (11,00,00), p=.01, gamma=.01, q=0:

|Design|Two-stage survival|
|---|---:|
|Fixed REFRESH bypass|.8091779607700227|
|Parallel four-gate realization|.8088208243744518|
|Sequential four-gate realization|.8091942664634513|

One realization helps while the other harms, at identical code/ideal logic/gate count. Their gap is .03734420889995 percentage point. Absolute gains are small in this frozen benchmark; the contribution is the exact structural separation, not an assumed economic benefit.

### Localization by complete physical fault traces

For fixed encoding/circuit and equal independent gate noise,

    dV/dgamma at0 = sum_i [V(only gate i flips)-V(no gates flip)].

Differentiate the finite fault-mask expansion: the no-fault term contributes -dV0, and each single-fault term contributes V_i.

|Gate|Parallel signed effect|Sequential signed effect|
|---:|---:|---:|
|0|-.000747925386|-.000747925386|
|1|-.020388112823|-.000971511032|
|2|-.020388112823|-.000971511032|
|3|-.023131429983|-.023131429983|
|Sum|-.064655581015|-.025822377433|

The topology changes which errors reach costly task contexts. This is a fixed-policy local sensitivity, not differentiation through an optimizing architecture.

## 5. Exact continuous optimality certificate

For p=.01, q=0 and capacity<=4, the sequential circuit with encoding (11,00,00) is globally optimal for EVERY gamma in [0,.01], allowing ties.

Every program is a rational polynomial of degree<=4 in gamma. The39,104 programs reduce to8,854 distinct value polynomials. Subtract each competitor, including the bypass, from the attaining polynomial. Its Bernstein coefficients on[0,.01] are all nonnegative. Thus all8,854 comparisons hold throughout the interval, without sampled interpolation or unresolved subdivisions.

For a common q<=1/2 the UPDATE programs undergo the same nonnegative affine transformation; their ordering stays fixed. The bypass is compared again and can become preferable. No global continuous2D phase diagram is claimed. Other rational points are solved by exact finite synthesis; browser controls use floating-point projections.

## 6. An upstream-independent last-port bound

For the unchanged v13 task constants a,b,D, let G(p)=max(0,a(1-p)^2-bp^2). In any single-output NAND DAG, the last independent flip followed by the q-latch produces e=gamma+q-2gamma q.

Relax all upstream computation to an arbitrary ideal table and the best equally priced encoding. Then

    V_any <= V_ref + max(0,(1-2e)G(p)-eD).

At q=0 no update can beat the bypass if

    gamma >= G(p)/(D+2G(p)).

At p=.01 the threshold is .01182419796035257..., about1.1824%. The statement allows arbitrary upstream depth, but requires the single independent final port. Zero-gate outputs are already bounded by the bypass in this task.

This is not an impossibility of reliable computation in general. Multiple retained outputs, a reliable voter, fail-silent execution, different fault dependence or another task change the contract. Any such final correction must be included, not granted for free.

## 7. Verification and remaining gate

15 scientific Python tests;3,120 independent scalar gate/mask/input executions; complete libraries through4 gates; exact encoder oracle;8,854 continuous comparisons; joint-extension tests; signed sensitivity checks;128 complete conditional traces of the witness. Fractions preserve exact arithmetic. Browser results are projections of the generated library.

R11 now has a correct local stochastic-boundary condition and a correlated-substrate falsifier. R14 has a shared-circuit noisy synthesis result with an attaining netlist and a task-specific last-port bound.

Still open: recurrent gate maintenance, faulty maintenance selection, nonuniform physical costs, multioutput signatures and a compact task-relative boundary smaller than the full joint law. The whole research program is not declared complete.

## 8. Principal predecessor and contribution

Krishnaswamy, Viamontes, Markov & Hayes, *Accurate Reliability Evaluation and Enhancement via Probabilistic Transfer Matrices*: https://ieee-ceda.org/media/accurate-reliability-evaluation-and-enhancement-probabilistic-transfer-matrices . This is the direct established framework for composing stochastic circuit behavior while preserving dependencies.

CDKA's executed contribution is the continuation-weighted adaptation: joint coding, bounded physical synthesis, exact interval certificate, same-cost topology separation, mechanistic traces and scoped last-port bound. These deserve evaluation as concrete contributions enabled by known tools; priority is assessed at the exact-result level.
