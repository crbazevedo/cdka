# T4.E — Recovery, spectral lifetime and the complete-controller support criterion

**Status:** classical absorbing-chain/support results specialized to explicit physical controllers; exact proofs and rational checks. No general original autonomy theorem.

## 1. Complete controller, not isolated hardware modes

Let Q be the finite sub-stochastic matrix over all live physical states of a FIXED implementable controller. Include readable memory, configuration, resources, and any clock or persistent seed the controller uses. Missing row mass means irreversible failure. Survival is S_n=mu Q^n 1.

Compute the greatest non-killing closed live set G by repeatedly deleting states with missing mass or any positive transition outside the remaining set. This is a fixed-controller calculation; a hidden-state feedback oracle is not allowed.

### Proposition E1

For this fixed finite controller, infinite survival equals the probability of reaching G before failure. If G is empty, survival tends to zero everywhere and the spectral radius of Q is below one. Positive survival requires positive reachability of G, not necessarily starting in G. Probability-one survival is strictly stronger.

**Proof.** Complete the matrix with an absorbing failure state. A trajectory that survives forever eventually visits a closed recurrent class excluding failure; all such classes lie in G. Its complement T is transient. Hitting probabilities satisfy

    v_G=1,
    (I-Q_TT)v_T=Q_TG 1.

The inverse exists because Q_TT is transient. QED.

For Q=[[1,0],[1/5,7/10]], G={0}, but the second state's infinite survival is (1/5)/(1-7/10)=2/3. Initial safe membership is not necessary for a positive chance of reaching safety.

### Uniform-block no-go, without independence

If every admissible continuation and reachable live history has conditional failure probability at least epsilon>0 within L steps, then survival at n is at most (1-epsilon)^floor(n/L). Condition on successive live blocks; independence is unnecessary. For fixed finite Q with empty G, a positive failure path of length at most the number of live states and a minimum positive edge probability supply such a bound.

The hypothesis must cover all permitted switching policies. It is insufficient to check each mode separately.

## 2. Recoverable redundancy greatly extends life without safe recurrence

States H and D mean two working components and one working component. Failure is absorbing. At H both components face independent damage d. At D, repair succeeds with probability r and returns H for the next epoch; otherwise the remaining component faces damage d. This phase ordering is explicit.

    Q=[[(1-d)^2, 2d(1-d)],
       [r,       (1-r)(1-d)]].

Missing masses are d^2 and (1-r)d. For d>0, every r in [0,1] leaves G empty. Even perfect repair of the degraded state cannot prevent simultaneous failure from H.

For Q=[[a,b],[c,e]],

    lambda_+ = (a+e+sqrt((a-e)^2+4bc))/2 < 1,
    det(I-Q)=d^2[(2-d)-r(1-d)]>0.

The expected epochs through and including failure, starting in H, are

    E_H[tau]=[d(3-2d)+r(1-d)]/{d^2[(2-d)-r(1-d)]}.

This follows directly from the first coordinate of (I-Q)^(-1)1. At r=1 it is 1/d^2+2/d-2: d=.01 gives 10,198 epochs, versus 100 for one unrepaired component. Both have infinite survival zero at positive d.

Recovery changes the rare-failure order from d to d^2 here, not the existence of a safe recurrent class. If a separately calibrated law has d approximately exp(-J/epsilon), the lifetime scale can be of order exp(2J/epsilon) under independent faults. This is not an exact or universal physical law; correlations, events, prefactors and repair costs matter.

## 3. A falsifier for mode-by-mode impossibility

Let

    A=[[0,1],[0,0]], B=[[0,0],[1,0]].

A^2=B^2=0. Every fixed mode kills all trajectories within two transitions. Yet AB=[[1,0],[0,0]] preserves state 0 at cycle boundaries. Alternation A,B is safe from that state. A state-contingent selector can implement [[0,1],[1,0]], safe from both. Independent fresh 50/50 mode choices instead yield (A+B)/2 and survival 2^-n.

This classical switching counterexample explains why the physical selector or persistent phase must be included in the architecture. Once it is included, the complete-controller support theorem is valid again. Spectral radii of isolated modes do not characterize coordinated products.

## 4. Instruments and next gate

Boolean support/SCCs identify non-killing recurrence. Positive matrices, resolvents and spectral radii quantify finite lifetimes. Realizable products diagnose temporal coordination. Resource and health states compile reconfiguration into the physical model, without turning a partially observed process into a fully observed one by fiat.

The next proof pays for reaching the better architecture instead of assuming its availability at time zero.

## 5. Verification and antecedents

42 rational damage/repair configurations are checked by independent exact linear solves, support iteration, spectral expressions and probability propagation. Switching and positive-reachability counterexamples have dedicated tests.

- Junges et al. (2018): https://proceedings.mlr.press/r16/junges18a.html
- PRISM strategy synthesis: https://www.prismmodelchecker.org/manual/RunningPRISM/Adversaries
- Efficient Formally Verified Maximal End Component Decomposition for MDPs (2024): https://doi.org/10.1007/978-3-031-71162-6_11
