# Reachable input domain: eight orbit masses and four signed contrasts

**Status:** exact analytic preservation for every finite D/R preparation
history, with rational boundary-restriction certificates for the inherited
physical kernels. Maintenance generally leaves the domain.

This result explains why a physically generated preparation class can need
fewer evaluator coordinates than an unrestricted physical state space. It
uses the acquisition and physical channels in
[`reachable_diagnosis.py`](../../cdka/reachable_diagnosis.py), the boundary
maps in [`reachable_restriction.py`](../../cdka/reachable_restriction.py), and
the preceding [maintenance response certificate](maintenance-enabled-signatures-proof.md).
The approximation and shared-plan guarantees are proved separately in
[`reachable-interfaces-proof.md`](reachable-interfaces-proof.md).

## 1. Variables and the physical acquisition

Let `b=(b1,b2,b3)` be the three retained cells, `Z in {0,1}` the hidden
substrate health, and `H in {0,1}` the fixed target bit. The prior of H is
fair and independent of initial substrate health. A single BSC observation
produces `Y=H xor E`, where `P(E=1)=eta`. The same realized Y is broadcast
to three independent write channels of error `e=1/50`. The inherited health
channel T is applied once after this acquisition interval.

Define the probability of writing configuration b from a broadcast y by

\[
B_y(b)=e^{\operatorname{dist}(b,y^3)}(1-e)^{3-\operatorname{dist}(b,y^3)}.
\]

Here `dist` is Hamming distance. If `p_z` is the substrate distribution after
the acquisition health transition, the two target-indexed submeasures are

\[
\begin{aligned}
\mu_1(z,b)&=\tfrac12p_z\bigl[(1-\eta)B_1(b)+\eta B_0(b)\bigr],\\
\mu_0(z,b)&=\tfrac12p_z\bigl[(1-\eta)B_0(b)+\eta B_1(b)\bigr].
\end{aligned}
\]

Their signed contrast is therefore

\[
\boxed{d(z,b)=\mu_1(z,b)-\mu_0(z,b)
 =\tfrac12p_z(1-2\eta)\bigl[B_1(b)-B_0(b)\bigr].}
\]

This equation uses one shared sensor outcome. Three independent sensor
outcomes would give a different acquisition law and an additional
observation cost.

The target H is not supplied to any physical control operation. It enters
only the success event and the evaluator's joint law. For every admissible
mass-preserving continuation w,

\[
V(w)=\operatorname{mass}(\mu_0)+dK_wg,
\]

where `g(z,b)` is the probability that the actual six-NAND voter outputs 1.
In this acquisition family `mass(mu_0)=1/2`, including after every legal
D/R preparation history.

## 2. The eight-dimensional exchangeable domain

A law or signed measure is exchangeable when its value is constant on
configurations with the same `(Z,|b|)`. There are eight such orbits. Store
their **total masses**

\[
m_{z,k}=\sum_{|b|=k}\nu(z,b),\qquad z\in\{0,1\},\ k\in\{0,1,2,3\}.
\]

The corresponding value at one microstate is

\[
\nu(z,b)=\frac{m_{z,|b|}}{\binom3{|b|}}.
\]

Let Q be the `8 x 16` matrix whose rows are the uniform probability laws
on individual orbits, and let A aggregate physical states into orbit
masses. Then `Q A=I_8`, and an exchangeable row measure is `m Q`.

This is an eight-dimensional linear domain of measures. Normalized
probability laws form an affine section with one known mass constraint.
The distinction matters when interpreting a linear rank that includes
mass.

Both acquisition submeasures are exchangeable. D preserves exchangeability
because its independent equal-rate cell channels commute with every port
permutation. R also preserves it: whatever its input law, R broadcasts one
actual voter output and makes three equal-rate independent writes. The
resulting cell law is a mixture of `B_0` and `B_1`. The voter itself need
not be symmetric under port permutation for this output law to be
exchangeable.

Health mixing does not depend on the port names. Consequently

\[
QK_a=QK_aAQ,\qquad a\in\{D,R\}.
\]

This proves preservation of an **input-distribution domain**. It does not
assert that individual physical states with the same count have equal
transition laws or equal voter outputs.

## 3. The four-dimensional contrast domain

Write `bar b` for the bitwise complement of b. Since
`B_1(bar b)=B_0(b)`, the acquisition contrast satisfies

\[
d(z,\bar b)=-d(z,b).
\]

Combine this antisymmetry with exchangeability. The orbit masses obey

\[
m_{z,3}=-m_{z,0},\qquad m_{z,2}=-m_{z,1}.
\]

Thus the contrast is determined by four numbers, in the order

\[
c=(m_{0,0},m_{0,1},m_{1,0},m_{1,1}).
\]

