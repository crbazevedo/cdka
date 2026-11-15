# Suffix-context implementation and experiment review

**5 November 2026.** Parent checkpoint
`ce252821be4fb5a5075ad12f71ee2da7f14acb7d`; active branches R11/R14.

## Verdict and scope

The finite-context theorem and implemented checker support the declared
ordinary-suffix cover. Exact decisions agree with the stronger eight-feature
parent. Full cold-use measurements support conditional adoption at the tested
K=12 and K=14 cases; the K=4 and K=8 cases are slower. The physical model,
acquisition, observation boundary and program grammar remain inherited.

The proof, production modules and experiment were reviewed separately. The
review identified a vacuous-certificate bug in an exploratory checker before
production and hardened the exact parent-fixture comparison in the experiment.
The retained [proof](suffix-context-proof.md),
[structural controls](../data/suffix-context-controls.json), and
[measurement samples](../data/suffix-context-benchmark.json) support the verdict.

## Implementation checks

The eight-feature checker verifies full sixteen-coordinate equalities rather
than relying on sampled terminal responses. It binds the supplied physical
kernels, terminal and fixed basis, rejects malformed dimensions and inexact
values, and verifies nonnegative outer D/R transports separately from signed
feature transports. The fixed basis works at repair success 0, 4/5 and 1.

The context checker requires eight initial identities, nonempty generators,
positive nested counts, exactly the needed transitions, nonnegative rational
coefficients, and indices bounded by the prefix after each row's birth. It
regenerates all children of retained suffixes and complete programs, verifies
every supplied assignment and retains actual words. A late cone row cannot be
used to justify an earlier closure step.

The first scratch checker accepted `initial=[]` through a truncated zip.
Together with an empty cone, this made every comparison vacuous and omitted MR
without a dominating representative. Production rejects that payload and
truncated initial lists. Regression tests also reject malformed counts,
missing transitions, future-level indices, altered exact identities and
invalid program-cover assignments.

Nineteen new tests cover the two production modules. Independent execution with
`python -S -O` passed all nineteen, establishing that neither site packages nor
enabled Python assertions are required for their checking paths. The
materialized local checkout's full unittest run passed **123 tests**. The
repository workflow additionally runs the complete checkout under Python
3.11, 3.12 and 3.13, with frozen context verification and structural-control
comparison added as explicit gates.

## Exact experiment checks

The frozen library stores one cone through depth thirteen and compact cover
layers for horizons 0, 1, 2, 4, 6, 8, 10, 12 and 14. Each smaller certificate
is reconstructed with the correct cone prefix and independently checked. The
benchmark does not reuse this library.

| Check | Verified count or result |
|---|---:|
| Small exhaustive physical responses with a retained dominator | 120 |
| Retained responses checked directly against full16 physics | 170 |
| Two-way dominance comparisons with the stronger reference frontiers | 340 |
| Retained-response agreements with the prior full16 family implementation | 53 |
| Principal inherited matrix entries | 384 |
| New production-module tests | 19 |
| Local materialized unittest suite | 123 |

The principal comparison validates all four history identities, the complete
96-program identity set and every matrix dimension before comparing values.
Its count is incremented from actual comparisons. Thus neither a truncated
zip nor a hardcoded total can conceal missing parent evidence.

DRDDM remains the principal minimax program; DDDDM remains maximin. The exact
joint-gate scans agree with exhaustive feasibility. The uninformative-sensor
control keeps every value at 1/2 and every regret at zero. Repair-success
boundaries use the same fixed observer and conservative standard-library
context discovery. [Deterministic results](../data/suffix-context-results.json)

The experiment's `--check` command is a reproduction harness: besides checking
frozen witnesses, it reconstructs reference frontiers and conservative repair
controls. The production functions `check_features`, `check_cone` and
`check_family` do not rediscover bases, cones or Pareto frontiers. Both the
harness and the independent structural controls passed with `-S -O`.

## Measurement audit

The reference is the previously accepted program-family algorithm with the
same eight-feature improvement. Each observation starts a fresh Python process.
Methods alternate order within three repetitions at each declared case.
The candidate compiler therefore pays cold NumPy/SciPy imports and the first
HiGHS initialization, all numerical support proposals, exact reconstruction
and family construction. Both paths pay their own physical construction,
preparation, encoding, observer construction, family certificate and decision
certificate serialization/parsing/checking, and queries.

Common interpreter startup and standard-library/project-module imports are
outside the timers. Optional frontier export is measured separately and is
outside the requested decision total. No precomputed cone enters either timed
pipeline. The recorded host used Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0.

| Preparations / K | Parent complete-run range | Context complete-run range | Ratio of complete-run medians |
|---|---:|---:|---:|
| 4 / 4 | 0.151030–0.196059 s | 0.667346–0.768265 s | 0.227682 |
| 16 / 8 | 0.437157–0.441871 s | 1.146926–1.225420 s | 0.373318 |
| 16 / 12 | 3.423126–3.654185 s | 2.612520–2.768391 s | 1.364953 |
| 16 / 14 | 15.284642–16.809920 s | 4.073452–4.505496 s | 3.742134 |

The data preserve raw component times and separately report their median sum.
The K=14 ratio of those sums is 3.836788; the ratio of complete-run medians is
3.742134. These are distinct descriptive statistics from three observations,
without a population-level confidence or universal crossover claim.

The fields for reusing a checked frontier are component-based estimates from
first-use samples, not separate reuse experiments. Serialized sizes are not
peak resident memory. At K=14, the context proof grows from the reference's
71,505 bytes to 796,063 bytes, while the two retained response caches both
occupy 49,657 serialized bytes. Increased proof size remains an explicit cost.

## Adverse controls and limits

The E-only reversal is a physical counterexample to order preservation through
M. It does not by itself prove that a whole unsafe optimizer would choose the
wrong global optimum. The all-horizon lineality argument establishes exact
finite lower bounds of 67 and 272 degraded-response classes at K=8 and K=12,
not the impossibility of every all-horizon pruning method.

The span-error control's twelve parameter settings and four original reference
observations remain preserved. They were single concurrent exploratory runs
with weaker cost boundaries, and do not enter the fresh-process comparison.
The cleaned reproducer's short exact sanity control passed with `-S -O`.
[Rejected route](suffix-span-control.md)

Coverage preserves one executable optimum and feasibility on the inherited
contrast cone and common reserved resource box. It does not preserve all tied
identities, full prediction envelopes or a Pareto objective adding actual
execution cost. Preparation enumeration remains explicit. Context cardinality,
frontier cardinality and rational bit size have no proved polynomial bound.
The benchmark's greater mandatory workload also lowers absolute terminal
fidelity, which is reported alongside regret in every exact scaling case.

## Continuity decision

The completed gate is accepted conditionally on its demonstrated larger
regime. The [integration record](../strategy/suffix-context-integration.md)
defines the next single obligation: exact preparation-family coverage with
compact common-decision outputs and attaining physical histories. It rejects
linear interpolation of informed maxima and requires exact convex witnesses,
same-preparation comparisons and a streamed four-coordinate reference. No
preparation-family experiment is claimed in this increment.
