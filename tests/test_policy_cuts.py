"""Independent exact oracles and falsification tests for CDKA T3.D/T4.C."""
from fractions import Fraction as F
from itertools import product
import unittest

from cdka.policy_cuts import (
    total_variation, dobrushin, feedback_envelope, deterministic_feedback_values,
    live_binary_value, PhysicalModel, renewal_model, cycle_profiles,
    profile_products, pareto_front, renewal_closed_form, randomized_cycle_profile,
)


class FeedbackEnvelopeTests(unittest.TestCase):
    def test_every_binary_three_input_two_action_channel_on_rational_grid(self):
        grid = (F(0), F(1,2), F(1))
        count = 0
        for probabilities in product(grid, repeat=6):
            channels = {c:{a:{0:1-probabilities[2*c+a],1:probabilities[2*c+a]}
                           for a in (0,1)} for c in (0,1,2)}
            self.assertEqual(feedback_envelope(channels), max(deterministic_feedback_values(channels)))
            count += 1
        self.assertEqual(count,729)

    def test_fixed_reset_vs_feedback_channel(self):
        channels = {c:{a:{0:F(a==0),1:F(a==1)} for a in (0,1)} for c in (0,1)}
        for a in (0,1):
            self.assertEqual(dobrushin({c:channels[c][a] for c in (0,1)}),0)
        self.assertEqual(feedback_envelope(channels),1)
        self.assertEqual(sorted(deterministic_feedback_values(channels)),[0,0,1,1])

    def test_single_input_cannot_signal_which_input(self):
        self.assertEqual(feedback_envelope({0:{0:{0:F(1)},1:{1:F(1)}}}),0)

    def test_information_not_created_from_identical_inputs(self):
        p = {0:F(1,3),1:F(2,3)}
        for f in product((0,1),repeat=2):
            output0={a:sum((p[c] for c in p if f[c]==a),F(0)) for a in (0,1)}
            output1=dict(output0)
            self.assertEqual(total_variation(output0,output1),0)

    def test_total_variation_rejects_normalized_survival_confusion(self):
        with self.assertRaises(ValueError):
            total_variation({0:F(1,3)},{1:F(1,3)})


class LiveMassTests(unittest.TestCase):
    def test_perfect_survivor_knowledge_can_hide_tiny_survival(self):
        live=F(1,1000)
        joint={(0,0):live/2,(1,1):live/2}
        self.assertEqual(live_binary_value(joint),(live,live,live))
        self.assertEqual(live_binary_value({(0,0):F(1,2),(1,1):F(1,2)})[2],1)

    def test_general_prior_and_memory_bayes_identity(self):
        grid=(F(0),F(1,8),F(1,4))
        for masses in product(grid,repeat=4):
            joint={(w,c):masses[2*w+c] for w in (0,1) for c in (0,1)}
            mass,d,v=live_binary_value(joint)
            direct=max(sum((joint[w,c] for w in (0,1) for c in (0,1)
                            if plan[c]==w),F(0)) for plan in product((0,1),repeat=2))
            self.assertEqual(v,direct)
            self.assertLessEqual(d,mass)
            self.assertLessEqual(v,mass)