Let E be the `4 x 16` matrix whose row indexed by `(z,k)`, for `k=0,1`, is
the uniform unit mass on orbit `(z,k)` minus the uniform unit mass on
orbit `(z,3-k)`. Then

\[
d=cE.
\]

Each basis row has total mass zero separately within its health block.
The four rows are linearly independent, so their span S has dimension
four. Its coefficients are signed quantities, not four physical states
or four probabilities.

The coordinate `m[z,1]` is the **sum over all three one-bit configurations**.
If instead a per-microstate value were stored, its contribution to a query
would require a factor of three. The implementation uses orbit masses.

## 4. D and R preserve S for all history lengths

### Diffusion

Let `C_e(b,b')` be the product of the three identical bit-flip channels.
It commutes with all port permutations and with simultaneous complementation:

\[
C_e(\bar b,\bar b')=C_e(b,b').
\]

For an antisymmetric input contrast,

\[
\begin{aligned}
d'(z',\bar b')
&=\sum_{z,b}d(z,b)T_{zz'}C_e(b,\bar b')\\
&=\sum_{z,b}d(z,\bar b)T_{zz'}C_e(b,b')\\
&=-d'(z',b').
\end{aligned}
\]

Permutation invariance is preserved by the same change-of-variable argument.
Therefore D maps S into S.

### Regeneration with the actual asymmetric voter

Let `f_z(b)` be the probability that the existing faulty six-NAND voter
outputs 1. No symmetry of this function is assumed. The regeneration kernel
has the form

