"""Independent preparation laws and paid-prefix checks for optional startup.

The trajectory oracle enumerates raw sensor and NAND events from the prior
independent SB test oracle.  It does not call either production propagator,
row compiler, event enumerator or optimized diagnostic probability helper.
"""
from collections import defaultdict
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest

from cdka import optional_startup as os
from cdka import shared_budget as sb
from cdka.recurrent_maintenance import Policy, policies
from cdka.selective_acquisition import Enable, ELIDE, FRESH, RETAIN, library
from test_shared_budget import flag_law, oracle_events, projection


BLIND = tuple(Policy(a, b) for a, b in product(('skip', 'service'), repeat=2))


def raw_initial(contract, circuit, prior, preparation, dummy=(0, 0, 0)):
    """Enumerate the actual health and an independent report-source health."""
    balance = 96
    spend = {'commissioning': F(0), 'setup': F(0), 'initial_write': F(0)}
    stages = [('commissioning', 24), ('setup', circuit.cost * contract.prices.setup)]
    if preparation != 'omit':
        stages.append(('initial_write', contract.prices.write))
    for name, price in stages:
        if balance < price:
            return dict(law={}, spend=spend, failures={'resource:' + name: F(1)},
                        writes=F(0), failed_remaining=F(balance))
        balance -= price
        spend[name] = F(price)
    law = defaultdict(F)
    health_law = ((0, 1 - prior), (1, prior))
    for health, health_mass in health_law:
        if preparation == 'omit':
            law[projection(health, dummy, balance)] += health_mass
            continue
        source_law = health_law if preparation == 'independent' else ((health, F(1)),)
        for source, source_mass in source_law:
            for errors, noise_mass in flag_law(3, contract.plant.diagnostic_error):
                word = tuple(source ^ error for error in errors)
                law[projection(health, word, balance)] += health_mass * source_mass * noise_mass
    return dict(law={s: q for s, q in law.items() if q}, spend=spend,
                failures={}, writes=F(preparation != 'omit'), failed_remaining=F(0))


def raw_run(contract, policy, circuit, horizon, objective, prior, preparation,
            dummy=(0, 0, 0)):
    initial = raw_initial(contract, circuit, prior, preparation, dummy)
    law = initial['law']
    spent = sum(initial['spend'].values(), F(0))
    failures = defaultdict(F, initial['failures'])
    failed_remaining = initial['failed_remaining']
    writes = initial['writes']
    services = gates = earned = spilled = tasks = cycles = F(0)
    curve = [sum(law.values(), F(0))]
    for step in range(horizon):
        following = defaultdict(F)
        for state, state_mass in law.items():
            events = oracle_events(contract, policy, circuit, state,
                                   terminal=objective == 'tasks' and step == horizon - 1)
            for event in events:
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
                    following[event['successor']] += mass
        law = dict(following)
        curve.append(sum(law.values(), F(0)))
    remaining = failed_remaining + sum((state[3] * mass for state, mass in law.items()), F(0))
    return dict(alive=law, survival=sum(law.values(), F(0)), spent=spent,
                failures={k: v for k, v in failures.items() if v},
                failed_remaining=failed_remaining, remaining=remaining,
                earned=earned, spilled=spilled, writes=writes, services=services,
                gates=gates, task_successes=tasks, completed_cycles=cycles,
                curve=tuple(curve))


def project(law):
    out = defaultdict(F)
    for (health, _, _, balance), mass in law.items():
        out[(health, balance)] += mass
    return dict(out)


