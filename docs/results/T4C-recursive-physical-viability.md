# T4.C — Recurrent physical control without free memory or survivor bias

**Status:** model-specific proofs, exact rational verification, and classical occupancy/finite-state-control instruments. Originality has not been established. This is progress beyond a precommitted repair timetable, not a general theory of autonomy.

## 1. General finite architecture and the controller's information

Underlying live states are `s=(W,C)`. The readable physical state C includes the declared memory, health, resource ledger and protocol phase. Admissible action laws have the form

\[
A_t\sim\pi_t(\cdot|C_t),
\]

not `pi_t(.|W_t,C_t)` and not a free function of forgotten observations. For finite-horizon nonstationary policies a physical/declared stage clock is allowed. A persistent random seed, if retained, is an additional physical state; fresh independent random coins are a different architecture.

`Q(s'|s,a)` is a sub-stochastic kernel over live states. Missing probability mass corresponds to irreversible failure. State-dependent sensors, memory damage, actuator repair, resource consumption and resource replenishment can all be represented in Q.

## 2. Proposition C1 — exact design recursion over unnormalized occupancy

Let `mu_t(s)=P(S_t=s, alive)` and let a **prescription** `phi:C→A(C)` choose one action for each readable state, shared by every hidden state having that same C. Define

\[
(\mu Q_\phi)(s')=\sum_s\mu(s)Q(s'|s,\phi(C(s))).
\]

For a horizon of h physical transitions and success defined as continued survival,

\[
\boxed{
V_0(\mu)=\sum_s\mu(s),\qquad
V_{h+1}(\mu)=\max_{\phi}V_h(\mu Q_\phi).
}
\]

**Why this is not an omniscient controller.** The distribution mu is computed by the *designer*, who selects a complete prescription. During execution the system receives only C and applies that prescription; mu and W are not runtime inputs. A sequence of prescriptions can be compiled before execution. If a model instead grants arbitrary history or a posterior update not implementable by its physical memory, it solves a relaxed problem.

**Proof.** Condition a valid finite-horizon design on its first prescription. Its next live occupancy is exactly `mu Q_phi`; the best remaining sequence has value `V_h`. Maximizing over feasible first prescriptions gives necessity and sufficiency by induction. At each finite horizon, expected survival is multi-affine in the time-indexed behavioral decision probabilities. With pathwise resource constraints already encoded in Q/actions, a maximum is attained at a deterministic prescription sequence. This last statement is **not** asserted for stationary-policy optimization, constrained averages, or worst-context objectives. QED.

For each fixed prescription sequence the value is linear in mu. Therefore `V_h` is the upper envelope of finitely many linear forms: positively homogeneous, piecewise linear and convex on the live-occupancy simplex. These are classical planning properties, not a new result.

### Proof instruments

- Matrix products and positive-kernel algebra provide exact propagation.
- Shared prescription variables enforce the information constraint.
- Missing mass handles safety without conditioning it away.
- Piecewise linearity permits alpha-vector and domination certificates.
- Independent fully observed DP remains a useful upper-bound/falsification oracle, not the solution.

## 3. A minimal recurrent repair-and-act organization

A hidden **static** context `W∈{0,1}` is initially equiprobable. An initial perfect sensor has stored W; there is no later direct sensing. The physical readable state is

\[
C=(\mathrm{phase},m,h,r).
\]

There are four reachable readable states and eight underlying live states:

- **Repair:** `(0,m,0,1)`. The actuator is worn; one resource token is present. Select a physical writing repair mode `a∈{0,1}` using m. The repair consumes the token, restores the actuator, and writes `m'=a XOR E`, where `E~Bernoulli(p)`, `0≤p≤1/2`.
- **Act:** `(1,m',1,0)`. Choose command `u∈{0,1}` using m'. If `u=W`, the command's physical latch becomes `m=u`; the successful environmental interaction replenishes one token while actuation wears the device. The state returns to `(0,u,0,1)`. Otherwise failure is absorbing.

The repair mode is chosen contingently by the organization, not precommitted independently of its memory. The completed act–repair loop sustains the next opportunity to act. Replenishment comes from the environment through a **specified physical transition**, not energy creation. The viability criterion and the energy coupling are designed model assumptions; their evolutionary origin is not explained.

Crucially, on every successful cycle the next physical state is `(W,m=W,repair,token=1)`. Any surviving implicit information in a previous command is explicitly present in the latch. There is no extra history or hidden random seed.

## 4. Proposition C2 — exact deterministic reliability-profile frontier

For n cycles, write the per-context survival profile as

\[
(s_0,s_1)=\big(P(\text{survive n cycles}|W=0),P(\text{survive n cycles}|W=1)\big).
\]

