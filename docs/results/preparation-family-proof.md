# Exact preparation families and common complete-program decisions

**5 November 2026.** Parent checkpoint
`2f9abfd01b5298de1a1889cc7c57776fa0f86572`; active research branches R11/R14.

This result addresses the preparation side of the declared decision problem.
The [previous suffix cover](suffix-context-proof.md) reduces the complete
continuations. The construction here covers ordinary preparation histories by
retained actual histories and exact convex identities in their task-sufficient
contrast representation. The two covers can then certify one common physical
program without requiring an explicit row for every preparation history.

The theorem is an exact finite-family statement. Its soundness does not imply
small convex hulls, a runtime advantage, or an endogenous physical controller.
Those claims have separate obligations. It preserves the inherited acquisition,
hidden shared causes, D/R/M kernels, observation boundary, mandatory workload
and common reserved resource box.

## 1. The physical boundary and the reduced preparation

Use the inherited four-by-sixteen matrix E=`CONTRAST_BASIS`. After the paid
acquisition, let the source-indexed submeasures satisfy

\[
\mu_1-\mu_0=-x_0 E,\qquad x_0\ge0,\qquad
\operatorname{mass}(\mu_0)=\tfrac12.
\]

The exact ordinary transports satisfy

\[
E K_a=A_a E,\qquad A_a\ge0,\qquad a\in\{D,R\}.
\]

Thus a chronological history u has signature x_u, with

\[
x_{u a}=x_u A_a.
\]

The retained word is extended on the **right** when propagating a preparation.
This is distinct from prepending a letter to a backward continuation response.
Both conventions must agree with the physical chronological word.

For a complete continuation p, let `q(p)=E K_p g`, where the full physical
continuation includes any permitted M before restriction to E. Since the
inherited kernels preserve mass, its source fidelity is

\[
V_x(p)=\tfrac12-xq(p).
\]

The reduced coordinates are signed-contrast coefficients, not probabilities
of four physical states. Equality of their convex combinations proves equality
of the declared task values; it need not identify the full pair of physical
submeasures. No four-coordinate forward maintenance closure is assumed.
[Physical derivation](reachable-interfaces-proof.md) ·
[Reachable domain](reachable-domain-proof.md)

All compared histories have the same ordinary length and the same remaining
continuation grammar and reserved resources. Actual past R counts may differ,
and those physical costs remain separately reported. If spent resources alter
future feasibility, that resource state must be included in the representation
or kept in separate typed families. A contrast-only hull does not establish
coverage across different remaining capability sets.

## 2. An inductive convex cover

Let X_t be the signatures of every legal length-t preparation history, and set
P_t=`conv(X_t)`. Linearity gives exactly

\[
P_0=\{x_0\},\qquad
P_{t+1}=\operatorname{conv}\bigl(P_tA_D\cup P_tA_R\bigr).
\]

Suppose Q_t consists of retained actual history/signature pairs and
`conv(Q_t)=P_t`. Generate only their ordinary children,

\[
C_{t+1}=\{(ua,x_uA_a):(u,x_u)\in Q_t,\ a\in\{D,R\}\}.
\]

Select a nonempty subset Q_(t+1) of these candidates. For **every** generated
candidate c, supply a witness against the final retained subset:

\[
c=\sum_{j\in Q_{t+1}}\alpha_{c,j}x_j,\qquad
\alpha_{c,j}\ge0,\qquad \sum_j\alpha_{c,j}=1.
\tag{1}
\]

**Preparation coverage theorem.** With Q_0 containing the exact acquisition
signature and empty history, identities (1) imply

\[
Q_t\subseteq X_t,\qquad \operatorname{conv}(Q_t)=\operatorname{conv}(X_t)
\]

for every checked level t. Here Q_t in the subset statement refers to its
actual history-labelled signatures; different histories may have equal
signatures, in which case one of them may represent the equality class.

**Proof.** The base is direct. Every generated child is an actual history
extension, so the new retained subset is physically generated. If
`x=sum_j lambda_j x_j` with nonnegative lambda summing to one, then
`x A_a=sum_j lambda_j (x_j A_a)`. Hence the convex hull of all ordinary children
of X_t equals that of C_(t+1). Equation (1) puts every candidate in the convex
hull of the retained subset. The reverse inclusion follows because retained
points are candidates. Induction proves equality. Equivalently, composing
two successive convex witnesses multiplies their nonnegative coefficients
and preserves their sum one. QED.

