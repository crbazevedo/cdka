# Continuation residuals after a resource transition changes

**Scope:** exact finite kernels, declared finite horizon, raw live probability,
and incurred cost including failed prefixes. The optional all-horizon result
below is response equality after verified invariant-space stabilization. It is
not an infinite-horizon cost order or a physical implementation certificate.

Implementation: [budget_continuation.py](../../cdka/budget_continuation.py).
Independent checks: [test_budget_continuation.py](../../tests/test_budget_continuation.py).

## The contract that must precede the algebra

The [v18 acquisition result](T4S-priced-selective-acquisition.md) used a second
expected acquisition ledger. Its ideal omission did not return tokens to the
physical actuator balance. Its identities `D1=DQ=DT=0` therefore cannot be
transferred to a resource-refund model without rebuilding the joint kernel.
The refund control already changes the next affordable maintenance actions.

The new physical compiler must include resource balance, physical records,
persistent hidden causes, and any controller memory or program stage that
affects continuation. Installation and startup consume the same initial
resource capital across complete programs. Each path must pay each charge
before executing the operation it purchases. Shared selector gates and reused
noisy outputs retain their joint law; the controller receives only its declared
observations. A guarded failure has explicit semantics and remains in the
probability accounting.

The residual checker consumes that compiled law. It does not establish these
physical obligations. This distinction is the same as the distinction between
task response closure and realizable observation-dependent selection in the
[core manuscript](../articles/core_interfaces.md).

## Exact finite identity

Use row laws and column responses. Let `Q` be the reference substochastic
live-state kernel, `T=Q+D` the candidate, and `c_Q,c_T` their expected immediate
incurred charges. Missing row mass is failure. Charges paid before failure
belong in `c`; they cannot be reconstructed from the surviving row alone.

For a common terminal response `g` and terminal cost `b`, define

\[
v_k=Q^kg,\qquad C_0=b,\qquad C_{k+1}=c_Q+QC_k.
\]

For every finite `n`, with `delta_c=c_T-c_Q`,

\[
T^ng-Q^ng=\sum_{j=0}^{n-1}T^jD v_{n-1-j},
\]

\[
C_{T,n}-C_{Q,n}
=\sum_{j=0}^{n-1}T^j[\delta_c+DC_{n-1-j}].
\]

If terminal responses/costs differ, add `T^n(g_T-g_Q)` and `T^n(b_T-b_Q)`,
respectively. The checker supports these boundary terms explicitly.

**Proof.** The response difference obeys
`Delta_v[n+1]=T Delta_v[n]+D v[n]`. The cost difference obeys
`Delta_C[n+1]=T Delta_C[n]+delta_c+D C[n]`. Unrolling these recurrences proves
the displayed identities, including their boundary terms. The implementation
also computes the direct reference/candidate recurrences and checks equality
with the independently propagated residual differences using exact rationals.

Changed startup laws must remain visible. For initial live laws `mu_Q,mu_T`,
the paired response difference equals

\[
\mu_T\Delta v_n+(\mu_T-\mu_Q)v_n.
\]

The cost difference additionally contains the difference of already incurred
startup charges. A same-state continuation certificate can therefore succeed
while actual paid-startup performance differs. Neither initial law is
normalized by its surviving mass.

## Gate and interpretation

For `k=0,...,H-1`, compute `r_k=Dv_k` and `s_k=delta_c+D C_k`.

| Exact local check | Conclusion through every `n<=H` |
|---|---|
| Common terminal response and every `r_k=0` | Equal responses from every supplied state. |
| Nonnegative terminal response difference and every `r_k>=0` | Candidate response never decreases. |
| Nonpositive terminal cost difference and every `s_k<=0` | Candidate incurred cost never increases. |

Nonnegativity of `T` proves the inequalities. With a common terminal response,
the equality criterion is necessary and sufficient for equal responses from
every state at every horizon through `H`. For only one designated terminal
horizon it is sufficient, not necessary. Cost and response inequality tests are
sufficient, not necessary: propagated residuals can compensate one another.

