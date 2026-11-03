# CDKA — Research State

**2026-11-03 · v13 / T4.N–T3.J: from a continuation signature to a costed physical update. Active branches: R11/R14.** Previous state and all v1–v12 artifacts remain preserved at commit 6cd99bb569b746bff6c354694387f15dfb17f50b.

[Reusable prompt](docs/methodology/prompt-fechamento-contextual.md) · [Methodology manual](docs/methodology/manual-fechamento-contextual.md) · [Proof Engine v13](docs/strategy/proof-engine-v13.md) · [Exact result](docs/results/T4N-noisy-physical-updates.md) · [Knowledge article](docs/articles/T4N.md) · [Interactive update lab](docs/lab/physical_update.html).

## Executed increment

1. **General combinatorial research method:** contract → continuations → appropriate quotient/aggregation/dominance → exact small traces → certificate → executable realization → refinement. The prompt distinguishes counting, probability, optimization, adversarial control and approximation instead of treating all problems as linear algebra. It preserves multiplicity, observability, costs, input/output complexity and fallback evidence.
2. **Real update between decisions:** the same v6 plant, restricted explicitly to SERVICE as the first action. The updater reads only a transported two-bit diagnosis and the new physical syndrome, executes a shared NAND network, and overwrites one bit used by the final HOLD/REFRESH interface. Health and the original diagnostic never enter runtime policy.
3. **Costed joint implementation:** exact gate libraries of capacity 0..4 provide 5,11,23,48,91 different Boolean functions. Prefix circuits are merged by available-function sets only under the ideal-gate contract. Each class retains a concrete netlist. The largest joint search is 64 encoders ×91 functions = 5824 programs.
4. **Certified noise/gate frontier:** two/three gates gain over the fixed command only for p<.01377800175004621 when final write is perfect; four gates do so until p<.10570305126989384. Between thresholds four gates are the smallest capacity with a strict improvement. Exact rational polynomial dominance covers the full p range and a common affine transformation covers every uniform output-write error q≤1/2.
5. **Task-relative one-bit realization:** at p=.01,q=0, baseline is .8091779607700227, best two/three gates .8092550445703148, best four gates .8094514713772433. These gains are small but the strict lower bound and attaining hardware witness are exact. This is not the unrestricted optimum over all first actions or arbitrary architectures.
6. **Contract-change falsifier:** a wire and two NAND inverters have the same ideal truth table, but internal independent gate-flip probability .1 gives error .18 in the latter. Noiseless functional equivalence cannot be reused for fault analysis without preserving signal dependencies.

## Research memory

**45 approaches and 34 rejected shortcuts** in the combined ledger. Historical files remain unchanged; the additive [v13 ledger](registry/v13-physical-update-addendum.json) adds R45 (costed continuation-update synthesis) as an instrument, and D34 (ideal circuit equivalence does not preserve internal fault behavior). R11/R14 remain the only active branches.

## Concluding the finite core

The program now contains a coherent finite chain: task-relative distinctions, causal/temporal cut obstructions, continuation preservation, exact generative closure, jointly coded physical memory, and one actual costed update circuit. Consolidate these as a precise claim/dependency map before expanding models.

The next narrow gates are (R11) task-sufficient noisy signal signatures when gates share faults, and (R14) jointly costed multioutput read/write/select circuits with upkeep. General recurrent self-maintenance and agency emergence are not declared completed. The successful finite case is an advancement and an executable reference, not a substitute for those obligations.

## Verification

14 scientific Python tests + one preservation/methodology test; six JavaScript tests. Evidence: 24 raw microstate cases, 728 gate/input truth checks, 1092 direct/polynomial evaluations, independent unquotiented netlist enumeration to three gates, 2814 exact interval dominance checks and a fault-contract counterexample. All mathematical values use Fractions; browser charts use the generated certificate.

The standalone lab was exercised in local Chromium desktop 1440×1100 and mobile 390×844: two SVGs, eight trace rows, three controls, no JS errors or horizontal document overflow. These are offline generated-byte checks, not independent live public-site browsing. CI and Pages are verified separately after the commit.

Reproduce: `python -m unittest discover -s tests -p 'test_physical_update*.py' -v`; `python -m experiments.physical_update_sweep --write --check`; `node --test tests/physical-update-lab.test.mjs`.
