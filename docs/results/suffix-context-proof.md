# Finite-context dominance for ordinary suffixes

**5 November 2026.** Parent checkpoint:
`ce252821be4fb5a5075ad12f71ee2da7f14acb7d`.

This result extends the [program-family cover](program-family-proof.md) at its
remaining exhaustive boundary: the ordinary suffixes to which maintenance may
later be prefixed. It preserves the inherited acquisition, hidden shared health,
actual six-NAND voter, D/R/M kernels, observation boundary, mandatory workload,
and prepaid resource box. It introduces no observation or physical operation.

The claim is a sufficient, independently checkable cover for a declared finite
horizon. Every representative is one original executable word. The proof does
not require constructing every ordinary suffix, but neither a fixed observer
dimension nor this induction bounds the certificate or frontier polynomially.

## 1. The maintenance boundary and the exact observer

Use column responses and row evaluation functionals. Let `g` be the actual
terminal readout, `K_w` the physical kernel product for word `w`, and `E` the
four-by-sixteen matrix `CONTRAST_BASIS`. Write

```
q(w) = E K_w g,
B    = E K_M.
```

The inherited reachable-domain theorem gives `mu_1-mu_0=-x E`, with `x>=0`,
and hence `V_mu(w)=1/2-x q(w)`. A componentwise smaller `q` is therefore at
least as good for every preparation in that cone. The checked identities

```
E K_a = A_a E,             A_a >= 0,             a in {D,R}
```

preserve this order under ordinary prefixes. There is no corresponding assumed
four-by-four maintenance transport. The exact boundary remains the full
four-by-sixteen row matrix `B`.

For efficient ordinary suffix propagation, take a fixed eight-by-sixteen signed
row matrix `O` and verify the following identities in all sixteen physical
coordinates:

```
O K_a = T_a O,             a in {D,R},
E     = U O,
B     = J O,
z_0   = O g.
```

Then the eight-component response `z(w)=O K_w g` satisfies

```
z(a w) = T_a z(w),         q(w) = U z(w),
q(M w) = J z(w).
```

These conclusions hold for every ordinary word by induction on its length.
The proof uses full row identities, not agreement on sampled response columns.
Neither `T_a`, `U`, nor `J` is assumed nonnegative. Their entries may be signed;
the observer itself does not establish a dominance order.

The first four rows of O are the original exchangeable antisymmetric rows E.
For a bit subset S, define `W_S(bits)=(-1)^(sum_(j in S) bits[j])/8`. Its other
four rows are `(v,-v)` across the healthy and degraded blocks, for

```
v = W_empty,
v = W_{0} - (W_{1}+W_{2})/2,
v = W_{0,1}+W_{0,2},
v = W_{1,2}.
```

These fixed rows are independent and supply a stable basis even in the
zero-repair control. The exact identities, including the signed transports,
are checked in [suffix_features.py](../../cdka/suffix_features.py).
The portable certificate calls O `C` and J `V`. This construction is a dual
linear observer: its coordinates are evaluations of signed rows,
not probabilities of eight physical states. No claim that maintenance preserves
this observer space is needed. Only its boundary rows `B` must have the stated
representation. In particular, it is not the earlier eight-orbit state
projection, whose maintenance closure is false.

The same observer must be supplied to the existing program-family baseline.
Its arithmetic savings and the savings from suffix pruning are separate claims.

## 2. A finite ladder of context cones

Fix the number `K>=0` of ordinary D/R updates. Let `C_t` be a finite matrix of
signed rows in the observer's eight-coordinate space. Each row is a context
functional acting on `z(w)`. Set `d=max(0,K-1)`. At every horizon, including
K=0 and K=1, require `J=H C_0` with `H>=0`. For `0<=t<d`, also require

```
rows(C_t) are contained in rows(C_(t+1)),
C_t T_a = L_(t,a) C_(t+1),          L_(t,a) >= 0,   a in {D,R}.
```

The implementation also supplies nonnegative witnesses for `U` in `C_0`.
That is a safe strengthening. Containment of `J` alone is sufficient when this
suffix library supplies only maintenance seeds and the outer frontier retains
ordinary words through its own recurrence.

For ordinary words `s,v`, define `s <=_t v` by

```
C_t z(s) <= C_t z(v)                 componentwise.
```

All context rows must be satisfied by the **same** word `s`. The conic
coefficients combine evaluation functionals for the proof; they do not combine
programs or grant a randomized controller. Two consequences are immediate:

1. **Shrinking-context extension.** If `s <=_(t+1) v`, then
   `a s <=_t a v`, because multiplication by `L_(t,a)>=0` preserves each
   inequality.