The audit returns both local certificate flags and exact direct comparison
flags. A failed local certificate triggers inspection of the exact paired
differences; it does not itself establish harmful omission. A statewise witness
also need not be reachable from an allowed preparation. Actual preparation
results are reported separately, including different paid startup laws.

Use the actual task gate before interpreting lower spending as useful. Early
death removes later purchases and can reduce expected cost while reducing the
unconditional probability of completing the required tasks. Conditional
survival normalization discards that loss. No such normalization is performed.

## API and terminal-stage convention

```python
from cdka.budget_continuation import finite_residual_audit, audit_summary

report = finite_residual_audit(
    Q, T, c_Q, c_T, horizon=H - 1,
    terminal=g_Q, candidate_terminal=g_T,
    terminal_cost=b_Q, candidate_terminal_cost=b_T,
    initial=mu_Q, candidate_initial=mu_T,
    initial_cost=setup_Q, candidate_initial_cost=setup_T,
)
compact = audit_summary(report)
```

Sparse kernels are tuples of dictionaries from integer destination indices to
`Fraction` or integer masses. `index_sparse` adapts a closed labelled state
mapping and rejects missing successors. `index_vector` orders labelled reward
vectors, requiring missing entries to be explicitly supplied or defaulted.
Float inputs are rejected.

`horizon` counts ordinary transitions **before** the final response/cost. If
the final physical task omits post-task renewal, use `H-1` ordinary transitions
and set `g` to the final-stage live probability and `b` to its incurred charge.
With no special terminal stage, defaults are `g=1` and `b=0`.

`include_vectors=True` retains all state response, cost, and residual vectors.
The default retains flags, first witnesses, and optional initial-law curves.
`audit_summary` omits vectors and retains only the last initial-law curve entry.
No routine prints or serializes the complete physical matrices automatically.

The supplied state domain must support the claimed continuation. Truncating a
reachable graph and deleting its successors is not an all-state certificate.
A layered finite-horizon construction may be valid for a specified initial
domain, but its artificial terminal boundaries must not be presented as an
invariant physical model.

## Optional exact all-horizon response equality

Let `U` span the reference response space

\[
W_Q=\operatorname{span}\{g,Qg,Q^2g,\ldots\}.
\]

Exact column elimination and image checking establish when this space has
stabilized. Then

\[
DU=0\quad\Longleftrightarrow\quad T^ng=Q^ng\quad\text{for every }n\ge0.
\]

**Proof.** Invariance makes every `Q^k g` a column combination of `U`, so the
finite residual identity gives the forward implication. Conversely, equality
at every horizon gives `D Q^k g=T T^k g-Q^{k+1}g=0` for every `k`.

`all_horizon_equal` returns `equal=True` only after stabilization and zero
residuals. If a dimension cap stops closure without a residual obstruction,
it returns `equal=None`. It does not convert a successful finite-horizon test
into an infinite claim. No analogous general all-horizon cost inequality is
claimed from a linear response basis alone.

## Incremental interface reuse and its limit

Given a verified old invariant interface `U`, the update residual is `D U`.
Closing `span(U,D U)` under `T` yields the smallest new invariant space that
contains the old one. Any such space must contain `DU=TU-QU`, which proves the
minimal-extension claim. The implementation checks old invariance first and
records stabilization, old dimension, seed residual rank, and new dimension.
It does not claim global minimality after discarding old requirements.

The exact linear algebra, residual telescoping, and invariant-space method are
established instruments. The adaptation here is their use at the boundary of
paid startup, failed-prefix spending, resource-dependent continuation, and a
physically compiled selector. A computational advantage remains an empirical
claim requiring the strongest cached baseline and all discovery/checking costs.

## Executable negative controls

Run with only the Python standard library:

```sh
python -S -O -m cdka.budget_continuation
python -S -O -m unittest discover -s tests -p test_budget_continuation.py
```

