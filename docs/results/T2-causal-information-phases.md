# T2.D — Causally valid barrier-to-bits phase diagram

**Status:** a quantitatively verified finite two-context example using classical Freidlin–Wentzell theory and set cover. **Novelty not established.** It corrects an earlier invalid comparison that inadvertently varied the initial state across candidate interventions.

## Question

Can an explicit bistable stochastic system show a 0-bit → 1-bit → infeasible transition in the *information necessary to select a viable intervention*, while keeping the causal experiment well-defined?

## Fixed physical experiment

Physical SDE for a constant control tilt \(u\):
\[
dX_t=(X_t-X_t^3+u)dt+\sqrt{2\varepsilon}\,dW_t.
\]
Two contexts \(W\in\{L,R\}\), with **fixed** initial states \(x_L=-1.1\), \(x_R=+1.1\). Three physically admissible interventions \(A=\{-0.2,0,+0.2\}\), chosen at \(t=0\) and held for the entire horizon \(T=3\).

**Failure event (fixed across actions):** reaching \(x=0\) from the initial side by time \(T\). It is not redefined as the changing potential's own separatrix. The initial state and the event are *common across interventions within each context*, so this is a legitimate counterfactual comparison.

The strict small-noise event rate is
\[
J_T(w,u)=\inf_{\phi(0)=x_w,\ \exists t\le T:\phi(t)=0}
\frac14\int_0^t[\dot\phi+U'_u(\phi)]^2ds.
\]
In this scalar example, the minimum action to reach 0 decreases with the available time; it is therefore calculated by the endpoint action with \(\phi(T)=0\).

## Exact variational instrument, approximate numerical values

The scalar path problem has the conserved energy \(E=(\dot x^2-U'^2)/4\). All chosen intervals connect initial point and failure threshold across a stationary point of \(U_u\), so a finite-time monotone minimizer has \(E>0\).

For \(\ell=\min(x_w,0)\), \(r=\max(x_w,0)\), solve
\[
T=\int_\ell^r\frac{dx}{\sqrt{U'_u(x)^2+4E}}
\]
and compute
\[
J_T(w,u)=
\frac12\int_\ell^r\sqrt{U'_u(x)^2+4E}\,dx
+\frac{U_u(0)-U_u(x_w)}2-ET.
\]
This formula is valid for both traversal directions because the physical potential difference retains its signed endpoint order.

For \(T=3\), the computed rate matrix is:

| Context / control | −0.2 | 0 | +0.2 |
|---|---:|---:|---:|
| Left \(x_0=-1.1\) | 0.460201 | 0.269641 | 0.127259 |
| Right \(x_0=+1.1\) | 0.127259 | 0.269641 | 0.460201 |

Reflection symmetry \(x\mapsto-x,\ u\mapsto-u\) requires \(J_T(L,u)=J_T(R,-u)\), independently checked.

## Why the action ordering is not an arbitrary coincidence

For two controls \(u_1<u_2\) acting on the **same** initial state and driven by the same Brownian path, scalar SDE comparison gives \(X^{u_1}_t\le X^{u_2}_t\) pathwise, under the usual strong-solution assumptions. Hence left-to-right crossing probability is monotone increasing in u, so its small-noise rate cannot increase when the tilt increases. On the right, the ordering reverses.

The numerical values provide strict margins for the chosen three actions; the comparison principle explains their order.

## Exact information phases in the small-noise, strict-margin sense

Declare a control asymptotically acceptable if its failure probability is at most \(e^{-c/\varepsilon}\). For rates \(J_T(w,u)\ne c\), the low-noise acceptability indicator eventually agrees with \(\mathbf1\{J_T(w,u)>c\}\).

Let
\[
c_0=J_3(L,0)\approx0.269641,\qquad
c_1=J_3(L,-0.2)\approx0.460201.
\]

- For \(0<c<c_0\), the neutral action \(u=0\) is acceptable for both contexts. **Minimum decision code = 1 message = 0 fixed bits.**
- For \(c_0<c<c_1\), no action works for both, but opposite control signs work for opposite contexts. **Minimum = 2 messages = 1 fixed bit.**
- For \(c>c_1\), no available intervention meets the required exponent for either context. **Infeasible, not "more bits needed."**
- At \(c=c_0\) or \(c=c_1\), the limiting exponent does not determine safety: prefactors and finite-ε effects matter. No equality-case classification is claimed.

This is a fully specified causal dynamics → finite-time action → risk relation → set-cover calculation. It is a meaningful verified synthesis, **not yet an original CDKA theorem**.

## What we learned from the failed earlier attempt

Using the tilt-dependent minimum \(a(u)\) as the initial state for each candidate action invalidates an action comparison: changing the action simultaneously changes the counterfactual reference state. The original parameter scan remains a valid physical calculation *for separately equilibrated systems*, but not a controlled decision experiment.

**Protocol for all future CDKA action studies:** fix context, initial state/distribution, failure/viability definition, clock horizon and observation authority before varying the intervention. Otherwise apparent information phase transitions may result from changing the task.

## Next proof obligations

1. Investigate finite-ε effects and prefactors near \(c_0,c_1\); use reliable Fokker–Planck/backward Kolmogorov or first-passage solvers rather than naïve Monte Carlo of rare events.
2. Allow a noisy observation of L versus R and calculate decision rate–distortion, not just exact fixed bits.
3. Make available controls depend on endogenous actuator state \(Z_t\), sensory reliability, and a resource budget \(R_t\).
4. Prove a coupled viability-information bound exceeding a mere pointwise application of existing LDP + set-cover theory.

## Reproduce

\`cdka/variational.py\` function \`fixed_frame_action\`, and \`tests/test_variational.py\` class \`CausalFrameTests\`. The checks cover reflection symmetry, monotonic control effects, exact-cover phase classification, and numerical rate comparisons.
