"""Physical and adversarial checks for compact streamed preparation decisions."""
import builtins
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from cdka.maintenance_access import base_operators, base_probes
from cdka.preparation_decisions import (
    check_decision, compile_decision, iter_preparations, joint_gate, make_problem,
    query_informed, query_informed_x,
)
from cdka.preparation_families import check_family as check_preparation_family
from cdka.program_families import (
    compile_decision as compile_table_decision, evaluate_frontier,
)
from cdka.reachable_diagnosis import acquisition, advance_updates, evaluate, preparation_laws
from cdka.reachable_restriction import contrast_signature
from cdka.semantic_closure import dot, push, word_value
from cdka.suffix_features import check_feature_family, compile_feature_family


FIXTURE = Path(__file__).parent / 'fixtures/preparation-families-small.json'
ORIGINAL_IMPORT = builtins.__import__


def no_numerical_import(name, *args, **kwargs):
    if name.split('.')[0] in ('numpy', 'scipy'):
        raise AssertionError('numerical discovery is forbidden in the pure checker')
    return ORIGINAL_IMPORT(name, *args, **kwargs)


def refresh_selected_values(certificate):
    regrets = tuple(map(F, certificate['worst_regrets']))
    minima = tuple(map(F, certificate['minimum_fidelities']))
    p = min(range(len(regrets)), key=regrets.__getitem__)
    q = max(range(len(minima)), key=minima.__getitem__)
    certificate.update(minimax_plan=p, minimax_regret=str(regrets[p]),
                       maximin_plan=q, maximin_fidelity=str(minima[q]))


class PreparationDecisionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops = base_operators()
        cls.g = base_probes()['readout']
        cls.law = acquisition()
        cls.frontier, program_certificate, _ = compile_feature_family(cls.ops, cls.g, 4)
        cls.frontier = check_feature_family(program_certificate, cls.ops, cls.g, 4)
        cls.problem = make_problem(cls.ops, cls.g, cls.law, 2, cls.frontier)
        cls.certificate, cls.stats = compile_decision(cls.problem)

    def test_streamed_signatures_and_informed_values_match_full_physics(self):
        for h in (0, 1, 2, 4):
            problem = make_problem(self.ops, self.g, self.law, h, self.frontier)
            cohort = preparation_laws(h)
            seen = []
            for history, point in iter_preparations(problem):
                seen.append(history or 'I')
                law = cohort[history or 'I']
                offset, signed = contrast_signature(*law)
                self.assertEqual(offset, F(1, 2))
                self.assertEqual(point, tuple(-value for value in signed))
                physical_values = tuple(evaluate(law, word) for word, _ in self.frontier)
                self.assertEqual(tuple(offset-dot(point, q) for _, q in self.frontier), physical_values)
                queried = query_informed(problem, history)
                self.assertEqual(queried['signature'], point)
                self.assertEqual(queried['best_value'], max(physical_values))
                self.assertEqual(physical_values[queried['best_plan']], queried['best_value'])
            self.assertEqual(seen, list(cohort))

    def test_streamed_reference_matches_table_objectives_and_joint_gates(self):
        for h in (2, 4):
            problem = make_problem(self.ops, self.g, self.law, h, self.frontier)
            certificate, stats = compile_decision(problem)
            cohort = preparation_laws(h)
            values = evaluate_frontier(self.frontier, [contrast_signature(*law) for law in cohort.values()])
            reference = compile_table_decision(values, preparation_labels=list(cohort),
                                                plan_labels=[word for word, _ in self.frontier])
            best = tuple(max(row) for row in values)
            regrets = tuple(max(b-row[j] for b, row in zip(best, values))
                            for j in range(len(self.frontier)))
            minima = tuple(min(row[j] for row in values) for j in range(len(self.frontier)))
            self.assertEqual(tuple(map(F, certificate['worst_regrets'])), regrets)
            self.assertEqual(tuple(map(F, certificate['minimum_fidelities'])), minima)
            self.assertEqual(certificate['minimax_regret'], reference['minimax_regret'])
            self.assertEqual(certificate['maximin_fidelity'], reference['maximin_fidelity'])
            self.assertEqual(stats['preparations_evaluated'], 2**h)
            self.assertEqual(stats['values_evaluated'], 2**h*len(self.frontier))
            self.assertEqual(stats['maximum_live_signature_vectors'], h+1)
            self.assertEqual(stats['query_coordinates'], 2)
            self.assertNotIn('preparation_best', certificate)
            self.assertFalse(stats['explicit_value_table'])
            self.assertFalse(stats['explicit_informed_profile'])
            self.assertTrue(check_decision(certificate, problem))
            for delta, floor in ((F(1, 500), F(21, 25)), (F(3, 1000), F(21, 25)),
                                 (F(3, 1000), F(17, 20)), (F(1, 200), F(17, 20))):
                expected = [j for j, (r, f) in enumerate(zip(regrets, minima))
                            if r <= delta and f >= floor]
                self.assertEqual(joint_gate(certificate, delta, floor), expected)
        self.assertEqual(self.certificate['plans'][self.certificate['minimax_plan']], 'DRDDM')
        self.assertEqual(self.certificate['plans'][self.certificate['maximin_plan']], 'DDDDM')
        self.assertEqual(joint_gate(self.certificate, F(3, 1000), F(17, 20)), [])

    def test_checked_hull_and_stream_use_identical_decision_and_query_contracts(self):
        hull_certificate = json.loads(FIXTURE.read_text())
        representatives = check_preparation_family(hull_certificate, self.ops, self.law, 4)
        problem = make_problem(self.ops, self.g, self.law, 4, self.frontier)
        streamed, stream_stats = compile_decision(problem)
        covered, covered_stats = compile_decision(
            problem, representatives, preparation_binding=problem['preparation_binding'])
        for key in ('plans', 'worst_regrets', 'minimum_fidelities', 'minimax_plan',
                    'minimax_regret', 'maximin_plan', 'maximin_fidelity', 'binding'):
            self.assertEqual(covered[key], streamed[key])
        self.assertEqual(covered_stats['preparations_evaluated'], 13)
        self.assertEqual(stream_stats['preparations_evaluated'], 16)
        self.assertEqual(covered_stats['query_coordinates'], stream_stats['query_coordinates'])
        for certificate in (streamed, covered):
            self.assertTrue(check_decision(certificate, problem))
            self.assertTrue(check_decision(certificate, problem, representatives,
                                          preparation_binding=problem['preparation_binding']))
        for missing_or_wrong in (None, '0'*64):
            with self.assertRaises(ValueError):
                compile_decision(problem, representatives, preparation_binding=missing_or_wrong)
            with self.assertRaises(ValueError):
                check_decision(streamed, problem, representatives, preparation_binding=missing_or_wrong)

    def test_attaining_samples_are_insufficient_for_universal_bounds(self):
        first = next(iter_preparations(self.problem))
        sampled, _ = compile_decision(self.problem, [first],
                                     preparation_binding=self.problem['preparation_binding'])
        # Each reported extremum is attained by a real history. The omitted
        # histories nevertheless refute the resulting universal claims.
        self.assertEqual(set(sampled['fidelity_attainers']), {'DD'})
        with self.assertRaisesRegex(ValueError, 'universal'):
            check_decision(sampled, self.problem)

    def test_informed_envelope_is_queried_at_signature_not_interpolated(self):
        dd, dr = query_informed(self.problem, 'DD'), query_informed(self.problem, 'DR')
        midpoint = tuple((a+b)/2 for a, b in zip(dd['signature'], dr['signature']))
        midpoint_query = query_informed_x(self.problem, midpoint)
        expected = max(self.problem['offset']-dot(midpoint, q) for _, q in self.frontier)
        self.assertEqual(midpoint_query['best_value'], expected)
        interpolated = (dd['best_value']+dr['best_value'])/2
        self.assertLess(expected, interpolated)
        self.assertEqual(query_informed_x(self.problem, dd['signature'])['best_value'], dd['best_value'])

    def test_zero_source_contrast_and_empty_workload_boundaries(self):
        front, _, _ = compile_feature_family(self.ops, self.g, 0)
        for h in (0, 3):
            problem = make_problem(self.ops, self.g, acquisition(F(1, 2)), h, front)
            certificate, stats = compile_decision(problem)
            self.assertEqual(set(certificate['worst_regrets']), {'0'})
            self.assertEqual(set(certificate['minimum_fidelities']), {'1/2'})
            self.assertEqual(stats['preparations_evaluated'], 2**h)
            self.assertEqual(certificate['ordinary_updates'], 0)
            self.assertTrue(check_decision(certificate, problem))
            self.assertEqual(joint_gate(certificate, F(0), F(1, 2)), list(range(len(front))))

    def test_generic_four_coordinate_fallback_is_exact(self):
        ops = dict(self.ops)
        ops['D'] = ops['R']
        front, cert, _ = compile_feature_family(ops, self.g, 2)
        front = check_feature_family(cert, ops, self.g, 2)
        problem = make_problem(ops, self.g, self.law, 2, front)
        self.assertIsNone(problem['codec'])
        certificate, stats = compile_decision(problem)
        self.assertEqual(stats['query_coordinates'], 4)
        self.assertTrue(check_decision(certificate, problem))
        for history, point in iter_preparations(problem):
            law = self.law
            for letter in history:
                law = tuple(push(row, ops[letter]) for row in law)
            offset, signed = contrast_signature(*law)
            self.assertEqual(point, tuple(-value for value in signed))
            physical = tuple(offset+dot(tuple(b-a for a, b in zip(*law)), word_value(ops, word, self.g))
                             for word, _ in front)
            self.assertEqual(query_informed(problem, history)['best_value'], max(physical))

    def test_checker_needs_no_compiler_search_or_numerical_packages(self):
        portable = json.loads(json.dumps(self.certificate))
        with patch('builtins.__import__', side_effect=no_numerical_import), \
                patch('cdka.preparation_decisions.compile_decision', side_effect=AssertionError('search')), \
                patch('cdka.reachable_diagnosis.preparation_laws', side_effect=AssertionError('table')), \
                patch('cdka.program_families.evaluate_frontier', side_effect=AssertionError('table')):
            self.assertTrue(check_decision(portable, self.problem))

    def test_universal_bounds_and_exact_attainment_are_both_mandatory(self):
        changes = (
            ('worst_regrets', lambda value: value/2, 'universal'),
            ('minimum_fidelities', lambda value: value+F(1, 1000), 'universal'),
            ('worst_regrets', lambda value: value+F(1, 1000), 'attainer'),
            ('minimum_fidelities', lambda value: value-F(1, 1000), 'attainer'),
        )
        for key, change, failure in changes:
            bad = deepcopy(self.certificate)
            bad[key] = [str(change(F(value))) for value in bad[key]]
            refresh_selected_values(bad)
            with self.subTest(key=key, failure=failure), self.assertRaisesRegex(ValueError, failure):
                check_decision(bad, self.problem)

    def test_real_history_and_correct_informed_comparator_are_checked(self):
        bad = deepcopy(self.certificate)
        witness = bad['regret_attainers'][0]
        law = advance_updates(self.law, witness['history'])
        values = tuple(evaluate(law, word) for word, _ in self.frontier)
        witness['comparator'] = min(range(len(values)), key=values.__getitem__)
        self.assertLess(values[witness['comparator']], max(values))
        with self.assertRaisesRegex(ValueError, 'comparator'):
            check_decision(bad, self.problem)
        bad = deepcopy(self.certificate)
        different = next(history for history in preparation_laws(2)
                         if evaluate(advance_updates(self.law, history), self.frontier[0][0])
                         != F(bad['minimum_fidelities'][0]))
        bad['fidelity_attainers'][0] = different
        with self.assertRaisesRegex(ValueError, 'attainer'):
            check_decision(bad, self.problem)

    def test_certificate_schema_shapes_exact_types_and_indices_are_strict(self):
        mutations = (
            lambda c: c.__setitem__('schema', 'wrong'),
            lambda c: c.__setitem__('binding', '0'*64),
            lambda c: c.__setitem__('history_length', True),
            lambda c: c.__setitem__('ordinary_updates', 4.0),
            lambda c: c.__setitem__('minimax_plan', True),
            lambda c: c.__setitem__('maximin_plan', -1),
            lambda c: c.__setitem__('minimax_regret', 0.0),
            lambda c: c.__setitem__('maximin_fidelity', False),
            lambda c: c['worst_regrets'].__setitem__(0, '0/1'),
            lambda c: c['minimum_fidelities'].__setitem__(0, 1.0),
            lambda c: c['worst_regrets'].pop(),
            lambda c: c['minimum_fidelities'].pop(),
            lambda c: c['regret_attainers'].pop(),
            lambda c: c['fidelity_attainers'].pop(),
            lambda c: c['regret_attainers'].__setitem__(0, None),
            lambda c: c['regret_attainers'][0].__setitem__('comparator', False),
            lambda c: c['regret_attainers'][0].__setitem__('comparator', 999),
            lambda c: c['regret_attainers'][0].__setitem__('history', 'DM'),
            lambda c: c['fidelity_attainers'].__setitem__(0, 'DDD'),
            lambda c: c['plans'].reverse(),
            lambda c: c.__setitem__('informed_samples', []),
            lambda c: c.pop('minimum_fidelities'),
        )
        for mutation in mutations:
            bad = deepcopy(self.certificate)
            mutation(bad)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                check_decision(bad, self.problem)
        for malformed in (None, [], '', 2):
            with self.assertRaises(ValueError):
                check_decision(malformed, self.problem)

    def test_problem_digest_binds_raw_physics_law_horizon_and_ordered_responses(self):
        variants = []
        ops = base_operators(F(0))
        variants.append(make_problem(ops, self.g, self.law, 2, self.frontier))
        variants.append(make_problem(self.ops, self.g, acquisition(F(1, 5)), 2, self.frontier))
        variants.append(make_problem(self.ops, self.g, self.law, 3, self.frontier))
        variants.append(make_problem(self.ops, self.g, self.law, 2, list(reversed(self.frontier))))
        variants.append(make_problem(self.ops, self.g, self.law, 2, self.frontier, contract={'case': 2}))
        q = list(self.frontier[0][1]); q[0] += F(1, 1000)
        changed_frontier = [(self.frontier[0][0], tuple(q))]+self.frontier[1:]
        variants.append(make_problem(self.ops, self.g, self.law, 2, changed_frontier))
        changed_g = list(self.g); changed_g[0] = 1-changed_g[0]
        variants.append(make_problem(self.ops, changed_g, self.law, 2, self.frontier))
        for variant in variants:
            self.assertNotEqual(variant['binding'], self.problem['binding'])
            with self.assertRaises(ValueError):
                check_decision(self.certificate, variant)
        self.assertEqual(variants[0]['preparation_binding'], self.problem['preparation_binding'])
        self.assertEqual(variants[3]['preparation_binding'], self.problem['preparation_binding'])
        self.assertEqual(variants[-1]['preparation_binding'], self.problem['preparation_binding'])

    def test_forged_problem_data_is_revalidated_instead_of_trusted(self):
        mutations = (
            lambda p: p.__setitem__('binding', '0'*64),
            lambda p: p.__setitem__('initial', (F(0),)*4),
            lambda p: p.__setitem__('offset', 0.5),
            lambda p: p.__setitem__('ordinary_updates', 4.0),
            lambda p: p['A'].__setitem__('D', p['A']['R']),
            lambda p: p.__setitem__('codec', None),
            lambda p: p['codec'].__setitem__('ratio', F(1)),
        )
        for mutation in mutations:
            bad = deepcopy(self.problem)
            mutation(bad)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                check_decision(self.certificate, bad)

    def test_factory_and_query_inputs_reject_invalid_domains_and_lossy_types(self):
        for h in (-1, True, 2.0, '2'):
            with self.assertRaises(ValueError):
                make_problem(self.ops, self.g, self.law, h, self.frontier)
        for frontier in ([], [('DD', (0.0, 0, 0, 0))], [('DMM', (0,)*4)],
                         [('D', (0,)*4), ('RR', (0,)*4)], [self.frontier[0]]*2):
            with self.assertRaises(ValueError):
                make_problem(self.ops, self.g, self.law, 2, frontier)
        malformed_ops = deepcopy(self.ops)
        key = next(iter(malformed_ops['M'][0]))
        malformed_ops['M'][0][key] /= 2
        with self.assertRaises(ValueError):
            make_problem(malformed_ops, self.g, self.law, 2, self.frontier)
        for law in (self.law[::-1], self.law[0], tuple(tuple(map(float, row)) for row in self.law)):
            with self.assertRaises(ValueError):
                make_problem(self.ops, self.g, law, 2, self.frontier)
        for history in ('I', 'D', 'DDM', ['D', 'D'], 0):
            with self.assertRaises(ValueError):
                query_informed(self.problem, history)
        for x in ((F(-1), 0, 0, 0), (0, 0, 0), (0.0, 0, 0, 0), (False, 0, 0, 0)):
            with self.assertRaises(ValueError):
                query_informed_x(self.problem, x)
        for delta, floor in ((True, 0), (0, 0.5), (F(-1), 0), ('0/1', 0)):
            with self.assertRaises(ValueError):
                joint_gate(self.certificate, delta, floor)

    def test_supplied_family_must_be_nonempty_and_well_formed(self):
        point = next(iter_preparations(self.problem))
        for family in ([], [('DD', (0, 0, 0))], [('DM', point[1])],
                       [('DD', (False, 0, 0, 0))], [('DD', (F(-1), 0, 0, 0))]):
            with self.assertRaises(ValueError):
                compile_decision(self.problem, family,
                                 preparation_binding=self.problem['preparation_binding'])
            with self.assertRaises(ValueError):
                check_decision(self.certificate, self.problem, family,
                               preparation_binding=self.problem['preparation_binding'])


if __name__ == '__main__':
    unittest.main()
