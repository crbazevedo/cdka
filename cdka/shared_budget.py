"""Shared-bank, pathwise-priced continuation of the v16/v18 finite plant.

This is a changed physical contract, not a refund in v18's separate ledger.
Actual NAND invocations, service and acquisition draw from one finite balance.
Selection uses pre-service health; task and enable use post-service health,
with fresh independent fault flags conditional on that persistent hidden cause.
The finite controller still sees only the inherited resource bins and its
executed-service signal.  See docs/strategy/shared-budget-contract.md.
"""
from dataclasses import dataclass, field, replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, lcm

from .recurrent_maintenance import (
    BITS, Model, Policy, gate_execution, health_after_service, next_health,
    policies, probability, raw_task_success, report_probability,
    select_probability, task_success,
)
from .selective_acquisition import Enable, ELIDE, FRESH, RETAIN, library

State = tuple[int, int, int, int]  # hidden health, first bit, last-two count, balance
STAGES = ('selection', 'service', 'task_base', 'task_gates', 'enable', 'write')
GATE_STAGES = ('selection', 'task', 'enable')
FAILURES = ('resource:selection', 'procedure', 'resource:task', 'task',
            'resource:enable', 'resource:write')
PRICE_GRID = tuple(product((0, 1, 2), (0, 6, 12, 24), (0, 6)))


def _nonnegative_integer(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f'{name} must be a nonnegative integer number of quanta')
    return value


@dataclass(frozen=True)
class Prices:
    gate: int = 0
    write: int = 0
    setup: int = 0

    def __post_init__(self):
        for name in ('gate', 'write', 'setup'):
            _nonnegative_integer(getattr(self, name), name)


@dataclass(frozen=True)
class Contract:
    prices: Prices = field(default_factory=Prices)
    plant: Model = field(default_factory=Model)
    unit: int = 24
    enable_noise: str = 'shared'
    decoupled_error: F | None = None

    def __post_init__(self):
        if type(self.unit) is not int or self.unit <= 0:
            raise ValueError('unit must be a positive integer')
        if not isinstance(self.prices, Prices) or not isinstance(self.plant, Model):
            raise ValueError('Prices and Model instances required')
        if self.enable_noise not in ('shared', 'decoupled'):
            raise ValueError('enable_noise must be shared or decoupled')
        if self.enable_noise == 'decoupled':
            if self.decoupled_error is None:
                raise ValueError('declare the decoupled enable error explicitly')
            gamma = probability(self.decoupled_error)
            if gamma > F(1, 2):
                raise ValueError('decoupled output flip must be at most 1/2')
            object.__setattr__(self, 'decoupled_error', gamma)
        elif self.decoupled_error is not None:
            raise ValueError('shared health does not accept an independent error rate')

    @property
    def capacity(self): return 4 * self.unit
    @property
    def endowment(self): return 4 * self.unit
    @property
    def commissioning(self): return self.unit
    @property
    def task_base(self): return self.unit
    @property
    def service_price(self): return 2 * self.unit
    @property
    def harvest(self): return 2 * self.unit
    @property
    def task_price(self): return self.task_base + 6 * self.prices.gate

    def mode(self, policy, balance):
        return 'skip' if balance < 3 * self.unit else (
            policy.at3 if balance < self.capacity else policy.at4)

    def middle(self, balance):
        return int(3 * self.unit <= balance < self.capacity)

    def enable_rate(self, post_health):
        return (self.plant.rate(post_health) if self.enable_noise == 'shared'
                else self.decoupled_error)

    @property
    def states(self):
        return tuple(product((0, 1), (0, 1), range(3), range(self.capacity + 1)))


def projection(state):
    """Project a full (health, three physical bits, balance) state."""
    z, bits, b = state
    if tuple(bits) not in BITS:
        raise ValueError('three binary diagnostic cells required')
    return z, bits[0], bits[1] + bits[2], b


def _validate_state(contract, state):
    if (not isinstance(state, tuple) or len(state) != 4 or
            any(type(x) is not int for x in state)):
        raise ValueError('state must be four integer coordinates')
    z, a, k, b = state
    if z not in (0, 1) or a not in (0, 1) or k not in range(3) or not 0 <= b <= contract.capacity:
        raise ValueError('state outside the declared physical quotient')