2. **Maintenance soundness.** If `s <=_t v`, then `q(Ms)<=q(Mv)`, since
   `C_0` is included in `C_t` and `J=H C_0` with `H>=0`.

Ordinary prefixes outside M are handled by the separate positive matrices
`A_a`. The context ladder handles ordinary letters inserted between M and the
stored suffix. Keeping these two boundaries distinct avoids assuming closure
of the original reachable contrast through maintenance.

### Constructing and checking the ladder

Store one row list and increasing prefix lengths
`r_0<=r_1<=...<=r_d`, with `C_t` equal to its first `r_t` rows. For the rows
newly introduced at level `t`, express each D/R image as a nonnegative rational
combination of rows available by level `t+1`; add an image as a new row if no
accepted combination is found. Transitions of older rows need not be repeated:
their existing witnesses remain valid in every later, larger prefix.

One transition witness per row is sufficient only when its indices are bounded
by the next prefix after that row's birth. Merely checking that indices refer
somewhere in the final row list is insufficient: it would allow an earlier
context to depend on a row not yet certified at the required horizon.

Numerical linear programming may propose a support for conic membership.
Acceptance requires reconstruction of exact rational coefficients, their
nonnegativity, and the exact row identity. If reconstruction fails, discovery
adds the row instead. A numerical false positive cannot become a certificate;
a false negative can increase construction cost without affecting soundness.
Row normalization may divide by a positive factor. An arbitrary sign change
would change the cone and is not an admissible normalization.

This discovery expands generators, not all context words. A row already
covered by a positive combination creates no separate descendants: linearity
and the checked transitions transport its combination. Nevertheless, the
number of necessary generators can grow rapidly. Their construction, support
search, rational size, serialization and checking remain charged work.

## 3. Nested suffix and complete-program covers

Let `W_n={D,R}^n`. Let `P_n` contain all words with exactly `n` ordinary updates
and at most one additional M, so `|P_n|=(n+2)2^n`. A suffix frontier `S_n`
contains actual words in `W_n` and their exact observer responses. An outer
frontier `F_n` contains actual words in `P_n` and their four-coordinate responses.

Start with `S_0={I}`. For `n=1,...,K`, generate only

```
G_n = {a s : a in {D,R}, s in S_(n-1)}.
```

Retain a subset `S_n` with a supplied cover of every member of `G_n` under
`<=_(K-n)`. The order is indexed by the remaining extension allowance; it is
not a single fixed-order Pareto recurrence.

**Suffix coverage.** For every `1<=n<=K` and every `v in W_n`, there is one
`s in S_n` with `s <=_(K-n) v`.

At `n=1`, the two words D and R are both generated from I, so their supplied
cover proves the assertion directly. For `n>=2`, write `v=a u`. By induction,
some `s in S_(n-1)` satisfies `s <=_(K-n+1) u`. Shrinking-context extension
gives `a s <=_(K-n) a u`. The generated word `a s` is then covered by one
member of `S_n` in that same order. Transitivity proves the claim. This is why
depth `K-1`, rather than `K`, is sufficient: the first expansion is exhaustive
over its two children and consumes no preceding suffix-dominance assertion.
For `K=0`, only the exact base word I is needed.

Construct the outer frontier as follows. At level zero, cover `{I,M}` under
componentwise four-coordinate order. At level `n>=1`, generate only

```
Q_n = {a f : a in {D,R}, f in F_(n-1)}
      union {M s : s in S_n}.
```

Use `A_a` on the first family and the exact bridge `J z(s)` on the second.
Retain a subset `F_n` with a supplied componentwise cover of every candidate.

**Complete-program coverage.** Every `p in P_n` has a representative
`f in F_n` with `q(f)<=q(p)`, for all `0<=n<=K`.

The base is direct. If `p=Mv`, suffix coverage and maintenance soundness give
a constructed seed `Ms` with `q(Ms)<=q(Mv)`. If `p=a u`, the induction for
`F_(n-1)` and `A_a>=0` give a constructed `a f` with `q(af)<=q(au)`.
The supplied cover of `Q_n` finishes either case. For `n=0`, M uses the
unmodified base suffix. No maintenance is prefixed to a member of `F_n`;
therefore this recurrence cannot introduce a second M.

No step of this proof assumes an already enumerated map from all `2^n` suffixes
to representatives. The map exists by composition of the finite supplied
covers and the induction. Discovery and checking regenerate only the retained
frontiers' children.

## 4. Preserved decisions and limits

