# CDKA — Research State

**2026-11-05 · v16 / T4.Q–T3.M: a diagnostic-controlled recurrent maintenance loop. Active proof branches R11/R14.** All prior sources and ledgers remain unchanged; v15 is preserved at commit2eb1da7b635da2165e3b767440371a69583df3d0.

[Learning compass](docs/strategy/learning-compass-v16.md) · [Strategy](docs/strategy/proof-engine-v16.md) · [Result/proof](docs/results/T4Q-recurrent-maintenance-loop.md) · [Miniarticle](docs/articles/T4Q.md) · [Decision record](docs/synthesis/decision-record-v16.md) · [Lab](docs/lab/recurrent_maintenance.html) · [Research-memory addendum](registry/v16-recurrent-learning-addendum.json).

## Executed contribution

1. One recurrent64-state process integrates stored noisy health diagnosis, maintenance chosen by the same fallible six-NAND bank that executes work, hidden restoration, resource harvest and report renewal. It is a NEW task, not an undeclared change to v15's terminal benchmark.
2. Initialization and common operation/diagnostic acquisition cost1 each; maintenance costs2 extra and must be funded before work. Correct work returns2, never after failure. Guard/routing remain explicit trusted base interfaces.
3.16 complete stationary routing programs are enumerated, with4 diagnosis-blind programs as a restricted baseline. The circuit reads only actual report cells and balance, not hidden health, designer posterior or a free clock-dependent policy.
4. An exact stochastic realization K_pi=A_pi E and M_pi=E A_pi yields E K_pi=M_pi E. The12-phase evaluator preserves health at report-writing time, current health and balance. It does not expose those variables to runtime or assert a deterministic state quotient.
5. Eight-cycle default survival: diagnostic .9174767896493894; best blind .9115317652171799; never maintain .7325971487141393. Expected service attempts1.2734000271 versus3.8507390345. Both initial health contexts improve over always-maintain, but the .915 separating target concerns the mean, not the degraded-context guarantee.
6. Procedure risk explains why repairing healthy hardware can hurt. Complete branch traces preserve health, physical report, selection faults and resources. An uninformative report ablation selects always-maintain; internal hardware can nevertheless create an action-health dependence without information in the report.
7. Uniform task success ceiling q*=.9952702938313536<1 implies V_n≤(q*)^n→0. Resource-recurrent operation is not immortal operation or full autonomous maintenance of all infrastructure.

## Lessons converted into policy

`learning-compass-v16.md` records twelve decision rules: preserve causality and correlations, price every step, separate average and contextual guarantees, retain future competence, distinguish evaluator rank from hardware memory, compare simpler baselines and separate correctness/contribution/priority/fertility. Expansion requires a new separation, certificate or relevant adaptation rather than merely more components.

## Research memory

**48 approaches,42 rejected shortcuts.** R48 records regenerative recurrent maintenance. D41 rejects merging current health with report-time health; D42 rejects inferring hidden-state independence of actions from an uninformative input register. Historical ledgers are not edited. Only R11/R14 remain active.

## Next decision gate

Compare fresh diagnosis and memory retention at equal declared cost. Test whether the common emission E remains valid; if not, identify the smallest lost dependence. R14 must separately account for alternate acquisition/routing libraries and their reliability before claiming a cheaper whole architecture.

The contribution is an executable recurrent coupling, stochastic realization certificate and scoped physical-policy separation. Existing FSC/POMDP and Markov tools enable these advances; broader priority remains an exact-result audit, not a reason to dismiss the adaptation.

## Verification

17 scientific Python tests +1 catalog test,7 JS tests;192 independent raw rows,192 policy/phase identities,2048 raw task fault/sensor cases,116 complete conditional trace rows. Exact Fraction arithmetic for decisive values. Offline Chromium desktop/mobile:7 controls,3 panels,2 SVGs, no JS error or overflow. Canonical CI and live deployment are checked separately.

Reproduce: `python -m unittest discover -s tests -p 'test_recurrent*.py' -v`; `python -m experiments.recurrent_sweep --write --check`; `node --test tests/recurrent-lab.test.mjs`.