def _validate_enable(enable):
    if not isinstance(enable, Enable) or enable.cost > 2:
        raise ValueError('the declared enable grammar permits at most two NANDs')


@lru_cache(None)
def _diagnostic(plant, health):
    one = plant.diagnostic_error if health == 0 else 1 - plant.diagnostic_error
    return tuple((a, k, (one if a else 1 - one) * comb(2, k) *
                  one ** k * (1 - one) ** (2 - k))
                 for a in (0, 1) for k in range(3))


@lru_cache(None)
def _enable_probability(contract, enable, post_health, repair, middle):
    return enable.probabilities(contract.enable_rate(post_health))[2 * repair + middle]


@dataclass(frozen=True)
class Outcome:
    probability: F
    start_balance: int
    end_balance: int
    successor: State | None
    failure: str | None
    spend: tuple[int, ...]
    gates: tuple[int, ...]
    requested_service: int | None = None
    executed_service: int = 0
    post_health: int | None = None
    enable: int | None = None
    task_success: bool = False
    cycle_complete: bool = False
    writes: int = 0
    services: int = 0
    earned: int = 0
    spilled: int = 0

    @property
    def spend_by_stage(self): return dict(zip(STAGES, self.spend))
    @property
    def gate_events(self): return dict(zip(GATE_STAGES, self.gates))
    @property
    def spent(self): return sum(self.spend)
    @property
    def failure_stage(self): return self.failure


