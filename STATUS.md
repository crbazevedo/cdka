# CDKA — Research State

**2026-11-02 · v12 / T4.M: generate continuation distinctions rather than enumerate paths. Active proof branches: R11/R14.** Previous state is preserved at commit 644945674871f7b0d6dcf7de1f1693d5c237c155. The v6 physical kernel and historical ledgers are unchanged.

[Result and proof](docs/results/T4M-context-closed-semantics.md) · [Strategy](docs/strategy/proof-engine-v12.md) · [Miniarticle](docs/articles/T4M.md) · [Interactive lab](docs/lab/semantic_closure.html) · [Research-memory addendum](registry/v12-semantic-addendum.json).

## Executed contribution

1. Exact constructive continuation closure: retain independent operator-word observables, derive Q_a B=B C_a, and return a real separating continuation when two signatures differ. This is a contract-aware CDKA instrument using established linear/automata ideas.
2. Unchanged 80-state physical model: four commands yield rank 20, 20 state-signature classes and 81 candidate vector evaluations, with rank growth 1→5→16→20. HOLD-only yields rank four and five evaluations. Closure certifies all subsequent command lengths, not just a sampled horizon.
3. Independent stable partition refinement recovers the 20-state physical quotient starting from only readable (syndrome,balance). Hidden health remains an evaluator variable, never an extra runtime observation.
4. Constructive nuisance-factor theorem: for a core-independent transition marginal and unobserved row-stochastic auxiliary channel, K_a L=L Q_a holds before product-state enumeration. Explicit 2–128-state tests retain rank two and five candidate evaluations; larger factorized counts are derived, not claimed runtime benchmarks.
5. Four-state compositional witness: identical outcomes for each isolated command, but PREPARE→CHECK separates with survival 1/0; the reverse order does not. Closure preserves noncommutative compositions.
6. Interface-change witness: identical fixed-action laws become distinguishable by a real sensor; u=Z yields success 1 versus 1/2. Observation masks grow the task space from rank two to four.
7. Distinguish three objects: a linear continuation signature, a valid stochastic state quotient, and a physically implementable memory. Rank two can separate 17 states; trace-equal states need not have a Markov quotient; an N-step failure chain can require rank N.
8. The v11 equal-endpoint plans now receive an automatically generated next-command witness; fixed HOLD already separates their future survival by .002062718070500702, and REFRESH reproduces the earlier .026369654670462817 difference.

## Research memory and contribution posture

The combined ledger has **44 approaches and 33 rejected shortcuts**. R44 is a supporting instrument for context-closed generative semantics; only R11/R14 are active. D30–D33 record failures of isolated-command equivalence, blind-to-feedback transfer, automatic Markov lumping and identification of algebraic rank with physical bits/general tractability. All historical records stay byte-identical.

The contribution is the constructive adaptation, exact fixed-plant reductions, operational contract and witness/falsification pipeline. Established algebra is not a reason to dismiss useful scientific innovation; priority of a broader jointly costed physical-interface theorem remains an explicit audit target.

## Next gates

**R11:** realize a task-relative approximate signature in a noisy physical update library without supplying an evaluator posterior or free exact scalar.

**R14:** restrict the jointly realizable read/write/command maps and price a minimal upgrade that preserves a new task, observation or authority. The next certificate must address physical implementation, not only evaluator dimension.

**Shared:** treat expanded oversight interfaces as operator additions; test whether their image lies in the existing signature space, and produce a separating trace/refinement obligation if not.

## Verification and artifacts

17 scientific Python tests plus one catalog-integrity test; seven JS tests. Exact checks: 1,488 small-system words, 85 original-plant command words, 64 existing two-step plans, 80 plant intertwining column identities, five multiplicity fixtures and 12 full-rank chain sizes. Python uses Fractions; independent oracles and explicit falsifiers are preserved.

Offline Chromium desktop 1440×1100 and mobile 390×844 render three SVGs, three panels and exercise four controls without JS exceptions or document overflow. These are generated-local-byte tests, not live-site browser verification. GitHub CI and Pages are checked separately after committing.

Reproduce: `python -m unittest discover -s tests -p 'test_semantic*.py' -v`; `python -m experiments.semantic_sweep --write`; `python -m experiments.semantic_sweep --check`; `node --test tests/semantic-lab.test.mjs`.
