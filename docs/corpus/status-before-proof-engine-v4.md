# CDKA — Research State

**Active gate:** G2 — policy-dependent physical information channels and recurrent viability. **Originality:** no general original CDKA theorem established; model-specific proofs and exact counterexamples are distinguished from known instruments. Historical notebooks remain preserved under [docs/corpus](docs/corpus).

## Current increment: T3.D / T4.C

[Proof Engine v3](docs/strategy/proof-engine-v3.md) · [interactive laboratory](https://crbazevedo.github.io/cdka/lab/policy_cuts.html) · [verification record](docs/experiments/E-policy-cuts-v3.md).

1. **Feedback envelope:** under independently feasible row-wise actions, the maximum closed-loop TV contraction coefficient equals the largest cross-input/cross-action row distance. Fixed reset modes each have coefficient zero, while feedback can attain one. This does not create information from identical inputs. [T3.D proof](docs/results/T3D-policy-aware-cuts.md).
2. **Survival-aware discrimination:** propagate the unnormalized joint `mu(W,C,alive)`. For a terminal binary decision, exact total success is `(mass + live separation)/2`. Perfect knowledge conditional on survival can coexist with arbitrarily small survival.
3. **Physical-policy synthesis:** exact design-time occupancy DP over shared prescriptions `C→A(C)`. The controller never receives hidden W, a free observation history, or the designer's occupancy as runtime information. Missing transition mass means failure.
4. **Recurrent maintenance family:** eight live physical states, four observable states, repair consumes a token, successful actuation replenishes a token from the environment and leaves a physical command latch. For repair error p and n cycles, robust survival is `(1-p)^n`; fair-context mean survival is `max(1/2,(1-p)^n)`. After seven cycles at p=0.1, the mean-optimal policy sacrifices one context rather than preserving both. [T4.C proof and caveats](docs/results/T4C-recursive-physical-viability.md).
5. **Randomness is architectural:** one extra persistent read-only independent random bit can change the robust feasible set. Fresh per-step randomization is not a substitute; writable protected memory carrying W is a stronger resource.
6. **Recurrence certificate:** per-context zero-error stationary policies can exist without a shared observation-consistent policy. Exact support invariants and a Boolean implication encoding certify the distinction.
7. **Deadline/fidelity bridge:** robust risk at most alpha requires `p≤1-(1-alpha)^(1/n)`. Under the explicitly stipulated surrogate `p=exp(-J_rep/epsilon)`, this gives an action threshold asymptotically logarithmic in n. Prefactors and uniformity remain required for a true diffusion application.

**Verification:** 18 new Python tests with rational arithmetic; 729 channel architectures; 1,875 randomized local laws; 8 JavaScript kernel tests; independent occupancy, cycle-profile and support-invariant oracles. Offline Chromium rendering/control checks passed at 1440×1000 and 390×844 with no JavaScript errors or horizontal overflow. These browser checks rendered the generated artifact bytes; they were not live public-site navigation tests. Repository CI and deployment are reported separately by GitHub Actions.

**Files:** `cdka/policy_cuts.py`, `tests/test_policy_cuts.py`, `experiments/policy_cuts_sweep.py`, `tests/policy-cuts.test.mjs`, two proof notes, two miniarticles and `docs/lab/policy_cuts.html`.

## Established baseline corpus (known tools, retained)

| Result | Content / link |
|---|---|
| B1 | [Minimum zero-error action code as set cover](docs/results/B1-set-cover.md), with 512 exact 3×3 relation checks |
| T1 / T1.B | [Information thresholds without attractor bifurcation](docs/results/T1-threshold.md); [binary rate–distortion](docs/results/T1-soft-information.md) |
| T2 / T2.A | [Strict-margin barrier-to-bits](docs/results/T2-barrier-to-bits.md); [finite-time action quadrature and OU oracle](docs/results/T2-time-constrained-action.md) |
| T2.B / T2.C | [Saddle-node asymptotics](docs/results/T2-saddle-node-scaling.md); [critical finite-time collapse proof](docs/results/T2-critical-collapse-proof.md) |
| T2.D | [Common-state causal information phases](docs/results/T2-causal-information-phases.md), avoiding action-dependent initial conditions |
| T3.A | [Restricted causal-authority KL gap](docs/results/T3-causal-authority-gap.md) |
| T3.B | [Sensor-error exponents and fixed-frame sensing/actuation allocation](docs/results/T3-fixed-frame-reliability-allocation.md) |
| T3.C / T4.B | [Temporal causal-cut counterexample](docs/results/T3C-temporal-causal-cut.md), exact repair-budget law, higher-order support obstruction and action-dependent reset signaling |
| T4.A | [Controlled lumpability as sufficient recursive quotient](docs/results/T4-controlled-lumpability.md) |

The initial seven articles and their source remain in `docs/lab/articles.mjs`; standalone extensions T3.C, T3.D and T4.C are maintained separately. The published [atlas](https://crbazevedo.github.io/cdka/) links the laboratories.

## Immediate next proof gate

**R1 — coupled implementation constraints:** replace independently selectable channel rows by a physically realizable prescription set `Phi(Z,R)`. Derive sharp bounds or a minimal strict gap against row-wise sensor/action feasibility. Circuit complexity, configuration cost and shared repair substrates must be explicit.

**R2 — produced repair fidelity:** let error probabilities be generated by a constrained sensing/repair/resource process. A positive homogeneous error floor prevents indefinite robust survival in the proved family; a decreasing error schedule cannot be assumed free. Couple an actually derived bistable repair-error law to the finite recurrence, with correct event/deadline and prefactor limits.

**R3 — acquisition versus transport:** new sensing can break `W→C→C'`. Analyze its cost and information gain separately rather than applying a contraction-only theorem to an acquisition step.

**R4 — beyond binary/static contexts:** compose dynamically changing action-compatibility supports with viable physical memory construction and repair; audit against constrained POMDPs and nonclassical information patterns.

The general question remains [issue #9](https://github.com/crbazevedo/cdka/issues/9). This increment supplies exact instruments and finite-family laws, not a universal theory of autonomy or spontaneous intentionality.

## Evidence discipline

Every claim states its physical boundary, memory/clock/randomness resources, intervention class, horizon, survival criterion and prior-art relationship. Tests establish implementation correctness on the cases checked; mathematical proof and novelty audit remain distinct obligations. No energy-in-joules interpretation is inferred merely from nats, action units or resource tokens.
