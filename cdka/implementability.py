"""CDKA T3.E/T4.D. Restricted selection, produced fidelity, recurrent budgets.

Model-specific exact algebra + certified grid optimization. Resource is
DIMENSIONLESS calibrated effort, not automatically joules or FW action.
Policies have no durable random seed, forgotten history or extra channels.
Stage allocations do not encode hidden W; renewal latch equals W on success.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import exp, expm1, isfinite, log, log1p, sqrt
from typing import Iterable


def _nonnegative(x: float, name: str) -> float:
    x = float(x)
    if not isfinite(x) or x < 0:
        raise ValueError(f'{name} must be finite and nonnegative')
    return x


def _count(n: int) -> int:
    if type(n) is not int or n < 1:
        raise ValueError('positive integer horizon required')
    return n


def cycle_profile(f0: F, f1: F, g0: F, g1: F, p: F) -> tuple[F, F]:
    """Actual (q0,q1) of selector -> BSC repair -> binary action decoder."""
    f0,f1,g0,g1,p = map(F,(f0,f1,g0,g1,p))
    if not all(0 <= x <= 1 for x in (f0,f1,g0,g1)) or not 0 <= p <= F(1,2):
        raise ValueError('invalid channel probabilities')
    y0,y1 = p+(1-2*p)*f0, p+(1-2*p)*f1
    return 1-g0-(g1-g0)*y0, g0+(g1-g0)*y1


def restricted_cycle_bound(sigma: F, p: F) -> F:
    """Exact robust one-cycle optimum if |f1-f0|<=sigma and decoder is free."""
    sigma,p=F(sigma),F(p)
    if not 0<=sigma<=1 or not 0<=p<=F(1,2):
        raise ValueError('sigma in [0,1], p in [0,1/2] required')
    return (1+(1-2*p)*sigma)/2


def restricted_reset_diameter(prescriptions: Iterable[tuple[F,F]]) -> F:
    """For physical reset-to-a hardware the row diameter is |f1-f0|.

    Supplying an explicit list preserves global implementability constraints;
    independently taking row projections would be a different architecture.
    """
    values=[]
    for x,y in prescriptions:
        x,y=F(x),F(y)
        if not (0<=x<=1 and 0<=y<=1): raise ValueError('invalid row')
        values.append(abs(y-x))
    if not values: raise ValueError('empty architecture')
    return max(values)


def produced_cycle(w: float, e: float) -> float:
    """Selector contrast 1-exp(-w), write error .5 exp(-e)."""
    w,e=_nonnegative(w,'selector effort'),_nonnegative(e,'repair effort')
    return .5*(1+(-expm1(-w))*(-expm1(-e)))


def optimal_cycle(r: float) -> float:
    """Exact one-cycle optimum with w+e=r: uniquely w=e=r/2 for r>0."""
    r=_nonnegative(r,'cycle effort')
    return .5*(1+(-expm1(-r/2))**2)


def log_cycle(r: float) -> float:
    r=_nonnegative(r,'cycle effort')
    x=exp(-r/2)
    return log1p(-x+x*x/2)


def log_cycle_slope(r: float) -> float:
    r=_nonnegative(r,'cycle effort')
    x=exp(-r/2)
    return x*(1-x)/(2*(1-x+x*x/2))


def log_cycle_curvature(r: float) -> float:
    r=_nonnegative(r,'cycle effort')
    x=exp(-r/2)
    return -x*(x*x-4*x+2)/(2*(x*x-2*x+2)**2)


def curvature_threshold() -> float:
    return -2*log(2-sqrt(2))


def tangent_threshold() -> float:
    """Unique r*>r_inflection: r*l'(r)=l(r)-l(0). Bisection."""
    lo,hi=curvature_threshold(),4.0
    def f(r): return r*log_cycle_slope(r)-log_cycle(r)-log(2)
    while f(hi)>0: hi*=2
    for _ in range(70):
        mid=(lo+hi)/2
        if f(mid)>0: lo=mid
        else: hi=mid
    return (lo+hi)/2


