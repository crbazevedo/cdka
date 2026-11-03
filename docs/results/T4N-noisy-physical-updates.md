# T4.N / T3.J — Realizing a continuation bit in a costed noisy update mechanism

**2026-11-03 · Contribution:** a small jointly synthesized physical interface and exact hardware/noise frontier, using the unchanged CDKA v6 plant. The update is an actual NAND network, not a designer-supplied posterior or an unrestricted lookup table. It provides a constructive bridge from v12 semantic reductions to executable finite memory. Circuit costs are library-relative; broader priority remains a precise-result audit, not a prerequisite to recognizing the adaptation.

## 1. The frozen causal and resource contract

We keep the same plant in `cdka/composition.py` and the v9 three-outcome diagnostic: signals have equal probability and conditional healthy probabilities 0.01, 0.5 and 0.99. The world and corrector health remain hidden.

**Important scope restriction:** the first physical action is SERVICE for every signal. This is the service-first continuation slice that exposed the v9/v11 update collision, not a claim to optimize all possible first actions. Initial resource b=4 pays SERVICE=2 and, only after success, receives the usual one-token harvest. At the second decision b=3, so both HOLD and REFRESH are affordable even when commanded by error. The terminal failure event and deadline are unchanged.

Hardware:
1. An equally priced fixed sensor encoder E maps each diagnostic to a two-bit physical register. The 64 encodings are considered jointly with the update circuit. Sensor acquisition and these initial latches are common to all designs.
2. Before update, each stored bit flips independently with probability p. The circuit reads only received bits (m0,m1) and the new physical syndrome k.
3. A fixed shared combinational circuit computes g(m0,m1,k). It may contain at most K two-input NAND gates, constants and wires; fanout is unrestricted. K is installed gate capacity, not a fungible energy token.
4. The circuit overwrites one physical output latch. That write/read channel flips its bit with probability q, independent of plant, input errors and circuit choice. The old diagnostic bits and syndrome are unavailable at final execution.
5. A fixed output interface maps 0→HOLD and 1→REFRESH. There is no separately readable plan pointer or full diagnostic.
6. An alternative fixed-command bypass can perform the best constant terminal action without activating the new write mechanism. It is the same baseline for every K.

NAND operations are ideal in the synthesis contract. q is a calibrated final update-channel error, NOT a derivation of reliability from individual faulty gates. The gate-fault falsifier below makes this distinction necessary. The design does not yet include recurrent logic maintenance or endogenous installation cost.

## 2. Exact weighted interface

Let T[y,k,u] be the joint live mass after SERVICE multiplied by success of terminal action u. Hidden health is summed only by the evaluator. For a fixed encoder and old-register error p, define

    A_x(u)=sum_y P(receive m | E(y),p) T[y,k,u],    x=(m,k),
    Delta_x=A_x(1)-A_x(0),
    B=sum_x A_x(0),     D=sum_x Delta_x.

For circuit truth table g and uniform final update error q,

    V(E,g;p,q)=B+qD+(1-2q) sum_(x:g(x)=1) Delta_x.

**Proof:** requested output 0 produces (1−q)A_x(0)+qA_x(1); requested output 1 produces the reverse. Subtracting the baseline and summing gives the affine identity. Failed first-stage mass is retained as failure. QED.

An unrestricted table chooses g(x)=1 exactly when Delta_x>0. A physical circuit library may not contain that whole table at its budget. For a fixed encoding, the exact loss against the unrestricted table is

    (1−2q) sum_(x:wrong-sign choice) |Delta_x|.

This is a continuation-weighted circuit-approximation objective. It exposes which readable input rows justify extra gates. It is not unweighted Boolean accuracy and not a claim that an internal bit represents all counterfactual futures.

## 3. A continuation quotient of the circuit-construction search

A partial NAND DAG provides a set S of already computed three-variable truth functions and has used d gates. Under ideal deterministic gates, uniform gate prices and free fanout, two partial circuits with identical S and d admit exactly the same future functions at the same further cost.

