"""Independent channel checks for the fixed-prior all-report intervention."""
from collections import defaultdict
from dataclasses import replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import unittest

from cdka import diagnostic_ablation as da
from cdka import optional_startup as os
from cdka import shared_budget as sb
from cdka.recurrent_maintenance import Model, Policy, policies, select_probability
from cdka.selective_acquisition import ELIDE, FRESH, RETAIN, library

try:
    from .test_shared_budget import oracle_events, flag_law
except ImportError:
    from test_shared_budget import oracle_events, flag_law


def raw_marginal(plant, prior):
    result = defaultdict(F)
    for source, mass in ((0, 1 - prior), (1, prior)):
        for flags, weight in flag_law(3, plant.diagnostic_error):
            bits = tuple(source ^ bit for bit in flags)
            result[(bits[0], bits[1] + bits[2])] += mass * weight
    return {state: mass for state, mass in result.items() if mass}


def projected(law):
    result = defaultdict(F)
    for (health, first, tail, balance), mass in law.items():
        result[(health, balance)] += mass
    return dict(result)


def independent_null_row(contract, policy, enable, state, prior, terminal=False):
    """Change only successful write outcomes of the raw physical event oracle.

    The reused oracle directly enumerates independent NAND/sensor flags and
    does not call shared_budget's event constructor or probability shortcuts.
    """
    result = defaultdict(F)
    marginal = raw_marginal(contract.plant, prior)
    for event in oracle_events(contract, policy, enable, state, terminal):
        target = event['successor']
        if target is None:
            continue
        mass = event['probability']
        if event['writes']:
            health, _, _, balance = target
            for (first, tail), report_mass in marginal.items():
                result[(health, first, tail, balance)] += mass * report_mass
        else:
            result[target] += mass
    return {state: mass for state, mass in result.items() if mass}


