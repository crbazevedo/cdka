# Research memory: evidence that changes the next decision

This is the continuity record for the active **R11/R14** line. Its purpose is
to turn a result or failure into a rule for the next experiment. The
[hypothesis register](../../registry/hypotheses.md) records scientific status;
the proofs, exact fixtures and reviews linked below remain the evidence.
This file should preserve why a decision changed, including routes that failed.

The larger objective is constructive control over task-relevant distinctions:
retain enough information to certify a physically feasible continuation,
recover a distinction when a new capability requires it, and pay for both the
physical mechanism and the computation that discovers the interface. Concrete
adaptations and implementations remain useful contributions when their
antecedents are established; originality, correctness and practical advantage
are separate claims. [Prior strategic decision](proof-engine-v15.md)

## Established checkpoint

The maintenance-access and reachable-diagnosis increments reuse one inherited
register, hidden substrate health and the actual six-NAND voter. The second
increment replaces arbitrary admissible preparations with one paid shared
sensor acquisition followed by D/R histories. Its terminal task is fidelity to
the hidden source H. The controller does not receive the evaluator's history
label, H, substrate health or repair result.

| Proven statement | Scope that must travel with it |
|---|---|
| Old/new response rank 10/12 | Arbitrary laws on 16 physical states; terminal event `vote=1`; at most one paid M. |
| Old/new response rank 11/13 | Arbitrary laws on the 32-state joint model; terminal event `vote=H`. |
| Four signed contrast coordinates | Shared fair-source acquisition and every finite D/R preparation history; known mass offset 1/2; an input-boundary representation. |
| Unique minimax common program DRDDM | The principal four-preparation, 96-program fixture: two preparation updates, exactly four continuation D/R updates, at most one additional M. |

The principal minimax regret is `0.0025321961178476887...`; its minimum
fidelity is `0.8491834489516084...`. DDDDM instead maximizes minimum
fidelity. No program in that library simultaneously attains regret at most
`0.003` and fidelity at least `0.85`. These are complete-program statements,
not claims about every possible adaptive controller.
[Integration](reachable-diagnosis-integration.md) ·
[Independent reproduction](../results/reachable-diagnosis-review.md)

## Lessons and their decision consequences

### Preserve the physical and informational contract

| ID | Evidence or failed simplification | Rule carried forward |
|---|---|---|
| RM.1 | A single sensor result is a shared cause of three writes. Shared health affects successive gate calls. Intermediate voter observations already distinguish the maintenance witness under the old library. | Preserve the joint causes and the declared observation boundary. Replacing a shared draw by independent marginals, revealing a history label, or adding an observation changes the problem and requires recertification. |
| RM.2 | The old arbitrary preparation pair is not a witness for the later acquisition class: old responses already identify the entire reachable contrast domain. Changing the terminal event changes global ranks. | State the preparation domain, terminal event, feasible continuations and known constants next to every sufficiency or minimality claim. Do not transfer a global witness or dimension into a different domain. |
| RM.3 | D/R preserve the four-coordinate contrast domain for every history length. M breaks it even for an actual acquisition law; reapplying the eight-orbit quotient yields a strictly nonzero error. | Check domain preservation for every operation. Compile a response through the complete physical continuation, including M, before restricting it to the input domain. Small error does not establish exactness. |
| RM.4 | Optional updates select immediate readout I in the principal healthy regime. DRDDM is the compromise for mandatory work. | Freeze the horizon convention, terminal time, resources and grammar before interpreting an optimum. Carry the workload requirement into the result statement. |

Evidence: [maintenance review](../results/maintenance-access-review.md),
[reachable-domain proof](../results/reachable-domain-proof.md), and
[reachable-diagnosis controls](../results/reachable-diagnosis-review.md).

### Preserve the decision, not just a convenient statistic

