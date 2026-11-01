"""CDKA: reliability exponents and endogenous sensing-vs-actuation budgets.

All statements are finite-model demonstrations built from classical
large-deviation/log-sum-exp principles. The two-well failure probabilities
are an *exponential surrogate*, not exact fixed-time diffusion exit laws.
The source of physical barriers is cdka.variational.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, log1p

from .variational import critical_tilt, left_barrier, right_barrier, binary_entropy


def effective_failure_exponent(good: float, bad: float, error: float) -> float:
    """Under conditional channel/failure independence: min(good,bad+error)."""
    if not all(isfinite(x) and x >= 0 for x in (good, bad, error)):
        raise ValueError("nonnegative finite exponents required")
    return min(good, bad + error)


def sensor_error(epsilon: float, kappa: float) -> float:
    """Symmetric sensor's wrong-classification probability (BSC surrogate).

    The factor 1/2 ensures an uninformative sensor at kappa=0.
    -epsilon*log P(error) -> kappa for epsilon -> 0 and kappa>0.
    """
    if not (isfinite(epsilon) and epsilon > 0 and isfinite(kappa) and kappa >= 0):
        raise ValueError("epsilon>0, kappa>=0 and both finite required")
    return 0.5 * exp(-kappa / epsilon)


def sensor_information(epsilon: float, kappa: float) -> float:
    """I(W;Y) in bits for equiprobable W and symmetric sensor error."""
    return 1.0 - binary_entropy(sensor_error(epsilon, kappa))


def finite_noise_failure_rate(
    epsilon: float, good: float, bad: float, kappa: float
) -> float:
    """Return -epsilon * log(P(failure)) without exponential underflow.

    The surrogate uses P(failure|correct)=exp(-good/epsilon),
    P(failure|wrong)=exp(-bad/epsilon) and a BSC sensor error
    delta=0.5 exp(-kappa/epsilon). The physical noise and sensor
    decision error are CONDITIONALLY independent after the state is fixed.
    """
    if not (isfinite(epsilon) and epsilon > 0):
        raise ValueError("epsilon must be finite and positive")
    effective_failure_exponent(good, bad, kappa)
    log_wrong = log(0.5) - kappa / epsilon
    delta = exp(log_wrong)
    log_correct = log1p(-delta) - good / epsilon
    log_mismatch = log_wrong - bad / epsilon
    top = max(log_correct, log_mismatch)
    bottom = min(log_correct, log_mismatch)
    return -epsilon * (top + log1p(exp(bottom - top)))


@dataclass(frozen=True)
class OptimalReliabilityAllocation:
    budget: float
    gamma: float
    action_tilt: float
    sensing_resource: float
    good_barrier: float
    bad_barrier: float
    sensor_error_exponent: float
    effective_exponent: float


def quartic_barrier_pair(tilt: float) -> tuple[float, float]:
    """(good, bad) barriers for the two symmetric context-conditioned wells.

    Right well protected by u=+tilt and left by u=-tilt (good).
    A wrong sign of u makes each corresponding initial well less stable.
    Assumes 0<=tilt<2/(3 sqrt(3)) to retain distinct stationary wells.
    """
    if not (isfinite(tilt) and 0 <= tilt < critical_tilt()):
        raise ValueError("tilt must lie in [0, saddle-node threshold)")
    return right_barrier(tilt), left_barrier(tilt)


def optimal_reliability_allocation(
    budget: float, gamma: float = 2.0, iterations: int = 75
) -> OptimalReliabilityAllocation:
    """Unique max-min optimum on 0<=tilt<=B for 0<B<critical_tilt.

    A physically illustrative shared resource B is allocated as:
      action tilt a, sensing effort s=B-a, sensor error exponent gamma*s.
    Effective failure exponent is
      min{Delta_good(a), Delta_bad(a)+gamma*(B-a)}.
    Exact optimality follows from opposite monotonicities of the branches.
    """
    if not (isfinite(budget) and 0 <= budget < critical_tilt()):
        raise ValueError("0<=budget<critical_tilt required")
    if not (isfinite(gamma) and gamma > 0):
        raise ValueError("gamma must be positive finite")
    if budget == 0:
        return OptimalReliabilityAllocation(
            0.0, gamma, 0.0, 0.0, 0.25, 0.25, 0.0, 0.25
        )
    lo, hi = 0.0, budget
    for _ in range(iterations):
        mid = (lo + hi) / 2
        good, bad = quartic_barrier_pair(mid)
        difference = good - bad - gamma * (budget - mid)
        if difference >= 0:
            hi = mid
        else:
            lo = mid
    a = (lo + hi) / 2
    s = budget - a
    good, bad = quartic_barrier_pair(a)
    kappa = gamma * s
    exponent = effective_failure_exponent(good, bad, kappa)
    return OptimalReliabilityAllocation(
        budget, gamma, a, s, good, bad, kappa, exponent
    )
