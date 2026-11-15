# Optional preparation and causal diagnostic content

## Declared comparison

This note concerns the unchanged [shared-budget plant and event order](../strategy/shared-budget-contract.md),
the fixed 24 price points and the two horizon-eight endpoints. Its only physical
extension is the right of an installed blind maintenance table to omit its
initial diagnostic acquisition. The original mandatory-preparation experiment
remains a valid, narrower experiment and its response data remain unchanged.

Let a complete program contain a maintenance table, an enable circuit and a
preparation choice. The physical family contains all 336 original paid
cost/profile representatives and 84 omitted-preparation representatives whose
two maintenance modes belong to `{skip, service}`. These 420 representatives
cover 1,280 rooted raw preparation/program combinations. An omitted preparation
does not install diagnostic cells with known values or provide a correlated
record for free. Both entries of its maintenance table are forbidden from
reading that record, including entries that happen to be unreachable in a
particular run.

The physical response is evaluated separately from two analytical interventions:

| Treatment | Startup payment | Initial report | Later acquired reports |
|---|---|---|---|
| Paid informative | Commissioning, setup and write | Original diagnostic channel | Original diagnostic channel |
| Omitted blind | Commissioning and setup | No diagnostic acquisition | Original channel when requested and funded; never read by the blind table |
| Initial-only null | Same as paid informative | Independent prior-marginal report | Original diagnostic channel |
| All-report null | Same as paid informative | Independent prior-marginal report | Same frozen prior-marginal law at every requested, funded acquisition |

The null treatments are counterfactual channel controls. They are not extra
physical candidates, installed random sources or changes to the prices.
No root NAND, sensing error, restoration rate, degradation rate or service
failure rate is improved by either intervention.

## 1. An unread register can be removed from the blind evaluator

Write a physical epoch state as \(s=(z,d,b)\), where \(z\) is hidden bank health,
\(d\) is the stored word and \(b\) is the resource balance. Let
\(\rho(s)=(z,b)\). For a blind maintenance table and every admitted enable
circuit, the one-step law projected by \(\rho\) and every same-step reward are
independent of \(d\).

The proof follows the actual causal order. The entry bin selects `skip` or
`service` without a diagnostic voter. The affordability guard uses only the
balance and requested service. Procedure failure, restoration and task
correctness depend on the actual service and hidden health. The enable circuit
reads only the actual service bit, frozen entry-bin signal and constants;
its fault flags depend on post-service health. Affordability, debit, wear,
harvest and spill use the same health/resource branch. A renewed or retained
word cannot affect any of these operations in the current step. The next
blind step again ignores that word.

Consequently there is a projected kernel \(\overline K\) such that

\[
 \sum_{s':\rho(s')=y}K((z,d,b),s')=\overline K((z,b),y),
\]

and the incurred-cost, failure, write, gate, service, harvest and spill reward
vectors factor through \(\rho\). The common terminal-task kernel has the same
property. Induction proves equality of all finite projected trajectories and
their accumulated rewards for any two initial laws with the same \((z,b)\)
marginal, regardless of how their unused register contents depend on health.

This establishes three consequences.

1. A dummy register coordinate in the omitted-preparation evaluator represents
   an equivalence class of unread physical states. It is not an initialized
   physical word or a free observation.
2. Paid informative, initial-only-null and all-report-null responses coincide
   exactly for every blind program at the same prepared balance. Their costs
   coincide as well, including costs on failed prefixes.
3. The blind evaluator can use at most the 194 health/balance labels of the
   capacity-96 model. This is a valid projection, not a minimality theorem.

Later acquisition remains a real, paid operation even when its output is
irrelevant to that blind program. A noisy or fixed enable can therefore waste
resources or terminate an otherwise successful work cycle by requesting an
unaffordable write. Blindness does not authorize removing those operations.

## 2. Exact initial-content effect at a matched resource state

Let \(\pi_z\) be the fixed initial health prior, \(P_z(d)\) the original
diagnostic-word channel, and

\[
 m(d)=\pi_0P_0(d)+\pi_1P_1(d).
\]

At the common paid prepared balance \(b\), the informative and null laws are

\[
 \alpha(z,d,b)=\pi_zP_z(d),\qquad
 \beta(z,d,b)=\pi_zm(d).
\]

This preserves both the health marginal and the entire diagnostic-word
marginal while removing their initial dependence. It is essential to preserve
the full word distribution. With the fixed fair health prior and diagnostic
error \(3/20\), each individual bit is fair but
\(m(000)=247/800\), whereas three independent fair bits would give \(1/8\).
The latter would be a different intervention.

