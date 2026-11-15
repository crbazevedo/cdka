"""End-to-end boundaries: neither side of a common decision may lose coverage."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

from cdka.maintenance_access import base_operators, base_probes
from cdka.preparation_decisions import joint_gate, query_informed
from cdka.preparation_pipeline import compile_task, check_task
from cdka.reachable_diagnosis import acquisition


class CoveredDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops = base_operators()
        cls.g = base_probes()['readout']
        cls.law = acquisition()
        cls.scope = {'fixture': 'common-physical-plan', 'allowed_work': '4DR+optionalM'}
        fixture = Path(__file__).parent / 'fixtures/preparation-families-small.json'
        cls.hull = json.loads(fixture.read_text())
        cls.candidate, cls.stats = compile_task(
            cls.ops, cls.g, cls.law, 4, 4, contract=cls.scope,
            preparation_certificate=cls.hull)

    def check(self, certificate, h=4, k=4, **kwargs):
        return check_task(certificate, kwargs.pop('operators', self.ops),
                          kwargs.pop('terminal', self.g), kwargs.pop('initial_law', self.law),
                          h, k, contract=kwargs.pop('contract', self.scope), **kwargs)

    def test_compact_decisions_equal_streaming_after_serialization(self):
        checked = self.check(json.loads(json.dumps(self.candidate)))
        baseline, _ = compile_task(self.ops, self.g, self.law, 4, 4,
                                   contract=self.scope, preparation_method='stream')
        self.check(baseline)
        keys = ('plans', 'worst_regrets', 'minimum_fidelities', 'minimax_plan',
                'minimax_regret', 'maximin_plan', 'maximin_fidelity')
        for key in keys:
            self.assertEqual(self.candidate['decision'][key], baseline['decision'][key], key)
        self.assertEqual(len(checked['preparations']), 13)
        self.assertEqual(self.stats['decision']['values_evaluated'], 130)
        for delta, floor in ((F(3, 1000), F(17, 20)), (F(1, 100), F(4, 5))):
            self.assertEqual(joint_gate(self.candidate['decision'], delta, floor),
                             joint_gate(baseline['decision'], delta, floor))
        self.assertEqual(query_informed(checked['problem'], 'RDDR')['history'], 'RDDR')

    def test_pipeline_rejects_unproved_subsets_and_missing_certificate_structure(self):
        mutations = []
        for field in ('program_certificate', 'preparation_certificate', 'decision'):
            c = deepcopy(self.candidate); c[field] = None; mutations.append(c)
        c = deepcopy(self.candidate); c['preparation_certificate']['layers'].pop(); mutations.append(c)
        c = deepcopy(self.candidate); c['program_certificate']['layers'].pop(); mutations.append(c)
        c = deepcopy(self.candidate); c['preparation_certificate']['layers'][4]['cover'].pop(); mutations.append(c)
        c = deepcopy(self.candidate); c['decision']['regret_attainers'].pop(); mutations.append(c)
        c = deepcopy(self.candidate); c['decision']['minimum_fidelities'][0] = '1'; mutations.append(c)
        c = deepcopy(self.candidate); c['preparation_method'] = 'stream'; mutations.append(c)
        c = deepcopy(self.candidate); c['ordinary_continuation_updates'] = True; mutations.append(c)
        c = deepcopy(self.candidate); c['extra'] = 'unbound'; mutations.append(c)
        for i, c in enumerate(mutations):
            with self.subTest(attack=i), self.assertRaises(ValueError):
                self.check(c)
        with self.assertRaises(ValueError):
            compile_task(self.ops, self.g, self.law, 4, 4,
                         preparation_method='stream', preparation_certificate=self.hull)

    def test_composed_binding_covers_physical_law_observable_workload_and_contract(self):
        for kwargs in ({'h': 3}, {'k': 3}, {'initial_law': acquisition(F(1, 5))},
                       {'terminal': tuple(1-value for value in self.g)},
                       {'operators': base_operators(F(0))},
                       {'contract': {'allowed_work': 'different'}}):
            with self.subTest(change=kwargs), self.assertRaises(ValueError):
                self.check(self.candidate, **kwargs)

    def test_preparation_cover_reuses_across_continuation_but_decision_does_not(self):
        # The same checked D/R hull serves a new K and maintenance mechanism.
        changed = base_operators(F(0))
        candidate, _ = compile_task(changed, self.g, self.law, 4, 1,
                                    preparation_certificate=self.hull, contract=self.scope)
        result = check_task(candidate, changed, self.g, self.law, 4, 1, contract=self.scope)
        self.assertEqual(len(result['preparations']), 13)
        c = deepcopy(candidate); c['decision'] = self.candidate['decision']
        with self.assertRaises(ValueError):
            check_task(c, changed, self.g, self.law, 4, 1, contract=self.scope)


if __name__ == '__main__':
    unittest.main()
