# T4.D — Produced fidelity: exact budget regimes and the cost of continued viability

**Status:** proved for an explicitly stipulated two-mechanism renewal family, classical analytical instruments; originality unestablished. The finite resource grid is numerically optimized globally on its grid, not asserted to be the exact continuous solution at every budget.

## 1. Model and scopes

T3.E established q(r)=1-exp(-r/2)+.5 exp(-r) as the optimal robust one-cycle probability when total effort r is optimally divided between state-contingent selection and physical repair writing. Failed trajectory mass is retained as failure; there is no renormalization.

For a deterministic, context-blind sequence r_t, without an extra persistent policy seed, robust n-cycle viability is

    V_n(r_1,...,r_n)=product_t q(r_t).

There is a declared physical clock or a resource-only scheduling rule. The adjustable reservoir does not encode W or past private random choices. Its finite-horizon allocation problem is

    maximize sum_t ell(r_t),  r_t>=0, sum_t r_t<=R,
    ell(r)=log q(r).

This is a standard reliability-allocation problem with a specific, analytically useful nonconcave benefit. Its scientific role is to distinguish free selection, free fidelity and physically generated precision.

## 2. Exact curvature and the failure of uniform allocation

Put x=exp(-r/2). Differentiation gives

    ell'(r) = x(1-x)/[2(1-x+x^2/2)],
    ell''(r) = -x(x^2-4x+2) / [2(x^2-2x+2)^2].

Therefore ell is strictly convex below

    r_i=-2 log(2-sqrt(2)) = 1.069599993479...,

and strictly concave above r_i. q(r_i)=2-sqrt(2)=0.585786437627.... The positive initial curvature is the signature of complementarity: both the selector and the repair channel must improve before much benefit appears.

### Proposition D1 — scarcity concentrates resources

If 0<R<=r_i, an optimal n-cycle schedule concentrates the entire budget in one cycle, leaving n-1 cycles at r=0. Its robust value is

    V_n^*(R)=q(R) 2^{-(n-1)}.

**Proof.** Every feasible coordinate is in [0,R], where ell is convex. The sum of convex functions attains a maximum at a vertex of the budget simplex. It is increasing, so all R is used. Symmetry makes each vertex equivalent. Strict convexity excludes nonvertex optima for R>0, n>1. QED.

For n=4,R=1 the optimal survival is 0.072176132609, whereas uniform allocation gives 0.066023892002. These are low absolute reliabilities: the claim is about which feasible policy is best under scarcity, not about acceptable engineering safety.

## 3. Concave envelope: a certificate and asymptotic scheduling law

There is a unique r_d>r_i satisfying

    r_d ell'(r_d)=ell(r_d)-ell(0).

Numerically r_d=1.968728321390..., q(r_d)=0.696140406883..., slope=0.168100022740.... Let s_d=ell'(r_d). Define

    hat_ell(r)=ell(0)+s_d r,  0<=r<=r_d;
               ell(r),        r>=r_d.

### Proposition D2 — exact concave envelope

hat_ell is the smallest concave majorant of ell on r>=0.

**Proof.** H(r)=r ell'(r)-ell(r)+ell(0) has derivative r ell''(r). It increases strictly to r_i and then decreases strictly to ell(0)=-log 2<0; its unique positive zero is r_d. Thus [ell(r)-ell(0)]/r reaches its unique maximum at r_d. The chord from (0,ell(0)) is above ell before r_d, and joins the concave tail tangentially. Any concave majorant must dominate this chord and the tail, proving minimality. QED.

Consequently, for all finite budgets,

    log V_n^*(R) <= n hat_ell(R/n).

This is an upper certificate, not generally an attainable finite-n equality. For R_n=n h, with fixed h>=0,

    lim_(n->infinity) [log V_n^*(n h)]/n = hat_ell(h).

For h<r_d, allocate r_d to approximately h/r_d of the cycles, zero to the others, and absorb the bounded leftover in at most one cycle. For h>=r_d, allocate h each cycle. The difference from the envelope is O(1) in log survival; its rate vanishes after division by n. This is deterministic time allocation, not a randomized mixture of persistent context-favoring policies.

## 4. Endogenous replenishment on successful cycles

A physical effort reservoir satisfies, along a surviving path,

    E_(t+1)=E_t-r_t+h,   0<=r_t<=E_t.

Resource h is acquired only after a correct intervention. The base actuator token in T4.C is separate; r_t prices the two additional reliability mechanisms. A failed organization acquires nothing further. Do NOT use the reservoir equation to renormalize away failed trajectories.

### Proposition D3 — resource-causal policy attaining the asymptotic rate

For finite initial E0 and constant finite h, the same maximal exponential survival rate hat_ell(h) is attainable in the declared class.

**Upper bound:** any live schedule obeys sum_(t=1)^n r_t<=E0+h(n-1), so the envelope certificate gives a limsup bounded by hat_ell(h).