With `0<p≤1/2`, the **non-dominated deterministic** profiles are exactly

\[
\boxed{(1,0),\quad(0,1),\quad((1-p)^n,(1-p)^n).}
\]

For `p=0`, the last profile is `(1,1)` and dominates the other two.

**Proof.** In a cycle the action decoder `g:{0,1}→{0,1}` is either constant or a permutation. If g is constant in any cycle, one context has zero survival thereafter, so the full profile is dominated by `(1,0)` or `(0,1)`. If all decoders are permutations, each context's correct transmission probability in each cycle is at most `1-p`; hence each component is at most `(1-p)^n`. Selecting repair and decoding as matching identity/permutation laws attains this bound for both contexts. Constant action policies attain the two axis profiles. QED.

The deterministic feasible set is not assumed convex. A convex combination of whole policies generally requires a **persistent policy-selection variable**, not just fresh local randomization.

## 5. Proposition C3 — average versus all-context viability

### Mean objective with a fair initial context

For finite-horizon deterministic or fresh-behavioral randomized laws,

\[
\boxed{V_n^{\rm mean}=\max\{1/2,(1-p)^n\}.}
\]

The deterministic frontier proves the assertion; the finite-horizon mean objective cannot be improved by fresh behavioral randomization (C1).

### Robust objective over both contexts, without a persistent external seed

\[
\boxed{V_n^{\rm robust}=\sup_\pi\min_w P^\pi(\text{alive through n}|W=w)=(1-p)^n.}
\]

**Proof, including fresh randomized laws.** In one cycle let `f_w=P(write1|m=w)` and `g_y=P(act1|m'=y)`. The probability of reading 1 is `y_w=p+(1-2p)f_w`. The per-context success probabilities satisfy

\[
q_0+q_1=1+(g_1-g_0)(y_1-y_0)\le2(1-p).
\]

Thus `q_0 q_1 ≤ (1-p)^2` by AM–GM. Because successful actuation returns each context to its specified physical state, and no persistent random state is available, the full conditional survivals factor as `s_w=product_t q_{w,t}`. Therefore

\[
\min(s_0,s_1)\le\sqrt{s_0s_1}\le(1-p)^n.
\]

The symmetric repair/act policy attains equality. QED.

### Numerical example

For `p=0.1`, preservation gives `0.9^n`. At n=6 both contexts can achieve `0.531441`; at n=7 the robust value falls to `0.4782969`. The mean optimizer can instead attain 0.5 forever by always selecting the action safe for only one context. At n=10:

| Criterion / architecture | Best value |
|---|---:|
| Robust, no additional persistent seed | 0.3486784401 |
| Mean over the two initial contexts | 0.5 |
| Mean restricted to the symmetric information-preserving policy | 0.3486784401 |
| Robust with one extra persistent independent read-only policy seed | 0.5 |
| Fully observed hidden-world relaxation | 1 |

The apparent preference to stop preserving the environmental distinction is induced by the **objective and physical architecture**, not evidence of emerging intention.

## 6. A durable random seed is an extra physical resource

An independent fair read-only seed `Z` that persists despite repair can choose once between the always-0 and always-1 policies. This gives survival 1/2 in each context for any horizon. Combining with the preserving policy, the robust optimum becomes

\[
\boxed{V_n^{\rm seed}=\max\{1/2,(1-p)^n\}.}
\]

The upper bound is the mean optimum conditional on each seed; the described policies attain it. Z carries no initial information about W, but supplies **persistent coordination between decisions**. It is not equivalent to fresh independent random numbers at each decision. A writable protected bit that can store W would be another, stronger architecture and could give perfect performance here.

This refutes any careless claim that all randomization or all one-bit memories have the same operational effect.

## 7. Knowledge among survivors can be misleading

Under symmetric preservation, live context masses after n cycles are `(1-p)^n/2` each, and the physical latch equals W. Therefore

\[
I(W;M\mid\text{alive})=1\text{ bit},\qquad
P(\text{alive})=(1-p)^n\to0\quad(p>0).
\]

One bit *conditional on surviving* is not a guarantee of organizational continuity. The unnormalized live measure in C1 and the mass-aware decision formula in T3.D retain this distinction.

## 8. Calculus and asymptotic instruments

For the robust value,

\[
\frac{\partial V_n^{\rm robust}}{\partial p}=-n(1-p)^{n-1},\qquad
p\le1-(1-\alpha)^{1/n}
\]

is necessary and sufficient for failure risk at most alpha over n cycles in this model.

The mean optimizer changes strategy at `(1-p)^n=1/2`, or

\[
p_c(n)=1-2^{-1/n}.
\]

This is a change in an optimization envelope; the physical kernel remains smooth in p. In the joint limit `p→0`, `n→infinity`, `np→tau`,

