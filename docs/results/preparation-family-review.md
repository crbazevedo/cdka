# Preparation-family implementation and experiment review

**5 November 2026.** Parent `2f9abfd01b5298de1a1889cc7c57776fa0f86572`.

## Verdict

The exact induction and composed checker support the declared preparation
cover and common complete-program decision. The benchmark supports conditional
adoption at h=12,K=4, h=16,K=4 and h=12,K=12. The h=2,K=4 ranges overlap; the
h=8,K=4 candidate is slower. No polynomial complexity, physical controller
memory, universal crossover, resident-memory reduction or stronger physical
fidelity claim is accepted.

[Proof and independent audit](preparation-family-proof.md) ·
[Exact sweep](../data/preparation-family-results.json) ·
[Fresh samples](../data/preparation-family-benchmark.json)

## Independent implementation checks

The preparation checker reconstructs the full physical D/R closure and actual
initial source-indexed law. Every retained word is regenerated from actual
children. It requires a complete witness for every candidate against the final
retained subset, nonnegative canonical rational coefficients and sum exactly
one. Missing layers, empty lists, invalid index types and malformed numerical
values are explicit failures, including with Python assertions disabled.

The compact decision checker rebuilds its physical problem, checks universal
bounds and independently propagates all actual-history attainers. Comparators
use the same history as the chosen program. It checks all retained candidates,
so an attained but inferior plan cannot certify global optimality. Its
lower-level supplied-family API explicitly requires independently established
coverage; the public composed checker discharges that premise from raw inputs.

The independent reviewer exercised all four combinations of program and
preparation methods at h=4,K=4 against all sixteen physical preparations and
all 96 original physical continuations. The shared two-amplitude/trailing-D
codec agreed with generic four-coordinate and full sixteen-state evaluation.
An incompatible identity D operator used the generic fallback correctly.
The focused audit found no soundness defect.

Thirty-three new regression tests cover physical identities, exact table
agreement, the frozen nontrivial hull, shared arithmetic/fallback, envelope
queries, same-program gates, malformed certificates and raw-input bindings.
They pass with `python -S -O`. The local materialized suite has 156 tests.
The repository workflow checks the complete checkout on Python 3.11, 3.12 and
3.13 and now includes the frozen preparation sweep and exact failure controls.

## Reproduction coverage

| Obligation | Evidence |
|---|---:|
| Frozen preparation horizons | 0, 1, 2, 4, 8, 12, 16 |
| Reference decision-construction value evaluations through h=12 | 195,302 |
| Inherited joint32 physical oracle comparisons | 384 |
| Independently propagated full16 preparation checks | 81 |
| Independently checked informed queries | 26 |
| Per-program bounds compared in fresh h=16 runs | All retained programs, every sample |

The reference evaluation count records work used to obtain the streamed
extrema; it is not a claim that 195,302 individual values were independently
compared to a raw-state oracle. The frozen sweep compares every retained
program's exact bounds with the complete stream through h=12. At h=16 it
checks all convex proof layers, universal bounds and actual attainers. The
separate benchmark performs and checks the entire h=16 stream and compares
exact per-program outputs with the cover in every repetition.

The h=16 frozen proof contains 199 retained actual histories and regenerates
1,867 candidates across all levels. Discovery used no failed LP or exact
support recovery in the recorded fixture. This success is an observation;
failed proposals would conservatively retain candidates.

## Measurement audit

Every sample is a fresh Python process. Program method `feature8` is shared at
K=4; `finite_context8` is shared at K=12. No frozen program or preparation cover
enters either timed worker. Both receive the same verified codec, and the
reference additionally uses its two-dimensional history generation. Hull
discovery remains in four coordinates.

The reference is a depth-first stream with at most h+1 live traversal states,
plus the shared O(h times retained-program-count) response cache and compact
extrema. It never materializes the full table or exhaustive informed profile.
Its checker independently replays the stream. The cover checker checks every
local convex identity, then the compact decision. Both also reconstruct the
physical model and verify the program cover.

The complete-use timer includes physical setup/acquisition, all discovery and
encoding, cold optional imports and first HiGHS initialization when required,
decision construction, complete JSON serialization/parsing/checking, the D^h
informed query, joint gates and compact answer serialization. Three threshold
pairs are queried using six scans: feasibility and feasible identities are
computed separately. A static reviewer found this duplicate scan; it remains
explicit, symmetric and paid in every sample. No source optimization was
introduced between samples. The metadata wording was corrected to disclose
the actual workload.

Interpreter startup, shared stdlib/project-module imports, subprocess transport
and post-task audit instrumentation are outside both timers. The complete-use
wall timer includes instrumentation gaps; component medians are separately
reported. NumPy 2.3.5 and SciPy 1.17.0 run under Python 3.12.14, with OMP,
OpenBLAS and MKL thread environment settings fixed to one for both methods.

| h / K | Stream complete range | Cover complete range | Ratio of medians |
|---|---:|---:|---:|
| 2 / 4 | 0.147840–0.193853 s | 0.180724–0.197868 s | 0.983343 |
| 8 / 4 | 0.275219–0.310218 s | 0.636385–0.748041 s | 0.457550 |
| 12 / 4 | 2.300354–2.307309 s | 1.334117–1.649935 s | 1.675849 |
| 16 / 4 | 39.149497–40.224637 s | 3.198558–3.337954 s | 12.148229 |
| 12 / 12 | 11.171572–12.017570 s | 2.924962–3.331908 s | 3.766084 |

These are descriptive statistics from three observations, not population
confidence intervals. The complete h=16 certificate grows from 19,683 to
1,261,965 bytes. Proof size, arithmetic bit length and runtime are different
costs. No reuse timing or resident-memory result is claimed.

## Retained counterexamples and integration limit

The conic-only physical counterexample changes the global maximin value and
falsely certifies a fidelity floor. The informed-envelope midpoint has a strict
Jensen gap. An attained but inferior program refutes using one history as a
global optimality certificate. Separate-history extrema overstate the actual
regret. All controls have exact fractions and standard-library reproduction.
[Controls](../data/preparation-family-controls.json)

The current result closes an offline evaluator obligation in the inherited
16-state source-fidelity model. It does not close the physical acquisition/
retention question in the different recurrent 64-state model. The next gate
is explicitly prepared in the [integration record](../strategy/preparation-family-integration.md),
with no new observation, ideal selector or free belief state presumed.
