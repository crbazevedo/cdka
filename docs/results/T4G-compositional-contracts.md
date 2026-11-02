# T4.G — Fallible upkeep, a changing world, and policy-safe compositional contracts

**Status:** scoped derivations using classical controlled lumpability and coupling; originality not established. Exact finite probabilities use rational arithmetic. This tests v5's ideal-corrector/static-context assumptions.

## 1. Physical contract and remaining idealizations

The world bit W can change during an epoch. Three physical cells m carry an earlier distinction. Their corrector has healthy/degraded state h, degrades, and can be serviced unsuccessfully. Sensing, correction, writing and actuation can all fail. Finite integer resource b pays for operations. Resources arrive **only after successful operation**.

The health flag, resource ledger and protocol clock remain reliably readable. A declared meta-selector implements the prescribed maps of these inputs. Those are explicit assumptions; we have not eliminated every trusted component. Hidden health and paid global implementation are next branches R11/R14.

Live epoch-boundary state is s=(W,m1,m2,m3,h,b), with majority(m)=W. Wrong terminal majority or physical execution failure kills the trajectory. A correct command may still leave one corrupted cell. W is not a runtime policy input.

### Fixed causal order

1. Select an affordable meta-action from the current readable register, h,b and declared remaining-horizon clock.
2. W flips with probability nu. Exchangeable independent cell upsets occur with probability d.
3. `hold` retains the result. `service` also retains it but attempts to restore next-epoch corrector health. `correct` takes current register majority through a fallible gate. `refresh` obtains a new noisy observation of current W, then uses the fallible gate. Both writing actions can independently corrupt written cells.
4. Actuation succeeds only if final majority equals current W and the execution mechanism does not fail. This is a declared fail-stop law, not cancellation of opposite command errors.
5. Only successful operation earns harvest. Health is updated; failed paths never receive resources or renormalization.

Costs hold/correct/refresh/service are 0/1/2/2. Default capacity=4, harvest=1; nu=1/10; cell upset=1/50; write upset=1/100; correction gate error=(1/100,1/5); sensor error=(1/25,1/5); execution failure=(1/200,3/100); degradation=1/20; service success=4/5. Tuple entries index healthy/degraded. These are normalized finite contracts, not thermodynamic calibration. Correlated variants require a joint kernel.

## 2. Independent component algebra

Let k count cells disagreeing with W. A world flip maps k to 3-k. After this, let i wrong cells flip into agreement and j correct cells become wrong. Then

    k_pre = k0-i+j,
    P(i,j|k0) = Binomial(k0,d)[i] Binomial(3-k0,d)[j].

For correction let a=P(k_pre<=1); for refresh let a=1-eta_h because a new physical observation of current W is obtained. A gate with inversion c_h gives a'=a(1-c_h)+(1-a)c_h. With write upset w,

    P(k_post=j)=a' Binomial(3,w)[j]+(1-a') Binomial(3,1-w)[j].

Only k_post<=1 and successful actuation contribute live mass. Multiply conditional health/resource factors. This constructs the macro law algebraically, independently of the raw bit-mask oracle.

## 3. Proposition G1 — exact, physically readable aggregation

Map live states to L(s)=(k,h,b), death to death. At a live decision boundary with three cells, k=0 iff the register is unanimous, otherwise k=1. The statistic is readable from physical disagreement without directly observing W. If wrong-majority states were allowed to remain live, k could be 2 or 3 and this interface would fail.

