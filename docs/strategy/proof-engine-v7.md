# CDKA Proof Engine v7 — Physically usable health knowledge

**Stage:** G4: hidden organizational health, paid diagnosis and globally costed contingent policies. **Scientific status:** model-specific exact propositions using existing Bayesian decision, finite-controller synthesis and controlled Markov instruments; novelty unestablished.

## Distill the research pivot

### Strategy: the physically available interface is the theorem's domain

Prior work v6 proved that `(k,h,b)` is a sufficient *physically readable* quotient while health `h` remains available. V7 removes this assumption, so that the same quotient is a correct designer statistic but not a runtime controller input. We preserve the underlying microphysics and the failure event rather than introducing an easier arbitrary payoff table.

We seek a gap between **knowing that a specific contingent policy would work** and **having the physical capability to diagnose, compile, select and fund that policy**. The primitive should ultimately be an architecture-dependent family `Φ(Z,R)` of complete prescriptions, not merely available command sets `A(c)`.

### Tactics: separate the three causes of lost control

1. **Information quality:** diagnostic error, delay and latent health drift.
2. **Decision implementability:** the same circuit must map readable diagnostic outputs to different commands; charge its fixed cost and represent its physical state.
3. **Physical viability:** the remaining resource must still finance the chosen command before the deadline; diagnostic failure also kills a path.

Each cause has a negative control: perfect unpaid observer oracle; perfect diagnostic but no selector; paid selector but no remaining action budget; accurate obsolete reading; and inspection that is itself risky. All share a fixed physical state, failure criterion and terminal horizon.

## Work backwards from a nontrivial strict gap

1. Find latent health states for which the optimal actions differ: in v6 the healthy corrector benefits from `refresh`, the degraded corrector favors `hold`.
2. Preserve the single physical kernel and calculate exact survival values by conditional health and action.
3. Erase the health flag from physical observations, while retaining the measurable syndrome `k` and resource ledger `B`.
4. Implement physical diagnosis as a BSC writing an observable bit, followed by health transition during an interval **common to both** policies.
5. Add fixed diagnostic and selector costs **independent of signal**, forbidding accidental sidechannel through resource balance.
6. Optimize complete terminal truth tables by exhaustive exact-rational enumeration, and cross-check the scalar threshold derived by calculus/decision geometry.
7. Extend to stage-dependent observation-memoryless controllers, allowing the offline designer to calculate an occupancy but not handing it to runtime.
8. Perturb each assumption and record which alternative route should activate.

## Results established in this increment

- **T4.H general formula:** exact Bayes decision over physically funded one-step diagnosis with hidden health and intervention-specific success.
- **T4.H scalar threshold:** with uniform prior and the default two-action ordering, `ΔV=(1/2)[g-(η+ν−2ην)(g+ℓ)]_+` if all program/command costs are affordable and inspection itself is safe. Exact critical error `6402641323/32975801023≈.1941618`.
- **T3.G selector feasibility:** `d=c=1`, terminal refresh cost2; B=3 produces no diagnostic gain even with perfect observation. At B=4 the contingent program is implementable and valuable. Resource costs do not encode H by themselves in this model.
- **T4.H hidden-health policy gap:** exact offline stage-dependent prescriptions reading only `(k,B)` give n=1,2,3 lower values than a full-health-visible Bellman relaxation; the gap grows across this tested fixture. Not a general monotonicity theorem.
- **Temporal diagnostic decay:** hidden-health drift makes the early observation stale; `η_eff(t)=[1-(1-2η)(1-2ν)^t]/2` and crosses a decision-value threshold without changing sensor bit capacity about its own past input.

## Instruments ranked by explanatory value

| Priority | Instrument | Role | Trap to avoid |
|---|---|---|---|
| A | Rational Bayes risk and Blackwell comparison | Exact one-step diagnostic value and action thresholds | Mutual information alone does not price action/circuit/deadline |
| A | Finite-state controller libraries / whole prescriptions | Separate available actions from implementable conditional rules | Cartesian product relaxation that invents hardware |
| A | Sub-stochastic occupancy DP | Design fixed physically readable policies without runtime latent state | Feeding a designer posterior to the controller |
| A | Product of binary Markov channels | Diagnosis staleness and diagnostic error | Comparing policies at different physical deadlines |
| B | LP/MILP and truth-table synthesis | Cost-aware selector-library certificates | Counting each action's costs independently |
| B | Discrete time-to-decision graphs | Complete information paths and resource sidechannel audit | Free memory of outcome-dependent expenditure |
| B | Exact fixed-kernel sensitivity/envelope | Prioritize improvement of diagnosis vs repair | Differentiating across a policy switch without checking |
| C | Bayesian filters with physical memory constraints | Multi-step hidden-health and resource-limited belief state | Unlimited posterior precision without physical storage |
| Later | Witsenhausen-style action signaling | Detect hidden resource/action channels | Asserting diagnosis impossible after ignoring action traces |
| Later | Freidlin–Wentzell and stochastic thermodynamics | Produce sensor/circuit error laws and energy costs | Equating bits, action exponents, tokens and joules |

## Proof gates and criteria

**G4.A — Complete now:** 12 new exact tests, including 162 independent health/diagnosis/age/budget configurations; exact threshold and failure-lifetime controls; strict hidden-vs-visible horizon values; independent two-stage prescription enumeration. No more feature expansion for this one-step subfamily without a new theorem or falsifier.

**G4.B — Next, active R11:** introduce a paid health diagnosis whose result must be stored through a subsequent repair before being used; jointly optimize acquisition, writing, retention and action with a **finite physical memory**. The belief-state oracle is an upper bound, not the implemented policy.

**G4.C — Next, active R14:** make the selector itself degradable, and model at least two hardware implementations with different fixed and recurrent costs. Find minimal physically attainable policy library and an exact program-installation certificate; compare against strong simple policies and constrained POMDP precedents.

**G5 — Conditional:** only advance to an invariant/viable recurrent component after G4.B/C demonstrate a strict physical cut or an implementability theorem stronger than the one-step standard Bayes calculation.

**G6 — Parked:** physical calibration of inspection/circuit failures and resource costs under fixed causal frame, with valid finite-noise probabilities and prefactors.

## Research memory and dead-end triggers

Canonical alternatives: `registry/research-options.json` (v7, 37 branches; at most two active). New diagnostic facts and falsified simplifications added under R33–R37 / D15–D18. Retain all v1–v6 original records and source files. Every restart must state the causal invariant, minimal test, trigger, proof target, closest predecessor, and stopping rule.

**Stop rule:** after two additional small models without a structural proof obligation or meaningful falsification, audit predecessor theorems and avoid enlarging the demo. New math must explain a restriction beyond a standard known POMDP, not merely reproduce it.

## Prior art explicitly limiting novelty

- Ellis, Jiang & Corotis 1995: inspection-maintenance POMDP.
- Kim, Choi & Lee 2018: integrated inspection, maintenance and installation.
- Lin, Song & Pozzi 2022: binary component inspection value-of-information.
- Winterer et al. 2024: physically simpler POMDP policy synthesis with MILP.
- POMDP value functions and belief-state filtering: classical tools.

Neither `ΔV` nor a threshold caused by fixed hardware cost is claimed as originally discovered. Our potential contribution requires **endogenously generated and sustained** sensing/selection capability coupled to future viability.
