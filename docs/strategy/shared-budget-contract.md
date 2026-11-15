# One pathwise budget for maintenance, work and acquisition

## Status and scope

`cdka/shared_budget.py` defines a new finite physical contract on top of the
v16 recurrent plant and the v18 bounded acquisition circuits. It does not
reinterpret the v18 expected-workload ledger as physical energy, and it does
not carry the old omission certificate into a changed resource transition.
The scalar resource below is an explicitly assumed, fungible budget measured
in integer quanta. Its prices are experimental parameters, not measurements
of NAND energy, sensor energy or actuator energy.

The inherited plant probabilities remain fixed: healthy/degraded bank output
flip rates `1/1000` and `1/50`, diagnostic error `3/20`, task-sensor error
`1/50`, healthy-bank degradation `1/20`, restoration `4/5`, and service
procedure failure `1/200`. The three stored diagnostic cells retain ideally
when acquisition is disabled. The task's fair world bit and noisy task
readings are drawn anew on every attempted task.

The whole-program class is finite and declared below. An optimum over that
class is not a claim about every resource-aware, clock-aware, randomized or
history-dependent controller.

## Physical state and readable signals

The full state at an epoch boundary is `(z, d, b)`: hidden bank health,
three physical diagnostic bits, and readable resource balance. The exact
evaluator uses the inherited symmetry quotient
`(z, d[0], d[1] + d[2], b)`. This is an evaluator state, not an observation
provided to the controller. For capacity 96 it contains 1,164 labels,
including zero balance. Reachable subsets are normally smaller.

The maintenance routing sees the balance bin. Its selected `vote` or
`inverse` primitive reads the three stored bits through the actual six-NAND
bank. The acquisition circuit receives only the executed-service bit `r`
and an epoch-entry resource signal `x`, along with constants zero and one.
It receives neither hidden health, the restoration outcome, diagnostic
contents, nor internal task or selector fault flags.

With unit `u = 24`, freeze the following bins at **epoch entry**, before
selection or service is charged:

| Entry balance | Maintenance routing | Enable input `x` |
|---|---|---|
| `0 <= b < 72` | forced `skip` | 0 |
| `72 <= b < 96` | program's `at3` mode | 1 |
| `b = 96` | program's `at4` mode | 0 |

These bins agree with the old low/service/full bins at integer multiples of
24. The middle signal is not recomputed after paying the enable gate or any
earlier debit. Subdividing balances into exact-price thresholds would define
a different controller family.

## Shared hardware and its remaining trusted boundary

The same six physical NAND gates are reused sequentially for maintenance
selection, task work and the acquisition-enable computation. A program with
one or two enable NANDs schedules those operations on the existing bank;
it does not receive one or two new independently healthy gates.

Selection uses the bank's entry health `z`. A successful service procedure
may change health to `h`. Task and enable invocations both use that same
post-service hidden health `h`. Each invocation draws fresh gate-fault flags
conditional on health. A circuit fanout reuses one computed noisy wire.
The evaluator must therefore retain `h` through the service, work and enable
branches. Averaging enable noise before those branches changes the joint law.

Reuse of an internal NAND also requires installed input routing, clocking
and an output tap. These are explicitly trusted interfaces in this finite
model. The routing/setup price below accounts for installation in the common
budget; it is not a price for newly added NAND hardware. The inherited
resource guard, input taps, bin decoder and acquisition actuator remain
trusted. This is a bounded physical implementation claim with that boundary,
not a fault model for every piece of control hardware.

## Prices and preparation

`Prices(gate=g, write=w, setup=i)` supplies nonnegative integer prices. The
fixed scale is:

| Quantity | Quanta |
|---|---:|
| Reservoir capacity and gross initial endowment | 96 |
| Initial commissioning | 24 |
| Mandatory non-gate task overhead | 24 |
| Service procedure, when actually executed | 48 |
| Harvest after a completed cycle | 48 |
| Each actually invoked bank NAND | `g` |
| One three-cell diagnostic acquisition and write | `w` |
| Enable routing/setup with `k` NAND operations | `k*i` |