Since `F_K` is a subset of the original executable library and covers every
word for every preparation in the reachable contrast cone, it preserves the
informed best value for each preparation. Replacement by a dominating word
cannot increase its same-history regret or reduce its fidelity. Thus the
original program-family consequences remain valid: optimal common minimax
regret, optimal maximin fidelity, and existence of a **single** program meeting
both a regret limit and a fidelity floor are preserved. The inherited
same-history argument also covers mixtures of declared preparation laws.

Representatives satisfy the same mandatory ordinary workload and at-most-one-M
grammar. Their R count or actual physical operation count may differ. This
result uses the common prepaid resource box; it does not establish dominance
when actual execution cost is an additional objective or tighter constraint.

The cover need not preserve every tied optimizer, every inferior response,
prediction envelopes, or uniqueness. Preparation-history enumeration remains
outside this result. A theorem about one finite `K` does not authorize reusing
its ladder for a larger horizon without new transition witnesses and covers.

## 5. What the independent checker must establish

The certificate binds the exact supplied physical kernels, terminal readout,
ordinary-update count and grammar. Binding prevents reuse on different inputs;
it does not replace the inherited physical derivation or the following checks.

1. Verify the observer identities in sixteen coordinates, and the four-coordinate
   positive D/R transports and exact maintenance bridge.
2. Parse exact canonical rationals. Reject floats and booleans used as rationals
   or indices, malformed row widths, invalid counts, and missing witnesses.
3. Require every initial context witness, a nonempty row family, nondecreasing
   positive prefix lengths, and exactly the required transition witnesses.
   Verify the nonnegative coefficients, birth-level index bounds and identities.
4. Require `K+1` program layers and the canonical base suffix cover. At each
   level, regenerate the two children of each retained suffix and each retained
   outer program, then form the required maintenance seeds.
5. Check every supplied cover assignment against its actual generated response,
   with legal nonduplicate kept indices and complete candidate coverage.
6. In the enclosing experiment, check preparation cone membership and the
   separate correlated decision certificate and feasibility scan.

Checking uses neither linear programming nor a new Pareto search. It must work
on a serialized-and-parsed certificate, reject malformed data explicitly, and
remain sound when Python assertions are disabled. Discovery dependencies can
remain optional and lazily imported. Discovery statistics do not substitute for
checked identities or become theorem claims merely by appearing in metadata.

### Empty-cone regression

Review found a concrete flaw in the first scratch checker. It zipped the eight
required initial rows with a supplied witness list without checking its length.
The payload `rows=[]`, `initial=[]`, `counts=[0]`, `transitions=[]` therefore
passed at depth zero. At `K=1`, all suffix feature vectors became empty, so
componentwise comparison accepted any pair vacuously. The prototype returned
`{D,R,DM,RM}`, although legal MR had no four-coordinate dominator in that set.

This is a coverage failure, not a numerical tolerance issue. Rejection of that
payload is a required regression, together with truncated initial witnesses,
decreasing counts, future-level witness indices and missing program layers.
The finite-horizon theorem above requires all of these structural obligations;
a collection of locally true identities with missing cases is not its proof.
The implementation is [suffix_contexts.py](../../cdka/suffix_contexts.py);
the [adversarial and physical regressions](../../tests/test_suffix_contexts.py)
check both this rejection and the common-representative coverage independently.

## 6. Two exact obstacles to stronger shortcuts

### Four-coordinate dominance does not survive M

Under the inherited default parameters, take ordinary words

```
p = RDDRRD,                q = RDRDDR.
```

Exact physical propagation gives strictly negative first and second entries and
zero third and fourth entries in `E(K_p g-K_q g)`. Thus p dominates q on the
entire original reachable contrast cone. In `B(K_p g-K_q g)`, however, the
first two entries are negative and the last two positive. With the original
sensor error `1/10`, initially healthy acquisition and preparation history
`D^32`, the exact differences have opposite signs:

```
V(p)-V(q)    =  0.000003656478196408728...,
V(Mp)-V(Mq)  = -0.00000015774769181492694... .
```

The decimals report exact rational computations. This pair refutes preservation
of the E order through M. It does not by itself show that an entire optimizer
using the unsafe shortcut would choose the wrong global optimum: another
retained word might cover both members of this particular pair. `D^32` is an
explicit physically reachable witness, not a shortest-history theorem over
all D/R preparations.
The [structural controls](../../experiments/suffix_context_controls.py) preserve
the exact rational differences and reproduce the counterexample using only
standard-library arithmetic.

### An all-horizon context cone forces two equalities