The checker need not compose and emit a witness for every original history.
The finite local covers prove that such witnesses exist by induction. Emitting
one explicit decomposition for every one of the 2^h histories would reintroduce
an exponential output requirement.

Retained points need not be exactly the geometric vertices, nor a uniquely
minimal list. Keeping an interior point or a numerically uncertain candidate
is sound. Every discard, however, requires the exact convex witness. Numerical
geometry or linear programming may propose supports; the identity and signs
must be reconstructed and verified in exact arithmetic in the original
signature coordinates. Arbitrary pointwise rescaling would change the hull.

### Small support does not imply a small retained family

In four coordinates, each convex witness can be chosen with at most five
nonzero terms. One constructive argument is to append a constant coordinate
one. More than five supported points are linearly dependent in this augmented
space. A dependence supplies coefficients beta with `sum beta=0` and
`sum beta_j x_j=0`. Moving the original positive coefficients along that
dependence until one first reaches zero preserves the represented point,
nonnegativity and sum one. Repeating removes terms until an affinely
independent support of size at most five remains.

This bounds the support of one witness. It does not bound how many actual
histories must be retained, how many numerical membership problems discovery
solves, or the total number of witnesses. A finite-dimensional signature can
have many extreme reachable preparations.

## 3. What the preparation cover preserves

Fix a finite family F of complete executable continuations. For a preparation x,
define the informed benchmark and same-preparation regret by

\[
B_F(x)=\max_{q\in F}V_x(q),\qquad
R_{P_h,F}(p)=\max_{x\in P_h}\bigl(B_F(x)-V_x(p)\bigr).
\]

The benchmark may choose a different complete program for each preparation.
Its choice is an evaluator comparator. The actual common controller does not
receive the history identifier, hidden source or substrate state.

For each fixed complete program p,

\[
\boxed{\min_{x\in P_h}V_x(p)=\min_{x\in Q_h}V_x(p)}
\tag{2}
\]

because V_x(p) is affine in x. The same statement holds for its maximum.
The finite retained set supplies an actual history attaining each extremum.

For regret, keep the oracle and chosen program at the same preparation:

\[
\begin{aligned}
R_{P_h,F}(p)
 &=\max_{x\in P_h}\max_{q\in F}\bigl(V_x(q)-V_x(p)\bigr)\\
 &=\max_{q\in F}\max_{x\in Q_h}\bigl(V_x(q)-V_x(p)\bigr)\\
 &=\max_{x\in Q_h}\bigl(B_F(x)-V_x(p)\bigr).
\end{aligned}
\tag{3}
\]

Each difference for a fixed pair of programs is affine; maxima over a finite
program family commute. That proves (3), without treating B_F itself as
affine. Equations (2) and (3) hold for every fixed complete p, not merely for
the optimizer eventually selected.

They preserve a common minimax-regret optimum, a common maximin-fidelity
optimum, and the existence of a **single** program satisfying

\[
R_{P_h,F}(p)\le\delta,\qquad
\min_{x\in P_h}V_x(p)\ge\phi.
\tag{4}
\]

No physically implemented randomization is added by convexifying the
uncertainty set. The extrema above are attained by retained actual histories.
The continuation remains one program feasible from every preparation in the
declared class.

### Composition with the existing complete-program cover

Let L_K be the entire original continuation library and let F_K be a checked
subset such that every p in L_K is dominated by one f in F_K on the whole
nonnegative contrast cone. Since all preparation signatures and their convex
combinations belong to that cone,

\[
B_{F_K}(x)=B_{L_K}(x)\quad\text{for all }x\in P_h.
\]

A dominating representative cannot increase same-preparation regret or
decrease fidelity. Conversely F_K is a subset of L_K. These two inclusions
establish equality of the common minimax and maximin values and preservation
of joint feasibility. Combining the preparation and program certificates
therefore reduces both axes of the decision table while preserving the
declared common decision.

The two reductions have different certificates. Preparation combinations
describe uncertainty in a task-sufficient representation. Program dominance
always selects an actual executable representative. Neither construction
authorizes replacing the common controller by a mixture of programs or a
history-dependent oracle. [Program-family theorem](program-family-proof.md)

## 4. Compact decisions, queries and attaining witnesses

The output contract may consist of one minimax program and its exact regret,
one maximin program and its exact minimum fidelity, optional joint feasibility,
and sufficient history/program witnesses. The retained preparation cover and
program cover supply the corresponding universal guarantees.

