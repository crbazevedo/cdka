# Formal audit: decision coverage, renewable realizations and physical selection

**5 November 2026.** Audited core: `docs/strategy/realizable-renewable-core.md`
at the preparation/v17 integration checkpoint
`9b7dbd15d63531dc0fa873c6f80a74e3a763120a`.

## Verdict

The corrected common-decision proposition is sound under its stated finite,
nonempty and common-feasibility premises. The useful additional connection is
to make **selector closure** explicit. Invariance under each fixed primitive
does not generally survive a state-dependent combination of those primitives.
A selector compatible with the emission interface preserves the weaker
invariance; a common output-reset factorization supplies a second, stronger
route that does not require that compatibility.

Output renewal nevertheless does not reconstruct input distinctions already
lost by an old code. The exact three-state witness below exhibits all three
points and turns an invalid decoder reuse into a false common-decision gate.
This is a finite algebraic audit witness, not a new CDKA hardware benchmark or
a historical-priority claim. The corresponding identities are constructive
instruments whose antecedents are audited separately.

## 1. The common-decision theorem and its actual premises

Let X be a nonempty preparation-signature set, let Q be a finite nonempty
subset of X with actual preparation witnesses, and let L be a finite nonempty
library of complete programs. Every p in L must be executable under the same
declared physical/resource/observation contract for every preparation in X.
Assume `V_x(p)=c+x r_p`, with known common c, and:

1. `conv(Q)=conv(X)`.
2. F is a subset of L, and for every p in L there is **one** f in F satisfying
   `V_x(f)>=V_x(p)` for **every** x in X.

The order of quantifiers in the second premise matters. A different retained
program at each x would not be a common executable representative. It would
also silently replace the actual controller by an informed selector.

Writing `B_L(x)=max_{q in L}V_x(q)`, the program cover gives

\[
B_L(x)=B_F(x).
\]

For any fixed p, affine values and pairwise differences give

\[
\begin{aligned}
m_X(p)&=\min_{x\in X}V_x(p)=\min_{x\in Q}V_x(p),\\
R_{X,L}(p)&=\max_{x\in X}\max_{q\in L}[V_x(q)-V_x(p)]\\
&=\max_{x\in Q}\max_{q\in F}[V_x(q)-V_x(p)].
\end{aligned}
\]

For completeness, even when X itself is infinite, each x in X is a convex
combination of points of finite Q. An affine functional at x cannot exceed
the maximum or fall below the minimum on Q. Conversely Q is contained in X,
so both extrema are attained there. There is no compactness assumption hidden
in finiteness of the physical state space.

If f dominates p, `m_X(f)>=m_X(p)` and `R_X(f)<=R_X(p)`. Together with F being
a subset of L, these inequalities prove equality of the common minimax and
maximin values and equivalence of existence of a program satisfying both
thresholds. They do not preserve uniqueness or every tied program identity.
No interpolation of the generally non-affine informed envelope is used.

The theorem requires affine task values. Unnormalized success/survival
probabilities of fixed physical kernels have that form. Ratios conditioned on
survival, unproved statewise feasibility substitutions and arbitrary nonlinear
scores do not inherit the theorem merely because the underlying states are
finite. The existing source-fidelity and recurrent survival calculations keep
their original probability mass.

[Preparation theorem](preparation-family-proof.md) ·
[Program cover](program-family-proof.md) ·
[Original class-certificate scope](reachable-interfaces-proof.md)

## 2. Law realization implies a value interface under a checked domain

Use row laws. Let E be an m-by-n stochastic matrix whose rows emit physical
states from evaluator phases. Let K_a be substochastic physical kernels and
M_a substochastic phase kernels satisfying

\[
E K_a=M_a E.
\tag{1}
\]

For every fixed word w and nonnegative phase submeasure lambda,

\[
(\lambda E)K_w=\lambda M_wE,
\qquad V_\lambda(w)=\lambda M_w E g.
\tag{2}
\]

Induction on the chronological word proves (2). Since `E 1=1`, total live
mass is `lambda M_w 1`; the reduction preserves failure mass. For any declared
terminal g, the response `r_w=M_w E g` is linear in the phase coefficients.
The common-decision theorem therefore applies downstream if its preparation
and program covers and physical feasibility premises are separately supplied.