For the default repair success `4/5`, let `C_infinity` be any topologically
closed cone of sixteen-coordinate row functionals containing the four rows of
`B` and invariant under right multiplication by D and R. This includes the
closed conic hull of every ordinary context `B_i K_u`. The following exact
obstruction limits, but does not rule out, pruning with a universal context order.

Put `h=19/20`, `lambda=24/25`, and

```
a = 4594792765036971255543 / 4882812500000000000000,
b = 3297616227072 / 3814697265625,
0 < b < a < h < 1.
```

Here a and b are the traces of the healthy and degraded two-by-two diagonal
blocks of `A_R`. With B row indices starting at zero, define

```
v = B_2 K_R (K_R-a I)(K_R-b I) / [h(h-a)(h-b)].
```

Exact row arithmetic verifies `v K_R=h v`. Consequently the cyclic row space
generated by `B_2` is annihilated by the square-free polynomial
`X(X-a)(X-b)(X-h)`. Its roots have the displayed strict ordering. The polynomial
in the definition of v is the projection onto the h eigenspace on that cyclic
space, so

```
B_2 K_R^m / h^m  ->  v.
```

This argument needs no assertion about the spectrum of the full physical R
operator. Closedness and invariance put v in `C_infinity`.

For a bit subset S, let `s_(z,S)` be the Walsh coefficient of a signed row in
health block z. Independent bit errors and the physical health transition give
after m applications of D

```
s_(0,S)(m) = (h lambda^|S|)^m s_(0,S)(0),
s_(1,S)(m) = lambda^(m|S|)
             [s_(0,S)(0)+s_(1,S)(0)-h^m s_(0,S)(0)].
```

Both `B_0` and v have total mass zero. After division by `lambda^m`, the
degree-zero health difference decays because `h<lambda`; every degree at least
two decays because `lambda<1`. Healthy degree-one terms also decay. If the
three total first-degree coefficients all equal gamma, the limit is gamma w,
where w is zero in healthy states and has degraded entries

```
w(1,bits) = [(-1)^bits[0]+(-1)^bits[1]+(-1)^bits[2]] / 8.
```

Exact calculation gives gamma=2 for `B_0`, whereas for v it gives

```
beta = -97789249826403799024011653198517846528
        / 736008414410103325506140176870361328125 < 0.
```

Thus both w and -w belong to `C_infinity`. Invariance also puts `w K_R` and
`-w K_R` there. Their two-dimensional span is exactly the span of the two
degraded rows of E; explicit coordinates are

```
E_2 = (-49/288) w + (3814697265625/2147235028992) w K_R,
E_3 = (817/288) w - (3814697265625/2147235028992) w K_R.
```

This span lies in the cone's lineality, the set of rows whose negatives also
belong to it. Therefore an inequality against every row of `C_infinity` forces
equality of both degraded contrast responses. Any universal-context cover of
ordinary words must retain at least one representative per distinct degraded
response pair. Exact finite enumeration yields 67 such pairs at K=8 and 272
at K=12. Those are finite lower bounds, not an asymptotic growth theorem and
not proof that every form of all-horizon pruning is impossible.

The [observer regressions](../../tests/test_suffix_features.py) verify the
finite row identities behind the limits. The structural controls additionally
compute the finite class counts by the closed two-coordinate degraded-response
recurrence, deduplicating exact pairs at every level. They need not construct
every complete word or approximate an infinite limit numerically.

Finite ladders have a declared remaining context allowance and need not include
these limiting directions. That is the reason the finite-horizon order can
identify more dominance than one context cone required to work for all lengths.

## 7. Cost obligations

Writing `s_n=|S_n|` and `f_n=|F_n|`, a nonzero level constructs
`2 s_(n-1)` suffix candidates and `2 f_(n-1)+s_n` outer candidates. Count
distinct constructed word labels by their union: a no-M word can occur in
both candidate families. Final complete programs never generated, all
intermediate candidates, retained words, and context-generator work are
different quantities.

The method must pay for the physical setup, observer construction and checking,
context discovery, exact witness recovery, program discovery, response
evaluation, certificate encoding/serialization/parsing/checking, and requested
decision outputs. Report rational bit lengths and serialized bytes separately
from timings and any resident-memory measurement. Reuse can amortize setup
only under the explicitly bound model and horizon; report fresh use separately.

The comparison is against the accepted program-family cover with the same
eight-coordinate observer, the same cached algebra and the same outputs. A
large reduction in suffixes does not by itself establish a total-cost gain.
Frontiers, context rows and rational coefficients may grow with K. This proof
therefore supplies no polynomial or subexponential complexity bound, no
universal runtime advantage, and no reduction of preparation enumeration.
