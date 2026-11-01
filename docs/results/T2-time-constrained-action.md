# T2.A — Time-constrained action is not the quasipotential

**Status:** classical variational identities, an independently checked 1D derivation; **not a novel theorem**. Date: 2026-11-01.

## The conceptual problem

A quasipotential barrier is an *unconstrained-time* asymptotic cost, not automatically the large-deviation cost to cross a separatrix within a prescribed deadline. CDKA's safety problem is explicitly temporal: sensing, decision, action and repair must occur before irreversible loss. Confusing the two actions could yield wrong required-memory thresholds.

## Physical and noise convention

Consider the one-dimensional gradient diffusion
\[
dX_t=-U'(X_t)\,dt+\sqrt{2\varepsilon}\,dW_t,
\qquad
U_u(x)=x^4/4-x^2/2-ux.
\]
Assume \(|u|<u_c=2/(3\sqrt3)\), so there are three simple equilibria \(a(u)<s(u)<b(u)\): left well, saddle and right well. Initially \(X_0=a\). In the Freidlin–Wentzell scaling with this noise convention,
\[
I_T[\phi]=\frac14\int_0^T(\dot\phi+U'(\phi))^2dt.
\]
For an endpoint event, define \(J_T=\inf_{\phi(0)=a,\phi(T)=s}I_T[\phi]\). The same optimal action governs first-hitting-by-\(T\) in this autonomous scalar model because the endpoint minimum action decreases with time. The usual first-hitting LDP still requires careful closed/open set treatment at the hitting boundary.

## P0 — Action decomposition (exact algebra)

Completing the square gives
\[
I_T[\phi]
=U(\phi_T)-U(\phi_0)
+\frac14\int_0^T(\dot\phi-U'(\phi))^2dt.
\]
Hence \(J_T\ge \Delta U=U(s)-U(a)\), which is the *quasipotential barrier*. Equality at finite time would require \(\dot\phi=U'(\phi)\) almost everywhere. Beginning exactly at a stable stationary point, uniqueness forces this reverse-gradient solution to remain at \(a\). It cannot reach \(s\) in finite time. Under the regular 1D minimizer hypotheses, \(J_T>\Delta U\) for every finite \(T\); \(J_T\downarrow\Delta U\) as \(T\uparrow\infty\).

This is an endpoint-constrained action statement, not a claim that every physical system minimizes thermodynamic energy.

## P1 — Exact reduction from a path optimization to one scalar parameter

The Euler–Lagrange equation for \(L(x,v)=(v+U'(x))^2/4\) is
\[
\ddot x=U'(x)U''(x).
\]
Autonomy gives the conserved Hamiltonian
\[
E=\dot x\frac{\partial L}{\partial \dot x}-L
=\frac14(\dot x^2-U'(x)^2).
\]
For the monotone minimizer from \(a\) to \(s\),
\[
\dot x=\sqrt{U'(x)^2+4E},\qquad E>0.
\]
Thus the high-dimensional trajectory optimization reduces to the positive root of
\[
T(E)=\int_a^s\frac{dx}{\sqrt{U'(x)^2+4E}}.
\]
A second quadrature gives
\[
\boxed{
J_T=\frac12\int_a^s\sqrt{U'(x)^2+4E}\,dx
+\frac{\Delta U}{2}-ET,\qquad T=T(E).
}
\]
The envelope identity is \(dJ_T/dT=-E<0\). This provides an exact analytic representation, calculated by one-dimensional numerical quadrature, without Monte Carlo or unproven trajectory discretization.

**Numerical checks** for \(u=0\): \(\Delta U=0.25\); \(J_{T=1}\approx0.3938774\), \(J_{T=2}\approx0.2867325\), \(J_{T=5}\approx0.2508972\). These depend on starting exactly at the minimum, target at the saddle, and the stated noise convention.

## P2 — An exactly solvable Ornstein–Uhlenbeck benchmark

For \(dX=-\kappa X\,dt+\sqrt{2\varepsilon}\,dW\), \(X_0=0\), and target \(X_T=d>0\), let \(v=\dot x+\kappa x\). Then
\[
d=\int_0^T e^{-\kappa(T-t)}v(t)\,dt.
\]
Cauchy–Schwarz and the controllability Gramian yield
\[
J_T^{OU}=\inf \frac14\int_0^T v(t)^2dt
=\frac{\kappa d^2}{2(1-e^{-2\kappa T})}.
\]
The quasipotential is \(\kappa d^2/2\), approached only as \(T\to\infty\). The minimum over first-hitting times \(t\le T\) occurs at \(t=T\).

The same formula follows from the *exact Gaussian endpoint variance* \(\mathrm{Var}(X_T)=\varepsilon(1-e^{-2\kappa T})/\kappa\), establishing an independent check of the action calculation.

## CDKA consequence — Correct the rate-to-knowledge map

For contexts \(w\), actions \(a\), horizon \(T\), and exponentially scaled risk \(\alpha_\varepsilon=e^{-c/\varepsilon}\), use *time-constrained* rates \(J_T(w,a)\) to build
\[
R_{T,c}(w,a)=\mathbf1\{J_T(w,a)>c\}
\]
away from equality. Apply the finite-state minimum cover to \(R_{T,c}\). A quasipotential-only replacement can misclassify actions when \(T\) is short.

### Important causal consistency check: parameter scans are not policy contrasts

For \(T=3\), the values \(J_3(u=-0.2)\approx0.493093\), \(J_3(u=0)\approx0.260916\), and \(J_3(u=+0.2)\approx0.091170\) describe **three distinct pre-equilibrated systems**, each starting at *its own action-dependent left minimum* \(a(u)\). They are valid parameter scans of the rate functional but **not** a controlled counterfactual comparison from a common initial physical state.

Consequently, one must **not** infer a legitimate 0-bit/1-bit action-compatibility phase diagram by treating these numbers as competing actions on the same starting condition. Doing so would inadvertently reset the initial state when changing the intervention, violating the causal experiment.

For a valid CDKA control calculation, **hold fixed across candidate actions**: the initial physical state or initial distribution, the failure/viability event, the horizon and the declared observational resources. Only the action-generated dynamics may change. One candidate model has \(X_0=-1\) or \(+1\), failure at the fixed separatrix \(x=0\), and a constant or feedback tilt \(u\) applied at \(t=0\). Its rates require a generalized finite-endpoint action solver; the equilibrium-root quadrature in this note is insufficient without adaptation.

This correction is methodological, not cosmetic: **counterfactual knowledge is relative to a controlled experiment with a common reference world**. In particular, policy-dependent redefinition of the failure event can create artificial "knowledge thresholds." The next T2 experiment must implement the common-state/common-event protocol before drawing information phase boundaries.

## Reproducibility

- \`cdka/variational.py\`: \`quartic_left_action\`, \`ou_endpoint_rate\`; no external Python dependency.
- \`tests/test_variational.py\`: scalar equilibrium roots, actions, limit, monotonicity, and Hamiltonian-envelope derivative.
- Numerical quadrature is checked for moderate deadlines; very long times require adaptive treatment around stationary points.

## Closest established instruments

- Freidlin–Wentzell sample-path large deviations and quasipotentials.
- Classical calculus of variations / Euler–Lagrange / autonomous first integrals.
- Reachability Gramian and Cauchy–Schwarz for the OU benchmark.
- [Berglund & Gentz (2010), Eyring–Kramers](https://math-mprf.org/journal/articles/id1221/).
- [Berglund review, Kramers' law](https://web.ma.utexas.edu/mp_arc-bin/mpa?yn=11-104).
- [Finite-time transitions and memory in an OU feedback process (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12433367/).

**Novelty classification:** baseline/bridge. A genuinely new CDKA result must incorporate constrained sensing, action authority, endogenous organizational resources, or a nontrivial bound beyond this composition.