| Control | Exact outcome | Incorrect inference rejected |
|---|---|---|
| `D1=0` | Two-step survival from state 0 is `1` for Q and `0` for T. | Equal immediate live mass preserves continuation. |
| Immediate saving | One-step cost changes `1 -> 0`; two-step cost changes `2 -> 3`. | The omitted charge equals total savings. |
| Same live kernel | Both kernels have live mass `1/2`; incurred costs are `1/2` and `1`. | Surviving transitions determine failed-prefix spending. |
| Rank-one redirect | Old dimension is 2, update and seed rank are 1, new dimension is N for N=3,4,8,16. | A small residual seed guarantees a small continuation interface. |

The rank control has one absorbing state and a cycle on all other states.
Redirecting one cycle row to the absorbing state makes successive continuation
responses distinguish every position. Every row remains stochastic.

These are algebraic controls, not unified-budget physical simulations. The
tests also compare telescoping with explicit dense finite sums, compare the
paid-startup/terminal-stage audit with independent forward propagation, retain
a failed sufficient cost certificate whose exact cost order succeeds, and
check that unstabilized closure cannot claim all-horizon equality. Test checks
use `unittest` and explicit exceptions, so `python -O` does not remove them.

## Whole-library gate

For complete programs under the same physical endowment and allowed
preparations, a cover must preserve both survival and incurred cost responses.
A representative may replace a program only when the same feasible
representative dominates all required responses on the preparation domain.
Terminal scalar survival dominance alone does not preserve a cost frontier or
longer continuation contexts. An external randomizing selector belongs in the
physical library and its charges before convex combinations become executable.

The physical experiment owns the complete library enumeration, affordability,
shared-resource construction, benchmark, and empirical outcome. This file
supplies the exact audit and its scope controls.

## Physical application: reachable resource-feedback obstruction

The [physical control experiment](../../experiments/shared_budget_controls.py)
applies the audit to `vote/vote`, comparing FRESH with ELIDE under the
[shared-budget compiler](../../cdka/shared_budget.py). The
[exact control record](../data/shared-budget-controls.json) binds the three
implementation source hashes and retains exact rational values. These are two
complete-program pair comparisons, not a claim about the best policy in the
whole library.

Both cases use endowment 96, unit 24, write price 6, setup price 0, and the
same paid fresh startup law at balance 66. The final task stops before enable,
renewal, wear, and harvest. Every horizon from one through eight tasks is
checked both by lazy backward responses/residual telescoping and by the
physical compiler's separate integer forward propagation.

### Ideal enable isolates the budget feedback

The diagnostic control sets gate price 0 and an explicitly decoupled ideal
enable. It does not present this idealized enable as the actual shared-health
hardware. The state `(health=1, first_bit=1, tail_count=2, balance=84)` has
positive probability `0.28633536231641205...` after one ordinary cycle under
both programs. At this common reachable state,

\[
D\mathbf1=0,\qquad Dg_{\rm final}=0,\qquad DQg_{\rm final}=0,
\qquad DQ^2g_{\rm final}=0.2309032280011588\ldots>0.
\]

On executed-service branches that complete the cycle, FRESH leaves balance
54 and ELIDE leaves 60. Both successor balances force a skip immediately.
After the next paid refresh, the respective balances can become 72 and 78.
At balance 72, service plus the ordinary task exhausts the balance and the
reference cannot pay the following write; balance 78 can pay it. The
distinction is therefore exposed by a later ordinary cycle, even though the
immediate live mass and two shorter terminal continuations agree. The witness
fits within five tasks: one reachable prefix cycle, the modified cycle, two
reference continuation cycles, and the final task.

The compiled row and incurred cost at the selected witness are checked against
raw gate-event and report enumeration for both ordinary and terminal kernels.
The local residual is a term of the exact complete-program comparison; it is
not a proposal to switch installed programs halfway through an execution.

### Actual shared-health enable retains the adverse shorter horizon

At gate price 1 with the actual shared-health enable, a negative continuation
residual is already reachable at the initial state `(0,0,0,66)`, whose startup
probability is exactly `0.3070625`. Its three-task residual is
`-0.0019764922505355886...`, despite zero immediate live-mass residual.
The complete three-task ELIDE program also has lower survival and lower
spending. That cheaper short run fails an equal-survival gate. The eight-task
pair reverses the survival ordering, and ELIDE incurs more total spending.

