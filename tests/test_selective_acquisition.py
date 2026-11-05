from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import unittest
from cdka.selective_acquisition import *
from cdka.recurrent_maintenance import policies,physical_row

class SelectiveAcquisitionTests(unittest.TestCase):
    p=Model()
    def test_frozen_kernel(self):
        b=Path('cdka/recurrent_maintenance.py').read_bytes()
        self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'0a01bbf40f78f314a56285c15822e7ac06c9848b')
    def test_full_library(self):
        entries,stats=library()
        self.assertEqual([s['netlists'] for s in stats],[4,10,50])
        self.assertEqual([s['channels'] for s in stats],[4,5,12])
        self.assertEqual(len(entries),21)
        for c in entries:
            for x in CONTEXTS:self.assertIn(c.run(*x,(0,)*c.cost),(0,1))
    def test_fresh_matches_original_all_rows(self):
        for pol in policies():
            Q=exact_kernel(self.p,pol,(F(1),)*4)[0]
            for s in self.p.microstates():
                a={}
                for t,w in physical_row(self.p,pol,s).items():
                    j=IX[projection(t)];a[j]=a.get(j,F(0))+w
                self.assertEqual(a,Q[IX[projection(s)]])
    def test_independent_raw_gate_and_cell_rows(self):
        count=0
        for c,g in ((FRESH,F(0)),(ELIDE,F(0)),(ELIDE,F(1,100)),(Enable(((2,3),(1,4)),5),F(1,10))):
            Q=exact_kernel(self.p,Policy(),c.probabilities(g))[0]
            for s in self.p.microstates():
                agg={}
                for t,w in raw_row(self.p,Policy(),c,g,s).items():
                    j=IX[projection(t)];agg[j]=agg.get(j,F(0))+w
                self.assertEqual(agg,Q[IX[projection(s)]]);count+=1
        self.assertEqual(count,256)
    def test_annihilation_uniform_over_routing(self):
        for pol in policies():self.assertEqual(annihilation_certificate(self.p,pol),96)
    def test_exact_preservation_all_initial_contexts_checked_horizons(self):
        for prior in (F(0),F(1,2),F(1)):
            for n in (0,1,2,4,8):
                a=evaluate(FRESH,horizon=n,prior=prior);b=evaluate(ELIDE,horizon=n,prior=prior)
                self.assertEqual(a['survival'],b['survival'])
                self.assertEqual(a['services'],b['services'])
                self.assertLessEqual(b['writes'],a['writes'])
    def test_point_exact_synthesis(self):
        for g,eps,expected_gates in ((F(0),F(0),1),(F(1,100),F(1,10000),0),(F(1,100),F(1,1000),1)):
            rows=[]
            for pol in policies():rows.extend(dict(r,policy=pol.name) for r in ranking(gamma=g,policy=pol))
            baseline=evaluate(FRESH)['survival'];best=min((r for r in rows if r['survival']>=baseline-eps),key=total_cost)
            self.assertEqual(best['gates'],expected_gates)
            self.assertEqual(best['policy'],'vote/vote')
            self.assertEqual(max(r['survival'] for r in rows),baseline)
    def test_cost_threshold_not_automatic_savings(self):
        a=evaluate(FRESH);b=evaluate(ELIDE)
        critical=(a['writes']-b['writes']-F(1,10))/b['gate_executions']
        self.assertAlmostEqual(float(critical),.07886470562996192,14)
        self.assertLess(total_cost(b,gate_price=F(1,100)),total_cost(a,gate_price=F(1,100)))
        self.assertGreater(total_cost(b,gate_price=F(1,10)),total_cost(a,gate_price=F(1,10)))
    def test_exact_polynomials(self):
        poly=elision_polynomials()
        for g in (F(0),F(1,200),F(1,100),F(1,20),F(1,2)):
            value=evaluate(ELIDE,g)
            self.assertEqual(poly_eval(poly['survival'],g),value['survival'])
            self.assertEqual(poly_eval(poly['writes'],g),value['writes'])
            self.assertEqual(poly_eval(poly['events'],g),value['successful_epochs'])
    def test_certified_noise_threshold(self):
        c=noise_certificate();lo,hi=c['threshold']
        self.assertLessEqual(poly_eval(c['loss'],lo),c['tolerance'])
        self.assertGreater(poly_eval(c['loss'],hi),c['tolerance'])
        self.assertLess(hi-lo,F(1,10**20))
        self.assertGreater(min(c['derivative_bernstein']),0)
    def test_fault_direction_and_last_update(self):
        s=localized_gate_sensitivity()
        self.assertEqual(sum((r['by_input'][3] for r in s),F(0)),0)
        self.assertEqual(s[-1]['sum'],0)
        self.assertEqual(sum((r['sum'] for r in s),F(0)),elision_polynomials()['survival'][1])
    def test_safe_direction_errors_only_do_extra_work(self):
        Q=exact_kernel(self.p,Policy(),(F(1),)*4)[0]
        for gamma in (F(0),F(1,100),F(1,2),F(1)):
            T=safe_extra_write_kernel(self.p,Policy(),gamma)
            for a,b in zip(Q,T):
                d={k:b.get(k,F(0))-a.get(k,F(0)) for k in a.keys()|b.keys()}
                self.assertEqual(sum(d.values(),F(0)),0)
                composed={}
                for k,w in d.items():
                    for j,v in Q[k].items():composed[j]=composed.get(j,F(0))+w*v
                self.assertFalse(any(composed.values()))
    def test_noisy_savings_decomposition(self):
        a=evaluate(FRESH);b=evaluate(ELIDE,F(1,100))
        omissions=1+b['successful_epochs']-b['writes']
        lost_tasks=a['successful_epochs']-b['successful_epochs']
        self.assertEqual(a['writes']-b['writes'],omissions+lost_tasks)
        self.assertGreater(lost_tasks,0)
    def test_horizon_zero_and_exact_backward_reference(self):
        out=evaluate(ELIDE,horizon=0)
        self.assertEqual(out['survival'],1);self.assertEqual(out['writes'],1)
        self.assertEqual(out['gate_executions'],0)
        for c in library(1)[0]:
            q=exact_kernel(self.p,Policy(),c.probabilities(F(1,100)))[0]
            v=[F(1)]*48
            for _ in range(3):v=[sum((w*v[j] for j,w in row.items()),F(0)) for row in q]
            self.assertEqual(sum((a*b for a,b in zip(initial_vector(self.p),v)),F(0)),evaluate(c,F(1,100),3)['survival'])
    def test_resource_refund_is_a_different_contract(self):
        base=evaluate(FRESH)['survival']
        self.assertEqual(refunded_evaluate(0),base)
        self.assertNotEqual(refunded_evaluate(1),base)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):Enable(((4,4),),4)
        with self.assertRaises(ValueError):ELIDE.probabilities(F(3,4))
        with self.assertRaises(ValueError):library(3)
        with self.assertRaises(ValueError):evaluate(ELIDE,horizon=-1)

if __name__=='__main__':unittest.main()
