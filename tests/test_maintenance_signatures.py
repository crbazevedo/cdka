"""Adversarial certificate checks and bounded-grammar cross-validation."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from cdka.maintenance_access import base_operators,base_probes,contract,witness_laws
from cdka.maintenance_signatures import (
    compile_one_maintenance,verify_one_maintenance,finite_horizon,
    verify_finite_horizon,signature,separator,
)
from cdka.semantic_closure import ExactBasis,word_value,dot


class MaintenanceSignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops=base_operators();cls.old={k:cls.ops[k] for k in ('D','R')}
        cls.p=base_probes();cls.meta=contract()
        cls.c=compile_one_maintenance(cls.old,cls.ops['M'],cls.p,contract=cls.meta)
        cls.f=finite_horizon(cls.old,cls.ops['M'],cls.p,max_updates=2,contract=cls.meta)

    def check(self,c):
        return verify_one_maintenance(c,self.old,self.ops['M'],self.p,contract=self.meta)

    def test_portable_certificate_checks_without_a_discovery_engine(self):
        portable=json.loads(json.dumps(self.c))
        with patch('cdka.maintenance_signatures.close_continuations',side_effect=AssertionError('search forbidden')), \
             patch('cdka.maintenance_signatures.ExactBasis',side_effect=AssertionError('basis search forbidden')):
            self.assertTrue(self.check(portable))
            self.assertTrue(verify_finite_horizon(self.f,self.old,self.ops['M'],self.p,contract=self.meta))

    def test_generator_certificate_is_identical_with_assertions_disabled(self):
        script = '''
import json
import sys
from cdka.maintenance_access import base_operators, base_probes, contract, witness_laws
from cdka.maintenance_signatures import compile_one_maintenance, verify_one_maintenance, separator
ops = base_operators()
old = {k: ops[k] for k in ('D', 'R')}
probes, scope = base_probes(), contract()
certificate = compile_one_maintenance(old, ops['M'], probes, contract=scope)
verified = verify_one_maintenance(certificate, old, ops['M'], probes, contract=scope)
print(json.dumps({'optimization': sys.flags.optimize, 'certificate': certificate,
                  'verified': verified, 'separator': separator(certificate, *witness_laws())}))
'''
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        for level, flags in ((0, ()), (1, ('-O',))):
            with self.subTest(optimization=level):
                result = subprocess.run(
                    [sys.executable, '-S', *flags, '-c', script],
                    cwd=Path(__file__).resolve().parents[1], env=env,
                    capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload['optimization'], level)
                self.assertTrue(payload['verified'])
                self.assertEqual(payload['certificate'], self.c)
                self.assertEqual(payload['separator']['word'], ['M'])

    def test_rank_lower_bound_and_operator_certificate_reject_tampering(self):
        corruptions=[]
        c=deepcopy(self.c);c['with_maintenance']['basis'][0][0]='123';corruptions.append(c)
        c=deepcopy(self.c);c['with_maintenance']['rank_certificate']['inverse_minor'][0][0]='123';corruptions.append(c)
        c=deepcopy(self.c);c['maintenance_image'][0][0]='123';corruptions.append(c)
        c=deepcopy(self.c);c['old_embedding'][0][0]='123';corruptions.append(c)
        c=deepcopy(self.c);c['old']['old_operator_coordinates']['D'][0][0]='123';corruptions.append(c)
        for c in corruptions:
            with self.assertRaises(ValueError):self.check(c)

    def test_scope_and_physical_kernel_are_part_of_the_binding(self):
        meta=deepcopy(self.meta);meta['readable'].append('hidden health')
        with self.assertRaises(ValueError):
            verify_one_maintenance(self.c,self.old,self.ops['M'],self.p,contract=meta)
        different=base_operators(F(1))
        with self.assertRaises(ValueError):
            verify_one_maintenance(self.c,self.old,different['M'],self.p,contract=contract(F(1)))

    def test_one_call_words_and_two_new_coordinates_are_attained(self):
        self.assertEqual((self.c['old']['dimension'],self.c['with_maintenance']['dimension']),(10,12))
        self.assertTrue(all(x['word'].count('M')<=1 for x in self.c['with_maintenance']['witnesses']))
        a,b=witness_laws()
        self.assertEqual(signature(self.c,a,layer='old'),signature(self.c,b,layer='old'))
        sep=separator(self.c,a,b)
        self.assertEqual(sep['word'],['M'])
        self.assertNotEqual(sep['left'],sep['right'])

    def test_bounded_grammar_matches_all_words_without_counting_M_as_D_or_R(self):
        for h in range(3):
            for permission in (0,1):
                basis=ExactBasis(16)
                for n in range(h+1):
                    for word in product(('D','R'),repeat=n):
                        candidates=[word]
                        if permission:
                            candidates += [word[:k]+('M',)+word[k:] for k in range(n+1)]
                        for w in candidates:
                            for v in self.p.values():basis.add(word_value(self.ops,w,v))
                self.assertEqual(len(basis.originals),self.f['layers'][f'{h}:{permission}']['dimension'])
        self.assertEqual(self.f['layers']['2:0']['dimension'],7)
        self.assertEqual(self.f['layers']['2:1']['dimension'],12)

    def test_finite_checker_rejects_missing_layer_and_extra_paid_call(self):
        c=deepcopy(self.f);del c['layers']['1:0']
        with self.assertRaises(ValueError):verify_finite_horizon(c,self.old,self.ops['M'],self.p,contract=self.meta)
        c=deepcopy(self.c);c['with_maintenance']['witnesses'][-1]['word']=['M','M']
        with self.assertRaises(ValueError):self.check(c)

    def test_zero_success_preserves_old_space_and_kernel_is_affine(self):
        zero=base_operators(F(0));one=base_operators(F(1))
        c=compile_one_maintenance(self.old,zero['M'],self.p,contract=contract(F(0)))
        self.assertEqual(c['with_maintenance']['dimension'],10)
        self.assertTrue(verify_one_maintenance(c,self.old,zero['M'],self.p,contract=contract(F(0))))
        for s in (F(1,10),F(4,5)):
            q=base_operators(s)['M']
            for i in range(16):
                for j in range(16):
                    self.assertEqual(q[i].get(j,F(0)),zero['M'][i].get(j,F(0))+s*(one['M'][i].get(j,F(0))-zero['M'][i].get(j,F(0))))

    def test_pair_midpoint_attains_the_bounded_minimax_prediction_error(self):
        a,b=witness_laws();mid=tuple((x+y)/2 for x,y in zip(a,b))
        largest=F(0)
        for n in range(3):
            for word in product(('D','R'),repeat=n):
                for k in range(n+1):
                    w=word[:k]+('M',)+word[k:];v=word_value(self.ops,w,self.p['readout'])
                    x,y,z=dot(a,v),dot(b,v),dot(mid,v)
                    self.assertEqual(abs(x-z),abs(y-z));self.assertEqual(abs(x-z),abs(x-y)/2)
                    largest=max(largest,abs(x-y))
        v=word_value(self.ops,('M',),self.p['readout'])
        self.assertEqual(largest,abs(dot(a,v)-dot(b,v)))


if __name__=='__main__':unittest.main()
