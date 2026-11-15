# Independent review: one pathwise budget and the use of diagnosis

**15 November 2026, UTC.** The bounded synthesis is internally consistent with
the declared physical contract. Its strongest result is negative for the
proposed information mechanism: **at all 16 points with positive NAND execution
price, a controller that never reads the stored diagnosis attains the maximum
survival.** The mandatory initial acquisition remains paid in this comparison.

Evidence: [physical implementation](../../cdka/shared_budget.py),
[independent physical tests](../../tests/test_shared_budget.py),
[complete synthesis](../../experiments/shared_budget_sweep.py),
[exact synthesis record](../data/shared-budget-results.json), and
[causal-use and continuation controls](../data/shared-budget-controls.json).
Exact fractions belong to those records; decimals below are for inspection.

## Provenance and independence

The inherited physical source is main
`c8eb621acf04c6581795662596c3c41cf2cac43c` (v18). This thread resumes from
PR12 head `e54de20fedd50358ad75328c336ce07e8492283b`, which integrated that
physical source with the audited manuscript. The earlier source audit also
inspected PR13 `692f70390cac9fbf401f050a9a4878663bb07dec`, PR14
`ff367d41c678b1ae5846c18542e7de9bb2ae5134`, and PR15
`df7505c27f2c8e89c94e592b1c0f8e7131799518`. Their verification and numerical
advances did not implement the common physical budget: the inherited recurrent,
selective-acquisition, and memory-renewal sources were unchanged. The new
records retain source SHA-256 bindings for this increment.

The review used three distinct checks: an independent event oracle for the
physics; inspection of the complete enumeration and all 24 completed,
source-matching price checkpoints; and a separate exact enumeration of the
blind-controller subfamily. Computational verification results on the later
branches provide no physical advantage for this experiment by themselves.

## Physical checks

The new test oracle directly enumerates six-NAND selector and task fault
flags, task-sensor errors, enable-circuit faults with shared-wire fanout, and
diagnostic-cell errors. It does not call the new compiler's event enumerator,
row builder, or optimized scalar probability helpers as its reference. Hidden
bank health remains shared through the actual service outcome; fault flags are
fresh at each invocation conditional on that health.

The ten tests cover:

- All 64 rooted zero-, one-, and two-NAND netlists, independently reduced to
  the same 21 gate-count/noise-profile classes; all 16 maintenance tables.
- Sixteen ordinary/terminal physical rows at affordability and fault
  boundaries, including failed paths and their incurred charges.
- Two independently propagated three-task/cycle runs, with exact survival,
  failure causes, resource balances, spending, harvesting, spill, writes,
  service counts, and NAND invocation counts.
- Startup at all 24 price points for every one of the 21 enable classes,
  including the initial report charge and an explicit failed-setup prefix.
- Zero-price FRESH agreement with both inherited v16 and v18 survival through
  three tasks/cycles for every maintenance table and both endpoint conventions.
- Frozen entry-bin inputs, the service-reservation boundary, no hypothetical
  write reservation, final-task fairness, and charges on failed prefixes.

A clean shared-cause counterexample gives expected write counts `5/8` with
shared hidden health and `9/16` after replacing enable noise by an averaged
independent rate. Another control rejects reuse of the same fault flags for
selection and task execution. These are exact causal-law checks, not measured
improvements in hardware.

All ten tests passed in normal Python, with `-O`, and with `-S -O`:

```sh
python -m unittest discover -s tests -p test_shared_budget.py -v
python -O -m unittest discover -s tests -p test_shared_budget.py -v
python -S -O -m unittest discover -s tests -p test_shared_budget.py -v
```

Execution times observed during this review are test diagnostics, not a
computational benchmark or a claim of evaluator speedup.

## Coverage, references, and endpoint fairness

Each of the 24 frozen price points evaluates 336 distinct cost/profile
programs, representing 1,024 raw complete programs, for each of two endpoints.
The 21-class reduction retains the full enable fault profile and NAND count;
both matter under shared health, execution prices, and setup prices.

Every reference is optimized over its whole declared subfamily at the same
prices, initial endowment, and endpoint. In particular, `no_enable_nand`
includes all four allowed direct outputs—zero, one, executed service, and the
entry-bin bit—combined with all 16 maintenance tables. It is stronger than
using always-FRESH alone. The no-maintenance reference likewise chooses among
all permitted enable circuits.

