# T4.S / T3.O — A priced physical compiler for selective acquisition

**CDKA v18 · 2026-11-05.** Executed contribution: one concrete NAND realizes a task-invisible update omission; the complete bounded selector/maintenance library is synthesized with an explicit installation/invocation/write ledger; a finite-horizon noise threshold is certified by exact polynomial arithmetic and mechanistic fault attribution. The result is an implementation-aware continuation/cost certificate, not a universal claim that less information is better.

## 1. Provenance reconciliation

Remote `main` at start was `a32b9a4bf7ecf558ce9bd7fadd90385698ba759f`: its canonical v17 studies renewal versus retention in `cdka/memory_renewal.py`. The previously delivered local v17 additive package additionally contains `diagnostic_retention.py` and an all-horizon write-elision lemma. Both are preserved. V18 depends only on the unchanged v16 `cdka/recurrent_maintenance.py`, Git blob `0a01bbf40f78f314a56285c15822e7ac06c9848b`, independently reproduces the omission, and does not overwrite either v17 history. The local D45 lesson is explicitly carried forward in the v18 additive ledger.

## 2. Frozen causal contract and a narrowly changed interface

The physical state is hidden bank health, three actual diagnostic cells, and readable token balance. The same six-NAND bank decides whether to service and performs work. Startup costs one token; each epoch reserves one common operation/acquisition slot. Service consumes two additional tokens before work. Only correct work returns two tokens, capped at four. Every alive prefix is retained with its ORIGINAL probability; no survivor normalization.

The added installed write-enable circuit sees only two existing physical signals:

- r: the executed service command (not whether service succeeded);
- x: whether the PRE-cycle balance was three, already distinguished by the resource routing library.

After successful work, its output either writes a fresh noisy diagnosis or retains the cells. No health readout, posterior, history pointer, new clock or diagnostic content enters this circuit. Retention is ideal in the principal synthesis. The physical task and operational token ledger remain unchanged.

Library: constants 0,1, input wires r,x, and up to two causal NAND gates. Each gate has a fresh independent output flip with probability gamma per invocation. Fanout shares the same physical noisy node. Initial routing and signal taps retain the baseline trusted-interface assumption. Installation of those common signals is not claimed free in physics; comparisons price only the NEW update circuit.

**Second ledger:** expected acquisition workload is priced separately in units of one diagnostic write:

    C = c_w E[number of writes, including startup]
        + c_g E[physical NAND executions]
        + c_I × installed NAND count.

This is an explicit accounting family, not a conversion to joules or an operational-token refund. Expectations are per initial system, not conditional on survival. A survival constraint prevents treating early death as efficient operation; savings are further decomposed into omitted writes and tasks lost.

## 3. Exact lossless omission and one-gate realization

The rule is

    enable = NAND(r,x) = NOT(r AND x).

It omits a write exactly after service from balance3. That successful branch leaves balance2. The next epoch is forced to skip service, cannot use the diagnosis in selecting maintenance, and then refreshes it. The task readings are acquired independently of that stored health diagnosis. Thus the interim contents cannot affect survival before replacement.

Let Q be all-refresh and T be the omission kernel on the48-class physical evaluator `(health, first cell, sum of last two cells, balance)`. Let D=T−Q. Every row of D is supported on balance2 and has zero mass separately at each health. Therefore

    D 1 = 0,       D Q = 0,       D T = 0.

Using `T^n−Q^n = sum_{t=0}^{n−1} T^t D Q^(n−1−t)` gives

    mu T^n 1 = mu Q^n 1     for every n>=0 and every initial live measure mu.

This applies to all sixteen baseline maintenance programs because balance2 is uniformly forced SKIP. It preserves health/balance/action behavior and survival, not equality of terminal memory. It depends on unchanged continuation access and a guaranteed next renewal.

The write-enable function is not among the zero-gate constants or individual signals; one NAND implements it. Within the declared library, exhaustive finite-horizon cost synthesis confirms the one-gate witness achieves the least example cost at zero allowed survival loss. The all-horizon preservation proof is separate from finite-horizon cost optimality.

## 4. Expected cost and amortization, not an invented energy saving

With vote/vote maintenance, eight epochs and the fair initial-health prior:

| Quantity | All refresh | Ideal one-NAND selective update |
|---|---:|---:|
| Survival | .9174767896493894 | .9174767896493894 |
| Expected writes | 8.587510024152317 | 7.889123279633160 |
| Expected gate executions | 0 | 7.587510024152318 |
| Installed gates | 0 | 1 |

Let S=.6983867445191578 be omitted writes and E=7.587510024152318 successful epochs. Selective update has smaller expected overhead exactly when

    c_w S > c_I + c_g E.

At `c_w=1, c_I=.10`, the critical invocation price is

    c_g < .07886470562996192.

For the ILLUSTRATIVE prices `c_g=.01, c_I=.10`, the expected overhead changes from8.58751002415 to8.06499837987:6.08455% lower, with exactly equal survival. If gate executions cost .10 instead, the same implementation is more expensive. Less writing is not automatically less total cost.

The budget is EXPECTED acquisition overhead, separate from the already pathwise-guarded actuator tokens. No deterministic per-run expenditure cap has been proved by this inequality.

## 5. Complete bounded synthesis, including simpler competitors

The grammar contains64 raw circuits:4 zero-gate outputs,10 rooted one-gate netlists and50 rooted two-gate netlists. Complete output profiles produce4+5+12=21 cost-indexed channel classes. Across16 whole maintenance programs, that is1024 raw program/netlist combinations represented by at most336 distinct channel/program pairs.