For every affordable action a and next macrocell B,

    sum_{s':L(s')=B} K^a(s'|s)

is the same for all s in one macrocell.

**Proof.** Permuting the three cells and simultaneously complementing W and all cells preserve the failure event, local noise contracts, health/resource transitions and action costs. These transformations act transitively inside each (k,h,b) class. Each action kernel is equivariant; the partition is invariant. Therefore all block-transition sums coincide. The binomial construction gives their common value. QED.

At capacity 4 there are **80 live microstates and 20 live macrostates**. The independent raw oracle enumerates world flips, every upset mask, sensor/gate outcome, write mask and health transition. All **240 affordable microstate-action rows** agree exactly; nine further rational fixtures check 1,008 rows.

Adding an absorbing death state gives K^a L=L barK^a. Stagewise intertwining composes by matrix multiplication. Intermediate mismatch counts can be unobservable, but there are no meta-policy decisions at these intermediate stages. Only the epoch-boundary readable statistic is supplied to the controller.

With matching whole-policy implementability and cell-constant objective/actions, Bellman induction transfers finite-horizon safety exactly and yields a physically readable optimal policy. In this class, even a full microstate relaxation has the same value and a macro policy attains it. This does not grant the executing controller hidden-state observations.

This is controlled lumpability applied to the specified organization, not a new aggregation theorem or a general scalability result.

## 4. Proposition G2 — compositional finite-horizon error

Suppose concrete and approximate systems have matching initial, observation and failure interfaces and the SAME realizable policy class under a specified lift. Conditional on every identical reachable input/history, component i differs by at most delta_i in total variation. This must be a uniform conditional contract, not a marginal fault rate.

Sequential maximal coupling gives per-epoch agreement at least kappa=product_i(1-delta_i). Thus, for any common lifted adaptive policy and a horizon-n path event,

    |P(event)-P_hat(event)| <= Delta_n,
    Delta_n = 1-[product_i(1-delta_i)]^n <= n sum_i delta_i.

**Proof.** On the event that coupled histories have not separated, common physical observations permit matching action selections. Couple each component while inputs agree. With probability at least kappa^n the entire relevant histories agree, hence so does the event. The mismatch event bounds the discrepancy. Conditioning sequentially suffices; independence between arbitrary life events is not needed. QED.

If policy classes match under the lift, |V*_n-Vhat*_n|<=Delta_n. A policy optimal in the approximation has deployed loss at most 2Delta_n, by adding two evaluation errors. Matching only action alphabets is insufficient.

No infinite-safety conclusion follows: Delta_n can approach one, and an arbitrarily small new failure edge can change recurrent support.

### Calibration check

Increasing both sensor errors by .02 gives exact maximum composed row-TV difference .019490376808. At n=10 the bound is .178668264306, while the largest actual optimum-value discrepancy over the 20 initial macrostates is .048352214308. The bound contains it and is conservative. The resulting deployed policy happens to have zero regret in this fixture at n=10; this is not a general invariance theorem.

## 5. Explicit falsifier and program pivot

Make cell upset probabilities (.30,.01,.01). States (W=0,m=100,h=0,b=4) and (W=0,m=010,h=0,b=4) have the same disagreement count. Their `hold` next-macro laws nevertheless differ by

    TV = 513619/2000000 = .2568095.

Exact count-only aggregation is false. Trigger R13 observable refinement or R12 an explicit approximate certificate. Do not drop this test or average away the residual. Removing h also fails because gate and actuation laws differ by health.

## 6. Correctness, freshness and maintenance

With a perfect old codeword, world flip .2, no cell/write/gate/execution faults and fresh sensor error .05:

    P(success|hold)=P(success|correct)=.8;
    P(success|refresh)=.95.

Correction preserves data integrity, not currency with a changing world. Conversely, with no drift/cell/write faults and a degraded correction gate c=.2, holding a correct register succeeds with 1 whereas correcting succeeds with .8.

In the default model, starting unanimous/healthy with b=4, optimal survival at n=1,3,10,30 is approximately .945778667, .838866610, .440708129, .075369848. Starting unanimous/degraded with b=4, `hold` is one-step optimal (deterministic tie handling), while `service` is optimal in the tested longer horizons. Future health matters.

Every allowed execution has conditional failure at least 1/200, so all policies satisfy survival <=(199/200)^n. This is a uniform conditional-hazard result for the specified architecture, not a universal limitation on autonomy.

## 7. Calculus as a calibration-priority instrument

For a fixed physically implemented policy sequence,

    d/dtheta [mu Q0 ... Q(n-1) 1]
      = sum_t mu Q0 ... Q(t-1) (dQt/dtheta) Q(t+1) ... Q(n-1) 1.

Local sensitivity is weighted by forward exposure and backward viable continuation. Missing mass stays failure. The implementation differentiates a common additive sensor-error change exactly and compares with an independently computed central difference, freezing the policy. At a policy-switch boundary the optimum is an envelope and may not have a unique derivative. No unchecked differentiation through argmax is used. This is classical matrix calculus.

## 8. Limits and next gate

Readable health, syndrome, resource and clock remain trusted interfaces. Noise is exchangeable and conditionally independent. The three-cell size is fixed. Meta-prescriptions are independently available by observed state. Each assumption has a named fallback in `registry/research-options.json`; next active branches are hidden-health diagnostics R11 and jointly costed implementation R14.

The current result is a verified compositional instrument. Scientific novelty requires a stronger physically constrained class and direct comparison to existing abstraction/FSC results.

## 9. Primary antecedents checked

- Buchholz, exact and ordinary lumpability: https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/exact-and-ordinary-lumpability-in-finite-markov-chains/2DC748F09D80BEEB03CCF18036E149D7
- Lavaei, Soudjani, Zamani, compositional abstraction and policy-refinement bounds: https://arxiv.org/abs/1808.00893
- Relaxed dissipativity composition: https://arxiv.org/abs/1902.01223
- Junges et al., finite-state POMDP synthesis: https://proceedings.mlr.press/r16/junges18a.html
- Tirinzoni et al., nonrectangular uncertainty: https://papers.nips.cc/paper_files/paper/2018/hash/7ec0dbeee45813422897e04ad8424a5e-Abstract.html

Code: `cdka/composition.py`; independent tests: `tests/test_composition.py`.
