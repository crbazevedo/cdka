# A maintenance capability can invalidate a previously exact compression

**Executed research gate: R11/R14, based on CDKA v15.** This increment adds a
single paid, physically selected maintenance capability to the existing
register process. It gives a necessary and sufficient extension test for an
old linear continuation interface, an attaining enlarged interface, and a
physical continuation separating two laws that were equivalent for every
old continuation.

The preceding kernel, voter and old updates are unchanged. The algebraic
response-space machinery is reused from v12. The contribution is the
maintenance-relative contract, its exact physical witness, and its resource
and realization accounting.

## 1. What the controller actually does

The physical state before resource bookkeeping is `(Z,a,b,c)`: the same
hidden substrate mode and three stored cells as v15. `D` and `R` are the
inherited DIFFUSE and REGENERATE updates. The diagnostic/command register
is physically modified by those updates; it is not a fresh designer
posterior at every stage.

The added `M` routine reserves and prepays **one complete service slot in
every branch**. The installed six-NAND voter reads the current cells with
its current, possibly degraded error law. A voted one requests a repair;
repair succeeds with the declared probability and sets the substrate to
healthy. A voted zero performs no repair. The result is hidden, the cells
are retained, and the inherited HEALTH transition follows the routine.

The six NANDs are reused in time for selection and later register/readout
operations. No extra copy of the voter or reliable diagnostic trigger is
assumed. Installed gates, gate evaluations, cell writes, clock intervals
and service slots are different costs; none is identified with joules.
Routing, a fixed phase controller and resource reservation remain
explicit common infrastructure assumptions.

The prepaid rule is substantive. Remaining resource does not reveal
whether the vote requested repair. With zero slots, `M` is unavailable;
its zero-mass kernel is a fail-closed representation of an inadmissible
call. No legal continuation from one slot contains two `M` calls.

The terminal task in this experiment is the event that the actual noisy
voter outputs one. It is not the complete plant-survival objective of
earlier CDKA experiments. A law over hidden health is an evaluator input;
the controller only executes the stated physical routine.

The old grammar executes `D/R` words without returning intermediate
observation flags to an external policy. It has **one terminal readout**.
The vote used by `M` is internal: it physically controls repair but is
not returned as a new externally readable observation. These restrictions
are part of the continuation library, not conclusions about every policy
that could be built from the same components.

## 2. A resource-sensitive continuation contract

Let `A={D,R}` denote the old substochastic kernels on a finite physical
state space. Matrices act on column observables. Let `G` contain the mass
observable and the declared terminal response. Every column is a response
of a physically declared continuation, not an arbitrary new measurement.

For a finite chronological word `w`, write `K_w g` for its terminal
response vector. Define the two legal response spaces

\[
W_0=\operatorname{span}\{K_u g:u\in A^*,\ g\in G\},
\]

\[
W_1=\operatorname{span}\left(W_0\cup
 \{K_u M K_v g:u,v\in A^*,\ g\in G\}\right).
\]

`W0` describes the task when maintenance cannot be used. `W1` describes
the task when at most one maintenance routine can be inserted. It allows
arbitrary finite old continuations on either side, subject to the
execution's separately declared update/time costs. It does **not** allow
arbitrarily many maintenance calls.

Two nonnegative, possibly unnormalised laws are equivalent for a space
when they give the same expectation for every response in that space.
Equal mass is part of this condition. The physical controller need not
compute either law or its signature.

## 3. Exact criterion for reusing the old interface

**Proposition 1.** The old interface remains sufficient after allowing one
paid maintenance routine if and only if

\[
M W_0\subseteq W_0.
\]

Equivalently, `W1=W0`.

**Sufficiency.** The old space is invariant under `D` and `R`. If it also
contains `M W0`, every response `K_u M K_v g` remains in `W0`: first apply
the old suffix, then `M`, then the old prefix. The old coordinates
therefore determine every legal one-maintenance continuation.

**Necessity.** Each old basis column is an actual old continuation
response. If the old interface determines all new continuations, it
determines `M` applied to every such column. For linear signatures on
unnormalised laws this requires those vectors to lie in `W0`. More
explicitly, if `Mv` lies outside `W0`, linear separation supplies a signed
row `delta` with `delta W0=0` but `delta Mv` nonzero. Because mass belongs
to `W0`, `delta` has zero total mass. Its positive and negative parts,
normalised by their equal positive mass, are probability laws `mu` and
`nu`. They agree on **every** old continuation but disagree on the real
continuation `M` followed by the old word witnessing `v`. QED.

