# T3.E — Available actions are not implementable policies

**Status:** model-specific propositions, proved using elementary channel algebra and classical control/reliability tools. Originality not established. Extends T3.D's rectangular row envelope and T4.C's recurrent organization; does not establish spontaneous agency.

## 1. The smallest implementability gap

A readable bit c is passed through physical reset hardware K(y|c,a)=1{y=a}. Both actions a=0,1 are physically possible at each c. Consider two architectures:

- Shared mode: the same mode must be used for both c. Deterministic prescriptions Phi_shared={(0,0),(1,1)}.
- State-contingent mode: Phi_full={0,1}^2, including (0,1) and (1,0).

Their **per-state projections of available actions are identical**, but their maximal closed-loop Dobrushin coefficients are 0 and 1, respectively. A random mixture of shared modes independent of c remains a constant-row channel. Thus replacing a joint feasible policy set Phi by the Cartesian product of its marginal action sets can invent a controller.

This is not a new mathematical phenomenon. Its role is to identify what must be primitive in CDKA: an implementability relation over whole prescriptions, not merely A(c).

For binary outputs write each attainable row as y_c=q_c^0+(q_c^1-q_c^0)f_c. Under a polyhedral implementability relation A f<=b, maximizing |y_c-y_d| is two linear programs per input pair. LP dual solutions certify limits. Discrete realizable circuits instead yield integer-program or finite enumeration problems. An expected-cost polytope must specify the distribution used to price rows; it must not silently replace pathwise physical constraints.

## 2. A continuously restricted selector

Use the T4.C renewal process: hidden static W in {0,1}; each surviving cycle starts with physical latch m=W, a worn actuator, and a base repair token. A repair write is selected using m. Writing suffers independent BSC error p in [0,1/2]. At the act stage, the decoder reads the rewritten bit y and chooses u. If u=W, the action latches m=u, replenishes the base token from a declared environmental transition and causes wear. Otherwise failure is absorbing.

The selector is restricted by |f_1-f_0|<=sigma, where f_w=P(write1|m=w). Both commands can still be chosen in either input state; the constraint couples their conditional probabilities. Terminal decoder g_y=P(act1|y) is unrestricted. sigma in [0,1] quantifies physical contingent selection, not quantity of stored information.

Let q_w be per-context success in a cycle. Then

    q0+q1 = 1+(g1-g0)(1-2p)(f1-f0)
           <= 1+(1-2p)sigma = 2 b(sigma,p).

### Proposition E1 — exact robust repeated viability

For specified stage parameters (sigma_t,p_t), fresh behavioral randomization, a declared clock, no extra persistent seed or channels, and successful renewal to the same physical context-specific state,

    sup_pi min_w P_pi(survive n cycles | W=w)
       = product_t b(sigma_t,p_t),
    b(sigma,p) = [1+(1-2p)sigma]/2.

**Proof.** At every stage q0*q1<=((q0+q1)/2)^2<=b^2. The conditional profile factors across successful renewals because there is no unmodeled persistent state. Therefore min(s0,s1)<=sqrt(s0*s1)<=product b_t. Equality is attained by symmetric selector f0=(1-sigma)/2, f1=(1+sigma)/2 and identity decoder g0=0,g1=1. QED.

The formula is not valid after adding a protected seed that selects one context to favor permanently, or a direct side channel bypassing the selector. These stronger architectures must be modeled separately. A random coin whose value is remembered is not a fresh behavioral coin.

## 3. Produce both selectivity and fidelity

Define an explicit normalized effort model:

    sigma(w)=1-exp(-w),
    p(e)=0.5 exp(-e),
    w,e>=0.

w funds the input-contingent selection mechanism; e funds repair-write fidelity. These are stipulated calibration laws, not a derivation from circuit thermodynamics. The actuator's base token, the terminal decoder and initial observation follow the declared baseline and are not priced by w,e. Thus r=w+e is additional adjustable effort, not the total thermodynamic cost of all computation.

The exact robust one-cycle value is

    b(w,e)=0.5[1+(1-exp(-w))(1-exp(-e))].

Either mechanism alone is insufficient: b(0,e)=b(w,0)=1/2. For w+e=r, AM-GM on exp(-w)+exp(-e) gives the unique optimum w=e=r/2 when r>0, hence

    q(r)=1-exp(-r/2)+0.5 exp(-r).

No generic numerical optimizer is necessary. All following lifetime statements refer to this controlled family and context-blind effort allocations. They are not universal resource laws.

For unequal physical efficiencies sigma=1-exp(-a w), p=.5exp(-b e), the scalar optimum solves

    a/[exp(a w)-1] = b/[exp(b e)-1],   w+e=r.

The equality follows from log-concavity of 1-exp(-x) and is the equality of marginal log benefits, not equality of arbitrary units. The implemented laboratory fixes a=b=1.

## 4. Bridge to physical action — conditional, not an identity of units

If a separate causal diffusion experiment justifies sensor/selector and repair-error exponents J_s,J_r on the same noise scale epsilon, effective error in the two binary cascade is exponentially governed by min(J_s,J_r), under the declared conditional independence and nondegenerate small-noise conditions. The complete probability is not determined by exponents alone.

A physically calibrated effort model might identify w=J_s/epsilon and e=J_r/epsilon only after identifying prefactors, deadlines and allowed action channels. It must not equate effort with joules or Freidlin-Wentzell action by terminology alone. Correlated error sources, fault correction, post-repair sensing, or action-dependent initialization change the result.

## 5. Verification

`cdka/implementability.py` contains exact Fraction channel calculations, the coupled-selector certificate, effort formulas and finite-grid resource optimization. The independent finite policy grid checks 3,675 feasible selector/decoder/noise combinations. A separate two-cycle enumeration checks the product certificate. Positive attainable witnesses accompany all upper bounds.

## Primary antecedents and distinction

- Polyanskiy & Wu, *Dissipation of information in channels with input constraints*, arXiv:1405.3629 / IEEE TIT 2016: cost constraints require more than an unconstrained scalar contraction coefficient. https://arxiv.org/abs/1405.3629
- Chatterjee & Varshney, *Energy-Reliability Limits in Nanoscale Feedforward Neural Networks and Formulas*, arXiv:1607.03572 / IEEE JSAIT 2020: explicit noisy-device reliability and operating-point constraints matter. https://arxiv.org/abs/1607.03572
- Junges et al., *Finite-State Controllers of POMDPs* (UAI 2018): synthesis of actually implementable bounded policies. https://proceedings.mlr.press/r16/junges18a.html

We do not claim the algebra, noisy-circuit tradeoff or constrained-policy idea is new. The research direction is compositional organization-dependent implementability with upkeep, correct causal accounting and proof certificates.
