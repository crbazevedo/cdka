# CDKA — Minimum mathematical instrument index

## Differential and stochastic dynamics

| Tool | Gives us | Use in CDKA |
|---|---|---|
| Cubic stationary-root algebra | Exact bistability domain and saddle-node tilt | Separate physical bifurcations from action-compatibility changes |
| Euler–Lagrange / autonomous Hamiltonian | A conserved energy parameter for FW minimizers | Replace path-space optimization by a 1D quadrature |
| Gramian and Cauchy–Schwarz | Exact minimal finite-time control action for OU | Independent check of nonlinear calculations |
| Freidlin–Wentzell | Rare trajectory probabilities via deterministic action | Risk exponents before a deadline |
| Eyring–Kramers | Mean metastable escape time | Long-time comparison, not fixed-deadline substitute |
| Normal forms and singular perturbation | Universal critical variables and exponents | Saddle-node \(\delta^{3/2}\) versus fixed-T \(\delta/T\) |
| Gamma-convergence | Controlled convergence of rescaled variational minima | Open scaling-limit proof obligation |

## Information and optimization

| Tool | Gives us | Use in CDKA |
|---|---|---|
| Set-cover integer programming | Minimal number of decision messages | Zero-error action sufficiency |
| LP dual certificates | Lower bounds on code cardinality | Verify combinatorial solvers |
| Hypergraph/Dowker complex | Joint rather than just pairwise compatibility | Understand feasible groups of contexts |
| Rate–distortion and Fano | Bits required at a specified error probability | Distinguish hard codes from average mutual information |
| Data processing and KL chain rule | Event-based information bound | Separate potential from physically realizable control |
| Girsanov | Cost of changing diffusion path laws under matched channels | Bridge physical actuation and KL without conflating units |
| Semialgebraic sign stratification | Exact parameter cells for polynomial safety inequalities | Locate code-size thresholds; not generic ODE reachability |

## Recursive regulation and autonomy

| Tool | Gives us | Use in CDKA |
|---|---|---|
| Controlled lumpability / bisimulation | Conditions for an exact predictive/viability quotient | Distinguish immediate from recursive knowledge |
| Belief-state DP / POMDP | Feasible observation-limited sequential policies | Degrading sensor/actuator and repair choices |
| Viability kernels and invariance | Whether a physical organization remains operable | Objective-relative survival, not universal purpose |
| Mechanism intervention and replay | Causal tests instead of correlational labels | Minimal operational autonomy criteria |

## Confirmed illustrative formulas

- \(U_u(x)=x^4/4-x^2/2-ux\), \(u_c=2/(3\sqrt3)\).
- Action identity: \(I_T=\Delta U+\frac14\int(\dot x-U')^2dt\).
- OU exact finite-time action: \(J_T=\kappa d^2/[2(1-e^{-2\kappa T})]\).
- Quartic at \(u=0\): \(\Delta U=0.25\), \(J_1\approx0.393877\).
- Near saddle-node: \(\Delta U\sim[4/(3\,3^{1/4})]\delta^{3/2}\) and \(J_T\sim\delta/(\sqrt3T)\) for fixed T.
- The scaling-collapse candidate uses \(\tau=3^{1/4}T\sqrt\delta\); normalized convergence still requires proof.
- Restricted Bernoulli actuator: \(C_{\rm phys}(\beta)=d_{\rm Bern}(2\beta\|1/2)>d_{\rm Bern}(\beta\|1/4)\) for \(\beta\in(1/4,1/2]\).
- Binary Hamming rate–distortion: \(R(D)=1-h_2(D)\) for \(D\le1/2\).

## Detailed derivations

- [Proof Engine strategy](proof-engine-v1.md)
- [T2.A — finite-horizon action](../results/T2-time-constrained-action.md)
- [T2.B — saddle-node critical scaling](../results/T2-saddle-node-scaling.md)
- [T3.A — causal authority gap](../results/T3-causal-authority-gap.md)
- [T4.A — controlled lumpability](../results/T4-controlled-lumpability.md)
- [T1.B — rate–distortion](../results/T1-soft-information.md)

**Methodological rule:** separate *known instrument*, *newly established example*, *conjectured extension*, and *proven original theorem*. Numerical convergence supports a conjecture, not a proof.