Therefore we generate signal sets, not every syntactically distinct netlist. Each newly retained set carries an actual topologically ordered gate witness. A gate duplicating an existing truth function is unnecessary for any minimum-cost ideal implementation and can be removed by rewiring its consumers.

The exact breadth-first synthesis gives:

| Maximum gates | Different available-signal sets at this depth | Functions realizable up to this depth |
|---:|---:|---:|
| 0 | 1 | 5 |
| 1 | 6 | 11 |
| 2 | 33 | 23 |
| 3 | 182 | 48 |
| 4 | 1,098 | 91 |

The constants and three input wires are the five zero-gate functions. An independent netlist enumerator retaining even redundant gates agrees through depth three. Every retained circuit is executed on all eight physical input combinations.

This is a concrete application of the generalized methodology: a compositional equivalence closes under extension and safely removes repeated partial constructions. It does not assert that exact circuit synthesis is generally easy.

## 4. Exact frontier for this continuation task

The only negative REFRESH advantage occurs for the low diagnosis with unanimous syndrome k=0. Define its magnitude a, the sum of the other two positive k=0 margins b, and total REFRESH advantage D:

    a = 0.00028111705753212826...,
    b = 0.020122208666474652...,
    D = 0.0225844087681837...,
    V_ref = 0.8091779607700227... .

All k=1 margins are positive. The physical-code and circuit search has the exact q=0 gain frontier

    G_K(p)=0,                          K=0,1;
           max(0,a(1−p)−bp),           K=2,3;
           max(0,a(1−p)^2−bp^2),       K=4.

Including final-write noise and the bypass gives

    V_K*(p,q)=V_ref + max(0,(1−2q) G_K(p) − qD),

for 0≤p,q≤1/2 and K∈{0,1,2,3,4}. Applying the positive part before or after the G formula gives the same final maximum.

### Attaining physical programs

With K=2, encode the low diagnosis as 01 and the others as 00. The updater computes

    g = k OR NOT m0.

Its implementation is `n0=NAND(k,k); g=NAND(n0,m0)`. The output is HOLD only when the retained bit indicates the low diagnosis and the register is unanimous.

With K=4, encode low as 11 and the others as 00. The updater computes

    g = k OR NOT(m0 AND m1).

One minimum-cost DAG is

    n0 = NAND(k,k)
    n1 = NAND(n0,m0)
    n2 = NAND(n1,n1)
    g  = NAND(n2,m1).

Only when both transported bits remain 1 and k=0 is HOLD selected. The code protects the high-cost positive contexts from a mistaken HOLD while allowing some less costly errors in the low context. This is unequal operational protection, not perfect correction of every bit error.

### Continuous, not grid-only, optimality

All 64 encoders and 91 truth functions up to four gates give 5,824 realizable program/function pairs. Their values before final write are rational quadratics in p. Exact algebraic interval checks establish 2,814 dominance inequalities over all p∈[0,1/2], separately for every gate budget. No three-gate circuit exceeds the two-gate frontier.

The q-dependence is a common nonnegative affine transformation of all program values, so the certification extends to every uniform q≤1/2; at q=1/2 all update choices tie. The bypass is compared afterward under its declared physical contract.

For q=0, useful-input thresholds are

    p_2 = a/(a+b) = 0.01377800175004621...,
    p_4 = sqrt(a)/(sqrt(a)+sqrt(b)) = 0.10570305126989384... .

Between these thresholds, no implementation with three or fewer gates improves the baseline, while a four-gate circuit does. This is a strict minimum-upgrade certificate within the stated hardware library.

## 5. Why four gates also attain the unrestricted table optimum here

For a fixed encoding, an unrestricted table never chooses HOLD on k=1 because every corresponding margin is positive. On k=0 it separates one negative-margin diagnostic (weight a) from a mixture of two positive-margin diagnostics (total weight b>a).

