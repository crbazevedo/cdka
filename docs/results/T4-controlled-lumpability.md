# T4.A — When a decision-sufficient code remains sufficient tomorrow

**Status:** controlled Markov lumpability / stochastic bisimulation is known. Its CDKA application tests the limitations of one-shot action sufficiency; not a new theorem.

## Question

A memory code can retain just enough information to choose today's acceptable action. When can that same compressed state correctly support all tomorrow's decisions?

## Finite physical model

Let \(S\) be a finite set of complete physical states (environment, sensor/actuator organization, resources and memory), \(P(s'|s,a)\) a controlled Markov kernel, \(A(s)\) the physically available actions, and \(V\subseteq S\) a specified viable set. The observer is assumed to know the compressed label \(m(s)\); physical realizability remains a separate question.

Finite-horizon optimal survival values:
\[
V_0(s)=\mathbf1_V(s),\qquad
V_{h+1}(s)=\mathbf1_V(s)\max_{a\in A(s)}
\sum_{s'}P(s'|s,a)V_h(s').
\]

## Proposition — sufficient condition for exact recursion

Assume a map \(m:S\to M\) such that whenever \(m(s)=m(t)\):

1. \(s\in V \iff t\in V\);
2. \(A(s)=A(t)\);
3. for every admissible action \(a\) and every code cell \(C=m^{-1}(k)\),
\[
\sum_{s'\in C}P(s'|s,a)=\sum_{s'\in C}P(s'|t,a).
\]

Then for all horizons \(h\), \(V_h(s)=v_h(m(s))\) for some \(v_h\), and there exists a finite-horizon optimal policy depending only on \(m\).

**Proof:** At \(h=0\), viability is constant on cells. Assume \(V_h\) is cell-constant. Each controlled continuation value is a sum over next-state cells with equal weights by condition 3. The available actions are identical by condition 2; maximization preserves equality and yields a code-dependent optimal action. Induction completes the proof.

This is standard strong controlled lumpability. **Failure of the conditions does not imply the code is necessarily inadequate for a particular viability task.** Exact predictive aggregation is stronger than task-relative decision sufficiency.

## Counterexample — one step needs zero bits; two steps need one bit

An initially observed binary context \(w\in\{-1,+1\}\) remains unchanged for two decisions. At step 0, the only acceptable choice is the same hold action regardless of w. At step 1, no observation is possible, and the only acceptable action is left for w=−1 or right for w=+1.

- Remembering only the safe action *now* requires one codeword (zero fixed-width bits).
- Guaranteeing both stages requires retaining w across time: two distinguishable codewords (one fixed-width bit).
- One-step action sufficiency is not recursively closed.

This is an elementary illustration rather than new dual-control theory.

## Operational instruments

1. Partition states by viability and action-availability labels.
2. Refine cells when action-conditioned probabilities of transitioning to current cells differ.
3. Iterate to a fixed point: a controlled probabilistic-bisimulation quotient.
4. Compare its code size with the one-step safe-action cover, without confusing predictive equivalence with minimal information for a single objective.
5. Under partial observation, verify that the code can actually be computed and retained by physically available sensors and memory.

## CDKA next step

Allow sensing, actuation and repair to evolve inside the same physical kernel \(P\). Derive a resource-relative information-state condition; compare it with fixed-actuator viability and partially observed control theory before making novelty claims.