def event_traces(contract, policy, enable, state, terminal=False, raw=False):
    """Exact complete branch traces, including failed prefixes and their spend.

    ``raw`` independently enumerates NAND flags, task sensor/gate events and
    fresh diagnostic words; it shares this explicit event-order bookkeeping.
    Neither mode gives hidden state or fault flags to the installed controller.
    A terminal successful task stops before enable, acquisition, wear and harvest.
    """
    _validate_state(contract, state)
    _validate_enable(enable)
    z, a, k, b = state
    p = contract.plant
    mode = contract.mode(policy, b)
    middle = contract.middle(b)  # frozen at epoch entry, before any debit
    bits = (a, int(k >= 1), int(k == 2))
    choice_gates = 6 if mode in ('vote', 'inverse') else 0
    choice_cost = choice_gates * contract.prices.gate
    results = []

    def emit(mass, balance, spend, gates, **kw):
        if mass:
            results.append(Outcome(F(mass), b, balance, spend=tuple(spend),
                                   gates=tuple(gates), **kw))

    blank = [0] * len(STAGES)
    if b < choice_cost:
        emit(F(1), b, blank, (0, 0, 0), successor=None, failure='resource:selection')
        return tuple(results)
    before_service = b - choice_cost
    chosen = {}
    if raw and choice_gates:
        for flags in product((0, 1), repeat=6):
            q = gate_execution(bits, flags) ^ int(mode == 'inverse')
            mass = p.rate(z) ** sum(flags) * (1 - p.rate(z)) ** (6 - sum(flags))
            chosen[q] = chosen.get(q, F(0)) + mass
    else:
        one = select_probability(p, z, bits, mode)
        chosen = {0: 1 - one, 1: one}

    for requested, pd in chosen.items():
        if not pd:
            continue
        repair = int(requested and before_service >= contract.service_price + contract.task_price)
        spend = [choice_cost, repair * contract.service_price, 0, 0, 0, 0]
        gates = [choice_gates, 0, 0]
        balance = before_service - spend[1]
        common = dict(requested_service=requested, executed_service=repair,
                      services=repair)
        if repair:
            emit(pd * p.procedure_failure, balance, spend, gates, successor=None,
                 failure='procedure', **common)
        procedure = 1 - p.procedure_failure if repair else F(1)
        for h, ph in health_after_service(p, z, repair):
            mass = pd * procedure * ph
            if not mass:
                continue
            branch = dict(common, post_health=h)
            if balance < contract.task_price:
                emit(mass, balance, spend, gates, successor=None,
                     failure='resource:task', **branch)
                continue
            after_task = balance - contract.task_price
            task_spend = list(spend)
            task_spend[2] = contract.task_base
            task_spend[3] = 6 * contract.prices.gate
            task_gates = [choice_gates, 6, 0]
            success = raw_task_success(p, h) if raw else task_success(p, h)
            emit(mass * (1 - success), after_task, task_spend, task_gates,
                 successor=None, failure='task', **branch)
            live = mass * success
            if terminal:
                emit(live, after_task, task_spend, task_gates,
                     successor=(h, a, k, after_task), failure=None,
                     task_success=True, **branch)
                continue
            enable_cost = enable.cost * contract.prices.gate
            if after_task < enable_cost:
                emit(live, after_task, task_spend, task_gates, successor=None,
                     failure='resource:enable', task_success=True, **branch)
                continue
            after_enable = after_task - enable_cost
            enable_spend = list(task_spend)
            enable_spend[4] = enable_cost
            enable_gates = [choice_gates, 6, enable.cost]
            if raw:
                outputs = {}
                gamma = contract.enable_rate(h)
                for flags in product((0, 1), repeat=enable.cost):
                    e = enable.run(repair, middle, flags)
                    pe = gamma ** sum(flags) * (1 - gamma) ** (enable.cost - sum(flags))
                    outputs[e] = outputs.get(e, F(0)) + pe
            else:
                pe = _enable_probability(contract, enable, h, repair, middle)
                outputs = {0: 1 - pe, 1: pe}
            for e, pe in outputs.items():
                write_cost = e * contract.prices.write
                info = dict(branch, enable=e, task_success=True)
                if after_enable < write_cost:
                    emit(live * pe, after_enable, enable_spend, enable_gates,
                         successor=None, failure='resource:write', **info)
                    continue
                complete_spend = list(enable_spend)
                complete_spend[5] = write_cost
                remaining = after_enable - write_cost
                target_balance = min(contract.capacity, remaining + contract.harvest)
                spill = max(0, remaining + contract.harvest - contract.capacity)
                if not e:
                    reports = ((a, k, F(1)),)
                elif raw:
                    reports = tuple((word[0], word[1] + word[2],
                                     report_probability(word, h, p.diagnostic_error))
                                    for word in BITS)
                else:
                    reports = _diagnostic(p, h)
                for aa, kk, pm in reports:
                    for zz, pz in next_health(p, h):
                        emit(live * pe * pm * pz, target_balance,
                             complete_spend, enable_gates,
                             successor=(zz, aa, kk, target_balance), failure=None,
                             cycle_complete=True, writes=e, earned=contract.harvest,
                             spilled=spill, **info)
    return tuple(results)


@dataclass(frozen=True)
class StepRow:
    transitions: dict
    spend_by_stage: dict
    failures_by_cause: dict
    gate_events: dict
    writes: F
    services: F
    earned: F
    spilled: F
    failed_remaining: F
    task_successes: F
    completed_cycles: F

    @property
    def spent(self): return sum(self.spend_by_stage.values(), F(0))
    @property
    def survival(self): return sum(self.transitions.values(), F(0))


def _add(out, key, value):
    if value:
        out[key] = out.get(key, F(0)) + value


@lru_cache(maxsize=2048)
def _step_row(contract, mode, enable, state, terminal):
    # The policy's unused bin is irrelevant to this row and must not defeat reuse.
    traces = event_traces(contract, Policy(mode, mode), enable, state, terminal)
    row = {}
    spend = {name: F(0) for name in STAGES}
    failures = {name: F(0) for name in FAILURES}
    gates = {name: F(0) for name in GATE_STAGES}
    quantities = dict(writes=F(0), services=F(0), earned=F(0), spilled=F(0),
                      failed_remaining=F(0), task_successes=F(0), completed_cycles=F(0))
    total = F(0)
    for trace in traces:
        mass = trace.probability
        total += mass
        if trace.successor is not None:
            _add(row, trace.successor, mass)
        else:
            _add(failures, trace.failure, mass)
            quantities['failed_remaining'] += mass * trace.end_balance
        for name, value in zip(STAGES, trace.spend):
            spend[name] += mass * value
        for name, value in zip(GATE_STAGES, trace.gates):
            gates[name] += mass * value
        for name in ('writes', 'services', 'earned', 'spilled'):
            quantities[name] += mass * getattr(trace, name)
        quantities['task_successes'] += mass * trace.task_success
        quantities['completed_cycles'] += mass * trace.cycle_complete
    if total != 1:
        raise AssertionError('causal outcomes must sum exactly to one')
    return StepRow(row, spend, failures, gates, **quantities)


