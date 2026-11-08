# T4.V — Certified regeneration instead of global commutation

**7 November 2026, São Paulo.** Executed contribution: a noncommuting common-environment specialization, exact run-histogram response and Markov weights, conservative source recognition, independent oracles, and same-host official comparisons. Renewal/partition tools are classical; the contribution is their checked integration into a concrete verification class. General priority/SOTA is not claimed.

## Contract

N heterogeneous finite components, common exogenous homogeneous binary Markov environment. Mode0 is work, mode1 restart. Local draws and initial laws are independent conditioned on the complete context history. All components advance synchronously; current context is used before the context transition. A local goal G_i is absorbing under both operators. The initial law alpha_i is outside the goal. Every non-goal restart row equals alpha_i, whereas completed components remain completed. Resets consume one step. The query is all local goals reached by H, equivalent to their conjunction at H by absorption.

The restricted PRISM parser consumes all source, checks ownership, exogeneity, guards, synchronization, probabilities, initial laws and goal. It is not a general PRISM/JANI frontend. The Python API requires the stated independence contract; flags do not prove arbitrary external source code.

## Theorem 1: regenerate the response, not the whole history

Let T_i be the transient work matrix and S_i=1 alpha_i the transient restart. Set f_i(l)=alpha_i T_i^l 1. For a mode word whose positive work runs have lengths l_1,...,l_r,

    P(i still incomplete | word) = product_j f_i(l_j),
    P(all complete | word) = product_i [1-product_j f_i(l_j)].

Proof: on the noncompleted mass, restart reestablishes alpha_i, retaining the previous noncompletion probability as a scalar. Each work run multiplies it by f_i(l). Leading/consecutive resets contribute1. Conditional local independence then gives the second identity. Completed mass is not reset. QED.

The scalar factors commute even though full work/reset operators fail goal-relative commutation. Thus the multiset of positive work-run lengths, not just exposure counts or last-reset age, preserves the response.

## Theorem 2: exact weights, not equiprobable histories

For a sorted nonempty histogram lambda, let n=sum(lambda), r=len(lambda), m=H-n and M(lambda)=r!/product_l c_l!, where c_l counts parts equal to l. Positive reset-run compositions have count B(m,k)=choose(m-1,k-1) for m>=k>=1, B(0,0)=1 and zero otherwise.

With initial context law nu and transition matrix A, sum over four endpoint cases:

| start/end | reset runs k | work→reset | reset→work |
|---|---:|---:|---:|
|0/0|r-1|r-1|r-1|
|0/1|r|r|r-1|
|1/0|r|r-1|r|
|1/1|r+1|r|r|

Each term is

    nu_start B(m,k) A00^(n-r) A11^(m-k) A01^(work→reset) A10^(reset→work).

Multiply their sum by M(lambda). This is w_H(lambda), the probability of every history with this histogram. Histories within a class need not have the same individual probability. Terms whose composition count is zero are omitted before evaluating exponents. The all-reset history has weight nu_1 A11^(H-1) and zero completion response.

Then

    p_H = sum_lambda w_H(lambda) product_i[1-product_(l in lambda) f_i(l)].

Complete exact history grouping independently checks every weight, not merely p_H.

## Theorem 3: structural size and complexity

Histograms are feasible iff sum(lambda)+len(lambda)-1<=H. Replacing every part l by l+1 gives partitions with parts>=2 and total<=H+1. Their counts telescope as sum_t[p(t)-p(t-1)]=p(H+1), including the empty histogram. Therefore the nonempty count is p(H+1)-1.

A streaming sorted-part DFS evaluates each histogram once, carrying an N-vector of log noncompletion probabilities and an exact permutation multiplicity. Arithmetic time is

    O(H sum_i d_i^2 + H^2 + N p(H+1)),

and storage O(NH+H^2+sum_i d_i^2), including the recursion stack. The partition function is exp(Theta(sqrt(H))), so the horizon dependence is subexponential, NOT polynomial. At fixed local size/H, dependence on component count is linear rather than the global product. Exact rational bit growth, input reading and output precision remain costs. Production float64/log evaluation is not a rigorous numerical interval certificate. Oversized partition sets are explicitly refused.

## Falsifiers and tracing

