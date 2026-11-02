# T4.I / T3.H — Decision-relevant diagnosis through repair and a fallible selector

**2026-11-02. Status:** exact finite-family derivations using classical Bayes decision, channel composition and finite-state-controller tools. No priority or general agency claim. This advances R11/R14 but does not complete recurrent joint maintenance.

## 1. Fixed physical and informational contract

We retain the v6/v7 terminal physical failure event, syndrome k=0 and two relevant interventions: HOLD=0 and REFRESH=1. Their exact conditional success probabilities, obtained from `cdka.composition.macro_row`, are:

| Hidden corrector health H | HOLD | REFRESH |
|---|---:|---:|
| healthy 0 | 0.894557536 | 0.945778666584 |
| degraded 1 | 0.872081216 | 0.6594959384 |

The new experiment contains:
- Initial hidden health H, with a fair prior in the scalar propositions (the exact oracle allows arbitrary prior).
- A diagnostic BSC with error eta writes a physical register M.
- **n compulsory repair intervals in both diagnosis and skip arms.** Each interval changes H with probability nu; flips an intact M with probability omega; and erases it to a visible symbol bottom with probability rho. A protection program prevents erasure but not flipping or obsolescence. These channels are conditionally independent in the scalar family.
- A separate hidden selector health S, initially bad with probability z. A healthy selector wears to bad with probability d per interval; bad stays bad. An optional late maintenance operation restores it with probability r. Its outcome is not read or handed to the policy. Selector errors are theta_good <= theta_bad <=1/2.
- An installed deterministic table g:{0,1,bottom}->{HOLD,REFRESH}. The only runtime input to it is M. No H, S, previous reading, resource pattern, persistent private seed or forgotten action is supplied.
- A symmetric-flip output driver: conditional on S, the requested command is inverted with probability theta_S. The alternative **fail-silent driver** sends HOLD when the same kind of fault occurs. These are DIFFERENT physical architectures, explicitly compared rather than silently exchanged.
- All paths have the same deadline and terminal event. Diagnostic failure zeta kills mass instead of renormalizing it. The skip arm uses the original fixed-command physical bypass, not the new contingent driver; the original v6 execution failures remain in its payoff.

### Pathwise resource contract

Every arm pays n tokens for the compulsory repairs. Diagnosis costs 1, installing the table costs 1, and **2 tokens are reserved for actual REFRESH even when the requested command is HOLD**, because the faulty driver may invert it. Protection costs n more; servicing the selector costs 1 more. Diagnostic programs therefore require

    B >= n + 4 + n * protect + service.

Charges are independent of the diagnostic outcome; unused reserves are not read as a channel. Protection and servicing are precommitted program choices. These are model tokens, not joules or generic circuit lower bounds. Alternative hardware costs change the result.

## 2. Proposition I1 — an exact decision-margin identity

Let mu(h,s,m) be the unnormalized terminal mass after all diagnostic/repair/service operations. It may contain arbitrary correlation between H and S. Put

    d_h = v_h(REFRESH)-v_h(HOLD),
    B_hold = sum_(h,s,m) mu(h,s,m) v_h(HOLD),
    A = sum_(h,s,m) mu(h,s,m) theta_s d_h,
    D_m = sum_(h,s) mu(h,s,m)(1-2 theta_s)d_h.

For the flip driver and independently implementable choices by each signal,

    V_diag* = B_hold + A + sum_m max(0,D_m).

**Proof.** Requesting REFRESH with probability x_m yields B_hold+A+sum_m x_m D_m. Maximize each affine term over x_m in [0,1]. Deterministic x_m=1{D_m>0} attains the bound; randomization adds no value to this one-step expectation. This is an elementary Bayes decision identity, not a new information measure. QED.

The whole-table physical library must really permit these independent choices. With coupled implementation constraints use the linear objective over the actual feasible table set; replacing it by all rows is a relaxation. If actions, timing or resource traces encode information, they must enter m/the full causal cut.

I1 remains valid for correlated H/S: averaging theta independently before weighting the state-dependent decision losses generally does not.

## 3. Proposition I2 — closed form in the symmetric independent family