E need not have independent rows. Different phase weights representing the
same initial physical law give the same physical continuation values by (2).
No phase label, coefficient vector or evaluator posterior becomes an
observation available to the controller.

The stronger factorization

\[
K_a=A_aE,\qquad M_a=EA_a
\tag{3}
\]

with A_a substochastic implies (1). It also puts the output of any initial
physical law mu into the family: `mu K_a=(mu A_a)E`. This is an output
regeneration property, stronger than closure from laws already in the family.
It does **not** imply that `mu A_a` can be recovered from an arbitrary smaller
input code. That additional sufficiency obligation has a counterexample below.

Equation (1) suffices for fixed-word composition. When the grammar admits
observation-dependent control, its compiled kernels need a separate check.

## 3. Two sufficient routes through an admissible selector

Assume an independently verified selector/operation mechanism has the joint
physical kernel

\[
K_\pi=\sum_a D_aK_a,
\tag{4}
\]

where D_a are nonnegative diagonal matrices and `sum_a D_a=I`. An abort or
failure outcome can be represented explicitly by a zero substochastic kernel.
Equation (4) is a physical premise, not a license to choose actions using hidden
state. The selector must use the actually installed observation and memory
channels, with its price and faults included.

### Route A: selector compatibility with a weak realization

Suppose (1) holds and there are nonnegative diagonal phase matrices
`Dhat_a`, summing to the phase identity, such that

\[
E D_a=\widehat D_a E.
\tag{5}
\]

Then

\[
E K_\pi
=\sum_a\widehat D_a M_a E
=M_\pi E,
\qquad M_\pi=\sum_a\widehat D_a M_a.
\tag{6}
\]

M_pi is substochastic because each of its rows is a nonnegative weighted sum
of substochastic phase rows with weights summing to one. Equation (5) says
that within each emission row's support, the selector weight is constant
with that row's phase weight. It is an evaluator compatibility condition;
the phase weights are not granted as physical inputs to the selector.

Compatibility is sufficient, not necessary. Its failure alone does not prove
that the complete selected kernel leaves the family; the final identity must
be checked. The witness below supplies an actual failure.

### Route B: common output regeneration

If every selected operation has the stronger common factorization (3), then

\[
K_\pi=\left(\sum_aD_aA_a\right)E=A_\pi E.
\tag{7}
\]

A_pi is substochastic. Thus `M_pi=E A_pi` supplies a valid realization even if
the selector fails compatibility (5). The common output reset reestablishes
the emission family after the selected operation.

### Shared causes must remain inside the joint kernel

It can be unsound to multiply a selector probability by an independently
computed intervention kernel when both reuse a fault or another hidden cause.
For example, observing the selector result may reweight a shared fault that
also affects the selected operation. In that case the correct conditional
operation kernel need not equal its unconditional intervention kernel.

A safe certificate can work directly with joint branch subkernels
`J_a(s,s')=P(executed branch a, endpoint s' | start s)`. If exact physical
construction establishes `J_a=B_aE`, with nonnegative B_a and
`sum_a B_a 1<=1`, then `K_pi=(sum_a B_a)E` without an extra independence
assumption. Alternatively, verify (4) from those joint branch laws. The state
must contain all needed persistent causes; a missing common cause cannot be
removed by a matrix identity for the wrong kernel.

## 4. One three-state witness separates the obligations

States are A0, A1 and B. The terminal task is membership in A, with
`g=(1,1,0)`. All kernels in this witness are stochastic. The old emission
matrix is

\[
E=\begin{pmatrix}1/2&1/2&0\\0&0&1\end{pmatrix}
=\begin{pmatrix}e_A\\e_B\end{pmatrix}.
\]

The old fixed-word grammar contains I, T, R and S:

| Operation | From A0 | From A1 | From B |
|---|---|---|---|
| I | A0 | A1 | B |
| T | A1 | A0 | B |
| R | e_A | e_A | e_B |
| S | e_B | e_B | e_A |

I and T respectively preserve and swap the two A microstates. R refreshes
within the logical group; S flips the logical group and refreshes it. The
matrix identities are `E I=E T=E R=E` and `E S=swap(E)`. R and S also admit
the strong factors