class DiagnosticAblationTests(unittest.TestCase):
    def test_whole_word_marginal_preserves_cell_dependence(self):
        plant = Model()
        for prior in (F(0), F(1, 3), F(1, 2), F(1)):
            self.assertEqual(dict(da.report_marginal(plant, prior)),
                             raw_marginal(plant, prior))
        marginal = dict(da.report_marginal(plant))
        self.assertEqual(marginal[(0, 0)], F(247, 800))
        self.assertNotEqual(marginal[(0, 0)], F(1, 8))
        self.assertEqual(sum(q for (a, _), q in marginal.items() if a), F(1, 2))

    def test_raw_physical_oracle_with_independent_report_draws(self):
        checks = (
            (sb.Prices(1, 6, 0), Policy(), ELIDE, (1, 1, 2, 90)),
            (sb.Prices(1, 6, 0), Policy('inverse', 'vote'), FRESH, (0, 0, 1, 84)),
            (sb.Prices(2, 12, 6), Policy('vote', 'inverse'),
             library(2)[0][-1], (1, 0, 1, 96)),
            (sb.Prices(0, 6, 0), Policy('service', 'skip'),
             library(2)[0][2], (1, 1, 0, 72)),
        )
        for prices, policy, enable, state in checks:
            contract = sb.Contract(prices)
            for prior in (F(1, 2), F(1, 3)):
                for terminal in (False, True):
                    kernel = da.compile_kernel(contract, policy, enable, terminal, prior)
                    self.assertEqual(kernel.transition(state), independent_null_row(
                        contract, policy, enable, state, prior, terminal))
                    targets, metrics = kernel.integer_row(state)
                    self.assertEqual({s: F(q, kernel.denominator) for s, q in targets},
                                     kernel.transition(state))

    def test_each_same_state_reward_and_health_resource_mass_are_unchanged(self):
        contract = sb.Contract(sb.Prices(1, 6, 6))
        for enable in library(2)[0]:
            for state in ((0, 0, 0, 72), (1, 1, 2, 84), (1, 0, 1, 96)):
                original = sb.compile_kernel(contract, Policy(), enable).row(state)
                changed = da.compile_kernel(contract, Policy(), enable).row(state)
                self.assertEqual(replace(changed, transitions=original.transitions), original)
                self.assertEqual(projected(changed.transitions), projected(original.transitions))

    def test_fresh_successor_report_is_independent_of_successor_health(self):
        contract = sb.Contract(sb.Prices(0, 6, 0))
        marginal = dict(da.report_marginal(contract.plant))
        state = (1, 1, 2, 90)
        kernel = da.compile_kernel(contract, Policy(), FRESH)
        row = kernel.transition(state)
        health_resource = projected(row)
        for (health, balance), mass in health_resource.items():
            for (first, tail), probability in marginal.items():
                self.assertEqual(row.get((health, first, tail, balance), F(0)),
                                 mass * probability)
        self.assertNotEqual(row, sb.compile_kernel(contract, Policy(), FRESH).transition(state))

    def test_retained_and_terminal_kernels_are_identical(self):
        contract = sb.Contract(sb.Prices(1, 6, 0))
        for state in ((0, 0, 1, 66), (1, 1, 2, 90), (0, 1, 0, 96)):
            self.assertEqual(da.compile_kernel(contract, Policy(), RETAIN).row(state),
                             sb.compile_kernel(contract, Policy(), RETAIN).row(state))
            for enable in library(2)[0]:
                self.assertEqual(da.compile_kernel(contract, Policy(), enable, True).row(state),
                                 sb.compile_kernel(contract, Policy(), enable, True).row(state))

    def test_blind_program_rewards_and_projected_trajectory_are_unchanged(self):
        contract = sb.Contract(sb.Prices(1, 6, 6))
        for at3, at4 in product(('skip', 'service'), repeat=2):
            policy = Policy(at3, at4)
            for enable in (FRESH, RETAIN, ELIDE):
                for objective in ('tasks', 'cycles'):
                    original = sb.run_exact(contract, policy, enable, 3, objective)
                    changed = da.run_exact(contract, policy, enable, 3, objective)
                    self.assertEqual(replace(changed, alive=original.alive), original)
                    self.assertEqual(projected(changed.alive), projected(original.alive))

    def test_half_error_channel_is_already_its_own_ablation(self):
        contract = sb.Contract(sb.Prices(0, 6, 0), plant=Model(diagnostic_error=F(1, 2)))
        for policy in policies():
            for enable in (FRESH, RETAIN, ELIDE):
                self.assertEqual(da.run_exact(contract, policy, enable, 2),
                                 sb.run_exact(contract, policy, enable, 2, 'tasks'))

    def test_startup_failures_and_horizon_zero_keep_the_paid_contract(self):
        for prices in (sb.Prices(1, 6, 6), sb.Prices(1, 80, 0), sb.Prices(1, 6, 90)):
            contract = sb.Contract(prices)
            for horizon in (0, 3):
                result = da.run_exact(contract, Policy(), ELIDE, horizon)
                if horizon == 0 or prices.write == 80 or prices.setup == 90:
                    initial_only = os.run_exact(contract, Policy(), ELIDE, horizon,
                                                'tasks', preparation='independent')
                    self.assertEqual(result, initial_only)
                self.assertEqual(result.spent + result.remaining + result.spilled,
                                 contract.endowment + result.earned)

    def test_report_ablation_does_not_erase_health_dependent_computation(self):
        plant = Model()
        requests = []
        for health in (0, 1):
            requests.append(sum((mass * select_probability(
                plant, health, (first, int(tail >= 1), int(tail == 2)), 'vote')
                for (first, tail), mass in da.report_marginal(plant)), F(0)))
        self.assertEqual(requests, [F(25102153867357447, 50000000000000000),
                                    F(262193521, 488281250)])
        self.assertNotEqual(*requests)

    def test_initial_and_all_report_response_identities_include_incurred_cost(self):
        contract = sb.Contract(sb.Prices(0, 6, 0))
        policy, enable, horizon = Policy(), ELIDE, 3
        informed = sb.compile_kernel(contract, policy, enable)
        null = da.compile_kernel(contract, policy, enable)
        terminal = sb.compile_kernel(contract, policy, enable, True)
        alpha = os.initialize(contract, policy, enable).measure
        beta = os.initialize(contract, policy, enable, preparation='independent').measure

        @lru_cache(None)
        def response(state, steps, cost):
            if steps == 0:
                row = terminal.row(state)
                return row.spent if cost else row.survival
            row = informed.row(state)
            return ((row.spent if cost else F(0)) +
                    sum((mass * response(target, steps - 1, cost)
                         for target, mass in row.transitions.items()), F(0)))

        physical = sb.run_exact(contract, policy, enable, horizon, 'tasks')
        initial_only = os.run_exact(contract, policy, enable, horizon, 'tasks',
                                    preparation='independent')
        all_null = da.run_exact(contract, policy, enable, horizon)
        for cost, metric in ((False, 'survival'), (True, 'spent')):
            startup = sum(((alpha.get(state, F(0)) - beta.get(state, F(0))) *
                           response(state, horizon - 1, cost)
                           for state in alpha.keys() | beta.keys()), F(0))
            self.assertEqual(startup, getattr(physical, metric) - getattr(initial_only, metric))
            correction, prefix = F(0), dict(beta)
            for j in range(horizon - 1):
                next_prefix = defaultdict(F)
                for state, mass in prefix.items():
                    original = informed.transition(state)
                    changed = null.transition(state)
                    correction += mass * sum((
                        (original.get(target, F(0)) - changed.get(target, F(0))) *
                        response(target, horizon - 2 - j, cost)
                        for target in original.keys() | changed.keys()), F(0))
                    for target, probability in changed.items():
                        next_prefix[target] += mass * probability
                prefix = dict(next_prefix)
            self.assertEqual(startup + correction,
                             getattr(physical, metric) - getattr(all_null, metric))


if __name__ == '__main__':
    unittest.main()
