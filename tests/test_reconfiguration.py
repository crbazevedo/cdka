from fractions import Fraction as F
from itertools import product
from math import exp,log
import unittest
from cdka.reconfiguration import (
    coupled_errors,xor_failure,xor_error_interval,independent_masks,common_masks,
    bounded_single_upset,repetition_success,repetition_certificate,safe_support,
    redundant_kernel,redundant_lifetime,redundant_radius,propagate_live,
    old_success,Retrofit,rational_solve,infinite_survival_fixed,switching_witness,
)


class CorrelationTests(unittest.TestCase):
    def test_all_joint_rational_error_laws(self):
        count=0
        for a,b,t in product([F(i,8) for i in range(9)],repeat=3):
            lo=max(F(0),a+b-1);hi=min(a,b)
            if not lo<=t<=hi:continue
            law=coupled_errors(a,b,t)
            self.assertEqual(sum(law.values()),1)
            self.assertEqual(law[1,0]+law[1,1],a)
            self.assertEqual(law[0,1]+law[1,1],b)
            direct=sum(p for e,p in law.items() if e[0]!=e[1])
            self.assertEqual(direct,xor_failure(a,b,t))
            low,high=xor_error_interval(a,b)
            self.assertLessEqual(low,direct);self.assertLessEqual(direct,high)
            count+=1
        self.assertEqual(count,165)

    def test_correlation_helps_parity_but_hurts_majority(self):
        p=F(1,10)
        self.assertEqual(xor_failure(p,p,p),0)
        self.assertEqual(xor_failure(p,p,p*p),F(18,100))
        self.assertEqual(xor_failure(p,p,0),F(1,5))
        self.assertEqual(repetition_success(common_masks(3,p)),1-p)
        self.assertEqual(repetition_success(independent_masks(3,p)),F(972,1000))

    def test_correctable_support_changes_zero_error_property(self):
        for p in (F(0),F(1,7),F(1,2),F(1)):
            self.assertEqual(repetition_success(bounded_single_upset(p)),1)
        self.assertFalse(repetition_certificate(1)['zero_error'])
        self.assertFalse(repetition_certificate(2)['zero_error'])
        self.assertTrue(repetition_certificate(3)['zero_error'])

    def test_independent_repetition_error_polynomial(self):
        for k in range(11):
            p=F(k,10)
            self.assertEqual(1-repetition_success(independent_masks(3,p)),3*p*p-2*p**3)

    def test_invalid_joint_law(self):
        with self.assertRaises(ValueError):coupled_errors(F(1,10),F(1,10),F(1,2))
        with self.assertRaises(ValueError):coupled_errors(-1,0,0)


class SupportAndRecoveryTests(unittest.TestCase):
    def test_exact_resolvent_vs_lifetime_formula(self):
        count=0
        for di in range(1,7):
            for ri in range(7):
                d,r=F(di,6),F(ri,6)
                Q=redundant_kernel(d,r)
                t=rational_solve([[F(i==j)-Q[i][j] for j in range(2)] for i in range(2)],(1,1))
                self.assertEqual(t[0],redundant_lifetime(d,r))
                self.assertEqual(safe_support(Q),frozenset())
                self.assertEqual(infinite_survival_fixed(Q),(0,0))
                self.assertLess(redundant_radius(d,r),1)
                count+=1
        self.assertEqual(count,42)

    def test_repair_changes_lifetime_order_not_closed_support(self):
        self.assertEqual(redundant_lifetime(F(1,100),1),10198)
        self.assertEqual(safe_support(redundant_kernel(0,1)),frozenset((0,1)))
        Q=redundant_kernel(F(1,10),F(4,5))
        vals=[sum(propagate_live(Q,(F(1),F(0)),n)) for n in (0,1,5,20,100)]
        self.assertTrue(all(x>y for x,y in zip(vals,vals[1:])))

    def test_positive_survival_does_not_require_safe_initial_state(self):
        Q=((F(1),F(0)),(F(1,5),F(7,10)))
        self.assertEqual(safe_support(Q),frozenset((0,)))
        self.assertEqual(infinite_survival_fixed(Q),(F(1),F(2,3)))
        self.assertGreater(sum(propagate_live(Q,(F(0),F(1)),20)),F(2,3))

    def test_switching_defeats_mode_by_mode_impossibility(self):
        w=switching_witness()
        self.assertEqual(w['A2'],((0,0),(0,0)))
        self.assertEqual(w['B2'],((0,0),(0,0)))
        self.assertEqual(infinite_survival_fixed(w['A']),(0,0))
        self.assertEqual(infinite_survival_fixed(w['B']),(0,0))
        self.assertEqual(infinite_survival_fixed(w['AB']),(1,0))
        self.assertEqual(infinite_survival_fixed(w['average']),(0,0))
        self.assertEqual(infinite_survival_fixed(w['closed_loop']),(1,1))

    def test_any_leak_breaks_fixed_safe_class(self):
        self.assertEqual(infinite_survival_fixed(((F(1),),)),(F(1),))
        for p in (F(1,10000),F(1,10),F(1)):
            self.assertEqual(infinite_survival_fixed(((1-p,),)),(F(0),))