METRICS = (tuple('spend:' + x for x in STAGES) +
           tuple('failure:' + x for x in FAILURES) +
           tuple('gates:' + x for x in GATE_STAGES) +
           ('writes', 'services', 'earned', 'spilled', 'failed_remaining',
            'task_successes', 'completed_cycles'))


def _metrics(row):
    return (tuple(row.spend_by_stage[x] for x in STAGES) +
            tuple(row.failures_by_cause[x] for x in FAILURES) +
            tuple(row.gate_events[x] for x in GATE_STAGES) +
            tuple(getattr(row, x) for x in METRICS[-7:]))


@lru_cache(None)
def _denominator(contract, enable):
    p = contract.plant
    bank = lcm(p.healthy_error.denominator, p.degraded_error.denominator) ** 6
    task = lcm(*(task_success(p, h).denominator for h in (0, 1)))
    en = lcm(*(q.denominator for h in (0, 1)
               for q in enable.probabilities(contract.enable_rate(h))))
    return (bank * p.procedure_failure.denominator * p.restoration.denominator *
            task * en * p.diagnostic_error.denominator ** 3 * p.degradation.denominator)


@lru_cache(maxsize=65536)
def _integer_row(contract, mode, enable, state, terminal):
    row = _step_row(contract, mode, enable, state, terminal)
    den = _denominator(contract, enable)

    def integer(value):
        scaled = value * den
        if scaled.denominator != 1:
            raise AssertionError('declared primitive denominator does not cover a row')
        return scaled.numerator

    return (tuple((target, integer(q)) for target, q in row.transitions.items()),
            tuple(integer(q) for q in _metrics(row)))


@dataclass(frozen=True)
class Kernel:
    contract: Contract
    policy: Policy
    enable: Enable
    terminal: bool = False

    @property
    def states(self): return self.contract.states
    @property
    def denominator(self): return _denominator(self.contract, self.enable)
    def row(self, state):
        _validate_state(self.contract, state)
        return _step_row(self.contract, self.contract.mode(self.policy, state[3]),
                         self.enable, state, self.terminal)
    def transition(self, state): return self.row(state).transitions
    def __getitem__(self, state): return self.transition(state)
    def rows(self, states=None):
        return {s: self.transition(s) for s in (self.states if states is None else states)}
    def integer_row(self, state):
        return _integer_row(self.contract, self.contract.mode(self.policy, state[3]),
                            self.enable, state, self.terminal)


@lru_cache(None)
def compile_kernel(contract, policy, enable, terminal=False):
    _validate_enable(enable)
    # Installation is paid only at initialization; both setup prices share rows.
    physical = replace(contract, prices=replace(contract.prices, setup=0))
    return Kernel(physical, policy, enable, bool(terminal))


@dataclass(frozen=True)
class Initial:
    measure: dict
    spend_by_stage: dict
    failures_by_cause: dict
    writes: F
    failed_remaining: F


def initialize(contract, enable, prior=F(1, 2)):
    """Commission, install routing, then acquire the mandatory initial report."""
    _validate_enable(enable)
    prior = probability(prior)
    balance = contract.endowment
    spend = dict(commissioning=F(0), setup=F(0), initial_write=F(0))
    for name, cost in (('commissioning', contract.commissioning),
                       ('setup', enable.cost * contract.prices.setup),
                       ('initial_write', contract.prices.write)):
        if balance < cost:
            return Initial({}, spend, {'resource:' + name: F(1)}, F(0), F(balance))
        balance -= cost
        spend[name] = F(cost)
    law = {}
    for z, pz in ((0, 1 - prior), (1, prior)):
        for a, k, pd in _diagnostic(contract.plant, z):
            _add(law, (z, a, k, balance), pz * pd)
    return Initial(law, spend, {}, F(1), F(0))