Initialization pays commissioning, then routing/setup, then the initial
diagnostic acquisition. If an operation is unaffordable, initialization stops
before that operation and retains all earlier spend and its remaining
balance. A successfully prepared program starts at
`72 - k*i - w`, with the same fair initial hidden-health prior and a real
diagnostic sample at error `3/20`.

The experiment inherits mandatory fresh preparation. Thus `RETAIN` means
no **renewal** after preparation; it does not mean a blind, unprepared
machine. Allowing programs to omit the initial acquisition would enlarge
the preparation/program class and requires its own comparison. No candidate
receives a free correlated initial report.

## Event order and affordability

Every debit occurs before its associated physical operation. There is no
overdraft, refund, survivor normalization, or credit against future harvest.
The stage order is:

1. Select the maintenance mode from the frozen entry bin. `skip` and
   `service` produce their fixed request without invoking a voter. `vote`
   and `inverse` pay for six NANDs, then compute the request using entry
   health `z`. Inability to fund that actual selector is a resource stop.
2. Apply the trusted affordability guard. Execute a requested service only
   if the **remaining** balance covers `48 + (24 + 6*g)`. Otherwise execute
   `r = 0`. This is a task reservation, not a possible-write reservation.
3. If `r = 1`, pay 48 and run the service procedure. Procedure failure
   stops immediately. A surviving degraded bank restores with probability
   `4/5`; an already healthy bank stays healthy.
4. Pay the mandatory task cost `24 + 6*g` and invoke the task's six-NAND
   computation. Unaffordability stops before task invocation. An incorrect
   task stops after all of that task's costs have been paid.
5. After successful work, pay `k*g` and invoke the actual enable netlist,
   at post-service health `h`. Insufficient balance stops before invocation.
6. If the computed enable bit is one, pay `w` and acquire a fresh report
   about `h`. Insufficient balance stops before acquisition. If the bit is
   zero, retain the physical register and pay no write cost.
7. Apply end-of-cycle health drift. Credit the 48-quanta harvest and clip
   the resulting stored balance at 96. Record any spilled credit.

There is no reservation for a write that may not be requested. In particular,
`RETAIN` does not pay for a hypothetical acquisition, and a noisy enable
may request an unaffordable write and stop. The service guard does not reserve
the later enable cost either: an otherwise affordable service can leave a
program unable to run its mandatory enable. These are explicit failed
protocol branches, retained in the result, rather than silently converted
to retention or supplied with extra resources.

For a completed branch, let `n_s` be six when the maintenance voter was
invoked and zero otherwise. With executed service `r` and enable result `e`,
the resource transition is

\[
b' = \min\{96,\ b - n_s g - 48r - (24 + 6g) - kg - ew + 48\}.
\]

The branch is included only when every earlier stage is fundable and its
physical procedure/work outcomes succeed. Costs on unsuccessful prefixes are
still charged. Harvest is withheld until all mandatory cycle operations
complete, so the full bin remains reachable. Crediting and clipping harvest
before a paid write would produce a different kernel and can make a full
post-write reservoir unreachable; that convention is not used here.

## Task and cycle endpoints

Two endpoints are supported and must not be conflated.

* `objective='cycles'` requires all operations in each of `H` cycles,
  including its selected acquisition/retention phase, to finish.
* `objective='tasks'` uses `H-1` ordinary cycle kernels followed by one
  terminal task kernel. After the last successful task, every candidate
  stops before enable, acquisition, wear and harvest. It keeps the
  post-task balance and post-service health. This endpoint does not erase
  the last correctly completed task because a needless later write would
  have been unaffordable.

Initialization is common to both endpoints, including horizon zero. Expected
task successes may exceed completed cycles because work can succeed before
an enable/write resource stop. Report these quantities separately.

## Complete bounded program family and references