\[
A_R=\begin{pmatrix}1&0\\1&0\\0&1\end{pmatrix},\qquad
A_S=\begin{pmatrix}0&1\\0&1\\1&0\end{pmatrix}.
\]

### Weak primitive closure does not imply selector closure

Let `D0=diag(1,0,1)` and `D1=diag(0,1,0)`. Admitting the fixed selector macro

\[
C=D_0 I+D_1 T
=\begin{pmatrix}1&0&0\\1&0&0\\0&0&1\end{pmatrix}
\]

maps both A microstates to A0. Although I and T each preserve the old emission
family, `e_A C=(1,0,0)` does not belong even to its linear span. The annihilator
`ell=(1,-1,0)` gives `E ell=0` but `E C ell=(1,0)`. Thus no phase matrix M_C,
even a signed one, satisfies `E C=M_C E`.

The selector violates (5): the first row of `E D0` is `(1/2,0,0)`, whereas a
diagonal phase rescaling of e_A would keep its first two entries equal.

By contrast, select I on the whole A block and S on B. The physical masks
are `diag(1,1,0)` and `diag(0,0,1)`, and the phase masks are `diag(1,0)` and
`diag(0,1)`. They satisfy (5), and (6) gives the valid phase kernel
`[[1,0],[1,0]]`.

### The old terminal-task scalar still survives C

For unit-mass laws define

\[
z=\mu(A0)+\mu(A1)-1/2=\mu b,
\qquad b=(1/2,1/2,-1/2).
\]

For I, T, R and C, `K b=b`; for S, `K b=-b`. Therefore every fixed word w
over the extended grammar `{I,T,R,S,C}` satisfies

\[
V_\mu(w)=1/2+(-1)^{\#S(w)}z.
\tag{8}
\]

This all-horizon guarantee follows from full matrix identities, not from a
sampled trajectory collection. One affine scalar plus known unit mass is
sufficient. The linear response span including mass is two-dimensional.

The reachable laws e_A, e_B and e_A C have rank three. Thus any full linear
law-emission representation containing this reachable family needs at least
three independent rows; the three-state identity emission is sufficient.
That bound is about this full-law family. It is neither a controller-memory
bound nor a statement about the physical v17 quotient. The same witness has
the one-free-coordinate terminal-task interface (8).

### Output reset does not recover a discarded input distinction

Now explicitly enlarge the installed grammar with

\[
U=D_0 S+D_1 R=A_U E,\qquad
A_U=\begin{pmatrix}0&1\\1&0\\1&0\end{pmatrix},\qquad
M_U=EA_U=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}.
\]

U uses the same incompatible masks, but both selected operations reset through
the common E. It therefore satisfies Route B and **does** intertwine E:
`E U=M_U E`. Its terminal response is
`U g=(0,1,1)`, which is outside the old span of `1` and g.

Take one acquisition `mu=(3/10,3/10,2/5)`. The actual equal-length histories
I and C produce

\[
\mu_0=(3/10,3/10,2/5),\qquad
\mu_1=(3/5,0,2/5).
\]

Both have the old signature `z=1/10`. The declared resource contract charges
both histories one preparation slot, padding I to the slot occupied by C,
and leaves **exactly one** continuation macro slot. R, S and each installed
conditional R/S rule occupy that slot. This is an abstract matched-slot and
deadline contract; it asserts no new CDKA hardware price or capability.

There are four deterministic maps from the binary observation to the two
operations R/S. The fourth rule is `W=D0 R+D1 S`, with rows `(e_A,e_B,e_B)`.
Thus the complete one-step deterministic class is `{R,S,U,W}`. Its values are:

| Preparation | R | S | U | W | Informed best |
|---|---:|---:|---:|---:|---|
| mu_0 | 3/5 | 2/5 | 7/10 | 3/10 | U |
| mu_1 | 3/5 | 2/5 | 2/5 | 3/5 | R, W |

