"""Exact independent bounded enumeration; no Monte Carlo claims."""
from fractions import Fraction as F
from itertools import product
from math import comb
import unittest
from cdka.faulty_updates import *
from cdka.physical_update import analytical_value, payoff_table, transport_probability


def scalar_execution(circuit,word,k,faults):
    wires=[0,1,word&1,word>>1,k]
    for (a,b),f in zip(circuit.gates,faults):
        wires.append(int(not(wires[a] and wires[b]))^f)
    return wires[circuit.output]


def independent_channel(circuit,gamma):
    out=[]
    for word in range(4):
        for k in range(2):
            value=F(0)
            for fs in product((0,1),repeat=circuit.cost):
                weight=gamma**sum(fs)*(1-gamma)**(circuit.cost-sum(fs))
                value+=weight*scalar_execution(circuit,word,k,fs)
            out.append(value)
    return tuple(out)


class FaultyUpdateTests(unittest.TestCase):
    def test_complete_raw_grammar_counts(self):
        lib,stats=complete_library()
        self.assertEqual([r['rooted_netlists'] for r in stats],[5,15,90,855,11430])
        self.assertEqual([r['terminal_channels'] for r in stats],[5,8,24,97,477])
        self.assertEqual(len(lib),611)
        self.assertTrue(any(len(set(c.gates))<len(c.gates) for c,_ in lib))

    def test_independent_scalar_oracle_all_two_gate_netlists(self):
        count=0
        for d in (1,2):
            for c in rooted_netlists(d):
                for word,k in product(range(4),range(2)):
                    for fs in product((0,1),repeat=d):
                        self.assertEqual(c.execute(word,k,fs),scalar_execution(c,word,k,fs));count+=1
                for gamma in (F(0),F(1,100),F(1,10),F(1,2)):
                    self.assertEqual(output_probabilities(c,gamma),independent_channel(c,gamma))
        self.assertEqual(count,3120)

    def test_channel_count_polynomial(self):
        for c,profile in complete_library()[0][::17]:
            powers=power_channel(profile)
            for row in profile:
                self.assertTrue(all(0<=count<=comb(c.cost,k) for k,count in enumerate(row)))
            for g in (F(0),F(1,1000),F(1,10),F(1,2)):
                expected=tuple(sum((F(a)*g**j for j,a in enumerate(row)),F(0)) for row in powers)
                self.assertEqual(expected,independent_channel(c,g))

    def test_shared_vs_separate_marginals_fail(self):
        r=shared_fault_witness()
        self.assertEqual(r['shared_marginals'],r['separate_marginals'])
        self.assertEqual(r['shared_output_error'],F(9,50))
        self.assertEqual(r['separate_output_error'],F(63,250))
        self.assertNotEqual(r['shared_joint'],r['separate_joint'])

    def test_joint_law_extension_matches_direct_network(self):
        for g in (F(0),F(1,100),F(1,10),F(1,2)):
            r=shared_fault_witness(g)
            for field,law in [('shared_circuit',r['shared_joint']),('separate_circuit',r['separate_joint'])]:
                extension=append_nand(law,(0,1),g)
                probability=sum((mass for values,mass in extension.items() if values[-1]),F(0))
                self.assertEqual(probability,output_probabilities(r[field],g)[0])
                self.assertEqual(sum(extension.values(),F(0)),1)

    def test_same_truth_different_physical_value(self):
        balanced=PhysicalCircuit(((1,4),(2,3),(1,6),(5,7)),8)
        sequential=PhysicalCircuit(((1,4),(2,5),(1,6),(3,7)),8)
        self.assertEqual(balanced.all_truths((0,)*4)[-1],sequential.all_truths((0,)*4)[-1])
        args=((3,0,0),F(1,100),F(1,100))
        self.assertLess(evaluate(balanced,*args),bypass_value())
        self.assertGreater(evaluate(sequential,*args),bypass_value())

    def test_noiseless_recovers_v13_frontier(self):
        for p in (F(0),F(1,100),F(1,10),F(1,2)):
            for cap in range(5):
                self.assertEqual(synthesize(p,F(0),capacity=cap)['value'],analytical_value(p,F(0),cap))

    def test_encoder_separability_against_independent_enumeration(self):
        for c,profile in complete_library()[0][::71]:
            p=F(1,100);g=F(1,200);q=F(1,1000)
            values={enc:evaluate(c,enc,p,g,q) for enc in product(range(4),repeat=3)}
            channel=independent_channel(c,g);T=payoff_table();enc=[]
            for y in range(3):
                score=[]
                for e in range(4):
                    total=F(0)
                    for word in range(4):
                        for k in range(2):
                            h=q+(1-2*q)*channel[2*word+k]
                            total+=transport_probability(e,word,p)*((1-h)*T[y][k][0]+h*T[y][k][1])
                    score.append(total)
                enc.append(max(range(4),key=lambda i:score[i]))
            self.assertEqual(evaluate(c,tuple(enc),p,g,q),max(values.values()))

    def test_complete_polynomial_certificate(self):
        c=fixed_input_certificate()
        self.assertEqual(c['programs_checked'],39104)
        self.assertEqual(c['distinct_polynomials'],8854)
        self.assertEqual(c['certified_leaves'],8854)
        for gamma in (F(0),F(1,10000),F(1,1000),F(1,200),F(1,100)):
            value=evaluate(c['circuit'],c['encoding'],c['p'],gamma)
            self.assertEqual(synthesize(c['p'],gamma)['value'],value)

    def test_bernstein_bounds_are_not_sampled_claims(self):
        self.assertEqual(prove_nonnegative((0,1,-1),0,1),1)
        self.assertEqual(prove_nonnegative((0,0,0),0,1),1)
        with self.assertRaises(ValueError):prove_nonnegative((-1,0),0,1,max_depth=2)

    def test_last_gate_bound_and_finite_no_go(self):
        for p in (F(0),F(1,100),F(1,10)):
            cutoff=last_gate_cutoff(p)
            self.assertEqual(last_gate_bound(p,cutoff),bypass_value())
            self.assertEqual(synthesize(p,F(1,50))['value'],bypass_value())
            for gamma in (F(0),F(1,1000),F(1,100)):
                self.assertLessEqual(synthesize(p,gamma)['value'],last_gate_bound(p,gamma))

    def test_signed_single_fault_derivative(self):
        c=PhysicalCircuit(((1,4),(2,5),(1,6),(3,7)),8)
        report=first_order_influences(c,(3,0,0));cert=fixed_input_certificate()
        self.assertEqual(report['uniform_noise_derivative_at_zero'],cert['rational_power_coefficients'][1])
        self.assertLess(report['gates'][-1]['signed_effect'],report['gates'][0]['signed_effect'])

    def test_fault_traces_complete_and_runtime_limited(self):
        c=PhysicalCircuit(((1,4),(2,5),(1,6),(3,7)),8)
        traces=runtime_fault_traces(c,3,0,F(1,100))
        self.assertEqual(len(traces),16)
        self.assertEqual(sum((t['probability'] for t in traces),F(0)),1)
        self.assertEqual(sum((t['probability']*t['output'] for t in traces),F(0)),output_probabilities(c,F(1,100))[6])
        self.assertTrue(all(set(t)=={'input','faults','probability','wires','output','command'} for t in traces))

    def test_terminal_law_not_safe_when_future_fault_correlated(self):
        shared={(0,0):F(1,2),(1,1):F(1,2)}
        independent={v:F(1,4) for v in product((0,1),repeat=2)}
        self.assertEqual(sum(p for (s,e),p in shared.items() if s),F(1,2))
        self.assertEqual(sum(p for (s,e),p in independent.items() if s),F(1,2))
        self.assertEqual(sum(p for (s,e),p in shared.items() if s^e),0)
        self.assertEqual(sum(p for (s,e),p in independent.items() if s^e),F(1,2))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):PhysicalCircuit(((2,5),),5)
        with self.assertRaises(ValueError):PhysicalCircuit(((3,2),),5)
        with self.assertRaises(ValueError):synthesize(F(3,4))
        with self.assertRaises(ValueError):complete_library(5)
        with self.assertRaises(ValueError):PhysicalCircuit().execute(4,0)

if __name__=='__main__':unittest.main()
