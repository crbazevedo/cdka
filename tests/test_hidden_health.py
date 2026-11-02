"""Exact independent checks; not evidence of mathematical novelty."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest

from cdka.composition import Contract, DEAD, COST, macro_row
from cdka.hidden_health import (
    DiagnosticContract, binary_threshold, undiagnosed_value,
    inspected_value, optimal_inspection, hidden_joint, hidden_health_occupancy
)


def independent_enumeration(c):
    """Different implementation: loop over initial health, diagnostic noise,
    delayed flip and terminal programs directly, no hidden_joint helper.
    """
    p=c.physical
    B=c.budget-c.inspection_cost-c.selector_cost
    if B<0: return None
    acts=tuple(a for a in ('hold','correct','refresh','service') if COST[a]<=B)
    outputs=[]
    for a0,a1 in product(acts, repeat=2):
        score=F(0)
        for health_initial in (0,1):
            prior=c.prior_degraded if health_initial else 1-c.prior_degraded
            for sensor_flipped in (0,1):
                q=c.sensor_error if sensor_flipped else 1-c.sensor_error
                signal=health_initial^sensor_flipped
                action=(a0,a1)[signal]
                for health_flipped in (0,1):
                    drift=c.health_drift if health_flipped else 1-c.health_drift
                    health_now=health_initial^health_flipped
                    score+=prior*q*drift*(1-c.inspection_failure)*(
                        1-macro_row(p,(c.syndrome,health_now,B),action)[DEAD])
        outputs.append((score,(a0,a1)))
    return max(x[0] for x in outputs)


class HiddenHealthTests(unittest.TestCase):
    def test_r11_strict_gap_visible_vs_hidden(self):
        c=DiagnosticContract()
        b=undiagnosed_value(c)
        self.assertEqual(b['value'],F(55207461,62500000))
        self.assertEqual(b['policy'],'hold')
        self.assertGreater(b['health_oracle'],b['value'])
        self.assertEqual(b['health_oracle']-b['value'],F(6402641323,250000000000))

    def test_paid_diagnosis_is_realized_by_two_signal_program(self):
        c=DiagnosticContract()
        v=inspected_value(c)
        self.assertEqual(v['decoder'],{0:'refresh',1:'hold'})
        self.assertEqual(v['post_budget'],2)
        self.assertEqual(v['value'],F(227232485323,250000000000))
        self.assertEqual(optimal_inspection(c)['gain'],F(6402641323,250000000000))

    def test_both_costs_are_needed_to_be_affordable(self):
        for b in (2,3):
            m=optimal_inspection(DiagnosticContract(budget=b))
            self.assertEqual(m['choice'],'skip')
            self.assertEqual(m['gain'],0)
        self.assertEqual(optimal_inspection(DiagnosticContract(budget=4))['choice'],'inspect')
        # An unattached diagnostic bit cannot alter a fixed action selector.
        c=DiagnosticContract(budget=4)
        self.assertLessEqual(inspected_value(c,conditional=False)['value'],undiagnosed_value(c)['value'])
        self.assertGreater(inspected_value(c)['value'],inspected_value(c,conditional=False)['value'])

    def test_exact_error_threshold_and_linear_gain(self):
        theta=binary_threshold(DiagnosticContract())['critical_error']
        self.assertEqual(theta,F(6402641323,32975801023))
        for eta in (F(0),F(1,20),F(1,10),F(1,6),theta,F(1,5),F(1,2)):
            c=DiagnosticContract(sensor_error=eta)
            calculated=binary_threshold(c)['actual_net_gain']
            self.assertEqual(optimal_inspection(c)['gain'],calculated)
        self.assertGreater(optimal_inspection(DiagnosticContract(sensor_error=F(1,10)))['gain'],0)
        self.assertEqual(optimal_inspection(DiagnosticContract(sensor_error=F(1,5)))['gain'],0)

    def test_timing_erodes_health_diagnosis(self):
        a=DiagnosticContract(sensor_error=F(1,20),health_drift=F(1,10))
        self.assertEqual(binary_threshold(a)['effective_error'],F(7,50))
        self.assertGreater(optimal_inspection(a)['gain'],0)
        b=DiagnosticContract(sensor_error=F(0),health_drift=F(1,5))
        self.assertEqual(optimal_inspection(b)['gain'],0)
        self.assertEqual(optimal_inspection(b)['choice'],'skip')

    def test_diagnostic_failure_can_reverse_value(self):
        c=DiagnosticContract(inspection_failure=F(1,20))
        self.assertLess(inspected_value(c)['value'],undiagnosed_value(c)['value'])
        self.assertEqual(optimal_inspection(c)['gain'],0)

    def test_prior_and_channel_are_normalized(self):
        for prior,eta,nu in product((F(0),F(1,4),F(1,2),F(4,5),F(1)),
                                    (F(0),F(1,8),F(1,2)),
                                    (F(0),F(1,4),F(1,2))):
            c=DiagnosticContract(prior_degraded=prior,sensor_error=eta,health_drift=nu)
            J=hidden_joint(c)
            self.assertEqual(sum(J.values(),F(0)),1)
            self.assertEqual(sum(J[1,y] for y in (0,1)),prior*(1-nu)+(1-prior)*nu)

    def test_162_joint_diagnosis_cases_against_independent_oracle(self):
        count=0
        for prior,eta,nu,b in product((F(1,4),F(1,2),F(3,4)),
                                       (F(0),F(1,5),F(1,2)),
                                       (F(0),F(1,5),F(1,2)),(2,3,4)):
            for k in (0,1):
                c=DiagnosticContract(budget=b,syndrome=k,prior_degraded=prior,
                                     sensor_error=eta,health_drift=nu)
                expected=independent_enumeration(c)
                actual=inspected_value(c)
                self.assertEqual(actual['value'],expected)
                count+=1
        self.assertEqual(count,162)

    def test_no_omitted_sidechannel_through_resource(self):
        c=DiagnosticContract()
        v=inspected_value(c)
        # Constant diagnosis fee and selector charge: both outputs leave
        # exactly the same resource balance. There is no affordable-mode
        # signaling through remaining tokens in this restricted design.
        self.assertEqual(v['post_budget'],2)
        self.assertTrue(all(COST[a]<=2 for a in v['decoder'].values()))

    def test_hidden_health_policy_vs_oracle_horizons(self):
        c=DiagnosticContract()
        for n in (1,2,3):
            r=hidden_health_occupancy(c.physical,0,4,n)
            self.assertLess(r['value'],r['health_oracle'])
            self.assertGreater(r['design_nodes'],0)
        self.assertEqual(hidden_health_occupancy(c.physical,0,4,1)['value'],
                         undiagnosed_value(c)['value'])

    def test_two_step_independent_exhaustive_plan(self):
        p=Contract(capacity=2)
        k=0;b=2
        target=hidden_health_occupancy(p,k,b,2,prior_degraded=F(1,3))['value']
        scores=[]
        for first in p.actions(b):
            initial={(k,0,b):F(2,3),(k,1,b):F(1,3)}
            posterior={}
            for s,v in initial.items():
                for nxt,q in macro_row(p,s,first).items():
                    if nxt!=DEAD:posterior[nxt]=posterior.get(nxt,F(0))+v*q
            obs=sorted(set((j,r) for (j,h,r) in posterior))
            for final in product(*(p.actions(balance) for k_,balance in obs)):
                plan=dict(zip(obs,final))
                score=F(0)
                for (j,h,r),pr in posterior.items():
                    score+=pr*(1-macro_row(p,(j,h,r),plan[j,r])[DEAD])
                scores.append(score)
        self.assertEqual(target,max(scores))

    def test_invalid_physical_inputs(self):
        for kwargs in ({'budget':5},{'budget':-1},{'sensor_error':F(3,4)},
                       {'health_drift':F(-1)},{'inspection_cost':-1},
                       {'selector_cost':F(1,2)}):
            with self.assertRaises(ValueError):DiagnosticContract(**kwargs)
        with self.assertRaises(ValueError):binary_threshold(DiagnosticContract(prior_degraded=F(1,4)))
        with self.assertRaises(ValueError):hidden_health_occupancy(Contract(),0,4,-1)

if __name__=='__main__':unittest.main()
