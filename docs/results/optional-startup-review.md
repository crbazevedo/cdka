# Independent review: optional startup and diagnostic content

**15 November 2026, Europe/Lisbon.** The bounded physical extension resolves
the missing comparator in SB. A program that never reads a diagnostic record
may decline the initial acquisition while keeping the same gross capital,
commissioning, circuit installation and future physical contract. The best
omitted-startup blind program attains the full physical optimum at **22 of
24** fixed price points. The remaining two points have both zero NAND execution
price and zero diagnostic write price. At every price point, the strongest
zero-enable-NAND subfamily attains the full optimum.

Evidence: [complete scan](../data/optional-startup-results.json),
[independent oracle](../../experiments/optional_startup_independent.py),
[independent exact certificates](../data/optional-startup-independent.json),
[preparation implementation](../../cdka/optional_startup.py),
[channel intervention](../../cdka/diagnostic_ablation.py), and
[formal distinctions](optional-startup-formal.md). Exact fractions and full
response hashes are in the machine-readable records; displayed decimals are
only for inspection.

## Provenance and preserved scope

The parent is PR12 head
`24d1e35ecde75defd495b5272bfb653f427bf528`; main remains
`c8eb621acf04c6581795662596c3c41cf2cac43c`. Read-only GitHub review inspected
the pull-request collection, all six branch heads, and the complete recursive
trees of main and the adjacent verification branches. The relevant heads were:

| Line | Inspected commit | Scope |
|---|---|---|
| PR13 | `692f70390cac9fbf401f050a9a4878663bb07dec` | Competitive continuation certificates |
| v20 | `bac94c00eb70babfc5ffeb89d0666e88eb4b4013` | Coupled verification |
| PR14 | `ff367d41c678b1ae5846c18542e7de9bb2ae5134` | Regenerative exposure |
| PR15 | `df7505c27f2c8e89c94e592b1c0f8e7131799518` | Certified algorithm selection |

None of those trees contained the SB or optional-startup implementation. Their
inherited recurrent, selective-acquisition and memory-renewal source blobs
were identical to main. Their exogenous-context, rank and reset assumptions
therefore supply no additional physical observation or advantage here.

The present extension preserves the plant probabilities, fixed 24-price grid,
initial health prior one half, gross capital 96, commissioning 24, six-gate
task/selection bank, trusted interfaces and all failed-prefix charges. The
inherited SB physical compiler and data remain unchanged. The two endpoints
are still seven complete cycles followed by the eighth terminal task, and
eight complete cycles. A terminal task uniformly stops before enable/write,
wear and harvest for every program.

## What the finite search covers

There are 336 original paid representatives and 84 new omitted-startup blind
representatives at each price: **420 physical candidates**, covering 1,280
raw preparation/program pairs. Omission is permitted only when both installed
maintenance bins choose from `skip` and `service`. All 21 enable cost/profile
classes remain available; these read only the executed-service and entry-bin
signals, never the record.

This syntactic restriction makes an uninitialized register safe without
adding a hidden validity sensor or a free diagnostic word. The evaluator's
dummy record labels have no physical informational meaning. For every blind
policy, projecting to hidden health and balance preserves future survival,
costs, failures, service, writes and resource transitions. Even a later paid
acquisition is unread by this family, so its probabilities sum out of the
projected kernel. Records that differ can still differ as stored physical
words; the claim concerns responses available to this controller.

The search does not cover a broader optional-startup controller that starts
without a record, later acquires one and then permits its first read. It also
does not add a clock, finer resource bins, arbitrary history, randomization or
other control hardware. The omitted family is complete under the declared
blind syntax; it is not every imaginable admissible optional preparation.

The strongest blind reference includes **both** its 84 paid and 84 omitted
members. The no-enable-NAND reference includes all direct outputs `0, 1, r, x`
with all admissible preparation/maintenance combinations. Always-FRESH,
never-renew and no-maintenance references are optimized within the same
physical union. These are complete-program comparisons at common gross
endowment, not comparisons at an artificially equal post-preparation balance.

