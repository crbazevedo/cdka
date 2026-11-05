"""Exact independently checked kernels, interface witness and program rankings."""
import unittest
import hashlib
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from cdka.recurrent_maintenance import (Model,Policy,policies,physical_row as old_row,
    forward as old_forward,emission,report_probability,task_success,initial_micro,push)
from cdka.memory_renewal import *


class RenewalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=Model()
        cls.ranking=ranking(cls.p,8)

    def test_preserves_source_v16(self):
        b=Path('cdka/recurrent_maintenance.py').read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        self.assertEqual(actual,'0a01bbf40f78f314a56285c15822e7ac06c9848b')

    def test_same_physical_resource_contract(self):
        for prog in programs():
            for state in self.p.microstates():
                q=row(self.p,prog,state)
                self.assertLessEqual(sum(q.values(),F(0)),1)
                z,m,b=state
                self.assertTrue(all(t[2] in {min(4,b+1),b-1} for t in q))
                self.assertTrue(all(1<=t[2]<=4 for t in q))
                if b<3:self.assertTrue(all(t[2]==b+1 for t in q))

    def test_always_refresh_matches_entire_old_kernel(self):
        for policy in policies():
            for state in self.p.microstates():
                self.assertEqual(row(self.p,Program(policy,'renew'),state),old_row(self.p,policy,state))

    def test_all_4096_micro_quotient_rows(self):
        checked=0
        for prog in programs():
            for state in self.p.microstates():
                self.assertEqual(aggregate(row(self.p,prog,state)),quotient_row(self.p,prog,macro(state)))
                checked+=1
        self.assertEqual(checked,4096)

    def test_independent_raw_fault_and_sensor_oracle_64_rows(self):
        checked=0
        for acq in ACQUISITIONS:
            for z,bits,b in product((0,1),((0,0,0),(0,1,1),(1,0,1),(1,1,1)),(2,3)):
                pr=Program(Policy(),acq);state=(z,bits,b)
                self.assertEqual(row(self.p,pr,state),oracle_row(self.p,pr,state));checked+=1
        self.assertEqual(checked,64)

    def test_forward_and_quotient_repeated_cycles(self):
        for acq in ACQUISITIONS:
            pr=Program(Policy(),acq)
            values,law=forward(self.p,pr,5,micro=True)
            reduced,r_law=forward(self.p,pr,5)
            self.assertEqual(values,reduced)
            self.assertEqual(aggregate(law),r_law)

    def test_backward_forward_exact_rank_oracle(self):
        for result in self.ranking:
            pr=result['program']
            self.assertEqual(result['value'],forward(self.p,pr,8)[0][-1])

    def test_projection_cannot_be_reused_for_retention(self):
        actual,projected=stale_projection_row(self.p,Policy(),(0,0,3))
        self.assertNotEqual(actual,projected)
        w=symmetry_defect(self.p)
        self.assertEqual(w['retained_difference'],w['formula'])
        self.assertNotEqual(w['retained_difference'],0)
        self.assertEqual(w['fresh_difference'],0)

    def test_selection_changes_memory_distribution_without_drift(self):
        p=Model(degradation=F(0))
        w=symmetry_defect(p)
        self.assertNotEqual(w['retained_difference'],0)
        for source in (0,1):
            self.assertEqual(report_probability((0,1,1),source,p.diagnostic_error),
                             report_probability((1,0,1),source,p.diagnostic_error))

    def test_exact_symmetric_defect_at_three_gate_rates(self):
        for rate in (F(0),F(1,1000),F(1,100)):
            p=Model(healthy_error=rate)
            w=symmetry_defect(p)
            self.assertEqual(w['retained_difference'],w['formula'])
            self.assertEqual(w['retained_difference']==0,rate==0)

    def test_ideal_retention_does_not_create_bit_changes(self):
        pr=Program(Policy(),'retain')
        for state in self.p.microstates():
            self.assertTrue(all(t[1]==state[1] for t in row(self.p,pr,state)))

    def test_program_rank_and_reoptimized_subfamilies(self):
        self.assertEqual(len(self.ranking),64)
        self.assertEqual(self.ranking[0]['program'],Program(Policy(),'renew'))
        best={a:max((r for r in self.ranking if r['program'].acquisition==a),key=lambda r:r['value']) for a in ACQUISITIONS}
        self.assertGreater(best['renew']['value'],best['after_skip']['value'])
        self.assertGreater(best['after_skip']['value'],best['after_service']['value'])
        self.assertGreater(best['after_service']['value'],best['retain']['value'])
        self.assertEqual(best['retain']['value'],old_forward(self.p,Policy('service','service'),8)[0][-1])

    def test_timing_matters_in_fixed_controller(self):
        vals={a:forward(self.p,Program(Policy(),a),8)[0][-1] for a in ACQUISITIONS}
        self.assertGreater(vals['renew'],vals['after_skip'])
        self.assertGreater(vals['after_skip'],vals['retain'])
        self.assertGreater(vals['retain'],vals['after_service'])

    def test_blind_program_value_ignores_memory_update(self):
        for a,b in product(('skip','service'),repeat=2):
            pr=Policy(a,b)
            values=[forward(self.p,Program(pr,acq),5)[0][-1] for acq in ACQUISITIONS]
            self.assertEqual(len(set(values)),1)

    def test_more_stored_correctness_not_uniform_value_order(self):
        vals=[forward(self.p,Program(Policy(),a),1)[0][-1] for a in ACQUISITIONS]
        self.assertEqual(len(set(vals)),1)

    def test_initial_law_and_final_observation_are_not_free_information(self):
        initial=initial_micro(self.p)
        self.assertEqual(sum(initial.values(),F(0)),1)
        for b in range(1,5):
            vals={prog.routing.mode(b) for prog in programs()}
            if b<3:self.assertEqual(vals,{'skip'})
            else:self.assertEqual(vals,{'skip','service','vote','inverse'})
        self.assertEqual(Program(acquisition='after_service').refresh(1),True)
        self.assertEqual(Program(acquisition='after_service').refresh(0),False)

    def test_uniform_hazard_and_no_survivor_normalization(self):
        ceiling=task_success(self.p,0)
        for acq in ACQUISITIONS:
            curve=forward(self.p,Program(Policy(),acq),8)[0]
            self.assertTrue(all(x>=y for x,y in zip(curve,curve[1:])))
            for n,value in enumerate(curve):self.assertLessEqual(value,ceiling**n)

    def test_support_failure_even_with_perfect_selector_and_static_health(self):
        p=Model(healthy_error=F(0),degradation=F(0))
        law=push(emission(p,(0,0,3)),lambda s:row(p,Program(Policy(),'retain'),s))
        self.assertGreater(law.get((0,(0,0,0),4),F(0)),0)
        self.assertTrue(all(law.get((0,m,4),F(0))==0 for m in BITS if sum(m)>=2))
        for v in (0,1):
            self.assertTrue(all(report_probability(m,v,p.diagnostic_error)>0 for m in BITS))

    def test_telescoping_trace_is_exact_and_terminal_update_has_zero_value(self):
        for a,b in (("renew","retain"),("after_skip","after_service")):
            left,right=Program(Policy(),a),Program(Policy(),b)
            pieces=difference_trace(self.p,left,right,8)
            self.assertEqual(sum(pieces),forward(self.p,left,8)[0][-1]-forward(self.p,right,8)[0][-1])
            self.assertEqual(pieces[-1],0)

    def test_invalid_programs_and_states(self):
        with self.assertRaises(ValueError):Program(acquisition='know_health')
        with self.assertRaises(ValueError):forward(self.p,Program(),-1)
        with self.assertRaises(ValueError):row(self.p,Program(),(0,(0,0,0),0))
        with self.assertRaises(ValueError):quotient_row(self.p,Program(),(0,0,3,3))

if __name__=='__main__':unittest.main()
