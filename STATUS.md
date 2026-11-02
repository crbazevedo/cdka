# CDKA — Research State

**Current increment:** Proof Engine v6, T4.G. **Active gate:** physically readable compositional contracts; next hidden-health diagnostics and jointly costed implementation. **Originality:** no general original CDKA theorem established. Scoped proofs, classical instruments and new program obligations remain distinct.

[Strategy and ordered gates](docs/strategy/proof-engine-v6.md) · [32-option catalog](registry/research-options.md) · [machine-readable ledger](registry/research-options.json) · [T4.G proof](docs/results/T4G-compositional-contracts.md) · [miniarticle](docs/articles/T4G.md) · [interactive lab](docs/lab/composition.html) · [verification](docs/experiments/E-composition-v6.md).

The previous STATUS is preserved byte-for-byte at [status-before-v6](docs/corpus/status-before-proof-engine-v6.md); its original root-relative links remain usable in [the immutable pre-v6 root](https://github.com/crbazevedo/cdka/blob/c4a50682d2d45a73b0b6b1b754142a3247447c8a/STATUS.md). Previous notebooks, proofs and laboratories are retained.

## Research memory is now explicit

- 32 options have IDs, status, hypothesis, reactivation trigger, minimal test, instruments, acceptance gate, fallback IDs and provenance. The catalog is not an exhaustive literature survey.
- 14 misleading simplifications are retained as rejected claims with reasons and alternate routes; they must not be resurrected silently.
- At most two branches are active: **R11 hidden health/paid diagnostics** and **R14 coupled implementation costs**. JSON validation tests enforce IDs, fallback links, required fields, active limit and parity between source and browser copy.
- Dead-end handling: preserve the failed causal contract, classify the failure, follow a named fallback, rerun positive/negative controls, and separate a known theorem from a new claim. After two scoped models without a new implication, freeze feature expansion and audit prior art.

## Executed results

1. **Fallible upkeep with a changing world.** Three-cell memory, drifting hidden W, fallible sensing, correction, writing, actuation and service. Health degrades and is repairable; finite resources arrive only after success. Readable health, resource ledger and clock remain explicitly trusted interfaces.
2. **Exact readable quotient.** Under the declared cell symmetries and fatal-command-error support, 80 live physical states reduce to 20 readable states (disagreement, health, resource). Independent raw-event and binomial-composition kernels match on all 240 affordable rows; nine further rational fixtures check 1,008 rows. This is known controlled lumpability, not a general scaling theorem.
3. **Freshness differs from integrity.** In the scoped example with world drift .2 and fresh sensor error .05, copying/correcting the old bit gives .8 success, while new sensing gives .95. A degraded corrector can harm an already-correct register.
4. **Real adversarial pivot.** Heterogeneous cell upset probabilities (.30,.01,.01) break count-only aggregation. Two same-count physical states differ by TV=513619/2000000. Refinement or a quantified approximation is required; removing health also breaks sufficiency.
5. **Finite-horizon compositional error.** Under uniform conditional component contracts and the same realizable policy class, event discrepancy is bounded by Delta_n=1-[product_i(1-delta_i)]^n. Optimal-value difference <=Delta_n; deployment regret <=2Delta_n. No infinite-support conclusion follows.
6. **Calibration/sensitivity.** A .02 increase in both sensor errors yields composed one-step delta=.019490376808; at n=10 bound=.178668264306 and actual maximum optimum discrepancy=.048352214308. Exact frozen-policy derivatives are checked by independent differences; argmax switches are not differentiated blindly.
7. **Maintenance is horizon-sensitive.** For an initially unanimous/degraded register with four resource tokens, hold is one-step optimal; service is optimal in the tested longer horizons. This is a model result, not an empirical universal rule.

## Ordered program

G0 ledger/ontology: executed. G1 fallible corrector and dynamic world: executed in declared scope. G2 exact readable decomposition: executed with falsifier. G3 approximate transfer: executed with finite-horizon limits. G4 hidden health and actual joint selector cost: next R11/R14. G5 structurally changing observation/policy families: open. G6 finite-noise physical calibration: parked until the structural certificate is worth calibrating. G7 novelty and independent proof-package audit: open.

The point is not to accumulate more toy models. A branch must deliver a discriminating implication, a counterexample or an instrument that reduces the next obligation.

## Verification

19 new Python tests (15 mathematical/model checks and 4 ledger checks); 6 JavaScript kernel tests; eight exact rational fixtures mirrored in the browser; 1,248 micro-to-macro row comparisons across declared fixtures; a full micro Bellman check; policy transfer and local derivative checks. Local Chromium tests exercised eight controls and catalog filters at 1440x1050 and 390x844 without JavaScript errors or horizontal overflow. These were generated-byte checks, not live public-site browser navigation. CI and Pages status are reported separately after commit.

Code: `cdka/composition.py`; `tests/test_composition.py`; `tests/test_research_options.py`; `experiments/composition_sweep.py`; `tests/composition.test.mjs`. The interactive lab includes the searchable 32-branch research ledger.

## Prior-art firewall

Exact controlled aggregation, maximal coupling, Bellman synthesis and compositional abstractions have established antecedents. Checked primary sources include Buchholz; Lavaei/Soudjani/Zamani; Junges et al.; and Tirinzoni et al. The current reduction is a verified application, not a new general theory. Originality would require an additional physically constrained class or consequential result that the closest known theorem does not already supply.

[Main hypothesis register](registry/hypotheses.md) · [v6 result register](registry/v6-results.md) · [prior v5 strategy](docs/strategy/proof-engine-v5.md). The longer program remains tracked in issue #9.
