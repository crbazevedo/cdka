from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest
from cdka.composition import (Contract,DEAD,COST,binom,tv,quotient,readable,
    macro_row,micro_row,aggregate,solve,evaluate,quotient_report,
    composition_bound,calibration_report,sensor_derivative_row,sensor_sensitivity)

class ComponentTests(unittest.TestCase):
    def test_all_raw_rows_equal_composed_rows(self):
        self.assertEqual(quotient_report(Contract()),dict(micro_states=80,macro_states=20,rows_checked=240,max_tv=F(0)))

    def test_observable_statistic_not_a_hidden_state_oracle(self):
        for state in Contract().micros(): self.assertEqual(readable(state),quotient(state))
        with self.assertRaises(ValueError): quotient((0,(1,1,1),0,4))

    def test_probability_mass_and_resource_prefix(self):
        p=Contract()
        for s in p.states():
            for a in p.actions(s[2]):
                row=macro_row(p,s,a)
                self.assertEqual(sum(row.values(),F(0)),1)
                self.assertTrue(all(x>=0 for x in row.values()))
                for y in row:
                    if y!=DEAD:self.assertEqual(y[2],min(p.capacity,s[2]-COST[a]+p.harvest))
        self.assertEqual(p.actions(0),('hold',))

    def test_direct_micro_bellman_equals_quotient(self):
        p=Contract(capacity=2);states=p.micros();v={s:F(1) for s in states}
        quotient_values=solve(p,4)['values']
        for n in range(1,5):
            v={s:max(sum((q*v[y] for y,q in micro_row(p,s,a).items() if y!=DEAD),F(0)) for a in p.actions(s[3])) for s in states}
            self.assertTrue(all(v[s]==quotient_values[n][quotient(s)] for s in states))

    def test_exact_kernel_reduction_on_nine_rational_models(self):
        count=0
        for nu,d in product((F(0),F(1,5),F(1,2)),(F(0),F(1,10),F(1,2))):
            r=quotient_report(Contract(capacity=2,world_flip=nu,cell_flip=d))
            self.assertEqual(r['max_tv'],0);count+=r['rows_checked']
        self.assertEqual(count,1008)

    def test_stale_knowledge_is_not_repaired_by_copying(self):
        p=Contract(world_flip=F(1,5),cell_flip=F(0),write_flip=F(0),correction_error=(F(0),F(0)),sensor_error=(F(1,20),F(1,20)),actuator_failure=(F(0),F(0)),degradation=F(0))
        s=(0,0,4)
        self.assertEqual(1-macro_row(p,s,'hold')[DEAD],F(4,5))
        self.assertEqual(1-macro_row(p,s,'correct')[DEAD],F(4,5))
        self.assertEqual(1-macro_row(p,s,'refresh')[DEAD],F(19,20))

    def test_faulty_correction_can_be_worse_than_holding(self):
        p=Contract(world_flip=F(0),cell_flip=F(0),write_flip=F(0),actuator_failure=(F(0),F(0)),correction_error=(F(1,100),F(1,5)))
        s=(0,1,4)
        self.assertEqual(1-macro_row(p,s,'hold')[DEAD],1)
        self.assertEqual(1-macro_row(p,s,'correct')[DEAD],F(4,5))

    def test_maintenance_changes_with_horizon(self):
        p=Contract();s=(0,1,4)
        self.assertEqual(solve(p,1)['policies'][1][s],'hold')
        self.assertEqual(solve(p,10)['policies'][10][s],'service')

    def test_asymmetric_substrate_falsifies_syndrome_only_quotient(self):
        p=Contract();site=(F(3,10),F(1,100),F(1,100))
        s=(0,(1,0,0),0,4);t=(0,(0,1,0),0,4)
        self.assertEqual(quotient(s),quotient(t))
        gap=tv(aggregate(micro_row(p,s,'hold',site)),aggregate(micro_row(p,t,'hold',site)))
        self.assertEqual(gap,F(513619,2000000))

    def test_removing_health_breaks_sufficiency(self):
        p=Contract()
        self.assertNotEqual(macro_row(p,(0,0,4),'correct')[DEAD],macro_row(p,(0,1,4),'correct')[DEAD])

    def test_positive_execution_hazard_kills_infinite_guarantee(self):
        p=Contract();floor=min(p.actuator_failure)
        for s in p.states():
            for a in p.actions(s[2]):self.assertGreaterEqual(macro_row(p,s,a)[DEAD],floor)
        for n in (1,3,10):self.assertTrue(all(v<=(1-floor)**n for v in solve(p,n)['values'][-1].values()))

    def test_calibration_certificate_and_policy_transfer(self):
        p=Contract();q=replace(p,sensor_error=tuple(e+F(1,50) for e in p.sensor_error))
        for n in (1,3,10):
            r=calibration_report(p,q,n)
            self.assertLessEqual(r['delta'],F(1,50))
            self.assertLessEqual(r['max_optimum_gap'],r['bound'])
            self.assertLessEqual(r['max_regret'],2*r['bound'])
        self.assertAlmostEqual(float(calibration_report(p,q)['max_optimum_gap']),.048352214308,places=10)

    def test_composition_bound_and_zero_limit(self):
        self.assertEqual(composition_bound([F(1,10),F(1,5)],1),F(7,25))
        self.assertEqual(composition_bound([F(1,10)],2),F(19,100))
        self.assertEqual(composition_bound([F(0)],1000),0)
        self.assertEqual(composition_bound([F(1)],0),0)
        self.assertEqual(composition_bound([F(1)],1),1)

    def test_exact_component_sensitivity_against_independent_difference(self):
        p=Contract();policies=solve(p,8)['policies'];eps=F(1,100000)
        plus=replace(p,sensor_error=tuple(x+eps for x in p.sensor_error))
        minus=replace(p,sensor_error=tuple(x-eps for x in p.sensor_error))
        vp,vm=evaluate(plus,policies),evaluate(minus,policies);gradient=sensor_sensitivity(p,policies)
        for s in p.states():
            self.assertLess(abs((vp[s]-vm[s])/(2*eps)-gradient[s]),F(1,1000000))
            for a in p.actions(s[2]):self.assertEqual(sum(sensor_derivative_row(p,s,a).values(),F(0)),0)

    def test_invalid_contracts_and_models(self):
        for kw in ({'capacity':-1},{'harvest':-1},{'world_flip':F(2)},{'sensor_error':(F(0),)},{'actuator_failure':(F(-1),F(0))}):
            with self.assertRaises(ValueError):Contract(**kw)
        with self.assertRaises(ValueError):solve(Contract(),-1)
        with self.assertRaises(ValueError):macro_row(Contract(),(0,0,0),'refresh')
        with self.assertRaises(ValueError):composition_bound([F(2)],2)

if __name__=='__main__':unittest.main()