A single attaining history proves a lower bound on a chosen program's regret
or an upper bound on its minimum fidelity. Paired with the appropriate
universal bound, it proves that program's exact worst case. It does **not** by
itself prove that no other common program is better.

For example, to certify a minimax choice p* with value r, it suffices to verify
that its regret never exceeds r on Q_h and, for every candidate p in F_K,
provide an actual retained history and comparator q whose difference
`V_x(q)-V_x(p)` is at least r. The latter comparator need not itself be the
informed optimum; any such difference is a valid lower bound. The complete
coverage of candidates makes the lower bounds global. The choice p* also has
one of these lower witnesses, so its value is attained exactly.

For maximin, verify the selected program's fidelity lower bound on Q_h and
provide, for every candidate, an actual retained history where its fidelity
is no greater than the reported optimum. Joint infeasibility can likewise
use a different violating history and, when needed, comparator for each
candidate. A feasibility witness must pass both inequalities for the same
common program. All supporting checks and certificate bytes remain paid work.

The complete vector of B(x_u) for every original history u is a different,
exponentially large output. It is not part of a compact decision contract.
For an individual query, propagate the supplied history to its exact signature
and evaluate

\[
B(x_u)=\max_{f\in F_K}\left(\tfrac12-x_uq(f)\right).
\]

Reading and propagating a length-h word remains paid query work. If an encoded
signature is supplied instead, the physical reachability or acquisition claim
is a separate input obligation. No constant-time history query is implied.

## 5. Independent verification obligations

A complete public checker must establish the following obligations. A digest
binds supplied data; it cannot establish the physical or mathematical truth
of the data it binds.

1. **Physical boundary.** Bind the declared acquisition, ordinary kernels,
   fixed E, horizon and chronological grammar. Verify the initial contrast,
   known mass offset and full sixteen-coordinate identities `E K_a=A_a E`.
   Establish the nonnegative cone needed to compose with the program cover.
2. **Base and horizon.** Require the exact base history/signature and every
   required level. Reject negative or boolean horizons, missing levels and
   empty retained families, including at zero signature or zero horizon.
3. **Actual children.** Regenerate both legal ordinary children of every
   retained parent in the declared order. Histories and coordinates must be
   derived from those children, rather than trusted as unrelated labels.
4. **Complete cover.** Require one witness for every generated candidate and
   valid, distinct retained indices. Witness references must point to the
   final retained candidates or to a separately checked acyclic decomposition.
   Cyclic references or references to subsequently discarded points are not
   substitutes for a complete proof.
5. **Exact convexity.** Parse canonical exact rationals, reject floats and
   booleans, require valid dimensions and indices, nonnegative coefficients,
   coefficient sum exactly one, and equality in every signature coordinate.
   An empty witness cannot cover even a zero vector: its coefficient sum is
   zero. Do not allow truncated zip operations to erase required coordinates
   or witnesses.
6. **Decision binding.** Verify the continuation cover, ordered program
   identities, response values and compact output contract. Then check all
   required common-decision inequalities and attaining/optimality witnesses.

Checking supplied identities requires neither numerical geometry nor a new
convex-hull search. Discovery may fail to find a true membership relation and
retain an additional point; that affects efficiency. A numerical proposal may
not bypass exact reconstruction or the independent checker. Rejections must
remain explicit when Python assertions are disabled.

At the mathematical level, the preparation cover depends on the acquisition
signature and ordinary transports, not on a particular terminal query. A new
decision may reuse it only after the relevant physical and resource bindings
are checked. The combined certificate must bind the actual continuation
library, terminal event, output contract and any thresholds fixed as part of
that task. Exact per-program extrema also support later threshold queries:
the query evaluates (4) against the verified bounds and need not rebuild the
underlying cover.

### End-to-end implementation corollary

The public [composed checker](../../cdka/preparation_pipeline.py),
`check_task`, starts from the raw D/R/M kernels, terminal readout, initial
source-indexed law, preparation horizon h and ordinary continuation workload K.
It first verifies either existing complete-program cover (`feature8` or
`finite_context8`) and obtains its exact physical program responses. It then
either verifies the [preparation cover](../../cdka/preparation_families.py)
or selects the complete streamed D/R grammar. Finally it builds the bound
decision problem and invokes the
[compact decision checker](../../cdka/preparation_decisions.py).

