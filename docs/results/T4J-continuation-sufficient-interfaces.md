# T4.J — A present action is not a sufficient interface for future control

**2026-11-02. Status:** exact scoped derivations and rational certificates using classical value-directed POMDP compression, alpha vectors, Bellman residuals and finite-state realizability. **No originality or universal agency claim.** This increment executes the v8 interface-sufficiency gate rather than adding another physical component.

## 1. Keep the physical problem fixed

We reuse `cdka.composition.Contract` from v6, unchanged: three-cell memory, hidden health H, world drift, fallible correction/sensing/writing/actuation, service, finite balance and resource replenishment only on successful paths. Initial readable syndrome k=0 and balance b=4 are fixed in every comparison. The canonical source blob at the baseline commit is `d2b9ccc2253b326af5d494b6d14c5dac6666105c`.

A three-valued diagnostic Y is physically available at the beginning. Before any control action, an encoder writes M=f(Y) in at most K distinct diagnostic-code states; Y is then unavailable. The executing policy reads only M, the physical (k,b), and a declared stage clock. It never reads H or the designer's posterior. M is retained across the two epochs in the main experiment. This retained register is an explicit idealization/capacity constraint, **not** a free posterior or a new derived energy cost. The preinstalled decoder library can implement any of the declared two-step tables. A test restricts that library separately.

Diagnostic acquisition costs are identical/sunk before the comparison boundary. K counts **additional diagnostic-code states**, not all memory in the underlying three-cell organization. A ternary register has three physical distinguishable states; fixed-width binary encoding requires two bits. Neither cardinality nor fixed-width bits is mutual information.

The sensor has P(Y=y)=1/3 with healthy probabilities p_y=(e,1/2,1-e), e in [0,1/2]. Thus P(H=healthy)=1/2 for every e. This is an actual generative sensor: P(Y=y|H=h)=2 P(Y=y,H=h). The posterior numbers label the design calculation; runtime receives the diagnostic label Y, not an oracle for H.

At the next epoch, fresh readable (k,b) can carry information about the action and physical trajectory. These channels are included, not artificially removed. No extra Y copy, free observation history, persistent random seed or readable encoder label outside M is supplied.

## 2. Algebraic unit: a complete continuation

An admissible two-step plan pi is:
1. first action a, one of affordable hold/correct/refresh/service;
2. an action g(k',b') for each reachable, physically observable next state.

There are **64** such deterministic plans at the base state. Every plan has a survival vector

    alpha_pi(h) = P(alive after two epochs | H_initial=h, pi).

For a diagnostic signal y, use its unnormalized joint mass mu_y(h)=P(Y=y,H=h), and define

    u_y(pi) = sum_h mu_y(h) alpha_pi(h).

The hidden-health transitions are integrated into alpha, not handed to the controller. Failure mass is never normalized away. Every encoded signal that chooses the same plan uses the same physically compiled continuation, including how it will react to k',b'.

## 3. Proposition J1 — exact loss of a continuation interface

Let Gamma be a common finite library of physical continuations. The full-diagnostic benchmark and the optimal decoder for a code f have values

    V_Y = sum_y max_(pi in Gamma) u_y(pi),
    V_f = sum_m max_(pi in Gamma) sum_(y:f(y)=m) u_y(pi).

Therefore the exact compression loss is

    L(f) = sum_m [sum_(y:f(y)=m) max_pi u_y(pi)
                 - max_pi sum_(y:f(y)=m) u_y(pi)] >= 0.

**Zero-loss criterion:** L(f)=0 if and only if, in every code cell, the signals share at least one maximizing **complete continuation**:

    intersection_(y:f(y)=m) argmax_pi u_y(pi) != empty.

**Proof.** Every summand is nonnegative because the sum of individual maxima dominates any common choice. Equality holds iff a common maximizing pi reaches each individual maximum; finiteness makes this maximum attained. Zero-probability signals impose no constraint. QED.

This is an elementary max-sum identity / Bayes decision argument with continuation plans as decisions. It is not a new compression theorem. The earlier minimum safe-action cover is a special zero-error version. Importantly, replacing 'continuation' by 'first action' is invalid.

**Whole-program qualification.** The formula assumes that independently choosing one admissible continuation per code produces an implementable complete decoder. A shared circuit cost or a globally coupled prescription library can forbid some such assignments. Then maximize over the actual joint family; the expression above becomes only a relaxation. Data-processing comparisons likewise require the same physical experiment/library.

Randomization cannot improve this finite mean objective when encoding and each table may be optimized freely: for a fixed decoder the objective is affine in the encoder, and for a fixed encoder it is affine in each table choice. A deterministic maximizer exists. Expected-cost coupling, minimax guarantees and persistent correlated randomness are different contracts.

## 4. Exact geometry in the original kernel

