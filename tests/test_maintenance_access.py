"""Independent physical and finite-continuation checks for paid maintenance.

The maintenance oracle spells out the six physical NANDs and enumerates
their fault flags. It does not call maintenance_row, voter_table,
execute_voter, the new quotient, or the signature builder.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import unittest

from cdka.boundary_voting import BITS, STATES, RATE, HEALTH, raw_update
from cdka.maintenance_access import (
    SUCCESS, WRITE_ERROR, PAID_STATES, PAID_INDEX, MACRO_INDEX,
    base_operators, base_probes, paid_operators, paid_probes,
    maintenance_row, raw_maintenance_row, maintenance_traces,
    macro_operators, paid_label, witness_laws, word_cost, evaluate_word,
)
from cdka.semantic_closure import close_continuations, dot, point, matrix


def oracle_voter(bits, errors):
    """Direct scalar wiring; all six errors belong to distinct physical gates."""
    a, b, c = bits
    n0 = (1 - a * b) ^ errors[0]
    n1 = (1 - a * c) ^ errors[1]
    n2 = (1 - b * c) ^ errors[2]
    n3 = (1 - n0 * n1) ^ errors[3]
    n4 = (1 - n3 * n3) ^ errors[4]
    return (1 - n2 * n4) ^ errors[5]


@lru_cache(None)
def oracle_readout(bits, rate):
    value = F(0)
    for errors in product((0, 1), repeat=6):
        n = sum(errors)
        value += rate**n * (1-rate)**(6-n) * oracle_voter(bits, errors)
    return value


def add(row, target, probability):
    if probability:
        row[target] = row.get(target, F(0)) + probability


@lru_cache(None)
def oracle_service(state, success):
    """Enumerate gate faults, repair success and subsequent health transition."""
    z, bits = state
    row = {}
    for errors in product((0, 1), repeat=6):
        n = sum(errors)
        probability = RATE[z]**n * (1-RATE[z])**(6-n)
        request = oracle_voter(bits, errors)
        outcomes = ((z, F(1)),) if not request else ((0, success), (z, 1-success))
        for after_service, p_service in outcomes:
            for next_health, p_health in enumerate(HEALTH[after_service]):
                add(row, (next_health, bits), probability * p_service * p_health)
    return row


@lru_cache(None)
def oracle_paid_row(state, primitive, success=SUCCESS):
    budget, health, bits = state
    if primitive == 'M':
        if not budget:
            return {}
        return {(0, h, b): p for (h, b), p in oracle_service((health, bits), success).items()}
    mode = {'D': 'diffuse', 'R': 'regenerate'}[primitive]
    return {(budget, h, b): p
            for (h, b), p in raw_update((health, bits), mode, WRITE_ERROR).items()}


def oracle_execute(law, word, success=SUCCESS):
    current = {s: p for s, p in zip(PAID_STATES, law) if p}
    for primitive in word:
        target = {}
        for state, p in current.items():
            for next_state, q in oracle_paid_row(state, primitive, success).items():
                add(target, next_state, p*q)
        current = target
    return sum((p*oracle_readout(bits, RATE[z])
                for (_, z, bits), p in current.items()), F(0))


def independent_rank(vectors):
    """Plain rational Gaussian elimination; independent of ExactBasis."""
    echelon = {}
    for candidate in vectors:
        row = list(candidate)
        for column, known in sorted(echelon.items()):
            scale = row[column]
            if scale:
                row = [x - scale*y for x, y in zip(row, known)]
        pivot = next((j for j, x in enumerate(row) if x), None)
        if pivot is not None:
            scale = row[pivot]
            echelon[pivot] = tuple(x/scale for x in row)
    return len(echelon)


def oracle_response_vectors(max_length):
    """Exhaustive finite words, not the production basis-discovery queue."""
    operators = {
        primitive: tuple({PAID_INDEX[t]: p for t, p in oracle_paid_row(s, primitive).items()}
                         for s in PAID_STATES)
        for primitive in ('D', 'R', 'M')
    }
    probes = (
        tuple(F(1) for _ in PAID_STATES),
        tuple(oracle_readout(bits, RATE[z]) for _, z, bits in PAID_STATES),
        tuple(F(r == 0) for r, _, _ in PAID_STATES),
        tuple(F(r == 1) for r, _, _ in PAID_STATES),
    )
    vectors = set(probes)
    frontier = list(probes)
    for _ in range(max_length):
        fresh = []
        for value in frontier:
            for q in operators.values():
                row = tuple(sum((p * value[j] for j, p in source.items()), F(0)) for source in q)
                vectors.add(row)
                fresh.append(row)
        frontier = fresh
    return tuple(vectors)


class MaintenanceAccessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops = paid_operators()
        cls.probes = paid_probes()
        cls.closure = close_continuations(cls.ops, cls.probes)
        legacy = base_operators()
        cls.legacy_closure = close_continuations(
            {k: legacy[k] for k in ('D', 'R')}, base_probes())

    def test_operational_updates_are_exactly_inherited(self):
        for primitive, mode in (('D', 'diffuse'), ('R', 'regenerate')):
            for i, (budget, health, bits) in enumerate(PAID_STATES):
                expected = {PAID_INDEX[(budget, h, b)]: p
                            for (h, b), p in raw_update((health, bits), mode, WRITE_ERROR).items()}
                self.assertEqual(self.ops[primitive][i], expected)

    def test_maintenance_matches_independent_six_gate_event_oracle(self):
        for success in (F(0), SUCCESS, F(1)):
            for state in STATES:
                expected = oracle_service(state, success)
                self.assertEqual(maintenance_row(state, success), expected)
                self.assertEqual(raw_maintenance_row(state, success), expected)
                self.assertEqual(sum(expected.values(), F(0)), 1)

    def test_full_traces_keep_gate_repair_and_health_causality(self):
        for state in STATES:
            traces = maintenance_traces(state)
            self.assertEqual(sum((t['probability'] for t in traces), F(0)), 1)
            aggregate = {}
            for trace in traces:
                self.assertEqual(trace['request'], oracle_voter(state[1], trace['fault_mask']))
                self.assertFalse(trace['repair_succeeded'] and not trace['request'])
                self.assertEqual(trace['target'][1], state[1])
                if trace['repair_succeeded']:
                    self.assertEqual(trace['post_service_health'], 0)
                add(aggregate, trace['target'], trace['probability'])
            self.assertEqual(aggregate, oracle_service(state, SUCCESS))

    def test_prepaid_slot_is_consumed_even_when_repair_cannot_succeed(self):
        for success in (F(0), SUCCESS, F(1)):
            q = paid_operators(success)['M']
            for i, (budget, _, bits) in enumerate(PAID_STATES):
                self.assertEqual(sum(q[i].values(), F(0)), budget)
                for j in q[i]:
                    self.assertEqual(PAID_STATES[j][0], 0)
                    self.assertEqual(PAID_STATES[j][2], bits)

    def test_second_service_is_impossible_under_every_intermediate_outcome(self):
        for i in range(32):
            after_one = self.ops['M'][i]
            self.assertTrue(all(not self.ops['M'][j] for j in after_one))
            self.assertEqual(evaluate_word(point(32, i), ('M', 'M')), 0)
        self.assertFalse(word_cost(('M', 'D', 'M'))['admissible_from_one_slot'])

    def test_already_healthy_bank_keeps_the_declared_degradation_law(self):
        for bits in BITS:
            for success in (F(0), SUCCESS, F(1)):
                self.assertEqual(maintenance_row((0, bits), success),
                                 {(0, bits): F(19, 20), (1, bits): F(1, 20)})

    def test_all_24_state_macro_rows_match_raw_aggregation(self):
        for success in (F(0), SUCCESS, F(1)):
            macro = macro_operators(success)
            for primitive in ('D', 'R', 'M'):
                for state in PAID_STATES:
                    aggregate = {}
                    for target, p in oracle_paid_row(state, primitive, success).items():
                        add(aggregate, MACRO_INDEX[paid_label(target)], p)
                    self.assertEqual(aggregate, macro[primitive][MACRO_INDEX[paid_label(state)]])
        for budget in (0, 1):
            for z, (a, b, c) in STATES:
                left = point(32, PAID_INDEX[(budget, z, (a, b, c))])
                right = point(32, PAID_INDEX[(budget, z, (a, c, b))])
                self.assertTrue(self.closure.equivalent(left, right))

    def test_two_update_values_match_independent_forward_enumeration(self):
        for i in range(32):
            law = point(32, i)
            for word in product(('D', 'R', 'M'), repeat=2):
                self.assertEqual(evaluate_word(law, word), oracle_execute(law, word))

    def test_witnesses_are_probability_laws_with_the_same_hidden_health(self):
        for budget in (0, 1):
            for law in witness_laws(paid=True, budget=budget):
                self.assertEqual(sum(law), 1)
                self.assertTrue(all(p >= 0 for p in law))
                self.assertTrue(all(not p or (r == budget and z == 1)
                                    for (r, z, _), p in zip(PAID_STATES, law)))

    def test_witness_equality_covers_the_old_closed_library(self):
        self.assertEqual(self.legacy_closure.dimension, 10)
        self.assertTrue(self.legacy_closure.verify())
        left, right = witness_laws()
        self.assertTrue(self.legacy_closure.equivalent(left, right))
        paid_left, paid_right = witness_laws(paid=True, budget=1)
        for length in range(5):
            for word in product(('D', 'R'), repeat=length):
                self.assertEqual(oracle_execute(paid_left, word), oracle_execute(paid_right, word))

    def test_paid_maintenance_is_an_exact_shortest_separator(self):
        left, right = witness_laws(paid=True, budget=1)
        self.assertEqual(evaluate_word(left, ()), F(468805981, 911641250))
        self.assertEqual(evaluate_word(left, ()), evaluate_word(right, ()))
        expected = F(21619539012817056454767961911,
                     1780549316406250000000000000000)
        self.assertEqual(evaluate_word(left, ('M',)) - evaluate_word(right, ('M',)), expected)
        separator = self.closure.separator(left, right)
        self.assertEqual(separator['word'], ('M',))
        self.assertEqual(separator['probe'], 'readout')
        self.assertEqual(separator['difference'], -expected)

    def test_repair_success_scales_the_gap_and_zero_success_removes_it(self):
        left, right = witness_laws(paid=True, budget=1)
        default = evaluate_word(left, ('M',)) - evaluate_word(right, ('M',))
        for success, expected_rank in ((F(0), 20), (SUCCESS, 22), (F(1), 22)):
            self.assertEqual(evaluate_word(left, ('M',), success) - evaluate_word(right, ('M',), success),
                             default * success / SUCCESS)
            closed = self.closure if success == SUCCESS else close_continuations(
                paid_operators(success), paid_probes())
            self.assertEqual(closed.dimension, expected_rank)
            self.assertTrue(closed.verify())
            self.assertEqual(closed.equivalent(left, right), success == 0)

    def test_consumed_resource_allows_the_same_distinction_to_be_forgotten(self):
        left, right = witness_laws(paid=True, budget=0)
        self.assertTrue(self.closure.equivalent(left, right))
        self.assertIsNone(self.closure.separator(left, right))
        for primitive in ('D', 'R', 'M'):
            self.assertEqual(oracle_execute(left, (primitive,)), oracle_execute(right, (primitive,)))

    def test_22_dimensional_closure_has_an_independent_finite_lower_bound(self):
        self.assertEqual(self.closure.dimension, 22)
        self.assertTrue(self.closure.verify())
        self.assertEqual(independent_rank(oracle_response_vectors(4)), 22)
        # Linear evaluator rank and the count of distinguishable point states differ.
        self.assertEqual(len(self.closure.state_classes()), 24)

    def test_two_total_primitive_steps_need_seven_or_eleven_coordinates_by_resource(self):
        responses = oracle_response_vectors(2)
        self.assertEqual(independent_rank([v[:16] for v in responses]), 7)
        self.assertEqual(independent_rank([v[16:] for v in responses]), 11)

    def test_exposing_an_intermediate_vote_changes_the_information_contract(self):
        # This instrument is NOT available in the principal controller library.
        # It records a further physical read without changing the hidden state.
        # Repeated reads give a new joint event even with no maintenance.
        old = base_operators()
        readable = {key: old[key] for key in ('D', 'R')}
        g = tuple(oracle_readout(bits, RATE[z]) for z, bits in STATES)
        readable['observe1'] = matrix([{i: g[i]} for i in range(16)])
        readable['observe0'] = matrix([{i: 1-g[i]} for i in range(16)])
        larger = close_continuations(readable, {'mass': [1]*16, 'readout': g})
        self.assertEqual(larger.dimension, 12)
        self.assertTrue(larger.verify())
        left, right = witness_laws()
        self.assertFalse(larger.equivalent(left, right))
        both_reads_one = tuple(x*x for x in g)
        self.assertEqual(dot(left, both_reads_one)-dot(right, both_reads_one),
                         -F(1014707502017298432, 69552707672119140625))

    def test_word_prices_separate_reusable_hardware_from_executions(self):
        self.assertEqual(word_cost(('D', 'M', 'R')),
                         {'installed_nands': 6, 'retained_cells': 3,
                          'voter_evaluations': 3, 'nand_evaluations': 18,
                          'cell_writes': 3, 'cell_channel_updates': 6,
                          'prepaid_service_slots': 1,
                          'clock_intervals': 4, 'admissible_from_one_slot': True})
        self.assertEqual(word_cost(('M',), terminal_readout=False)['nand_evaluations'], 6)
        with self.assertRaises(ValueError):
            word_cost(('unknown',))

    def test_persistent_repair_health_cannot_be_replaced_by_a_mean_gate_rate(self):
        state = (1, 1, (0, 1, 1))
        law = point(32, PAID_INDEX[state])
        future = oracle_paid_row(state, 'M')
        correct = sum((p*oracle_readout(bits, RATE[z]) for (_, z, bits), p in future.items()), F(0))
        mean = sum((p*RATE[z] for (_, z, _), p in future.items()), F(0))
        naive = oracle_readout(state[2], mean)
        self.assertEqual(evaluate_word(law, ('M',)), correct)
        self.assertNotEqual(correct, naive)


if __name__ == '__main__':
    unittest.main()
