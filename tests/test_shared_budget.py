"""Independent physical checks for the unified, pathwise resource contract.

The reference below enumerates NAND output flags and cell errors directly.  It
does not call shared_budget's event enumerator, row builder, or scalar physical
probability helpers.  Aggregation only follows conditional independence after
the hidden, shared bank health and executed service have been fixed.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
import unittest

from cdka import shared_budget as sb
from cdka.recurrent_maintenance import Model, Policy, forward, policies
from cdka.selective_acquisition import Enable, ELIDE, FRESH, RETAIN, library
from cdka.selective_acquisition import evaluate as inherited_evaluate


BITS = tuple(product((0, 1), repeat=3))
VOTER_WIRES = ((0, 1), (0, 2), (1, 2), (3, 4), (6, 6), (5, 7))


@lru_cache(None)
def flag_law(size, error):
    out = []
    for flags in product((0, 1), repeat=size):
        probability = error ** sum(flags) * (1 - error) ** (size - sum(flags))
        if probability:
            out.append((flags, probability))
    return tuple(out)


def raw_voter(bits, flags):
    wires = list(bits)
    for (left, right), flag in zip(VOTER_WIRES, flags):
        wires.append((1 - (wires[left] & wires[right])) ^ flag)
    return wires[-1]


def raw_enable(circuit, repair, middle, flags):
    wires = [0, 1, repair, middle]
    for (left, right), flag in zip(circuit.gates, flags):
        wires.append((1 - (wires[left] & wires[right])) ^ flag)
    return wires[circuit.output]


@lru_cache(None)
def raw_task_probability(plant, health):
    error = (plant.healthy_error, plant.degraded_error)[health]
    success = F(0)
    for world in (0, 1):
        for sensor_flags, sensor_mass in flag_law(3, plant.task_sensor_error):
            readings = tuple(world ^ flag for flag in sensor_flags)
            for gate_flags, gate_mass in flag_law(6, error):
                if raw_voter(readings, gate_flags) == world:
                    success += sensor_mass * gate_mass / 2
    return success


def raw_selector(plant, health, bits, mode):
    if mode in ('skip', 'service'):
        return ((int(mode == 'service'), F(1)),)
    error = (plant.healthy_error, plant.degraded_error)[health]
    decision = defaultdict(F)
    for flags, mass in flag_law(6, error):
        decision[raw_voter(bits, flags) ^ int(mode == 'inverse')] += mass
    return tuple(decision.items())


def projection(health, bits, balance):
    return health, bits[0], bits[1] + bits[2], balance


@lru_cache(maxsize=128)
def oracle_events(contract, policy, circuit, state, terminal=False):
    """Small exact event oracle, including stopped paths and their paid prefix."""
    plant = contract.plant
    gate, write = contract.prices.gate, contract.prices.write
    health, first, tail_sum, entry_balance = state
    old_bits = (first, int(tail_sum >= 1), int(tail_sum == 2))
    middle = int(72 <= entry_balance < 96)
    mode = 'skip' if entry_balance < 72 else (policy.at3 if middle else policy.at4)
    selection_price = 6 * gate if mode in ('vote', 'inverse') else 0
    events = []

    def emit(mass, balance, spend, failure=None, successor=None,
             writes=0, services=0, gates=0, earned=0,
             task_success=0, cycle_complete=0):
        if mass:
            events.append(dict(probability=mass, balance=balance,
                               spend=dict(spend), failure=failure,
                               successor=successor, writes=writes,
                               services=services, gates=gates, earned=earned,
                               task_success=task_success,
                               cycle_complete=cycle_complete))

    if entry_balance < selection_price:
        emit(F(1), entry_balance, {}, failure='resource_selection')
        return events
    first_spend = {'selection': selection_price}
    after_selection = entry_balance - selection_price
    selection_gates = 6 if mode in ('vote', 'inverse') else 0
    for requested, decision_mass in raw_selector(plant, health, old_bits, mode):
        repair = int(requested and after_selection >= 48 + 24 + 6 * gate)
        after_service = after_selection - 48 * repair
        prefix = dict(first_spend, service=48 * repair)
        procedure_survival = 1 - plant.procedure_failure if repair else F(1)
        if repair:
            emit(decision_mass * (1 - procedure_survival), after_service,
                 prefix, failure='procedure', services=1, gates=selection_gates)
        health_branches = ((0, plant.restoration), (health, 1 - plant.restoration)) if repair else ((health, F(1)),)
        for post_health, health_mass in health_branches:
            mass = decision_mass * procedure_survival * health_mass
            if not mass:
                continue
            task_price = 24 + 6 * gate
            if after_service < task_price:
                emit(mass, after_service, prefix, failure='resource_task',
                     services=repair, gates=selection_gates)
                continue
            after_task = after_service - task_price
            task_spend = dict(prefix, task=task_price)
            task_gates = selection_gates + 6
            correct = raw_task_probability(plant, post_health)
            emit(mass * (1 - correct), after_task, task_spend,
                 failure='task', services=repair, gates=task_gates)
            successful = mass * correct
            if terminal:
                emit(successful, after_task, task_spend,
                     successor=projection(post_health, old_bits, after_task),
                     services=repair, gates=task_gates, task_success=1)
                continue
            enable_price = circuit.cost * gate
            if after_task < enable_price:
                emit(successful, after_task, task_spend,
                     failure='resource_enable', services=repair,
                     gates=task_gates, task_success=1)
                continue
            after_enable = after_task - enable_price
            enable_spend = dict(task_spend, enable=enable_price)
            rate = (plant.healthy_error, plant.degraded_error)[post_health]
            for flags, gate_mass in flag_law(circuit.cost, rate):
                enabled = raw_enable(circuit, repair, middle, flags)
                enabled_mass = successful * gate_mass
                execution_gates = task_gates + circuit.cost
                if enabled and after_enable < write:
                    emit(enabled_mass, after_enable, enable_spend,
                         failure='resource_write', services=repair,
                         gates=execution_gates, task_success=1)
                    continue
                after_write = after_enable - enabled * write
                full_spend = dict(enable_spend, write=enabled * write)
                words = tuple((tuple(post_health ^ bit for bit in noise), weight)
                              for noise, weight in flag_law(3, plant.diagnostic_error)) if enabled else ((old_bits, F(1)),)
                drift = ((0, 1 - plant.degradation), (1, plant.degradation)) if post_health == 0 else ((1, F(1)),)
                balance = min(96, after_write + 48)
                for word, word_mass in words:
                    for new_health, drift_mass in drift:
                        emit(enabled_mass * word_mass * drift_mass, balance,
                             full_spend,
                             successor=projection(new_health, word, balance),
                             writes=enabled, services=repair,
                             gates=execution_gates, earned=48,
                             task_success=1, cycle_complete=1)
    return events


def summarize(events):
    row, failures = defaultdict(F), defaultdict(F)
    totals = {key: F(0) for key in ('spend', 'writes', 'services', 'gates',
                                  'earned', 'task_success', 'cycle_complete')}
    for event in events:
        mass = event['probability']
        if event['successor'] is not None:
            row[event['successor']] += mass
        if event['failure']:
            failures[event['failure']] += mass
        totals['spend'] += mass * sum(event['spend'].values())
        for key in totals.keys() - {'spend'}:
            totals[key] += mass * event[key]
    return dict(row), dict(failures), totals


def raw_library():
    """All rooted causal NAND netlists, including physical duplicates."""
    out = [Enable((), output) for output in range(4)]
    for pair in combinations_with_replacement(range(4), 2):
        out.append(Enable((pair,), 4))
        for second in combinations_with_replacement(range(5), 2):
            if 4 in second:
                out.append(Enable((pair, second), 5))
    return tuple(out)


def independent_profile(circuit):
    return tuple(tuple(sum(raw_enable(circuit, repair, middle, flags)
                           for flags in product((0, 1), repeat=circuit.cost)
                           if sum(flags) == fault_count)
                       for fault_count in range(circuit.cost + 1))
                 for repair, middle in product((0, 1), repeat=2))


def perfect_plant(**changes):
    args = dict(healthy_error=F(0), degraded_error=F(0),
                diagnostic_error=F(0), task_sensor_error=F(0),
                degradation=F(0), restoration=F(0), procedure_failure=F(0))
    args.update(changes)
    return Model(**args)


def independent_initial(contract, circuit, prior=F(1, 2)):
    balance = 96 - 24 - circuit.cost * contract.prices.setup - contract.prices.write
    if balance < 0:
        raise ValueError('the bounded reference assumes feasible startup')
    law = defaultdict(F)
    for health, mass in ((0, 1 - prior), (1, prior)):
        for flags, weight in flag_law(3, contract.plant.diagnostic_error):
            word = tuple(health ^ bit for bit in flags)
            law[projection(health, word, balance)] += mass * weight
    return dict(law)


def independent_run(contract, policy, circuit, horizon, objective, prior=F(1, 2)):
    law = independent_initial(contract, circuit, prior)
    spent = F(24 + circuit.cost * contract.prices.setup + contract.prices.write)
    earned = spilled = failed_remaining = F(0)
    failures = defaultdict(F)
    writes, services, gates = F(1), F(0), F(0)
    tasks = cycles = F(0)
    for step in range(horizon):
        next_law = defaultdict(F)
        for state, state_mass in law.items():
            for event in oracle_events(contract, policy, circuit, state,
                                       terminal=objective == 'tasks' and step == horizon - 1):
                mass = state_mass * event['probability']
                expense = sum(event['spend'].values())
                spent += mass * expense
                earned += mass * event['earned']
                spilled += mass * (state[3] - expense + event['earned'] - event['balance'])
                writes += mass * event['writes']
                services += mass * event['services']
                gates += mass * event['gates']
                tasks += mass * event['task_success']
                cycles += mass * event['cycle_complete']
                if event['failure']:
                    failures[event['failure'].replace('resource_', 'resource:')] += mass
                    failed_remaining += mass * event['balance']
                else:
                    next_law[event['successor']] += mass
        law = dict(next_law)
    remaining = failed_remaining + sum((state[3] * mass for state, mass in law.items()), F(0))
    return dict(alive=law, survival=sum(law.values(), F(0)), spent=spent,
                earned=earned, spilled=spilled, remaining=remaining,
                failed_remaining=failed_remaining, failures=dict(failures),
                writes=writes, services=services, gates=gates,
                tasks=tasks, cycles=cycles)


class SharedBudgetTests(unittest.TestCase):
    def test_complete_physical_library_and_policy_coverage(self):
        raw = raw_library()
        representatives, statistics = library(2)
        self.assertEqual(len(raw), 64)
        self.assertEqual([sum(c.cost == size for c in raw) for size in range(3)], [4, 10, 50])
        self.assertEqual(len(policies()), 16)
        self.assertEqual(len(raw) * len(policies()), 1024)
        raw_profiles = {(c.cost, independent_profile(c)) for c in raw}
        self.assertEqual(raw_profiles, {(c.cost, independent_profile(c)) for c in representatives})
        self.assertEqual(len(raw_profiles), 21)
        self.assertEqual([s['channels'] for s in statistics], [4, 5, 12])
        for circuit in raw:
            self.assertEqual(independent_profile(circuit), circuit.profile())

    def test_independent_event_rows_at_resource_and_fault_boundaries(self):
        two_gate = Enable(((2, 3), (4, 4)), 5)
        cases = (
            (sb.Prices(), Policy(), FRESH, (0, 0, 0, 96)),
            (sb.Prices(1, 6, 0), Policy('inverse', 'service'), ELIDE, (1, 1, 1, 83)),
            (sb.Prices(1, 12, 6), Policy(), two_gate, (1, 1, 2, 84)),
            (sb.Prices(0, 24, 0), Policy('service', 'skip'), Enable((), 2), (1, 0, 1, 72)),
            (sb.Prices(1, 6, 0), Policy(), ELIDE, (0, 1, 1, 31)),
            (sb.Prices(1, 6, 0), Policy(), ELIDE, (0, 1, 2, 30)),
            (sb.Prices(1, 0, 0), Policy(), FRESH, (1, 0, 2, 29)),
            (sb.Prices(2, 12, 6), Policy('service', 'inverse'), two_gate, (1, 1, 1, 96)),
        )
        for prices, policy, circuit, state in cases:
            contract = sb.Contract(prices=prices)
            for terminal in (False, True):
                with self.subTest(prices=prices, policy=policy.name, circuit=circuit, state=state, terminal=terminal):
                    events = oracle_events(contract, policy, circuit, state, terminal)
                    expected, failures, totals = summarize(events)
                    actual = sb.compile_kernel(contract, policy, circuit, terminal).row(state)
                    self.assertEqual(sum(e['probability'] for e in events), 1)
                    self.assertEqual(actual.transitions, expected)
                    self.assertEqual({k: v for k, v in actual.failures_by_cause.items() if v},
                                     {k.replace('resource_', 'resource:'): v for k, v in failures.items()})
                    self.assertEqual(actual.spent, totals['spend'])
                    self.assertEqual(actual.writes, totals['writes'])
                    self.assertEqual(actual.services, totals['services'])
                    self.assertEqual(sum(actual.gate_events.values()), totals['gates'])
                    self.assertEqual(actual.earned, totals['earned'])
                    self.assertEqual(actual.task_successes, totals['task_success'])
                    self.assertEqual(actual.completed_cycles, totals['cycle_complete'])

    def test_tiny_independent_propagation_and_stopped_resource_conservation(self):
        contract = sb.Contract(prices=sb.Prices(1, 6, 6))
        circuit = Enable(((2, 3), (1, 4)), 5)
        policy = Policy('inverse', 'vote')
        for objective in ('tasks', 'cycles'):
            reference = independent_run(contract, policy, circuit, 3, objective, F(1, 3))
            actual = sb.run_exact(contract, policy, circuit, 3, objective, F(1, 3))
            for field in ('alive', 'survival', 'spent', 'earned', 'spilled',
                          'remaining', 'failed_remaining', 'writes', 'services'):
                self.assertEqual(getattr(actual, field), reference[field], (objective, field))
            self.assertEqual(sum(actual.gate_events.values()), reference['gates'])
            self.assertEqual(actual.task_successes, reference['tasks'])
            self.assertEqual(actual.completed_cycles, reference['cycles'])
            self.assertEqual({k: v for k, v in actual.failures_by_cause.items() if v}, reference['failures'])
            self.assertEqual(actual.survival + sum(actual.failures_by_cause.values()), 1)
            self.assertEqual(actual.spent + actual.remaining + actual.spilled, 96 + actual.earned)
            self.assertGreater(actual.failed_remaining, 0)

    def test_shared_hidden_health_is_not_an_averaged_enable_error(self):
        plant = perfect_plant(degraded_error=F(1, 2))
        shared = sb.Contract(plant=plant)
        decoupled = sb.Contract(plant=plant, enable_noise='decoupled', decoupled_error=F(1, 4))
        policy = Policy('skip', 'skip')
        good = sb.compile_kernel(shared, policy, ELIDE)
        bad = sb.compile_kernel(decoupled, policy, ELIDE)
        states = ((0, 1, 2, 96), (1, 1, 2, 96))
        shared_writes = sum(good.row(state).writes for state in states) / 2
        independent_writes = sum(bad.row(state).writes for state in states) / 2
        # The successful task selects healthier banks before enable is invoked.
        self.assertEqual(shared_writes, F(5, 8))
        self.assertEqual(independent_writes, F(9, 16))
        self.assertEqual(shared_writes - independent_writes, F(1, 16))
        self.assertNotEqual(good[states[0]], bad[states[0]])

    def test_fresh_fault_flags_are_not_reused_across_bank_invocations(self):
        plant = perfect_plant(degraded_error=F(1, 5), task_sensor_error=F(1, 7))
        state = (1, 1, 2, 96)
        selection = dict(raw_selector(plant, 1, (1, 1, 1), 'vote'))[1]
        fresh_joint = selection * raw_task_probability(plant, 1)
        reused_joint = F(0)
        for world in (0, 1):
            for noise, sensor_mass in flag_law(3, plant.task_sensor_error):
                bits = tuple(world ^ bit for bit in noise)
                for flags, flag_mass in flag_law(6, plant.degraded_error):
                    if raw_voter((1, 1, 1), flags) and raw_voter(bits, flags) == world:
                        reused_joint += sensor_mass * flag_mass / 2
        self.assertNotEqual(fresh_joint, reused_joint)
        row = sb.compile_kernel(sb.Contract(plant=plant), Policy(), RETAIN)[state]
        self.assertEqual(sum(mass for target, mass in row.items() if target[3] == 72), fresh_joint)

    def test_frozen_entry_bin_and_reservation_boundary(self):
        plant = perfect_plant()
        contract = sb.Contract(plant=plant)
        policy = Policy('service', 'skip')
        kernel = sb.compile_kernel(contract, policy, RETAIN)
        for balance, expected in ((71, 95), (72, 48), (95, 71), (96, 96)):
            row = kernel[(0, 1, 2, balance)]
            self.assertEqual(row, {(0, 1, 2, expected): F(1)})
        priced = sb.Contract(prices=sb.Prices(1, 0, 0), plant=plant)
        # At 84, the entry signal remains middle after service/task debits.
        self.assertEqual(sb.compile_kernel(priced, policy, ELIDE)[(0, 1, 2, 84)],
                         {(0, 1, 2, 53): F(1)})
        # Vote first spends six; 83 cannot reserve 78, whereas 84 can.
        voting = sb.compile_kernel(priced, Policy(), RETAIN)
        self.assertEqual(voting.row((0, 1, 2, 83)).services, 0)
        self.assertEqual(voting.row((0, 1, 2, 84)).services, 1)

    def test_no_hypothetical_write_reservation_and_final_task_fairness(self):
        contract = sb.Contract(prices=sb.Prices(0, 24, 0), plant=perfect_plant())
        policy = Policy('service', 'service')
        state = (0, 1, 2, 72)
        complete = sb.compile_kernel(contract, policy, FRESH).row(state)
        final = sb.compile_kernel(contract, policy, FRESH, True).row(state)
        retain = sb.compile_kernel(contract, policy, RETAIN).row(state)
        self.assertEqual(complete.services, 1)
        self.assertEqual(complete.task_successes, 1)
        self.assertEqual(complete.failures_by_cause['resource:write'], 1)
        self.assertEqual(complete.spent, 72)
        self.assertEqual(complete.earned, 0)
        self.assertEqual(final.transitions, {(0, 1, 2, 0): F(1)})
        self.assertEqual(final.spent, 72)
        self.assertEqual(final.writes, 0)
        self.assertEqual(final.completed_cycles, 0)
        self.assertEqual(final.earned, 0)
        self.assertEqual(retain.transitions, {(0, 1, 2, 48): F(1)})
        # The complete run also omits dead terminal acquisition for H tasks.
        priced = sb.Contract(prices=sb.Prices(1, 24, 0), plant=perfect_plant())
        for circuit in (FRESH, ELIDE):
            tasks = sb.run_exact(priced, Policy(), circuit, 1, 'tasks')
            cycles = sb.run_exact(priced, Policy(), circuit, 1, 'cycles')
            self.assertEqual(tasks.survival, 1)
            self.assertEqual(cycles.survival, 0)
            self.assertEqual(tasks.gate_events['enable'], 0)
            self.assertEqual(tasks.writes, 1)  # mandatory startup only
            self.assertEqual(tasks.spent, 78)
            self.assertEqual(tasks.remaining, 18)

    def test_failure_prefixes_pay_only_executed_stages(self):
        failure_contract = sb.Contract(prices=sb.Prices(1, 6, 0),
                                       plant=perfect_plant(procedure_failure=F(1)))
        events = sb.event_traces(failure_contract, Policy('service', 'service'), ELIDE, (1, 1, 2, 84))
        self.assertEqual(len(events), 1)
        failure = events[0]
        self.assertEqual(failure.failure, 'procedure')
        self.assertEqual(failure.spent, 48)
        self.assertEqual(failure.end_balance, 36)
        self.assertEqual(failure.gates, (0, 0, 0))
        self.assertFalse(failure.task_success)
        contract = sb.Contract(prices=sb.Prices(1, 6, 0), plant=perfect_plant())
        for balance, cause, cost in ((29, 'resource:task', 0),
                                     (30, 'resource:enable', 30),
                                     (31, 'resource:write', 31)):
            traces = sb.event_traces(contract, Policy(), ELIDE, (0, 1, 2, balance))
            self.assertEqual(len(traces), 1)
            trace = traces[0]
            self.assertEqual(trace.failure, cause)
            self.assertEqual(trace.spent, cost)
            self.assertEqual(trace.end_balance, balance - cost)
            self.assertEqual(trace.earned, 0)
        noisy = sb.Contract(prices=sb.Prices(2, 12, 0), plant=perfect_plant(task_sensor_error=F(1, 2)))
        traces = sb.event_traces(noisy, Policy(), ELIDE, (0, 1, 2, 60))
        task_failures = [t for t in traces if t.failure == 'task']
        self.assertTrue(task_failures)
        for trace in traces:
            self.assertEqual(trace.start_balance + trace.earned,
                             trace.spent + trace.end_balance + trace.spilled)
            self.assertGreaterEqual(trace.end_balance, 0)
            if trace.failure:
                self.assertEqual(trace.earned, 0)
        for trace in task_failures:
            self.assertEqual(trace.spent, 36)
            self.assertEqual(trace.gates, (0, 6, 0))
            self.assertEqual(trace.writes, 0)

    def test_setup_and_startup_share_the_endowment_for_complete_price_grid(self):
        self.assertEqual(sb.PRICE_GRID, tuple(product((0, 1, 2), (0, 6, 12, 24), (0, 6))))
        for prices in sb.PRICE_GRID:
            contract = sb.Contract(prices=sb.Prices(*prices))
            for circuit in library(2)[0]:
                initial = sb.initialize(contract, circuit, F(1, 3))
                self.assertEqual(initial.measure, independent_initial(contract, circuit, F(1, 3)))
                self.assertEqual(initial.writes, 1)
                self.assertEqual(sum(initial.spend_by_stage.values()),
                                 24 + circuit.cost * prices[2] + prices[1])
                self.assertFalse(initial.failures_by_cause)
        two_gate = Enable(((2, 3), (4, 4)), 5)
        failed = sb.initialize(sb.Contract(prices=sb.Prices(setup=40)), two_gate)
        self.assertEqual(failed.measure, {})
        self.assertEqual(failed.spend_by_stage, {'commissioning': F(24), 'setup': F(0), 'initial_write': F(0)})
        self.assertEqual(failed.failed_remaining, 72)
        self.assertEqual(failed.failures_by_cause, {'resource:setup': F(1)})

    def test_zero_price_fresh_survival_matches_both_inherited_models(self):
        contract = sb.Contract()
        for policy in policies():
            old_curve, _ = forward(contract.plant, policy, 3)
            old_fresh = inherited_evaluate(FRESH, horizon=3, p=contract.plant, policy=policy)
            for objective in ('tasks', 'cycles'):
                current = sb.run_exact(contract, policy, FRESH, 3, objective)
                self.assertEqual(current.curve, old_curve, (policy.name, objective))
                self.assertEqual(current.survival, old_fresh['survival'])


if __name__ == '__main__':
    unittest.main()