This proposition is an exact extension-of-library condition. It does not
say that the old interface was inaccurate for its previous task, or
that the new capability improves every objective. Adding a capability
can make previously dispensable distinctions relevant.

## 4. Constructing the smallest sufficient linear extension

The construction is

\[
W_1=\operatorname{inv}_{D,R}(W_0+MW_0).
\]

The existing v12 compiler first constructs `W0`. Apply `M` once to each
accepted old basis vector. Retain independent images. Only prepend old
updates to the new accepted vectors. Every retained vector has a
physical word with zero or one `M`; rejecting a dependent vector
discards its old-prefix descendants by linearity.

This differs from closing freely under `{D,R,M}`, which would silently
permit multiple paid calls. The one-call construction contains all
legal responses and only their span.

**Proposition 2.** If the resulting basis has `d1` independent columns,
it is an exact sufficient homogeneous linear signature of dimension
`d1`, including mass. No smaller homogeneous linear signature can
determine the expectations of all legal responses for all
unnormalised input laws.

**Proof.** The construction contains the probes, `W0`, `M W0`, and is
closed under old prefixes, so it contains every legal response. Every
accepted column is itself a legal response, so the span contains no
extra requirements. A sufficient linear signature must span those
`d1` independent response functionals; its rank is therefore at least
`d1`. Taking their values is an attaining signature. QED.

For normalised laws, known total mass can be supplied as a constant in
an affine representation. These dimensions are not counts of physical
states, memory bits, or minimal nonlinear encodings. In particular,
the three-cell physical controller is not replaced by `d1` runtime
registers containing probabilities.

## 5. A checkable certificate, separate from discovery

Let `F0` and `F1` be matrices whose columns are the accepted bases. The
certificate supplies exact rational matrices satisfying

\[
K F_r=F_r B_{K,r}\quad (K\in\{D,R\},\ r=0,1),
\]

\[
F_0=F_1 E,\qquad MF_0=F_1 C,
\]

and representations of each terminal probe in both bases. It also
supplies a legal word/probe witness for every column and an inverse of
a square minor of each basis. The inverse proves that the columns
are independent.

`verify_one_maintenance` checks these equalities, replays the supplied
words and multiplies each minor by its supplied inverse. It does not
run the compiler, discover a new basis, search continuations or
perform Gaussian elimination. A SHA-256 binding covers every kernel
entry, terminal probe, operator name and declared physical contract.
Changing the costs/scope metadata or the physical kernels invalidates
the binding.

This algebraic checker does not prove that a kernel is physically
correct. The raw fault-mask and repair/health-event oracle validates
that separate obligation.

## 6. The short-horizon certificate is a different statement

For at most `h` old updates and at most `r` maintenance calls, use the
graded spaces

\[
W_{h,0}=\operatorname{span}\left(G\cup
 \bigcup_{K\in A} K W_{h-1,0}\right),
\]

\[
W_{h,1}=\operatorname{span}\left(G\cup
 \bigcup_{K\in A} K W_{h-1,1}\cup M W_{h,0}\right).
\]

At `h=0`, omit old-update terms. An `M` call is an additional clock
interval; `h=2` means at most two `D/R` updates and one optional
maintenance interval, plus terminal readout. It does not mean that
three operations were performed in two clock intervals.

The finite-horizon compiler retains actual legal words and uses the
same basis-rank certificate. Its checker verifies the recursive
inclusions using the preceding layers. These two-sided arguments
(every basis column is legal, every legal response is covered) prove
the exact rank for each bounded grammar. Unlimited-horizon ranks
must not be reported as the minima of a two-update problem.

## 7. Why the physical maintenance step reveals a lost distinction

Write `f_z(b)` for the voter output-one probability in stored pattern
`b` at health `z`. In degraded state, a repair is requested with
probability `f_1(b)`, and succeeds with probability `s`. A repaired
substrate remains healthy through the subsequent HEALTH transition
with probability `19/20`. Hence

\[
(Mg)(1,b)=f_1(b)+s\frac{19}{20}f_1(b)
                \bigl(f_0(b)-f_1(b)\bigr),
\]

where `g` is the terminal readout response. The new expectation
depends on a product of the faulty selection probability and the
effect of repairing that same mechanism. Preserving old marginal
responses need not preserve this product.

The selection/repair event is generated by the actual retained
register. Its hidden health result is a common cause of subsequent
gate faults. Computing at an average independent gate-error rate
would discard that dependence and would be a different kernel.

## 8. Exact scope of the dimension upgrade

The independent compiler and checker give:

| Old `D/R` updates allowed | No maintenance | At most one additional `M` |
|---|---:|---:|
| None | 2 | 3 |
| At most one | 4 | 9 |
| At most two | 7 | 12 |
| Arbitrary finite old continuation | 10 | 12 |