For p=P(H_initial=healthy|Y), the value of a plan is the affine line

    v_pi(p)=p alpha_pi(0)+(1-p)alpha_pi(1).

The upper envelope of all 64 lines has exactly three active continuations:

| Plan | First action | Second action if unanimous | Second action if discordant | alpha healthy | alpha degraded |
|---|---|---|---|---:|---:|
| A (index 50) | service | hold | refresh | .802544803986 | .776128934336 |
| B (index 58) | service | refresh | refresh | .843492469862 | .774863451679 |
| C (index 42) | refresh | refresh | refresh | .880959281319 | .434934892766 |

All three first actions leave balance 3 after success. Actual code-generated policies read k and b, not the posterior p. The exact switches are

    p_AB = 3734866303040 / 124585244227163
         = .0299784001404694...,
    p_BC = 106227674660136454136000 / 117936053240605881436351
         = .9007226521597878....

An exact upper-hull algorithm derives these rational intersections. Every competing line is checked at both endpoints of each hull interval; linearity certifies the whole continuum, not only a sampled grid. Raw physical bit-mask enumeration independently agrees with both alpha coordinates of all 64 plans.

### Same immediate action, incompatible optimal suffixes

At p=.01, plan A is optimal; at p=.5, plan B is optimal. Both prescribe service now. If the next record is unanimous, A holds and B refreshes. The same current choice cannot justify merging their diagnostic histories losslessly.

## 5. Three states are necessary for exact composition in the fixture

For the equal-weight diagnostic with p=(.01,.5,.99), the three signals have different optimal continuation profiles (A,B,C; payoff-equivalent hold/service ties do not create a shared plan).

| Diagnostic-code capacity | Best survival across two epochs | Loss vs full diagnostic |
|---:|---:|---:|
| 1 | .8091779607700227 | .0115120696421331 |
| 2 | .8204089133546236 | .0002811170575321 |
| 3 | .8206900304121558 | 0 |

The two-code optimum groups the first two signals: f=(0,0,1). Its exact loss is

    43924540239395040459 / 156250000000000000000000.

In percentage-point units, the third diagnostic state improves survival by **0.0281117058 point**. Exact sufficiency has a strict mathematical threshold, but the operational gain is small. No claim is made that an extra physical memory cell or protective circuit is worth its real cost.

For a **single** epoch at these same signals, two code states suffice: hold at the first two diagnostic labels and refresh at the third. Thus exact decision sufficiency at one epoch need not compose into exact sufficiency for two.

A one-code architecture is not a wholly memoryless agent: the original three cells, syndrome, resource and clock remain. Only the diagnostic interface is collapsed. An extra durable copy of Y would restore the full value, but that copy is exactly the physical resource excluded by the K bound.

## 6. The horizon does NOT monotonically determine memory needed for a new optimum

Change only the initial diagnostic accuracy to p=(.15,.5,.85), preserving the fair health prior and the physical kernel. The one-epoch optimum still distinguishes hold from refresh, requiring two diagnostic codes. The two-epoch optimum chooses the **same complete plan B** for all three signals, requiring only one.

    Required exact diagnostic codes: one epoch 2 -> two epochs 1.

At e=.01 the direction was 2 -> 3. Hence no general monotonic law follows for the memory needed to attain separately optimized horizon-specific objectives.

This does **not** contradict monotonicity when the specification is expanded: a code required to preserve every decision problem in a family cannot become easier to construct by adding more required tasks. Changing the endpoint objective is not the same as adding constraints while retaining earlier ones.

It also does not show that noisier sensing improves control. The value decreases or stays constant under sensor garbling when interfaces and costs are fixed; a smaller code can suffice because the attainable benchmark itself has changed.

If the requirement is instead to predict the outcome probabilities of **every** candidate continuation for each initial Y, the three distinct p values remain different whenever e<1/2: one nonconstant alpha line already separates them. Exact prediction and optimal-action sufficiency are different requirements.

## 7. Proposition J2 — recursive update must itself be physically realizable

Let h be a design-time name for an observable history, c_t(h) its proposed physical code, and let a,o be the common actual action and next readable signal. A deterministic update

    c_(t+1) = g_t(c_t,a,o)

