import builtins
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from cdka.maintenance_access import base_operators
from cdka.preparation_families import (
    _check_cover, _discover_cover, _exact_support,
    check_family, compile_family, make_preparation_model, preparation_binding,
)
from cdka.reachable_diagnosis import acquisition, advance_updates, preparation_laws
from cdka.reachable_restriction import contrast_signature
from cdka.semantic_closure import push


FIXTURE = Path(__file__).parent / 'fixtures/preparation-families-small.json'


def no_numerical_import(name, *args, **kwargs):
    if name.split('.')[0] in ('numpy', 'scipy'):
        raise AssertionError('optional numerical import during standard-library operation')
    return ORIGINAL_IMPORT(name, *args, **kwargs)


ORIGINAL_IMPORT = builtins.__import__


class PreparationFamiliesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops = base_operators()
        cls.law = acquisition()
        cls.model = make_preparation_model(cls.ops, cls.law)
        cls.certificate = json.loads(FIXTURE.read_text())
        cls.frontier = check_family(cls.certificate, cls.ops, cls.law, 4)

    def test_frozen_checker_needs_no_discovery_or_numerical_imports(self):
        with patch('builtins.__import__', side_effect=no_numerical_import), \
                patch('cdka.preparation_families._discover_cover', side_effect=AssertionError('discovery')), \
                patch('cdka.preparation_families._numeric_cover', side_effect=AssertionError('numerical discovery')), \
                patch('cdka.preparation_families.ExactBasis', side_effect=AssertionError('basis search')):
            actual = check_family(deepcopy(self.certificate), self.ops, self.law, 4)
        self.assertEqual(actual, self.frontier)
        self.assertEqual(len(actual), 13)

    def test_recursive_convex_witnesses_cover_every_physical_history(self):
        # Compose the local witnesses independently. Then compare their
        # represented signatures with the full physical sixteen-state laws.
        represented = {'': {0: F(1)}}
        frontier = [('', self.model['initial'])]
        for depth, layer in enumerate(self.certificate['layers']):
            candidates = ([(word+letter, push(point, self.model['sparse_A'][letter]))
                           for word, point in frontier for letter in ('D', 'R')]
                          if depth else frontier)
            retained = [candidates[index] for index in layer['keep']]
            after = {}
            for word, mixture in represented.items():
                for branch, letter in enumerate(('D', 'R') if depth else ('',)):
                    combined = {}
                    for previous_index, previous_weight in mixture.items():
                        child_index = 2*previous_index+branch if depth else previous_index
                        for kept_index, coefficient in layer['cover'][child_index]:
                            combined[kept_index] = combined.get(kept_index, F(0)) + previous_weight*F(coefficient)
                    self.assertEqual(sum(combined.values(), F(0)), 1)
                    self.assertTrue(all(weight >= 0 for weight in combined.values()))
                    history = word+letter
                    actual_law = advance_updates(self.law, history)
                    offset, signed = contrast_signature(*actual_law)
                    rebuilt = tuple(sum((weight * retained[index][1][coordinate]
                                         for index, weight in combined.items()), F(0))
                                    for coordinate in range(4))
                    self.assertEqual(offset, F(1, 2))
                    self.assertEqual(rebuilt, tuple(-value for value in signed))
                    after[history] = combined
            represented, frontier = after, retained
        self.assertEqual(len(represented), 16)
        self.assertEqual(frontier, self.frontier)
        for history, point in frontier:
            self.assertEqual(len(history), 4)
            self.assertEqual(set(history)-{'D', 'R'}, set())
            self.assertEqual(point, tuple(-value for value in contrast_signature(
                *advance_updates(self.law, history))[1]))

    def test_zero_horizon_simplex_and_conservative_paths_are_standard_library(self):
        with patch('builtins.__import__', side_effect=no_numerical_import):
            for h, optimize in ((0, True), (1, True), (2, True), (4, False)):
                frontier, certificate, stats = compile_family(self.ops, self.law, h, optimize=optimize)
                self.assertEqual(check_family(certificate, self.ops, self.law, h), frontier)
                self.assertEqual(len(stats), h+1)
                self.assertEqual(stats[-1]['history_candidates'], 2**h)
                self.assertEqual(stats[-1]['retained'], 2**h)

    def test_task_hull_is_not_a_full_probability_law_hull(self):
        uninformative = acquisition(F(1, 2))
        with patch('builtins.__import__', side_effect=no_numerical_import):
            frontier, certificate, stats = compile_family(self.ops, uninformative, 4)
            self.assertEqual(check_family(certificate, self.ops, uninformative, 4), frontier)
        self.assertEqual(frontier, [('DDDD', (F(0),)*4)])
        self.assertEqual(stats[-1]['history_candidates'], 2)
        self.assertEqual(stats[-1]['histories_never_generated'], 14)
        laws = preparation_laws(1, F(1, 2))
        self.assertNotEqual(laws['D'], laws['R'])
        self.assertEqual(contrast_signature(*laws['D']), contrast_signature(*laws['R']))

    def test_convex_mass_is_required_even_when_every_signature_is_zero(self):
        law = acquisition(F(1, 2))
        _, certificate, _ = compile_family(self.ops, law, 0)
        bad = deepcopy(certificate)
        bad['layers'][0]['cover'][0][0][1] = '2'
        with self.assertRaisesRegex(ValueError, 'sum to one'):
            check_family(bad, self.ops, law, 0)
        bad['layers'][0]['cover'][0] = []
        with self.assertRaises(ValueError):
            check_family(bad, self.ops, law, 0)

    def test_missing_or_invalid_coverage_cannot_be_vacuously_accepted(self):
        payloads = []
        for changes in ('layers', 'keep', 'cover', 'one_missing_cover', 'one_missing_layer'):
            bad = deepcopy(self.certificate)
            if changes == 'layers':
                bad['layers'] = []
            elif changes in ('keep', 'cover'):
                bad['layers'][-1][changes] = []
            elif changes == 'one_missing_cover':
                bad['layers'][-1]['cover'].pop()
            else:
                bad['layers'].pop()
            payloads.append(bad)
        for bad in payloads:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    check_family(bad, self.ops, self.law, 4)

    def test_strict_convex_witness_shapes_types_and_values(self):
        alterations = (
            lambda layer: layer['keep'].__setitem__(0, True),
            lambda layer: layer['keep'].__setitem__(0, -1),
            lambda layer: layer['keep'].append(layer['keep'][0]),
            lambda layer: layer['cover'][0].__setitem__(0, [True, '1']),
            lambda layer: layer['cover'][0].__setitem__(0, [999, '1']),
            lambda layer: layer['cover'][0].__setitem__(0, [0, '-1']),
            lambda layer: layer['cover'][0].__setitem__(0, [0, True]),
            lambda layer: layer['cover'][0].__setitem__(0, [0, 1.0]),
            lambda layer: layer['cover'][0].__setitem__(0, [0, '2/2']),
            lambda layer: layer['cover'][0].append([0, '0']),
            lambda layer: layer['cover'].__setitem__(0, [[0, '1', 'extra']]),
            lambda layer: layer.__setitem__('alleged_dimension', 0),
        )
        for alter in alterations:
            bad = deepcopy(self.certificate)
            alter(bad['layers'][0])
            with self.assertRaises(ValueError):
                check_family(bad, self.ops, self.law, 4)

    def test_retained_identity_or_weight_corruption_is_rejected(self):
        layer = self.certificate['layers'][-1]
        index = next(i for i, witness in enumerate(layer['cover']) if len(witness) > 1)
        bad = deepcopy(self.certificate)
        witness = bad['layers'][-1]['cover'][index]
        witness[0][1] = str(F(witness[0][1]) + F(1, 1000))
        witness[1][1] = str(F(witness[1][1]) - F(1, 1000))
        with self.assertRaises(ValueError):
            check_family(bad, self.ops, self.law, 4)
        bad = deepcopy(self.certificate)
        bad['layers'][-1]['keep'] = list(reversed(bad['layers'][-1]['keep']))
        with self.assertRaises(ValueError):
            check_family(bad, self.ops, self.law, 4)

    def test_binding_separates_initial_law_ordinary_physics_and_horizon(self):
        changed = dict(self.ops)
        changed['R'] = changed['D']
        with self.assertRaises(ValueError):
            check_family(self.certificate, changed, self.law, 4)
        with self.assertRaises(ValueError):
            check_family(self.certificate, self.ops, acquisition(F(1, 5)), 4)
        with self.assertRaises(ValueError):
            check_family(self.certificate, self.ops, self.law, 3)
        changed_law = [list(row) for row in self.law]
        for row in changed_law:
            row[0] += F(1, 10**9)
            row[1] -= F(1, 10**9)
        changed_model = make_preparation_model(self.ops, changed_law)
        self.assertEqual(changed_model['initial'], self.model['initial'])
        self.assertNotEqual(changed_model['binding'], self.model['binding'])
        with self.assertRaises(ValueError):
            check_family(self.certificate, self.ops, changed_law, 4)

    def test_preparation_binding_is_reusable_across_maintenance_and_terminal_tasks(self):
        other = base_operators(F(0))
        self.assertEqual(make_preparation_model(other, self.law)['binding'], self.model['binding'])
        self.assertEqual(check_family(self.certificate, other, self.law, 4), self.frontier)
        self.assertNotEqual(preparation_binding(self.model, 4), preparation_binding(self.model, 5))

    def test_physical_input_guards_are_not_replaced_by_a_digest(self):
        cases = []
        bad = deepcopy(self.ops)
        key = next(iter(bad['D'][0]))
        bad['D'][0][key] -= F(1, 10**9)
        cases.append((bad, self.law))
        bad = deepcopy(self.ops)
        bad['D'][0].clear()
        bad['D'][0][True] = F(1)
        cases.append((bad, self.law))
        bad = deepcopy(self.ops)
        bad['D'][0].clear()
        bad['D'][0][0] = 1.0
        cases.append((bad, self.law))
        bad_law = [list(row) for row in self.law]
        bad_law[0].pop()
        cases.append((self.ops, bad_law))
        bad_law = [list(row) for row in self.law]
        bad_law[0][0] += F(1, 1000)
        bad_law[1][0] -= F(1, 1000)
        cases.append((self.ops, bad_law))
        cases.append((self.ops, self.law[::-1]))
        for operators, law in cases:
            with self.assertRaises(ValueError):
                check_family(self.certificate, operators, law, 4)

    def test_horizon_and_certificate_schema_are_strict(self):
        for h in (True, -1, 4.0, '4'):
            with self.assertRaises(ValueError):
                check_family(self.certificate, self.ops, self.law, h)
        for key, value in (('schema', 'wrong'), ('history_length', True),
                           ('binding', '0'*64), ('model_binding', '0'*64)):
            bad = deepcopy(self.certificate)
            bad[key] = value
            with self.assertRaises(ValueError):
                check_family(bad, self.ops, self.law, 4)

    def test_exact_support_rejects_false_numerical_proposals(self):
        origin = (F(0),)*4
        unit = (F(1), F(0), F(0), F(0))
        self.assertIsNone(_exact_support([origin, unit], (F(2), F(0), F(0), F(0)), [0, 1]))
        self.assertIsNone(_exact_support([origin, unit], (F(0), F(1), F(0), F(0)), [0, 1]))
        self.assertEqual(_exact_support([origin, unit], (F(1, 3), F(0), F(0), F(0)), [0, 1]),
                         [(0, F(2, 3)), (1, F(1, 3))])

    def test_affine_intervals_need_no_optional_geometry_solver(self):
        candidates = [(str(i), tuple(F(i*j) for j in (1, 2, 3, 4))) for i in (0, 1, 2)]
        with patch('builtins.__import__', side_effect=no_numerical_import):
            frontier, certificate, stats = _discover_cover(candidates, True)
        portable = json.loads(json.dumps(certificate, default=str))
        self.assertEqual(_check_cover(candidates, portable), frontier)
        self.assertEqual([word for word, _ in frontier], ['0', '2'])
        self.assertEqual(stats['maximum_support'], 2)


if __name__ == '__main__':
    unittest.main()
