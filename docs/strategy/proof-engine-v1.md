# CDKA Proof Engine v1.0 — Instrumental research strategy

**2026-11-01 · Active stage M1→M2 · No novel CDKA theorem claimed.**

## Mathematical chain to make precise

\[
(\theta,Z,R,\Pi_{\rm phys})\to\mathscr C_T\to J_T(w,a)\to
R_{T,c}(w,a)\to K_{\min}\to\mathcal O_{t+1}.
\]

Physical organization and intervention constraints determine attainable path laws. Constrained path actions determine finite-horizon risk rates. Risk thresholds define a state–action compatibility relation. Its hypergraph determines the minimum zero-error decision code. Recursively maintaining the organization changes the admissible actions and future observations.

**Our scientific opportunity is in the coupled arrows, not any known formula in isolation.**

## Ranked toolbox

| Priority | Mathematical tool | Task | Established antecedent |
|---|---|---|---|
| A | Cubic discriminant and saddle-node normal form | Exact attractors and critical exponents | Bifurcation theory |
| A | Euler–Lagrange, autonomous Hamiltonian, quadrature | Finite-time action without path discretization | Calculus of variations |
| A | OU controllability Gramian | Independent exact finite-horizon benchmark | Linear systems / Cauchy–Schwarz |
| A | Freidlin–Wentzell LDP and contraction | Path probability to action minimization | Stochastic processes |
| A | Eyring–Kramers, potential theory | Long-time mean exit and validity limits | Metastability |
| B | Hypergraphs, 0–1 set cover, linear-program dual | Minimal action-sufficient code and certificates | Combinatorial optimization |
| B | Rate–distortion, Fano, data processing | Information required at nonzero risk | Information theory |
| B | Path-space KL and admissible law families | Universal lower vs physical intervention cost | Girsanov / constrained KL control |
| C | Controlled lumpability, bisimulation, POMDP DP | Does a decision code remain sufficient in time? | Stochastic control |
| C | Causal interventions and replay | Internal regulation vs externally scripted behavior | Structural causal models |
| Later | Gamma-convergence | Uniform scaling of near-critical action minimizers | Variational convergence |
| Later | Fisher–Shahshahani and replicator geometry | Endogenously selected regulatory mechanisms | Evolutionary dynamics |

No generic "agency objective," deep RL or universal free-energy ansatz is needed at this stage.

## G1 — T2 mathematical bridge

- Prove fixed-time quartic action via the first integral and one-dimensional quadrature.
- Use OU as a theorem-level independent benchmark.
- Show quasipotential scaling \(\Delta U\sim C\delta^{3/2}\) and fixed-deadline action \(J_T\sim\delta/(\sqrt3 T)\).
- Investigate a normalized finite-\(\tau\) scaling theorem through rescaled action functionals and compactness.
- Use \(J_T(w,a)\), not the quasipotential alone, for risk-sensitive action compatibility.
- Produce a phase diagram in horizon \(T\), risk rate \(c\), tilt \(u\), noise \(\varepsilon\).

**Exit criterion:** rigorous identities and numeric error checks; any new claim must exceed a plain composition of FW+set cover. See T2.A and T2.B proof notes.

## G2 — T3/T4 potential novelty gate

- Add a sensor/actuator organization \(Z_t\), repair resources \(R_t\) and observation-limited policy class \(\Pi_{\rm impl}\).
- Derive *separate* Fano/data-processing and physical-control bounds first.
- Characterize the joint realizable region of diagnostic information, intervention action and sustained organizational resource.
- Search for a strict joint feasibility bound unaccounted for by independent marginal limits.
- Test finite models by exhaustive policy enumeration, with dual-control and resource-constrained POMDP prior-art comparison.
- Compare one-step action sufficiency against an exact recursively lumpable state abstraction.

**Exit criterion:** prove a new constrained relation or publish an informative counterexample; do not rename standard constrained POMDP feasibility as novel.

## G3 — Causal autonomy discrimination

Intervene independently on memory, sensing, actuators and endogenous repair; compare passive stability, feedback, observationally matched external replay and self-maintenance. Quantify identifiability subject to a declared boundary and intervention authority. Do not treat complexity or persistence as agency.

## Known optimization certificates for action codes

For acceptable states \(H_a\subseteq W\), minimum code size is the integer program
\[
\min_{z\in\{0,1\}^{|A|}}\sum_a z_a,\quad
\sum_{a:w\in H_a}z_a\ge1\quad(\forall w).
\]
Its LP dual (after relaxation) is
\[
\max_{y_w\ge0}\sum_w y_w,\quad
\sum_{w\in H_a}y_w\le1\quad(\forall a).
\]
Dual feasible points certify lower bounds. This is known set-cover algebra, not CDKA novelty. For polynomial threshold constraints, semialgebraic sign cells may yield exact parameter regimes; do not presume arbitrary ODE reachability is semialgebraic.

## Evidence protocol

Every result requires: (1) definition and scope; (2) proof or falsifying counterexample; (3) independent finite/analytic verification; (4) numerical method and precision/error limits; (5) scientific prior art; (6) visualization of feasible sets, rates, asymptotics or phase geometry; (7) status in the hypothesis register. Document failures rather than reformulating to rescue an assertion.

**Next proposed original theorem target:** characterize recursive viable-control information when the same endogenously evolving organization determines sensing quality, physically admissible interventions and its own repair.
