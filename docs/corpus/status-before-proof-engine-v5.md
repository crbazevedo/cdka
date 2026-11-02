# CDKA — Research State

**Active gate:** G2 — joint policy implementability and physically funded recurrent reliability. **Current increment:** Proof Engine v4, T3.E / T4.D. **Originality:** no general original CDKA theorem established; model-specific proofs and exact counterexamples remain explicitly distinguished from known tools.

[Proof Engine v4](docs/strategy/proof-engine-v4.md) · [New miniarticle](docs/articles/T3E-T4D.md) · [New interactive lab](docs/lab/implementability.html) · [Verification](docs/experiments/E-implementability-v4.md) · [Supplemental result register](registry/v4-results.md).

The prior operational snapshot is preserved byte-for-byte at [status-before-v4](docs/corpus/status-before-proof-engine-v4.md); its original root-relative links can also be followed in [the immutable pre-v4 version](https://github.com/crbazevedo/cdka/blob/0d66d713da02ecec62a7d3806bcad953376faef9/STATUS.md). Historical notebooks and all earlier proof notes remain unchanged.

## New demonstrated results

1. **Available actions are not a policy architecture.** Two devices with identical per-state available commands can have maximal closed-loop distinguishability 0 or 1, depending on whether their conditional choices can be combined into one mechanism. The joint implementability relation must not be replaced by its Cartesian marginal relaxation.
2. **Constructive physical selector.** A flagged erasure interface realizes exactly the prescription strip |f1-f0|<=sigma. This is a finite channel construction, not an arbitrary regularization constraint. [Proof](docs/results/T3E-physical-selector-realization.md).
3. **Costed selectivity and repair.** With selector contrast sigma and repair error p, robust renewal survival is product [1+(1-2p_t)sigma_t]/2. Under the stipulated effort laws sigma=1-exp(-w), p=.5exp(-e), a cycle budget r=w+e optimally splits equally; q(r)=1-exp(-r/2)+.5exp(-r). [T3.E](docs/results/T3E-implementable-prescriptions.md).
4. **Resource allocation has two regimes.** log q is convex up to r=1.06959999 and concave above it. Scarce total budget optimally concentrates in one cycle; a claim of always-uniform investment is false. Exact finite-grid DP is independently checked against enumeration.
5. **Concave-envelope certificate.** A tangent at r=1.96872832 gives a sharp asymptotic log-survival rate under average resource limits. A resource-causal threshold rule, collecting h only after each successful intervention, attains that rate. Finite h still implies exponential decay in this architecture.
6. **Exact high-reliability budget.** For beta>=2-sqrt(2), minimum total normalized effort is -2n log[1-sqrt(2 beta^(1/n)-1)], asymptotically 2n log n. Its coefficient and law are model-dependent, not universal thermodynamic claims.
7. **Finite design versus infinite policy.** A sequence with leading cumulative effort 2n log n can have zero or positive infinite survival depending on its lower-order log-log term. Exact criterion in this family: sum exp(-r_t/2)<infinity. [T4.D proofs](docs/results/T4D-produced-fidelity-budgets.md).

## Verification and corpus

14 new Python tests, including 3,675 rational local-policy combinations and 125 constructive selector triples; 6 new JavaScript tests; exact finite-grid and independent enumeration oracles. Offline Chromium checks rendered five SVGs and exercised all controls at desktop/mobile sizes. No public-site browser validation is inferred from those offline checks. GitHub CI and Pages deployment are verified separately after publication.

Files: `cdka/implementability.py`, `cdka/selector_realization.py`, corresponding tests, `experiments/implementability_sweep.py`, three proof notes, the v4 strategy, miniarticle and `docs/lab/implementability.html` with isolated kernels and charts.

## Retained foundations

[Full main register](registry/hypotheses.md) · [Proof Engine v3](docs/strategy/proof-engine-v3.md) · [T3.D policy-aware cuts](docs/results/T3D-policy-aware-cuts.md) · [T4.C recurrent organization](docs/results/T4C-recursive-physical-viability.md) · [B1 set cover](docs/results/B1-set-cover.md) · [T2 finite-time action](docs/results/T2-time-constrained-action.md) · [T2 causal phases](docs/results/T2-causal-information-phases.md) · [T3.B fixed-frame tradeoff](docs/results/T3-fixed-frame-reliability-allocation.md).

## Next hypotheses

**H-structure:** costly self-reconfiguration changes the actual feasible prescription family Phi(Z,R), potentially creating a protected information channel and a nonempty recurrent safe kernel. Derive minimum enabling cost using observation-consistent support synthesis and finite controller libraries.

**H-correlation:** common physical noise may invalidate independent selector/write failures. Start with exact coupling/Frechet bounds and identify error cancellation versus common-mode catastrophe before new stochastic asymptotics.

**H-redundancy:** distinguish progressively rarer errors from recoverable errors. Correction, redundancy and tolerable nonfatal actions may break the present n log n law and finite-flux no-go; their costs and physical channels must be explicit.

**H-physical calibration:** derive actual error probabilities from fixed-causal-frame bistable mechanisms. Do not substitute a large-deviation exponent for a finite-noise probability or equate nats, action, normalized effort and joules.

The broader issue remains [#9](https://github.com/crbazevedo/cdka/issues/9). A general theory of spontaneous autonomy or intention is still not established by these finite models.