The primary objective is **seven complete cycles followed by the eighth task**.
No program pays for an unused terminal enable, write, wear step, or harvest.
The secondary objective completes all eight cycles. Intermediate enable/write
resource failure remains absorbing even after that cycle's task succeeded;
harvest arrives only after cycle completion. These conventions are explicit
and consistently applied. The resulting optimum is over this grammar and
schedule, not over arbitrary ways of completing eight tasks or adding an
unpriced fallback that skips an unaffordable acquisition.

## What the full scan establishes

At all 16 price points with `gate > 0`, an enable NAND provides no improvement
over the strongest zero-enable-NAND subfamily in maximum survival, for either
endpoint. At those points, every selected cost winner at the declared absolute
survival-loss tolerances `0`, `1/10000`, `1/1000`, and `1/100` also uses zero
enable NANDs.

Only two points have a positive maximum-survival gain from an enable NAND:
`(gate, write, setup) = (0, 6, 0)` and `(0, 6, 6)`. Their primary gains over
the strongest zero-enable-NAND reference are respectively
`0.0022874614735214375...` and `0.0011855088304654703...`, or approximately
`0.228746` and `0.118551` percentage points. Both require free NAND execution.
Their primary winner is `e06 = NAND(1, executed_service)`, a noisy complement
of service, rather than the old ELIDE circuit. For the complete-cycle endpoint
the representative winner changes to ELIDE. Endpoint convention therefore
changes the selected circuit even in these favorable points.

The never-renew subfamily attains the primary maximum at 20 of 24 points. Its
best member exceeds always-FRESH at 18 points, ties it at four, and loses at
two. For example, `(gate, write) = (1, 12)` gives survival approximately
`0.8778163` versus `0.7701221`; at `(1, 24)`, always-FRESH cannot complete the
first required cycle while the never-renew maximum is approximately
`0.8565415`. This last gap reflects an explicit affordability failure, not a
small accuracy improvement.

The cost frontier is a valid finite frontier of **unconditional expected
incurred spending and survival**. It includes failed-prefix costs and uses
exact rational comparisons. Some paid-gate programs remain on much
lower-survival portions of that frontier. The data therefore do not establish
global cost domination of every paid-gate program. Cheap early stopping must
not be described as efficiency, and a favorable ELIDE-versus-FRESH comparison
under one fixed maintenance policy must not replace the stronger optimized
reference in the whole-library claim.

## Independent blind-controller enumeration

The review separately evaluated all four maintenance tables drawn from
`{skip, service}` in both resource bins, combined with all 21 enable classes,
at all 24 price points: **2,016 exact eight-task evaluations**. The best blind
representative at every point is

```python
policy = Policy('service', 'service')
enable = RETAIN
```

It attains the full-library maximum at 20 points, including all 16 points with
positive NAND execution price. The exact controls retain this representative
at every price and verify its equality to the global maximum for both
endpoints. The four primary gaps are:

| Gate price | Write price | Setup price | Global maximum minus best blind survival |
|---:|---:|---:|---:|
| 0 | 0 | 0 or 6 | `0.00594502443220947...` |
| 0 | 6 | 0 | `0.0022874614735214375...` |
| 0 | 6 | 6 | `0.0011855088304654703...` |

Its diagnostic-selection invocation count is exactly zero, its enable
invocation count is exactly zero, and its write count is exactly one—the
mandatory startup report. Task sensors and the task's six NANDs remain active.

A lexical representative such as `service/inverse:e00` can obscure this
result. Its full-balance inverse branch is unreachable on the relevant live
paths. It has the same physical behavior and value as the blind representative;
the retained record is never read. For example, the ordinary live-balance path
at gate/write prices `(1, 6)` is
`66, 84, 54, 72, 90, 60, 78, 48, 66`. The primary endpoint stops the last task
before its harvest; the controls record that terminal step separately.

Thus these positive-price optima establish the sufficiency of a resource-only
service rule within the declared experiment. They do not establish operational
value for the diagnosis that the inherited startup acquired. The separate
[continuation analysis](shared-budget-continuation.md) retains reachable
counterexamples to transferring the old omission certificate, with startup,
failure spending, and finite-horizon limits explicit.

## Decision after the evidence

The common-budget gate can close with this bounded negative result and its
exact controls. The next physical obligation is to permit a blind program to
decline the initial diagnostic acquisition, charge the resulting startup
correctly, and resynthesize under that explicit startup choice before making
a renewed claim about the value of operational information. The altered
initial balance can change later maintenance timing, so the present optimum
must be recomputed under that extension. Preserve the present price grid and
adverse cases; changing prices to obtain a preferred gate winner would not
resolve the missing information-value comparison.
