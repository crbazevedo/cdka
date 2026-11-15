"""Physical closure, proof-boundary and shared-algebra ablation regressions."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import unittest
from unittest.mock import patch

from cdka.boundary_voting import BITS
from cdka.maintenance_access import base_operators, base_probes
from cdka.program_families import compile_family, transports
from cdka.reachable_diagnosis import plan_words
from cdka.reachable_restriction import CONTRAST_BASIS, contrast_response
from cdka.semantic_closure import ExactBasis, apply, dot, push, word_value
from cdka.suffix_features import (
    FEATURE_BASIS, action, check_feature_family, check_features,
    compile_feature_family, compile_features,
)


class SuffixFeaturesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops = base_operators()
        cls.g = base_probes()['readout']
        cls.certificate = compile_features(cls.ops, cls.g)
        cls.features = check_features(cls.certificate, cls.ops, cls.g)
        cls.frontier, cls.family, cls.stats = compile_feature_family(
            cls.ops, cls.g, 4, feature_certificate=cls.certificate)

    def test_feature_checker_is_portable_and_does_not_rediscover(self):
        certificate = json.loads(json.dumps(self.certificate))
        family = json.loads(json.dumps(self.family))
        with patch('cdka.suffix_features.ExactBasis', side_effect=AssertionError('no row reduction')):
            with patch('cdka.suffix_features._cover', side_effect=AssertionError('no Pareto search')):
                self.assertEqual(check_features(certificate, self.ops, self.g), self.features)
                self.assertEqual(check_feature_family(family, self.ops, self.g, 4), self.frontier)

    def test_ordinary_and_maintenance_responses_are_full_physical_equalities(self):
        entries = [('', self.features['z'])]
        for n in range(5):
            if n:
                entries = [(a+word, action(self.features['T'][a], z))
                           for word, z in entries for a in ('D', 'R')]
            for word, z in entries:
                full = word_value(self.ops, word, self.g)
                self.assertEqual(z, tuple(dot(row, full) for row in FEATURE_BASIS))
                self.assertEqual(action(self.features['U'], z), contrast_response(full))
                self.assertEqual(action(self.features['V'], z),
                                 contrast_response(apply(self.ops['M'], full)))

    def test_fixed_basis_is_independent_of_repair_success(self):
        basis = ExactBasis(16)
        self.assertTrue(all(basis.add(row) for row in FEATURE_BASIS))
        self.assertEqual(len(basis.originals), 8)
        for success in (F(0), F(4, 5), F(1)):
            with self.subTest(success=success):
                operators = base_operators(success)
                certificate = compile_features(operators, self.g)
                features = check_features(certificate, operators, self.g)
                self.assertEqual(features['C'], FEATURE_BASIS)
                frontier, family, _ = compile_feature_family(
                    operators, self.g, 2, feature_certificate=certificate)
                self.assertEqual(frontier, compile_family(operators, self.g, 2)[0])
                self.assertEqual(check_feature_family(family, operators, self.g, 2), frontier)
        self.assertEqual({a: sum(len(row) for row in self.features['T'][a]) for a in ('D', 'R')},
                         {'D': 16, 'R': 31})

    def test_signed_features_are_not_a_stochastic_quotient(self):
        self.assertTrue(any(value < 0 for rows in self.features['T'].values()
                            for row in rows for value in row.values()))
        self.assertTrue(all(value >= 0 for rows in self.features['A'].values()
                            for row in rows for value in row.values()))
        # The maintenance map genuinely uses the four additional features.
        self.assertTrue(any(j >= 4 for row in self.features['V'] for j in row))

    def test_baseline_changes_only_suffix_algebra(self):
        parent_frontier, _, parent_stats = compile_family(self.ops, self.g, 4)
        self.assertEqual(self.frontier, parent_frontier)
        self.assertEqual(self.stats, parent_stats)
        self.assertEqual(self.stats[-1]['no_m_suffixes'], 16)
        self.assertEqual(self.stats[-1]['complete_words_generated'], 44)
        self.assertEqual(self.stats[-1]['complete_words_never_generated'], 52)
        full, certificate, _ = compile_feature_family(
            self.ops, self.g, 4, feature_certificate=self.certificate, prune=False)
        self.assertEqual({word for word, _ in full}, {''.join(word) for word in plan_words(4)})
        self.assertEqual(len(full), 96)
        self.assertEqual(check_feature_family(certificate, self.ops, self.g, 4), full)
        for word, response in full:
            self.assertEqual(response, contrast_response(word_value(self.ops, word, self.g)))

    def test_zero_horizon_has_identity_and_one_maintenance(self):
        frontier, certificate, stats = compile_feature_family(self.ops, self.g, 0, prune=False)
        self.assertEqual([word for word, _ in frontier], ['', 'M'])
        self.assertEqual(check_feature_family(certificate, self.ops, self.g, 0), frontier)
        self.assertEqual(stats[0]['complete_words_generated'], 2)
        self.assertEqual(stats[0]['complete_words_never_generated'], 0)

    def test_feature_proof_rejects_false_identities_and_malformed_dimensions(self):
        mutations = []
        for path in (('C', 0, 0), ('T', 'D', 0, 0), ('T', 'R', 7, 7),
                     ('U', 0, 0), ('V', 2, 4), ('z', 0)):
            bad = deepcopy(self.certificate)
            target = bad
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = str(F(target[path[-1]])+1)
            mutations.append(bad)
        bad = deepcopy(self.certificate); bad['C'] = []; mutations.append(bad)
        bad = deepcopy(self.certificate); bad['T']['D'].pop(); mutations.append(bad)
        bad = deepcopy(self.certificate); bad['T']['R'][0].pop(); mutations.append(bad)
        bad = deepcopy(self.certificate); bad['U'] = []; mutations.append(bad)
        bad = deepcopy(self.certificate); bad['V'][0] = []; mutations.append(bad)
        bad = deepcopy(self.certificate); bad['z'].pop(); mutations.append(bad)
        bad = deepcopy(self.certificate); del bad['T']['R']; mutations.append(bad)
        bad = deepcopy(self.certificate); bad['unexpected'] = 1; mutations.append(bad)
        for value in (0.0, False, '0.0', '0/1', '1/0', None):
            bad = deepcopy(self.certificate); bad['U'][0][1] = value; mutations.append(bad)
        for index, bad in enumerate(mutations):
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                check_features(bad, self.ops, self.g)

    def test_feature_binding_covers_model_terminal_and_declared_basis(self):
        with self.assertRaises(ValueError):
            check_features(self.certificate, base_operators(F(0)), self.g)
        changed = list(self.g); changed[0] += F(1, 1000)
        with self.assertRaises(ValueError):
            check_features(self.certificate, self.ops, changed)
        bad = deepcopy(self.certificate); bad['binding'] = '0'*64
        with self.assertRaises(ValueError):
            check_features(bad, self.ops, self.g)
        bad = deepcopy(self.certificate); bad['schema'] += '.other'
        with self.assertRaises(ValueError):
            check_features(bad, self.ops, self.g)

    def test_input_numerics_and_dimensions_are_exact(self):
        for value in (0.0, False, '0.0', '0/1'):
            terminal = list(self.g); terminal[0] = value
            with self.subTest(terminal=value), self.assertRaises(ValueError):
                compile_features(self.ops, terminal)
        for value in (0.0, False, '0.0', '0/1', F(-1)):
            operators = deepcopy(self.ops); operators['D'][0][0] = value
            with self.subTest(probability=value), self.assertRaises(ValueError):
                compile_features(operators, self.g)
        malformed = []
        operators = deepcopy(self.ops); operators['D'][0][16] = F(0); malformed.append(operators)
        operators = deepcopy(self.ops); operators['D'][0][0] = F(2); malformed.append(operators)
        operators = deepcopy(self.ops); operators['D'] = operators['D'][:-1]; malformed.append(operators)
        operators = deepcopy(self.ops); del operators['M']; malformed.append(operators)
        for operators in malformed:
            with self.assertRaises(ValueError):
                compile_features(operators, self.g)
        with self.assertRaises(ValueError):
            compile_features(self.ops, self.g[:-1])

    def test_family_rejects_missing_or_invalid_cover_witnesses(self):
        mutations = []
        bad = deepcopy(self.family); bad['layers'] = []; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0] = {}; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0]['keep'] = []; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0]['cover'] = []; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0]['keep'] = [0, 0]; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0]['keep'][0] = False; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0]['cover'][0] = 99; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][0]['cover'][1] = 0; mutations.append(bad)
        bad = deepcopy(self.family); bad['layers'][-1]['cover'].pop(); mutations.append(bad)
        bad = deepcopy(self.family); bad['ordinary_updates'] = 4.0; mutations.append(bad)
        bad = deepcopy(self.family); bad['binding'] = '0'*64; mutations.append(bad)
        bad = deepcopy(self.family); bad['features']['V'][2][4] = '0'; mutations.append(bad)
        for index, bad in enumerate(mutations):
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                check_feature_family(bad, self.ops, self.g, 4)
        for k in (True, 4.0, -1, 3):
            with self.subTest(k=k), self.assertRaises(ValueError):
                check_feature_family(self.family, self.ops, self.g, k)
        with self.assertRaises(ValueError):
            compile_feature_family(self.ops, self.g, 4, prune=1)

    def test_unbounded_context_lineality_has_exact_spectral_witnesses(self):
        """Check the finite identities behind the all-horizon obstruction.

        Distinct R roots and the displayed eigenprojection give B2 R^n/h^n
        tending to v. D's health-Walsh blocks give B0 D^n/lambda^n -> 2w and
        v D^n/lambda^n -> beta*w, beta<0. Any closed invariant cone containing
        B therefore contains both signs of w and wR, spanning E_bad. Counts
        of finite-horizon response classes are separate enumeration evidence.
        """
        A = transports(self.ops)
        B = tuple(push(row, self.ops['M']) for row in CONTRAST_BASIS)
        a = A['R'][0][0]+A['R'][1][1]
        b = A['R'][2][2]+A['R'][3][3]
        h, lam = F(19, 20), F(24, 25)
        self.assertTrue(0 < b < a < h < lam < 1)
        v = push(B[2], self.ops['R'])
        v = tuple(x-a*y for x, y in zip(push(v, self.ops['R']), v))
        v = tuple(x-b*y for x, y in zip(push(v, self.ops['R']), v))
        v = tuple(x/(h*(h-a)*(h-b)) for x in v)
        self.assertEqual(push(v, self.ops['R']), tuple(h*x for x in v))
        # This identity also gives the square-free cyclic annihilator
        # B2 R(R-aI)(R-bI)(R-hI)=0, including the zero R eigenvalue.
        w = (F(0),)*8 + tuple(F(sum((-1)**bit for bit in bits), 8) for bits in BITS)
        self.assertEqual(push(w, self.ops['D']), tuple(lam*x for x in w))
        beta = F(-97789249826403799024011653198517846528,
                 736008414410103325506140176870361328125)
        self.assertLess(beta, 0)
        for row, coefficient in ((B[0], F(2)), (v, beta)):
            self.assertEqual(sum(row, F(0)), 0)
            for j in range(3):
                moment = sum((row[z*8+i]*((-1)**bits[j])
                              for z in (0, 1) for i, bits in enumerate(BITS)), F(0))
                self.assertEqual(moment, coefficient)
        # Prove the full D health-Walsh block formula, not just one trajectory.
        for mask in product((0, 1), repeat=3):
            subset = tuple(i for i, use in enumerate(mask) if use)
            row = tuple(F((-1)**sum(bits[j] for j in subset), 8) for bits in BITS)
            scale = lam**len(subset)
            self.assertEqual(push(row+(F(0),)*8, self.ops['D']),
                             tuple(scale*h*x for x in row)+tuple(scale*(1-h)*x for x in row))
            self.assertEqual(push((F(0),)*8+row, self.ops['D']),
                             (F(0),)*8+tuple(scale*x for x in row))
        lineality = ExactBasis(16)
        self.assertTrue(lineality.add(w))
        self.assertTrue(lineality.add(push(w, self.ops['R'])))
        for row in CONTRAST_BASIS[2:]:
            coefficients = lineality.coordinates(row)
            rebuilt = tuple(sum((coefficients[j]*basis_row[i]
                                 for j, basis_row in enumerate(lineality.originals)), F(0))
                            for i in range(16))
            self.assertEqual(row, rebuilt)


if __name__ == '__main__':
    unittest.main()
