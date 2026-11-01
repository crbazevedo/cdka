"""Fixed-frame sensing-versus-actuation reliability trade-off.

Mathematical example, not a general agency theorem. The sensor-error and
conditional-diffusion-failure exponents are treated as independent given W.
No self-repair or autonomous budget generation is modeled.
"""
from dataclasses import dataclass
from math import isfinite
from .variational import fixed_frame_action


@dataclass(frozen=True)
class FixedFrameAllocation:
    horizon: float
    budget: float
    gamma: float
    actuation: float
    sensing: float
    good_action_rate: float
    wrong_action_rate: float
    sensing_error_rate: float
    effective_failure_rate: float


def optimize_fixed_frame_budget(B:float, T:float=3, gamma:float=2,
                                iterations:int=35,n:int=512)->FixedFrameAllocation:
    """Maximize min{J_T(-a), J_T(+a)+gamma(B-a)} for a in [0,B].

    Fixed initial x0=-1.1 and fixed failure threshold x=0 under every
    intervention. The resource B is a dimensionless model-scale budget.
    Restrict B <= .2 so the integration interval crosses a stationary
    point under both controls; this supports the positive-energy solver.
    """
    if not all(isfinite(x) for x in (B,T,gamma)) or not 0<B<=.2 or T<=0 or gamma<=0:
        raise ValueError("0<B<=.2, positive finite T and gamma required")
    def rates(a):
        good=fixed_frame_action(T,-a,n=n)
        bad=fixed_frame_action(T,+a,n=n)
        return good,bad
    lo,hi=0,B
    for _ in range(iterations):
        mid=(lo+hi)/2
        good,bad=rates(mid)
        if good-bad-gamma*(B-mid)>0:hi=mid
        else:lo=mid
    a=(lo+hi)/2
    good,bad=rates(a)
    sense=B-a
    k=gamma*sense
    return FixedFrameAllocation(T,B,gamma,a,sense,good,bad,k,min(good,bad+k))


def local_reliability_sensitivity(T:float=3,h:float=.005,n:int=1024)->float:
    """Numerical -d J_T(left,u)/du at u=0, with fixed causal endpoints."""
    return (fixed_frame_action(T,-h,n=n)-fixed_frame_action(T,h,n=n))/(2*h)
