# T3.B — Reliability exponents, sensing–actuation allocation and the missing knowledge variable

**Status:** exact min-plus asymptotic, causally valid fixed-state action rates, and a one-dimensional optimization; tested numerically. Classical ingredients, **not an original autonomous-agency theorem**.

## Why Shannon information alone is insufficient here

For two equiprobable contexts \(W\in\{L,R\}\), suppose a symmetric sensor misclassifies the context with probability
\[
\delta_\varepsilon=\frac12 e^{-\kappa/\varepsilon}.
\]
Its mutual information is
\[
I(W;Y)=1-h_2(\delta_\varepsilon)\longrightarrow1\ \text{bit}
\]
for *every* fixed \(\kappa>0\) as \(\varepsilon\to0\).

Yet two sensors with very different \(\kappa\) can generate radically different probabilities of catastrophic control failure. Their limiting Shannon information is identical, while their **error exponents** differ.

This is a fundamental distinction for a theory relating knowledge to safety: *what a system can discriminate on average* and *how reliably it can discriminate before an irreversible event* are not equivalent.

This phenomenon belongs to classical information-reliability/large-deviation theory; its role in CDKA is to determine which information quantity belongs in a viability theorem.

## Derive the min-plus law

Let \(J_{\mathrm{good}}\) be the small-noise failure action under a correctly selected intervention, and \(J_{\mathrm{bad}}\) under the wrong intervention. Assume conditional independence of the sensor classification error and physical trajectory noise given the context and chosen control.

The probability of failure is asymptotically a sum of two exponential contributions:
\[
P_\varepsilon(\mathrm{failure})
\asymp (1-\delta_\varepsilon)e^{-J_{\rm good}/\varepsilon}
+\delta_\varepsilon e^{-J_{\rm bad}/\varepsilon}.
\]
The log-sum-exp/Laplace principle yields
\[
\boxed{
\lim_{\varepsilon\to0}-\varepsilon\log P_\varepsilon(\mathrm{failure})
=\min\{J_{\rm good},J_{\rm bad}+\kappa\}.
}
\]
The **min-plus algebra** is not a metaphor: it is the asymptotic algebra of competing rare-event routes. A high-quality physical intervention may be undermined by a low-reliability classifier.

**Boundary:** prefactors affect finite-\(\varepsilon\) values, and the effective exponent need **not** increase monotonically for every decreasing \(\varepsilon\). The code tests convergence, not an incorrect global monotonicity claim.

## Causally valid physical-rate inputs

Use the *same* physical state, failure set and deadline for all controls:
\[
dX_t=(X_t-X_t^3+u)dt+\sqrt{2\varepsilon}\,dW_t.
\]
For the left context, \(X_0=-1.1\), failure at fixed \(x=0\), time horizon \(T\). Protection applies \(u=-a\), wrong-sign actuation \(u=+a\), with \(0\le a\le0.2\).

Define \(J_g(T,a)=J_T(x_0=-1.1,u=-a,\mathrm{hit}\ 0)\) and \(J_b(T,a)=J_T(x_0=-1.1,u=+a,\mathrm{hit}\ 0)\). Reflection gives the analogous right-context actions.

Unlike a parameter scan that starts each tilt at its own equilibrium, these are **valid intervention contrasts from one common physical initial condition**. See [T2.D](T2-causal-information-phases.md).

## Shared sensing–actuation budget

Let the dimensionless model budget \(B\) be allocated into:
- actuation magnitude \(a\);
- sensing resources \(s=B-a\);
- sensor error exponent \(\kappa=\gamma s\), \(\gamma>0\).

The effective risk exponent is
\[
\boxed{
\Lambda_T(a;B,\gamma)=
\min\big\{J_g(T,a),\ J_b(T,a)+\gamma(B-a)\big\}.
}
\]
For our scalar controlled process, the first branch increases with protective magnitude; the second decreases because both wrong-sign physical protection and sensing reliability deteriorate as actuation receives more resources.

At \(a=0\), the good branch is the minimum, whereas at \(a=B>0\) the bad branch is the minimum. With strict monotonicity, the unique max-min optimum is the branch intersection:
\[
\boxed{
J_g(T,a^*)-J_b(T,a^*)=\gamma(B-a^*).
}
\]
No multidimensional optimizer is necessary. **A scalar root finder gives a globally optimal allocation under the stated surrogate assumptions.**

## Small-budget theorem by local sensitivity

Let
\[
q_T=-\left.\frac{\partial J_T(-1.1,u)}{\partial u}\right|_{u=0}>0
\]
for the same endpoint and deadline. Then
\[
J_g(T,a)=J_0+q_Ta+O(a^2),\quad
J_b(T,a)=J_0-q_Ta+O(a^2).
\]
The branch equation gives the small-budget asymptotic:
\[
\boxed{
\frac{a^*}{B}\to\frac{\gamma}{\gamma+2q_T},
\qquad
\frac{\Lambda_T(a^*)-J_0}{B}
\to\frac{\gamma q_T}{\gamma+2q_T}
\quad (B\downarrow0).
}
\]
Thus the optimal allocation is governed by the **deadline-sensitive physical action derivative** \(q_T\), not by a generic information weight.

For \(T=3\), the exact finite-time quadrature gives \(q_T\approx0.83744\). With \(\gamma=2\), the small-budget optimal actuation share is about 54.4%. At \(B=0.1\), numerical optimization yields \(a^*\approx0.05443\) and \(\Lambda_T(a^*)\approx0.31702\).

This result is a genuine computed bridge between stochastic action, observation reliability and a shared resource constraint, but remains a **toy model grounded in existing mathematics**, not a new general control theorem.

## Algebraic and methodological tools that made it possible

1. **Freidlin–Wentzell:** identify the two physical failure exponents from a valid fixed-state counterfactual.
2. **Log-sum-exp/Laplace principle:** combine sensor error and physical failure in min-plus algebra.
3. **Monotone comparative dynamics:** prove opposite ordering of good and wrong-sign action rates.
4. **Max-min geometry:** reduce the optimum to equality of competing branches.
5. **Envelope theorem/local differentiation:** derive \(q_T\) and the small-budget slope.
6. **Finite simulation only for verification:** bisection and quadrature checked against an exhaustive allocation grid.

## What this does not establish

- The sensor noise model and conditional independence are specified, not derived from physical sensing thermodynamics.
- Budget is allocated by an external experimenter and is not yet **endogenously generated, repaired or sustained** by the controller.
- No general connection from nats of mutual information to joules of physical expenditure is implied.
- Finite-\(\varepsilon\) rates and critical equality cases require prefactor analysis.

## Next T3/T4 target

Endogenize the resource state and the sensing/actuation mechanisms themselves. Prove a bound on *ongoing viability* that cannot be reduced to an externally allocated static budget. Compare to dual control, reliability-function theory and constrained POMDPs before claiming novelty.

**Reproduce:** \`cdka/causal_tradeoff.py\` and \`tests/test_variational.py\` SharedBudgetTests.
