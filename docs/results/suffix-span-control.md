# Rejected control: a uniform span-error cover of ordinary suffixes

The uniform span route did not remove enough suffix work to justify approximate
coverage. At an allowed value error of `1/10000`, it retained all 256 ordinary
suffixes at K=8 and 1,023 of 1,024 at K=10. At `1/1000`, it retained 239 and 914,
respectively: reductions of 6.64% and 10.74%. It did not become the production
method. The selected exact route uses horizon-indexed contextual orders; see
[the contextual-cover proof](suffix-context-proof.md).

All original observations, including unsuccessful settings, are in
[suffix-span-control.json](../data/suffix-span-control.json). The
[reproducer](../../experiments/suffix_span_control.py) keeps the original full16
response algorithm and adds explicit contract, binding, shape and witness checks.
The historical timings have not been replaced with measurements of that cleaned
implementation.

## Contract and exact acceptance

The control uses the inherited sixteen-state D/R/M kernels, one fair hidden
source, the same actual terminal readout, exactly K ordinary updates and at most
one additional M. Every retained representative is an actual program word.
There is no physical-model change, free observation or four-dimensional M
transition. Ordinary suffix responses remain full sixteen-coordinate vectors.

For two responses q and r, write

\[
\operatorname{sp}(q-r)=\max_i(q_i-r_i)-\min_i(q_i-r_i).
\]

At each of K ordinary levels, the local allowance is
\(\delta=\epsilon/K\). A proposed replacement is accepted only when the exact
rational inequality \(\operatorname{sp}(q-r)\le 2\delta\) holds. Floating-point
values screen proposals; they cannot authorize a merge. A screening false
negative merely retains an additional candidate. The supplied checker reconstructs
the same physical responses and verifies every replacement with rational
arithmetic, without repeating proposal search.

The existing positive four-coordinate family cover handles complete programs
outside the ordinary-suffix loop. Its dominance checks remain exact. M seeds
are computed with the full physical boundary \(E K_Mq\). The certificate binds
the physical operators, terminal, horizon, allowed error and grammar; it rejects
empty or malformed covers and noncanonical or inexact rational inputs.

## Why the ledger is valid

Every physical kernel in this control is stochastic. Each coordinate of Kd is
a convex combination of the coordinates of d, so
\(\operatorname{sp}(Kd)\le\operatorname{sp}(d)\). This applies to M as well as
D/R. The checker requires row mass exactly one: general substochastic kernels
do not support this argument, because a constant observable need not remain
constant.

For a fair source, the physical submeasures \(\mu_0\) and \(\mu_1\) each have
mass 1/2. Their contrast \(\nu=\mu_1-\mu_0\) has total mass zero and
\(\|\nu\|_1\le1\). Subtracting the midpoint of the range of d therefore gives

\[
|\nu d|
\le \tfrac12\operatorname{sp}(d).
\]

An accepted local replacement consequently changes any such source's physical
value by at most \(\delta\), including after any physical prefix. If
\(e_n\) is the sum through level n of the largest actual local span/2 at each
level, the triangle inequality and stochastic contraction give

\[
e_n\le n\delta\le\epsilon.
\]

The JSON `uniform_error` field records this exact rational ledger. It is a
uniform upper bound, not a measured error over a finite preparation sample.

The outer positive cover may improve a representative rather than approximate
its value symmetrically. Its relevant conclusion is one-sided: for every legal
complete program p, some retained actual program r satisfies
\(V_i(r)\ge V_i(p)-e_K\) simultaneously on every fair physical preparation in
the inherited negative contrast cone. D/R preserve that input domain; the
ordinary-suffix span bound also survives the full M boundary. Thus the nested
recurrence retains this coverage statement.

