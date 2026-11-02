# CDKA — Research State

**2026-11-02 · Increment v8, T4.I / T3.H. Active branches: R11/R14 only.** Exact scoped derivations with classical tools; no general agency theorem or originality claim. The prior [v7 snapshot is immutable in git](https://github.com/crbazevedo/cdka/blob/f9371cf41227eb58a869b9fbc16be9153ca31118/STATUS.md).

[Proof and physical contract](docs/results/T4I-diagnosis-through-repair.md) · [Proof Engine v8](docs/strategy/proof-engine-v8.md) · [Miniarticle](docs/articles/T4I.md) · [Interactive lab](docs/lab/diagnostic_transport.html) · [Catalog evidence addendum](registry/v8-transport-addendum.json).

## Executed in this increment

- A diagnosis traverses compulsory physical repairs; register erasure, bit flips, corrector-health drift and selector wear are explicit. Hidden selector health can be serviced imperfectly. The runtime table observes M only, not H/S or a designer posterior.
- Exact terminal Bayes margin formula works with arbitrary joint hidden health and unnormalized survival mass. The scalar closed form additionally requires the declared independent symmetric channels.
- For the default v7 physical payoff, a flip-prone selector introduces a task-weighted negative term even when the diagnostic contains information. Flagged erasure and command corruption are not interchangeable.
- At equal added cost, selector service outperforms perfect erasure protection in the verified fixture: expected success .8880487061076224 versus .88452784853498. With both upgrades it is .898773394576916. Baseline bypass remains .883319376.
- A finite delay can eliminate actionable value while stored information remains strictly positive. With stable H, perfect initial diagnosis, erasure .2 per repair and command error .05, the paid program stops improving survival at the eighth repair while it still stores .16777216 bit.
- A single task-optimal binary encoding is attained by grouping diagnostic signals according to the sign of their probability-weighted intervention advantage, under symmetric transport and outcome-independent costs. A two-task counterexample shows this does not imply recursive sufficiency.
- Same marginal H/S distributions with different dependence yield distinct success values (.866412885772 vs .8986857151752); averaging selector error independently is not generally valid.

## Scope and remaining gate

This is a **single terminal decision after n repairs**, with precommitted protection/service programs. It is not a solved recurrent controller that diagnoses and maintains its own selectors. The fixed-command bypass, controller library, symptom k=0, resource accounting and fault semantics are explicit assumptions. The fail-silent alternative is a changed architecture, not free safety hardware.

Next joint proof gate: concatenate two decision/maintenance tasks and identify a physically readable interface that preserves future action choice, not only today's positive margin. Prove a sufficient condition or a smallest strict gap; compare with existing finite-state POMDP synthesis before adding components.

## Research memory

The canonical v7 ledger (37 branches, 18 rejected shortcuts) is unchanged. The immutable [v8 addendum](registry/v8-transport-addendum.json) adds two refutations and evidence for R11/R14, with reactivation triggers and existing fallback IDs. Combined view: **37 branches, 20 rejected shortcuts**, only R11/R14 active. Tests verify the v7 base blob hash, referential integrity and the combined counts.

## Verification

18 new scientific Python tests plus one catalog test; 486 exact independent channel/driver evaluations, 80 correlated mass fixtures and 125 binary-encoder cases. Eight JS tests compare browser formulas with Fraction-derived fixtures. Offline Chromium rendered four SVGs and exercised nine controls/reset at 1440×1100 and 390×844, without JS exceptions or horizontal overflow. These checks use generated local bytes, not live public-site navigation. GitHub CI/Pages status is checked separately.

Source: `cdka/diagnostic_transport.py`; tests: `tests/test_diagnostic_transport.py`, `tests/test_transport_catalog.py`, `tests/transport.test.mjs`; reproducible certificates: `python -m experiments.diagnostic_transport_sweep`.

All earlier proofs, source and laboratories remain intact. The main catalog remains at [registry/research-options.md](registry/research-options.md); the previous [v7 strategy](docs/strategy/proof-engine-v7.md) records its state before this evidence update.
