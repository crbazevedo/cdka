from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from math import comb
import unittest
from cdka.composition import Contract,DEAD,macro_row,micro_row,quotient
from cdka.continuation_interfaces import plans,equal_signal_joint,best_code,regret_breakdown
from cdka.joint_compilation import evaluate_witness
from cdka.trace_microscope import (
    physical_events,step_branches,trace_program,trace_summary,endpoint_alias_witness,
    harmful_route_witness,suffix_conflict,semantic_distance,coupling_guard,terminal_law)

class TraceMicroscopeTests(unittest.TestCase):
    def test_local_raw_events_match_canonical_and_independent_kernel(self):
        p=Contract();count=0
        for s in p.states():
            for a in p.actions(s[2]):
                row=defaultdict(F)
                for x in step_branches(p,s,a):row[x.after]+=x.probability
                self.assertEqual(dict(row),macro_row(p,s,a))
                micro=(0,(0,0,0) if s[0]==0 else (1,0,0),s[1],s[2])
                independent=defaultdict(F)
                for z,q in micro_row(p,micro,a).items():independent[quotient(z)]+=q
                self.assertEqual(dict(row),dict(independent));count+=1
        self.assertEqual(count,60)

    def test_complete_tree_reproduces_outcomes(self):
        cases=0
        fixtures=[((0,0,3),(58,58,58,42)),((0,1,3),(58,58,58,42)),
                  ((0,1,3),(50,58,58,42)),((0,0,0),(48,48,48,48)),
                  ((0,0,0),(63,63,63,63))]
        for p in [F(0),F(1,100),F(1,10),F(1,5),F(1,2)]:
            for enc,dec in fixtures:
                ts=trace_program(enc,dec,p);s=trace_summary(ts)
                self.assertEqual(s['mass'],1)
                self.assertEqual(s['value'],evaluate_witness(enc,dec,p));cases+=1
        self.assertEqual(cases,25)

    def test_early_failures_have_no_fake_continuation(self):
        ts=trace_program((0,0,3),(58,58,58,42),F(1,10))
        for t in ts:
            if t['failed_epoch']==1:self.assertEqual(len(t['steps']),1)
            if t['outcome']=='failed':self.assertEqual(t['terminal'],DEAD)
        self.assertTrue(any(t['failed_epoch']==1 for t in ts))

    def test_hidden_health_is_not_an_input_to_policy(self):
        ts=trace_program((0,0,3),(58,58,58,42),F(1,10));mapping={}
        for t in ts:
            for phase,step in enumerate(t['steps']):
                k,hidden,b=step.before
                key=(phase,t['readable_word'],k,b)
                if key in mapping:self.assertEqual(mapping[key],step.action)
                mapping[key]=step.action

    def test_endpoint_alias_for_every_prior_in_fixture_grid(self):
        for prior in [F(0),F(1,100),F(1,2),F(99,100),F(1)]:
            r=endpoint_alias_witness(prior);a,b=r['rows']
            self.assertEqual(a['two_stage_survival'],b['two_stage_survival'])
            self.assertGreater(r['third_gain'],0)
            self.assertEqual(r['fixed_refresh_gain'],r['health_mass_gain']*r['health_payoff_gap'])
        fair=endpoint_alias_witness()
        self.assertEqual(fair['third_gain'],fair['fixed_refresh_gain'])
        for row in fair['rows']:self.assertEqual(set(row['third_policy'].values()),{'refresh'})
        low=endpoint_alias_witness(F(0))
        self.assertNotEqual(low['third_gain'],low['fixed_refresh_gain'])

    def test_terminal_distribution_is_sufficient_for_readable_extension(self):
        for plan in (48,63):
            ts=trace_program((0,0,0),(plan,)*4,F(0))
            self.assertEqual(trace_summary(ts)['terminal'],terminal_law(plan))

    def test_harmful_route_identity_on_exact_grid(self):
        for i in range(51):
            r=harmful_route_witness(F(i,100))
            self.assertEqual(sum(r['signed_health_contributions']),r['net_gain'])
            self.assertGreaterEqual(r['net_gain'],0)
        r=harmful_route_witness(F(1,10))
        self.assertEqual(r['injective_route'],F(9,100))
        self.assertEqual(r['merged_route'],F(1,100))
        self.assertLess(r['signed_health_contributions'][0],0)
        self.assertGreater(r['signed_health_contributions'][1],0)

    def test_regret_leading_order_by_polynomial_coefficients(self):
        count=0
        for a,b in product(range(3),repeat=2):
            vals=((F(a),F(b)),)
            for x in range(4):
                for dec in product(range(2),repeat=4):
                    r=semantic_distance((x,),dec,vals)[0]
                    poly=[F(0)]*3
                    for received in range(4):
                        gap=max(vals[0])-vals[0][dec[received]]
                        distance=(x^received).bit_count()
                        for j in range(3-distance):
                            poly[distance+j]+=gap*((-1)**j)*comb(2-distance,j)
                    first=next((j for j,v in enumerate(poly) if v),None)
                    self.assertEqual(r['distance'],first)
                    self.assertEqual(r['leading'],F(0) if first is None else poly[first]);count+=1
        self.assertEqual(count,576)

    def test_middle_signal_semantic_distance(self):
        p=plans(Contract());vals=((sum(p[58].alpha)/2,sum(p[42].alpha)/2),)
        dec=(0,0,0,1)
        self.assertEqual(semantic_distance((1,),dec,vals)[0]['distance'],1)
        self.assertEqual(semantic_distance((0,),dec,vals)[0]['distance'],2)

    def test_suffix_conflict_explains_all_v9_loss(self):
        r=suffix_conflict();self.assertEqual(r[0]['runtime_input'],r[1]['runtime_input'])
        self.assertNotEqual(r[0]['reference_next'],r[1]['reference_next'])
        lib=plans(Contract());joint=equal_signal_joint();code=best_code(lib,joint,2)
        b=regret_breakdown(Contract(),lib,joint,code)
        self.assertEqual(sum((x['deficit']for x in r),F(0)),b['total'])
        self.assertEqual(b['initial_action_loss'],0)

    def test_cross_world_coupling_is_not_identified_by_marginals(self):
        couplings=coupling_guard();rescue=[]
        for law in couplings.values():
            self.assertEqual(sum(law.values()),1)
            for coord in (0,1):self.assertEqual(sum(q for pair,q in law.items()if pair[coord]),F(4,5))
            rescue.append(law.get((0,1),F(0)))
        self.assertEqual(rescue,[F(0),F(1,5)])

    def test_invalid_program_rejected(self):
        with self.assertRaises(ValueError):trace_program((0,5,1),(58,)*4)
        with self.assertRaises(ValueError):trace_program((0,0,1),(999,)*4)
        with self.assertRaises(ValueError):harmful_route_witness(F(2,3))

if __name__=='__main__':unittest.main()