These are ranks including the mass functional. In the two-update
grammar, the upgrade is `7 -> 12`; when extending the already closed
old interface, it is `10 -> 12`. The latter states that exactly **two
additional homogeneous linear response coordinates** are necessary
and sufficient for all the newly allowed continuations. It does not
mean two physical cells, and it does not assign the unlimited-horizon
old rank to a two-update task.

For explicit resource state `r=0,1`, the full process has 32 physical
microstates. The inherited `b <-> c` symmetry and the paid routine
admit a 24-class Markov quotient `(r,Z,a,b+c)`. The task interface has
dimension `10+12=22`: no service remains at `r=0`, while one service
can still be called at `r=1`. The smaller 22-dimensional object is
a linear response interface, not a 22-state Markov chain.

Indeed, the paid maintenance block maps the zero-slot response basis
into the one-slot response space and kills an unavailable second call.
Old updates preserve each resource sector. The block-diagonal response
basis therefore intertwines every legal kernel. The physical resource
input is retained throughout; hidden health does not become readable.

### A discontinuous exact rank, with a continuous operational effect

Write the physical routine as `M_s=M_0+s Delta`, where `s` is its
repair-success probability. The selector law is fixed before repair,
so this dependence is exactly affine. The certificates establish
`M_0 W0` contained in `W0`. Consequently

\[
W_0+M_s W_0=W_0+\Delta W_0\qquad (s>0),
\]

and closing both sides under the old updates gives the **same**
12-dimensional one-call space for every `s` in `(0,1]`. At `s=0`
the old 10-dimensional space suffices. This is an algebraic statement
for the whole parameter interval, not inference from a grid of success
rates.

For any fixed pair of old-equivalent laws, the difference in a word
with one `M_s` is affine in `s`, and its constant term is zero. The
gap is therefore linear in `s`. An arbitrarily weak positive ability
can require an additional exact coordinate while producing an
arbitrarily small decision-relevant numerical effect.

### An explicit pair and a useful tolerance criterion

Let all initial states have degraded `Z=1`. With common denominator
`1458626`, use the probability weights

| Stored cells | Left law | Right law |
|---|---:|---:|
| `000` | 0 | 30625 |
| `001` | 0 | 736513 |
| `011` | 0 | 691488 |
| `100` | 736513 | 0 |
| `101` | 722113 | 0 |

The laws have equal expectations for all ten old basis responses.
The old closure certificate therefore proves equality for **every**
old `D/R` word, not merely the short words checked experimentally.

With `s=4/5`, the word `M` followed by terminal readout separates them.
The exact right-minus-left difference is

\[
-\frac{21619539012817056454767961911}
        {1780549316406250000000000000000}.
\]

For a finite declared family of response queries, let `Delta_max` be
the largest absolute response gap of this pair. Any predictor that
assigns the same interface to both laws must have worst-case error
at least `Delta_max/2` on this pair. The componentwise midpoint of
their response vectors attains that bound; it is also the response
of their average law. Thus a tolerance below `Delta_max/2` makes the
distinction necessary even for a nonlinear common predictor.

This is a two-law prediction certificate. It is not a global optimum
over the entire old equivalence class, an optimal control policy,
or a physical implementation of the midpoint. It makes the value of
an exact distinction explicit instead of presuming every nonzero
gap justifies more hardware.

## 9. The intermediate-observation control

If the old library had already exposed intermediate voter results,
it would contain observation-conditioned kernels such as
`diag(f)` and `diag(1-f)`, not only `D` and `R`. Closing that larger
library gives rank 12 in this fixture. The same two initial laws can
then be separated without maintenance, by a readout-one branch
followed by another readout.

That control is essential to interpreting the result. The new routine
permits a new **causal use** of the noisy vote in the existing silent
update grammar. It is not a claim that no other observation-capable
controller could access the distinction with the same voter hardware.
Adding intermediate measurements, their outcome memory and their
conditional policy mapping changes the contract and its prices.

## 10. Interpretation and remaining obligation

The result concerns the smallest declared **linear evaluator
interface**, coupled to an explicit paid intervention and real
register updates. It directly separates two costs: discovering which
distinctions matter, and keeping the physical means to use them.

The prepaid one-call grammar proves a precise contribution without
claiming an indefinitely self-maintaining organism or a jointly
optimised controller for the entire earlier plant. A future grammar
that exposes service outcomes, allows budget-dependent external
branching, adds another maintenance call, or changes the terminal
task requires another certificate. The existing physical law and
old certificates remain valid within their stated contracts.
