# Attempt 01 is NOT a successful official comparison

Workflow42437031478 returned green because `python ... | tee ...` lacked pipefail. The Python harness correctly raised after API incompatibilities, but the shell discarded that exit. Three calls were incompatible with installed Stormpy2.0.0: result.at, top-level perform_bisimulation and create_filter_initial_states_symbolic.

The full invalid logs remain immutable at commit906c627b6405620f7328950f675f13c4ee37c53f under research/v21/evidence/official. Those records are not accepted as solver comparisons and no speedup claim is based on them. The mathematical unit tests were separate, but a green workflow is insufficient scientific evidence.

Correction: current public API uses result[index], stormpy.transformations.perform_bisimulation(...,bisimulation_type=...) and stormpy.filter_initial_states(result,model). Added an API/value smoke gate, explicit bash pipefail to every piped run, and full output validation. Only a subsequent error-free run can establish official measurements. Raw failure evidence is retained rather than erased from provenance.