## Independent physical enumeration

The independent oracle imports neither the SB compiler nor the new preparation
or ablation evaluators. It enumerates task sensor errors and NAND output faults
directly, runs the declared wiring including reused wires, and propagates an
exact rational law on `(hidden health, balance)`. It retains the shared hidden
health through actual service, work and enable, with fresh conditional flags.
Its row cost includes unsuccessful procedure, task and later resource stops.

All **4,032** omitted-startup survival/spending pairs were independently
evaluated: 84 programs times 24 prices times two endpoints. The certificate
contains 48 complete-response hashes, with lexical base program identifiers
and exact fractions. The production scan checks every hash against this
certificate. Its 48 paid-response hashes are also checked against the frozen
SB scan. Agreement therefore covers every candidate response in the physical
union, not merely the selected winners.

The final review checked all 24 source-bound checkpoints and the completed
52,416-response record. All 48 original-paid response hashes and all 48
independent-omission hashes agree; the source and input-data SHA-256 bindings
also agree. Across both endpoints, the scan checks 8,064 paid-blind channel
comparisons: survival, every spending stage, failures, gate/write/service
counts, resources and progress curves remain identical under initial-only
and all-report ablation. These checks preserve the intended intervention
boundary instead of assuming it from the program's name.

The independent certificate was generated normally and reproduced with
assertions and site initialization disabled:

```sh
python -m experiments.optional_startup_independent --write
python -S -O -m experiments.optional_startup_independent --check
```

The new preparation tests separately inspect raw initial report laws,
unaffordable startup prefixes, arbitrary unread register contents, short raw
trajectories and terminal fairness. The intervention tests check complete-word
marginals, replacement at renewal and unchanged same-epoch rewards. These
controls supplement the complete response comparison; they do not establish
a claim about unmodelled hardware.

## Physical result and the remaining positive information case

At every price, the best omitted blind representative is
`service/service + RETAIN`. It pays no initial write and never requests a later
one. It executes no maintenance voter or enable NAND. Its eight-task survival
is independent of the unused write and enable-installation prices:

| NAND execution price | Omitted blind survival | Expected incurred spending |
|---:|---:|---:|
| 0 | 0.9115317652171799 | 392.0429783536903 |
| 1 | 0.8843750584753485 | 382.60032160588895 |
| 2 | 0.8714799680489522 | 381.4147169935532 |

It attains the full optimum at 22 points, including all 16 positive-NAND-price
points. At zero write price an equivalent paid lexical representative can be
selected by a tie break; this does not mean the unused report has decision
value. The omitted blind program is an available optimum with the same
survival/spending pair.

The old free-NAND, write-price-six enable gains remain valid in their original
mandatory-preparation family. They no longer beat the strengthened comparator:
the omitted blind value is about 0.911532, above their approximately 0.888658
and 0.887556 primary values. This is a changed feasible preparation family,
not a correction of the earlier exact arithmetic. No prices were selected
after observing the result.

Maximum survival does not describe the entire cost frontier. At free execution
and free installation, some declared survival-loss tolerances select enable
circuits: for example, `gate = write = setup = 0` selects `vote/vote:e13` at
tolerance 0.001 and `vote/vote:e17` at tolerance 0.01. With `gate = setup = 0`
and write price six, the tolerance-0.01 winner is omitted blind
`service/service:e05`, with survival about 0.904929 and incurred spending about
390.734 versus the maximum-survival blind reference's 0.911532 and 392.043.
These are explicit survival/spending tradeoffs. They do not contradict the
maximum-survival finding, and must not be deleted to support a global claim
against every circuit.

At all 16 positive-execution-price points, all four declared cost-tolerance
winners use zero enable NANDs in each endpoint: 64 such comparisons per
endpoint. All five free-price exceptions are retained in both endpoint
records, including the same `e05` tradeoff at write prices 12 and 24.
This is a claim about the specified tolerances, not every
point on the full finite frontier.

