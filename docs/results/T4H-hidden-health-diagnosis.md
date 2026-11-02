# T4.H — Health diagnosis is useful only if the organization can act on it

**Scientific status (2026-11-01):** exact finite-model proposition and enumerated witnesses using classical Bayesian value-of-information and finite-state-controller tools. **Originality unestablished.** This is an extension of the v6 physically readable three-cell corrector, not a new general theory of knowledge.

## Question, causal contract and motivation

When a corrector's health is hidden, can purchasing a measurement improve physical viability if the same organization must also fund the diagnostic, an input-contingent selector, and the terminal intervention? When does a correct *past* diagnostic cease to justify a *present* action?

We fix the v6 `cdka.composition.Contract` physical kernel, including world drift, noisy cells, correction, fresh sensing, execution errors and resource acquisition only after success. At the **current** live epoch boundary, the three-cell disagreement syndrome `k∈{0,1}` and integer resource `B` are physically readable. Health `H∈{0,1}` is hidden, with `H=0` healthy, `H=1` degraded. The v6 mathematical state `(k,H,B)` is no longer claimed to be a runtime signal.

A mandatory interval occurs **in both** the diagnosis and no-diagnosis arms. During that interval health flips with probability `ν`, independently of diagnosis noise. The test reads initial health through a symmetric BSC of error `η` and writes one physically readable bit `Y`; it consumes `d` resource tokens and fails irreversibly with probability `ζ`. Using `Y` to select different terminal interventions additionally requires a selector circuit costing `c` upfront; `d,c` are fixed and do not depend on the observed result. Terminal actions retain their exact v6 costs (`hold:0, correct:1, refresh:2, service:2`). All other resources and relevant clocks are held fixed. These are **stipulated architectural costs**, not joules.

The terminal policy without diagnosis is constant with respect to H. With paid diagnosis and installed selector, it is a mapping `g:{0,1}→A(B-d-c)`. The controller does **not** receive H, a posterior distribution from the designer, forgotten history, or outcome-dependent budget signaling. The v6 physical failure event is identical in both arms; action success is `1-K_H^a(death)`.

## General exact one-step evaluation (no equal-prior assumption)

Let `p_h=P(H_initial=h)`, `O_η(y|h)` be the binary diagnostic kernel, and `D_ν(h'|h)` be health drift during the mandatory interval. Define

`m(h',y)=sum_h p_h O_η(y|h) D_ν(h'|h)`.

Let `v_{h'}(a,b)=1-P(death|k,h',b,a)` using the *same* terminal physical kernel. Then

