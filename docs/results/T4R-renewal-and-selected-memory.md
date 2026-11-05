# T4.R / T3.N — Retaining the bits does not retain the diagnostic interface

**2026-11-05 · CDKA v17.** Contribution: a same-task, same-price renewal/retention comparison; an exact failure certificate for the previous regenerative representation; a valid physical quotient; complete stationary-library synthesis and temporal attribution. These are implemented adaptations of finite-controller, conditional-probability and stochastic-aggregation tools. Priority is assessed at the precise contribution, separately from correctness and fertility.

## 1. Frozen process, new acquisition grammar

Use the original v16 six-NAND bank, rates, hidden health, three stored bits, four balance levels, maintenance, fatal task criterion and success-only replenishment. The source `cdka/recurrent_maintenance.py` has git blob `0a01bbf40f78f314a56285c15822e7ac06c9848b` and is unchanged.

The bank sees only actual report cells and balance. Hidden health is not provided. A cycle costs one common operating/memory-service token before work; service costs two more and must be affordable. Correct work replenishes two, capacity four. Initialization is paid. Maintenance outcome remains hidden. Guard/routing/common acquisition primitives retain explicit idealizations.

A preinstalled two-row table chooses from the **executed service command**, not hidden restoration success:

| Table | No service | Service |
|---|---|---|
| retain | keep | keep |
| renew | new diagnosis | new diagnosis |
| after_service | keep | new diagnosis |
| after_skip | new diagnosis | keep |

Retention is ideal: no bit corruption or wear. Renewal uses the same noisy v16 sensor, about post-service health, before the same end-cycle degradation. Both occupy the same paid memory-service bundle. This is a **matched-price comparison**, not an energy-optimality claim. Unequal prices require another synthesis. Sixteen routing programs cross four acquisition tables: 64 stationary whole programs. No additional runtime clock or posterior is supplied.

## 2. Fixed-controller and reoptimized results

Eight-cycle survival, uniform initial health:

| Memory rule | Same vote/vote routing | Best routing for that rule |
|---|---:|---:|
| retain | .8958752016508781 | .9115317652171799 |
| renew | **.9174767896493894** | **.9174767896493894** |
| after_service | .8874864374106240 | .9115512983110162 |
| after_skip | .9164918233322648 | .9164918233322648 |

The best of all64 is `vote/vote|renew`. Reoptimization under retention selects a program whose reachable behavior is effectively diagnosis-blind. This is exact within the declared library and fixture, not a universal information ordering.

For fixed vote/vote, renewal improves over retention by .021601587998511283 (2.1601588 percentage points). Refresh after skipped service beats refresh after service by .029005385921640647 (2.9005386 points). The reoptimized comparison is also reported to avoid attributing a poorly adapted policy entirely to a memory primitive.

## 3. Mechanism: observation cannot be restricted only to its own trigger

Under after_service, a stored 'healthy' report tends to select no service. If the bank later degrades, that report stays until service occurs. A degraded physical bank still triggers service from000 with probability .110414194688 due to decision faults; this is not a refreshed diagnosis.

At epoch8 the unconditional masses of being alive, degraded, and holding a majority-'healthy' report are .1879564485072842 (after_service), .03759468027021188 (after_skip), .04377678063366565 (renew), and .10449125682297541 (retain). These are evaluator trace events, not extra runtime signals. No survivor normalization occurs. Renewal after skipped service can detect the change needed to justify later maintenance.

## 4. Fresh-memory realization does not transfer to retention

The v16 fresh process factors as K=A E and M=E A, so

    E K=M E;     (lambda E) K^n=(lambda M^n)E.

E samples reports conditioned on report-time health, current health and balance. It is a12-phase stochastic evaluator, not a runtime health observation or a deterministic state quotient.

Under retention, decisions depend on old bits and alter health, resources and survival. The retained law after those events need not belong to E's family. Adding a source-health label alone does not fix it: selection changes the law within that label.

### Exact separating witness

Start with healthy bank, its noisy report and balance3. Under vote/vote with retention, compare live healthy no-service endpoints with balance4 and words011 and101. The source sensor gives equal word masses; the actual selector does not choose no-service equally.