class OptionalStartupTests(unittest.TestCase):
    def test_preparation_laws_against_raw_cell_oracle(self):
        two_gate = Enable(((2, 3), (4, 4)), 5)
        for prices in (sb.Prices(0, 6, 0), sb.Prices(1, 24, 6), sb.Prices(2, 12, 6)):
            contract = sb.Contract(prices)
            for prior in (F(0), F(1, 3), F(1, 2), F(1)):
                for preparation in os.PREPARATIONS:
                    actual = os.initialize(contract, BLIND[-1], two_gate, prior, preparation)
                    expected = raw_initial(contract, two_gate, prior, preparation)
                    self.assertEqual(actual.measure, expected['law'])
                    self.assertEqual(actual.spend_by_stage, expected['spend'])
                    self.assertEqual(actual.writes, expected['writes'])
                    self.assertEqual(actual.failed_remaining, expected['failed_remaining'])
                    self.assertEqual(actual.failures_by_cause, expected['failures'])

    def test_fresh_preparation_preserves_existing_complete_run(self):
        cases = (
            (sb.Prices(), Policy(), FRESH),
            (sb.Prices(1, 6, 6), Policy('inverse', 'vote'), ELIDE),
            (sb.Prices(2, 24, 6), BLIND[-1], RETAIN),
        )
        for prices, policy, circuit in cases:
            contract = sb.Contract(prices)
            for horizon in (0, 1, 3):
                for objective in ('tasks', 'cycles'):
                    self.assertEqual(
                        os.run_exact(contract, policy, circuit, horizon, objective, F(1, 3)),
                        sb.run_exact(contract, policy, circuit, horizon, objective, F(1, 3)))

    def test_omission_requires_complete_blind_table_not_unreachable_name(self):
        for policy in policies():
            self.assertEqual(os.blind(policy), policy in BLIND)
            if policy in BLIND:
                self.assertEqual(os.initialize(sb.Contract(), policy, RETAIN,
                                               preparation='omit').writes, 0)
            else:
                with self.assertRaises(ValueError):
                    os.run_exact(sb.Contract(), policy, RETAIN, 0,
                                 preparation='omit')
        for value in ('none', '', None):
            with self.assertRaises(ValueError):
                os.initialize(sb.Contract(), BLIND[0], RETAIN, preparation=value)
        for horizon in (-1, 1.0, True):
            with self.assertRaises(ValueError):
                os.run_exact(horizon=horizon)
        with self.assertRaises(ValueError):
            os.run_exact(objective='successes')

    def test_matched_price_control_preserves_full_report_marginal(self):
        contract = sb.Contract(sb.Prices(1, 6, 0))
        prior = F(1, 3)
        fresh = os.initialize(contract, Policy(), RETAIN, prior, 'fresh')
        independent = os.initialize(contract, Policy(), RETAIN, prior, 'independent')
        report = defaultdict(F)
        for (_, first, tail, _), mass in fresh.measure.items():
            report[(first, tail)] += mass
        self.assertEqual(project(fresh.measure), project(independent.measure))
        for (health, first, tail, _), mass in independent.measure.items():
            self.assertEqual(mass, (prior if health else 1 - prior) * report[(first, tail)])
        # Shared report-source health leaves cells correlated, even though the
        # whole report is independent of the actual bank health after ablation.
        p_first = sum(q for (first, _), q in report.items() if first)
        p_tail = sum(q * F(tail, 2) for (_, tail), q in report.items())
        p_both = sum(q * F(first * tail, 2) for (first, tail), q in report.items())
        self.assertNotEqual(p_both, p_first * p_tail)
        self.assertEqual(fresh.spend_by_stage, independent.spend_by_stage)
        self.assertEqual(fresh.writes, independent.writes)

    def test_short_raw_trajectories_preserve_stopped_prefixes_and_endpoints(self):
        two_gate = Enable(((2, 3), (1, 4)), 5)
        cases = (
            (sb.Prices(1, 6, 6), BLIND[-1], two_gate, 'omit'),
            (sb.Prices(0, 12, 0), BLIND[-1], FRESH, 'omit'),
            (sb.Prices(1, 6, 6), Policy('vote', 'inverse'), ELIDE, 'independent'),
        )
        for prices, policy, circuit, preparation in cases:
            contract = sb.Contract(prices)
            for objective in ('tasks', 'cycles'):
                with self.subTest(prices=prices, objective=objective, preparation=preparation):
                    expected = raw_run(contract, policy, circuit, 3, objective, F(1, 3), preparation)
                    actual = os.run_exact(contract, policy, circuit, 3, objective, F(1, 3), preparation)
                    for field in ('alive', 'survival', 'spent', 'failed_remaining',
                                  'remaining', 'earned', 'spilled', 'writes',
                                  'services', 'task_successes', 'completed_cycles', 'curve'):
                        self.assertEqual(getattr(actual, field), expected[field], field)
                    self.assertEqual({k: v for k, v in actual.failures_by_cause.items() if v},
                                     expected['failures'])
                    self.assertEqual(sum(actual.gate_events.values()), expected['gates'])
                    self.assertEqual(actual.gate_events['selection'] == 0, os.blind(policy))
                    self.assertEqual(actual.spent + actual.remaining + actual.spilled,
                                     96 + actual.earned)

    def test_uninitialized_record_has_no_projected_effect_in_blind_family(self):
        contract = sb.Contract(sb.Prices(1, 6, 0))
        # Every enable channel is covered.  Records may affect the evaluator's
        # retained labels, but cannot affect maintenance, rewards or (z,b).
        for policy in BLIND:
            for circuit in library(2)[0]:
                for terminal in (False, True):
                    kernel = sb.compile_kernel(contract, policy, circuit, terminal)
                    for health, balance in product((0, 1), (30, 72, 84, 96)):
                        reference = kernel.row((health, 0, 0, balance))
                        for first, tail in product((0, 1), range(3)):
                            row = kernel.row((health, first, tail, balance))
                            self.assertEqual(project(row.transitions), project(reference.transitions))
                            self.assertEqual(replace(row, transitions={}),
                                             replace(reference, transitions={}))
                            self.assertEqual(row.gate_events['selection'], 0)

    def test_arbitrary_unread_initial_cells_give_same_physical_trajectory(self):
        contract = sb.Contract(sb.Prices(1, 6, 6))
        policy = BLIND[-1]
        for circuit in (RETAIN, ELIDE):
            actual = os.run_exact(contract, policy, circuit, 3, 'tasks', preparation='omit')
            for dummy in product((0, 1), repeat=3):
                expected = raw_run(contract, policy, circuit, 3, 'tasks', F(1, 2), 'omit', dummy)
                self.assertEqual(project(actual.alive), project(expected['alive']))
                for field in ('survival', 'spent', 'earned', 'spilled', 'remaining',
                              'failed_remaining', 'writes', 'services'):
                    self.assertEqual(getattr(actual, field), expected[field])

    def test_failed_preparation_and_zero_horizon_keep_actual_charges(self):
        two_gate = Enable(((2, 3), (4, 4)), 5)
        for preparation in os.PREPARATIONS:
            actual = os.run_exact(sb.Contract(sb.Prices(1, 6, 40)), BLIND[0],
                                  two_gate, 0, 'tasks', preparation=preparation)
            self.assertEqual(actual.survival, 0)
            self.assertEqual(actual.spent, 24)
            self.assertEqual(actual.remaining, 72)
            self.assertEqual(actual.writes, 0)
            self.assertEqual(actual.failures_by_cause['resource:setup'], 1)
        for preparation, survival, writes, spent, remaining in (
                ('fresh', 0, 0, 24, 72), ('independent', 0, 0, 24, 72),
                ('omit', 1, 0, 24, 72)):
            actual = os.run_exact(sb.Contract(sb.Prices(0, 100, 0)), BLIND[-1],
                                  RETAIN, 0, 'cycles', preparation=preparation)
            self.assertEqual((actual.survival, actual.writes, actual.spent, actual.remaining),
                             (survival, writes, spent, remaining))

    def test_initial_content_ablation_is_exactly_invisible_to_blind_rewards(self):
        for prices in (sb.Prices(0, 6, 0), sb.Prices(1, 24, 6)):
            contract = sb.Contract(prices)
            for circuit in (RETAIN, FRESH, ELIDE):
                for objective in ('tasks', 'cycles'):
                    fresh = os.run_exact(contract, BLIND[-1], circuit, 3, objective)
                    independent = os.run_exact(contract, BLIND[-1], circuit, 3, objective,
                                               preparation='independent')
                    self.assertEqual(project(fresh.alive), project(independent.alive))
                    self.assertEqual(replace(fresh, alive={}), replace(independent, alive={}))

    def test_more_startup_balance_need_not_help_a_fixed_coarse_bin_policy(self):
        # On the predeclared grid and fair prior, omission raises balance66
        # to72.  Service then consumes48 and work24; direct e=r requests a
        # six-quantum write before any harvest, which cannot be funded.
        contract = sb.Contract(sb.Prices(0, 6, 0))
        direct_service = Enable((), 2)
        fresh = os.run_exact(contract, BLIND[-1], direct_service, 8, 'tasks')
        omitted = os.run_exact(contract, BLIND[-1], direct_service, 8, 'tasks',
                               preparation='omit')
        independent = raw_run(contract, BLIND[-1], direct_service, 8, 'tasks',
                              F(1, 2), 'fresh')
        self.assertEqual(fresh.survival, independent['survival'])
        self.assertEqual(fresh.spent, independent['spent'])
        self.assertGreater(fresh.survival, F(88, 100))
        self.assertLess(fresh.survival, F(89, 100))
        self.assertEqual(omitted.services, 1)
        self.assertEqual(omitted.survival, 0)
        self.assertEqual(omitted.spent, F(2397, 25))
        self.assertEqual(omitted.earned, 0)
        self.assertEqual(omitted.writes, 0)
        self.assertEqual(omitted.gate_events['selection'], 0)
        self.assertEqual(omitted.failures_by_cause['resource:write'], omitted.task_successes)


if __name__ == '__main__':
    unittest.main()
