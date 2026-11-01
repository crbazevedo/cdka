# T1 — Informational threshold without an attractor bifurcation

**Status:** proved illustrative example; novelty unestablished, not a general theorem.

## Physical system (stronger than a static map)

A continuously evolving, globally stable linear system with hidden context `w∈{-1,+1}`, static action `u∈{-1,+1}` chosen at t=0 and held constant, parameter `λ≥0`, and initial `x(0)=0`:
\[
\dot x(t)=-x(t)+\lambda w+u.
\]

There are no later observations or action updates. The requirement is uniform infinite-horizon safety:
\[
|x(t)|\leq 3/2\qquad\forall t\geq0.
\]

For every (w,u,λ), the unique equilibrium `x*=λw+u` is globally exponentially stable, with linearization eigenvalue -1. Its location changes smoothly with λ, and its number/stability do not change: **no attractor bifurcation**.

The exact trajectory is `x(t)=(λw+u)(1-e^{-t})`. Therefore infinite-horizon safety is equivalent to `|λw+u|≤3/2`.

## Proposition and proof

Let k(λ) be the minimum number of distinct action labels needed by a deterministic zero-error encoder/decoder with perfect knowledge of w at encoding time.

\[
k(\lambda)=
\begin{cases}
1,&0\leq\lambda\leq 1/2,\\
2,&1/2<\lambda\leq5/2,\\
\infty,&\lambda>5/2.
\end{cases}
\]

For w=+1, action u=-1 is safe iff λ≤5/2, while action u=+1 is safe iff λ≤1/2. For w=-1 the roles of u are reversed. Hence a common action exists for λ≤1/2; otherwise each context requires its opposite action until λ=5/2; above that point neither action is safe in either world. B1 gives the minimum code sizes. QED.

The corresponding **fixed worst-case memory** is 0 bits, 1 bit, or infeasible.

This is not a discontinuity in Shannon entropy H(W) (which stays 1 bit under a fair context prior), nor an attractor bifurcation. It is a change in **action compatibility relative to a safety requirement**.

## Restrictions and negative controls

- The action is committed at t=0. If later observations or fast switching are allowed, the memory requirement may change.
- For a finite horizon T, the threshold is different since `|x(T)|=(1-e^{-T})|λw+u|`.
- If actions are continuous, u may compensate w over a larger region.
- If safety is relaxed or sensor/action boundaries change, thresholds shift.
- This is a **demonstration**, not evidence that physically distinct knowledge states "emerge" from the ODE.
- No explicit intelligence, semantics, or autonomy follows from this calculation.

## Reproduce

```bash
python -m unittest discover -s tests -v
python -m experiments.threshold_sweep
```

Next: derive stochastic viability sets from asymptotic action barriers (T2), then introduce resource-dependent sensing/action availability (T3/T4).


## Extension E0.1 — Time and actuator authority substitute for memory

For a fixed **finite** horizon T>0, `|x(t)|` increases monotonically toward the equilibrium magnitude, so safety is equivalent to

\[
|\lambda w+u| \le B_T,\qquad B_T=\frac{3/2}{1-e^{-T}}.
\]

For discrete actions `u∈{-1,+1}`, since `B_T>1`, the thresholds are

\[
k_T(\lambda)=
\begin{cases}
1,&\lambda\le B_T-1,\\
2,&B_T-1<\lambda\le B_T+1,\\
\infty,&\lambda>B_T+1.
\end{cases}
\]

Example: at `T=ln 2`, `B_T=3`; the two thresholds shift from 0.5 and 2.5 (infinite horizon) to 2 and 4. A short decision horizon can therefore demand less knowledge than a long-term viability guarantee. This is relative to **fixed open-loop action commitment**; allowing observations and later intervention creates a different problem.

**Actuator variation.** With an additional neutral action `u=0`, the infinite-horizon common-action region extends to `λ≤1.5`. At `λ=1`, two actions require one bit but three actions require zero bits to choose some safe action. The model has not acquired knowledge: it has acquired an option that reduces the knowledge needed for this task.

These extensions remain elementary demonstrations, not novel general theorems.
