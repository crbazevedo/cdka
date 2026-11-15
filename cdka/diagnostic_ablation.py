"""Fixed-cost counterfactual removal of diagnostic report content.

This is an analytical intervention, not an additional executable controller
or free random source.  Each paid acquisition draws a whole report from the
same frozen prior-predictive law, independently of the actual bank health.
The report's three cells retain their original marginal dependence.  Actual
health still controls selector/task/enable faults, restoration and wear.

The shared-budget event order, all debits, failed-prefix rewards and trusted
interfaces are unchanged.  Only the report conditional law is intervened on;
the initial report and every successful later acquisition use that law.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as F
from functools import lru_cache, partial
from math import comb, lcm

from . import shared_budget as sb
from .optional_startup import initialize, propagate
from .recurrent_maintenance import Policy, probability
from .selective_acquisition import ELIDE


def _add(out, key, value):
    if value:
        out[key] = out.get(key, F(0)) + value


@lru_cache(None)
def report_marginal(plant, prior=F(1, 2)):
    """Prior mixture of entire diagnostic words, projected by tail symmetry.

    The prior is frozen once for the experiment.  It is not recomputed from
    an endogenous live population or a hidden current-health branch.
    """
    prior = probability(prior)
    marginal = {}
    for health, mass in ((0, 1 - prior), (1, prior)):
        one = plant.diagnostic_error if health == 0 else 1 - plant.diagnostic_error
        for first in (0, 1):
            for tail in range(3):
                value = (mass * (one if first else 1 - one) * comb(2, tail) *
                         one ** tail * (1 - one) ** (2 - tail))
                _add(marginal, (first, tail), value)
    return tuple(marginal.items())


@lru_cache(None)
def _denominator(contract, enable, prior, terminal):
    original = sb.compile_kernel(contract, Policy(), enable, terminal).denominator
    if terminal:
        return original
    return original * lcm(*(q.denominator for _, q in report_marginal(contract.plant, prior)))


@lru_cache(maxsize=2048)
def _row(contract, mode, enable, state, prior, terminal):
    policy = Policy(mode, mode)
    original = sb.compile_kernel(contract, policy, enable, terminal).row(state)
    if terminal:
        return original
    retained, renewed = {}, {}
    for event in sb.event_traces(contract, policy, enable, state):
        if event.successor is None:
            continue
        health, first, tail, balance = event.successor
        if event.enable == 1:
            # Sum out the original report draw before imposing the independent
            # full-word law.  Keep its joint successor health/resource mass.
            _add(renewed, (health, balance), event.probability)
        else:
            _add(retained, event.successor, event.probability)
    targets = dict(retained)
    for (health, balance), mass in renewed.items():
        for (first, tail), report_mass in report_marginal(contract.plant, prior):
            _add(targets, (health, first, tail, balance), mass * report_mass)
    # No same-epoch event or reward reads the newly produced report.  This
    # conditional-law intervention therefore preserves each original metric.
    return replace(original, transitions=targets)


def _metrics(row):
    return (tuple(row.spend_by_stage[x] for x in sb.STAGES) +
            tuple(row.failures_by_cause[x] for x in sb.FAILURES) +
            tuple(row.gate_events[x] for x in sb.GATE_STAGES) +
            tuple(getattr(row, name) for name in sb.METRICS[-7:]))


@lru_cache(maxsize=65536)
def _integer_row(contract, mode, enable, state, prior, terminal):
    row = _row(contract, mode, enable, state, prior, terminal)
    denominator = _denominator(contract, enable, prior, terminal)

    def integer(value):
        scaled = value * denominator
        if scaled.denominator != 1:
            raise AssertionError('primitive denominator does not cover the intervened row')
        return scaled.numerator

    return (tuple((target, integer(mass)) for target, mass in row.transitions.items()),
            tuple(integer(value) for value in _metrics(row)))


@dataclass(frozen=True)
class Kernel:
    contract: sb.Contract
    policy: Policy
    enable: object
    prior: F = F(1, 2)
    terminal: bool = False

    @property
    def states(self):
        return self.contract.states

    @property
    def denominator(self):
        return _denominator(self.contract, self.enable, self.prior, self.terminal)

    def row(self, state):
        return _row(self.contract, self.contract.mode(self.policy, state[3]),
                    self.enable, state, self.prior, self.terminal)

    def transition(self, state):
        return self.row(state).transitions

    def __getitem__(self, state):
        return self.transition(state)

    def integer_row(self, state):
        return _integer_row(self.contract, self.contract.mode(self.policy, state[3]),
                            self.enable, state, self.prior, self.terminal)


@lru_cache(None)
def compile_kernel(contract, policy, enable, terminal=False, prior=F(1, 2)):
    """Compile the all-acquisition null channel at a declared frozen prior."""
    original = sb.compile_kernel(contract, policy, enable, terminal)
    return Kernel(original.contract, policy, enable, probability(prior), bool(terminal))


def run_exact(contract=sb.Contract(), policy=Policy(), enable=ELIDE, horizon=8,
              objective='tasks', prior=F(1, 2)):
    """Paid startup and all renewals under the fixed-cost report intervention.

    This is not the narrower initial-only ``optional_startup.independent``
    control: later reports here are also independent of their actual source
    health.  Report margins after endogenous filtering need not match those
    under the original channel, because the frozen prior is not updated.
    """
    prior = probability(prior)
    initial = initialize(contract, policy, enable, prior, preparation='independent')
    return propagate(contract, policy, enable, initial, horizon, objective,
                     kernel_factory=partial(compile_kernel, prior=prior))


def clear_row_caches():
    """Release bounded row caches between unrelated price scans."""
    _integer_row.cache_clear()
    _row.cache_clear()


def cache_info():
    return {'integer_rows': _integer_row.cache_info(),
            'fraction_rows': _row.cache_info()}
