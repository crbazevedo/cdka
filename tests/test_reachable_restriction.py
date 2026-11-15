import copy
import json
from fractions import Fraction as F
from pathlib import Path
import unittest
from unittest.mock import patch

from cdka.maintenance_access import base_operators, base_probes
from cdka.reachable_restriction import (
    ORBIT_LAWS, collapse, expand, is_exchangeable, orbit_response,
    domain_preservation, projected_kernel, compile_old_restriction,
    verify_old_restriction, restricted_signature, restricted_value, query_cache,
    contrast_signature, contrast_response, contrast_value, contrast_domain_preservation,
    compile_contrast_restriction, verify_contrast_restriction, CONTRAST_BASIS,
)
from cdka.semantic_closure import dot, word_value


class ReachableRestrictionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops = base_operators()
        cls.g = base_probes()['readout']
        p = Path(__file__).resolve().parents[1] / 'docs/data/maintenance-access-closed-certificate.json'
        cls.old = tuple(tuple(map(F, v)) for v in json.loads(p.read_text())['old']['basis'])

    def test_orbit_domain_is_identified_by_old_responses_with_independent_inverse_check(self):
        cert = compile_old_restriction(self.old, contract={'scope': 'input domain'})
        with patch('cdka.reachable_restriction._inverse', side_effect=AssertionError('discovery forbidden')):
            self.assertTrue(verify_old_restriction(cert, self.old, contract={'scope': 'input domain'}))
        for mutation in ('inverse', 'binding', 'old_indices'):
            bad = copy.deepcopy(cert)
            if mutation == 'inverse': bad['inverse'][0][0] = str(F(bad['inverse'][0][0])+1)
            elif mutation == 'binding': bad['binding'] = '0'*64
            else: bad['old_indices'][0] = bad['old_indices'][1]
            with self.assertRaises(ValueError): verify_old_restriction(bad, self.old, contract={'scope': 'input domain'})

    def test_domain_is_preserved_by_old_updates_but_not_maintenance(self):
        self.assertTrue(domain_preservation(self.ops['D'])['preserved'])
        self.assertTrue(domain_preservation(self.ops['R'])['preserved'])
        self.assertFalse(domain_preservation(self.ops['M'])['preserved'])
        self.assertTrue(domain_preservation(base_operators(F(0))['M'])['preserved'])

    def test_projection_is_valid_at_boundary_and_invalid_as_free_maintenance_quotient(self):
        words = [('M','R'), ('D','M','R'), ('R','M','D')]
        cached = query_cache(self.ops, self.g, words)
        projected = {k: projected_kernel(v) for k, v in self.ops.items()}
        wrong = [word_value(projected, w, orbit_response(self.g)) for w in words]
        self.assertTrue(any(a != b for a, b in zip(cached['restricted'], wrong)))
        for i, law in enumerate(ORBIT_LAWS):
            mu0 = tuple(F(0) for _ in law)
            sig = restricted_signature(mu0, law)
            for j, full in enumerate(cached['full']):
                self.assertEqual(restricted_value(sig, cached['restricted'][j]), dot(law, full))

    def test_signed_contrasts_and_domain_rejection(self):
        law = tuple(a/3-b/2 for a,b in zip(ORBIT_LAWS[1], ORBIT_LAWS[6]))
        self.assertTrue(is_exchangeable(law))
        self.assertEqual(expand(collapse(law)), law)
        raw = [F(0)]*16; raw[1] = F(1)
        self.assertFalse(is_exchangeable(raw))
        with self.assertRaises(ValueError): restricted_signature(raw, raw)

    def test_four_dimensional_contrast_domain_closes_before_maintenance(self):
        from cdka.reachable_diagnosis import preparation_laws
        for h in range(5):
            for law in preparation_laws(h).values():
                sig = contrast_signature(*law)
                for word in ((),('M',),('M','R'),('D','R','M')):
                    full = word_value(self.ops,word,self.g)
                    self.assertEqual(contrast_value(sig,contrast_response(full)),
                                     restricted_value(restricted_signature(*law),orbit_response(full)))
        self.assertTrue(contrast_domain_preservation(self.ops['D'])['preserved'])
        self.assertTrue(contrast_domain_preservation(self.ops['R'])['preserved'])
        self.assertFalse(contrast_domain_preservation(self.ops['M'])['preserved'])
        self.assertTrue(contrast_domain_preservation(base_operators(F(0))['M'])['preserved'])

    def test_old_responses_separate_the_four_contrast_coordinates(self):
        cert = compile_contrast_restriction(self.old,contract={'domain':'source contrast'})
        with patch('cdka.reachable_restriction._inverse',side_effect=AssertionError('discovery forbidden')):
            self.assertTrue(verify_contrast_restriction(cert,self.old,contract={'domain':'source contrast'}))
        bad = copy.deepcopy(cert);bad['inverse'][0][0]=str(F(bad['inverse'][0][0])+1)
        with self.assertRaises(ValueError):verify_contrast_restriction(bad,self.old,contract={'domain':'source contrast'})
        with self.assertRaises(ValueError):contrast_signature(ORBIT_LAWS[0],ORBIT_LAWS[4])


if __name__ == '__main__':
    unittest.main()
