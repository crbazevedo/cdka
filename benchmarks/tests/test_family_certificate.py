from fractions import Fraction as F
from itertools import product
import unittest
import numpy as np
from cdka.family_certificate import *

class FamilyCertificateTests(unittest.TestCase):
    def test_small_complete_stationary_oracle(self):
        checks=0
        for n in (4,6,8):
            for seed in (7,23,71):
                rows,m=workflow_family(n,seed);c=compile_family(rows)
                for h in (0,1,2,4):
                    lo,hi=independent_enumeration(rows,h)
                    self.assertEqual(lo,hi);self.assertEqual(lo,c.values_exact(h));checks+=1
        self.assertEqual(checks,36)
    def test_arbitrary_adaptive_bellman_exact(self):
        for seed in (1,7,23,71):
            rows,_=workflow_family(12,seed);c=compile_family(rows)
            lo=hi=(F(1),)*12
            for h in range(8):
                self.assertEqual(lo,c.values_exact(h));self.assertEqual(hi,lo)
                lo=tuple(min(sum((p*lo[j] for j,p in r.items()),F(0)) for r in opts) for opts in rows)
                hi=tuple(max(sum((p*hi[j] for j,p in r.items()),F(0)) for r in opts) for opts in rows)
    def test_rank_two_does_not_need_equal_states(self):
        for n in (16,64,256):
            rows,m=workflow_family(n);c=compile_family(rows)
            self.assertEqual(c.rank,2);self.assertEqual(len(set(m['q'])),n)
            for h in (1,2,5):
                self.assertEqual(c.values_exact(h),tuple(q*m['r']**(h-1) for q in m['q']))
    def test_same_immediate_survival_but_different_future(self):
        rows,_=workflow_family(12,perturb=True);w=compile_family(rows)
        self.assertEqual(w['reason'],'separating_row');self.assertEqual(w['total_horizon'],2)
        self.assertEqual(sum(rows[0][0].values()),sum(rows[0][1].values()))
        self.assertNotEqual(F(w['difference']),0)
    def test_new_observable_requires_new_certificate(self):
        rows,_=workflow_family(8);c=compile_family(rows)
        self.assertIsInstance(c,Certificate)
        seen=[]
        for j in range(8):
            w=compile_family(rows,[int(i==j) for i in range(8)])
            seen.append(isinstance(w,dict) and w['reason']=='separating_row')
        self.assertTrue(any(seen))
    def test_full_rank_chain_and_limit_are_not_equivalence(self):
        n=10;rows=tuple((({i+1:F(1)} if i<n-1 else {}),) for i in range(n))
        c=compile_family(rows);self.assertEqual(c.rank,n)
        w=compile_family(rows,max_rank=3);self.assertEqual(w['reason'],'rank_limit')
    def test_common_matrix_coordinate_certificate(self):
        rows,_=workflow_family(20);c=compile_family(rows)
        for i,opts in enumerate(rows):
            for row in opts:
                for j,v in enumerate(c.basis):
                    expected=sum((c.basis[k][i]*c.transition[k][j] for k in range(c.rank)),F(0))
                    self.assertEqual(sum((p*v[t] for t,p in row.items()),F(0)),expected)
    def test_original_cdka_case(self):
        rows,m=cdka_elision_family();c=compile_family(rows)
        self.assertEqual(m['variable_rows'],12);self.assertEqual(c.rank,7)
        lo=hi=(F(1),)*48
        for h in range(5):
            self.assertEqual(lo,hi);self.assertEqual(lo,c.values_exact(h))
            lo=tuple(min(sum((p*lo[j] for j,p in r.items()),F(0)) for r in opts) for opts in rows)
            hi=tuple(max(sum((p*hi[j] for j,p in r.items()),F(0)) for r in opts) for opts in rows)
    def test_numerical_long_horizon_accuracy(self):
        rows,m=workflow_family(32);c=compile_family(rows)
        for h in (100,10000,1000000):
            expected=np.array([float(q)*float(m['r'])**(h-1) for q in m['q']])
            self.assertLess(np.max(np.abs(c.values_float(h)-expected)),1e-8)
    def test_invalid_models(self):
        for rows in ((),((),),(({0:F(2)},),),(({0:F(-1)},),),(({1:F(1)},),)):
            with self.assertRaises(ValueError):compile_family(rows)
    def test_sparse_baseline_matches_all_states(self):
        rows,_=workflow_family(32);c=compile_family(rows)
        lo,hi=bellman(sparse_family(rows),123)
        np.testing.assert_allclose(lo,hi,atol=1e-12);np.testing.assert_allclose(lo,c.values_float(123),atol=1e-12)
    def test_permutation_does_not_affect_rank(self):
        for seed in range(20):
            rows,_=workflow_family(16,seed);self.assertEqual(compile_family(rows).rank,2)

if __name__=='__main__':unittest.main()