Maintenance retains all 16 pairs of `at3`/`at4` modes from
`{skip, service, vote, inverse}`. The acquisition grammar contains the four
zero-NAND outputs `0, 1, r, x`, all ten rooted one-NAND netlists, and all fifty
rooted two-NAND netlists. Commutative inputs are ordered, and a rooted
netlist has no unused charged NAND. Grouping by the full fault-count output
profile at the same NAND count gives 4 + 5 + 12 = 21 channels. The profiles
are polynomial identities in the error rate, so the grouping remains valid
when the same circuit is evaluated at both hidden-health rates.

The complete declared family therefore has 1,024 raw programs and 336
cost-indexed channel/program representatives. Comparators include the best
of all 16 maintenance policies for unconditional renewal (`FRESH`) and no
renewal (`RETAIN`), and the best zero-enable-NAND program over all four
available outputs. A zero-enable-NAND program can still pay for an actual
maintenance voter. Blind maintenance references use only `skip`/`service`;
they are distinct from the zero-enable-NAND reference.

Setup is charged from the same gross initial endowment for every program.
It changes preparation balance, so a comparison with positive setup costs
must not secretly compare kernels from a common post-setup resource state.

## Predeclared finite experiment and controls

The modest parameter grid is

\[
g\in\{0,1,2\},\qquad w\in\{0,6,12,24\},\qquad i\in\{0,6\}.
\]

It contains 24 price points, each evaluated on the full 336-representative
family at horizon eight. Task completion is the primary endpoint; completed
cycles, all failure causes, actual spend, gate/write/service counts, remaining
balance and spill are also reported. Expected spend is per initial system,
including failed prefixes. A small spend caused by early failure is not an
acquisition advantage.

The scale gives a meaningful granular middle band without claiming empirical
calibration. At `g=1`, a requested voted service and task can be funded in
the middle band when entry balance is at least 84; a one-NAND enable needs
one additional quantum. At `g=2`, those first three operations require the
entire 96-quanta full reservoir. A subsequent positive-cost enable cannot
be funded on that service branch, and the voted-service middle-band branch
is vetoed. This adverse regime is part of the grid, not removed after seeing
the outcome.

Required controls are:

* Zero extra prices reproduce the inherited v16 all-refresh survival for
  every maintenance policy. With independently specified enable noise they
  reproduce the v18 resource transition after scaling balances by 24.
* Shared-health enable faults remain inside the actual restoration/work
  branches. `enable_noise='decoupled'` with an explicitly declared fixed
  rate is a separate comparison contract, including an ideal-enable control.
* Exact raw NAND/sensor event enumeration checks physical row construction;
  state symmetry is checked against full three-bit states.
* Every trace and expected trajectory conserves resources:
  initial endowment plus harvest equals all incurred spend, retained
  resources on both live and stopped branches, and spill.
* The old omission identity is rechecked against the changed resource
  transitions and full continuation responses. Failure of the old identity
  is evidence about its boundary, not evidence that extra resources harm an
  unrestricted optimal controller.

Zero-price **spend** does not reproduce v16's bookkeeping: v16 debits its
common operating slot before a possible service-procedure failure. This
contract pays the task's overhead only when task invocation is reached.
Zero-price survival and live resource transitions agree; failed-prefix
charges intentionally reflect the newly declared event timing.

## Public evaluator interface

`Contract(Prices(gate, write, setup))`, inherited `Policy`, and inherited
`Enable` identify a complete program. `initialize` returns the paid startup
law and charges; `initial_measure` returns just its unnormalized live law.
`compile_kernel(..., terminal=False)` exposes exact sparse rows through
`kernel[state]`, `.transition(state)` and `.row(state)`. The latter includes
expected stage charges and failure causes. `event_traces` retains the
individual causal outcomes and balances; its `raw=True` mode enumerates
primitive flags and fresh report words independently of the optimized
probability profiles, while sharing the documented stage bookkeeping.

`run_exact(..., horizon=8, objective='tasks')` uses sparse integer propagation
under a common exact denominator and returns rational outputs. It keeps the
law unnormalized. The final `remaining` includes resources on stopped
branches, while `balance_distribution` is the live subdistribution only.
The module asserts exact probability-mass and resource conservation. Cached
physical rows ignore the setup price because setup affects only
initialization; `clear_row_caches()` releases the large row cache between
unrelated sweeps.