Define

    g = v_0(REFRESH)-v_0(HOLD) = 0.051221130584,
    l = v_1(HOLD)-v_1(REFRESH) = 0.2125852776,
    L = l-g > 0,
    V0 = [v_0(HOLD)+v_1(HOLD)]/2 = 0.883319376.

After n intervals,

    e_n = [1-(1-2 eta)((1-2 nu)(1-2 omega))^n]/2,
    a_n = (1-rho)^n              (or 1 under protection),
    z_n = 1-(1-z)(1-d)^n,
    theta = theta_good + z_n(theta_bad-theta_good),

with z_n replaced by (1-r)z_n after servicing. Put U=[g-e_n(g+l)]_+.

Under the flip driver, I1 reduces to

    V_diag* = (1-zeta)[V0 - theta L/2 + a_n(1-2theta)U/2].

**Proof.** The retained messages have signed advantages [g-e(g+l)]/2 and [eg-(1-e)l]/2. The second is nonpositive for e<=1/2 and l>=g. The erased symbol has advantage (g-l)/2<0. The signal-independent flipping offset is theta(g-l)/2. Multiplication by retention and diagnostic survival gives the expression. QED.

The overall achievable value also includes the skip branch and unaffordable programs are excluded. In the default fair-prior geometry the base is V0. A paid diagnosis has positive net value exactly when

    a_n(1-2theta)U > theta L + 2 zeta V0/(1-zeta),

for zeta<1. With zeta=1 it is always useless. Boundary cases a_n=0 and theta=1/2 are evaluated directly, not divided by zero.

### Irrecoverable loss versus risky use

When theta=zeta=0, flagged erasure scales the gain by a_n without changing its sign. An intact informative message can help, and an erased one triggers the safe constant choice. With a flip-prone selector, even requesting the fallback HOLD can produce a damaging REFRESH. The apparatus now needs enough remaining advantage to justify being activated at all.

For a stable world and no bit flips, eta=0, rho=.2, theta=.05, zeta=0, the diagnostic still carries .8^n bits. Its net gain is positive through n=7, negative at n=8, even though it still retains .16777216 bit at n=8. A finite expiry of **actionable value** can arise without all information disappearing.

## 4. Proposition I3 — same fault frequency, different operational meaning

For a fail-silent driver (a fault forces HOLD rather than inverting the command), the analogous value is

    V_diag,silent* = (1-zeta)[V0 + a_n(1-theta)U/2].

Proof is again affine maximization; requesting HOLD is no worse when a fault occurs. With zeta=0, all a_n>0, theta<1 and U>0 give a positive gain, irrespective of how small it is.

This does **not** assert that fail-silent hardware is free or easy to build. It isolates the fault contract needed to eliminate the detrimental term -theta L/2. Pricing a separate trusted guard and maintaining it is an open obligation. The result falsifies treating component "reliability" as a sufficient physical specification.

## 5. What to maintain first? A marginal-benefit certificate

Fix e, n=1, zeta=0 and the relevant action geometry. Suppose equally priced options either eliminate erasure or reduce theta to theta_1. Write a=1-rho. Their improvements over the same installed unprotected driver are exactly

    gain_protect = (1-a)(1-2theta)U/2,
    gain_service = (theta-theta_1)[L+2aU]/2.

Protection saves decision distinctions; service both preserves their execution and reduces harmful command inversions. Their relative value is task-dependent, not determined by retained bits.

Default eta=.05, rho=.6, z=.5, theta_good=0, theta_bad=.3, r=.8, nu=omega=d=zeta=0:

| Budget | Optimal feasible program | Total terminal survival |
|---:|---|---:|
| 4 | bypass / skip | .883319376 |
| 5 | skip (paid diagnosis would achieve .876541378398) | .883319376 |
| 6 | service selector + diagnosis | .8880487061076224 |
| 7 | protect register + service + diagnosis | .898773394576916 |

At budget 6, protection alone gives .884527848534708, less than servicing. The unprotected diagnostic carries .285441217154 bit about current H, but at budget 5 using its faulty circuit still underperforms bypass. Program selection avoids that loss.

### Same health marginals are not enough

