"""CDKA classical mathematical instruments, not original theorems.

Quasipotential, finite-time Freidlin--Wentzell actions for one-dimensional
quartic gradients, OU benchmark, Bernoulli information bounds, and restricted
causal authority. Pure Python standard library; explicit noise convention:
    dX = -U'(X) dt + sqrt(2 epsilon) dW.
"""
from dataclasses import dataclass
from math import acos, cos, exp, isfinite, log, pi, sqrt


def quartic_potential(x: float, u: float = 0.0) -> float:
    return x**4 / 4 - x*x/2 - u*x


def quartic_gradient(x: float, u: float = 0.0) -> float:
    return x**3 - x - u


def critical_tilt() -> float:
    """Positive saddle-node tilt: 2/(3 sqrt(3))."""
    return 2/(3*sqrt(3))


def quartic_equilibria(u: float = 0.0) -> tuple[float, float, float]:
    """Left stable, middle saddle, right stable. Only strict bistability."""
    if not isfinite(u) or abs(u) >= critical_tilt():
        raise ValueError("Three distinct equilibria require |u| < 2/(3 sqrt(3))")
    theta = acos((3*sqrt(3)/2)*u) / 3
    return tuple(sorted((2/sqrt(3)*cos(theta - 2*pi*k/3) for k in range(3))))


def left_barrier(u: float = 0.0) -> float:
    a,s,_ = quartic_equilibria(u)
    return quartic_potential(s,u) - quartic_potential(a,u)


def right_barrier(u: float = 0.0) -> float:
    _,s,a = quartic_equilibria(u)
    return quartic_potential(s,u) - quartic_potential(a,u)


def saddle_node_constant() -> float:
    """Delta U_left ~ C*(u_c-u)^1.5 as u tends to u_c from below."""
    return 4/(3*3**0.25)


def simpson(f, low: float, high: float, n: int = 2048) -> float:
    if n < 2 or n % 2 != 0:
        raise ValueError("Simpson subdivisions must be positive and even")
    h=(high-low)/n
    total=f(low)+f(high)
    for i in range(1,n):
        total+=(4 if i%2 else 2)*f(low+h*i)
    return total*h/3


@dataclass(frozen=True)
class FiniteTimeAction:
    horizon: float
    tilt: float
    left_minimum: float
    saddle: float
    quasipotential: float
    action: float
    excess_action: float
    conserved_energy: float


def quartic_left_action(T: float,u: float=0.0,n: int=2048) -> FiniteTimeAction:
    """Exact 1D variational quadrature, evaluated numerically (no Monte Carlo).

    Paths start at the left stable equilibrium and reach the middle saddle
    at exactly T. Monotone optimal path solves
       xdot = sqrt(U'(x)^2+4 E), E > 0.
    The energy E is determined by T = integral dx/sqrt(U'^2+4E).
    This is not Kramers' mean exit time.
    """
    if not isfinite(T) or T <= 0:
        raise ValueError("finite strictly positive T required")
    if n < 2 or n%2: raise ValueError("positive even Simpson subdivisions required")
    a,s,_=quartic_equilibria(u)
    U=quartic_gradient
    dU=left_barrier(u)
    def time_from_energy(E: float) -> float:
        return simpson(lambda x:1/sqrt(U(x,u)**2+4*E),a,s,n)
    low=1e-14
    high=1.0
    while time_from_energy(high)>T:
        high*=4
    # T up to ~8 is well resolved with n=2048; longer horizons require
    # adaptively refined quadrature due narrow saddle-end boundary layers.
    if time_from_energy(low)<T:
        raise ValueError("T too large for fixed numerical resolution; increase n")
    for _ in range(52):
        mid=(low+high)/2
        if time_from_energy(mid)>T:low=mid
        else:high=mid
    E=(low+high)/2
    kinetic=simpson(lambda x:sqrt(U(x,u)**2+4*E),a,s,n)
    J=0.5*kinetic + 0.5*dU - E*T
    return FiniteTimeAction(T,u,a,s,dU,J,J-dU,E)


def ou_endpoint_rate(kappa:float,distance:float,T:float) -> float:
    """OU endpoint/exiting-by-T LDP action under sqrt(2 eps) noise.

    Controlled reachability Gramian: G_T=(1-exp(-2 kappa T))/(2 kappa).
    Action = distance^2/(4 G_T).
    """
    if kappa<=0 or T<=0 or distance<0:
        raise ValueError("positive kappa and horizon, nonnegative distance")
    from math import expm1
    return kappa*distance**2 / (-2*expm1(-2*kappa*T))


def binary_entropy(p:float)->float:
    if not (0<=p<=1):raise ValueError("p must lie in [0,1]")
    return -sum(q*log(q,2) for q in (p,1-p) if q>0)


def binary_rate_distortion(delta:float)->float:
    """R(D) for a uniform binary source and Hamming distortion D."""
    if not 0<=delta<=1:raise ValueError("distortion must lie in [0,1]")
    return 1-binary_entropy(delta) if delta<=0.5 else 0.0


def bernoulli_kl(p:float,q:float)->float:
    if not (0<=p<=1 and 0<=q<=1):raise ValueError("probabilities outside [0,1]")
    if q==0:return 0.0 if p==0 else float('inf')
    if q==1:return 0.0 if p==1 else float('inf')
    return sum(a*log(a/b) for a,b in ((p,q),(1-p,1-q)) if a>0)


def restricted_authority_gap(beta:float):
    """P0 independent fair Y,Z, event E=(Y=1,Z=1).

    Control can change marginal Y~Bern(q), Z remains fair independent.
    To obtain P(E)>=beta>1/4, q>=2 beta, so beta<=1/2 is necessary.
    Restricted path KL is d_Bern(2beta||.5) vs data-processing lower bound
    d_Bern(beta||.25). Returns (achievable optimum, universal lower, gap).
    """
    if not (0.25<=beta<=0.5): raise ValueError("beta must be in [1/4,1/2]")
    actual=bernoulli_kl(2*beta,0.5)
    lower=bernoulli_kl(beta,0.25)
    return actual,lower,actual-lower


def saddle_normal_form_action(tau: float, n: int=2048) -> float:
    """Universal fixed-time action for gradient 1-z^2 on [-1,1].

    F(tau) = (1/4) inf integral_0^tau (z' + 1-z^2)^2 ds.
    Quasipotential F(infinity)=4/3; short-time leading F(tau)~1/tau.
    """
    if not isfinite(tau) or tau<=0:raise ValueError("positive finite tau required")
    if n<2 or n%2:raise ValueError("positive even subdivisions required")
    def g(z):return 1-z*z
    def duration(E):return simpson(lambda z:1/sqrt(g(z)**2+4*E),-1,1,n)
    lo=1e-13;hi=1.0
    while duration(hi)>tau:hi*=4
    if duration(lo)<tau:raise ValueError("tau exceeds fixed-resolution stability")
    for _ in range(53):
        md=(lo+hi)/2
        if duration(md)>tau:lo=md
        else:hi=md
    E=(lo+hi)/2
    return .5*simpson(lambda z:sqrt(g(z)**2+4*E),-1,1,n)+2/3-E*tau
