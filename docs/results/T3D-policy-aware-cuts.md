# T3.D — Policy-aware information cuts: convex rows and survivor mass

**Status:** elementary propositions derived and checked with classical Dobrushin contraction, decision theory and finite-state control. **No originality claim.** This note repairs two potential errors in interpreting T3.C: treating fixed repair modes as the entire closed-loop channel, and conditioning away trajectories on which the organization has already failed.

## 1. Question, causal scope and minimal definitions

A physical organization exposes a state `C` to its action-selection mechanism. `C` includes every readable memory, actuator mode, resource trace and clock admitted by the model. The hidden context is `W`. For this section only, repair follows

\[
W\longrightarrow C\longrightarrow (A,C'),\qquad
K^\pi(c'|c)=\sum_{a\in A(c)}\pi(a|c)K(c'|c,a).
\]

Thus no new direct observation of W enters during this repair. If the transition depends on W beyond C, it can introduce new information; the contraction assertion below is then not applicable as stated.

An action is selected from `A(c)` based on **actual available C**, not an unrecorded history. The mode `a` is not necessarily observed later: it matters only through its physically persistent consequences in C'.

## 2. Proposition D1 — sharp feedback envelope under row-wise constraints

For a stochastic matrix K, let

\[
\delta(K)=\max_{c\ne d}\operatorname{TV}(K(\cdot|c),K(\cdot|d)).
\]

If every row can independently choose any admissible action, then

\[
\boxed{
\sup_\pi\delta(K^\pi)
=\max_{c\ne d}\max_{a\in A(c),\,b\in A(d)}
\operatorname{TV}\big(K(\cdot|c,a),K(\cdot|d,b)\big).
}
\]

**Proof.** Each closed-loop row belongs to the convex hull of its admissible rows. For distributions over a and b,

\[
\operatorname{TV}\left(\sum_a p_a K_c^a,\sum_b q_bK_d^b\right)
\le\sum_{a,b}p_aq_b\operatorname{TV}(K_c^a,K_d^b)
\le \max_{a,b}\operatorname{TV}(K_c^a,K_d^b).
\]

Choose a maximizing pair of **distinct** input states and deterministic actions for these two rows. Complete the prescription arbitrarily on the other rows. This attains the upper bound. With one input state, the coefficient is zero. QED.

**Qualification.** An expected-budget constraint linking choices across input rows or a restriction on the physical circuit implementing the prescription can exclude this maximizing pair. The expression remains an upper bound but need not be tight for that more restrictive class. Likewise it is a worst-input-pair envelope, not automatically the optimum for a particular initial channel or future viability requirement.

### Example: reset hardware is a writing channel

For `K^a(c'|c)=1{c'=a}`, each fixed a erases C and has coefficient zero. But `a=c` produces the identity channel, whose coefficient is one. The operation is not creating information about W from nothing: for the complete closed-loop experiment,

\[
\operatorname{TV}(P_{C'|W=0},P_{C'|W=1})
\le\delta(K^\pi)\operatorname{TV}(P_{C|W=0},P_{C|W=1}).
\]

Identical input laws remain identical under a common policy. Acting can **transport or recode** an existing distinction. Genuinely acquiring a new distinction requires a physical coupling that carries new information about the world.

### Instrumental payoff

The one-step optimization is a finite row-diameter problem, not a search over all randomized policies. For binary outputs each row is an interval of Bernoulli parameters; the optimization is geometrically the largest distance from the diagonal in a rectangle of attainable row pairs. This makes an exact upper-bound oracle and a clear visualization possible.

## 3. Proposition D2 — usable discrimination must retain the failed mass

Let

\[
\mu(w,c)=P(W=w,C=c,\text{organization alive}),\quad w\in\{0,1\}.
\]

This is a **subprobability** distribution. Set

\[
M=\sum_{w,c}\mu(w,c),\qquad
D_{\rm live}=\sum_c|\mu(0,c)-\mu(1,c)|.
\]

If both final actions are available at every live c and the safe choice is U=W, the optimal total success probability is

\[
\boxed{
V(\mu)=\sum_c\max\{\mu(0,c),\mu(1,c)\}
=\frac{M+D_{\rm live}}{2}\le M.
}
\]

**Proof.** For each c, select the more massive of its two context alternatives. Apply `max(x,y)=(x+y+|x-y|)/2` and sum. No equal-prior assumption is needed. QED.

This is a classical decision identity applied to killed physical processes, not a new information measure.

### Counterexample: perfect surviving knowledge, vanishing viability

Consider `mu(0,0)=mu(1,1)=s/2`, with all other live mass zero. On every surviving trajectory, the register correctly identifies W. Under the normalized surviving population, information is exactly one bit and classification accuracy is 100%. Nevertheless `M=D_live=s`, so the actual viability is s. Taking s→0 does not improve the organization.

A recursion that renormalizes after failure turns `s` into 1 and creates a fictitious result. Our solver carries all alive mass **without normalization**; loss of mass is absorbing failure.

`(M,D_live)` is sufficient for this terminal binary decision, not for arbitrary future physical control. Different organizations with the same pair can have different actuator availability or future channel dynamics.

## 4. Verification and limits

- All **729** three-input/two-action/binary-output channel families on the probability grid `{0,1/2,1}` were checked against enumeration of all deterministic feedback prescriptions.
- Fixed resets give coefficients `0,0`; feedback achieves 1. A single input cannot become distinguishable by changing an action.
- The subprobability identity was checked against every terminal binary decoder on a rational probability grid.
- Proofs establish the propositions under their hypotheses; tests check implementations, not novelty.

Code: `cdka/policy_cuts.py` (`feedback_envelope`, `live_binary_value`).
Tests: `tests/test_policy_cuts.py`.
Interactive companion: [Policy cuts laboratory](../lab/policy_cuts.html).

## 5. Program role and next proof obligation

T3.C established a failed information path. T3.D characterizes the envelope once actions can create alternative physical paths, without confusing survivors with the full experiment. T4.C now asks whether the organization can **repeat** a viable action–repair loop and with which reliability guarantees.

The future contribution must be in policy-constrained, resource-coupled, recurrent information transport—not in claiming the classical TV formula as a new theory.

## Primary sources and exact relationship

- Gaubert & Qu (2015), [Dobrushin's ergodicity coefficient](https://doi.org/10.1007/s00020-014-2193-2): contraction geometry and row-distance antecedents. D1 is an elementary control-envelope consequence, not a claim that this paper states D1 verbatim.
- Grover, [research on implicit communication and Witsenhausen](https://users.ece.cmu.edu/~pgrover/pubs.html): control actions as information channels. The reset example is an elementary illustration.
- Junges et al. (2018), [Finite-State Controllers of POMDPs using Parameter Synthesis](https://proceedings.mlr.press/r16/junges18a.html): explicit bounded controllers and model-based correctness. Our exact enumerator is a tiny reference instance, not a new synthesis algorithm.