| ID | Evidence or failed simplification | Rule carried forward |
|---|---|---|
| RM.5 | Pairwise optimal-plan intersections can all be nonempty while the whole-class intersection is empty. Agreement on a first action can hide incompatible suffixes. DRDDM is optimal for no individual preparation. | Certify one complete feasible program shared by the whole class. Do not restrict candidates to individual optima or select a suffix using unavailable history information. |
| RM.6 | Subtracting response envelopes attained at different histories invents positive regret even for a pointwise dominating plan. | Use correlated differences: `R(p)=max_h(max_q V[h,q]-V[h,p])`. Keep the same preparation in the program and its comparator, and retain attaining witnesses. |
| RM.7 | Under the fixed sensor contract, `V_eta=1/2+(1-2 eta)(V_0-1/2)`. At `eta=1/2`, every regret is zero and every fidelity is 1/2. | Apply the relative-loss limit and absolute-fidelity floor to the same program. Lower regret alone can indicate lost information rather than better control. |
| RM.8 | A coordinatewise response midpoint need not be the response of a probability law. Uniform prediction error epsilon implies at most 2 epsilon decision regret in general. | Label free response centers, physical law centers and decision guarantees separately. Do not propagate a free center as a physical state or reuse a pair-specific tolerance as a whole-class guarantee. |

Evidence: [class theorem and counterexamples](../results/reachable-interfaces-proof.md)
and [principal exact fixture](../data/reachable-diagnosis-results.json).

### Pay for the complete method and retain adverse evidence

| ID | Evidence or failed simplification | Rule carried forward |
|---|---|---|
| RM.9 | The four-coordinate evaluator lowers measured runtime and serialized cache size, but still enumerates `2^h` histories and `(K+2)2^K` programs. Its fixed dimension does not bound the number of reachable extreme points. | Compare against the strongest available cached evaluator. Price discovery, encoding, compilation, queries, witness construction, checking, serialization and reuse. Fewer coordinates or visited leaves alone do not establish a speedup or a complexity bound. |
| RM.10 | Supplied inverse identities and attaining witnesses can be checked without rerunning basis discovery or optimization. The table certificate nevertheless assumes physically correct, complete inputs. | Separate discovery from verification and measure both. Bind exact values, ordered identities and contract. Check physical kernels, reachability and grammar completeness independently; a hash only binds data. |
| RM.11 | Installed gates, gate evaluations, writes, cell-channel updates, service slots and clock intervals are different resources. Repair is prepaid in both internal branches. | Keep physical cost vectors and evaluator costs separate. Report common reservation and actual execution. Do not treat evaluator coordinates as readable physical memory or invent an uncalibrated scalar energy price. |
| RM.12 | Earlier count-only reduction, omitted persistent noise and redundancy favored over cheaper maintenance failed. The later naive maintenance quotient and optional-workload interpretation also failed. | Preserve a minimal counterexample and the corrected decision. Stop or narrow machinery that fails correctness or total-cost gates; do not add a new physical model to make the same claim easier. |

Evidence: [cost and implementation benchmark](../data/reachable-diagnosis-benchmark.json),
[maintenance discovery/check contract](maintenance-access-bridge.md),
[class checker scope](../results/reachable-interfaces-proof.md), and
[earlier dead ends](proof-engine-v15.md).

## Active next gate: certify program families before enumeration

The established baseline is the cached four-coordinate evaluator, with exact
rational arithmetic. The current unresolved bottleneck is constructing all
complete programs. The next experiment keeps the physical model, observation
boundary and one-maintenance grammar fixed while attempting to reject an entire
residual program family before generating its members. Preparation enumeration
may remain explicit in this first gate; success on one axis must not be reported
as solving both.

The comparison must answer five concrete obligations:

1. **Declared output.** State whether the search returns one optimal program,
   all optimal programs, a tolerance-qualified program, or infeasibility of a
   joint regret/fidelity gate. Equality pruning that preserves one optimum does
   not establish uniqueness or enumerate all ties. A dominance frontier proved
   sufficient under the same prepaid resource box need not preserve the complete
   prediction-response envelopes, all tied program identities, or a Pareto front
   that adds actual per-program execution cost as an objective or constraint.
2. **Coverage and soundness.** Every legal complete program is represented by
   an evaluated leaf or a certified rejected family. A checkable residual bound
   must justify every rejection without enumerating the rejected members.
   An optimistic controller with extra information may supply a bound, but is
   not an executable substitute for the original controller.
