"""Independent finite controls for selector and realization scope claims."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import unittest

from experiments.core_interface_witness import model, run, advance, dot, rank


def raw_paths(initial_state, word):
    """Enumerate microbranches from operation meanings, without matrix helpers."""
    paths = [(initial_state, F(1))]
    for action in word:
        following = []
        for state, mass in paths:
            if action == 'I':
                branches = [(state, F(1))]
            elif action == 'T':
                branches = [(1-state if state < 2 else 2, F(1))]
            elif action == 'R':
                branches = [(0, F(1, 2)), (1, F(1, 2))] if state < 2 else [(2, F(1))]
            elif action == 'S':
                branches = [(2, F(1))] if state < 2 else [(0, F(1, 2)), (1, F(1, 2))]
            elif action == 'C':
                branches = [(0 if state < 2 else 2, F(1))]
            elif action == 'U':
                branches = [(2, F(1))] if state == 0 else [(0, F(1, 2)), (1, F(1, 2))]
            elif action == 'W':
                branches = [(0, F(1, 2)), (1, F(1, 2))] if state == 0 else [(2, F(1))]
            else:
                raise ValueError('raw action')
            following.extend((target, mass*probability) for target, probability in branches)
        paths = following
    return tuple(sum((mass for target, mass in paths if target == state), F(0))
                 for state in range(3))


class CoreInterfaceWitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = model()
        cls.evidence = run()

    def test_fixed_word_scalar_matches_independent_microbranches(self):
        k, g, feature = (self.case[name] for name in ('operators', 'terminal', 'feature'))
        count = 0
        for depth in range(4):
            for letters in product(tuple(k), repeat=depth):
                word = ''.join(letters)
                for state in range(3):
                    initial = k['I'][state]
                    physical = raw_paths(state, word)
                    self.assertEqual(physical, advance(initial, word, k))
                    self.assertEqual(dot(physical, g), F(1, 2)+(-1)**word.count('S')*feature[state])
                    count += 1
        self.assertEqual(count, 468)

    def test_selector_macro_has_declared_observation_dependency(self):
        # U chooses S at A0/B and R at A1. A0/A1 cannot share the only
        # available observation if this selector is claimed implementable.
        micro_observation = (0, 1, 0)
        routing = {0: 'S', 1: 'R'}
        actual = self.evidence['selectors']['common_reset_control']['kernel_U']
        for state in range(3):
            expected = raw_paths(state, routing[micro_observation[state]])
            self.assertEqual(expected, tuple(map(F, actual[state])))
            self.assertEqual(expected, raw_paths(state, 'U'))
        group_observation = ('A', 'A', 'B')
        self.assertEqual(group_observation[0], group_observation[1])
        self.assertNotEqual(routing[micro_observation[0]], routing[micro_observation[1]])

    def test_failure_of_full_law_family_and_task_sufficiency_are_distinct(self):
        e, k = self.case['emission'], self.case['operators']
        after = advance(e[0], 'C', k)
        self.assertEqual(after, (F(1), F(0), F(0)))
        self.assertEqual(e[0][0], e[0][1])
        self.assertNotEqual(after[0], after[1])
        self.assertEqual(dot(e[0], self.case['feature']), dot(after, self.case['feature']))
        self.assertEqual(rank((*e, after)), 3)

    def test_output_reset_does_not_recover_lost_input_phase_weights(self):
        d = self.evidence['decision_reversal']
        laws = [tuple(map(F, row)) for row in d['preparations']]
        endpoints = []
        for law in laws:
            endpoints.append(tuple(sum((law[s]*raw_paths(s, 'U')[j] for s in range(3)), F(0))
                                   for j in range(3)))
        self.assertNotEqual(endpoints[0], endpoints[1])
        # Both endpoints are freshly exchangeable, despite different weights.
        for law in endpoints:
            self.assertEqual(law[0], law[1])
        self.assertEqual([sum(row[:2]) for row in endpoints], [F(7, 10), F(2, 5)])
        self.assertEqual(d['old_signatures'], ['1/10', '1/10'])

    def test_stale_decoder_changes_common_optimum_and_joint_feasibility(self):
        d = self.evidence['decision_reversal']
        self.assertEqual(d['actual']['minimax_program'], 'R')
        self.assertEqual(d['actual']['minimax_regret'], '1/10')
        self.assertEqual(d['actual']['maximin_value'], '3/5')
        self.assertEqual(d['actual']['worst_regrets'], ['1/10', '3/10', '1/5'])
        self.assertEqual(d['actual']['gate']['feasible_programs'], [])
        self.assertEqual(d['false_decision']['minimax_program'], 'U')
        self.assertEqual(d['false_decision']['minimax_regret'], '0')
        self.assertEqual(d['false_decision']['maximin_value'], '7/10')
        self.assertEqual(d['false_decision']['gate']['feasible_programs'], ['U'])

    def test_complete_one_step_deterministic_class_has_terminal_cover(self):
        p = self.evidence['deterministic_policy_cover']
        laws = [tuple(map(F, row)) for row in self.evidence['decision_reversal']['preparations']]
        self.assertEqual(len(set(tuple(rule) for rule in p['routing_by_observation'].values())), 4)
        for rule, routing in p['routing_by_observation'].items():
            for state, observation in enumerate(p['observation_by_state']):
                self.assertEqual(raw_paths(state, rule), raw_paths(state, routing[observation]))
        w_values = [sum((law[s]*sum(raw_paths(s, 'W')[:2]) for s in range(3)), F(0))
                    for law in laws]
        self.assertEqual(w_values, [F(3, 10), F(3, 5)])
        self.assertEqual(p['retained_cover']['W'], 'R')
        for key in ('informed_values', 'minimax_regret', 'maximin_value', 'gate'):
            self.assertEqual(p['full_decision'][key], self.evidence['decision_reversal']['actual'][key])
        contract = self.evidence['decision_contract']
        self.assertEqual(contract['preparation_slots'], 1)
        self.assertEqual(contract['remaining_continuation_slots'], 1)
        self.assertFalse(contract['external_controller_coin_available'])

    def test_two_step_boundary_and_failure_of_contextual_dominance(self):
        control = self.evidence['two_step_positive_control']
        laws = [tuple(map(F, row)) for row in self.evidence['decision_reversal']['preparations']]
        for column, word in enumerate(control['labels']):
            for row, law in enumerate(laws):
                independent = sum((law[s]*sum(raw_paths(s, word)[:2]) for s in range(3)), F(0))
                self.assertEqual(independent, F(control['actual_values'][row][column]))
        self.assertEqual(control['selected_values']['SU'], ['4/5', '4/5'])
        self.assertEqual(control['selected_values']['WU'], ['17/20', '7/10'])
        self.assertEqual(control['decision']['minimax_regret'], '1/20')
        self.assertEqual(control['decision']['gate']['feasible_programs'], ['SU', 'WU'])
        restricted = control['restricted_RSU_library']['decision']
        self.assertEqual(restricted['minimax_regret'], '0')
        self.assertEqual(restricted['gate']['feasible_programs'], ['RU', 'SU'])
        self.assertFalse(control['within_actual_contract'])

    def test_external_coin_changes_the_policy_class(self):
        control = self.evidence['randomization_boundary_control']
        laws = [tuple(map(F, row)) for row in self.evidence['decision_reversal']['preparations']]
        independent = []
        for law in laws:
            independent.append(sum((law[s]*(F(2, 3)*sum(raw_paths(s, 'R')[:2])
                                            + F(1, 3)*sum(raw_paths(s, 'U')[:2]))
                                    for s in range(3)), F(0)))
        self.assertEqual(independent, [F(19, 30), F(8, 15)])
        self.assertEqual(control['same_input_regrets'], ['1/15', '1/15'])
        self.assertTrue(control['strict_regret_improvement'])
        self.assertFalse(control['within_actual_contract'])
        self.assertEqual(control['maximin_value_with_any_mixture'], '3/5')
        self.assertFalse(control['joint_gate_feasible_with_any_mixture'])

    def test_frozen_witness_reproduces_without_numerical_discovery(self):
        path = Path(__file__).resolve().parents[1] / 'docs/data/core-interface-witness.json'
        self.assertEqual(self.evidence, json.loads(path.read_text()))
        self.assertEqual(self.evidence['bounded_control']['words'], 781)
        self.assertEqual(self.evidence['bounded_control']['value_comparisons'], 2343)


if __name__ == '__main__':
    unittest.main()
