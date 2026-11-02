from fractions import Fraction as F
from itertools import product
from math import exp,log,sqrt
import unittest
from cdka.implementability import *


def compositions(total,n):
    if n==1:
        yield(total,);return
    for a in range(total+1):
        for tail in compositions(total-a,n-1): yield(a,)+tail


class ImplementabilityTests(unittest.TestCase):
    def test_marginal_actions_do_not_define_policy_architecture(self):
        coupled=[(F(0),F(0)),(F(1),F(1))]
        rectangle=list(product((F(0),F(1)),repeat=2))
        self.assertEqual(restricted_reset_diameter(coupled),0)
        self.assertEqual(restricted_reset_diameter(rectangle),1)
        self.assertEqual({x for x,y in coupled},{x for x,y in rectangle})
        self.assertEqual({y for x,y in coupled},{y for x,y in rectangle})

    def test_exact_coupled_sum_and_product_bounds(self):
        count=0
        for sigma,p in product((F(0),F(1,2),F(1)),(F(0),F(1,10),F(1,2))):
            b=restricted_cycle_bound(sigma,p)
            for *_,q0,q1 in constrained_policy_grid(sigma,p):
                self.assertLessEqual(q0+q1,2*b)
                self.assertLessEqual(q0*q1,b*b);count+=1
            q0,q1=cycle_profile((1-sigma)/2,(1+sigma)/2,F(0),F(1),p)
            self.assertEqual(q0,b);self.assertEqual(q1,b)
        self.assertEqual(count,3675)

    def test_two_cycle_fresh_policies_no_hidden_seed(self):
        laws=constrained_policy_grid(F(1,2),F(1,4),denominator=2)
        b=restricted_cycle_bound(F(1,2),F(1,4))
        maximum=F(0)
        for a,z in product(laws,repeat=2):
            s0,s1=a[-2]*z[-2],a[-1]*z[-1]
            self.assertLessEqual(s0*s1,b**4)
            maximum=max(maximum,min(s0,s1))
        self.assertLessEqual(maximum,b*b)

    def test_cycle_effort_split_global(self):
        for r in (0,.2,1,3,10):
            for k in range(101):
                self.assertLessEqual(produced_cycle(r*k/100,r*(1-k/100)),optimal_cycle(r)+1e-14)
            self.assertAlmostEqual(produced_cycle(r/2,r/2),optimal_cycle(r),14)

    def test_exact_calculus_and_inflection(self):
        inf=curvature_threshold()
        self.assertAlmostEqual(optimal_cycle(inf),2-sqrt(2),14)
        self.assertGreater(log_cycle_curvature(.1),0)
        self.assertLess(log_cycle_curvature(3),0)
        for r in (.3,1,2,5):
            h=1e-4
            d1=(log_cycle(r+h)-log_cycle(r-h))/(2*h)
            d2=(log_cycle(r+h)-2*log_cycle(r)+log_cycle(r-h))/(h*h)
            self.assertAlmostEqual(d1,log_cycle_slope(r),8)
            self.assertAlmostEqual(d2,log_cycle_curvature(r),6)

    def test_scarce_budget_concentration_is_certified(self):
        for n in (2,3,4):
            for units in range(1,11):
                r=units*.1
                oracle=optimal_grid_schedule(n,units)
                theorem=log_cycle(r)+(n-1)*log_cycle(0)
                self.assertAlmostEqual(oracle.log_survival,theorem,13)
                self.assertEqual(sum(x>0 for x in oracle.allocations),1)

    def test_grid_dp_against_independent_compositions(self):
        for n in (1,2,3,4):
            for units in range(0,15):
                exact=max(sum(log_cycle(.3*k) for k in c) for c in compositions(units,n))
                answer=optimal_grid_schedule(n,units,.3)
                self.assertEqual(sum(answer.allocations),units)
                self.assertAlmostEqual(answer.log_survival,exact,13)

    def test_tangent_envelope_majorizes_and_is_concave(self):
        star=tangent_threshold()
        self.assertAlmostEqual(star,1.9687283214,9)
        self.assertAlmostEqual(star*log_cycle_slope(star),log_cycle(star)+log(2),13)
        ys=[]
        for k in range(201):
            r=k*.04
            val=concave_log_envelope(r)
            self.assertGreaterEqual(val+1e-13,log_cycle(r));ys.append(val)
        for a,b,c in zip(ys,ys[1:],ys[2:]): self.assertLessEqual(a-2*b+c,1e-12)

    def test_total_budget_envelope_upper_bound(self):
        for n in (2,3,5):
            for units in (1,5,15,30):
                ans=optimal_grid_schedule(n,units,.2)
                self.assertLessEqual(ans.log_survival,n*concave_log_envelope(units*.2/n)+1e-12)

    def test_high_reliability_budget_exact(self):
        for n,beta in product((1,2,10,100),(2-sqrt(2),.8,.9,.99)):
            R=minimum_high_reliability_budget(n,beta)
            self.assertAlmostEqual(n*log_cycle(R/n),log(beta),12)
            self.assertGreater(R,fidelity_only_budget(n,beta))

    def test_n_log_n_scaling(self):
        beta=.9
        for n in (100,1000,10000):
            R=minimum_high_reliability_budget(n,beta)
            leading=2*n*(log(n)-log(-log(beta)))
            self.assertLess(abs(R-leading),.2)

    def test_harvest_budget_and_asymptotic_attainment(self):
        for h in (0,.3,1,2,4):
            r=harvesting_schedule(2000,h)
            spent=0
            for t,e in enumerate(r['allocations']):
                self.assertLessEqual(spent+e,h*t+1e-9)
                spent+=e
            self.assertLessEqual(r['rate'],r['rate_upper']+1e-12)
            self.assertLess(abs(r['rate']-concave_log_envelope(h)),.002)

    def test_mean_not_robust_mixture_and_assumptions(self):
        b=restricted_cycle_bound(F(1,2),F(1,10))
        self.assertLess(b**5,F(1,2))
        self.assertEqual((F(1)+F(0))/2,F(1,2))
        for fn,args in ((optimal_cycle,(-1,)),(optimal_grid_schedule,(0,2)),
                        (minimum_high_reliability_budget,(2,.5)),
                        (produced_cycle,(float('nan'),1)),(restricted_reset_diameter,([],))):
            with self.assertRaises(ValueError): fn(*args)

if __name__=='__main__':unittest.main()
