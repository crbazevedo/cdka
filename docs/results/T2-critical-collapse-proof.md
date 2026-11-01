# T2.C — Critical scaling collapse: direct quadrature proof

**Status:** mathematical derivation within a specified scalar gradient model, using standard variational results. **Originality not established.** This is a refinement of the proof obligation in T2.B.

## Problem and exact rescaling

For \(dX_t=-U'_u(X_t)dt+\sqrt{2\varepsilon}\,dW_t\), \(U_u=x^4/4-x^2/2-ux\), start at the left minimum and reach the middle saddle by time \(T\). Put
\[
u_c=\frac2{3\sqrt3},\quad \delta=u_c-u\downarrow0,\quad
x_c=-\frac1{\sqrt3}.
\]
Introduce
\[
x=x_c+3^{-1/4}\sqrt\delta\,z,\qquad
\tau=3^{1/4}T\sqrt\delta,\qquad
e=E/\delta^2.
\]
Because the quartic gradient expansion is exact,
\[
U'_u(x)=\delta g_\delta(z),\quad
g_\delta(z)=1-z^2+\delta^{1/2}3^{-3/4}z^3.
\]
The left minimum and saddle become \(z_-(\delta)\to-1\) and \(z_+(\delta)\to1\).

## The limiting scalar quadrature

For any finite \(\tau>0\), define \(e_\delta>0\) by the **one-dimensional equation**
\[
\tau=
\int_{z_-(\delta)}^{z_+(\delta)}
\frac{dz}{\sqrt{g_\delta(z)^2+4e_\delta}}.
\tag{1}
\]
The right side is continuous and strictly decreasing in \(e>0\), ranges from \(+\infty\) to \(0\), and hence determines a unique \(e_\delta(\tau)>0\). Its limit is the unique \(e(\tau)>0\) solving
\[
\tau=\int_{-1}^1\frac{dz}{\sqrt{(1-z^2)^2+4e(\tau)}}.
\tag{2}
\]

The exact finite-horizon action quadrature from T2.A, after rescaling, is
\[
\frac{3^{1/4}J_T(u_c-\delta)}{\delta^{3/2}}
=\frac12
\int_{z_-}^{z_+}\sqrt{g_\delta(z)^2+4e_\delta}\,dz
+\frac{3^{1/4}\Delta U_\delta}{2\delta^{3/2}}
-e_\delta\tau.
\tag{3}
\]

## Proposition — normalized action collapse (fixed positive scaled time)

For every fixed \(\tau\in(0,\infty)\) and \(T(\delta)=\tau/(3^{1/4}\sqrt\delta)\),
\[
\boxed{
\lim_{\delta\downarrow0}
\frac{3^{1/4}J_{T(\delta)}(u_c-\delta)}{\delta^{3/2}}
=\mathcal F(\tau)
}
\]
where
\[
\mathcal F(\tau)=
\frac12\int_{-1}^{1}\sqrt{(1-z^2)^2+4e(\tau)}\,dz
+\frac23-e(\tau)\tau,
\]
and \(e(\tau)\) is uniquely defined by (2).

### Direct proof, avoiding an unnecessarily heavy Gamma-convergence apparatus

1. The cubic stationary-root equation shows \(z_\pm(\delta)\to\pm1\), and \(g_\delta\to g_0=1-z^2\) uniformly on a fixed neighborhood of \([-1,1]\).
2. For each \(e>0\), integrands in (1) converge uniformly, and the corresponding time functions converge locally uniformly in \(e\), including the moving endpoints. The limiting time function is strictly decreasing and maps \((0,\infty)\) onto \((0,\infty)\).
3. Hence solutions of the implicit equation satisfy \(e_\delta(\tau)\to e(\tau)\), for each fixed finite \(\tau>0\).
4. In (3), the first integral converges; the normalized barrier satisfies \(3^{1/4}\Delta U_\delta/\delta^{3/2}\to4/3\) by the saddle-node normal form. Passing to the limit yields the stated \(\mathcal F\). QED, conditional only on the classical existence and monotonicity characterization of the 1D minimum-action path in T2.A.

The one-dimensional minimizer is monotone: its conserved energy is \(E>0\) because a finite-time extremal cannot start at the equilibrium with \(E=0\) and leave it by uniqueness; hence its velocity never vanishes and must point from the left minimum to the saddle.

The argument is valid for *fixed positive finite scaled \(\tau\)*. Uniformity as \(\tau\to0\) or \(\tau\to\infty\) is a separate issue.

## End-point regimes and time scales

- **Short scaled time:** \(e(\tau)\sim\tau^{-2}\), \(\mathcal F(\tau)\sim\tau^{-1}\) as \(\tau\downarrow0\).
- **Long scaled time:** \(e(\tau)\to0\), \(\mathcal F(\tau)\to4/3\) as \(\tau\uparrow\infty\).
- **Fixed original deadline:** if \(T\) is fixed while \(\delta\to0\), then \(\tau\to0\). A separate Cauchy–Schwarz/straight-line squeeze proves \(J_T\sim\delta/(\sqrt3T)\), as in T2.B.
- **Long-time quasipotential:** if \(T\sqrt\delta\to\infty\) within a regime where uniform convergence is justified, the barrier law is \(\Delta U\sim[4/(3\,3^{1/4})]\delta^{3/2}\). Do not derive uniformity solely from pointwise convergence in \(\tau\).

**Key insight:** the intrinsic critical relaxation time scales as \(1/\sqrt\delta\). The effective action has different apparent exponents depending on whether intervention occurs faster or slower than that time scale.

## Numerical independent check

The exact quartic quadrature and universal normal-form quadrature use independently parameterized root equations, with a common transparent Simpson integration routine. At \(\tau=0.4\), the universal value is approximately \(\mathcal F(0.4)=3.219878\). For \(\delta=0.03,0.01,0.002\), the respective absolute normalized deviations are approximately 0.01973, 0.00650, 0.00129. These numbers support the limit but do **not** constitute its proof.

Code: \`cdka/variational.py\` functions \`quartic_left_action\`, \`saddle_normal_form_action\`; tests: \`tests/test_variational.py\`.

## Strategic consequence

Use algebraic normal forms, conservation laws and implicit-function continuity **before** reaching for expensive trajectory optimization, Monte Carlo, symbolic PDE solvers or general Gamma-convergence. In this one-dimensional case the reduced quadrature already delivers the scaling theorem.

The scientific novelty frontier remains elsewhere: translating these physical action rates into admissible action sets, constrained information codes and evolving *organizational* capacities. Existing saddle-node scaling and variational identities alone are not CDKA-specific discoveries.
