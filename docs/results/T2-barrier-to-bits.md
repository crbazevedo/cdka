# T2 — Large-deviation action barriers to decision-code size

**Status:** candidate derived corollary; **not** a proven novel CDKA theorem.

Let W and A be finite. For each fixed context w, candidate action a and noise ε>0, let
\[
p_\varepsilon(w,a)=P_\varepsilon(\text{viability failure before }T\mid w,\operatorname{do}(a))
\]
and suppose the small-noise exponent `J_T(w,a)=lim_{ε→0}[-ε log p_ε(w,a)]` exists (in [0,+∞]). Take a risk threshold `α_ε=exp(-c/ε)`, c>0. Declare an action safe exactly when `p_ε(w,a)≤α_ε`.

**Elementary asymptotic lemma.** For any fixed (w,a) with J_T(w,a)>c, the action is safe for all sufficiently small ε. If J_T(w,a)<c, it is unsafe for all sufficiently small ε. At J_T=c the exponent alone does **not** determine safety. Because W×A is finite, if no equality occurs, one common ε₀ suffices for all pairs.

Therefore, away from all boundary equalities, the finite action-compatibility relation stabilizes as ε→0 to
\[
R_c(w,a)=1\{J_T(w,a)>c\}.
\]
By B1, minimum zero-error deterministic code cardinality eventually equals the minimum action cover of this limiting relation, **provided each world remains feasible**; otherwise the instance is infeasible.

**Proof outline:** the definition of the limit gives `-ε log p_ε` above/below c with a uniform positive margin for small ε; exponentiating reverses signs. Finite W×A permits a shared noise threshold. Apply B1 to the stabilized relation. QED.

**What this does not say:** finite-ε probability is always captured by an asymptotic exponent; risk thresholds not exponentially scaled obey the same result; or the bare composition of LDP+set cover is mathematically new. A rate J based on a quasipotential needs a properly specified stochastic model and event.

**Potential research extension:** make action authority, observation quality, available memory and the rate functional depend on endogenously evolving organization Z and resources R. Ask for a *joint* bound and counterexamples against separable baseline inequalities, rather than just reapplying B1 to newly tabulated actions.
