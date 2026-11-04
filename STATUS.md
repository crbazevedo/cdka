# CDKA — Research State

**2026-11-04 · v15 / T4.P–T3.L: realized correction, two-update signatures and paid maintenance. Active proof branches: R11/R14.** All prior physical kernels and ledgers remain unchanged; v14 is preserved at commit7fa14299961937a580f0de7c0af46511313e834e.

[Result](docs/results/T4P-realized-correction-interfaces.md) · [Strategy](docs/strategy/proof-engine-v15.md) · [Miniarticle](docs/articles/T4P.md) · [Lab](docs/lab/boundary_voting.html) · [Additive ledger](registry/v15-realized-correction-addendum.json).

## Executed results

1. The six-NAND majority voter has exact asymmetry f(011)-f(101)=2gamma(1-gamma)(1-2gamma)^2. Ideal function symmetry does not certify its faulty physical realization.
2. For the two declared register updates with hidden substrate health, the complete16-state process has an exact12-class physical quotient (Z,a,b+c). The abstract symmetric majority would allow8 classes (Z,a+b+c). Independent row and two-update oracles agree exactly; current joint bits alone do not determine future failures when Z is persistent.
3. Exact invariant response spaces have ranks10 and5 respectively in the fixed rational fixture. These are evaluator coordinates, not hardware-memory bits or a newly readable health input.
4. Explicit18-gate triplication+voter,10-gate shared-output voter, and4-gate original selector are compared in the SAME SERVICE-first terminal task. A paid one-bank maintenance attempt changes conditional voter/selector reliability and is not revealed to the policy. One resource token leaves both terminal actions affordable.
5. In the default fixture p=.01, degraded gamma=.02, restored gamma=.001, maintenance success=.8: bypass .809177960770; unmaintained triple .808854141237; voter-maintained triple .809277629247; maintained single .809328337152. Absolute differences are small; the structural comparison is exact within this portfolio.
6. Minimum service success to beat bypass is .490971934444 for the single selector and .611718916306 for the redundant voter. Affine endpoint certificates prove that direct selector maintenance dominates voter maintenance for the ENTIRE success interval[0,1], other parameters fixed.
7. Repair health must be retained as a common latent cause; replacing it by a mean independent gate-error rate changes the outcome. More installed copies do not remove the last-port limit.

## Scope and contribution

The portfolio and register-closure experiments share the actual voter but are not a jointly optimized recurrent agent. The result is an implementation-relative stochastic reduction and costed maintenance separation with complete witnesses. It is not universal optimality among all18-gate circuits. Existing PTM and Markov aggregation tools support the adaptation; correctness, contribution, priority and fertility remain separate assessments.

## Research memory

**47 approaches,40 rejected shortcuts**; R47 records this verified instrument. D38–D40 preserve failures of ideal-symmetry transfer, averaging hidden bank health, and unconditional preference for redundancy. Historical files remain immutable. R11/R14 only are active.

## Next gate

One small recurrent model must include selection of maintenance by a physically stored diagnostic and a fallible selector, with hidden mechanism health, shared components and the same resource ledger. Reuse the certified quotient rather than adding unrelated components. Require a necessity/sufficiency condition, or strict impossibility with a minimum realizable upgrade, before broadening the model.

## Verification

17 scientific Python tests plus one catalog test and seven JS tests. 192 exact quotient rows;384 two-update comparisons;2048 raw voter masks;2560 independent module/voter fault cases;128 complete conditional traces. Polynomial identity is coefficientwise; service dominance uses exact affine endpoints. No Monte Carlo inference.

Local Chromium desktop1440×1100 and mobile390×844: six portfolio rows, three panels, three exercised controls, two SVGs, no JS errors or horizontal overflow. These are offline file-byte checks; live publication is checked separately through GitHub Actions.

Reproduce: `python -m unittest discover -s tests -p 'test_boundary*.py' -v`; `python -m experiments.boundary_voting_sweep --write --check`; `node --test tests/boundary-voting-lab.test.mjs`.