exists on the declared reachable graph iff

    c_t(h)=c_t(h') and the same (a,o) is possible
    implies c_(t+1)(h a o)=c_(t+1)(h' a o).

**Proof.** Necessity follows because a function cannot output two distinct values on one input. For sufficiency, assign the uniquely agreed output to each reachable triple and complete unused inputs arbitrarily. QED. Library membership, runtime space and resource costs must still be checked separately.

This is a finite congruence/realizability condition, not a new automata theorem. The verifier returns the conflicting pair if it fails. When the low and medium diagnostics are merged and both observe 'unanimous' after service, the desired distinct suffix label cannot be regenerated from that common code and observation. Recomputing a posterior from an erased original Y would introduce an unmodeled memory channel.

Keeping the initial distinction or adding an actual new observation can fix the conflict. A mere calculation in the designer does not.

## 8. Proposition J3 — value loss decomposes along the actual surviving trajectories

In a finite-horizon history-based reference problem let V*_t(h) be optimal survival and Q*_t(h,a) its continuation value. H_t is a full **observable** history, not the hidden physical health. Let pi be any physically implemented compressed controller also admissible in the reference class. Define its Bellman deficit

    e_t(h,a)=V*_t(h)-Q*_t(h,a) >=0.

Then

    V* - V^pi = sum_t E_pi[1{alive at t} e_t(H_t,A_t)].

**Proof.** Conditional expectation gives Q*_t(h,a)=E[1{next alive} V*_(t+1)(H_(t+1)) | h,a]. Subtract adjacent value terms and telescope along the actual pi occupancy; V*_N=1 on surviving histories and 0 on death. QED. This is the classical performance-difference/Bellman-residual identity applied to a killed process, not a new invariant.

If e_t<=epsilon_t on the relevant reachable histories, loss is at most sum_t P_pi(alive at t)epsilon_t, hence at most sum epsilon_t. An early death has already been charged to its earlier deficit; conditioning it away is invalid. At zero loss every positive-mass deficit vanishes.

In the two-code fixture, the loss at the first action is exactly zero. **All .0002811170575321 loss occurs in the continuation decision.** Initial-action correctness would entirely miss it.

This certificate is policy/task-relative and can be weaker than preserving every transition law. Conversely, it does not grant recursive code updates or physical circuits for free. The code must pass J2 and its actual library/budget constraints before the value identity is used.

## 9. Compression versus transport

If a flagged erasure with probability rho independently destroys the diagnostic code **before selecting a plan**, without changing health, the event, resources or the decoder, then

    V_f,rho = (1-rho)V_f + rho V_constant.

The erasure flag itself is a readable state. The derivative is V_constant-V_f. This is a calibration identity, not the v8 harmful-driver formula: it assumes no faulty output selection or age-dependent health change. When any such mechanism is introduced, use the full joint physical oracle.

## 10. Prior-art audit and remaining contribution gate

The current work is **an instrument and a scoped counterexample package**, not a novel theory of information states. The strongest direct predecessors are:

- Poupart & Boutilier, *Value-directed Compression of POMDPs*, NeurIPS 2002. Its lossless condition explicitly preserves rewards and recursive compressed transitions; its linear version uses invariant/Krylov subspaces. [Author abstract](https://www.cs.toronto.edu/~cebly/Papers/vdib-abs.html), [paper](https://www.cs.toronto.edu/~cebly/Papers/vdib.pdf). Pages 3–4 and the relevant theorem were inspected. This directly anticipates the general idea of continuation-preserving compression.
- Subramanian, Sinha, Seraj & Mahajan, *Approximate Information State*, JMLR 23(12), 2022. [Primary article page](https://jmlr.org/papers/v23/20-1165.html). Recursive sufficiency and bounded approximate-policy loss are established antecedents.
- Andriushchenko et al., *Inductive synthesis of finite-state controllers for POMDPs*, UAI 2022. [Primary article](https://proceedings.mlr.press/v180/andriushchenko22a.html). Candidate library plus teacher/oracle is the next instrument if exact enumeration becomes expensive.
- Wang et al., *What to Preserve in Recursive Computation: A Local Predictive Sufficiency Principle*, arXiv 2610.04303, 2026-10-03. [Preprint](https://arxiv.org/abs/2610.04303). A recent directly adjacent recursive-prediction program; abstract/formulation inspected, exhaustive theorem equivalence audit pending. Do not claim priority over its local-interface language.

The genuine next obligation is a joint physical interface/circuit constraint under a changing maintenance architecture that these ordinary abstractions cannot replace without losing a substantive restriction. The current two-epoch result does not yet meet that originality gate.

## 11. Reproduce and falsify

- `python -m unittest discover -s tests -p 'test_continuation_interfaces.py' -v`
- `python -m experiments.continuation_sweep`
- `python -m experiments.continuation_sweep --check`

16 tests; 64 continuation plans checked against raw three-cell transitions (128 initial-health coordinates); exact continuous envelope; all labeled encoders at capacities 1–3 on four diagnostic laws; residual decomposition; forbidden-decoder, hidden-memory and update-conflict falsifiers.

The experiment extends the number of decision epochs, not the baseline physical law. Current limitations: finite three-output initial sensor, retained diagnostic register, two epochs, known model, fixed resource prices, and an installed unconstrained meta-decoder. No spontaneous goals, physically calibrated memory-energy law or full recurrent self-maintenance theorem is asserted.
