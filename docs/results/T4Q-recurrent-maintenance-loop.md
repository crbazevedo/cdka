# T4.Q / T3.M — A diagnostic-controlled recurrent maintenance loop

**2026-11-05 · Executed contribution.** One finite process connects a physically stored diagnosis, a fallible maintenance decision, a shared gate bank, stochastic restoration, task execution, diagnostic renewal, wear and a pathwise resource account. An exact stochastic-emission reduction gives a12-phase evaluator for the64-state physical process. A finite library comparison exhibits an attainable survival target unavailable to its diagnosis-blind stationary sublibrary.

This is a NEW recurrent benchmark, not the old SERVICE-first terminal task repeated without change. The six-NAND voter and calibrated healthy/degraded rates are inherited from v15. No universal or thermodynamic cost claim is made.

## 1. Frozen causal and resource contract

Live state `(Z,M,b)`: hidden bank health Z=0/1, stored three-bit diagnostic M=(a,b,c), and readable reservoir b∈{1,2,3,4}. There are64 states. The v15 six-NAND bank is reused for selection and task execution. Errors are .001/.02 per gate in healthy/degraded modes, fresh conditional on the persistent mode; fanout preserves the actual signal.

Default calibration: diagnostic bit error .15; task-sensor bit error .02; healthy-bank wear .05 per cycle; restoration success .8; fatal procedure risk .005. These are explicit model parameters, not measurements. Initialization pays one diagnostic token from endowment4, leaving b=3. Initial health is equiprobable; conditional results are retained separately.

### Epoch order

1. Debit one operating token at the START. This common priced bundle includes task sensing, operation and diagnostic acquisition/write. Disabling unused diagnostic acquisition for blind designs would define another cost library.
2. A fixed installed program at balance3 or4 selects skip, request service, pass the noisy diagnostic vote, or invert it. At balances1/2 a resource guard forces skip. The same bank that needs service computes the vote. Guard and routing remain trusted base interfaces.
3. If service executes, debit two MORE tokens before harvest. It is permitted only for b≥3. Procedure failure is fatal. Otherwise restoration sets the bank healthy with probability .8; failure leaves its mode unchanged. The restoration outcome is hidden.
4. A fresh fair task bit W is sensed by three BSC(.02) readings. The same bank, in its actual post-service health, votes on them. Output≠W is absorbing failure.
5. Only success yields two tokens, capped at4: b'=min(4,b+1−2·service). Write a noisy diagnosis of post-service health. Then healthy may degrade with probability .05. The report can therefore be stale at the next decision.

No failure path harvests resources. No designer posterior or external reliable maintenance trigger enters the policy. Sensor fidelity, routing and guard reliability remain calibrated/trusted; this does not endogenize every infrastructure component.

### Two declared policy libraries

Four routing modes at each of two eligible balances give16 stationary programs. The diagnosis-blind sublibrary uses only skip/service, giving4 programs. Programs are fixed at installation. No horizon clock, adaptive program rewriting or arbitrary truth table over the whole memory is supplied. Installed gates, memory and consumable tokens are separate resources. The common routing cost is declared, not optimized here.

## 2. Physical kernel

Let v_z(m) be the exact output-one probability of the voter. The probability of a correct new task is

    w_healthy=.9952702938313536...
    w_degraded=.9322251541147811...

The service probability c_pi(z,m,b) is0/1 or v_z(m)/1−v_z(m), depending on the installed mode. Actual health affects it through the faulty hardware, not through a readable health input.

Conditioning on service r, post-service health h and next health z', successful transition mass is

    P(r|z,m,b) (1−zeta)^r P(h|z,r) w_h H(h,z') E_h(m').

E_h is the actual diagnostic channel. H is wear AFTER that measurement. Hidden outcomes are summed after composing their conditional later effects, never by replacing the bank with its mean gate error.

## 3. Exact regenerative realization

A phase is `(v,z,b)`, where v is health when the last report was written and z is current health. Only(v,z)=(0,0),(0,1),(1,1) occur: wear does not spontaneously heal. With four balances there are12 phases.

Let E(c,(z,m,b))=P(M=m|v) be the stochastic emission matrix. Let A_pi map a physical state to successful post-task/post-wear phases before drawing the next report. Then

    K_pi=A_pi E,      M_pi=E A_pi,
    E K_pi=M_pi E.

For initial acquisition mu0=lambda0 E and every sequence of installed policies,

    mu0 K_pi0 ... K_pit=(lambda0 M_pi0 ... M_pit)E.

**Proof:** conditional factorization yields K=A E. Associativity gives E K=(E A)E; induction gives the displayed identity. E is stochastic and A substochastic, so failure mass is preserved. The identity holds for every parameter in the declared grammar, not merely the numeric fixture.

