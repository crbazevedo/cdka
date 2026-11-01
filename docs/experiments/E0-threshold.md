# E0 — Exact finite checks for action compatibility

**Objective:** independently verify B1 and the globally stable plant example T1. These checks do not establish novelty.

## Design

- Exhaustive enumeration of all 2^9=512 safe-action binary relations with three worlds and three actions.
- Solver A enumerates subsets of actions (set cover). Solver B enumerates partitions of worlds into message classes with nonempty intersection of safe actions. Assert equality.
- Exercise edges λ=0, 0.5, immediately above 0.5, 2.5, immediately above 2.5.
- Track incompatibility of triples despite pairwise compatibility.

## Acceptance

- Every 3×3 relation agrees between independent algorithms, including infeasible cases.
- T1 exact threshold equalities are correct, and equilibrium stability is analytically justified (Jacobian -1).
- Reproducibility uses only Python standard library and succeeds via \`python -m unittest discover -s tests -v\`.

## Exclusions

No stochastic LDP, autonomy experiment, information-metric novelty, or model of endogenous sensors/actuators is established by E0. Extend E0 only once T2 conditions are precisely declared.

## E0.1 — Completed additional checks

- Finite-horizon threshold shift at \`T=ln2\`: 2 and 4.
- Adding \`u=0\` reduces worst-case memory at \`λ=1\` from one bit to zero.
- Invalid horizon and action parameters rejected.
- Total local baseline unit tests: **11 passing**.