class OccupancyTests(unittest.TestCase):
    def test_true_joint_solver_rejects_omniscient_solution(self):
        model,initial=renewal_model(F(0),selectable_repair=False)
        self.assertEqual(model.survival_optimum(initial,2)['value'],F(1,2))
        self.assertEqual(model.full_state_oracle(initial,2),1)
        model2,init2=renewal_model(F(0),selectable_repair=True)
        self.assertEqual(model2.survival_optimum(init2,2)['value'],1)

    def test_joint_offline_design_matches_independent_product_oracle(self):
        for error in (F(0),F(1,10),F(1,4),F(1,2)):
            for n in range(1,5):
                model,initial=renewal_model(error)
                design=model.survival_optimum(initial,2*n)
                independent=max((p0+p1)/2 for p0,p1 in profile_products(error,n))
                self.assertEqual(design['value'],independent)
                self.assertEqual(design['value'],renewal_closed_form(error,n)['mean'])
                mu=tuple(initial.get(s,F(0)) for s in model.states)
                for phi in design['plan']:
                    mu=model.advance(mu,phi)
                self.assertEqual(sum(mu,F(0)),design['value'])

    def test_occupancy_is_not_exposed_to_runtime_policy(self):
        model,initial=renewal_model(F(1,5))
        solution=model.survival_optimum(initial,6)
        for phi in solution['plan']:
            for c in phi:
                self.assertEqual(len(c),4)
                phase,m,health,resource=c
                self.assertEqual(health,phase)
                self.assertEqual(resource,1-phase)
                self.assertIn(m,(0,1))

    def test_failure_mass_never_normalized(self):
        model,initial=renewal_model(F(1,4))
        mu=tuple(initial.get(s,F(0)) for s in model.states)
        repair={c:model.actions[c][0] for c in model.actions}
        act={c:(('write',c[1]) if c[0]==0 else ('act',c[1])) for c in model.actions}
        after_repair=model.advance(mu,repair)
        after_act=model.advance(after_repair,act)
        self.assertEqual(sum(after_repair,F(0)),1)
        self.assertEqual(sum(after_act,F(0)),F(1,2))

    def test_stationary_invariant_shared_policy(self):
        perfect,initial=renewal_model(F(0))
        noisy,_=renewal_model(F(1,10))
        reset,_=renewal_model(F(0),selectable_repair=False)
        self.assertTrue(list(perfect.stationary_safe_witnesses(tuple(initial))))
        self.assertFalse(list(noisy.stationary_safe_witnesses(tuple(initial))))
        self.assertFalse(list(reset.stationary_safe_witnesses(tuple(initial))))
        for w in (0,1):
            required=((w,(0,w,0,1)),)
            self.assertTrue(list(noisy.stationary_safe_witnesses(required)))


class RenewalGeometryTests(unittest.TestCase):
    def test_all_local_policies_and_horizons_match_pareto_certificate(self):
        for e in (F(1,10),F(1,4),F(1,2)):
            for n in range(1,9):
                points=profile_products(e,n)
                balanced=(1-e)**n
                expected=frozenset(((F(1),F(0)),(F(0),F(1)),(balanced,balanced)))
                self.assertEqual(pareto_front(points),expected)
                self.assertEqual(max(min(p) for p in points),balanced)
                self.assertEqual(max(sum(p)/2 for p in points),max(F(1,2),balanced))

    def test_every_local_randomized_rule_on_exact_grid_obeys_sum_and_product_bounds(self):
        grid=(F(0),F(1,4),F(1,2),F(3,4),F(1))
        count=0
        for e in (F(1,10),F(1,4),F(1,2)):
            for values in product(grid,repeat=4):
                q0,q1=randomized_cycle_profile(e,values[:2],values[2:])
                self.assertLessEqual(q0+q1,2*(1-e))
                self.assertLessEqual(q0*q1,(1-e)**2)
                count+=1
        self.assertEqual(count,1875)

    def test_average_vs_all_contexts_and_hidden_random_seed(self):
        result=renewal_closed_form(F(1,10),10)
        self.assertEqual(result['robust'],F(9,10)**10)
        self.assertEqual(result['mean'],F(1,2))
        self.assertGreater(result['persistent_seed_robust'],result['robust'])

    def test_short_horizon_mean_equals_robust_then_branches_separate(self):
        self.assertEqual(renewal_closed_form(F(1,10),6)['mean'],F(9,10)**6)
        self.assertEqual(renewal_closed_form(F(1,10),7)['mean'],F(1,2))

    def test_rare_noise_time_scaling(self):
        from math import exp
        for tau in (.3,.7,1.5):
            n=1000
            error=F(round(tau*1000),1000000)
            self.assertAlmostEqual(float((1-error)**n),exp(-tau),delta=.001)

    def test_zero_noise_and_validations(self):
        self.assertEqual(renewal_closed_form(F(0),100)['robust'],1)
        with self.assertRaises(ValueError):
            renewal_model(F(3,4))
        with self.assertRaises(ValueError):
            renewal_closed_form(F(1,4),0)

if __name__=='__main__':
    unittest.main()
