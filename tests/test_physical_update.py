"""Exact CDKA v13 circuits, continuous dominance and independent physical paths."""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import isclose
import unittest
from cdka.physical_update import (
    Circuit, INPUTS, BASE, nand_library, payoff_table, margins,
    evaluate, raw_value, bypass_value, program_polynomial, candidates,
    synthesize, analytical_value, phase_certificate, family_constants,
    gate_fault_falsifier,
)


class PhysicalUpdateTests(unittest.TestCase):
    def test_fixed_plant_reference_values(self):
        self.assertEqual(bypass_value(),F(632170281851580256591,781250000000000000000))
        T=payoff_table()
        self.assertEqual(sum((T[y][k][0] for y in range(3) for k in (0,1)),F(0)),
                         F(30726310625071837,39062500000000000))

    def test_every_circuit_truth_table_from_actual_gates(self):
        library,profile=nand_library(4)
        self.assertEqual([r['functions']for r in profile],[5,11,23,48,91])
        self.assertEqual([r['signal_sets']for r in profile],[1,6,33,182,1098])
        for truth,circuit in library.items():
            for m,k in product(range(4),(0,1)):
                self.assertEqual(circuit.execute(m,k),(truth>>(2*m+k))&1)
        self.assertEqual(library[187].cost,2)
        self.assertEqual(library[191].cost,4)

    def test_independent_no_quotient_netlist_enumeration_to_three_gates(self):
        states=[(tuple(BASE),())];seen=set(BASE)
        for depth in range(1,4):
            nxt=[]
            for signals,gates in states:
                for i,j in combinations_with_replacement(range(len(signals)),2):
                    t=255^(signals[i]&signals[j])
                    seen.add(t)
                    nxt.append((signals+(t,),gates+((i,j),)))
            states=nxt
            self.assertEqual(seen,set(nand_library(depth)[0]))

    def test_affine_write_noise_decomposition(self):
        a,b,D=family_constants()
        T=payoff_table();B=sum(T[y][k][0]for y in range(3)for k in (0,1))
        for enc,truth,p,q in product(((0,1,3),(3,0,0)),(0,170,187,191,255),
                                     (F(0),F(1,10)),(F(0),F(1,100),F(1,2))):
            v0=evaluate(enc,truth,p,0)
            self.assertEqual(evaluate(enc,truth,p,q),B+q*D+(1-2*q)*(v0-B))

    def test_actual_microstate_oracle(self):
        library,_=nand_library()
        checked=0
        for enc,p,q,t in product(((3,0,0),(0,1,3)),(F(0),F(1,10)),
                                  (F(0),F(1,100)),(170,187,191)):
            self.assertEqual(evaluate(enc,t,p,q),raw_value(enc,library[t],p,q))
            checked+=1
        self.assertEqual(checked,24)

    def test_polynomial_matches_direct_event_expansion(self):
        checked=0
        library,_=nand_library(4)
        for enc in ((0,0,0),(0,1,3),(3,0,0),(1,2,3)):
            for truth in library:
                c=program_polynomial(enc,truth)
                for p in (F(0),F(1,7),F(1,2)):
                    self.assertEqual(c[0]+p*c[1]+p*p*c[2],evaluate(enc,truth,p))
                    checked+=1
        self.assertEqual(checked,1092)

    def test_entire_noise_interval_is_certified(self):
        cert=phase_certificate()
        self.assertEqual(cert['dominance_checks'],2814)
        self.assertEqual([x['programs']for x in cert['budgets']],[320,704,1472,3072,5824])
        self.assertAlmostEqual(cert['threshold_two_gates'].approximate(),.01377800175004621)
        self.assertAlmostEqual(cert['threshold_four_gates'].approximate(),.10570305126989384)

    def test_synthesis_matches_closed_form_joint_budgets(self):
        for p,q,budget in product((F(0),F(1,100),F(1,10),F(1,5)),
                                   (F(0),F(1,100),F(1,2)),range(5)):
            r=synthesize(p,q,budget)
            self.assertEqual(r['value'],analytical_value(p,q,budget))
            self.assertLessEqual(r['circuit'].cost,budget)

    def test_unrestricted_truth_table_oracle(self):
        for p,q in product((F(0),F(1,100),F(1,10),F(1,4)),(F(0),F(1,100))):
            best=F(0)
            for enc in product(range(4),repeat=3):
                row=margins(enc,p)
                val=sum(max((1-q)*x[0]+q*x[1],q*x[0]+(1-q)*x[1]) for x in row)
                best=max(best,val)
            self.assertEqual(max(best,bypass_value()),analytical_value(p,q,4))

    def test_minimal_upgrade_and_bypass(self):
        self.assertEqual(analytical_value(F(1,10),0,3),bypass_value())
        self.assertGreater(analytical_value(F(1,10),0,4),bypass_value())
        self.assertEqual(analytical_value(F(1,100),F(1,50),4),bypass_value())
        self.assertGreater(analytical_value(F(1,100),F(1,100),4),bypass_value())

    def test_rows_of_weighted_continuation_gap(self):
        enc=(3,0,0);p=F(1,100);q=F(1,100)
        row=margins(enc,p);ds=[x[1]-x[0]for x in row]
        optimum=sum(max(x)for x in row)
        for truth in (0,170,187,191,255):
            chosen=sum(x[(truth>>i)&1]for i,x in enumerate(row))
            regret=sum(abs(d)for i,d in enumerate(ds)if bool((truth>>i)&1)!=(d>0))
            self.assertEqual(optimum-chosen,regret)
            besttruth=sum(int(d>0)<<i for i,d in enumerate(ds))
            self.assertEqual(evaluate(enc,besttruth,p,q)-evaluate(enc,truth,p,q),(1-2*q)*regret)

    def test_equivalent_ideal_programs_are_not_noisy_gate_equivalents(self):
        r=gate_fault_falsifier(F(1,10))
        self.assertEqual(r['wire_error'],0)
        self.assertEqual(r['double_inverter_error'],(F(9,50),F(9,50)))
        self.assertEqual(r['formula'],F(9,50))

    def test_no_hidden_state_at_runtime_interface(self):
        import inspect
        self.assertEqual(list(inspect.signature(Circuit.execute).parameters),['self','word','syndrome','faults'])
        circuit=nand_library()[0][191]
        self.assertEqual([circuit.execute(3,k)for k in (0,1)],[0,1])

    def test_invalid_contracts(self):
        for b in (-1,6,2.5):
            with self.assertRaises(ValueError):nand_library(b)
        with self.assertRaises(ValueError):evaluate((0,1,2),256)
        with self.assertRaises(ValueError):evaluate((0,1,2),3,F(2,3))
        with self.assertRaises(ValueError):Circuit(0).execute(4,0)
        with self.assertRaises(ValueError):synthesize(budget=5)


if __name__=='__main__':unittest.main()