The attainable improvement is convex in that positive-class channel mixture. It is bounded by the larger of the improvements obtained by assigning both positive diagnoses to either constituent word. Thus an optimum can merge the positive pair.

The Hamming distance between this word and the negative word is 0,1 or 2. Their best improvements are respectively

    0,
    [a(1−p)−bp]_+,
    [a(1−p)^2−bp^2]_+.

When both are positive, the last exceeds the second by (b−a)p(1−p). Opposite two-bit words attain the unrestricted optimum; the four-gate circuit realizes its sign rule. This proof relies on the observed margin signs and the symmetric independent-bit channel. Other tasks and channels require new analysis.

## 6. Measured values and mechanistic traces

| Old bit error p | New bit error q | Best ≤1 gate | Best ≤2 or ≤3 gates | Best ≤4 gates |
|---:|---:|---:|---:|---:|
| 0 | 0 | 80.917796% | 80.945908% | 80.945908% |
| 1% | 0 | 80.917796% | 80.925504% | 80.945147% |
| 1% | 1% | 80.917796% | 80.917796% | 80.922016% |
| 10% | 0 | 80.917796% | 80.917796% | 80.920444% |

The gains are small in this frozen SERVICE-first plant; the point is a strict representation/update/circuit separation, not a large engineering improvement or a reason to price arbitrarily expensive hardware.

At p=1%, the two-gate circuit benefits from a single retained diagnostic bit; the four-gate circuit uses redundancy in the incoming word, then compresses the result into one freshly written action bit. A new signal k can overturn the initially intended suffix without needing a hidden-history lookup.

The incoming memory has two cells, the final action register one cell, and the gate budget 2 or 4. These are different resources. The rank-20 evaluator space from v12 is neither handed to the runtime policy nor claimed to be physically encoded in one bit. This bit is sufficient only for the declared terminal binary task.

## 7. Falsifier: noiseless function equivalence fails under a gate-fault contract

A wire carrying m and a circuit with two successive NAND inverters compute the same ideal function. If each inverter independently flips its output with probability γ, the two-gate circuit has error

    2γ(1−γ),

while the ideal wire's error is zero in that fault contract. For γ=0.1, they differ by 18 percentage points of logical error.

Therefore, merging partial circuits by ideal truth functions is certified only for ideal-gate extensions and the separate uniform final write channel. Gate-dependent faults, timing, fanout loading or correlated substrates require richer signatures and can change the optimal netlist. The negative test is retained as a specific trigger, not a general rejection of semantic synthesis.

## 8. What this closes and what remains

**Closed within the finite family:** a physically readable, recursively placed update after a real plant step; joint initial coding and shared-circuit synthesis; a minimal upgrade; exact global noise/gate frontier; and independent gate-level and raw-state execution.

**Not closed:** ideal NAND gates, the fixed first action, an equally priced initial encoder, base wires and actuator interface, uniform final-write noise, two-stage horizon and no recurrent gate maintenance. A general invariant evaluator basis is not yet a general physical realization.

The next paper-grade target is a costed realization theorem for a family of continuation signatures under an explicit noisy update grammar. Before adding mechanisms, consolidate v9–v13 as one claim map with hypotheses, witnesses, counterexamples and the closest predecessor.

## 9. Instruments and evidence

14 Python tests, 24 raw microstate comparisons, 728 truth-table/gate input checks, 1,092 direct-versus-polynomial evaluations, independent unquotiented circuit enumeration through three gates, 2,814 continuous dominance checks, and a gate-fault counterexample. Browser values are projections of an exact rational certificate.

Primary related instruments: [De Micheli et al., state assignment](https://research.ibm.com/publications/optimal-state-assignment-for-finite-state-machines); [Poupart & Boutilier, value-directed POMDP compression](https://www.cs.toronto.edu/~cebly/Papers/vdib-abs.html); [Tzeng, probabilistic automata equivalence](https://doi.org/10.1137/0221017). They enable the work; the contribution is the physically constrained adaptation and independently certified update frontier, whose broader priority is assessed separately.