**Corollary.** Acceptance of this composition establishes the exact worst
same-history regret and minimum fidelity of every returned complete program
over every original length-h preparation. The reported minimax and maximin
choices attain the respective optima over the entire original continuation
library. A joint gate applied to those checked extrema is feasible precisely
when an original common complete program meets both thresholds.

The first stage proves physical program-response correctness and domination
of omitted original programs. The second proves that every original
preparation signature lies in the retained convex hull, or traverses every
history directly. Equations (2) and (3) then extend the decision checker's
universal inequalities to the original preparation class. Independently
propagated actual-history attainers establish equality for each reported
extremum; comparing all retained programs establishes optimality. Program
domination extends the optimum and joint-feasibility statements to the
original library. This proves the corollary.

The outer certificate cannot choose an unchecked response frontier or
preparation subset. Streaming rejects a supplied preparation certificate;
the covered path derives its representatives from the full local cover
sequence. The lower-level decision API makes independent coverage an explicit
premise, and this outer checker discharges it. Digests additionally bind the
physical inputs and method selection; recomputing a digest cannot replace a
missing identity or coverage proof. The output contains per-retained-program
extrema and witnesses, with informed values available by query. It contains
no exhaustive B(x_u) vector.

### Focused production audit

The independent audit exercised all four composed method combinations at
h=4, K=4 under `python -S -O`, using the frozen exact preparation fixture.
Its 13 retained histories agreed on every retained program's regret and
fidelity with all 16 actual sixteen-state preparations and all 96 original
physical continuation responses. The shared specialized evaluator agreed
exactly with both the generic four-coordinate recurrence and the full
physical calculation. Replacing D by the identity kernel caused that
specialization to decline and the generic path to remain exact.

The checker rejected missing candidate witnesses and levels, empty retained
families, empty witnesses even at zero contrast, boolean and negative indices,
noncanonical/float/boolean coefficients, the physical conic-only witness in
section 6, missing decision bounds, false history attainers, invalid comparators
and altered program identities. It also rejected rebindings to a changed
initial physical law or maintenance operator, and a streaming certificate
that retained a supplied subset certificate even after its outer digest was
recomputed. No soundness defect was found in this focused audit. These small
checks support the implementation obligations above; they do not establish
performance or replace the general induction.

## 6. Retained physical counterexamples

The [standard-library control script](../../experiments/preparation_family_controls.py)
reproduces the following statements with exact fractions and explicit failure
checks under `python -S -O`. The
[portable exact data](../data/preparation-family-controls.json) retain the
parameters, signatures, values and attaining words.

### Conic identities can remove the physically worst preparation

Use the inherited acquisition with sensor error 1/10, explicitly set initial
bad-health probability to one, and use two ordinary preparation updates. The
actual histories DR and RR satisfy

\[
x_{RR}=\alpha x_{DR},\qquad
\alpha=\frac{65551895140387323168}{75155083711181640625}
       =0.8722217034884954\ldots.
\]

A purported cover that retains DD, DR and RD and discards RR with this one
coefficient satisfies nonnegativity and the exact vector identity. It fails
the coefficient-sum condition. For the legal complete program DDDDM, the
true minimum fidelity over all four histories is
`0.7530433327196799...`; the retained-only calculation gives
`0.7871559623268850...`. DDDDM also uniquely attains the maximin optimum in
both the complete and incorrectly reduced classes. Thus their global
maximin values differ by the same amount.

A fidelity floor halfway between these values,
`0.7700996475232824...`, is declared feasible by the false cover and is
infeasible over the actual full class. A regret ceiling of one isolates this
floor failure because every physical fidelity lies in [0,1]. This control
uses one fixed acquisition and one history length within its explicitly
declared all-bad case. It adds no physical operation or runtime observation.

### Informed maxima are not affine in the preparation signature

Return to the default initially healthy acquisition, two preparation updates
and four ordinary continuation updates. The actual history DD uniquely prefers
RDDDM, while DR uniquely prefers DDDDM. Let x be the midpoint of their
signatures. Every fixed program value at x is the average of its two endpoint
values; the control checks all 96 complete programs. Nevertheless,

\[
\frac{B(x_{DD})+B(x_{DR})}{2}-B\left(\frac{x_{DD}+x_{DR}}2\right)
=0.0015262077737953094\ldots>0.
\]

The midpoint is an uncertainty mixture in the convexified evaluator domain.
It is not asserted to be an omitted actual history or a freely implemented
preparation procedure. The example proves that convex decompositions do not
permit interpolation of informed maxima. Formula (3), rather than such
interpolation, justifies regret preservation.