**Attainment for 0<h<r_d:** a stationary resource rule spends r_d when E_t>=r_d and otherwise spends zero. The reservoir remains bounded (after any finite initial transient); the fraction of funded cycles tends to h/r_d by resource conservation. Thus average log survival tends to ell(0)+h[ell(r_d)-ell(0)]/r_d.

**For h>=r_d:** spend h whenever enough is available. With E0=0, one zero-effort bootstrap cycle supplies h after success; every subsequent successful cycle spends h and recovers h. The finite transient does not change the exponent. For h=0 the asymptotic rate is ell(0).

Since hat_ell(h)<0 for every finite h, robust survival tends to zero exponentially. Regenerating the ability to perform another cycle is not equivalent to guaranteeing indefinite error-free viability. This is a theorem of the stated noisy architecture, NOT a universal limitation on living systems or agency.

A discrete or finite-capacity reservoir must be analyzed separately; the implemented numerical illustration uses a continuous nonnegative effort reservoir with no leakage and enough capacity for the threshold. Threshold arithmetic has floating-point tolerance; analytical claims do not depend on that implementation.

## 5. Exact minimum budget for high reliability

For target beta in [2-sqrt(2),1), define v=beta^(1/n). Then

    R_min(n,beta)=-2n log[1-sqrt(2 beta^(1/n)-1)].

### Proposition D4 — global continuous minimum in the stated target range

Every allocation attaining product q(r_t)>=beta has q(r_t)>=beta, hence r_t>=r_i. On that region ell is concave. Jensen implies product q(r_t)<=q(R/n)^n, and uniform r_t=R/n achieves equality. Inverting q gives the formula. QED.

No assertion of uniform global optimality is made for all lower targets. The scalar optimizer in the laboratory uses exact grid DP in that regime.

For beta=.9:

| cycles n | total effort R_min |
|---:|---:|
| 1 | 4.4967088628 |
| 10 | 91.0586754244 |
| 100 | 1371.1074656280 |
| 1000 | 18316.2452088886 |

For fixed beta and large n,

    R_min(n,beta)=2n[log n-log(-log beta)]+o(n).

With a perfect FREE selector and only repair error .5 exp(-e), the analogous leading cost is n log n. The coefficient two is specific to two equally calibrated costly noisy mechanisms; it is not a universal thermodynamic constant. For m specified serial mechanisms analogous balancing deserves an explicit separate derivation.

## 6. Finite lifetime design is not an infinite schedule

Because 1-q(r)=x-x^2/2 with x=exp(-r/2),

    .5 exp(-r/2) <= 1-q(r) <= exp(-r/2).

For a single specified infinite effort sequence,

    product_(t>=1) q(r_t)>0  iff  sum_(t>=1) exp(-r_t/2)<infinity.

No independence between arbitrarily defined life events is needed for the general product of conditional failure hazards; here the equality with q comes from the declared renewal architecture.

For example r_t=2 log(t+1)+2a log log(t+e)+c (c>=0) has positive infinite survival exactly when a>1, by the integral test. All such sequences have leading cumulative effort 2n log n, but their infinite-horizon outcomes differ. Therefore the finite-horizon leading asymptotic R~2n log n does NOT characterize one viable indefinite policy: lower-order terms and temporal availability matter.

## 7. Limits and next proof obligation

All results assume the renewal latch and no independent persistent policy seed, two mechanisms with independent BSC noise, context-blind precision allocations, absorbing failure on any incorrect action, a perfect terminal decoder, and a declared expenditure law. Shared error, corrective redundancy, tolerable mistakes, new observation, action signaling through resources, finite reservoir capacity or resource-dependent physical topology require a new model.

The next object is a policy-dependent organization kernel with changing feasible prescription set Phi(Z,R), where resources may fund **creating a qualitatively different policy/repair architecture**, not only reducing a fixed error probability. Quantify when self-reconfiguration breaks the present no-go and how much physical information and resource it requires.

## Verification and antecedents

`cdka/implementability.py` and `tests/test_implementability.py` compare channel identities against rational policy enumeration; finite-grid DP against independent weak-composition enumeration; derivatives against finite differences; high-reliability inversion; and resource-causal schedules against prefix conservation and the envelope.

- Reliability allocation among serial components has a long literature: *Optimal Reliability Allocation with Discrete Cost-Reliability Data for Components*, Operations Research 47 (1999), 899. https://doi.org/10.1287/opre.47.6.899
- Chatterjee & Varshney, energy-reliability constraints of heterogeneous noisy circuits: https://arxiv.org/abs/1607.03572
- Polyanskiy & Wu, cost-constrained information dissipation: https://arxiv.org/abs/1405.3629
- Thermodynamically consistent circuits are a possible physical calibration source, not validation of our chosen effort law: *Stochastic thermodynamic bounds on logical circuit operation*, PRE 111, 034110 (2025). https://doi.org/10.1103/PhysRevE.111.034110
