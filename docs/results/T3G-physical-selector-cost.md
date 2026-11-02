# T3.G — The price of a decision rule is not the sum of available actions

**Status:** elementary counterexample and exact feasibility boundary. Known finite-controller/circuit-resource principles. No novelty claim.

## Primitive contract

Let `Y∈{0,1}` be a physically stored diagnostic signal. The possible terminal controls are `hold` (cost 0) and `refresh` (cost 2). Each is individually admissible whenever its action cost is affordable. However, they can be selected according to `Y` only if a **whole-prescription selector** is installed, at fixed cost `c`.

Thus, without the selector, available truth tables are only `(hold,hold)` and `(refresh,refresh)`; with it, the organization can also realize `(hold,refresh)` and `(refresh,hold)`. It is incorrect to form the Cartesian product of the available per-input actions without paying for that physical conditional mechanism.

The diagnosis itself has cost `d`. Both expenditures occur before terminal action and do not vary with its outcome. With resource B the full physical decision must satisfy

\[
 B\ge d+c+\max_y \mathrm{cost}(g(y)).
\]

This is a **pathwise** resource condition for the complete prescription, not a population-average charge. A policy that always uses `hold` need not buy a selector and is correctly priced separately.

## Two-stage feasibility theorem (scoped)

For the explicit v6 one-step success table in T4.H, `hold` dominates all other actions on the fair-prior undiagnosed branch. With a diagnosis, `refresh` can improve the decision only when observed health favors it. Therefore, with `d=c=1`, the positive diagnostic value requires `B>=4` and effective sensor error `e<e_*≈.1941618`, assuming no diagnostic failure. Both inequalities together are sufficient because the exact contingent decoder `(refresh,hold)` is then affordable.

With B=3, a perfect diagnostic *exists and may be stored*, but after financing test and selector the `refresh` action is unavailable. The information is not operationally usable for this task. At B=4, value increases from .883319376 to .908929941292. This is a discontinuity in the feasible policy library, not a physical attractor bifurcation or an entropy jump.

## Why the global cost is necessary

A linear relaxation that prices each observed row independently can mistakenly allow a conditional policy whose rows share expensive circuitry. Conversely, preprogramming a fixed action may cost less than paying a full programmable selector. For a library of physically implementable tables `Φ(Z,R)`, the correct optimization primitive is

\[
\max_{\phi\in\Phi(Z,R)}\sum_{h,y}P(h,y)V(h,\phi(y)),
\]

with the actual pathwise resource transition of the entire implementation. `Φ` is a representation of available hardware and programs, not a universal law specifying how every real device works.

## Falsification and next theorem candidate

- Outcome-dependent diagnosis spending would make the remaining resource a **physical side channel**. The current no-bypass formula would need recomputation on the entire readable `(Y,R,Z)`.
- A cheaper single adaptive controller, preinstalled selector or universal safe action can invalidate the B=4 threshold.
- A diagnostic could change the physical state, consume time or cause failures; those changes must enter the common causal frame.
- If an installed selector can wear, repair itself or be rewritten, its implementability becomes **endogenous** and must be included in the same recurrent physical model.

**Next target:** characterize a jointly funded finite-state *policy library* with hidden selector health and paid diagnostic feedback, and prove a nonseparable viability condition not reducible to standard POMDP/inspection constructions. Existing methods remain antecedents to audit.

See T4.H for complete physical scores and independent exact validation.