class ReconfigurationTests(unittest.TestCase):
    def test_old_macro_matches_v4_effort_calibration(self):
        for r in range(9):
            effort=2*r*log(2)
            q=1-exp(-effort/2)+.5*exp(-effort)
            self.assertAlmostEqual(float(old_success(r)),q,places=14)

    def test_bellman_against_independent_path_enumeration(self):
        checks=0
        for cap in range(1,4):
            for K in range(1,cap+2):
                for h in (0,1,2):
                    m=Retrofit(cap,K,h,F(4,5),F(9,10))
                    table,_=m.finite(4)
                    for n in range(5):
                        for b in range(cap+1):
                            self.assertEqual(table[n][b],m.brute_value(n,b))
                            checks+=1
        self.assertEqual(checks,435)

    def test_infinite_dag_against_all_stationary_prescriptions(self):
        for cap in range(1,5):
            for K in range(1,cap+1):
                for h in (0,1,2,3):
                    m=Retrofit(cap,K,h,F(3,4),F(1))
                    maxvals=[F(0)]*(cap+1)
                    options=[list(range(b+1))+(['S'] if b>=K else []) for b in range(cap+1)]
                    for plan in product(*options):
                        for b0 in range(cap+1):
                            b=b0;seen=set();mass=F(1)
                            while b not in seen:
                                seen.add(b);a=plan[b]
                                if a=='S':
                                    mass*=m.install;break
                                mass*=old_success(a);b=m.next_balance(b,a)
                            else:mass=F(0)
                            maxvals[b0]=max(maxvals[b0],mass)
                    self.assertEqual(tuple(maxvals),m.infinite()[0])

    def test_financed_delaying_installation_can_beat_earliest_path(self):
        m=Retrofit()
        path=m.infinite_path(0)
        self.assertEqual([x['action'] for x in path],['run:0','run:3','run:4','switch'])
        best=path[-1]['mass']
        earliest=old_success(0)*old_success(2)*m.install
        self.assertEqual(best,F(489177,1310720))
        self.assertGreater(best,earliest)
        self.assertAlmostEqual(exp(-m.log_path_cost(0)),float(best),places=13)

    def test_finite_horizon_objective_changes_installation_decision(self):
        m=Retrofit();v,p=m.finite(25)
        self.assertTrue(p[1][8].startswith('run:'))
        self.assertEqual(p[25][8],'switch')
        self.assertEqual(v[25][0],m.infinite()[0][0])
        for n in range(25):
            self.assertTrue(all(v[n][b]>=v[n+1][b] for b in range(9)))

    def test_capacity_floor_and_failure_support(self):
        self.assertEqual(Retrofit(7,8,5).infinite()[0],(F(0),)*8)
        self.assertGreater(Retrofit(8,8,5).infinite()[0][0],0)
        self.assertEqual(Retrofit(8,8,5,upgraded=F(999,1000)).infinite()[0],(F(0),)*9)
        self.assertEqual(Retrofit(8,8,0).infinite()[0][0],0)
        self.assertEqual(Retrofit(8,8,0).infinite()[0][8],F(9,10))

    def test_explicit_finite_to_infinite_error_certificate(self):
        for cap,K,h in ((3,3,1),(3,2,2),(3,4,2),(3,3,0)):
            m=Retrofit(cap,K,h);inf=m.infinite()[0];v,_=m.finite(15)
            for n in range(1,16):
                for b in range(cap+1):
                    self.assertGreaterEqual(v[n][b],inf[b])
                    self.assertLessEqual(v[n][b]-inf[b],old_success(cap)**n)

    def test_strict_error_floor_remains_fatal_long_term(self):
        m=Retrofit(4,3,2,F(1),F(9,10));v,_=m.finite(20)
        maxq=max(old_success(m.capacity),m.upgraded)
        for n in range(1,21):
            for b in range(5):
                self.assertLessEqual(v[n][b],maxq**(n-1))

    def test_resource_prefixes_and_no_failure_renormalization(self):
        m=Retrofit()
        path=m.infinite_path(0);mass=F(1)
        for node in path:
            if node['action']=='switch':mass*=m.install
            else:
                r=int(node['action'].split(':')[1]);self.assertLessEqual(r,node['balance'])
                mass*=old_success(r)
            self.assertEqual(node['mass'],mass)
        self.assertLess(mass,1)

    def test_invalid_parameters(self):
        for kw in ({'capacity':-1},{'cost':0},{'harvest':-1},{'install':F(3,2)}):
            with self.assertRaises(ValueError):Retrofit(**kw)
        with self.assertRaises(ValueError):Retrofit().next_balance(1,2)
        with self.assertRaises(ValueError):old_success(-1)

if __name__=='__main__':unittest.main()