For any exact unchanged continuation response \(v(z,d,b)\), the initial-content
effect is

\[
 (\alpha-\beta)v
 =\pi_0\pi_1\sum_d
   [P_0(d)-P_1(d)]\,[v(0,d,b)-v(1,d,b)].
\]

This identity follows by expanding the two mixture terms for each health.
It applies to survival, incurred cost or any other linear expectation over
the same continuation. It is an exact contrast of conditional responses,
not a comparison between different resource balances. If startup fails,
both matched-cost treatments fail at the same stage and have the same charges;
their content effect is zero.

For a blind continuation, \(v(z,d,b)\) is independent of \(d\). Since both
\(P_0\) and \(P_1\) sum to one, the initial-content effect vanishes exactly.
For a diagnostic-reading continuation, its sign must be evaluated. A record
with a useful correlation can still be routed through an ineffective policy.

The initial-only control does not measure the total contribution of all
diagnoses: subsequent requested reports are still generated by the original
informative channel.

## 3. The all-report intervention and its boundary

The all-report null replaces \(P_h(d)\) by the same frozen \(m(d)\) at every
successful paid acquisition. It does so after conditioning on the actual
service, work, enable and affordability outcomes. The replacement report is
independent of that branch's actual bank health. Retention remains retention.
The final task kernel is unchanged because that endpoint ends before another
acquisition.

For a fixed incoming state, no operation following the new report in that
epoch reads it. Therefore every same-step reward is unchanged. The successor
joint health/resource mass is unchanged as well. Only its coupling to the
new diagnostic word changes. In the implementation, summing out the original
report and redistributing the renewed mass after health drift is equivalent
to replacing the report before drift: drift depends on health, not on that
new word. Keeping the full joint successor health/resource mass is necessary;
independently replacing either marginal would change the plant.

The fixed prior is not recomputed from the current population of surviving
machines, a policy-conditioned history or hidden health. Consequently this
control preserves the original startup report marginal, but need not preserve
the endogenous report marginal at later acquisitions. Its exact description
is a **fixed-prior-marginal channel ablation with matched costs and event
order**.

The intervention does not remove every possible health-correlated signal.
Actual health still affects computation through the faulty NAND bank. For
example, averaging a `vote` request over the null word distribution yields

\[
 \Pr(r_{\rm requested}=1\mid z=0)
 =\frac{25102153867357447}{50000000000000000}
 \approx0.5020430773471489,
\]

\[
 \Pr(r_{\rm requested}=1\mid z=1)
 =\frac{262193521}{488281250}
 \approx0.536972331008.
\]

The physical task readings also remain available for actual task computation.
Thus “null diagnostic channel” does not mean “a machine with no information”
or “a completely health-independent action law.”

## 4. Continuation identities for fixed programs

Fix a paid program. Let \(K\) be its informative ordinary-cycle kernel and
\(N\) its all-report-null kernel. Let \(\alpha\) and \(\beta\) be the matched
paid initial laws above. All kernels are substochastic; no survival
normalization is used.

For the cycle endpoint use \(n=H\) and \(g=\mathbf1\). For the task endpoint
with \(H\ge1\), use \(n=H-1\) and \(g=K_{\rm task}\mathbf1\), where the
terminal task kernel is common to both channels. Then

\[
 V_I=\alpha K^ng,\qquad V_N=\beta N^ng,
\]

and

\[
 V_I-V_N
 =(\alpha-\beta)K^ng
 +\beta\sum_{j=0}^{n-1}N^j(K-N)K^{n-1-j}g.
\]

The first term is the initial-only content effect under the unchanged
informative continuation. The second propagates later channel changes through
the null outer prefixes and informative remaining responses. Either term may
have a sign that differs from the complete comparison. Equal immediate
health/resource projections do not imply equal continued values once a
future maintenance voter reads the new word.

For incurred cost, let \(c\) be the common ordinary-cycle cost vector and
\(b_c\) the common boundary cost: zero for the cycle endpoint, terminal-task
cost for the task endpoint. Define

\[
 u_0=b_c,\qquad u_{j+1}=c+Ku_j.
\]

With common startup spend \(a\), the informative total is \(a+\alpha u_n\).
Define the null cost response analogously with \(N\). Their exact difference
is

\[
 C_I-C_N
 =(\alpha-\beta)u_n
 +\beta\sum_{j=0}^{n-1}N^j(K-N)u_{n-1-j}.
\]