3. **Correlated witnesses.** Preserve same-history comparator differences and
   the absolute floor. Count the work needed to discover the informed per-history
   optima; importing them from an exhaustively built table is not free pruning.
4. **Fair total cost.** Compare matched outputs with the current cached
   four-coordinate baseline. Report setup, search, encoding, certificate
   construction/checking, rational bit lengths, serialized size and reuse.
   Count complete programs never generated separately from prefixes visited.
5. **Decision after evidence.** Promote the method only with soundness and a
   measured total-cost advantage on a declared family. Otherwise retain the
   exact obstruction, looseness or overhead result and narrow the next attempt.

The existing [integration gate](reachable-diagnosis-integration.md) authorizes
either a successful certificate with demonstrated savings or a recorded
obstruction. The earlier benchmark establishes no family-pruning result.
New outcomes belong in a dated decision record linked to their code, exact
certificates, benchmark and independent review.

## How to extend this memory

For each substantive iteration, append the claim tested, the unchanged contract,
the decisive evidence, the accepted or rejected method, and the one resulting
next obligation. Preserve the original failed claim when its correction matters.
Use separate labels for proved identities, verified finite fixtures, local
runtime measurements and open hypotheses. Lessons transferred from another
project are design hypotheses here until a local proof or experiment supports
them; do not import its numerical results as CDKA evidence.

## Decision record — 4 November 2026: program-family gate accepted conditionally

**Claim tested.** Avoid generating complete programs while preserving one
optimal common executable program under the unchanged acquisition, D/R/M
physics, mandatory workload and prepaid resource box. This record resolves the
previous gate above; R11/R14 remain the only active research branches.

**Accepted result.** An inductive cone-dominance cover preserves informed
values, minimax regret, maximin fidelity and joint regret/fidelity feasibility.
It uses nonnegative D/R transports and the exact four-by-sixteen bridge `E M`
on full physical suffixes. Every representative is an original complete
program, not a convex mixture or a free response envelope. At K=8 the method
generates 542 of 2,560 complete programs, leaves 2,018 ungenerated and retains
17 representatives. The exact sweep checks 3,192 dominance relations, 53
retained physical responses and all 384 parent-fixture values.
[Proof](../results/program-family-proof.md) ·
[Exact evidence](../data/program-family-results.json)

**Cost decision.** With 16 preparations and K=8, the matched-output total falls
from 3.81252 s to 1.40047 s, a local 2.7223-fold speedup including cold physical
setup and the independent family checker. Four preparations/K=4 are effectively
tied; four preparations/K=6 are slightly slower with pruning. Accept the
algorithm for its demonstrated regime, not as a universal replacement.
[Benchmark](../data/program-family-benchmark.json) ·
[Review](../results/program-family-review.md)

**Rejected route retained.** Physical Bellman, signed-state and hybrid
branch-and-bound controls prune substantial families but lose total time to
their shared four-coordinate baseline. The K4/K6 records are single fresh-run
controls, not repeated performance estimates. Their outcome reinforces that
avoided leaves alone are insufficient.
[K4 control](../data/program-family-bound-control-k4.json) ·
[K6 control](../data/program-family-bound-control-k6.json)

**New operating rules.** Cold setup must clear relevant caches; a warmed median
can hide construction cost. Give both algorithms the same algebraic
improvements and the same requested outputs. The compact decision certificate
proves informed values and the two optima; joint feasibility still requires a
scan of the retained response matrix. The cover preserves neither all ties,
full prediction envelopes nor execution-cost Pareto tradeoffs. Historical
timings with different setup protocols must be qualified before comparison.

**Current next gate.** Avoid the remaining `2^K` full no-M suffix seeds with a
certified order that remains valid under suffix extension and the `E M`
boundary. Do not assume four-coordinate closure through M. Compare against the
accepted implementation including checking cost; retain an obstruction if no
net gain survives. Preparation enumeration `2^h` remains explicitly open and
does not become a second active experiment in this step.
[Integrated decision](program-family-integration.md)