At `gate = write = 0`, `vote/vote + FRESH` has survival
0.9174767896493894, above the blind optimum by
0.00594502443220947, or about **0.594502 percentage points**. Both setup prices
give the same result because this program uses no enable NAND. Sensor and
gate faults remain present; only the two specified prices are zero.

## Separate causal estimands

Two analytical interventions preserve debit order, prices and all other
physical transitions. The first replaces only the initial joint
health/report law by the product of its two marginals. The second replaces
the initial report and every later acquired report by the same fixed
prior-predictive whole-word law, independently of the actual source health.
Within-word dependence is preserved. Three independent fair bits would define
a different intervention.

The latter's renewal marginal is frozen at the declared prior, not recalibrated
to the endogenous population of surviving machines. Consequently it is not a
claim that every later report marginal matches the original trajectory. Both
controls are causal interventions, not executable alternative sensors or a
free source of randomness. Bank faults still depend on hidden health, and
task sensors remain active.

At the positive free-price case, the physical winning program's survival
falls from 0.9174767896493894 to 0.9071546660505188 after initial-only ablation,
and to 0.8853791662882591 after all-report ablation. These are **fixed-program**
effects of approximately 1.032212 and 3.209762 percentage points. Reoptimizing
the full comparison world, including omitted blind candidates, gives
0.9115317652171799 in each ablation. The resulting optimized effect is the
smaller 0.594502-point gap. Reporting the fixed-program loss as the optimized
value of information would overstate the result.

The complete scan confirms that both reoptimized channel effects are exactly
zero at the other 22 points, for both endpoints. There are no negative
reoptimized channel effects on this grid. This finite sign pattern is a
result, not a general information-monotonicity assumption.

No general theorem says a specified information channel improves every
controller, and a physical-family gap alone does not isolate content from
resource changes. The matched-cost interventions and the preparation union
answer these separate questions. The broader physical conclusion is bounded:
the diagnostic mechanism supplies no extra optimal survival at the 22 other
declared points, although diagnostic content can still change a suboptimal
program's outcome.

## Resource phase is not diagnostic content

A sharp negative control occurs at `gate = 0`, `write = 6`, with either setup
price. Keep the blind maintenance policy `service/service` and direct enable
`r` (`e02`) fixed. Paid startup gives eight-task survival
0.8863706416129852; omitting startup gives zero.

Omission starts at balance 72. The program immediately services for 48 and
performs its task for 24, after which its mandatory six-quanta write is
unaffordable. Paid startup starts at 66, so the first service is skipped and
the later resource phase differs. The record is never read in either case.
This is a scheduling consequence of the coarse controller and explicit
affordability protocol, not a benefit from diagnostic content.

The enlarged optimum cannot worsen because the paid candidates remain in
the union. That set-inclusion fact does not imply that removing an expense
improves every fixed program. Here a different omitted blind program,
`service/service + RETAIN`, achieves 0.9115317652171799 and avoids the
unaffordable write. Retaining the paid option is therefore essential to a
sound optional-preparation comparison.

## Decision supported by the review

The startup obligation closes within the fixed grammar and grid. The earlier
positive-price negative result strengthens, and a genuine diagnostic-content
effect remains as a separately scoped free-price control. These results do
not justify additional enable circuits, a favorable-price search, a global
frontier-domination claim or a universal assertion that diagnosis is useless.
Further work must identify the missing decision requirement and its physically
readable information before enlarging the controller family or the plant.
The next bounded obligation is an offline validity audit of the existing
16-table, 21-channel grammar: determine which originally nonblind programs
can omit startup while guaranteeing that their first actual record read
occurs only after a successful physical acquisition. A validity coordinate
used by that proof is not a new bit made available to the installed
controller. This addresses the declared deferred-first-read exclusion
without changing prices, task physics or the controller's observation access.
