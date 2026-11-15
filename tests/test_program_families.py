"""Proof-boundary tests for the exact, inductive program-family cover."""
from copy import deepcopy
from fractions import Fraction as F
import unittest
from unittest.mock import patch

from cdka.maintenance_access import base_operators, base_probes
from cdka.program_families import (
    compile_family, check_family, unpruned_shared, evaluate_frontier,
    compile_decision, check_decision, transports, transport, dominated,
)
from cdka.reachable_diagnosis import preparation_laws, plan_words
from cdka.reachable_restriction import (
    CONTRAST_BASIS, collapse, contrast_response, contrast_signature,
    contrast_domain_preservation, expand_contrast,
)
from cdka.semantic_closure import apply, push, word_value


class ProgramFamiliesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ops=base_operators()
        cls.g=base_probes()['readout']
        cls.frontier,cls.certificate,cls.stats=compile_family(cls.ops,cls.g,4)
        cls.full=unpruned_shared(cls.ops,cls.g,4)
        cls.cohorts={h:preparation_laws(h) for h in (2,4)}
        cls.signatures={h:[contrast_signature(*law) for law in cohort.values()]
                        for h,cohort in cls.cohorts.items()}

    def test_complete_response_algebra_agrees_with_full_physics(self):
        self.assertEqual({w for w,_ in self.full},
                         {''.join(w) for w in plan_words(4)})
        for word,response in self.full:
            self.assertEqual(response,contrast_response(word_value(self.ops,word,self.g)))
        for _,response in self.full:
            self.assertTrue(any(dominated(other,response) for _,other in self.frontier))

    def test_checker_covers_unconstructed_families_without_pareto_discovery(self):
        with patch('cdka.program_families._cover',side_effect=AssertionError('discovery forbidden')):
            self.assertEqual(check_family(self.certificate,self.ops,self.g,4),self.frontier)
        last=self.stats[-1]
        self.assertEqual((last['candidates'],last['retained']), (34,10))
        self.assertEqual((last['complete_words_generated'],last['complete_words_never_generated']), (44,52))
        self.assertEqual(sum((last['complete_words_generated'],last['complete_words_never_generated'])),96)

    def test_nonminimal_covers_are_valid_certificates(self):
        front,certificate,_=compile_family(self.ops,self.g,2,prune=False)
        self.assertEqual(len(front),16)
        self.assertEqual(check_family(certificate,self.ops,self.g,2),front)
        # The proof establishes coverage, not that Pareto discovery was rerun.
        certificate=deepcopy(certificate)
        n=len(certificate['layers'][-1]['keep'])
        certificate['layers'][-1]['keep'].reverse()
        certificate['layers'][-1]['cover']=[n-1-i for i in certificate['layers'][-1]['cover']]
        self.assertEqual(check_family(certificate,self.ops,self.g,2),list(reversed(front)))

    def test_all_decision_objectives_and_joint_feasibility_are_preserved(self):
        for h,signatures in self.signatures.items():
            results=[]
            for entries in (self.full,self.frontier):
                values=evaluate_frontier(entries,signatures)
                kw={'preparation_labels':list(self.cohorts[h]),
                    'plan_labels':[w or 'I' for w,_ in entries], 'contract':{'h':h,'k':4}}
                cert=compile_decision(values,**kw)
                self.assertTrue(check_decision(cert,values,**kw))
                best=tuple(map(F,cert['preparation_best']))
                gates=[]
                for delta,floor in ((F(1,500),F(21,25)),(F(3,1000),F(21,25)),
                                    (F(3,1000),F(17,20)),(F(1,200),F(17,20))):
                    gates.append(any(max(b-row[j] for b,row in zip(best,values))<=delta and
                                     min(row[j] for row in values)>=floor
                                     for j in range(len(entries))))
                results.append((cert['preparation_best'],cert['minimax_regret'],
                                cert['maximin_fidelity'],gates))
                if h==2:
                    self.assertEqual(entries[cert['minimax_plan']][0],'DRDDM')
                    self.assertEqual(entries[cert['maximin_plan']][0],'DDDDM')
                    self.assertEqual(gates,[False,True,False,True])
            self.assertEqual(results[0],results[1])

    def test_preparation_cone_guard_and_uninformative_sensor_boundary(self):
        for signatures in self.signatures.values():
            self.assertTrue(all(all(x<=0 for x in signed) for _,signed in signatures))
        for invalid in ((F(1),F(0),F(0),F(0)),(F(-1),F(1),F(0),F(0))):
            with self.assertRaises(ValueError):
                evaluate_frontier(self.frontier,[(F(1,2),invalid)])
        cohort=preparation_laws(2,eta=F(1,2))
        values=evaluate_frontier(self.frontier,[contrast_signature(*law) for law in cohort.values()])
        self.assertTrue(all(v==F(1,2) for row in values for v in row))
        kw={'preparation_labels':list(cohort),'plan_labels':[w for w,_ in self.frontier]}
        cert=compile_decision(values,**kw)
        self.assertEqual(F(cert['minimax_regret']),0)
        self.assertTrue(check_decision(cert,values,**kw))
        self.assertLess(len(self.frontier),len(self.full))  # All ties are not retained.

    def test_maintenance_bridge_is_full_sixteen_dimensional(self):
        A=transports(self.ops)
        self.assertTrue(all(x>=0 for a in ('D','R') for row in A[a] for x in row))
        self.assertFalse(contrast_domain_preservation(self.ops['M'])['preserved'])
        for word in ('','D','R','RDR'):
            full=word_value(self.ops,word,self.g)
            self.assertEqual(transport(A['M_boundary'],full),
                             contrast_response(apply(self.ops['M'],full)))
        bad=deepcopy(self.certificate)
        bad['transports']['M_boundary']=[
            [str(x) for x in expand_contrast(tuple(collapse(push(e,self.ops['M']))[j]
                                                  for j in (0,1,4,5)))]
            for e in CONTRAST_BASIS]
        with self.assertRaises(ValueError):
            check_family(bad,self.ops,self.g,4)

    def test_moving_maintenance_to_the_end_is_not_a_valid_rewrite(self):
        signature=contrast_signature(*self.cohorts[4]['DDDD'])
        entries=[(w,contrast_response(word_value(self.ops,w,self.g))) for w in ('MR','RM')]
        mr,rm=evaluate_frontier(entries,[signature])[0]
        self.assertGreater(mr,rm)

    def test_zero_repair_still_has_exact_cover(self):
        ops=base_operators(F(0))
        front,certificate,_=compile_family(ops,self.g,2)
        self.assertEqual(check_family(certificate,ops,self.g,2),front)
        for word in plan_words(2):
            response=contrast_response(word_value(ops,word,self.g))
            self.assertTrue(any(dominated(q,response) for _,q in front))
        with self.assertRaises(ValueError):
            check_family(self.certificate,ops,self.g,4)

    def test_cover_rejects_false_and_malformed_witnesses(self):
        mutations=[]
        c=deepcopy(self.certificate);c['layers'][0]['cover'][1]=0;mutations.append(c)
        c=deepcopy(self.certificate);c['layers'][-1]['cover'].pop();mutations.append(c)
        c=deepcopy(self.certificate);c['layers'][0]['cover'][0]=False;mutations.append(c)
        c=deepcopy(self.certificate);c['layers'][0]['keep']=[0,0];mutations.append(c)
        c=deepcopy(self.certificate);c['layers'][0]['cover'][0]=99;mutations.append(c)
        c=deepcopy(self.certificate);c['layers'][0]=None;mutations.append(c)
        c=deepcopy(self.certificate);c['layers']=None;mutations.append(c)
        c=deepcopy(self.certificate);c['ordinary_updates']=4.0;mutations.append(c)
        c=deepcopy(self.certificate);c['transports']['D'][0].pop();mutations.append(c)
        c=deepcopy(self.certificate);c['transports']['M_boundary'][0][0]='1/0';mutations.append(c)
        for value in (0.0,False,'0.0','0/1'):
            c=deepcopy(self.certificate);c['transports']['D'][2][0]=value;mutations.append(c)
        for c in mutations:
            with self.subTest(c=c),self.assertRaises(ValueError):
                check_family(c,self.ops,self.g,4)
        with self.assertRaises(ValueError):
            check_family(self.certificate,self.ops,self.g,True)

    def test_compact_decision_proof_is_bound_to_values_labels_and_scope(self):
        values=((F(4,5),F(7,10),F(1,10)),(F(7,10),F(4,5),F(1,10)))
        kw={'preparation_labels':['a','b'],'plan_labels':['p','q','r'],'contract':{'k':1}}
        cert=compile_decision(values,**kw)
        self.assertTrue(check_decision(cert,values,**kw))
        # The changed dominated response leaves the optimum unchanged. Its digest must still fail.
        changed=(values[0][:2]+(F(1,5),),values[1])
        for matrix,args in ((changed,kw),(values,{**kw,'plan_labels':['q','p','r']}),
                            (values,{**kw,'contract':{'k':2}})):
            with self.assertRaises(ValueError):
                check_decision(cert,matrix,**args)

    def test_compact_decision_rejects_false_bounds_and_numeric_types(self):
        values=((F(4,5),F(7,10),F(1,10)),(F(7,10),F(4,5),F(1,10)))
        kw={'preparation_labels':['a','b'],'plan_labels':['p','q','r']}
        cert=compile_decision(values,**kw)
        for key,value in (('minimax_regret','1/20'),('minimax_regret','1/5'),
                          ('maximin_fidelity','69/100'),('maximin_fidelity','71/100'),
                          ('minimax_plan',True),('maximin_plan',-1),
                          ('regret_lower_witness',[False,0,0]),
                          ('preparation_best_plans',[True,1]),
                          ('preparation_best',{'4/5':0}),
                          ('fidelity_upper_witness',[0]),('minimax_regret',0.1),
                          ('maximin_fidelity',True)):
            bad=deepcopy(cert);bad[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):
                check_decision(bad,values,**kw)
        bad=deepcopy(cert);bad['regret_lower_witness'][0]=0
        with self.assertRaises(ValueError):
            check_decision(bad,values,**kw)


if __name__=='__main__':
    unittest.main()