For every physical law, `R g=(1,1,0)` dominates `W g=(1,0,0)`. Retaining
`{R,S,U}` therefore covers the entire four-rule class for this one-step
terminal objective. In particular, the retained and complete classes have
identical informed envelopes, common minimax/maximin values and joint gate
existence. No independent controller coin is available in this contract;
the stochastic physical emissions of R/S do not automatically grant one.
The controller receives only the current binary flag for this selection,
with no later decision inside the slot. The preparation-history identifier
is provenance for the evaluator, not an additional runtime controller input.

The true common minimax is R with regret 1/10; the maximin value is 3/5.
U has worst regret 1/5 and minimum value 2/5. The joint gate
`regret<=1/10` and `value>=2/3` is infeasible.

Reconstructing both laws from the old scalar as the fresh mixture
`(z+1/2,1/2-z) E` falsely replaces mu_1 by mu_0. It reports U as minimax
with zero regret and minimum value 7/10, falsely certifying the joint gate.
Yet U's two true output laws are both fresh emissions: their phase weights
are `(7/10,3/10)` and `(2/5,3/5)`. Output regeneration is valid; recovering
those input-dependent weights from the old scalar is not.

The rows `1`, g and U g have rank three. Over the corresponding full
reachable affine span this enlarged task interface requires two free linear
coordinates with known unit mass. This local rank statement is distinct from
requiring an extra coordinate on the two-law fixture alone, where some other
scalar could simply identify the pair.

### The deadline and deterministic-policy scope are substantive

Allowing two continuation slots changes the result. The exact positive
controls are:

| Two-step word | Value at mu_0 | Value at mu_1 |
|---|---:|---:|
| RU | 7/10 | 7/10 |
| SU | 4/5 | 4/5 |
| WU | 17/20 | 7/10 |

Over all sixteen words of length two from `{R,S,U,W}`, the informed values
are `(17/20,4/5)`. SU is common minimax with regret 1/20 and maximin with
value 4/5. SU and WU pass the original joint gate. RU has regret 3/20 and
does not pass. The one-step infeasibility certificate therefore requires its
one-step deadline.

Restricting the two-step alphabet to `{R,S,U}` instead gives nine words,
informed values `(4/5,4/5)`, zero common regret for SU and a passing gate for
both RU and SU. These are different two-step libraries. The terminal
dominance of W by R is not contextual dominance: `WU(mu_0)=17/20` exceeds
`RU(mu_0)=7/10`. A one-step program cover cannot silently be reused to prune
prefixes before a new suffix. This is exactly why coverage must certify the
actual complete-program grammar and objective being evaluated.

A separately supplied independent common coin also changes the policy class.
Choosing U with probability 1/3 and R with probability 2/3 gives values
`(19/30,8/15)` and same-input regrets `(1/15,1/15)`, improving the deterministic
minimax regret 1/10. This is an exact improvement control, without a claim of
randomized minimax optimality. The maximin value remains 3/5 under any mixture
of the four one-step rules: no rule exceeds 3/5 at mu_1, and R attains 3/5
at both inputs. The 2/3 fidelity floor remains impossible. No such coin is
included in the actual one-step contract.

### Observation and grammar boundary

The masks D0/D1 require distinguishing A1 from A0/B. A declared observation
`o(A0)=o(B)=0, o(A1)=1` and installed routing tables can implement those masks
in this finite abstraction. A readout exposing only the logical A/B group
cannot implement them. Physical installation and pricing are premises of the
enlarged grammar, not consequences of the matrix algebra.

C is an opaque primitive in the extended fixed-word grammar of (8). Its
algebraic selector decomposition does not export an internal flag to the
controller. U and W are newly installed conditional compositions of R/S;
their implementation may use the same physical flag if access and routing
are actually provided. A new observation alphabet is not logically required,
but the admissible composition capability has changed. Admitting one fixed
macro does not grant every routing table. The scalar guarantee (8)
concerns the specified fixed-word terminal-task library. The witness does not
contradict a predictive-state representation whose tests already quantify over
these observations and policy contingencies.

## 5. What the current production checker does and does not establish

