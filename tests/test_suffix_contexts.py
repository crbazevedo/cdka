"""Independent physical and adversarial checks of the finite suffix cover."""
import builtins
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from cdka.maintenance_access import base_operators, base_probes
from cdka.program_families import compile_decision, dominated, evaluate_frontier
from cdka.reachable_diagnosis import plan_words, preparation_laws
from cdka.reachable_restriction import CONTRAST_BASIS, contrast_response, contrast_signature
from cdka.semantic_closure import apply, dot, push, word_value
from cdka.suffix_contexts import check_family, compile_family


FIXTURE = Path(__file__).with_name('fixtures') / 'suffix-contexts-k4.json'


class SuffixContextsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.operators = base_operators()
        cls.terminal = base_probes()['readout']
        cls.certificate = json.loads(FIXTURE.read_text())
        cls.frontier = check_family(cls.certificate, cls.operators, cls.terminal, 4)
        cls.physical = [(''.join(word), contrast_response(word_value(cls.operators, word, cls.terminal)))
                        for word in plan_words(4)]

    def test_frozen_certificate_checks_without_discovery_or_optional_imports(self):
        original_import = builtins.__import__

        def limited_import(name, *args, **kwargs):
            if name.split('.')[0] in {'numpy', 'scipy'}:
                raise AssertionError('optional numerical dependency forbidden in checker')
            return original_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=limited_import), \
                patch('cdka.suffix_contexts.discover_cone', side_effect=AssertionError('cone discovery')), \
                patch('cdka.suffix_contexts._cover', side_effect=AssertionError('Pareto discovery')), \
                patch('cdka.suffix_contexts.compile_features', side_effect=AssertionError('feature discovery')):
            checked = check_family(self.certificate, self.operators, self.terminal, 4)
        self.assertEqual(checked, self.frontier)

    def test_actual_representatives_cover_full_physical_programs(self):
        physical = dict(self.physical)
        for word, response in self.frontier:
            self.assertIn(word, physical)
            self.assertEqual(response, physical[word])
            self.assertEqual(sum(a in 'DR' for a in word), 4)
            self.assertLessEqual(word.count('M'), 1)
        for _, response in self.physical:
            self.assertTrue(any(dominated(other, response) for _, other in self.frontier))
        frontier, certificate, stats = compile_family(
            self.operators, self.terminal, 4,
            feature_certificate=self.certificate['features'],
            cone_certificate=self.certificate['cone'])
        self.assertEqual(frontier, self.frontier)
        self.assertEqual(check_family(certificate, self.operators, self.terminal, 4), frontier)
        last = stats['layers'][-1]
        self.assertEqual((last['no_m_suffix_candidates'], last['no_m_suffixes_retained']), (6, 4))
        self.assertEqual((last['complete_words_generated'], last['complete_words_never_generated']), (22, 74))
        self.assertEqual((last['candidates'], last['retained']), (22, 10))

    def test_suffix_representative_is_common_to_all_literal_residual_contexts(self):
        # Independent, small exhaustive control: use full16 rows and suffixes,
        # not the supplied feature/cone identities, and require one common
        # representative per discarded suffix across every residual context.
        suffix = [('', self.terminal)]
        boundary = tuple(push(row, self.operators['M']) for row in CONTRAST_BASIS)
        for n in range(1, 5):
            candidates = [(a + word, apply(self.operators[a], response))
                          for word, response in suffix for a in 'DR']
            suffix = [candidates[i] for i in self.certificate['layers'][n]['suffix']['keep']]
            contexts = list(CONTRAST_BASIS) + list(boundary)
            current = list(boundary)
            for _ in range(4 - n):
                current = [push(row, self.operators[a]) for row in current for a in 'DR']
                contexts.extend(current)
            for word in product('DR', repeat=n):
                response = word_value(self.operators, word, self.terminal)
                self.assertTrue(any(all(dot(row, representative) <= dot(row, response)
                                        for row in contexts) for _, representative in suffix), word)

    def test_common_decisions_and_joint_gate_match_full_library(self):
        preparations = preparation_laws(2)
        signatures = [contrast_signature(*law) for law in preparations.values()]
        results = []
        for entries in (self.physical, self.frontier):
            values = evaluate_frontier(entries, signatures)
            decision = compile_decision(values, preparation_labels=list(preparations),
                                        plan_labels=[word for word, _ in entries])
            best = tuple(map(F, decision['preparation_best']))
            feasible = any(max(b - row[j] for b, row in zip(best, values)) <= F(3, 1000)
                           and min(row[j] for row in values) >= F(17, 20)
                           for j in range(len(entries)))
            self.assertEqual(entries[decision['minimax_plan']][0], 'DRDDM')
            self.assertFalse(feasible)
            results.append((decision['preparation_best'], decision['minimax_regret'],
                            decision['maximin_fidelity'], feasible))
        self.assertEqual(results[0], results[1])

    def test_empty_cone_attack_is_rejected_before_vacuous_dominance(self):
        _, certificate, _ = compile_family(self.operators, self.terminal, 1, optimize=False)
        certificate['cone'] = {'rows': [], 'counts': [0], 'initial': [], 'transitions': []}
        with self.assertRaises(ValueError):
            check_family(certificate, self.operators, self.terminal, 1)
        # This was an actual unsound outcome of the earlier zip-truncation bug.
        omitted = contrast_response(word_value(self.operators, 'MR', self.terminal))
        bad_kept = [contrast_response(word_value(self.operators, word, self.terminal))
                    for word in ('D', 'R', 'DM', 'RM')]
        self.assertFalse(any(dominated(response, omitted) for response in bad_kept))

    def test_cone_parser_rejects_missing_future_negative_and_false_witnesses(self):
        mutations = []
        c = deepcopy(self.certificate); c['cone']['initial'].pop(); mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['initial'] = [[] for _ in range(8)]; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['transitions'].pop(); mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['counts'][1] = 1; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['counts'][0] = True; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['counts'][-1] -= 1; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['rows'][0].pop(); mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['rows'][0] = ['0'] * 8; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['initial'][0][0][0] = c['cone']['counts'][0]; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['transitions'][0]['D'][0][0] = c['cone']['counts'][1]; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['transitions'][0]['D'][0][1] = '-1'; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['transitions'][0]['D'][0][1] = '1/123'; mutations.append(c)
        c = deepcopy(self.certificate); c['cone']['initial'][0][0][0] = False; mutations.append(c)
        c = deepcopy(self.certificate); del c['cone']['transitions'][0]['R']; mutations.append(c)
        for value in (0.0, False, '0.0', '0/1', '1/0'):
            c = deepcopy(self.certificate); c['cone']['rows'][0][0] = value; mutations.append(c)
            c = deepcopy(self.certificate); c['cone']['initial'][0][0][1] = value; mutations.append(c)
        for c in mutations:
            with self.subTest(cone=c['cone']), self.assertRaises(ValueError):
                check_family(c, self.operators, self.terminal, 4)

    def test_cover_and_contract_tampering_is_rejected(self):
        mutations = []
        c = deepcopy(self.certificate); c['layers'].pop(); mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][0]['suffix']['keep'][0] = False; mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][0]['front']['cover'][1] = 0; mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][2]['suffix']['cover'].pop(); mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][2]['suffix']['keep'] = []; mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][2]['suffix']['keep'] = [0, 0]; mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][1]['suffix']['cover'][0] = 1; mutations.append(c)
        c = deepcopy(self.certificate); c['ordinary_updates'] = 4.0; mutations.append(c)
        c = deepcopy(self.certificate); c['binding'] = 'unbound'; mutations.append(c)
        c = deepcopy(self.certificate); c['features']['binding'] = 'unbound'; mutations.append(c)
        c = deepcopy(self.certificate); c['layers'][0] = None; mutations.append(c)
        c = deepcopy(self.certificate); c['extra_scope'] = 'ignored'; mutations.append(c)
        for c in mutations:
            with self.subTest(c=c), self.assertRaises(ValueError):
                check_family(c, self.operators, self.terminal, 4)
        for k in (True, -1, 4.0, 3):
            with self.subTest(k=k), self.assertRaises(ValueError):
                check_family(self.certificate, self.operators, self.terminal, k)
        with self.assertRaises(ValueError):
            check_family(self.certificate, base_operators(F(0)), self.terminal, 4)

    def test_boundary_horizons_and_zero_repair_use_standard_library_fallback(self):
        for repair in (F(0), F(2, 3)):
            operators = base_operators(repair)
            for k in (0, 1, 2):
                front, certificate, stats = compile_family(operators, self.terminal, k, optimize=False)
                self.assertEqual(check_family(certificate, operators, self.terminal, k), front)
                self.assertEqual(stats['cone']['lp_calls'], 0)
                for word in plan_words(k):
                    response = contrast_response(word_value(operators, word, self.terminal))
                    self.assertTrue(any(dominated(other, response) for _, other in front))


if __name__ == '__main__':
    unittest.main()
