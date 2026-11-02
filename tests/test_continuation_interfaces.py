"""Exact certificates: continuation value is not current-action equivalence."""
from fractions import Fraction as F
from itertools import product
import unittest
from cdka.composition import Contract
from cdka.continuation_interfaces import (
    Plan,plans,micro_alpha,score,upper_envelope,equal_signal_joint,
    weighted_table,partitions,evaluate_code,lossless_witness,best_code,
    exact_code_count,transported_code_value,regret_breakdown,update_witness,
)


class ContinuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=Contract();cls.lib=plans();cls.joint=equal_signal_joint()

    def test_all_64_plans_agree_with_raw_bit_oracle(self):
        self.assertEqual(len(self.lib),64)
        for pi in self.lib:self.assertEqual(pi.alpha,micro_alpha(self.p,pi))

    def test_exact_continuous_upper_hull(self):
        hull=upper_envelope(self.lib)
        self.assertEqual(tuple(i for _,_,i in hull),(50,58,42))
        self.assertEqual(hull[0][1],F(3734866303040,124585244227163))
        self.assertEqual(hull[1][1],F(106227674660136454136000,117936053240605881436351))
        for lo,hi,i in hull:
            # For every competing affine line, endpoints certify the entire interval.
            for j in range(len(self.lib)):
                self.assertGreaterEqual(score(self.lib[i],lo),score(self.lib[j],lo))
                self.assertGreaterEqual(score(self.lib[i],hi),score(self.lib[j],hi))
        for t in map(lambda i:F(i,200),range(201)):
            winners=[i for lo,hi,i in hull if lo<=t<=hi]
            self.assertEqual(max(score(self.lib[i],t) for i in winners),
                             max(score(pi,t) for pi in self.lib))

    def test_sensor_is_a_real_joint_distribution(self):
        self.assertEqual(sum((x[0] for x in self.joint),F(0)),F(1,2))
        self.assertEqual(sum((x[1] for x in self.joint),F(0)),F(1,2))
        for h in (0,1):self.assertEqual(sum((2*x[h] for x in self.joint),F(0)),1)
        self.assertTrue(all(sum(row,F(0))==F(1,3) for row in self.joint))

    def test_minimum_codes_one_and_two_decisions(self):
        self.assertEqual(exact_code_count(plans(horizon=1),self.joint),2)
        self.assertEqual(exact_code_count(self.lib,self.joint),3)
        r=best_code(self.lib,self.joint,2)
        self.assertEqual(r['labels'],(0,0,1))
        self.assertEqual(r['loss'],F(43924540239395040459,156250000000000000000000))

    def test_same_current_action_still_needs_two_continuations(self):
        low,medium=self.lib[50],self.lib[58]
        self.assertEqual(low.first,medium.first)
        self.assertEqual(low.first,'service')
        self.assertNotEqual(low.action_after((0,3)),medium.action_after((0,3)))
        w=lossless_witness(self.lib,self.joint,(0,0,1))
        self.assertFalse(w['lossless'])
        self.assertEqual(w['conflicting_cells'],{0:(0,1)})

    def test_independent_all_labeled_encoders(self):
        for tail in (F(0),F(1,100),F(3,20),F(1,2)):
            joint=equal_signal_joint(tail)
            for cap in (1,2,3):
                # All labeled encoders (including relabelings), not partition recursion.
                brute=max(evaluate_code(self.lib,joint,x)['value']
                          for x in product(range(cap),repeat=3))
                self.assertEqual(best_code(self.lib,joint,cap)['value'],brute)

    def test_no_loss_common_maximizer_equivalence(self):
        for tail in (F(0),F(1,100),F(3,20),F(1,2)):
            joint=equal_signal_joint(tail)
            for f in partitions(3):
                r=evaluate_code(self.lib,joint,f)
                self.assertEqual(r['loss']==0,lossless_witness(self.lib,joint,f)['lossless'])

    def test_horizon_does_not_monotonically_increase_optimal_code_count(self):
        joint=equal_signal_joint(F(3,20))
        self.assertEqual(exact_code_count(plans(horizon=1),joint),2)
        self.assertEqual(exact_code_count(self.lib,joint),1)

    def test_regret_identity_and_location_of_loss(self):
        for f in partitions(3):
            r=evaluate_code(self.lib,self.joint,f)
            d=regret_breakdown(self.p,self.lib,self.joint,r)
            self.assertEqual(d['total'],r['loss'])
            self.assertGreaterEqual(d['initial_action_loss'],0)
            self.assertGreaterEqual(d['continuation_loss'],0)
        best=best_code(self.lib,self.joint,2)
        self.assertEqual(regret_breakdown(self.p,self.lib,self.joint,best)['initial_action_loss'],0)

    def test_more_labels_never_reduce_value_with_unchanged_library(self):
        for tail in (F(0),F(1,100),F(1,10),F(3,20),F(1,2)):
            v=[best_code(self.lib,equal_signal_joint(tail),cap)['value'] for cap in (1,2,3)]
            self.assertTrue(v[0]<=v[1]<=v[2])

    def test_erasure_value_and_exact_sensitivity(self):
        f=(0,0,1);base=best_code(self.lib,self.joint,1)['value']
        v=evaluate_code(self.lib,self.joint,f)['value']
        for rho in (F(0),F(1,3),F(1)):
            self.assertEqual(transported_code_value(self.lib,self.joint,f,rho),(1-rho)*v+rho*base)
        left=transported_code_value(self.lib,self.joint,f,F(1,4))
        right=transported_code_value(self.lib,self.joint,f,F(1,4)+F(1,1000))
        self.assertEqual((right-left)*1000,base-v)

    def test_more_memory_does_not_create_a_forbidden_decoder(self):
        limited=tuple(pi for pi in self.lib if len({a for _,a in pi.second})==1)
        self.assertEqual(len(limited),16)
        self.assertLess(best_code(limited,self.joint,3)['value'],
                        best_code(self.lib,self.joint,3)['value'])
        self.assertEqual(best_code(limited,self.joint,3)['value'],
                         best_code(self.lib,self.joint,2)['value'])

    def test_recursive_update_cannot_recover_forgotten_history(self):
        cur={'low':0,'medium':0};nxt={'L':0,'M':1}
        edges=(('low','service','unanimous','L'),('medium','service','unanimous','M'))
        bad=update_witness(cur,nxt,edges)
        self.assertFalse(bad['realizable'])
        self.assertEqual(bad['required_outputs'],(0,1))
        cur={'low':0,'medium':1}
        self.assertTrue(update_witness(cur,nxt,edges)['realizable'])
        measured=(('low','service',('unanimous','low'),'L'),
                  ('medium','service',('unanimous','medium'),'M'))
        self.assertTrue(update_witness({'low':0,'medium':0},nxt,measured)['realizable'])

    def test_unmodeled_side_channel_is_an_extra_physical_register(self):
        # Exposing the lost diagnostic Y at runtime defeats an alleged
        # one-code impossibility; the FULL cut then has three states.
        full=evaluate_code(self.lib,self.joint,('y0','y1','y2'))
        collapsed=evaluate_code(self.lib,self.joint,(0,0,0))
        self.assertGreater(full['value'],collapsed['value'])
        self.assertEqual(full['loss'],0)

    def test_zero_mass_is_not_a_required_distinction(self):
        joint=(self.joint[0],(F(0),F(0)),self.joint[2])
        self.assertEqual(exact_code_count(self.lib,joint),2)

    def test_invalid_inputs_and_partition_count(self):
        self.assertEqual(len(list(partitions(3))),5)
        with self.assertRaises(ValueError):equal_signal_joint(F(3,4))
        with self.assertRaises(ValueError):plans(horizon=3)
        with self.assertRaises(ValueError):best_code(self.lib,self.joint,0)
        with self.assertRaises(ValueError):transported_code_value(self.lib,self.joint,(0,0,1),2)
        with self.assertRaises(ValueError):weighted_table(self.lib,[(F(1),F(1))])


if __name__=='__main__':unittest.main()
