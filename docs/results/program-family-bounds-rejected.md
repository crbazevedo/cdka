# Residual Bellman bounds: a measured rejection

Three sound bounds eliminate complete-program families before enumeration, but
all three lose on total measured cost in these controls. Fewer generated leaves
and smaller certificates are insufficient reasons to retain a search architecture.
The implementations remain a reproducible negative experiment, not production
optimizers. Results below replace the earlier exploratory timings.

## Fixed workload and bounds

The physical model, paid acquisition, hidden health, faulty NAND voter, and D/R/M
kernels are unchanged. The cohort consists of the four h=2 histories DD, DR, RD,
and RR. A complete program contains exactly K ordinary D/R updates and at most
one additional M. The history identifier remains unavailable to the continuation.
There are 96 programs at K4 and 512 at K6. The objective is one common minimax
program, with informed comparators drawn from the same grammar.

The controls use three increasingly restrictive upper bounds:

- **Physical32:** Bellman envelopes act on the two positive H-indexed physical
  submeasures. They relax the common schedule to choices depending on hidden
  state. This optimistic controller is a proof device and is never executed.
- **Signed16:** source laws are cancelled before bounding. For residual response
  envelopes L≤q≤U and signed contrast d, the upper value is
  `1/2 + d_positive·U + d_negative·L`. Relative to Physical32, this removes the
  nonnegative slack `sum_i min(mu0_i,mu1_i)(U_i−L_i)`.
- **Four/full:** before M, nonnegative weights `x=−contrast4` use the certified
  positive D/R maps and a four-coordinate Bellman envelope. Its M alternatives
  apply the full physical kernel to the signed basis rows. After M, transport
  and bounds use16 entries. Four-coordinate propagation through M is never used.

Each method first discovers every informed maximum by bounded search, then finds
one common minimax program. No informed maximum is supplied by enumeration.
Exact rational comparisons recover the same four maxima and regret as both
enumerators: DRDDM at K4 and DRDDDDM at K6.

## Final control measurements

Sources: [K4 raw results](../data/program-family-bound-control-k4.json) and
[K6 raw results](../data/program-family-bound-control-k6.json). Each file comes
from one fresh process and one pass through the five methods. These are neither
medians nor confidence intervals, and support no universal runtime claim.

All totals include cold shared kernel/preparation setup, encoding, response or
bound compilation, queries or searches, certificate construction, JSON
serialization and parsing, and checking. Shared setup was 0.130940 seconds at K4
and 0.109852 seconds at K6, charged once to every method's inclusive total.

| K | Method | Complete words never formed | Prefix visits | Check seconds | Inclusive total seconds |
|---:|---|---:|---:|---:|---:|
|4|Existing four-coordinate enumerator|0|—|0.012743|0.440885|
|4|Four-coordinate enumerator with shared suffixes|0|—|0.013181|0.281199|
|4|Physical32|55|202|1.168909|2.539563|
|4|Signed16|65|164|0.502422|1.206104|
|4|Four/full|65|161|0.393471|0.949546|
|6|Existing four-coordinate enumerator|0|—|0.089963|3.072715|
|6|Four-coordinate enumerator with shared suffixes|0|—|0.089092|1.253519|
|6|Physical32|382|828|6.722739|14.170975|
|6|Signed16|439|525|2.080319|5.525538|
|6|Four/full|439|525|1.336188|3.209026|

Prefix visits sum the informed and common searches. At K6, the four-coordinate
bound visits exactly the same tree as Signed16. Its cheaper arithmetic helps,
but does not offset prefix propagation and verification. The residual envelopes
still combine incompatible future choices across components; retaining more
contrast structure before M does not remove this post-M obstruction.

The enumerators here produce the broader existing class certificate, including
per-program prediction and regret information. Searches certify one optimum.
This output mismatch biases cost against the enumerators, which nevertheless
win. Therefore these controls are not the primary matched performance comparison.
That comparison is the separate [program-family benchmark](../data/program-family-benchmark.json),
where the frontier and strengthened enumerator return the same compact decision
outputs and receive the same algebraic optimizations.

## Counting and certification

“Never formed” subtracts the union of complete words formed during seeds and
both searches from `(K+2)2^K`. Reaching a prefix with no ordinary updates remaining
already forms a valid word, even when its bound prevents evaluation. Its optional
last-M child is a different word. The raw `family_leaves_pruned` statistic includes
such already formed leaves and must not be substituted for this count.

The checker recomputes bound recurrences, checks attaining witnesses and pruning
inequalities, and verifies recursive grammar coverage without optimizing again.
Serialized search certificates occupy 7,602–8,937 bytes at K4 and 22,099–34,331 at
K6, compared with 118,290 and 756,883 bytes for the broader class certificates.
Those storage savings do not reverse the measured runtime result.

Reproduce from the repository root:

```bash
python -m experiments.program_family_bound_controls --h 2 --k 4
python -m experiments.program_family_bound_controls --h 2 --k 6
```
