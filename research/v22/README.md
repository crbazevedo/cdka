# V22 — Learned representation choice, numerically enclosed answer

The portfolio chooses between the two v21 regenerative algorithms BEFORE solving. Its cost predictor is fitted only on24 Meeting calibration cases, frozen by hash, and evaluated on48 generated held-out instances: sequential, dense and rare-event families. A separate same-host CI replication regenerates all raw evidence; it does not reuse timings from the prior local package.

## Numerical contract

Inputs are exact rational Markov probabilities satisfying the rank-one restart contract. Both formulas run in outward-rounded dyadic intervals using arbitrary-size integers. For probability p in[l,u], the returned rational midpoint m satisfies the requested tolerance whenever

    (u-l)/2 <= atol + rtol*l.

Then |m-p|<=atol+rtol*p. Default atol=0,rtol=1e-8. Start64 dyadic-resolution bits, increase32, refuse if512 bits are insufficient. The returned rational bounds, not their float display, are authoritative. Zero may need a structural certificate. This is numerical containment for the specified model, not a confidence interval for real-world parameter uncertainty or a theorem-prover verification of Python.

A deliberately bad cost predictor can waste time but cannot authorize an inadequate interval. Thus learned selection and answer validity are separated. No universal time-competitive bound is inferred from the benchmark.

## Executed local study (separate source package/host)

24 training/48 holdout;46/48 fastest-backend selections. Sum of timing medians:.450218s portfolio,.693665s fixed histogram,1.294835s fixed subset. Approximate geometric slowdown1.0115 against a retrospective best-of-two oracle, descriptive with3 repeats. All48 answers meet relative tolerance;24 have additional exact rational answers. A rare probability2.4644388122664e-31 produced2.22e-16 in the old floating inclusion-exclusion baseline WITH its conditioning warning. The enclosure correctly refines to160 bits; an even rarer6.2154e-49 case uses224 bits in this absolute dyadic grid.

The complete local artifact contains15 new tests and22 inherited regressions, raw timings, frozen hashes and dashboard. This repository mirror has a compact independent9-test suite and repeats calibration/evaluation on the runner. Do not mix the two timing environments or inherit v21 Storm speedups.

## Reproduction

```sh
cd research/v22
python -m pip install numpy==2.3.5 scipy==1.17.0
OPENBLAS_NUM_THREADS=1 python experiments/study.py train
OPENBLAS_NUM_THREADS=1 python experiments/study.py evaluate
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
```

Validation, selection and every precision retry are included. Input construction/imports excluded equally. Three rotating-order repetitions. Heldout data are generated, not a new independent public application corpus. There is no new Storm run in this increment.

The local package vendors v21 artifact blob cd799239df2482198cebdfe315d0358258806450; this mirror reuses published v21 blob94630af184b0291bc31c8841325c621c24c8a214. Same model/API contract, separately recorded code and independently tested replication.

## Impact and antecedents

Concrete contribution: a sound selection interface joining regenerative structure, bounded representations, adaptive precision and a frozen evaluation, with outcome-independent validity. Algorithm selection (Rice1976) and directed numerical verification (Hartmanns, TACAS2022, arXiv2110.08785) are enabling instruments. New work is the class-specific compiled combination, not a claim to invent interval arithmetic or portfolios.

Next gate: recognize structure in independent public models; compare official sound/exact configurations at matched accuracy; optimize positive enclosures with normalized exponents. Do not open another physical-device family before external coverage and a concise paper.
