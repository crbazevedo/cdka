"""Exhaustive independent policy and causal-channel checks for T3.C/T4.B."""
from fractions import Fraction as F
from itertools import product
import unittest

from cdka.causal_cut import (
    CausalCutSystem, ERASED, MEMORY, bayes_best,
    total_variation_binary, zero_error_support_obstructions,
    deterministic_minimal_obstructions, physical_configuration_bypass,
    enumerate_repair_schedules, higher_order_compatibility_obstruction,
    general_safe_decision_value,
)


class MinimalCausalCutTests(unittest.TestCase):
    def test_minimal_deterministic_search(self):
        examples=deterministic_minimal_obstructions()
        self.assertEqual(len(examples),4)
        for sensor,reset,value in examples:
            self.assertEqual(len(set(sensor)),2) # perfect one-bit observation
            self.assertEqual(len(set(reset)),1) # compulsory repair destroys it
            self.assertEqual(value,F(1,2))

    def test_independent_marginals_are_feasible_but_joint_is_not(self):
        model=CausalCutSystem() # full erasure; one mandatory repair
        self.assertEqual(model.initial_sensor_information_bits(),1)
        self.assertTrue(model.actuator_ready)
        self.assertEqual(model.max_protections(),0)
        self.assertEqual(model.best_success(),F(1,2))
        self.assertEqual(model.exact_formula(),F(1,2))
        self.assertEqual(model.memory_tv(),0)
        self.assertEqual(model.zero_error_obstructions(),
                         {ERASED:frozenset((0,1))})
        # With one additional physical resource, protect the memory
        repaired=CausalCutSystem(budget=2)
        self.assertEqual(repaired.best_success(),1)
        self.assertEqual(repaired.memory_tv(),1)
        self.assertEqual(repaired.zero_error_obstructions(),{})

    def test_all_binary_channel_and_resource_combinations(self):
        # Fraction arithmetic gives exact, not floating-point, comparison.
        cases=0
        for n in range(1,5):
            for B in range(n,2*n+1):
                for eta,rho,nu in product(
                    (F(0),F(1,4),F(1,2)),
                    (F(0),F(1,3),F(1)),
                    (F(0),F(1,5),F(1,2))
                ):
                    model=CausalCutSystem(eta,rho,nu,n,B)
                    oracle=model.best_success()
                    theoretical=model.exact_formula()
                    self.assertEqual(oracle,theoretical)
                    self.assertEqual(oracle,(1+model.memory_tv())/2)
                    cases+=1
        self.assertEqual(cases,378)

    def test_enumerate_precommitted_repair_schedules(self):
        for n in range(1,5):
            for budget in range(n,2*n+1):
                s=CausalCutSystem(F(1,6),F(1,2),F(1,7),n,budget)
                scores=enumerate_repair_schedules(s)
                self.assertTrue(scores)
                self.assertEqual(max(scores.values()),s.best_success())
                self.assertEqual(s.best_success(),s.exact_formula())

    def test_horizon_decay_and_budget_threshold(self):
        for n in range(1,6):
            self.assertEqual(CausalCutSystem(cycles=n,budget=n).best_success(),F(1,2))
            self.assertEqual(CausalCutSystem(cycles=n,budget=2*n).best_success(),1)
            if n>1:
                self.assertEqual(CausalCutSystem(cycles=n,budget=2*n-1).best_success(),F(1,2))
            self.assertEqual(CausalCutSystem(cycles=n,budget=n-1).best_success(),0)
        p=[CausalCutSystem(rho=F(1,2),cycles=n,budget=n).best_success()
           for n in range(1,6)]
        self.assertTrue(all(a>b for a,b in zip(p,p[1:])))

    def test_external_actions_can_store_knowledge(self):
        self.assertEqual(physical_configuration_bypass(),(F(1,2),F(1)))
        # No result about physical memory is sound without checking all
        # accessible physical variables, not only an explicit register.

    def test_general_hypergraph_support_criterion(self):
        W={0:frozenset((0,2)),1:frozenset((1,2))}
        joint={(0,ERASED):F(1,2),(1,ERASED):F(1,2)}
        self.assertEqual(zero_error_support_obstructions(joint,W,MEMORY),{})
        W_no_common={0:frozenset((0,)),1:frozenset((1,))}
        self.assertEqual(zero_error_support_obstructions(joint,W_no_common,MEMORY),
                         {ERASED:frozenset((0,1))})

    def test_data_processing_and_information_horizon(self):
        s=CausalCutSystem(eta=F(1,5),rho=F(1,4),nu=F(1,10),cycles=3,budget=3)
        self.assertLess(s.terminal_information_bits(),s.initial_sensor_information_bits())
        self.assertGreaterEqual(s.terminal_information_bits(),0)
        self.assertLessEqual(s.terminal_information_bits(),1)
        self.assertEqual(s.memory_tv(),F(3,5)*F(4,5)**3*F(3,4)**3)

    def test_three_world_higher_order_cut(self):
        value,pairwise,failures=higher_order_compatibility_obstruction()
        self.assertTrue(pairwise)
        self.assertEqual(value,F(2,3))
        self.assertEqual(failures,{ERASED:frozenset((0,1,2))})

    def test_generic_viability_with_overlapping_actions(self):
        A={0:frozenset((0,2)),1:frozenset((1,2))}
        joint={(0,ERASED):F(1,2),(1,ERASED):F(1,2)}
        value,decoder=general_safe_decision_value(joint,A,(ERASED,))
        self.assertEqual(value,1)
        self.assertEqual(decoder[ERASED],2)

    def test_invalid_parameters(self):
        for kw in ({'eta':F(2,3)},{'rho':F(-1,2)},{'nu':F(3,4)},
                   {'cycles':0},{'budget':-1}):
            with self.assertRaises(ValueError):
                CausalCutSystem(**kw)
        s=CausalCutSystem()
        with self.assertRaises(ValueError):
            s.terminal_joint((True,)) # not enough resource

    def test_one_step_information_is_not_future_information(self):
        s=CausalCutSystem(rho=F(1,2),nu=F(0),cycles=2,budget=2)
        self.assertEqual(s.initial_sensor_information_bits(),1)
        self.assertEqual(s.memory_tv(),F(1,4))
        self.assertEqual(s.best_success(),F(5,8))
        self.assertEqual(CausalCutSystem(rho=F(1,2),nu=F(0),
                                        cycles=2,budget=4).best_success(),1)


if __name__ == "__main__":
    unittest.main()