\[
V_n^{\rm robust}\to e^{-\tau},\quad V_n^{\rm mean}\to\max\{1/2,e^{-\tau}\}.
\]

The crossover is `tau=log 2`. This gives a dimensionless horizon/noise collapse, derived from an elementary product limit rather than a new universality claim.

For a **specified** sequence of repair errors `p_t∈[0,1/2]`, the same robust product proof gives `V_n^robust=product_t(1-p_t)`. Positive infinite-horizon robust survival occurs exactly when `sum_t p_t<infinity`. A finite homogeneous architecture with a strictly positive per-cycle error floor cannot satisfy that condition. A mechanism that progressively lowers error must itself be physically modeled and paid for; the sequence cannot be inserted as free perfection.

## 9. Recurrence certificates without probability approximation

For a stationary physical policy phi, compute its largest live support G such that every positive-probability successor from G stays in G and no row loses mass. Iterative deletion gives G exactly.

A single observation-consistent phi guarantees zero-error recurrent viability from an initial support iff that support is contained in G_phi. An integer/Boolean certificate uses `x_ca∈{0,1}` and `y_s∈{0,1}`:

- `sum_a x_ca=1` for each physical observation c;
- `y_s=1` for all initial states;
- for every positive edge `s --a--> s'`, `y_s+x_C(s),a-1 ≤ y_s'`;
- for every failure edge, `y_s+x_C(s),a ≤ 1`.

This is standard observation-consistent finite-controller safety synthesis. In our noisy renewal model, each world separately has four safe stationary controllers, but **no common controller** is safe for both. At zero repair noise the shared safe cycle exists.

## 10. Verified evidence and remaining research frontier

- Exact occupancy design was checked against an independent cycle-profile product oracle.
- All 16 deterministic one-cycle prescriptions were enumerated; the deterministic Pareto frontier was verified for multiple horizons and rational noise levels.
- **1,875** fresh randomized one-cycle laws were checked for the sum/product certificates.
- The initial local suite contains **18** new Python tests, in addition to repository tests.
- No general originality claim follows. The exact frontiers are results for this explicitly defined finite family; the broad machinery has strong antecedents.

Next: introduce genuinely adaptive choice of sensing, protected memory, energy harvesting and repair quality; preserve full information constraints; derive either a compositional viability certificate beyond classical baselines or a rigorous counterexample to the proposed reduction.

## Primary antecedents

- [Nayyar, Mahajan & Teneketzis (2012 preprint), common-information prescriptions](https://arxiv.org/abs/1209.1695): centralized design with decentralized/locally informed execution. Our recurrence specializes the general designer perspective to fixed physical memory and killed transitions.
- [Dibangoye, Buffet & Simonin (IJCAI 2015), structural control results](https://ijcai.org/proceedings/2015/14): plan-time occupancy statistics versus execution-time information; piecewise-linear value structure.
- [Junges et al. (UAI 2018), finite-state controller synthesis](https://proceedings.mlr.press/r16/junges18a.html): correct-by-construction bounded controllers and parametric Markov chains.
- [Inspection, Maintenance, and Repair with Partial Observability (1995)](https://doi.org/10.1061/(ASCE)1076-0342(1995)1:2(92)): older maintenance-POMDP antecedent. The linked publication establishes that maintenance under partial observation is not new.

## 11. Conditional bridge back to stochastic action and physical resource

Suppose a separate, fixed-causal-frame physical repair model justifies the **exponential surrogate** `p=exp(-J_rep/epsilon)`, with `p≤1/2`. The repair-noise parameter p above is a probability; epsilon here is the noise scale in that other physical model. Then the exact finite-family reliability requirement becomes

\[
\boxed{
J_{\rm rep}\ge-\varepsilon\log\left[1-(1-\alpha)^{1/n}\right].
}
\]

For fixed alpha and large n, the required action scale is

\[
J_{\rm rep}\gtrsim \varepsilon\left(\log n-\log[-\log(1-\alpha)]\right).
\]

This is exact under the stipulated exponential probability law and a derived large-n expansion, **not** an exact finite-noise Freidlin–Wentzell theorem. A large-deviation exponent alone omits prefactors and uniformity requirements when n also grows. To attach it to a real bistable repair model, derive the correct event/deadline rate and bound prefactors uniformly over the relevant policies and horizons.

If the organization has a physical action ceiling `J_rep≤J_max`, then under this surrogate the reliable lifetime is bounded by

\[
n\le\frac{\log(1-\alpha)}{\log(1-e^{-J_{\max}/\varepsilon})}.
\]

This is the most direct next coupling of T2's variational action, T3's causal authority/resources and T4's repeated-maintenance horizon. Neither J nor epsilon is automatically energy measured in joules.
