"""Exact robust bounds, incompatible centers, and certificate corruption."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations
import json
import unittest
from unittest.mock import patch

from cdka.reachable_interfaces import (
    compile_reachable_interface, verify_reachable_interface, table_binding,
    contrast_value, admissible_plans,
)


class ReachableInterfaceTests(unittest.TestCase):
    def compile(self, table, **kwargs):
        result = compile_reachable_interface(table, **kwargs)
        self.assertTrue(verify_reachable_interface(result, table, **kwargs))
        return result

    def test_singleton_and_two_law_midpoint(self):
        c = self.compile([[F(2, 3)]])
        self.assertEqual(c['prediction']['free_radius'], '0')
        self.assertEqual(c['decision']['minimax_regret'], '0')
        self.assertEqual(c['decision']['common_optimal_plans'], [0])
        c = self.compile([[0, 1], [1, 0]])
        self.assertEqual(c['prediction']['free_center'], ['1/2', '1/2'])
        self.assertEqual(c['prediction']['uniform_law_center'], ['1/2', '1/2'])
        self.assertEqual(c['prediction']['free_radius'], '1/2')
        self.assertEqual(c['decision']['minimax_regret'], '1')

    def test_three_coordinate_midpoint_need_not_be_a_law(self):
        table = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        c = self.compile(table)
        midpoint = tuple(map(F, c['prediction']['free_center']))
        physical = tuple(map(F, c['prediction']['uniform_law_center']))
        self.assertEqual(sum(midpoint), F(3, 2))
        self.assertEqual(sum(physical), 1)
        self.assertTrue(all(sum(row) == 1 for row in table))
        self.assertEqual(c['prediction']['free_radius'], '1/2')
        self.assertEqual(c['prediction']['uniform_law_radius'], '2/3')

    def test_pairwise_plan_compatibility_does_not_imply_a_common_triple(self):
        table = ((1, 1, 0), (0, 1, 1), (1, 0, 1))
        for pair in combinations(table, 2):
            c = self.compile(pair)
            self.assertEqual(len(c['decision']['common_optimal_plans']), 1)
        c = self.compile(table)
        self.assertEqual(c['decision']['common_optimal_plans'], [])
        self.assertEqual(c['decision']['minimax_regret'], '1')

    def test_same_first_action_does_not_make_complete_plans_compatible(self):
        table = ((F(9, 10), F(1, 10)), (F(1, 10), F(9, 10)))
        plans = ('D,R', 'D,M')
        self.assertEqual(plans[0].split(',')[0], plans[1].split(',')[0])
        c = self.compile(table, plan_labels=plans)
        self.assertEqual(c['decision']['common_optimal_plans'], [])
        self.assertEqual(c['decision']['minimax_regret'], '4/5')

    def test_regret_preserves_same_history_correlation(self):
        table = ((F(1, 10), 0), (F(9, 10), F(8, 10)))
        c = self.compile(table, plan_labels=('pi', 'alternative'))
        self.assertEqual(c['decision']['chosen_plan'], 0)
        self.assertEqual(c['decision']['minimax_regret'], '0')
        self.assertEqual(c['decision']['plan_regrets'], ['0', '1/10'])
        lower = tuple(map(F, c['prediction']['lower']))
        upper = tuple(map(F, c['prediction']['upper']))
        independent_box_comparison = upper[1]-lower[0]
        self.assertEqual(independent_box_comparison, F(7, 10))

    def test_minimax_plan_can_be_no_row_optimum_and_differs_from_maximin(self):
        table = ((F(9, 10), F(6, 10), 1), (F(5, 10), F(6, 10), F(1, 10)))
        c = self.compile(table)
        decision = c['decision']
        self.assertEqual(decision['preparation_optimal_plans'], [2, 1])
        self.assertEqual(decision['chosen_plan'], 0)
        self.assertEqual(decision['minimax_regret'], '1/10')
        self.assertEqual(decision['maximin_plan'], 1)
        self.assertEqual(decision['maximin_value'], '3/5')
        self.assertEqual(admissible_plans(c, maximum_regret=F(1, 5),
                                         minimum_value=F(11, 20)), [])
        self.assertEqual(admissible_plans(c, maximum_regret=F(2, 5),
                                         minimum_value=F(11, 20)), [1])
        self.assertEqual(admissible_plans(c, maximum_regret=F(1, 10),
                                         minimum_value=F(1, 2)), [0])

    def test_sensor_attenuation_preserves_order_but_can_destroy_absolute_value(self):
        original = ((F(9, 10), F(6, 10), 1), (F(5, 10), F(6, 10), F(1, 10)))
        baseline = self.compile(original)
        for eta in (F(1, 10), F(1, 4), F(1, 2)):
            scale = 1-2*eta
            table = tuple(tuple(F(1, 2)+scale*(x-F(1, 2)) for x in row)
                          for row in original)
            c = self.compile(table)
            self.assertEqual(F(c['prediction']['free_radius']),
                             scale*F(baseline['prediction']['free_radius']))
            self.assertEqual(tuple(map(F, c['decision']['plan_regrets'])),
                             tuple(scale*F(x) for x in baseline['decision']['plan_regrets']))
            if eta < F(1, 2):
                self.assertEqual(c['decision']['chosen_plan'], baseline['decision']['chosen_plan'])
                self.assertEqual(c['decision']['maximin_plan'], baseline['decision']['maximin_plan'])
            else:
                self.assertEqual(c['decision']['minimax_regret'], '0')
                self.assertEqual(c['decision']['maximin_value'], '1/2')
                self.assertEqual(admissible_plans(c, minimum_value=F(3, 5)), [])

    def test_all_rational_mixtures_obey_bounds_and_vertices_attain_them(self):
        table = ((F(3, 4), F(1, 2), F(1, 4)),
                 (F(1, 4), F(3, 4), F(1, 2)),
                 (F(1, 2), F(1, 4), F(3, 4)))
        c = self.compile(table)
        center = tuple(map(F, c['prediction']['free_center']))
        certified_radius = F(c['prediction']['free_radius'])
        certified_regrets = tuple(map(F, c['decision']['plan_regrets']))
        largest_errors = F(0)
        largest_regrets = [F(0)]*3
        for a in range(6):
            for b in range(6-a):
                weights = (F(a, 5), F(b, 5), F(5-a-b, 5))
                response = tuple(sum(weights[i]*table[i][j] for i in range(3))
                                 for j in range(3))
                error = max(abs(x-y) for x, y in zip(response, center))
                self.assertLessEqual(error, certified_radius)
                largest_errors = max(largest_errors, error)
                for j in range(3):
                    actual_regret = max(response)-response[j]
                    self.assertLessEqual(actual_regret, certified_regrets[j])
                    largest_regrets[j] = max(largest_regrets[j], actual_regret)
        self.assertEqual(largest_errors, certified_radius)
        self.assertEqual(tuple(largest_regrets), certified_regrets)

    def test_portable_checker_does_not_invoke_optimizer(self):
        table = ((F(1, 3), F(2, 3)), (F(3, 4), F(1, 4)))
        c = json.loads(json.dumps(self.compile(table)))
        with patch('cdka.reachable_interfaces.compile_reachable_interface',
                   side_effect=AssertionError('optimizer forbidden')), \
             patch('cdka.reachable_interfaces._argmax',
                   side_effect=AssertionError('max search forbidden')), \
             patch('cdka.reachable_interfaces._argmin',
                   side_effect=AssertionError('min search forbidden')):
            self.assertTrue(verify_reachable_interface(c, table))

    def test_contract_values_and_ordered_identities_are_bound(self):
        table = ((F(2, 3), F(1, 3)), (F(1, 3), F(2, 3)))
        kwargs = dict(preparation_labels=('DD', 'RR'), plan_labels=('M', 'RM'),
                      contract={'history_readable': False, 'paid_acquisition': 1})
        c = self.compile(table, **kwargs)
        self.assertEqual(c['contract_sha256'], table_binding(table, **kwargs))
        changed = deepcopy(kwargs); changed['contract']['history_readable'] = True
        with self.assertRaises(ValueError):
            verify_reachable_interface(c, table, **changed)
        changed = deepcopy(kwargs); changed['plan_labels'] = ('RM', 'M')
        with self.assertRaises(ValueError):
            verify_reachable_interface(c, table, **changed)
        with self.assertRaises(ValueError):
            verify_reachable_interface(c, (table[1], table[0]), **kwargs)

    def test_envelopes_centers_and_attaining_witnesses_reject_tampering(self):
        table = ((0, F(1, 3)), (F(2, 3), 1), (F(1, 3), F(2, 3)))
        original = self.compile(table)
        corruptions = []
        c = deepcopy(original); c['prediction']['lower'][0] = '-1'; corruptions.append(c)
        c = deepcopy(original); c['prediction']['upper_witnesses'][0] = 0; corruptions.append(c)
        c = deepcopy(original); c['prediction']['free_center'][0] = '0'; corruptions.append(c)
        c = deepcopy(original); c['prediction']['free_radius'] = '1/6'; corruptions.append(c)
        c = deepcopy(original); c['prediction']['uniform_law_center'][0] = '0'; corruptions.append(c)
        c = deepcopy(original); c['prediction']['uniform_law_radius'] = '1'; corruptions.append(c)
        c = deepcopy(original); c['prediction']['uniform_law_radius_witness']['plan'] = 9; corruptions.append(c)
        for c in corruptions:
            with self.assertRaises(ValueError):
                verify_reachable_interface(c, table)

    def test_regret_lower_witnesses_and_common_plan_set_reject_tampering(self):
        table = ((F(9, 10), F(8, 10), 0), (F(9, 10), 0, F(8, 10)))
        original = self.compile(table)
        self.assertEqual(original['decision']['common_optimal_plans'], [0])
        corruptions = []
        c = deepcopy(original); c['decision']['preparation_optima'][0] = '1'; corruptions.append(c)
        c = deepcopy(original); c['decision']['preparation_optimal_plans'][0] = 1; corruptions.append(c)
        c = deepcopy(original); c['decision']['plan_regrets'][1] = '1'; corruptions.append(c)
        c = deepcopy(original); c['decision']['plan_regret_witnesses'][1]['preparation'] = 0; corruptions.append(c)
        c = deepcopy(original); c['decision']['plan_regret_witnesses'][1]['comparator_plan'] = 1; corruptions.append(c)
        c = deepcopy(original); c['decision']['chosen_plan'] = 1; corruptions.append(c)
        c = deepcopy(original); c['decision']['minimax_regret'] = '1/10'; corruptions.append(c)
        c = deepcopy(original); c['decision']['maximin_value'] = '1'; corruptions.append(c)
        c = deepcopy(original); c['decision']['maximin_plan'] = 1; corruptions.append(c)
        c = deepcopy(original); c['decision']['common_optimal_plans'] = []; corruptions.append(c)
        for c in corruptions:
            with self.assertRaises(ValueError):
                verify_reachable_interface(c, table)

    def test_invalid_tables_and_malformed_certificates_are_rejected(self):
        for table in ([], [[]], [[0], [0, 1]], [[0.5]], [[True]]):
            with self.assertRaises(ValueError):
                compile_reachable_interface(table)
        with self.assertRaises(ValueError):
            compile_reachable_interface([[0, 1]], plan_labels=('same', 'same'))
        c = self.compile([[0]])
        del c['decision']['plan_regret_witnesses']
        with self.assertRaises(ValueError):
            verify_reachable_interface(c, [[0]])

    def test_constant_hidden_bit_contrast_matches_explicit_joint_lift(self):
        zero = (F(1, 10), F(1, 5))
        one = (F(3, 10), F(2, 5))
        kernel = ((F(4, 5), F(1, 5)), (F(1, 3), F(2, 3)))
        g = (F(1, 4), F(3, 4))
        response = tuple(sum(p*x for p, x in zip(row, g)) for row in kernel)
        end_zero = tuple(sum(zero[i]*kernel[i][j] for i in range(2)) for j in range(2))
        end_one = tuple(sum(one[i]*kernel[i][j] for i in range(2)) for j in range(2))
        lifted = sum(end_zero[j]*(1-g[j])+end_one[j]*g[j] for j in range(2))
        self.assertEqual(contrast_value(zero, one, response), lifted)

    def test_substochastic_contrast_keeps_surviving_zero_mass(self):
        zero, one = (F(1, 4), F(1, 4)), (F(1, 4), F(1, 4))
        response, mass = (F(1, 4), F(1, 2)), (F(1, 2), F(3, 4))
        actual = contrast_value(zero, one, response, mass_response=mass)
        direct = sum(z*(t-x)+o*x for z, o, x, t in zip(zero, one, response, mass))
        self.assertEqual(actual, direct)
        self.assertEqual(actual, F(5, 16))
        self.assertNotEqual(actual, contrast_value(zero, one, response))
        self.assertEqual(contrast_value(zero, one, (0, 0), mass_response=(0, 0)), 0)

    def test_contrast_checks_probability_and_mass_constraints(self):
        for zero, one, response, mass in (
            ((-1,), (1,), (F(1, 2),), None),
            ((F(1, 2),), (F(1, 2),), (2,), None),
            ((F(1, 2),), (F(1, 2),), (F(3, 4),), (F(1, 2),)),
            ((F(1, 2),), (F(1, 2), F(0)), (F(1, 2),), None),
        ):
            with self.assertRaises(ValueError):
                contrast_value(zero, one, response, mass_response=mass)


if __name__ == '__main__':
    unittest.main()
