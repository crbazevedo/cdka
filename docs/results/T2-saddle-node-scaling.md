# T2.B — Saddle-node criticality: two action exponents and a crossover

**Status:** elementary saddle-node normal-form derivations and checked asymptotics; the scalar fixed-scaled-time collapse now has a **direct quadrature proof** in [T2.C](T2-critical-collapse-proof.md); higher-dimensional generalizations remain open. No claim of first discovery.

## Why this matters

The standard Eyring–Kramers picture says that an escape barrier collapses as a well disappears. But *the fastest path consistent with a finite deadline* has a different asymptotic cost. This gives CDKA an unusually informative testbed for the dependence of a viability-related knowledge threshold on both parameter distance to bifurcation and time authority.

## Exact critical point

For \(U_u(x)=x^4/4-x^2/2-ux\), stationary points solve \(x^3-x=u\). A saddle-node occurs at
\[
u_c=\frac{2}{3\sqrt3},\qquad x_c=-\frac1{\sqrt3}.
\]
Put \(\delta=u_c-u\downarrow0\), \(y=x-x_c\). Taylor expansion is *exact*:
\[
U_u'(x_c+y)=\delta-\sqrt3\,y^2+y^3.
\]
The left stable and saddle roots have
\[
x_a=x_c-3^{-1/4}\sqrt\delta+O(\delta),\quad
x_s=x_c+3^{-1/4}\sqrt\delta+O(\delta).
\]
Their separation is \(\ell_\delta=2\,3^{-1/4}\sqrt\delta+O(\delta)\).

## P3 — Universal quasipotential exponent

The barrier is the potential integral between the roots. To leading order:
\[
\Delta U_\delta=\int_{x_a}^{x_s}U'(x)\,dx
\sim \frac4{3\,3^{1/4}}\delta^{3/2}.
\]
Thus the well's metastable barrier decays with exponent \(3/2\), a standard saddle-node normal-form law. Numerical checks show the ratio to the predicted leading term approaches 1 as \(\delta\to0\).

The curvatures at the well and saddle have magnitude
\[
|U''(x_{a,s})|\sim2\,3^{1/4}\sqrt\delta.
\]
A formally substituted Eyring–Kramers prefactor therefore scales as \(\delta^{-1/2}\). However, **Eyring–Kramers is not uniform through the degenerate saddle**. The activation asymptotic assumes \(\Delta U_\delta/\varepsilon\gg1\); near \(\delta\sim\varepsilon^{2/3}\), one needs critical-regime analysis (see Berglund & Gentz).

## P4 — Finite-deadline exponent \(1\), with a short proof

For fixed \(T>0\), the FW action is
\[
I_T[\phi]=\frac14\int_0^T\dot\phi^2dt+
\frac12\Delta U_\delta+
\frac14\int_0^T U'(\phi)^2dt.
\]
Cauchy–Schwarz provides the lower bound
\[
J_T(\delta)\ge \frac{\ell_\delta^2}{4T}+\frac{\Delta U_\delta}{2}.
\]
For the linear interpolating path from \(x_a\) to \(x_s\), the first two terms meet this bound, and the last term is \(O(T\delta^2)\), since \(U'=O(\delta)\) between these roots. Therefore
\[
\frac{\ell_\delta^2}{4T}+\frac{\Delta U_\delta}{2}
\le J_T(\delta)\le
\frac{\ell_\delta^2}{4T}+\frac{\Delta U_\delta}{2}+O(T\delta^2).
\]
In particular, at **fixed T**,
\[
\boxed{J_T(\delta)\sim \frac{\delta}{\sqrt3\,T}.}
\]
This is a different exponent from the quasipotential \(\Delta U_\delta\sim C\delta^{3/2}\). The asymptotic regimes differ because the system's intrinsic relaxation time diverges near saddle-node criticality.

**Important:** Both unnormalized actions converge to zero as \(\delta\downarrow0\). The noncommutativity concerns their *normalized asymptotics and scaling regimes*, not the limits of the two unnormalized numbers.

## C1 — Scalar scaling collapse via quadrature

Introduce scaled coordinates and time:
\[
x=x_c+3^{-1/4}\sqrt\delta\,z,\qquad
\tau=3^{1/4}\sqrt\delta\,T.
\]
The action becomes
\[
I_T=\frac{\delta^{3/2}}{4\,3^{1/4}}
\int_0^\tau
\left[z'(s)+1-z(s)^2+
\delta^{1/2}3^{-3/4}z(s)^3\right]^2ds.
\]
The normalized limiting variational problem has endpoint conditions \(z(0)=-1,z(\tau)=+1\) and
\[
\mathcal F(\tau)=\frac14\inf_{z}
\int_0^\tau[z'+1-z^2]^2ds.
\]
**Established in the scalar model by the direct implicit-quadrature argument of [T2.C](T2-critical-collapse-proof.md):**
\[
\boxed{
J_{T(\delta)}(u_c-\delta)
\sim\frac{\delta^{3/2}}{3^{1/4}}\,
\mathcal F(3^{1/4}T(\delta)\sqrt\delta)
}
\]
in a scaling window where \(\tau\) tends to a strictly positive finite limit. The normalized function has two asymptotic regimes:
\[
\mathcal F(\tau)\sim1/\tau\quad(\tau\downarrow0),\qquad
\mathcal F(\tau)\to4/3\quad(\tau\uparrow\infty).
\]
These recover the fixed-deadline \(\delta/T\) cost and the infinite-time \(\delta^{3/2}\) quasipotential. The fixed-positive-scaled-time limit follows by the scalar quadrature proof. Uniformity as \(\tau\to0\) or \(\tau\to\infty\) and multivariate extensions remain open.

## Methodology and next proof obligations

1. **Local algebra:** compute exact cubic stationary roots and the saddle-node Taylor normal form.
2. **Variational bound:** use Cauchy–Schwarz and straight-line construction for the fixed-\(T\) law.
3. **Hamiltonian reduction:** use \(E=(\dot x^2-U'^2)/4\) and time quadrature for normalized action.
4. **Critical uniformity:** use the scalar time/energy quadrature and implicit inverse continuity (T2.C); reserve Gamma-convergence for non-reducible settings.
5. **Information bridge:** treat the resulting \(J_T(u,w)\) as risk exponents, form compatible-action hypergraphs, and identify where control-code cardinality jumps. Do not label a physical saddle-node an information transition automatically.

## Benchmark

See \`cdka/variational.py\` and \`tests/test_variational.py\`. E.g. \(\delta=.01\) and \(T=1\) give \(J_T\approx0.006308\), compared to fixed-time asymptotic \(\delta/\sqrt3\approx0.005774\) and quasipotential \(\Delta U\approx0.001014\).

## Prior work

- [Berglund & Gentz, nonquadratic saddles, 2010](https://math-mprf.org/journal/articles/id1221/).
- [Avelin, Julin & Viitasaari, geometric Eyring–Kramers, 2023](https://link.springer.com/article/10.1007/s00220-023-04845-z).
- Freidlin–Wentzell and standard saddle-node normal forms.

**Novelty classification:** basic exponents and singular perturbation are known mathematical machinery. A CDKA contribution requires new information/authority/maintenance coupling, or a genuinely unrecorded result following a rigorous survey.