### Attainment and separate extrema do not certify the common optimum

In the same default four-history/96-program case, DDDDM has an exactly attained
worst regret of `0.00436701240997997...`, yet DRDDM has strictly smaller common
regret `0.0025321961178476887...`. One accurate worst-case witness for DDDDM
therefore does not establish minimax optimality.

For DRDDM, independently maximizing the informed value and minimizing its own
value produces `0.0052113003950940056...`, which exceeds its actual worst
regret. Those extrema use different preparations. The exact same-history
differences and their attaining histories are retained in the control data.

## 7. Costs and the acceptance boundary

Write v_t=`|Q_t|`. The inductive constructor generates exactly `2 v_t`
candidate history/signature pairs at the next nonzero level, rather than
requiring every original history. Count every generated candidate before
discarding it, every retained point, every membership proposal, exact witness
recovery, and the full local certificate. Retaining only actual histories
does not make their labels, signatures or witness encodings free.

The strong reference streams the same four-coordinate preparation recurrence
and returns the same compact decisions. It must not be charged for an
unrequested full response table or explicit B vector. Both sides receive the
same checked complete-program frontier and arithmetic improvements. Price
physical setup, preparation encoding, discovery, response evaluation, exact
decision construction, serialization/parsing, independent checking and reuse.
Cold optional imports and first solver initialization belong to discovery
when they occur in the delivered first-use path.

### The shared two-amplitude arithmetic specialization

For the inherited model, the evaluator recognizes an exact shape family

\[
S_\kappa=\begin{pmatrix}
(3+\kappa)/4&3(1-\kappa)/4&0&0\\
0&0&(3+\kappa)/4&3(1-\kappa)/4
\end{pmatrix},\qquad
x=cS_\kappa,\qquad \rho=(24/25)^2.
\]

Here c contains two health-block amplitudes. The shape is
`kappa=rho^(t+1)`, where t counts trailing D updates since the most recent R,
or since acquisition when no R has occurred. The code derives a constant
two-by-two matrix D_2 and an affine matrix `R_2(kappa)` and checks the complete
four-coordinate identities

\[
S_\kappa A_D=D_2S_{\rho\kappa},\qquad
S_\kappa A_R=R_2(\kappa)S_\rho.
\]

Both sides of each identity are affine in kappa. Their exact equality at
kappa=0 and kappa=1 therefore proves equality for every kappa, rather than
merely sampling two visited states. The actual initial signature is separately
checked against `c_0 S_rho`. Induction now updates c through D_2 or
R_2(kappa), increments t after D and resets t after R. Evaluating a continuation
uses the exact pair `S_kappa q(p)`, so its fidelity remains
`1/2-c(S_kappa q(p))`. A failed identity or initial-shape check selects the
generic four-coordinate recurrence.

The trailing-D state and its shape-dependent response pairs remain part of
this representation. It is not a global two-dimensional linear quotient of
the preparation hull: different shapes can span all four contrast coordinates.
The hull and its convex witnesses stay in the original four coordinates.
Both streamed and covered decision paths receive the same verified arithmetic
specialization, and its setup, response cache and query costs are included in
their comparisons.

The certificate support bound above does not establish a polynomial bound on
v_t, total discovery, encoded certificate size or runtime. Rational bit lengths
must be reported and charged. A fixed four-coordinate evaluator alone settles
none of those costs. A large avoided-history count is evidence of structural
compression; conditional adoption still requires a measured total-cost gain
against the matched streamed reference.

## 8. Contribution to the larger operational question

The combined construction has two sides: retained reachable histories cover
the uncertainty class, and retained feasible programs cover the continuation
class. Their intersection is a common decision with exact value bounds and
physical attaining witnesses. This specifies which distinctions the declared
decision needs and gives a constructive test that omitted distinctions cannot
change that decision.

It remains a design-time evaluator and compiler result. The history label is
not exposed to the controller. No physical organism acquires this certificate
for free, and no enduring ability to observe, act, repair or maintain the
compiler follows from fewer arithmetic operations. The recurrent-maintenance
work on the main branch concerns a distinct 64-state, twelve-emission physical
loop; the present theorem uses the 16-state source-fidelity model. Connecting the two
requires testing the representations when actual available capabilities,
resource states or observation interfaces change, including counterexamples
when the previously certified interface ceases to suffice. That bridge is a
further scientific obligation, not a consequence of this hull theorem.