\[
 V_{\rm skip}(B)=\max_{a\in A(B)}\sum_{h',y}m(h',y)v_{h'}(a,B),
\]

\[
 V_{\rm diag}(B)=
 (1-\zeta)\sum_y\max_{a\in A(B-d-c)}\sum_{h'}m(h',y)v_{h'}(a,B-d-c),
\]

when `B≥d+c`, and diagnosis is physically unavailable otherwise. In either case, only physically affordable actions enter the maximum. The overall optimum is `max(V_skip,V_diag)`. Each maximum is attained by a deterministic physical prescription over a terminal stored bit. Randomization cannot improve this one-step expected survival because the objective is affine in action probabilities.

**Proof:** expand the joint distribution of `(H_initial,Y,H_final)` using the declared independent channels. Without diagnostic input, the action must be constant. After paying for the selector and test, independent choices by each `Y` are exactly the installed controller's capability; maximization separates by `Y`. Irreversible diagnostic failure scales the surviving branch by `1−ζ`. No posterior is used at runtime. QED.

This is the standard one-step Bayes value-of-information calculation with a **whole-policy resource constraint**. It is not novel by itself.

## Exact two-action phase transition

For the default v6 corrector, one epoch, `k=0`, and a uniform hidden-health prior, the relevant actions are `hold` and `refresh`: `correct` and `service` never improve the one-step action-success score over `hold` at a fixed affordable budget. Their conditional success values (exact rational fractions in the code) are:

| Hidden health | Hold | Refresh |
|---|---:|---:|
| healthy H=0 | 0.894557536 | 0.945778666584 |
| degraded H=1 | 0.872081216 | 0.6594959384 |

Put

\[
 g=v_0({\rm refresh})-v_0({\rm hold})>0,\quad
 \ell=v_1({\rm hold})-v_1({\rm refresh})\ge g.
\]

Without health information, `hold` is optimal and `V_0=[v_0(hold)+v_1(hold)]/2`. For the diagnostic, the effective BSC error with respect to **health at actuation time** is

\[
 e=\eta+\nu-2\eta\nu
   =\frac{1-(1-2\eta)(1-2\nu)}2.
\]

**Proposition H1.** Assume no diagnostic failure `ζ=0` and resources sufficient for `d+c+cost(refresh)` in the diagnostic branch. Then the exact improvement is

\[
\boxed{\Delta V=\frac12\max\{0,\ g-e(g+\ell)\}.}
\]

In particular, diagnosis improves the optimal decision iff

\[
\boxed{e< e_* =\frac{g}{g+\ell}.}
\]

**Proof:** conditioning on `Y=0`, the expected conditional advantage of refresh over hold is `(1-e)g-eℓ`. Conditioning on `Y=1` it is `eg-(1-e)ℓ≤0` because `ℓ≥g` and `e≤1/2`. Hence choose refresh only after Y=0 and only if the first advantage is positive. Each Y occurs with probability one half. QED.

For the default kernel

\[
 g=\frac{6402641323}{125000000000},\quad
 \ell=\frac{265731597}{1250000000},\quad
 \boxed{e_*=\frac{6402641323}{32975801023}\approx0.194161813341.}
\]

A perfect diagnosis yields `V_skip=0.883319376`, `V_diag=0.908929941292`, an exact gain `0.025610565292`. At error `η=0.1,ν=0` the gain is `0.0124202448828`. At error `η=0.2`, no benefit is attainable by any installed two-output diagnostic decoder.

For nonzero diagnostic failure, the net gain becomes

\[
\Delta V_{\zeta}=\max\{0, (1-\zeta)[V_0+\tfrac12(g-e(g+\ell))_+]-V_0\}.
\]

At perfect diagnostic and no drift, diagnostic failure `ζ` eliminates any benefit when `ζ≥6402641323/227232485323≈0.02817661`.

### Physical affordability boundary

For the studied default `d=c=1`, `refresh` costs 2. With resource `B=2,3`, diagnosis cannot make `refresh` affordable after buying its sensor and selector, so its value is no better than `hold`, even for perfect diagnostic information. Only at `B=4` is the contingent map `(Y=0→refresh,Y=1→hold)` physically implementable and beneficial. This is **not** a universal `B≥4` rule: it depends on the declared costs and possible alternative operations.

### Observation age

If health changes independently with probability `ν` across `d_t` elapsed intervals, the error relative to present health is

\[
 e_{d_t}=\frac{1-(1-2\eta)(1-2\nu)^{d_t}}2.
\]

With `η=.05,ν=.10`, the error is `.05,.14,.212,.2696,…` for elapsed intervals `0,1,2,3,…`: the diagnosis helps only during the first two values in this example. The same measurement remains informative about the *past* health even when it is no longer useful for the *current* action.

## A separate multistep information-pattern gap

With health hidden, consider the **restricted** physical controller whose readable state is only `(k,B)` plus a declared stage clock; no implicit posterior or health flag is granted. Design-time occupancy may be used to compile a fixed sequence of prescriptions, but not supplied during execution.

The exact occupancy recursion is

\[
F_0(\mu)=\|\mu\|_1,\qquad
F_{n+1}(\mu)=\max_{\phi:(k,B)\to A(B)}F_n(\mu Q_\phi).
\]

The full-health-observed Bellman recursion is an upper bound, not an implementable baseline. From the uniform-health state `(k=0,B=4)` in the original v6 physical kernel:

| Epochs n | Best stage-clock/(k,B) prescription | Health-visible relaxation | Gap |
|---:|---:|---:|---:|
| 1 | 0.8833193760 | 0.9089299413 | 0.0256105653 |
| 2 | 0.8091779608 | 0.8513094382 | 0.0421314774 |
| 3 | 0.7386942711 | 0.8008554458 | 0.0621611747 |

These values use exact rational state-transition propagation. They are **not** the value of allowing a paid diagnosis in every epoch; the models are intentionally distinct to avoid confusing policy design with runtime observability. At horizon 2 the restricted planner is independently checked against exhaustive first/second-stage prescriptions; at horizon 3 the occupancy design uses 9,733 memoized design nodes in this fixture.

## What the result falsifies

1. A quotient `(k,h,b)` can be mathematically exact but no longer physically observable if `h` is hidden.
2. A correct diagnostic bit need not yield a better achievable action if the selector or intervention is unaffordable.
3. A diagnosis of *past* health need not help control the present organization.
4. A risky diagnostic can reduce survival even when its answer would improve conditional decision accuracy.
5. Availability of each action separately does not prove implementability of the contingent truth table. It requires a physically funded selector.

## Toolchain, limits and novelty

- Exact rational Bayes decision: partial-observation value.
- Blackwell/data processing: diagnostic garbling and health-change timing.
- Whole-prescription feasible sets: implementation cost and non-rectangularity.
- Unnormalized occupancy DP: no survival conditioning or free runtime belief.
- Independent full-health relaxation: strict information-pattern gap.
- Rational exhaustive terminal decoder: verifier, not proof of a general theorem.

The health transition and sensing are independent conditional on previous health. Diagnostic costs are constant across outcomes, so the resource balance does not act as an unmodeled health-signaling channel. The physical cost unit is a model token, not energy. A selector cost of `c` is a declared library contract; alternative circuitry may realize the same mapping more cheaply. No general infinite-horizon or self-constituted objective is claimed.

**Primary antecedents:**
- Ellis, Jiang & Corotis (1995), [Inspection, Maintenance, and Repair with Partial Observability](https://doi.org/10.1061/(ASCE)1076-0342(1995)1:2(92)).
- Kim, Choi & Lee (2018), [POMDP framework for joint maintenance, inspection and sensor installation](https://doi.org/10.1016/j.compchemeng.2018.02.015).
- Lin, Song & Pozzi (2022), [Optimal inspection of binary systems via Value of Information](https://doi.org/10.1016/j.ress.2021.107944).
- Winterer et al. (2024), [Strong Simple Policies for POMDPs](https://doi.org/10.1007/s10009-024-00747-0).

**Implementation:** `cdka/hidden_health.py`; **independent checks:** `tests/test_hidden_health.py`. **No mathematically original theorem is asserted.**