Only completed conditional output laws at equal cost are merged. No noisy PREFIX is merged by ideal truth. At gamma=0, further identical evaluated channels give288 programs; positive tested noise points retain336.

Exact synthesis at gamma=0,.005,.01,.05 minimizes the declared cost subject to average survival at least `V_refresh−epsilon`. All program comparisons use rational arithmetic. Example optima at gamma=.01:

| Allowed absolute survival loss | Best program (example prices) |
|---:|---|
| 0 | all refresh, no enable gate |
| .0001 (=.01 percentage point) | all refresh |
| .001 (=.1 percentage point) | one-NAND omission, vote/vote |
| .01 (=1 percentage point) | no renewed diagnosis, blind affordable-service program |

These are library-wide POINTWISE certificates, not a claim of continuous optimality over gamma, prices and tolerance. Browser sliders reprice the complete fixed-gamma=.01 library; the separate one-gate noise chart uses its polynomial certificate.

## 6. Gate faults: useless extra work and harmful omissions are different

For the one NAND, output probabilities in contexts `(r,x)=00,01,10,11` are

    (1−gamma,1−gamma,1−gamma,gamma).

A fault at11 causes an extra write on the safe-to-omit branch. That direction cannot reduce survival. A fault in the other three contexts omits a potentially relevant diagnosis and can reduce future viability.

If errors were restricted to extra writes at11, every rate in[0,1] would preserve all-horizon survival; the only effect would be reduced write savings. Implementing such directional protection is a DIFFERENT fault/architecture contract, not granted to the ordinary noisy NAND.

For the actual symmetric gate, the exact value is a polynomial of degree at most8 in gamma. The derivative of `V_refresh−V_selective(gamma)` has strictly positive Bernstein coefficients on[0,.1]. Loss is therefore strictly increasing on that entire interval.

With epsilon=.0001, the unique admissible-noise threshold is isolated by exact rational brackets of width <10^−20:

    gamma* ≈ .008252248170071292 (0.825224817% per invocation).

For gamma=.005, survival is .9174162820934071; the loss is .0060507556 percentage point, below the declared .01-point allowance. Example expected overhead is6.49666% lower than all refresh. For gamma=.01 the loss is .0121267565 point, exceeding that stricter allowance.

The certificate concerns the fair-prior mean, horizon8 and default physical rates. Ideal gamma=0 preservation is stronger: all horizons and all initial live measures. Do not conflate them.

## 7. Exact internal attribution

For Q0=ideal omission and B_j the kernel difference when only context j flips its enable decision,

    dV/dgamma at0 = sum_t sum_j mu Q0^t B_j Q0^(n−1−t) 1.

Eight-epoch contributions by readable selector context are:

| Context | Signed derivative contribution |
|---|---:|
| r=0,x=0 | −.0080746057325740 |
| r=0,x=1 | −.0029347076948005 |
| r=1,x=0 | −.0010671439914812 |
| r=1,x=1 | **0 exactly** |

The final write contributes zero to terminal survival. This makes the semantic distinction between fault directions explicit: faults that merely miss an opportunity to omit are not equivalent to faults that suppress information still needed.

Because fewer completed tasks also reduce writing, the report checks

    W_refresh−W_selective
      = omitted writes under selective policy
        + (completed tasks under refresh − completed tasks under selective).

At gamma=.01, .0004444371 of the write-count difference comes from fewer successful epochs. It is reported separately, not sold as useful efficiency.

## 8. A saved token would change the very condition that justified omission

An adversarial variant refunds one operational token after an omitted acquisition. The service-from3 branch now reaches balance3 rather than2. Maintenance is no longer forced off next epoch, so the stale diagnosis can affect the next decision.

For the same fixed policy, the eight-epoch value changes from .9174767896493894 to .9180194629817634. It improves in this fixture, but the important conclusion is that the **old equality certificate no longer applies**.

Extra resources have not been shown harmful under optimal choice. The falsified shortcut is transferring a certificate after changing the resource transition. Saving a resource can change which distinctions will matter next. A fully priced physical controller must be recompiled after that change.

## 9. Contribution, instrument and remaining scope

The result joins causal continuation irrelevance with a physically constructed write-enable, an exact whole-program cost frontier on a bounded grammar, a toleranced noise certificate and direction-specific failure attribution. It is a concrete adaptation and synthesis result enabled by known matrix, circuit and decision methods.

It does not optimize all circuits, diagnose all infrastructure, price actual energy, solve a pathwise acquisition budget or remove the original fatal task hazard. The final acquisition actuator and resource signal interface retain declared base idealizations. The nonlinear effect of refunding operational resources is explicitly exposed rather than hidden.

## 10. Primary antecedents

- Soleymani, Baras & Hirche, *Value of Information in Feedback Control: Quantification* (2022), DOI10.1109/TAC.2021.3113472, https://arxiv.org/abs/1812.07534 . Relevant: cost-benefit semantics for event-triggered information. It does not by itself supply this physical NAND implementation or all-horizon omission certificate.
- Soleymani, Baras & Hirche, *Value of Information in Feedback Control: Global Optimality* (2023), DOI10.1109/TAC.2022.3194125, https://ieeexplore.ieee.org/document/9842327/ . Relevant: rigorous joint triggering/control results for a different Gauss–Markov class.
- van Oosterom, Maillart & Kharoufeh, *Optimal maintenance policies for a safety-critical system and its deteriorating sensor* (2017), DOI10.1002/nav.21763, https://repub.eur.nl/pub/102727/ . Relevant: coordinated sensor/system maintenance under partial observation.

Primary abstracts were inspected; this is not an exhaustive priority audit. Validity, concrete contribution, priority and fertility remain separate.
