# T3.A — A realizability gap beyond the universal information lower bound

**Status:** exact finite counterexample and standard KL data-processing proof; **known in principle**, not a novel theorem.

## Problem

An arbitrary reweighting of trajectories may be mathematically allowed but not physically realizable by a controller. A lower bound in information units does not automatically imply that an actuator can achieve the corresponding event probability with that cost.

Let \(P^0\) be a reference law on trajectories, \(E\) a relevant outcome event, \(p_0=P^0(E)\), and \(\mathcal Q_{\mathrm{phys}}\) the laws physically realizable by the system's sensors, actuation channels, authority, timing and resources.

Define the minimum path-information intervention required to achieve success probability \(\beta>p_0\):
\[
C_{\mathrm{phys}}(\beta)=
\inf_{\substack{Q\in\mathcal Q_{\mathrm{phys}}\\Q(E)\ge\beta}}
D_{\mathrm{KL}}(Q\|P^0).
\]

## P5 — The universal event-divergence bound

Data processing under the indicator map \(\omega\mapsto1_E(\omega)\) yields
\[
C_{\mathrm{phys}}(\beta)\ge
d_{\mathrm{Bern}}(\beta\|p_0)
\]
when \(p_0<\beta\), assuming the event probability and law classes are well defined. The chain rule sharpens this:
\[
D(Q\|P^0)
=d_{\mathrm{Bern}}(q\|p_0)
+qD(Q(\cdot\mid E)\|P^0(\cdot\mid E))
+(1-q)D(Q(\cdot\mid E^c)\|P^0(\cdot\mid E^c)),
\]
with \(q=Q(E)\). The gap has an exact meaning: changing path statistics *within the success and failure groups*, even when only their aggregate event probabilities are of interest.

A universal path-law optimizer would tilt by only the event indicator. Real physics may not allow such a law.

## P6 — Explicit restricted-actuator gap

Let under \(P^0\), independent bits \(Y,Z\sim\operatorname{Bernoulli}(1/2)\), with \(E=\{Y=1,Z=1\}\), so \(p_0=1/4\). The actuator may choose \(q=P(Y=1)\) but cannot alter \(Z\); it stays independent and fair.

Then \(Q_q(E)=q/2\). To achieve \(\beta\in(1/4,1/2]\), \(q\ge2\beta\). The cost of changing the full law is
\[
D(Q_q\|P^0)=d_{\mathrm{Bern}}(q\|1/2).
\]
Since the Bernoulli divergence increases for \(q>1/2\), the exact physical optimum is
\[
C_{\mathrm{phys}}(\beta)=d_{\mathrm{Bern}}(2\beta\|1/2).
\]
The universal lower bound is strictly smaller for \(1/4<\beta\le1/2\):
\[
\Gamma(\beta)=d_{\mathrm{Bern}}(2\beta\|1/2)
-d_{\mathrm{Bern}}(\beta\|1/4)>0.
\]
At \(\beta=.4\): \(C_{\mathrm{phys}}\approx0.192745\) nats, event lower bound \(\approx0.054116\) nats, so the gap is \(\approx0.138629\) nats. For \(\beta>1/2\), the event is impossible regardless of the information budget; the physical cost is \(+\infty\).

**Interpretation:** even after paying the minimum *unconstrained information change* needed to make an outcome more likely, a controller restricted to a subset of causal channels may require strictly more change or may be unable to reach the event. This is a mathematically elementary example of a *causal authority gap*.

Do not interpret KL in nats as energy in joules without a specified stochastic physical model and valid change-of-measure identity.

## CDKA program implications

- The physically admissible law family \(\mathscr C_T\) is primitive; cannot be replaced by all measures on path space.
- **Potential influence** must be distinguished from available *causal authority*, contingent action selection, and self-maintained capacity.
- T3 should seek a coupled bound that varies with an endogenous sensor/actuator/repair organization rather than simply applying this known inequality to a fixed channel.
- T4 should track how \(\mathcal Q_{\mathrm{phys}}(Z_t,R_t)\) changes with state and history.

## Proof instruments and prior art

KL chain rule and data-processing; constrained linearly solvable control; path-space change of measure where applicable.

- [Bušić & Meyn (2018), Action-Constrained MDPs With KL Cost](https://proceedings.mlr.press/v75/busic18a.html).
- [Todorov (2006), Linearly-solvable MDPs](https://proceedings.neurips.cc/paper/2006/hash/d806ca13ca3449af72a1ea5aedbed26a-Abstract.html).
- [Girsanov-based information and control connections](https://pmc.ncbi.nlm.nih.gov/articles/PMC13596642/).

**Research status:** reproducible exact counterexample; novelty lies in the future endogenous-organizational extension, not in the information inequality.
