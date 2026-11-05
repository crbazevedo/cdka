# Program-family dominance under the reachable contrast cone

This result extends the [reachable-domain theorem](reachable-domain-proof.md)
without changing the acquisition, physical D/R/M kernels, observation boundary,
or mandatory-work grammar. It concerns **one optimal complete program** and
feasibility of a common regret/fidelity guarantee under the same prepaid resource
box. It does not reconstruct every response in the original program library.

## 1. The domain and the order

Let E be the four-by-sixteen matrix whose rows are the signed contrast basis
vectors in `reachable_restriction.CONTRAST_BASIS`. The existing theorem gives

```
mu_1 - mu_0 = -x E,             V_mu(w) = 1/2 + x b(w),
b(w) = -E K_w g.
```

The implementation stores `q(w)=E K_w g=-b(w)` to reuse the existing response
evaluator. Its componentwise comparison is consequently `q(f)<=q(p)`. The sign
convention differs; the certified order and physical values are identical.

Here x is a row vector, b(w) is a column vector, and g is the actual terminal
six-NAND readout response. For the fixed fair-source sensor acquisition with
sensor error between zero and one half, the four entries of x are nonnegative.
The inherited write error is 1/50. The two entries for each health state are
half its health probability, times `(1-2 eta)`, times the positive differences
between the zero-source and one-source write probabilities in cell-count orbits
zero and one. Thus the initial contrast belongs to this cone.

For a in {D,R}, derive A_a by transporting each row of E through the **full**
physical kernel. The checker verifies both identities and inequalities:

```
E K_a = A_a E,                  A_a[i,j] >= 0.
```

It follows that x becomes x A_a after an ordinary preparation update, and
remains nonnegative. This is an inductive assertion for every finite D/R
history, not a fitted property of the four-history fixture. Nonnegative mixtures
of these preparation laws also satisfy it. The cone is an evaluator domain;
its coordinates are not extra observations supplied to the controller.

Define r to dominate s when `r[i] >= s[i]` for all four coordinates. Then
`1/2+x r >= 1/2+x s` for every input in the cone. Also

```
b(a w) = A_a b(w),
r >= s  implies  A_a r >= A_a s.
```

Consequently a supplied componentwise dominance inequality remains valid under
every D/R prefix. It certifies an entire family of complete words without
constructing each prefixed response.

This is an order on responses over a restricted input domain. It is neither
componentwise dominance on all sixteen physical states nor a Markov quotient
that permits maintenance to propagate four-coordinate states.

## 2. A recurrence that respects the maintenance boundary

Let P_n contain every complete word with exactly n D/R updates and at most one
additional M. Its size is `(n+2) 2^n`. Let S_n contain the full sixteen-coordinate
responses `K_v g` for **every** v in {D,R}^n. The recurrence retains S_n without
cone pruning because these responses may later receive M on their left.

A retained set F_n consists of actual complete words and their four-coordinate
responses. It must dominate P_n: for every p in P_n, some f in F_n has
`b(f) >= b(p)`. Start with candidates I and M at n=0. At a later level form only

```
C_n = { a f : a in {D,R}, f in F_(n-1) }
      union { M v : v in {D,R}^n }.
```

The first family uses A_D or A_R on the retained four-coordinate responses.
For the second family, compute the exact physical contraction `-E K_M (K_v g)`.
It can be implemented by first propagating M in sixteen coordinates and then
restricting, or by precomputing the four-by-sixteen matrix `B=E K_M` and
contracting it with the still sixteen-coordinate suffix response. The checker
verifies all four rows of this identity. B is **not** a four-by-four maintenance
operator and does not discard post-maintenance distinctions. Select a subset F_n of C_n that dominates every
candidate. A Pareto search is one discovery procedure; the soundness theorem
only needs the supplied dominance assignments.

**Coverage proof.** At level zero both legal words are candidates. Suppose the
claim holds at n-1. A legal word p in P_n either begins with M or begins with
D/R. In the first case p=Mv with v containing exactly n ordinary updates and
no M, so p is an explicitly constructed seed. In the second case p=a u with
u in P_(n-1). By induction there is f in F_(n-1) with b(f)>=b(u). Positivity
gives b(a f)>=b(a u), so a constructed candidate dominates p. Finally its
assigned representative in F_n dominates that candidate. Transitivity completes
the induction. No member of the rejected prefix families is needed by this
argument or by its checker.

The first nontrivial supplied witness is MD dominated by DM. In the stored
q convention, all four entries of `q(MD)-q(DM)` are strictly positive. Hence
every `uMD` is covered by `uDM` for an arbitrary D/R prefix u. At K=8 the
128 such words with prefix length seven are never constructed. This concerns
these terminal suffixes; it is not an unrestricted rewrite of every occurrence
of MD inside a word with further actions afterward.

