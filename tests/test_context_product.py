import unittest, random, hashlib
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import numpy as np
from cdka.context_product import *


def independent_weights(R,alpha,H):
    out=[F(0)]*(H+1)
    if H==0:return (F(1),)
    for path in product((0,1),repeat=H):
        p=alpha[path[0]]
        for a,b in zip(path,path[1:]):p*=R[a][b]
        out[sum(path)]+=p
    return tuple(out)


def kron(A,B):
    return tuple(tuple(A[i][j]*B[r][s] for j in range(len(A)) for s in range(len(B)))
                 for i in range(len(A)) for r in range(len(B)))


class ContextProductTests(unittest.TestCase):
    def test_shared_context_is_not_independent_product(self):
        ir=meeting(2);H=5;c=compile_context(ir)
        actual=c.exact(H)
        wrong=prod(compile_context(ContextIR((local,),ir.environment)).exact(H) for local in ir.components)
        self.assertNotEqual(actual,wrong)
        self.assertEqual(actual,raw_global_exact(ir,H))

    def test_original_storm_models_have_identical_bytes(self):
        expected={2:'d09479851f4fd0e76af9c751f83e8da4cf8c9d277dff9a793f6b2ea396791db8',
          4:'5ade86d2e68d5b0a852fca274bca2589a79fbf7f2f22667c7cf26ce6dae49bd1',
          6:'cc4749f67bccfbf8e04aceaa9eb5d830ef35df02cc274828971be3540b1a2f2d',
          8:'f44a2da20cc39e480e60a37f36673351a420db904324a7ec434481f7da1648e4'}
        for n,sha in expected.items():
            text=render_prism(meeting(n))
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),sha)
            compile_context(parse_prism(text))

    def test_recovered_official_solver_values(self):
        rows=[(2,10,.012079766554395514),(4,10,.0008608097758093338),
          (6,10,.0001532153556742773),(8,10,4.735172000847746e-05),
          (6,50,.11963305989109549)]
        for n,H,value in rows:
            self.assertAlmostEqual(compile_context(parse_prism(render_prism(meeting(n)))).evaluate(H)['probability'],value,places=14)

    def test_three_independent_oracles_on_small_instances(self):
        count=0
        for n in (1,2,3):
            for H in range(7):
                ir=meeting(n);c=compile_context(ir);exact=c.exact(H)
                self.assertEqual(exact,raw_global_exact(ir,H))
                self.assertEqual(exact,path_exact(ir,H));count+=1
        self.assertEqual(count,21)

    def test_numerical_tensor_keeps_global_dependence(self):
        for n in range(1,7):
            for H in (0,1,2,5,10):
                ir=meeting(n)
                self.assertAlmostEqual(compile_context(ir).evaluate(H)['probability'],global_tensor(ir,H),14)

    def test_occupation_dp_counts_correct_current_context(self):
        R=mat([[F(2,3),F(1,3)],[F(1,4),F(3,4)]])
        for alpha in ((F(1),F(0)),(F(0),F(1)),(F(2,5),F(3,5))):
            for H in range(9):
                w=occupation_weights(R,alpha,H,True)
                self.assertEqual(w,independent_weights(R,alpha,H))
                self.assertEqual(sum(w),1)
                self.assertTrue(np.allclose(np.array(w,float),occupation_weights(R,alpha,H),atol=1e-14,rtol=0))

    def test_initial_world_zero_time_general_case(self):
        c=Component.make('x',[[1,0],[0,1]],[[1,0],[0,1]],(F(1,3),F(2,3)),(1,))
        ir=ContextIR((c,),context_initial=(F(1,4),F(3,4)))
        a=compile_context(ir)
        self.assertEqual(a.exact(0),F(2,3));self.assertAlmostEqual(a.evaluate(0)['probability'],2/3)
        self.assertEqual(a.exact(4),F(2,3))

    def test_single_time_conditioned_product(self):
        ir=replace(meeting(2),context_initial=(F(1,3),F(2,3)))
        self.assertEqual(compile_context(ir).exact(1),path_exact(ir,1))

    def test_no_commutation_order_witness(self):
        A=mat([[0,1,0],[0,1,0],[0,0,1]])
        B=mat([[1,0,0],[0,0,1],[0,0,1]])
        g=(F(0),F(0),F(1));mu=(F(1),F(0),F(0))
        self.assertEqual(sum(a*b for a,b in zip(mu,mv(A,mv(B,g)))),1)
        self.assertEqual(sum(a*b for a,b in zip(mu,mv(B,mv(A,g)))),0)
        ir=ContextIR((Component.make('x',A,B,mu,(2,)),))
        with self.assertRaisesRegex(ContractViolation,'order affects goal'):
            compile_context(ir)

    def test_task_relative_commutation_accepts_noncommuting_dynamics(self):
        core=meeting(1).components[0]
        R0=mat([[1,0],[1,0]])
        R1=mat([[0,1],[1,0]])
        P0=kron(core.kernels[0],R0);P1=kron(core.kernels[1],R1)
        self.assertNotEqual(mm(P0,P1),mm(P1,P0))
        comp=Component.make('core_x_aux',P0,P1,(1,0,0,0,0,0),(4,5))
        ir=ContextIR((comp,));compiled=compile_context(ir)
        rec=compiled.certificate['local_records'][0]
        self.assertEqual(rec['certificate'],'commutation on invariant goal space')
        self.assertEqual(rec['goal_space_dimension'],3)
        for H in range(7):
            self.assertEqual(compiled.exact(H),path_exact(ir,H))
            self.assertEqual(compiled.exact(H),compile_context(ContextIR((core,))).exact(H))
        with self.assertRaises(ContractViolation):compile_context(ir,task_relative=False)

    def test_same_counts_have_different_weights_not_different_response(self):
        ir=meeting(1);c=ir.components[0];g=(F(0),F(0),F(1))
        paths=[(0,0,1),(0,1,0)]
        response=[];weights=[]
        for p in paths:
            v=c.initial
            for z in p:v=vm(v,c.kernels[z])
            response.append(sum((v[i] for i in c.target),F(0)))
            weights.append(ir.context_initial[p[0]]*prod(ir.environment[a][b] for a,b in zip(p,p[1:])))
        self.assertEqual(response[0],response[1]);self.assertNotEqual(weights[0],weights[1])

    def test_random_rational_families(self):
        rng=random.Random(172903);cases=0
        for trial in range(32):
            cs=[]
            for i in range(1+trial%2):
                p=F(rng.randint(1,8),10);q=F(rng.randint(1,8),10)
                P=mat([[1-p,p,0],[1-q,0,q],[0,0,1]])
                coeff=(F(rng.randint(1,9),10),F(rng.randint(1,9),10))
                K=tuple(tuple(tuple((1-a)*int(r==s)+a*P[r][s] for s in range(3)) for r in range(3)) for a in coeff)
                cs.append(Component.make(str(i),*K,(1,0,0),(2,)))
            a=F(rng.randint(1,8),10);b=F(rng.randint(1,8),10);pi=F(rng.randint(0,10),10)
            ir=ContextIR(tuple(cs),mat([[a,1-a],[b,1-b]]),(pi,1-pi));cmp=compile_context(ir)
            for H in range(5):
                self.assertEqual(cmp.exact(H),raw_global_exact(ir,H))
                self.assertEqual(cmp.exact(H),path_exact(ir,H));cases+=1
        self.assertEqual(cases,160)

    def test_parser_rejects_nonlocal_guard(self):
        text=render_prism(meeting(2)).replace('e=0 & s1=0','e=0 & s2=0',1)
        with self.assertRaises(ContractViolation):compile_context(parse_prism(text))

    def test_parser_rejects_nonlocal_write_or_extra_query(self):
        t=render_prism(meeting(2))
        for text in (t.replace("s1'=0","s2'=0",1),t+' rewards "x" true:1; endrewards',t.replace('[step]','[other]',1)):
            with self.assertRaises(ContractViolation):parse_prism(text)

    def test_bad_goals_and_nonabsorbing_rejected(self):
        c=meeting(1).components[0]
        for targets in ((),(3,),(-1,),(2,2),(True,)):
            with self.assertRaises(ContractViolation):compile_context(ContextIR((replace(c,target=targets),)))
        bad=Component.make('bad',[[F(1,2),F(1,2)],[1,0]],[[1,0],[1,0]],(1,0),(1,))
        with self.assertRaisesRegex(ContractViolation,'nonabsorbing'):compile_context(ContextIR((bad,)))

    def test_contract_rejections(self):
        ir=meeting(1)
        for kw in ({'initial_product':False},{'conditional_noise_independent':False},
                   {'exogenous_environment':False},{'cartesian_goal':False},{'scheduler':'interleaved'}):
            with self.assertRaises(ContractViolation):compile_context(replace(ir,**kw))
        with self.assertRaises(ContractViolation):compile_context(ContextIR(()))
        with self.assertRaises(ContractViolation):compile_context(replace(ir,components=ir.components*2))

    def test_stochastic_inputs_validate_before_algebra(self):
        ir=meeting(1);c=ir.components[0]
        with self.assertRaises(ContractViolation):compile_context(replace(ir,context_initial=(F(1),F(1))))
        with self.assertRaises(ContractViolation):compile_context(replace(ir,environment=((1,1),(0,1))))
        with self.assertRaises(ContractViolation):compile_context(ContextIR((replace(c,initial=(1,0)),)))
        with self.assertRaises(ContractViolation):compile_context(ContextIR((replace(c,kernels=(mat([[1,0],[0,1]]),)*2),)))

    def test_horizon_validation_all_evaluators(self):
        c=compile_context(meeting(1))
        for H in (-1,1.2,True,'3'):
            for fun in (c.evaluate,c.exact,lambda h:raw_global_exact(c.ir,h),lambda h:path_exact(c.ir,h),lambda h:global_tensor(c.ir,h)):
                with self.assertRaises(ValueError):fun(H)

    def test_constant_context_recovers_v19(self):
        ir=replace(meeting(3),environment=mat([[1,0],[0,1]]),context_initial=(F(0),F(1)))
        product_value=F(1)
        for c in ir.components:
            v=c.initial
            for _ in range(7):v=vm(v,c.kernels[1])
            product_value*=sum((v[j] for j in c.target),F(0))
        self.assertEqual(compile_context(ir).exact(7),product_value)

    def test_mass_not_renormalized_to_survivors(self):
        c=compile_context(meeting(3));out=c.evaluate(5)
        self.assertAlmostEqual(float(out['occupation_weights'].sum()),1,14)
        self.assertLess(out['probability'],.01)
        self.assertEqual(c.exact(5),raw_global_exact(c.ir,5))

    def test_parser_empty_environment_and_trailing_illegal(self):
        with self.assertRaises(ContractViolation):parse_prism('dtmc module environment e:[0..1] init 0; [step] e=0 -> (1/1):(e\'=0); [step] e=1 -> (1/1):(e\'=1); endmodule label "goal" = ;')
        with self.assertRaises(ContractViolation):parse_prism(render_prism(meeting(1)).replace('dtmc','mdp',1))

if __name__=='__main__':unittest.main()