def concave_log_envelope(r: float) -> float:
    """Smallest concave majorant of l(r)=log(optimal_cycle(r)) on r>=0."""
    r=_nonnegative(r,'mean effort')
    star=tangent_threshold()
    if r<=star:
        return -log(2)+r*log_cycle_slope(star)
    return log_cycle(r)


def schedule_log_survival(resources: Iterable[float]) -> float:
    return sum(log_cycle(r) for r in resources)


@dataclass(frozen=True)
class GridAllocation:
    horizon: int
    quantum: float
    units: int
    log_survival: float
    allocations: tuple[int,...]


def optimal_grid_schedule(n: int, units: int, quantum: float=.1) -> GridAllocation:
    """Global exact combinatorial optimum ON THE DECLARED RESOURCE GRID.

    Log probabilities use floating point; optimality is for integer units,
    not a certificate of the full continuous finite-horizon optimum.
    """
    _count(n)
    if type(units) is not int or units<0: raise ValueError('invalid units')
    quantum=_nonnegative(quantum,'quantum')
    if quantum==0: raise ValueError('positive quantum required')
    ell=[log_cycle(k*quantum) for k in range(units+1)]
    dp=[float('-inf')]*(units+1); dp[0]=0.0
    paths={0:()}
    for _ in range(n):
        new=[];new_paths={}
        for b in range(units+1):
            v,k=max((dp[b-k]+ell[k],k) for k in range(b+1))
            new.append(v);new_paths[b]=paths[b-k]+(k,)
        dp,paths=new,new_paths
    return GridAllocation(n,quantum,units,dp[units],paths[units])


def minimum_high_reliability_budget(n: int, beta: float) -> float:
    """Exact continuous minimum for beta>=2-sqrt(2), beta<1.

    This is TOTAL effort of n context-blind allocations, each optimally split
    w=e. Every feasible component lies in log-concave region; Jensen applies.
    """
    _count(n)
    if not isfinite(beta) or not 2-sqrt(2)<=beta<1:
        raise ValueError('beta in [2-sqrt(2),1) required by theorem')
    failure=-expm1(log(beta)/n)
    x=2*failure/(1+sqrt(1-2*failure))
    return -2*n*log(x)


def fidelity_only_budget(n: int, beta: float) -> float:
    """Baseline: selection free/perfect, repair p=.5 exp(-e)."""
    _count(n)
    if not isfinite(beta) or not 0<beta<1: raise ValueError('beta in (0,1)')
    failure=-expm1(log(beta)/n)
    return max(0.0,n*log(.5/failure))


def harvesting_schedule(n: int, inflow: float, initial: float=0.0):
    """Resource-causal stationary rule attaining the concave-envelope rate.

    Replenishment occurs only after a successful act; schedule/log product
    describe unnormalized survival through that branch. A separate base
    actuator token follows the previous renewal model. Adjustable effort
    comes from this reservoir; no information about W is encoded in it.
    """
    _count(n); inflow=_nonnegative(inflow,'inflow');initial=_nonnegative(initial,'initial')
    star=tangent_threshold(); target=star if inflow<star else inflow
    balance=initial; allocations=[]; balances=[balance]; log_survival=0.0
    for _ in range(n):
        spend=target if balance+1e-12>=target else 0.0
        if spend>balance: spend=balance
        allocations.append(spend)
        log_survival+=log_cycle(spend)
        balance=balance-spend+inflow
        balances.append(balance)
    return {'allocations':allocations,'balances':balances,'log_survival':log_survival,
            'rate':log_survival/n,'rate_upper':concave_log_envelope(inflow+initial/n)}


def constrained_policy_grid(sigma: F,p: F,denominator: int=4):
    """Independent exact finite policy oracle for the coupled contrast law."""
    sigma,p=F(sigma),F(p)
    grid=tuple(F(k,denominator) for k in range(denominator+1))
    return [(f0,f1,g0,g1,*cycle_profile(f0,f1,g0,g1,p))
            for f0,f1,g0,g1 in product(grid,repeat=4) if abs(f1-f0)<=sigma]