With diagnostic error eta, healthy gate error gamma, healthy task success q_H and degradation d:

    mu'(H,011,4)-mu'(H,101,4)
      = -eta^2(1-eta) q_H (1-d)
        · 2gamma(1-gamma)(1-2gamma)^2.

Every mixture of the original iid sensor emissions about either source-health value is exchangeable in all three positions and assigns these words equal mass. The nonzero difference excludes **every such mixture**, even with freely chosen weights conditional on final health/balance. Fresh renewal yields zero difference.

This holds with d=0: the bank need not change its health for action/resource selection to invalidate the sensor-emission family. Bits did not decay.

### A separate support witness without selector error

Set healthy gate error and degradation to zero, with diagnostic error strictly between0 and1/2. The ideal majority selector reaches balance4 only with at most one 'degraded' bit. Each original source-health emission has positive mass on all eight words. No nonzero mixture can produce the selected support. Thus the closure failure is not merely the asymmetric topology of a faulty voter.

## 5. A valid physical reduction for the extended grammar

Full state (Z,m0,m1,m2,b) has64 live possibilities. The actual voter is symmetric under swapping its last two positions. The signature

    (Z,m0,m1+m2,b)

has48 states. Retention and fresh iid acquisition respect this residual symmetry. Acquisition sees the executed command only, so resource and health transitions also preserve it. Therefore

    K_program L=L Kbar_program

for all64 programs. An independent binomial construction of fresh count laws and deterministic retention agrees with all4096 physical rows. This proves correctness under all repeated compositions allowed by the grammar.

These are sufficient evaluator states, not a minimal-dimensionality proof or48 physical memory states granted to the controller. Z remains hidden.

## 6. Locate each update's contribution

For the same initial law and two fixed program kernels L,R:

    mu L^n 1-mu R^n 1
      = sum[t=0..n-1] mu R^t (L-R) L^(n-1-t) 1.

This telescoping identity provides signed expected contributions, not individual counterfactual rescues. Renewal versus retention yields, in percentage points over eight cycles:

    .1110570, .2783103, .2575742, .4160253,
    .3422665, .4575167, .2974088, 0.

The exact sum is2.1601587998511283 points. The final update has zero value because no later task uses it. All four acquisition rules have identical one-cycle survival. This checks timing and prevents rewarding information merely for being present.

## 7. Generalizations and scope

Action/selection events reweight retained information by their likelihood. Invariant emission families give sufficient stochastic realizations, and renewal can establish such a family. Neither fact makes renewal universally better: new prices, initial accuracy, sensing dynamics or tasks can change the ordering.

The new result is a concrete physical failure of a prior realization, a certified replacement quotient, a64-program stationary optimum and a temporal mechanism. It is not general history-dependent POMDP optimality. Every task retains q_H<1, so all programs remain bounded by q_H^n; operational recurrence is not infinite survival.

## 8. Verification and antecedents

20 scientific Python tests plus a catalog-integrity test; six JavaScript tests. Exact4096 quotient rows;1024 old-kernel comparisons;64 independently enumerated raw rows; backward/forward checks for all64 programs; repeated-cycle comparisons; telescoping identities and static/noiseless support controls. V16 source is byte-verified. Browser charts use generated floating-point kernels; they do not establish optimization by sampling.

Predecessors: Junges et al.,2018, finite-state controllers (https://proceedings.mlr.press/r16/junges18a.html); van Oosterom et al.,2017, joint maintenance of system and sensor (https://doi.org/10.1002/nav.21763); Kolchinsky & Wolpert,2018, causal viability-related semantic information (https://arxiv.org/abs/1806.08053). The matched acquisition grammar, physical selection witness and recurrent implementation analysis are the contribution here; the underlying conditioning and Markov tools are established instruments.

Run: `python -m unittest discover -s tests -p 'test_memory_renewal*.py' -v`; `python -m experiments.memory_renewal_sweep --write --check`; `node --test tests/renewal-lab.test.mjs`.
