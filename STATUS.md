# CDKA — v18 execution snapshot

**2026-11-05 · T4.S/T3.O: continuation-certified selective acquisition, now physically realized and priced. R11/R14 remain the only active branches.** Historical sources are not changed.

[Proof](docs/results/T4S-priced-selective-acquisition.md) · [Learning/direction](docs/strategy/direction-v18.md) · [Knowledge article](docs/articles/T4S.md) · [Lab](docs/lab/selective_acquisition.html) · [Additive catalog](registry/v18-selective-acquisition-addendum.json).

## Provenance and execution

Canonical v17 at a32b9a4 contains renewal/retention. The previously delivered local v17 additionally proved write elision. V18 integrates these sources without replacing either and uses the unchanged v16 core (blob0a01bbf40f78f314a56285c15822e7ac06c9848b).

1. One NAND on (executed service, pre-balance3) implements the omission. Exact D1=0,DQ=0 proof preserves all finite-horizon survival, for every initial live measure and all16 maintenance programs.
2.64 raw enable netlists (0–2 gates),21 cost-indexed channels,16 whole maintenance programs:1024 physical combinations, at most336 distinct exact program evaluations per noise point. False independence in noisy partial circuits is not used.
3. Installation, invocation and write counts are jointly priced in a SEPARATE expected acquisition-overhead ledger. The operational token budget remains unchanged. At illustrative costs(1 per write,.01 per gate execution,.10 per gate installed), ideal elision costs8.064998 versus8.587510,6.08455% lower at identical survival.
4. For the one actual noisy NAND, a rational degree-eight polynomial and positive derivative Bernstein coefficients on[0,.1] certify a unique noise threshold .008252248170071292 for mean eight-cycle loss tolerance .0001. At gamma=.005 the loss is .00605076 percentage point and example overhead6.49666% lower.
5. Context-wise fault attribution: accidental extra writes on the safe branch have exactly zero survival derivative; false omissions in other contexts are harmful. Counts distinguish writes omitted from tasks lost to failures.
6. Refund counterexample: returning a saved token changes the post-service state and future decision. The old elision equality no longer applies. In the chosen fixed policy the value improves, but requires a new proof.

## Research memory and next gate

50 approaches,48 rejected shortcuts after explicit import of local-v17 D45 and addition of D46–D48. R50 is an executed instrument; R11/R14 remain active. The next gate is one unified pathwise acquisition/actuation budget and a physically shared selector, not another unrelated component.

The finite-core manuscript should organize a single result family around interface sufficiency, physical implementation, all-horizon certificates and tolerance/cost frontiers. Originality is assessed at exact-result level; classical event-triggered/POMDP tools do not negate concrete synthesis contributions.

## Verification scope

16 scientific Python tests +1 catalog test,7 JavaScript tests. 1024 v16 fresh-row equalities,256 independent raw gate/cell rows,1536 annihilation-row identities across all16 maintenance programs, exact whole-library comparisons at four declared noise points and rational threshold brackets. No Monte Carlo inference. Expected overhead is not a deterministic per-run energy budget.

Local Chromium desktop/mobile: three panels, two SVGs, five exercised controls, no JS errors or document overflow. This is local-byte QA. Remote CI and Pages status are separate records and are not presumed by this document.

Run `python -m unittest discover -s tests -p 'test_selective*.py' -v`; `python -m experiments.selective_acquisition_sweep --write --check`; `node --test tests/selective-acquisition.test.mjs`.