def initial_measure(contract, enable, prior=F(1, 2)):
    return initialize(contract, enable, prior).measure


@dataclass(frozen=True)
class RunSummary:
    survival: F
    spent: F
    spend_by_stage: dict
    failures_by_cause: dict
    gate_events: dict
    writes: F
    services: F
    earned: F
    spilled: F
    failed_remaining: F
    remaining: F
    task_successes: F
    completed_cycles: F
    alive: dict
    balance_distribution: dict
    curve: tuple
    objective: str


def run_exact(contract=Contract(), policy=Policy(), enable=ELIDE, horizon=8,
              objective='cycles', prior=F(1, 2)):
    """Exact sparse integer propagation, including all failed-prefix charges.

    ``tasks`` uses H-1 ordinary cycle kernels and one terminal task kernel.
    ``cycles`` completes the acquisition/retention phase of every cycle.
    Both objectives pay the same commissioning and startup acquisition.
    """
    if type(horizon) is not int or horizon < 0:
        raise ValueError('finite nonnegative horizon required')
    if objective not in ('cycles', 'tasks'):
        raise ValueError('objective must be cycles or tasks')
    initial = initialize(contract, enable, prior)
    md = lcm(*(q.denominator for q in initial.measure.values()))
    law = {s: int(q * md) for s, q in initial.measure.items()}
    totals = [0] * len(METRICS)
    curves = [sum(initial.measure.values(), F(0))]
    regular = compile_kernel(contract, policy, enable)
    terminal = compile_kernel(contract, policy, enable, True)
    for t in range(horizon):
        kernel = terminal if objective == 'tasks' and t == horizon - 1 else regular
        den = kernel.denominator
        next_law = {}
        next_totals = [q * den for q in totals]
        for state, mass in law.items():
            targets, rewards = kernel.integer_row(state)
            for target, numerator in targets:
                next_law[target] = next_law.get(target, 0) + mass * numerator
            for j, reward in enumerate(rewards):
                next_totals[j] += mass * reward
        law = next_law
        totals = next_totals
        md *= den
        curves.append(F(sum(law.values()), md))
    measured = {name: F(value, md) for name, value in zip(METRICS, totals)}
    spend = dict(initial.spend_by_stage)
    spend.update({name: measured['spend:' + name] for name in STAGES})
    failures = {name: measured['failure:' + name] for name in FAILURES}
    for name, q in initial.failures_by_cause.items():
        _add(failures, name, q)
    gates = {name: measured['gates:' + name] for name in GATE_STAGES}
    alive = {state: F(mass, md) for state, mass in law.items()}
    balances = {}
    for state, mass in alive.items():
        _add(balances, state[3], mass)
    failed_remaining = initial.failed_remaining + measured['failed_remaining']
    remaining = failed_remaining + sum((mass * s[3] for s, mass in alive.items()), F(0))
    spent = sum(spend.values(), F(0))
    survival = sum(alive.values(), F(0))
    if survival + sum(failures.values(), F(0)) != 1:
        raise AssertionError('unconditional live and stopped mass must sum to one')
    if spent + remaining + measured['spilled'] != contract.endowment + measured['earned']:
        raise AssertionError('pathwise resource conservation failed in expectation')
    return RunSummary(survival, spent, spend, failures, gates,
                      initial.writes + measured['writes'], measured['services'],
                      measured['earned'], measured['spilled'], failed_remaining,
                      remaining, measured['task_successes'], measured['completed_cycles'],
                      alive, balances, tuple(curves), objective)


def clear_row_caches():
    """Drop large physical row caches between unrelated parameter sweeps."""
    _integer_row.cache_clear()
    _step_row.cache_clear()


def cache_info():
    return {'integer_rows': _integer_row.cache_info(), 'fraction_rows': _step_row.cache_info()}
