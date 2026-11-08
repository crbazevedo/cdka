# CDKA v21 — Noncommuting common-reset verification

This research branch adds a new exact structural specialization. It does not overwrite the CDKA main corpus or transfer v20 speedups to a new algorithm.

## Class

Heterogeneous independent local draws conditional on an exogenous common binary Markov history. A work tick advances each local task. A reset tick sends every unfinished local state to the same local initial distribution while preserving completion. Initial law is a product of those restart laws. Local goals are absorbing; the global goal is their conjunction.

Work/reset operators generally fail even goal-relative commutation. The new response statistic is the histogram of positive work-run lengths. Resets consume one time step; achievements completed before a reset are not lost. Histories with the same histogram can have different probabilities: the evaluator sums their true Markov weights using transition-count and run-composition factors.

For horizon H, there are p(H+1)-1 possible nonempty histograms, where p is the integer partition function; the all-reset case is separate. For fixed local state size, arithmetic time is O(N H + H^2 + N p(H+1)), subexponential in H and linear in N, not polynomial jointly in both. Production is float64 logarithmic evaluation, not certified numeric intervals. Fractions provide exact independent oracles.

## Reproduction

```sh
cd research/v21
python -m pip install numpy==2.3.4 stormpy==2.0.0
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python experiments/benchmark.py official
```

22 tests cover exact history weights, product-state dynamics, regenerative formulas, a second informed subset/renewal algorithm, Markov edge cases, task-relative noncommutation, conservative full-file PRISM parsing and refusal conditions.

## Competitive protocol

The focused workflow runs the committed implementation, Storm sparse, Storm sparse with strong bisimulation, Storm symbolic, and an informed renewal/inclusion-exclusion baseline on the SAME generated PRISM files. Three fresh subprocesses; alternating method order; threads fixed to one. Read/parse/certify-or-build/check are inside the main time; initialization, RSS and all raw logs are preserved. Timeout is explicit. Any mismatch or execution error is reported, not removed from the table.

The common-reset family is our extension of public Meeting parameter pairs, not an unmodified external benchmark. The original twelve-component source and MIT license are retained. Extended N>12 cases use new distinct synthetic pairs, not a claim of published instances.

Official results are only established when this run completes and evidence/official/results.json exists with successful status. They are not inferred from local tensor timing. No general SOTA claim is made from a narrow favorable family.

## Next decision

Compare run-histogram evaluation against subset-renewal evaluation as N/H vary. Report regions where each loses. Seek a rank-r regeneration boundary or finite response algebra only after the rank-one contract and complete weights are verified. R11/R14 remain the two foundational branches; this is a competitive evaluation instrument.
