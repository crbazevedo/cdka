"""Independent CDKA finite-surrogate checks; not originality evidence."""
import math
import unittest

from cdka.reliability import (
    effective_failure_exponent, sensor_error, sensor_information,
    finite_noise_failure_rate, quartic_barrier_pair,
    optimal_reliability_allocation,
)
from cdka.variational import critical_tilt


class ExponentTests(unittest.TestCase):
    def test_min_plus_error_exponent(self):
        good, bad, kappa = .42, .12, .2
        self.assertAlmostEqual(effective_failure_exponent(good,bad,kappa),.32)
        previous = -float('inf')
        for eps in (.2,.1,.05,.025,.0125):
            empirical = finite_noise_failure_rate(eps,good,bad,kappa)
            self.assertGreater(empirical, previous)
            previous = empirical
        self.assertAlmostEqual(previous,.32,delta=.014)

    def test_mi_saturates_different_reliability_rates(self):
        # The sensor error exponent cannot be recovered from limiting 1 bit.
        eps=.001
        self.assertAlmostEqual(sensor_information(eps,.02),1,places=6)
        self.assertAlmostEqual(sensor_information(eps,.2),1,places=6)
        self.assertAlmostEqual(sensor_information(eps,0),0)
        self.assertAlmostEqual(sensor_error(.1,0),.5)

    def test_quartic_symmetric_barriers(self):
        self.assertEqual(quartic_barrier_pair(0),(.25,.25))
        good,bad = quartic_barrier_pair(.15)
        self.assertGreater(good,.25)
        self.assertLess(bad,.25)
        with self.assertRaises(ValueError):
            quartic_barrier_pair(critical_tilt())

    def test_unique_optimum_and_branch_equalization(self):
        for B in (.015,.1,.2,.3):
            result = optimal_reliability_allocation(B, gamma=2)
            self.assertAlmostEqual(result.action_tilt+result.sensing_resource,B,12)
            self.assertGreater(result.action_tilt,0)
            self.assertLess(result.action_tilt,B)
            self.assertAlmostEqual(result.good_barrier,
                                   result.bad_barrier+result.sensor_error_exponent,places=10)
            self.assertGreater(result.effective_exponent,.25)
            # Exhaustive discretization is an independent lower-precision oracle.
            grid_max = -math.inf
            for i in range(501):
                a=B*i/500
                g,b=quartic_barrier_pair(a)
                exponent=min(g,b+2*(B-a))
                grid_max=max(grid_max,exponent)
            self.assertGreaterEqual(result.effective_exponent+1e-10,grid_max)

    def test_small_budget_linear_slope(self):
        B=.0002
        result=optimal_reliability_allocation(B, gamma=2)
        # da*/dB -> gamma/(gamma+2) = 1/2 at zero tilt.
        self.assertAlmostEqual(result.action_tilt/B,.5,delta=.002)
        self.assertAlmostEqual((result.effective_exponent-.25)/B,.5,delta=.002)

    def test_finite_rate_matches_barriers_at_optimum(self):
        result=optimal_reliability_allocation(.2,2)
        values=[finite_noise_failure_rate(eps,
                result.good_barrier,result.bad_barrier,
                result.sensor_error_exponent) for eps in (.1,.05,.02,.005)]
        self.assertTrue(all(a<b for a,b in zip(values,values[1:])))
        self.assertAlmostEqual(values[-1],result.effective_exponent,delta=.005)

    def test_reliability_feasibility_threshold(self):
        g,b=.42,.12
        c=.25
        self.assertLess(effective_failure_exponent(g,b,.05),c)
        self.assertGreater(effective_failure_exponent(g,b,.2),c)
        self.assertAlmostEqual(c-b,.13)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            sensor_error(0,.1)
        with self.assertRaises(ValueError):
            optimal_reliability_allocation(critical_tilt(),2)
        with self.assertRaises(ValueError):
            optimal_reliability_allocation(.1,0)
        with self.assertRaises(ValueError):
            finite_noise_failure_rate(.1,-1,.2,.3)

if __name__ == "__main__":
    unittest.main()