An externally intervened initial register outside this emission family cannot simply be initialized in12 phases. One complete successful-cycle kernel still maps it into that family via mu A E. The hidden phase variables are evaluator coordinates, not an observation or a posterior given to the controller. This is not claimed to be a deterministic lumping of64 states into12 readable classes.

## 4. Exact library result

For fixed pi, survival is mu0 K_pi^n1=lambda0 M_pi^n1. Enumeration of all16 stationary programs at horizon8 selects the physical diagnostic vote at both eligible balances.

|Policy|V1|V8|V16|V64|
|---|---:|---:|---:|---:|
|Never maintain|.9637477240|.7325971487|.5214719653|.0503657294|
|Always when affordable|.9840209510|.9115317652|.8401960478|.5152913371|
|Use stored diagnostic|.9843666538|**.9174767896**|**.8541184980**|**.5560412679**|

Exact fractions, not rounded displays, determine all comparisons. Optimality is asserted for the evaluated eight-cycle stationary library, not every horizon or arbitrary history-dependent controller.

Every blind stationary program is bounded by .9115317652171799 at8 cycles. The diagnostic program attains .9174767896493894. Hence beta=.915 is an exact separating target. It was chosen AFTER analysis to display the strict separation, not as a preregistered empirical threshold.

This is a fair-prior mean, NOT a per-health guarantee. Diagnostic-policy values conditional on initial health are .9360758966041455 and .8988776826946334; always-maintain gives .9247179780371182 and .8983455523972417. Both contexts improve, but the degraded one is below beta.

Expected maintenance attempts over8 cycles, per initially deployed system, are1.2734000271 versus3.8507390345. Expected completed tasks are7.5875100242 versus7.5644314894. All live-prefix mass is counted, not only survivors.

## 5. What traces reveal

The immediate benefit of service at eligible balance is

    B_z=(1−zeta)sum_h P(h|z,service)w_h−w_z.

In this fixture B_healthy=−.004976351469156768 and B_degraded=.045522805443817684. Healthy service adds procedure risk without improving the bank; degraded service can restore enough reliability to help. Resources and future decisions can still alter the multi-epoch optimum.

A stale000 report in a degraded bank requests maintenance with probability .110414194688; the same word in a healthy bank does so with .005975052938035992. A hardware logic error can accidentally help when a report is stale and hurt when it is current. This is not a general claim that noise helps, nor evidence that the register knows hidden health.

The certificate contains116 complete conditional branch rows for four physical sources, including procedure and task failures. The full recurrent law is propagated exactly; those displayed traces are explanations, not a statistical estimator.

With diagnostic error eta=.5, the best stationary value is always-maintain's .9115317652, while diagnostic voting falls to .8844477041. Yet uniform report bits still produce vote-one probabilities .501617015984006 and .5294254592 in healthy/degraded hardware. No information in the input register does not imply absence of a physical health→action path.

## 6. Recurrence is not infinite survival

On every successful path b≥1 and every maintenance debit was funded beforehand. Resource feasibility is not silently violated. Nevertheless q*=max_z w_z=.9952702938313536...<1, and every epoch must execute a task. Every live row sum is at most q*, even with additional health-aware choice inside this primitive family. Consequently

    P(alive after n) <= (q*)^n -> 0.

The process closes an operational maintenance/resource loop, not thermodynamic metabolism, universal agency or infinite reliability. Recoverable task errors or a different task sensor/actuator contract would require new analysis.

## 7. Contribution and next boundary

The concrete advance is the jointly executable shared-bank loop, a policy-uniform stochastic-emission certificate, an exact library-relative viability separation and mechanistic maintenance accounting. Established FSC/POMDP and Markov-factorization tools enable this adaptation.

Next, let acquisition compete with physical retention at the same cost. Test when K_pi=A_pi E can still share one E. If it fails, extract the smallest report/health dependence needed, rather than supplying a free belief state. Separately price routing/guard failure before making stronger autonomy claims.

Primary methodological antecedents: [Junges et al., finite-state controllers](https://proceedings.mlr.press/r16/junges18a.html); [inspection and maintenance under partial observability](https://ascelibrary.com/doi/10.1061/(ASCE)1076-0342(1995)1:2(92)); [maintenance with a deteriorating sensor](https://repub.eur.nl/pub/102727). Contribution and priority are assessed at the actual coupling and guarantee, not dismissed because their algebraic tools are established.

## 8. Verification

17 scientific Python tests;192 independent raw microkernel rows;192 exact policy/phase intertwining rows;2048 scalar task mask/sensor cases;16 programs;4 blind programs;116 conditional causal branch rows. Fraction arithmetic determines decisive comparisons. Generated browser values are tested floating-point projections. Reproduce with `python -m unittest discover -s tests -p 'test_recurrent*.py' -v`, `python -m experiments.recurrent_sweep --write --check`, and `node --test tests/recurrent-lab.test.mjs`.