For completeness, this gives a bound on choosing a minimax-regret plan from the
retained set. Let \(b_i\) and \(\widehat b_i\) be the informed optima over all
legal programs and over the retained programs. Because the latter are actual
programs and cover the former within \(e_K\),
\(0\le b_i-\widehat b_i\le e_K\). A representative of a true minimax-regret
optimizer incurs at most \(e_K\) additional regret against \(b_i\). Choosing
the retained optimizer against \(\widehat b_i\) contributes at most another
\(e_K\) when its regret is evaluated against \(b_i\). Hence

\[
R_{\rm full}(\widehat p)\le R_{\rm full}^{*}+2e_K
\le R_{\rm full}^{*}+2\epsilon.
\]

This is an approximation guarantee. It does not establish exact fidelity
thresholds, exact joint feasibility or preservation of all tied programs.

## Preserved observations

The following times are **single concurrent exploratory observations**, in
seconds. Imports, physical kernel/probe construction and serialization were
outside the timers. The reference recorded compilation only; its checker was
not timed. These observations preceded the stronger PF8 baseline and are
excluded from the central end-to-end comparison. The error column is a decimal
display of the exact rational ledger stored in the data file.

| K | Allowed epsilon | Retained ordinary suffixes | Actual ledger bound | Control compile | Control check |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.00001 | 16 / 16 | 0 | 0.024260 | 0.022657 |
| 4 | 0.0001 | 16 / 16 | 0 | 0.023413 | 0.023052 |
| 4 | 0.001 | 16 / 16 | 0 | 0.022956 | 0.022925 |
| 6 | 0.00001 | 64 / 64 | 0 | 0.094487 | 0.092554 |
| 6 | 0.0001 | 64 / 64 | 0 | 0.100086 | 0.099825 |
| 6 | 0.001 | 62 / 64 | 0.0000962399 | 0.093164 | 0.092629 |
| 8 | 0.00001 | 256 / 256 | 0 | 0.484236 | 0.465215 |
| 8 | 0.0001 | 256 / 256 | 0 | 0.484459 | 0.429744 |
| 8 | 0.001 | 239 / 256 | 0.0002968783 | 0.452841 | 0.453633 |
| 10 | 0.00001 | 1,024 / 1,024 | 0 | 2.724805 | 1.906217 |
| 10 | 0.0001 | 1,023 / 1,024 | 0.0000074228 | 2.685268 | 1.966696 |
| 10 | 0.001 | 914 / 1,024 | 0.0004386713 | 2.418421 | 1.799474 |

The contemporaneous full16 family compiler took 0.024485, 0.090704, 0.396164
and 1.954312 seconds at K=4,6,8,10. No speedup is inferred from these noisy,
incomplete timings. The span compiler was slower in the recorded K=8 and K=10
settings even before adding its certificate check.

The existing family method already avoided constructing many legal complete
programs. At K=8 it constructed 542; the `epsilon=1/1000` span control constructed
513, only 29 fewer. At K=10 the corresponding counts were 2,090 and 1,896,
only 194 fewer. Its total avoided-program count must not be presented as an
incremental gain over the current family method. The final frontier cardinalities
were unchanged in every tested epsilon setting: 10, 11, 17 and 27 across the
four horizons. Cardinality equality is not a proof that the retained words or
their exact decision values coincide.

## Reproduction and retained check

Run the bounded exact sanity case:

```sh
python experiments/suffix_span_control.py
```

It checks a float-screened proposal lying strictly beyond the exact boundary,
stochastic contraction, rejection of a substochastic kernel, certificate replay,
and physical coverage and the regret bound against all K=3 legal programs for
the four length-two preparation histories. The positive-error case actually
merges a suffix; the zero-error case retains all eight. This finite comparison
is a regression check of the implementation, separate from the uniform argument.

Reproduce all exploratory parameter settings explicitly:

```sh
python experiments/suffix_span_control.py --sweep
```

This prints new measurements; it does not overwrite the preserved historical
record. The control remains rejected because its exact acceptance test yields
negligible compression at the tighter tolerance and limited compression at
the looser tolerance while introducing approximate coverage and proposal cost.
