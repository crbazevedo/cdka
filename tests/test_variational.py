"""Independent numeric and algebraic checks of classical instruments."""
import math
import unittest
from cdka.variational import (
    quartic_equilibria, critical_tilt, quartic_gradient, left_barrier,
    right_barrier,saddle_node_constant,quartic_left_action,
    ou_endpoint_rate,binary_rate_distortion,restricted_authority_gap,
    bernoulli_kl,
)


class FiniteTimeTests(unittest.TestCase):
    def test_equilibria(self):
        self.assertEqual(tuple(round(x,12) for x in quartic_equilibria(0)),(-1.,0.,1.))
        for u in (-.2,0.,.2):
            for x in quartic_equilibria(u):self.assertAlmostEqual(quartic_gradient(x,u),0.,places=10)
        self.assertAlmostEqual(critical_tilt(),.3849001794597505)

    def test_symmetric_barriers(self):
        self.assertAlmostEqual(left_barrier(),.25)
        self.assertAlmostEqual(right_barrier(),.25)
        self.assertAlmostEqual(left_barrier(.1),right_barrier(-.1),places=11)
        self.assertLess(left_barrier(.1),.25)
        self.assertGreater(right_barrier(.1),.25)

    def test_saddle_node_universal_scaling(self):
        c=saddle_node_constant()
        errors=[]
        for delta in (.08,.02,.005,.001):
            ratio=left_barrier(critical_tilt()-delta)/(c*delta**1.5)
            errors.append(abs(ratio-1))
        self.assertTrue(all(a>b for a,b in zip(errors,errors[1:])))
        self.assertLess(errors[-1],0.001)

    def test_action_exceeds_quasipotential(self):
        samples=[quartic_left_action(T) for T in (.5,1,2,5)]
        self.assertTrue(all(s.action>s.quasipotential for s in samples))
        self.assertTrue(all(a.action>b.action for a,b in zip(samples,samples[1:])))
        self.assertAlmostEqual(samples[1].action,.3938774144,delta=.002)
        self.assertAlmostEqual(samples[-1].action,.250897173,delta=.002)

    def test_action_conserved_energy_derivative(self):
        T=1.3;h=.002
        left=quartic_left_action(T-h).action
        right=quartic_left_action(T+h).action
        middle=quartic_left_action(T)
        self.assertAlmostEqual((right-left)/(2*h),-middle.conserved_energy,delta=.004)

    def test_ou_finite_time_action(self):
        J1=ou_endpoint_rate(1,1,1)
        self.assertAlmostEqual(J1,1/(2*(1-math.exp(-2))))
        self.assertGreater(ou_endpoint_rate(1,1,.5),J1)
        self.assertGreater(J1,ou_endpoint_rate(1,1,2))
        self.assertAlmostEqual(ou_endpoint_rate(1,1,20),.5,places=10)

    def test_rate_distortion_soft_vs_hard(self):
        self.assertAlmostEqual(binary_rate_distortion(0),1)
        self.assertAlmostEqual(binary_rate_distortion(.5),0)
        self.assertGreater(binary_rate_distortion(.05),binary_rate_distortion(.2))
        self.assertLess(binary_rate_distortion(.05),1)

    def test_authority_gap_strict(self):
        for beta in (.3,.35,.4,.49,.5):
            actual,lower,gap=restricted_authority_gap(beta)
            self.assertGreater(actual,lower)
            self.assertGreater(gap,0)
        self.assertAlmostEqual(restricted_authority_gap(.4)[0],bernoulli_kl(.8,.5))

    def test_assumptions_guarded(self):
        with self.assertRaises(ValueError): quartic_equilibria(critical_tilt())
        with self.assertRaises(ValueError): quartic_left_action(0)
        with self.assertRaises(ValueError): restricted_authority_gap(.7)




class CriticalScalingTests(unittest.TestCase):
    def test_scaling_normal_form_collapse(self):
        from cdka.variational import critical_tilt, quartic_left_action, saddle_normal_form_action
        tau=0.4
        reference=saddle_normal_form_action(tau)
        errors=[]
        for delta in (.03,.01,.002):
            T=tau/(3**.25*math.sqrt(delta))
            action=quartic_left_action(T,critical_tilt()-delta).action
            norm=action*3**.25/delta**1.5
            errors.append(abs(norm-reference))
        self.assertTrue(errors[0]>errors[1]>errors[2])
        self.assertLess(errors[-1],.05)

    def test_small_tau_normal_form_limit(self):
        from cdka.variational import saddle_normal_form_action
        for tau in (.03,.05,.1):
            self.assertLess(abs(saddle_normal_form_action(tau)*tau-1),.09)


class CausalFrameTests(unittest.TestCase):
    def test_fixed_initial_symmetric_counterfactual(self):
        from cdka.variational import fixed_frame_action
        for u in (-.2,0,.2):
            jl=fixed_frame_action(3,u,initial=-1.1,target=0)
            jr=fixed_frame_action(3,-u,initial=1.1,target=0)
            self.assertAlmostEqual(jl,jr,places=9)

    def test_fixed_causal_frame_information_phases(self):
        from cdka.variational import fixed_frame_action
        from cdka.finite import minimum_action_cover
        controls=(-.2,0,.2)
        jl=[fixed_frame_action(3,u,initial=-1.1,target=0) for u in controls]
        jr=[fixed_frame_action(3,u,initial=1.1,target=0) for u in controls]
        self.assertTrue(jl[0]>jl[1]>jl[2])
        self.assertTrue(jr[0]<jr[1]<jr[2])
        for c,k in ((.2,1),(.3,2),(.5,None)):
            safe={"L":{u for u,rate in zip(controls,jl) if rate>c},
                  "R":{u for u,rate in zip(controls,jr) if rate>c}}
            cover=minimum_action_cover(safe)
            self.assertEqual(None if cover is None else len(cover),k)
        self.assertAlmostEqual(jl[1],.269641458,delta=.002)
        self.assertAlmostEqual(jl[0],.460201393,delta=.002)


class SharedBudgetTests(unittest.TestCase):
    def test_optimum_equalizes_competing_error_exponents(self):
        from cdka.causal_tradeoff import optimize_fixed_frame_budget
        for budget in (.025,.1,.2):
            v=optimize_fixed_frame_budget(budget,T=3)
            self.assertGreater(v.actuation,0)
            self.assertLess(v.actuation,budget)
            self.assertAlmostEqual(v.good_action_rate,
                                   v.wrong_action_rate+v.sensing_error_rate,places=6)

    def test_optimum_vs_independent_grid(self):
        from cdka.causal_tradeoff import optimize_fixed_frame_budget
        from cdka.variational import fixed_frame_action
        budget=.12;v=optimize_fixed_frame_budget(budget,T=3)
        for i in range(61):
            a=budget*i/60
            g=fixed_frame_action(3,-a,n=512)
            b=fixed_frame_action(3,+a,n=512)
            objective=min(g,b+2*(budget-a))
            self.assertGreaterEqual(v.effective_failure_rate+1e-9,objective)

    def test_small_budget_share_depends_on_deadline_sensitivity(self):
        from cdka.causal_tradeoff import optimize_fixed_frame_budget,local_reliability_sensitivity
        for T in (1,3,5):
            q=local_reliability_sensitivity(T)
            result=optimize_fixed_frame_budget(.005,T=T)
            predicted=2/(2+2*q)
            self.assertAlmostEqual(result.actuation/result.budget,predicted,delta=.01)


if __name__=='__main__':unittest.main()