With perfect M=H, P(H=1)=P(S=bad)=1/2 and selector errors (0,.4), two joint laws with identical marginals yield:
- S=H: .866412885772;
- S=1-H: .8986857151752.

The selector being bad precisely when choosing a mistaken REFRESH is expensive makes a difference. I1 handles both; plugging average theta into I2 does not. The simple independent formula is not a general theorem about shared substrates.

## 6. Proposition I4 — a task-specific bit can be optimal before noisy storage

For a finite diagnostic alphabet y, let d_y be its signed, probability-weighted advantage of REFRESH over HOLD. One encoder bit z=f(y) passes through the same symmetric bit-flip/flagged-erasure channel and independent flip driver as above, with outcome-independent cost.

**Claim:** an optimal one-step encoder groups positive d_y separately from nonpositive d_y (or reverses the bit labels). This is task sufficiency, not reconstruction of hidden health.

**Proof.** If A=sum_{f(y)=0}d_y and D=sum_y d_y, the two non-erased output margins are affine in A: omega D+(1-2omega)A and (1-omega)D-(1-2omega)A. The erased output is fixed. The optimal decoder value is the sum of positive parts of affine functions, plus constants; hence convex in A. Feasible A lies between sum of negative d_y and sum of positive d_y, and both endpoints are attained by the sign partition. A convex function attains its maximum at one of these endpoints. Symmetric relabeling gives the same optimum. QED.

This reduction can replace exponential encoder enumeration with signed-margin accumulation **under its stated channel and implementation assumptions**. The exact oracle enumerates all binary encoders/decoders on 125 three-signal integer-margin instances. Asymmetric or signal-dependent failures, label-dependent costs and constrained encoder circuitry require a new analysis.

It does NOT provide recursive sufficiency. A single action safe in both worlds makes today's optimal code constant; tomorrow's opposite required actions may need the distinction that was discarded. An explicit two-task counterexample is retained in tests.

## 7. Verification, novelty and next gate

18 Python tests, including 486 channel/driver/architecture cases, 80 correlated live-mass examples, 125 encoder cases, exact microstate propagation, exhaustive eight-policy terminal decoding, nested v7 values and adversarial bypasses. Fractions preserve exact equality; browser charts use verified floating-point fixtures.

This remains a one-episode diagnostic-to-actuation bridge, possibly spanning several repairs. Maintenance is precommitted and selector health is latent; it is not a solved recurrent diagnosis/selector-maintenance POMDP. Protected memory is one physically specified alternative; a durable actuator trace is a stronger bypass, not an allowed free register. The terminal v6 decoder/observation interface remains a declared primitive.

**Next:** produce a certificate for concatenating these modules while retaining a physically sufficient interface. A terminal positive-margin bit need not support a later maintenance choice. Seek the smallest extra physical statistic needed for two successive tasks, compare to FSC synthesis, and stop adding components if the only outcome is a larger standard POMDP.

## Primary antecedents / audit

- Blackwell (1953), *Equivalent Comparisons of Experiments*, DOI 10.1214/aoms/1177729032. Classical comparison of information experiments, not a new CDKA principle.
- Junges et al. (2018), *Finite-State Controllers of POMDPs using Parameter Synthesis*: https://proceedings.mlr.press/r16/junges18a.html . Bounded physical memory and executable control are established machinery.
- Andriushchenko et al. (2022), *Inductive synthesis of finite-state controllers for POMDPs*: https://proceedings.mlr.press/v180/andriushchenko22a.html . A successor if brute-force synthesis stops scaling.
- *State observation accuracy and finite-memory policy performance*, https://www.sciencedirect.com/science/article/abs/pii/S0167637713000801 . Prior warning that limited controllers do not automatically benefit from a better sensor. Our optimized single-episode fixed-interface formulas remain monotone in information; acquisition/hardware costs change the physical experiment.
- Fenwick, Claxton & Sculpher (2008), DOI 10.1177/0272989X07308751. Value of information and implementation have been studied jointly outside this physical-controller model; no priority claimed for that verbal distinction. Full-text comparison remains pending.

Implementation: `cdka/diagnostic_transport.py`; independent checks: `tests/test_diagnostic_transport.py`; executable fixtures: `experiments/diagnostic_transport_sweep.py`.
