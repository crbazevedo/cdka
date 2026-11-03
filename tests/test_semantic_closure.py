"""Exact generative certificates and independent small-word/failure oracles."""
from fractions import Fraction as F
from itertools import product
import hashlib
from pathlib import Path
import unittest

from cdka.semantic_closure import (
    ExactBasis, apply, push, dot, vector, matrix, close_continuations,
    point, word_value, observation_masks, refine_lumping, quotient_matrix,
    plant_operators, delayed_fixture, feedback_fixture, rank_vs_states,
    delayed_chain, refinement_falsifier, lift_nuisance,
)
from cdka.composition import Contract, quotient, COST, macro_row, DEAD


class SemanticClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states, cls.ops, cls.labels = plant_operators(micro=True)
        cls.all = close_continuations(cls.ops, {'alive':[1]*len(cls.states)})

    def test_base_physical_contract_unchanged(self):
        body=Path('cdka/composition.py').read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        self.assertEqual(blob,'d2b9ccc2253b326af5d494b6d14c5dac6666105c')

    def test_symbolic_generation_exact_plant(self):
        c=self.all
        self.assertEqual(len(self.states),80)
        self.assertEqual(c.dimension,20)
        self.assertEqual(c.profile,(1,5,16,20,20))
        self.assertEqual(c.attempts,81)
        self.assertTrue(c.verify())
        classes=c.state_classes()
        self.assertEqual(len(classes),20)
        self.assertEqual({frozenset(quotient(self.states[i]) for i in g) for g in classes},
                         {frozenset((s,)) for s in Contract().states()})

    def test_quotient_found_without_supplying_hidden_health_partition(self):
        # The stable partition starts with only the actually readable (k,b).
        out=refine_lumping(self.ops,self.labels)
        self.assertEqual(len(out['blocks']),20)
        self.assertEqual(out['history'][0],10)
        for q in self.ops.values():
            reduced=quotient_matrix(q,out['blocks'])
            self.assertEqual(len(reduced),20)
        # Some blocks differ by hidden H despite the same current observation.
        # They are evaluator states, never free runtime input.
        self.assertLess(len(set(self.labels)),len(out['blocks']))

    def test_repertoire_changes_effective_rank(self):
        c=close_continuations({'hold':self.ops['hold']},{'alive':[1]*80})
        self.assertEqual(c.dimension,4)
        self.assertEqual(len(c.state_classes()),4)
        self.assertEqual(c.profile,(1,2,3,4,4))
        self.assertTrue(c.verify())
        # Health/syndrome persist; reservoir is irrelevant to HOLD-only survival.
        for i,s in enumerate(self.states):
            for j,t in enumerate(self.states):
                if quotient(s)[:2]==quotient(t)[:2]:
                    self.assertTrue(c.equivalent(point(80,i),point(80,j)))

    def test_full_words_against_basis_independent_enumeration(self):
        # Independent direct expansion of EVERY command word up to length 3.
        q=self.ops;g=vector([1]*80);checked=0
        for n in range(4):
            for word in product(q,repeat=n):
                v=word_value(q,word,g)
                coefficients=self.all.basis.coordinates(v)
                rebuilt=tuple(sum((a*b[i] for a,b in zip(coefficients,self.all.basis.originals)),F(0)) for i in range(80))
                self.assertEqual(v,rebuilt)
                checked+=1
        self.assertEqual(checked,85)

    def test_row_signature_updates_on_distributions(self):
        c=self.all;mu=vector([F(1,80)]*80)
        for label,q in self.ops.items():
            sig=c.signature(mu);b=c.reduced_operator(label)
            updated=tuple(sum((sig[i]*b[i][j] for i in range(c.dimension)),F(0)) for j in range(c.dimension))
            self.assertEqual(updated,c.signature(push(mu,q)))

    def test_shortest_composite_witness(self):
        names,ops,probes=delayed_fixture();c=close_continuations(ops,probes)
        x,y=point(4,0),point(4,1)
        for a in ops:
            self.assertEqual(dot(x,word_value(ops,(a,),probes['alive'])),
                             dot(y,word_value(ops,(a,),probes['alive'])))
        w=c.separator(x,y)
        self.assertEqual(w['word'],('prepare','check'))
        self.assertEqual((w['left'],w['right']),(1,0))
        self.assertFalse(c.equivalent(x,y))

    def test_order_cannot_be_removed_by_permuting_commands(self):
        names,ops,probes=delayed_fixture();y=point(4,1)
        self.assertEqual(dot(y,word_value(ops,('prepare','check'),probes['alive'])),0)
        self.assertEqual(dot(y,word_value(ops,('check','prepare'),probes['alive'])),1)

    def test_open_loop_equivalence_breaks_when_readable_feedback_allowed(self):
        states,q,observed,mu,nu=feedback_fixture()
        blind=close_continuations(q,{'alive':[1]*4})
        full=close_continuations(observed,{'alive':[1]*4})
        self.assertEqual(blind.dimension,2)
        self.assertEqual(full.dimension,4)
        self.assertTrue(blind.equivalent(mu,nu))
        self.assertFalse(full.equivalent(mu,nu))
        feedback=tuple(word_value(observed,('observe:0','act0'),[1]*4)[i]+
                       word_value(observed,('observe:1','act1'),[1]*4)[i] for i in range(4))
        self.assertEqual(dot(mu,feedback),1)
        self.assertEqual(dot(nu,feedback),F(1,2))
        self.assertIsNotNone(full.separator(mu,nu))

    def test_observation_contingent_two_step_policies_on_same_plant(self):
        st,ops,labels=plant_operators(masks=True)
        c=close_continuations(ops,{'alive':[1]*len(st)})
        self.assertEqual(c.dimension,20)
        self.assertTrue(c.verify())
        # All 64 two-epoch plans from the original fixed initial b=4.
        from cdka.continuation_interfaces import plans
        p=Contract();lib=plans(p,b=4)
        self.assertEqual(len(lib),64)
        for plan in lib:
            for h in (0,1):
                initial=(0,h,4)
                result=F(0)
                for s,mass in macro_row(p,initial,plan.first).items():
                    if s==DEAD: continue
                    a=plan.action_after((s[0],s[2]))
                    result+=mass*sum((q for t,q in macro_row(p,s,a).items() if t!=DEAD),F(0))
                self.assertEqual(result,plan.alpha[h])

    def test_exact_rank_is_not_physical_code_cardinality(self):
        q,g=rank_vs_states(17);c=close_continuations(q,g)
        self.assertEqual(c.dimension,2)
        self.assertEqual(len(c.state_classes()),17)
        self.assertTrue(c.verify())

    def test_no_universal_collapse_delayed_chain(self):
        for n in range(1,13):
            q,g=delayed_chain(n);c=close_continuations(q,g)
            self.assertEqual(c.dimension,n)
            self.assertEqual(len(c.state_classes()),n)
            self.assertTrue(c.verify())
        q,g=delayed_chain(9);c=close_continuations(q,g)
        w=c.separator(point(9,0),point(9,1))
        self.assertEqual(len(w['word']),8)

    def test_linear_signature_does_not_imply_stochastic_quotient(self):
        q,g=refinement_falsifier();c=close_continuations(q,g)
        self.assertEqual(c.dimension,3)
        self.assertTrue(c.equivalent(point(5,3),point(5,4)))
        with self.assertRaises(ValueError):
            quotient_matrix(q['step'],c.state_classes())
        self.assertEqual(len(refine_lumping(q,[0]*5)['blocks']),5)
        self.assertTrue(c.verify())

    def test_constructive_nuisance_elimination_without_trace_enumeration(self):
        core={'stay':matrix([{0:F(3,4),1:F(1,8)},{1:F(1,2)}]),
              'repair':matrix([{0:F(4,5)},{0:F(2,3)}])}
        small=close_continuations(core,{'alive':[1,1]})
        self.assertEqual(small.dimension,2)
        for multiplicity in (1,2,5,16,64):
            big=lift_nuisance(core,multiplicity)
            c=close_continuations(big,{'alive':[1]*(2*multiplicity)})
            self.assertEqual(c.dimension,2)
            self.assertEqual(c.attempts,5)
            self.assertEqual(len(c.state_classes()),2)
            self.assertTrue(c.verify())
            for label,q in big.items():
                blocks=(tuple(range(multiplicity)),tuple(range(multiplicity,2*multiplicity)))
                self.assertEqual(quotient_matrix(q,blocks),core[label])

    def test_semantic_equality_is_not_merely_common_safe_action(self):
        A=({0,1},{1,2},{0,2})
        self.assertTrue(all(A[i]&A[j] for i in range(3) for j in range(i+1,3)))
        self.assertFalse(set.intersection(*A))
        # Operational compatibility lacks transitivity even in simpler cases.
        B=({0},{0,1},{1})
        self.assertTrue(B[0]&B[1]);self.assertTrue(B[1]&B[2]);self.assertFalse(B[0]&B[2])

    def test_exact_rational_random_systems_against_word_oracle(self):
        # Reproducible 48 small kernels, no probability simulations.
        checked=0
        for k in range(48):
            q={}
            for ai in range(2):
                rows=[]
                for i in range(3):
                    a=(k+2*i+ai)%4;b=(2*k+i+3*ai)%4
                    row={i:F(a,8),(i+1)%3:F(b,8)}
                    rows.append(row)
                q[str(ai)]=matrix(rows)
            c=close_continuations(q,{'alive':[1]*3});self.assertTrue(c.verify())
            for length in range(5):
                for word in product(q,repeat=length):
                    v=word_value(q,word,[1]*3)
                    c.basis.coordinates(v);checked+=1
            self.assertLessEqual(c.attempts,1+2*3)
        self.assertEqual(checked,48*31)

    def test_invalid_contracts_rejected(self):
        with self.assertRaises(ValueError):matrix([{0:2}])
        with self.assertRaises(ValueError):matrix([{0:-1}])
        with self.assertRaises(ValueError):close_continuations({}, {})
        with self.assertRaises(ValueError):close_continuations({'a':matrix([{0:1}])},{'x':[1,1]})


if __name__=='__main__':unittest.main()