\[
K_R((z,b),(z',b'))
=T_{zz'}\bigl[(1-f_z(b))B_0(b')+f_z(b)B_1(b')\bigr].
\]

Every contrast in S satisfies `sum_b d(z,b)=0` for each z. Set

\[
a_z=\sum_b d(z,b)f_z(b).
\]

Then its propagated contrast is

\[
\begin{aligned}
d'(z',b')
&=\sum_zT_{zz'}\left[
 B_0(b')\sum_b d(z,b)
 +(B_1(b')-B_0(b'))\sum_b d(z,b)f_z(b)\right]\\
&=\boxed{\sum_z T_{zz'}a_z\bigl[B_1(b')-B_0(b')\bigr].}
\end{aligned}
\]

The last expression is exchangeable and antisymmetric. Thus R maps S
into S even though the voter distinguishes some arrangements with the
same number of ones.

### Arbitrarily long preparation histories

Acquisition places d in S, and each D/R update preserves S. Induction
therefore gives

\[
dK_h\in S\quad\text{for every finite }h\in\{D,R\}^*.
\]

Equivalently, there are exact `4 x 4` linear update matrices U_D and U_R
such that

\[
EK_a=U_aE,\qquad a\in\{D,R\}.
\]

They are obtained by pushing the four basis rows and extracting their
four orbit masses. Checking these eight basis images is sufficient to
check the two identities on all of S. It is not necessary to enumerate
histories to establish the dimension bound. The experiment retains the
full physical preparation construction as an independent reference and
uses the four-coordinate restriction at the query boundary.

## 5. Query restriction must follow the complete physical continuation

For an arbitrary physical response column q, define its orbit averages

\[
\bar q_{z,k}=\frac1{\binom3k}\sum_{|b|=k}q(z,b).
\]

The four-coordinate query is

\[
Eq=
\begin{pmatrix}
\bar q_{0,0}-\bar q_{0,3}\\
\bar q_{0,1}-\bar q_{0,2}\\
\bar q_{1,0}-\bar q_{1,3}\\
\bar q_{1,1}-\bar q_{1,2}
\end{pmatrix}.
\]

Consequently

\[
\boxed{V(w)=\operatorname{mass}(\mu_0)+c(EK_wg).}
\]

The order of operations is essential: first obtain `q_w=K_w g` through the
complete inherited physical continuation, including M when present; then
restrict that response to the preparation domain by E. This identity holds
for every d in S even when the continuation leaves S after its first action.

The intermediate eight-coordinate method performs the same calculation
using `d`'s eight orbit masses and `QK_wg`. The experiment checks the
32-state joint evaluation, 16-entry signed contrast, eight orbit coordinates
and four antisymmetric coordinates against each other on all 384 entries
of the principal response table.

These identities reduce the boundary payload and the cost of evaluating
compiled queries. They do not eliminate the cost of constructing a physical
query column. A claim about compiling an arbitrary combinatorial model
without explicit kernels requires a separate algorithm and certificate.

## 6. Maintenance generally leaves both domains

For a degraded input state, successful repair occurs with probability
`s f_1(b)`. In the existing health channel, the repaired healthy state
persists with probability `19/20`. Hence the contribution from the degraded
contrast to the healthy output block is

\[
d'_0(b)=\frac{19}{20}s f_1(b)d_1(b)
\]

plus the transported contribution from an initially healthy block. The
product `f_1(b)d_1(b)` generally preserves neither exchangeability nor
antisymmetry. The voter is asymmetric, and `f_1(b)` generally differs from
`f_1(bar b)`.

This failure occurs for an actual acquisition law, without choosing an
arbitrary signed basis vector. Start healthy, acquire one shared sensor
output with `eta=1/10`, write with `e=1/50`, apply the acquisition health
transition, then execute M with `s=4/5`. If `d'=dM`, exact evaluation gives

\[
d'_0(000)+d'_0(111)
=\frac{29634054247008}{2384185791015625}
\approx0.012429423226444265,
\]

which violates antisymmetry, and

\[
d'_0(011)-d'_0(101)
=\frac{39414816}{3814697265625}
\approx0.000010332357525504,
\]

which violates exchangeability. The initial acquisition is a legitimate
history-length-zero preparation, so this is a reachable-domain
counterexample.

Thus the same fixed expansion E cannot simply be reapplied after M as an
exact projection. Similarly, repeatedly using the eight-orbit transition
`QKA` is invalid unless `QK=QKAQ` has been checked for that operation.
The [independent review](reachable-diagnosis-review.md) supplies a nonzero
terminal-response separator for the naive projection and an exact error
on the principal four-preparation fixture.

With `s=0`, M applies only the inherited health transition while retaining
the cells, and both domains are preserved. Preservation may also hold on
particular zero or degenerate contrasts. The counterexample establishes
failure of preservation on the whole domain, not failure at every input.

## 7. What the old response restriction certificate proves

Let F_0 be the previously certified old response basis on the 16 physical
states, with ten columns including mass. Restrict each old response to S,
giving the columns of `E F_0`. For the current kernels this matrix has rank
four. The certificate selects four actual old response columns and supplies
an inverse of their `4 x 4` restricted matrix.

If C is that matrix, checking `C C_inverse=I_4` proves that the old responses
already identify every contrast c in S. A checker only multiplies the
supplied rational matrices; it does not repeat rank discovery. The
certificate binds the old basis, domain identifier and physical contract.
The generated artifact records old-basis indices `[1,2,3,4]` for this
restriction.

Similarly, `QF_0` has rank eight and a separate inverse certificate shows
that old responses distinguish every exchangeable input law. These are
different statements: the eight-dimensional domain contains general
exchangeable measures, while S contains exchangeable contrasts that are
antisymmetric under complementation.

Because `EF_0` is injective on the entire four-dimensional linear domain,
an exact **linear** response-preserving representation on that entire
domain requires at least four independent coordinates. Four therefore
match this stated linear-domain lower bound.

This does not prove four is an absolute minimum for a particular normalized
cohort of four preparations. Its affine hull has dimension at most three;
known constants may be supplied separately, and task-relative decision
compression may identify additional preparations. It also says nothing
about the minimum number of bits, cells, physical states or arbitrary
nonlinear codes. The source prior supplies the offset `1/2` in this fixture;
a general target prior would require retaining its mass offset explicitly.
At `eta=1/2` the actual contrast is zero and the preparation contrast rank
collapses to zero; the ambient four-dimensional domain is not a claim that
every parameter setting or preparation family needs four coordinates.

## 8. The new target changes the unrestricted response ranks

The previous task was the event `readout=1` on the 16-state register. Its
unrestricted old and one-maintenance response dimensions were 10 and 12.
The current task is `readout=H`, with a hidden target bit carried through
the dynamics. The independent control constructs the unrestricted joint
32-state model and recomputes the response closure. Its dimensions are
**11 without maintenance and 13 with at most one M**, including mass.

The signed-contrast identity explains how the existing basis can be reused
with a target-mass offset, without claiming that changing the terminal task
leaves its global rank unchanged. The four-coordinate result instead uses
the restricted acquisition domain and the fair-source symmetry proved
above. Global response rank and boundary-domain dimension answer different
questions; both controls are recorded in the
[exact results](../data/reachable-diagnosis-results.json).

## 9. Consequence for the preparation class

The contrast's four-dimensional domain is preserved for arbitrarily long
D/R preparation histories. This converts the observed rank-four behavior
at history lengths two, four and six into a structural bound rather than
a conjecture extrapolated from those finite enumerations.

The number of histories and the complexity of their reachable convex hull
can still grow with length. A fixed state-vector dimension alone does not
prove a polynomial bound for discovering all extreme preparations or
optimizing over arbitrary switched histories. The present class certificate
uses explicitly generated finite preparations, and its common-plan
guarantees extend to their convex hull through the separate envelope and
regret theorems.

The useful conclusion is precise: the acquisition mechanism and permitted
preparation dynamics restrict the input laws enough that old response
coordinates already identify every relevant contrast in S. Maintenance
can still change predictions and the best shared complete plan. Its full
physical response is compiled before applying the four-coordinate
boundary restriction.
