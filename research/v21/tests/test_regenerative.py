from fractions import Fraction as F
from itertools import product
from collections import defaultdict,Counter
from dataclasses import replace
from pathlib import Path
import math,random,re,unittest
import numpy as np
from cdka.regenerative import *

class RegenerationTests(unittest.TestCase):
    def test_partition_histogram_bijection(self):
        for h in range(18):
            parts=list(run_partitions(h))
            self.assertEqual(len(parts),partition_number(h+1)-1)
            self.assertEqual(len({p for p,m in parts}),len(parts))
            for p,m in parts:
                self.assertLessEqual(sum(p)+len(p)-1,h)
                self.assertEqual(tuple(sorted(p)),p)
                self.assertEqual(m,math.factorial(len(p))//math.prod(math.factorial(c) for c in Counter(p).values()))
    def test_exact_all_history_weights_not_only_values(self):
        for nu in ((F(1),F(0)),(F(1,3),F(2,3)),(F(0),F(1))):
            m=meeting_restart(1,initial_environment=nu)
            for h in range(1,9):
                _,groups=path_oracle(m,h,True)
                computed={p:mul*base_weight_exact(m,h,sum(p),len(p)) for p,mul in run_partitions(h)}
                computed[()]=nu[1]*m.environment[1][1]**(h-1)
                self.assertEqual(sum(computed.values(),F(0)),1)
                for p,g in groups.items():self.assertEqual(g['weight'],computed[p])
    def test_exact_three_independent_algorithms(self):
        count=0
        for n in (1,2,3):
            m=meeting_restart(n)
            for h in range(8):
                a=exact_histogram_value(m,h)
                self.assertEqual(a,path_oracle(m,h))
                self.assertEqual(a,renewal_subset_baseline(m,h,True));count+=1
        self.assertEqual(count,24)
    def test_joint_state_oracle(self):
        for nu in ((F(1),F(0)),(F(1,2),F(1,2))):
            m=meeting_restart(2,initial_environment=nu)
            for h in range(6):self.assertEqual(exact_histogram_value(m,h),joint_oracle(m,h))
    def test_production_against_generic_tensor(self):
        for n in range(1,6):
            m=meeting_restart(n);c=compile_model(m)
            for h in (0,1,2,4,7,10):
                a=c.evaluate(h)['probability'];b=tensor_baseline(m,h)
                self.assertTrue(math.isclose(a,b,rel_tol=5e-12,abs_tol=5e-15),(n,h,a,b))
    def test_v20_count_equivalence_really_fails(self):
        m=meeting_restart(2)
        self.assertNotEqual(word_response(m,(0,0,1)),word_response(m,(0,1,0)))
        w=noncommutation_witness(m.components[0]);self.assertIsNotNone(w)
        self.assertNotEqual(w['left'],w['right'])
    def test_histogram_keeps_order_boundaries(self):
        m=meeting_restart(2)
        a=(0,0,1,0,1);b=(0,1,1,0,0)
        self.assertEqual(tuple(sorted(work_runs(a))),tuple(sorted(work_runs(b))))
        self.assertEqual(word_response(m,a),word_response(m,b))
        self.assertNotEqual(word_probability(m,a),word_probability(m,b))
    def test_last_reset_does_not_erase_completed_jobs(self):
        c=Local(mat([[0,1,0],[0,0,1],[0,0,1]]),mat([[1,0,0],[1,0,0],[0,0,1]]),vector([1,0,0]),(2,))
        m=Model((c,))
        self.assertEqual(work_runs((0,0,1,1,0))[-1],work_runs((0,1,1,1,0))[-1])
        self.assertEqual(word_response(m,(0,0,1,1,0)),1)
        self.assertEqual(word_response(m,(0,1,1,1,0)),0)
    def test_random_rational_transient_components(self):
        rng=random.Random(20261107);checks=0
        for _ in range(24):
            cs=[]
            for j in range(1+_%2):
                raw=[]
                for i in range(2):
                    nums=[rng.randrange(1,8) for k in range(3)];s=sum(nums);raw.append([F(x,s) for x in nums])
                raw.append([0,0,1]);p=F(rng.randrange(1,5),5);alpha=vector([p,1-p,0])
                cs.append(Local(mat(raw),(alpha,alpha,vector([0,0,1])),alpha,(2,)))
            a,b=F(rng.randrange(6),5),F(rng.randrange(6),5)
            m=Model(tuple(cs),mat([[a,1-a],[b,1-b]]),vector([F(2,5),F(3,5)]))
            for h in (2,4,6):
                self.assertEqual(exact_histogram_value(m,h),path_oracle(m,h));checks+=1
        self.assertEqual(checks,72)
    def test_degenerate_environment_transitions(self):
        for a,b in product((F(0),F(1)),repeat=2):
            for nu in ((F(1),F(0)),(F(0),F(1))):
                m=meeting_restart(2,[[a,1-a],[b,1-b]],nu)
                for h in (1,4,7):
                    exact=exact_histogram_value(m,h)
                    self.assertEqual(exact,path_oracle(m,h))
                    self.assertAlmostEqual(float(exact),compile_model(m).evaluate(h)['probability'],14)
    def test_more_than_one_absorbing_goal_state(self):
        P=mat([[F(1,2),F(1,4),F(1,8),F(1,8)],[F(1,4),F(1,4),F(1,4),F(1,4)],[0,0,F(1,2),F(1,2)],[0,0,0,1]])
        R=mat([[1,0,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
        m=Model((Local(P,R,vector([1,0,0,0]),(2,3)),))
        for h in range(6):self.assertEqual(exact_histogram_value(m,h),path_oracle(m,h))
    def test_original_external_parameters_first_twelve(self):
        txt=(Path(__file__).resolve().parents[1]/'external/meeting-12.prism').read_text()
        for i,c in enumerate(meeting_restart(12).components,1):
            p=F(re.search(fr'const double p{i}=([0-9.]+);',txt)[1])
            q=F(re.search(fr'const double q{i}=([0-9.]+);',txt)[1])
            self.assertEqual(c.work,mat([[1-p,p,0],[1-q,0,q],[0,0,1]]))
    def test_prism_complete_roundtrip(self):
        for n in (1,2,4,8,12):
            model=meeting_restart(n);text=render_prism(model);comp=parse_prism(text)
            self.assertEqual(comp.model,model)
            self.assertEqual(comp.certificate['source_sha256'],sha256(text.encode()).hexdigest())
    def test_refuse_cross_reads_unknown_source_and_goal(self):
        text=render_prism(meeting_restart(2))
        for bad in (text+'\n rewards "x" true:1; endrewards',text.replace('e=0 & s1=0','e=0 & s1=0 & s2=0'),text.replace('[step]','[other]',1),text.replace('(s1=2) & (s2=2)','(s1=2) | (s2=2)'),text.replace('module P2','module P1')):
            with self.assertRaises((ValueError,ZeroDivisionError)):parse_prism(bad)
    def test_reset_not_rank_one_rejected(self):
        m=meeting_restart(1);c=m.components[0]
        bad=replace(c,restart=mat([[1,0,0],[0,1,0],[0,0,1]]))
        with self.assertRaises(ContractError):compile_model(replace(m,components=(bad,)))
    def test_initial_and_reset_distribution_must_match(self):
        m=meeting_restart(1);c=m.components[0]
        with self.assertRaises(ContractError):compile_model(replace(m,components=(replace(c,initial=vector([0,1,0])),)))
    def test_reset_must_not_destroy_completion(self):
        m=meeting_restart(1);c=m.components[0]
        with self.assertRaises(ContractError):compile_model(replace(m,components=(replace(c,restart=mat([[1,0,0]]*3)),)))
    def test_all_work_agrees_with_independent_finite_chains(self):
        m=meeting_restart(3,[[1,0],[0,1]])
        for h in (2,4,8):
            expected=math.prod(1-local_survival_exact(c,h)[h] for c in m.components)
            self.assertEqual(expected,exact_histogram_value(m,h))
    def test_product_of_marginals_loses_common_history(self):
        m=meeting_restart(2)
        exact=exact_histogram_value(m,6)
        product_of_means=math.prod(exact_histogram_value(replace(m,components=(c,)),6) for c in m.components)
        self.assertNotEqual(exact,product_of_means)
    def test_compiled_does_not_construct_global_tensor(self):
        m=meeting_restart(1000);c=compile_model(m);r=c.evaluate(12)
        self.assertTrue(math.isfinite(r['log_probability']))
        self.assertEqual(r['histogram_classes'],partition_number(13))
        self.assertEqual(len({x.work for x in m.components}),1000)
    def test_all_queries_validate_horizon_even_optimized_python(self):
        m=meeting_restart(1);c=compile_model(m)
        for h in (-1,True,1.5):
            for fun in (lambda:c.evaluate(h),lambda:exact_histogram_value(m,h),lambda:path_oracle(m,h),lambda:tensor_baseline(m,h)):
                with self.assertRaises(ContractError):fun()
        with self.assertRaises(ContractError):c.evaluate(100)
    def test_dependency_flags_and_bad_dimensions_rejected(self):
        m=meeting_restart(1)
        for field in ('exogenous_environment','conditional_product_noise','independent_initial','synchronous'):
            with self.assertRaises(ContractError):compile_model(replace(m,**{field:False}))
        for env in (mat([[F(1,2),F(1,4)],[0,1]]),mat([[1]])):
            with self.assertRaises(ContractError):compile_model(replace(m,environment=env))
        with self.assertRaises(ContractError):compile_model(replace(m,initial_environment=vector([1,0,0])))
        with self.assertRaises(ContractError):compile_model(replace(m,components=()))

if __name__=='__main__':unittest.main()