1. WW R and W R W have equal exposure counts but unequal two-stage completion probability. V20's commutation-on-goal test rejects this family correctly.
2. WW RR W and W RRR W have identical last-reset age but different outcomes in a deterministic two-stage process; completed work persists.
3. WW R W R and W RR WW have the same histogram{1,2} and response, but different Markov weights.
4. A partial reset with transient rows(1,0) and(1/2,1/2) does not regenerate the same law. Under work[[1/2,1/2,0],[1/2,0,1/2],[0,0,1]], run orders(1,1,2) and(1,2,1) give25/64 and3/8, a1/64 difference. The compiler refuses it.
5. Shared environmental history creates real dependence; multiplying local marginals gives a different answer.

## Informed competing representation

An independent subset-renewal evaluator uses inclusion–exclusion over N components. For each subset S, q_S(l)=product_(i in S) f_i(l). A renewal convolution computes the probability that all members of S remain incomplete; inclusion–exclusion recovers all complete. Arithmetic cost O(2^N H^2), low storage, possible floating cancellation. Its Fraction implementation is an oracle. The float version reports conditioning, not clipped answers.

This method wins at smallN/largeH. Histogram evaluation wins asN grows with moderateH. An eventual portfolio should select the representation from structural parameters, not hide unfavorable regions.

## Official comparison completed in this increment

Code commit b8d245541f9d031b0934e29218ab4963097b2337; immutable evidence f4a79052d0cf92c3a36693533c67bb2053506284; run42437618512. Stormpy2.0.0/numpy2.3.4/Python3.12.16, AMD EPYC7763, thread env1. Same PRISM/property for all methods. Five cases × five methods × three fresh subprocesses=75 valid timings; no error or mismatch. Read/parse/build-or-certify/solve included; process startup/RSS separately retained.

|N,H|histogram ms|Storm sparse ms|Storm+strong bisim ms|Storm symbolic ms|informed renewal ms|
|---|---:|---:|---:|---:|---:|
|2,10|2.784|20.256|20.187|47.964|2.131|
|4,10|3.771|22.320|22.115|378.953|3.558|
|6,10|4.620|40.528|41.337|1135.148|5.854|
|8,10|5.632|451.194|468.054|6493.131|13.006|
|4,20|11.923|21.727|21.708|496.436|4.222|

For N8/H10, ratio80.11 against the fastest measured Storm internal total;4.87 including complete process. RSS42.62MiB vs155.48MiB sparse and137.83MiB bisimulation. Strong bisimulation actually reduced13,122 states to6,816 in a checked sample; build/minimization time is not excluded.

This is a narrow synthetic common-reset extension of published Meeting parameter pairs, not unmodified benchmark data and not general SOTA. Tessa GPU/Dice and all Storm tunings were not run. Specialist baseline losses are shown. Local benchmarks on another CPU remain separate; no cross-host ratios.

## Evidence correction

Attempt01 at906c627 had incompatible API calls and a missing pipefail that turned a failed Python pipeline green. It is explicitly invalidated and preserved. The corrected harness uses public2.0 APIs, a small API/value smoke gate, pipefail and explicit result checks. A green workflow alone is not evidence.

## Validation and contribution

22 unit tests under normal and optimized Python:24 three-way exact algorithm cases,12 microstate cases,30 tensor comparisons,72 random rational cases,24 complete histogram-weight sweeps, degenerate contexts, multiple goals and parser/refusal tests. Additional complete H6 trace set:32 reachable histories,14 positive histogram classes. Local copies of25 official median values were reproduced; source-summary Git hash is2fe21002f45e2dec030be571ed39e1aa34afa943.

The useful new package is a certified noncommuting specialization and an empirical N/H representation tradeoff. Existing renewal theory, Markov run combinatorics and integer partitions are instruments; exact scientific priority for their coupling here remains an explicit audit task.

Primary antecedents: NIST DLMF26.2/27.14; Chechkin–Sokolov2018 (10.1103/PhysRevLett.121.050601); Decoupling Combinatorial Complexity: a Two-Step Approach to Distributions of Runs (10.1007/s11009-018-9689-1); Melloni–Stam–Ytrehus, Dynamic Security Aspects of Onion Routing (eprint2023/1439), flagged from primary search text as an ordered-composition/renewal antecedent requiring full review. No assertion of exhaustive novelty is made.