It is safe for a frontier to contain both zero-M and one-M words. The recurrence
only prefixes a frontier member with D/R. Every newly prefixed M takes its input
from the **unpruned** S_n, never from F_n. Pruning S_n on its four-coordinate
response before applying M would require a separate proof and is not performed.

## 3. Which decisions survive the reduction

For a declared preparation class let `B_h=max_p V[h,p]`. Dominance coverage and
the inclusion F_K subset P_K give

```
max_(p in P_K) V[h,p] = max_(f in F_K) V[h,f] = B_h.
```

If f dominates p, then their regrets and minimum fidelities satisfy

```
R(f) = max_h (B_h - V[h,f]) <= max_h (B_h - V[h,p]) = R(p),
L(f) = min_h V[h,f]          >= min_h V[h,p]          = L(p).
```

The informed maxima, optimal common minimax-regret value, optimal maximin-fidelity
value, and existence of a **single** program satisfying both `R<=delta` and
`L>=tau` are therefore preserved. The earlier same-history regret theorem lifts
these guarantees to the convex hull of the declared preparation laws. It does
not require a free runtime mixture selector or a controller that observes h.

The selected representative is an original executable program. Its physical
cost is charged exactly as before. Replacing p by f may change its actual number
of voter calls or writes, but both must fit the same common prepaid reservation.
If actual execution cost becomes a further objective or a tighter constraint,
the present response-only dominance relation no longer suffices.

Other nonclaims follow directly. Dominated words can still tie on a boundary
input, including the uninformative sensor. The reduced library does not list
all optimal identities or establish uniqueness. Removing inferior responses can
change lower prediction envelopes, so a prediction certificate for F_K is not
a full prediction certificate for P_K. The theorem preserves the stated
decision values and feasibility, not the entire earlier response interface.

## 4. Discovery and checking have different obligations

The certificate specifies the grammar, physical binding, retained candidate
indices and, for every generated candidate, an index of a retained dominator.
The family checker and its decision-certificate composition perform the following
finite tasks:

1. Validate the grammar and the binding to the supplied exact kernels and
   readout. Their derivation from physical traces is a separate inherited
   obligation; a family-certificate hash does not establish physical validity.
2. Verify `E K_a=A_a E` and nonnegativity for D/R.
3. Verify `B=E K_M`, regenerate each required full sixteen-coordinate no-M
   suffix, and form its exact M seed.
4. Regenerate only the D/R children of the preceding retained frontier.
5. Check legal, nonduplicate retained indices and every supplied four-coordinate
   dominance inequality, including complete candidate coverage.
6. In the enclosing experiment, validate the preparation signatures' cone
   membership, evaluate the final representatives, and check the separate
   correlated decision certificate and its witnesses.

Checking does not discover a Pareto frontier and does not generate words covered
only through the induction. It still pays for the unpruned no-M seeds, physical
arithmetic, certificate parsing and decision evaluation. A hash binds inputs;
the identities, inequalities and grammar coverage provide the proof.

## 5. Complexity and the remaining obligation

Writing f_n for the retained frontier size, level n>=1 constructs `2 f_(n-1)+2^n`
candidates, instead of all `(n+2)2^n` legal words. Complete words never generated
at the final level must be counted separately from intermediate candidates,
suffix seeds and comparisons. Pareto discovery can itself be expensive; a small
final frontier is not a sufficient runtime argument.

All `2^n` no-M suffixes remain. The frontier can also grow with the horizon.
This result therefore gives neither a polynomial bound nor a solution to
preparation-history enumeration. Its empirical acceptance requires a total-cost
comparison against a no-pruning compiler using the **same** full suffix sharing
and safe four-coordinate D/R propagation. Historical comparison against the
earlier sixteen-coordinate compiler is secondary. Construction, checking,
encoding, serialization and decision costs must be included for both methods.

## 6. A tempting physical shortcut is false

The principal K=4 optimizers end with M. That does not prove that maintenance
can always be moved to the end. Keep the same acquisition parameters and take
the physically generated history DDDD. For the exact K=1 workload,

```
V(MR) - V(RM)
  = 40138800756772432239466537872536806052590838348827139645969863971
    /135525271560688054250931600108742713928222656250000000000000000000000
  = 0.00029617207399432015... > 0.
```

An earlier repair can help the following physical regeneration. The family
proof retains this behavior by applying M at every legal seed position and
checking response inequalities, rather than imposing an unsupported scheduling
rule inferred from one optimum.
