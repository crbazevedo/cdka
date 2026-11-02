# T4.F — Reconfiguration is a risky, financed option, not a free new controller

**Status:** exact finite-family stopping/reachability laws and constructive policies; classical instruments, originality unestablished. This is not optimization over all physically conceivable controllers.

## 1. Physical and informational contract

Each successful old cycle begins with a correct physical latch m=W, as in T4.C. W is a static hidden bit. Selection/writing use m; correct action renews that latch and harvests, wrong action is absorbing failure. Effort schedules use only readable resources and a declared clock, not W, hidden history or private persistent seeds. Resource levels do not encode W in this library.

A finite extra reservoir has balance b and capacity C. Integer effort j gives the symmetric per-context reliability

    q_j=1-2^-j+0.5*4^-j.

This is v4's optimally split q(r) at normalized effort r=2j log 2. Tokens are not joules. Other base hardware/decoder assumptions remain explicit. Only after a correct operation:

    b'=min(C,b-j+h), 0<=j<=b.

At b>=K the organization may spend K to reconfigure. The operation occupies this epoch, includes its logical response/copying in success probability s, and enters a new architecture with per-epoch reliability q_N. Failure is absorbing. Its later maintenance is a specified funded cycle, not free perfection.

One concrete q_N=1 family is T3.F's three-bit register, correct majority/rewrite mechanism, and at most one upset per epoch. The noise is positive but support is bounded. With independent positive bit flips instead, q_N=1-(3p^2-2p^3)<1. K includes implementing the new controller, not merely its added storage.

Context-dependent effort, implicit resource signaling, extra sensing or private seeds constitute different architectures. The results below are exact only for this symmetric resource-controlled library.

## 2. Finite-horizon Bellman equation

Let V_n(b) be survival for n remaining epochs in the old architecture. The already-new value is q_N^n:

    V_0(b)=1,
    V_n(b)=max{
      max_(0<=j<=b) q_j V_(n-1)(min(C,b-j+h)),
      s q_N^(n-1) if b>=K
    }.

A policy sees actual resource/architecture state, not W or design occupancy. Scalar continuation is affine in fresh randomization, so deterministic resource prescriptions attain the optimum in this symmetric library. Per-context values coincide; thus the scalar value is its worst-context guarantee.

Finite horizons can prefer continuing instead of installing: installation risk needs enough future benefit. The policy is a map of resource and remaining horizon, not an assumed universal switching time.

## 3. Exact indefinite result if the new support is safe

Assume q_N=1 and s>0. If C<K, no installation is possible and infinite survival is zero because q_j<=q_C<1. If h=0 and b<K the result is also zero. If b>=K, immediate installation attains s; postponing cannot beat the same installation success multiplied by additional risks. If C>=K and h>0, reaching installation has positive probability from every b, not generally probability one.

Let R(b) be optimal probability of reaching the new safe class before failure. Set R(b)=s for b>=K. For b<K:

    R(b)=max_(0<=j<=min(b,h-1)) q_j R(min(C,b-j+h)).

**Why this is an acyclic exact recursion.** More initial resource cannot reduce attainable reachability: balance transitions are monotone and any previously allowed expenditure remains feasible. A step j>=h gives no resource progress while multiplying survival by q_j<1. Removing that segment cannot hurt an installation-reaching path. Therefore an optimal path uses only j<h before switching; its resource strictly increases. The resulting backwards dynamic program is exact. QED.

**Error certificate:** for every n,

    0<=V_n(b)-R(b)<=q_C^n.

The finite-optimal policy's mass already installed by n is at most R(b); its remaining live old mass is at most q_C^n. Conversely, truncating an indefinite-optimal policy gives the lower bound. This proved estimate may be numerically loose but is not an unsubstantiated convergence tolerance.

## 4. Earliest feasible installation is not optimal

Take C=K=8, h=5, s=.9, q_N=1 and b0=0. The exact indefinite optimum follows:

| Epoch | Resource | Action | Resource after success |
|---|---:|---|---:|
| 1 | 0 | spend 0, survival 1/2 | 5 |
| 2 | 5 | spend 3, survival 113/128 | 7 |
| 3 | 7 | spend 4, survival 481/512 | 8 |
| 4 | 8 | install, survival 9/10 | new architecture |

    R(0)=(1/2)(113/128)(481/512)(9/10)
        =489177/1310720
        =0.373212432861328125.

The earliest feasible route 0->5->8 spends 0 then 2 and installs, yielding (1/2)(25/32)(9/10)=.3515625. Improving immediate operation and postponing installation one epoch improves total success by 6.1582% relative. This is a model-specific optimality result, not a general recommendation to wait.

## 5. Probability versus support

If q_N<1, infinite survival is zero throughout this finite library. Installation occurs at most once; all other epochs have reliability <=q_max=max(q_C,q_N)<1. Thus

    V_n(b)<=q_max^(n-1), n>=1,

even with perfect installation. A new architecture can still greatly improve finite life and be the finite-horizon optimum.

The difference at q_N=1 is a change in failure support, not a robust prediction under arbitrary thermal/Gaussian noise. The reservoir threshold C=K is also library-relative: signaling through resource levels or a cheaper controller implementation changes the problem.

## 6. Exact min-plus reformulation; not a universal action principle

The success of an installation path is s times the product of its q_j. Put c_j=-log q_j and C(b)=-log R(b). Then

    C(K)=-log s,
    C(b)=min_j {c_j+C(b-j+h)}.

This is an exact shortest-path problem on resource states, not Hamilton's stationary action. Reconfiguration changes the viable path geometry and makes its optimization explicit.

If a separate physical calculation gives failure p_j approximately A_j exp(-J_j/epsilon), then -log q_j=-log(1-p_j) is approximately p_j, **not** J_j/epsilon. Confusing the rare-failure rate with negative log success distorts the objective. The initial state, failure event, deadline, allowed interventions, joint noise and prefactors must remain fixed and declared.

## 7. Achieved and open

Achieved: an organization acts to acquire the resources needed for a later self-reconfiguration; installation changes its information-preserving policy class; optimality counts the risk of getting there. The controller is implemented through physical latch, resource and architecture state.

Open: a fallible maintained corrector; a changing hidden world and costly new sensing; hidden damage; context-dependent budgets without omitted signaling; reconfiguration of higher-order action compatibility. No spontaneous goals or general agency theorem is asserted.

## 8. Verification and antecedents

435 finite cases are checked against independent un-memoized path enumeration. Every stationary resource prescription is enumerated for capacities 1..4, eligible costs and several harvest rates. Exact fractions, prefix constraints, convergence bounds and support perturbations are independently tested.

- Consumption-MDP synthesis: https://doi.org/10.1007/978-3-030-53291-8_22
- Quantitative consumption/reachability: https://www.sciencedirect.com/science/article/abs/pii/S0020019022000990
- Finite-state POMDP controllers: https://proceedings.mlr.press/r16/junges18a.html
- Energy-parity games: https://arxiv.org/abs/1001.5183

Source: `cdka/reconfiguration.py`; tests: `tests/test_reconfiguration.py`; certificates: `experiments/reconfiguration_sweep.py`.