| Physical case | Tasks | ELIDE minus FRESH survival | ELIDE minus FRESH incurred charge |
|---|---:|---:|---:|
| Ideal enable, gate price 0 | 3 | 0 exactly | -2.7061793535 |
| Ideal enable, gate price 0 | 5 | +0.1046008552 | -0.1525735178 |
| Ideal enable, gate price 0 | 8 | +0.1045344384 | +10.7835921259 |
| Shared-health enable, gate price 1 | 3 | -0.0183314247 | -19.0600511494 |
| Shared-health enable, gate price 1 | 4 | +0.4127744223 | +15.9859153530 |
| Shared-health enable, gate price 1 | 8 | +0.3775250841 | +80.8545701813 |

At eight tasks, the ideal-enable survival values are
`0.7843500593905487` and `0.8888844977850047`; the incurred charges are
`286.4362440421368` and `297.21983616799423`. The actual shared-health values
are `0.4457942473134273` and `0.8233193314252591`, with incurred charges
`266.60241796545205` and `347.4569881467451`. Charges can exceed initial
endowment because successful ordinary cycles earn resources; every charge is
still subject to the pathwise affordability rule.

The two cases check 960 and 1,752 reachable state/remaining-horizon contexts,
respectively. Responses query the real full row oracle lazily, so no outgoing
successor is deleted at a truncated boundary. No finite response rank or
all-horizon physical conclusion is reported. The tests additionally exercise
setup price 6, where the candidate's paid initial balance becomes 60 while the
reference starts at 66, and verify both startup terms against forward runs.

Reproduce the exact physical record with:

```sh
python -S -O -m experiments.shared_budget_controls --write
python -S -O -m experiments.shared_budget_controls --check
```

`--check` independently recomputes the scientific bytes and rejects missing or
stale artifacts without overwriting them. Runtime timings appear only in the
console summary and are excluded from the deterministic JSON artifact.

The original v18 equality is therefore unavailable under this changed
resource contract. What replaces it is a finite, auditable comparison with
reachable witnesses and separate survival/cost conclusions. The whole-library
search remains a separate obligation.

## Causal-use control for the retained report

The exact controls also evaluate the single fixed program
`Policy('service','service') + RETAIN` at all 24 frozen price points, for both
eight-task and eight-cycle endpoints. Comparison with the complete-library
[synthesis record](../data/shared-budget-results.json) shows that this same
program attains the global maximum survival and the selected maximum's
incurred cost at **20 of 24 points for each endpoint**. This includes every
point with positive gate price. These comparisons use the frozen exact maxima;
the control itself is not another policy-library search.

Every positive-probability physical branch on this candidate's live prefixes
has zero diagnostic-selection gate invocations. Its mode is determined by
balance alone (`skip` or `service`), the affordability guard determines whether
service executes, and RETAIN never queries the stored report. The record
provides the deterministic live balance/mode/requested-service/executed-service
path and checks the final task separately. Task sensor and task NAND calls
remain active; zero stored-report reads does not mean an absence of sensing or
computation.

The initial diagnostic acquisition remains mandatory and paid. The control
does not remove it, refund its price, or claim that this is the best achievable
architecture after changing the startup grammar. It establishes a narrower
causal fact: these complete continuations do not use the report contents that
the inherited startup purchased. A test intervenes on every stored report
configuration at fixed hidden health and reachable balance 84 and verifies
identical projected health/resource transition law, incurred charges, service
execution and failures for both ordinary and terminal stages.

At the four price points where this fixed blind candidate falls below the
global maximum, the result is recorded as a positive exact gap. Their eight-task
gaps are `0.00594502443220947...` at gate/write prices `(0,0)` for either setup
price, `0.0022874614735214375...` at `(0,6,0)`, and
`0.0011855088304654703...` at `(0,6,6)`. Thus retaining a record and successfully
using a record remain separate claims. A survival optimum attained by this
blind candidate does not demonstrate that the retained diagnosis preserves
useful operational knowledge.