| Obligation | Present implementation or enclosing evidence |
|---|---|
| Valid supplied D/R kernels and fair initial submeasures | `make_preparation_model` checks row stochasticity, all sixteen-coordinate transport identities, initial contrast and cone membership. |
| Actual preparation history coverage | The preparation checker regenerates retained children and verifies complete exact convex witnesses, including coefficient sum one. |
| Physical response and complete fixed-word grammar coverage | The program-family checker propagates responses through supplied kernels and checks the original D/R plus at-most-one-M grammar. |
| Per-program extrema and optimality over the covered library | The decision checker verifies universal inequalities and independently propagates actual attaining histories. |
| Physical acquisition provenance, observation access, controller installation and common resource reservation | These remain obligations of the physical model/experiment; contract metadata binds them but does not derive or prove them. |

The last row is not a discovered production defect. The code explicitly
states that acquisition provenance is an enclosing obligation, and the
inherited experiment supplies the shared sensor, faulty voter, fixed word/
phase control and common worst-case resource reservation. The manuscript
should retain that boundary when calling the result a physical decision
certificate. Arbitrary user metadata, a digest or an exact numerical kernel
does not establish actual sensor access or installed controller memory.

[Preparation model](../../cdka/preparation_families.py) ·
[Composed checker](../../cdka/preparation_pipeline.py) ·
[Physical contract and reservation](../../cdka/reachable_diagnosis.py)

## 6. Verification and recommended manuscript scope

The [standard-library reproducer](../../experiments/core_interface_witness.py)
checks the old intertwining identities, two strong reset factors, the selector
counterexample, compatible-selector identities, regenerated U/W factorizations,
response/full-law ranks and the true/false common decisions. It also checks the
complete deterministic one-step cover, the two distinct two-step libraries
and the separately enabled common-coin control. It verifies
2,343 value calculations from all three physical basis laws over the 781
fixed words of length at most four. The all-word theorem is separately supplied
by the exact transport identities.

Nine [regression tests](../../tests/test_core_interface_witness.py) pass under
`python -S -O`. Their independent microbranch enumerator checks 468 bounded
state/word cases, reconstructs the selector macro from its declared observation
and routing table, and verifies that true renewed outputs have different
phase weights. It independently checks all 32 preparation/two-step values
in the complete sixteen-word class and the external-coin values. The frozen
[exact fixture](../data/core-interface-witness.json) reproduces without
numerical discovery. No benchmark or hardware-memory reduction is claimed.

The strongest supported integration is conditional and constructive: obtain
an affine value interface from a checked realization, establish closure for
the actual admitted selector or complete program, then apply preparation and
program coverage to a common physical decision. Preserve the input domain at
every boundary. When a new operation leaves it, output renewal can restore
future realization while the transition itself still requires distinctions
the old input code omitted. This connects the manuscript's three obligations
without conflating their representations or introducing a free observer.

## 7. Bounded implementation hardening: optimized generator execution

The assertion-disabled audit exposed a preexisting defect in
`compile_one_maintenance`: the old basis was seeded by `assert new.add(value)`.
Python `-O` removes the entire assertion expression, including the insertion.
Old witnesses were still appended, so later accepted maintenance responses
were paired with the wrong witness positions and the basis/witness counts
diverged. The focused suite reproduced one incorrect empty-word separator
and two certificate-verification errors. The independent checker correctly
rejected the malformed certificates with `invalid signature certificate:
witness count`; this was a generator defect, not acceptance by the checker.

The minimal correction executes `new.add(value)` unconditionally and raises
an explicit `AssertionError` if an old basis vector unexpectedly fails
independence. The independent verifier and finite-horizon construction are
unchanged. One new subprocess regression executes the complete generator and
checker under both `-S` and `-S -O`, checks the actual optimization flags,
compares the entire certificate to ordinary output, and checks that the
separating word is still M.

The ordinary default certificate is identical before and after this fix. Its
canonical JSON SHA-256, using sorted keys and compact separators, remains
`8e7d8f55d3037fe9174442a28e7bd5c5ff7b38742c9fc3249242b4f4a729d717`.
The generated old/new dimensions remain 10/12, with matching witness counts.
No scientific fixture was changed by this repair.

The maintenance-signature suite passes **nine tests** in each of ordinary and
`-S -O` execution, including the one added subprocess regression. This count
is separate from the **nine new-interface witness tests** in Section 6.
The repair changes optimized execution correctness and adds no scientific or
physical-model claim.
