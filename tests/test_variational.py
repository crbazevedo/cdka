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


if __name__=='__main__':unittest.main()
