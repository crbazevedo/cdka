"""Optional blind preparation and an initial-information intervention for SB.

The physical cycle kernels and prices are those of :mod:`shared_budget`.
``fresh`` is the original paid informative preparation.  ``omit`` can be
installed only with a blind maintenance table: both bins choose skip/service,
so no continuation can read an uninitialized diagnostic register.  Its dummy
record coordinates are evaluator labels, not a supplied physical report.

``independent`` is a matched-cost causal intervention on the initial joint
law.  It preserves the entire report marginal and hidden-health marginal but
removes their dependence.  It does not claim an installed free random source.
Subsequent requested acquisitions retain the original informative sensor law.
"""
from fractions import Fraction as F
from math import lcm

from . import shared_budget as sb
from .recurrent_maintenance import Policy, probability
from .selective_acquisition import Enable, ELIDE


PREPARATIONS = ('fresh', 'omit', 'independent')


def blind(policy):
    """Whether the complete installed maintenance table never reads a report."""
    return (isinstance(policy, Policy) and
            policy.at3 in ('skip', 'service') and
            policy.at4 in ('skip', 'service'))


def _validate(policy, enable, preparation):
    if not isinstance(policy, Policy):
        raise ValueError('an installed Policy is required')
    if not isinstance(enable, Enable) or enable.cost > 2:
        raise ValueError('the declared enable grammar permits at most two NANDs')
    if preparation not in PREPARATIONS:
        raise ValueError('preparation must be fresh, omit or independent')
    if preparation == 'omit' and not blind(policy):
        raise ValueError('omitted preparation requires both bins to be blind')


def _add(out, key, value):
    if value:
        out[key] = out.get(key, F(0)) + value


def initialize(contract, policy, enable, prior=F(1, 2), preparation='fresh'):
    """Return the paid startup subdistribution under the declared preparation.

    Every preparation starts from the same gross endowment and pays the same
    commissioning and enable-routing prices.  Omission pays no initial write
    and returns two possible health labels with dummy unread record (0, 0).
    There is no change to later task, maintenance, acquisition or failure law.

    For ``independent`` the product P(z) P(D) preserves the *joint three-cell*
    marginal of the old report; replacing it with three fair independent bits
    would be a different intervention.  This is an analytical causal control.
    """
    _validate(policy, enable, preparation)
    prior = probability(prior)
    if preparation != 'omit':
        initial = sb.initialize(contract, enable, prior)
        if preparation == 'fresh' or not initial.measure:
            return initial
        marginal = {}
        for (_, first, tail, balance), mass in initial.measure.items():
            _add(marginal, (first, tail, balance), mass)
        law = {}
        for health, mass in ((0, 1 - prior), (1, prior)):
            for (first, tail, balance), report_mass in marginal.items():
                _add(law, (health, first, tail, balance), mass * report_mass)
        return sb.Initial(law, dict(initial.spend_by_stage),
                          dict(initial.failures_by_cause), initial.writes,
                          initial.failed_remaining)

    balance = contract.endowment
    spend = dict(commissioning=F(0), setup=F(0), initial_write=F(0))
    for name, cost in (('commissioning', contract.commissioning),
                       ('setup', enable.cost * contract.prices.setup)):
        if balance < cost:
            return sb.Initial({}, spend, {'resource:' + name: F(1)},
                              F(0), F(balance))
        balance -= cost
        spend[name] = F(cost)
    law = {}
    for health, mass in ((0, 1 - prior), (1, prior)):
        _add(law, (health, 0, 0, balance), mass)
    return sb.Initial(law, spend, {}, F(0), F(0))


