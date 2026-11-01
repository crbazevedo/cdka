# Research method / evidence protocol

1. **Specify ontology:** state, system boundary, exogenous forcing, organization, sensors, actuators, repair resources, horizon and failure condition.
2. **Fix quantifiers:** distinguish "there exists an omniscient policy" from "there exists an implementable policy with this observation/memory budget".
3. **Write the claim:** proposition, proof assumptions, proof/counterexample and known antecedents; avoid suggestive words replacing definitions.
4. **Run independent checks:** mathematical proof first; exhaustive finite-state oracle second; stochastic computations only when justified by a model and uncertainty estimates.
5. **Adversarial tests:** no-actuator randomness, open-loop universal action, fake predictive memory, passive synchronized oscillator, replayed externally generated action, depletion and failed repair.
6. **Record novelty:** known result, corollary, candidate extension, original-verified theorem, or falsified; no leap from tests to universal explanatory theory.
7. **Preserve provenance:** archive historical notes unchanged and track changes as new docs/commits/issues; make explicit where earlier informal wording was tightened.

Prioritized technical tools: finite relations and combinatorics; information inequalities and decision theory; POMDP/viability DP; causal interventions; dynamical stability; then Freidlin-Wentzell/Girsanov; replicator dynamics only after a concrete proof obligation requires it.

**Practical constraint:** the first laboratory intentionally needs no deep learning or heavy scientific stack. A minimal exact oracle is more valuable than a complex simulation that can only reproduce the designer's objectives.