There is no one-step cost difference in this channel intervention. Accumulated
spend can nevertheless differ because changed reports change future actions,
failure risk and the probability of reaching later purchases. Every reward
already includes charges on branches that subsequently fail. At \(H=0\),
compare only the paid preparation law and startup charges directly.

## 5. Reoptimization is a separate estimand

Let \(\mathcal B\) contain all blind programs with paid or omitted preparation.
Let \(\mathcal P\) contain the original paid informative programs plus the
omitted blind programs. Let \(\mathcal N\) be the analytical family obtained
by replacing every paid program's diagnostic channel with the all-report
null, while keeping the same omitted blind alternatives.

Define \(V_B^*\), \(V_P^*\) and \(V_N^*\) as the maximum survival in these
families. Costs are used only for the declared exact tie break or explicit
survival-loss tolerance. Because the blind responses coincide under matched
channels and \(\mathcal B\) is available in both comparisons,

\[
 V_P^*\ge V_B^*,\qquad V_N^*\ge V_B^*.
\]

The physical opportunity gap \(V_P^*-V_B^*\) measures the value of allowing
the whole original diagnostic-reading program family against its strongest
blind physical reference. By itself it does not isolate sensor content:
the larger family also contains noisy voting and different resource usage.

The reoptimized channel effect \(V_P^*-V_N^*\) isolates the specified report
intervention across the same decision grammar and resource contract. There
is no general theorem here that this difference is nonnegative. The finite
grammar does not include every free garbling or randomized controller that
would support an unrestricted information-order argument. Its sign is an
exact result of the declared experiment.

For selected maximizers \(p_P\) and \(p_N\), the reoptimized difference can
also be written

\[
 V_P^*-V_N^*
 =[V_P(p_P)-V_N(p_P)]
 -[V_N(p_N)-V_N(p_P)].
\]

The first bracket measures the fixed informative winner's sensitivity to the
channel intervention. The second is the benefit of adapting the program to
that intervention. Reporting only the first bracket can overstate the value
remaining after the comparator is allowed to reoptimize.

## 6. Omission changes resources and can harm a fixed program

Omission changes a successfully prepared balance from \(72-ki-w\) to
\(72-ki\). It also removes the initial write charge. This is a physical
preparation change, not the matched-balance information intervention above.
Because the installed controller uses coarse balance bins, changing its
initial balance can change the maintenance phase and later affordability.

An exact counterexample uses \((g,w,i)=(0,6,0)\), blind
`service/service`, and the zero-NAND enable output `r` (actual service).
Paid preparation starts at balance 66, so the first maintenance is forced
skip; its eight-task survival is approximately 0.8863706416129852. Omitted
preparation starts at 72. It executes service for 48 and work for 24. If
those operations succeed, enable `r=1` requests a six-quantum write from
balance zero. That write fails before any harvest. Hence the omitted
program's eight-task survival is exactly zero; its incurred spend is
\(95.88\) in expectation, including commissioning and procedure failures.

This is a failure of that fixed program's use of additional initial resource.
It is not a proof that more resources harm an unrestricted optimal controller.
Keeping both paid and omitted preparations ensures the enlarged physical
family never loses the old optimum. Forcing every blind program to omit
preparation would remove legitimate resource-phase alternatives and would
not implement the stated optional-preparation contract.

## Executable evidence

The implementation is additive: [optional initialization and propagation](../../cdka/optional_startup.py)
leave [the shared-budget kernel](../../cdka/shared_budget.py) unchanged;
[the all-report intervention](../../cdka/diagnostic_ablation.py) supplies its
own separately named kernel. [The complete scan](../../experiments/optional_startup_sweep.py)
reoptimizes the physical and counterfactual families on the inherited grid.
[Independent blind enumeration](../../experiments/optional_startup_independent.py)
uses direct physical flags and a health/resource evaluator.

[Ten channel checks](../../tests/test_diagnostic_ablation.py) compare null
rows against an independent primitive-event oracle, verify unchanged
same-state rewards and projected health/resource law, preserve retention and
the terminal endpoint, establish blind invariance, and recover exact equality
when the original diagnostic error is one half. They also retain the explicit
health-correlated-computation control above, and independently check both
initial and continued response identities for survival and incurred cost.
The full exact response data and
their source hashes are in [the optional-startup scan](../data/optional-startup-results.json).

These results concern a bounded physical family and a declared analytical
intervention. They do not establish universal uselessness of diagnosis,
minimality of a representation, energy calibration or a novel general theory
of information value.