def run_exact(contract=sb.Contract(), policy=Policy(), enable=ELIDE, horizon=8,
              objective='cycles', prior=F(1, 2), preparation='fresh'):
    """Exact unnormalized propagation through the frozen shared-budget kernels.

    ``tasks`` applies H-1 complete cycles and the common terminal-task kernel.
    ``cycles`` applies H complete cycles.  Startup is charged even at H=0;
    both endpoints retain costs and remaining resources on failed prefixes.

    With omitted preparation, ``alive`` record coordinates before the first
    paid acquisition are dummy labels.  Only their projection onto health and
    balance is a physical statement.  Blindness makes all reported rewards,
    failures and projected continuation laws independent of that placeholder.
    """
    initial = initialize(contract, policy, enable, prior, preparation)
    return propagate(contract, policy, enable, initial, horizon, objective)


def propagate(contract, policy, enable, initial, horizon=8, objective='cycles',
              kernel_factory=sb.compile_kernel):
    """Propagate a fully accounted Initial through supplied exact cycle kernels.

    A kernel factory uses the frozen ``compile_kernel`` calling convention
    and returns ``denominator`` plus ``integer_row(state)`` in ``sb.METRICS``
    order.  This separation permits declared causal channel interventions
    while retaining exactly one startup/failed-prefix/resource accountant.
    The supplied Initial must already include all startup charges and stops.
    """
    _validate(policy, enable, 'fresh')
    if not isinstance(initial, sb.Initial):
        raise ValueError('a fully accounted Initial is required')
    if type(horizon) is not int or horizon < 0:
        raise ValueError('finite nonnegative horizon required')
    if objective not in ('cycles', 'tasks'):
        raise ValueError('objective must be cycles or tasks')
    denominator = lcm(*(mass.denominator for mass in initial.measure.values()))
    law = {state: int(mass * denominator)
           for state, mass in initial.measure.items()}
    totals = [0] * len(sb.METRICS)
    curves = [sum(initial.measure.values(), F(0))]
    regular = kernel_factory(contract, policy, enable)
    terminal = kernel_factory(contract, policy, enable, True)
    for step in range(horizon):
        kernel = terminal if objective == 'tasks' and step == horizon - 1 else regular
        row_denominator = kernel.denominator
        next_law = {}
        next_totals = [value * row_denominator for value in totals]
        for state, mass in law.items():
            targets, rewards = kernel.integer_row(state)
            for target, numerator in targets:
                next_law[target] = next_law.get(target, 0) + mass * numerator
            for index, reward in enumerate(rewards):
                next_totals[index] += mass * reward
        law, totals = next_law, next_totals
        denominator *= row_denominator
        curves.append(F(sum(law.values()), denominator))

    measured = {name: F(value, denominator)
                for name, value in zip(sb.METRICS, totals)}
    spend = dict(initial.spend_by_stage)
    spend.update({name: measured['spend:' + name] for name in sb.STAGES})
    failures = {name: measured['failure:' + name] for name in sb.FAILURES}
    for name, mass in initial.failures_by_cause.items():
        _add(failures, name, mass)
    gates = {name: measured['gates:' + name] for name in sb.GATE_STAGES}
    alive = {state: F(mass, denominator) for state, mass in law.items()}
    balances = {}
    for state, mass in alive.items():
        _add(balances, state[3], mass)
    failed_remaining = initial.failed_remaining + measured['failed_remaining']
    remaining = failed_remaining + sum((mass * state[3]
                                       for state, mass in alive.items()), F(0))
    spent = sum(spend.values(), F(0))
    survival = sum(alive.values(), F(0))
    if survival + sum(failures.values(), F(0)) != 1:
        raise AssertionError('unconditional live and stopped mass must sum to one')
    if spent + remaining + measured['spilled'] != contract.endowment + measured['earned']:
        raise AssertionError('pathwise resource conservation failed in expectation')
    return sb.RunSummary(
        survival, spent, spend, failures, gates,
        initial.writes + measured['writes'], measured['services'],
        measured['earned'], measured['spilled'], failed_remaining,
        remaining, measured['task_successes'], measured['completed_cycles'],
        alive, balances, tuple(curves), objective)
