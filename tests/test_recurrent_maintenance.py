from fractions import Fraction as F
from itertools import product
import unittest
from cdka.recurrent_maintenance import (
    Model,Policy,policies,BITS,VOTER,gate_execution,voter,task_success,
    raw_task_success,emission,micro_to_phase,physical_row,reduced_row,raw_row,
    push,initial_phase,initial_micro,forward,vector_value,all_stationary,
    event_traces,run_summary,select_probability,
)


class RecurrentMaintenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.p=Model()

    def test_frozen_v15_physical_voter(self):
        from cdka.boundary_voting import VOTER as OLD,BITS as OLD_BITS,voter_table
        self.assertEqual(VOTER,OLD)
        for rate in (self.p.healthy_error,self.p.degraded_error,F(1,10)):
            self.assertEqual(tuple(voter(bits,rate) for bits in BITS),voter_table(rate))
        self.assertEqual(BITS,OLD_BITS)

    def test_independent_work_fault_enumeration(self):
        for z in (0,1):self.assertEqual(task_success(self.p,z),raw_task_success(self.p,z))
        self.assertLess(task_success(self.p,1),task_success(self.p,0))
        self.assertLess(task_success(self.p,0),1)

    def test_state_and_policy_inventory(self):
        self.assertEqual(len(self.p.microstates()),64)
        self.assertEqual(len(self.p.phases()),12)
        self.assertEqual(len(policies()),16)
        self.assertEqual(sum(not p.at3.startswith(('vote','inverse')) and not p.at4.startswith(('vote','inverse')) for p in policies()),4)

    def test_raw_physical_rows_three_distinct_programs(self):
        for policy in (Policy(),Policy('service','skip'),Policy('inverse','service')):
            for state in self.p.microstates():
                self.assertEqual(raw_row(self.p,policy,state),physical_row(self.p,policy,state))
                self.assertLessEqual(sum(raw_row(self.p,policy,state).values(),F(0)),1)

    def test_regenerative_intertwining_every_policy_and_phase(self):
        # E K = (E A) E, directly comparing physical vs reduced propagation.
        for policy in policies():
            for phase in self.p.phases():
                lhs=push(emission(self.p,phase),lambda s:physical_row(self.p,policy,s))
                rhs=push(reduced_row(self.p,policy,phase),lambda s:emission(self.p,s))
                self.assertEqual(lhs,rhs)

    def test_stochastic_emission_not_free_observation(self):
        for phase in self.p.phases():
            self.assertEqual(sum(emission(self.p,phase).values(),F(0)),1)
        self.assertEqual(initial_micro(self.p),push(initial_phase(self.p),lambda s:emission(self.p,s)))
        # Same actual bank and resource, different legitimately stored reports:
        values=[sum(physical_row(self.p,Policy(),(1,bits,3)).values(),F(0)) for bits in ((0,0,0),(1,1,1))]
        self.assertNotEqual(values[0],values[1])
        # This does NOT license merging arbitrary microstates with the same bank/resource.

    def test_raw_and_reduced_multicycle_values(self):
        for policy in (Policy(),Policy('service','service'),Policy('skip','skip')):
            c,m=forward(self.p,policy,5)
            raw,law=forward(self.p,policy,5,raw=True)
            self.assertEqual(c,raw)
            self.assertEqual(push(m,lambda s:emission(self.p,s)),law)

    def test_resource_and_mass_trace_invariants(self):
        for policy in policies():
            for z,bits,b in ((0,(0,1,1),1),(1,(1,1,1),2),(0,(0,0,0),3),(1,(1,0,1),4)):
                traces=event_traces(self.p,policy,(z,bits,b))
                self.assertEqual(sum((t['mass'] for t in traces),F(0)),1)
                for t in traces:
                    self.assertGreaterEqual(t['balance_after_debit'],0)
                    if t['outcome']=='live':self.assertTrue(1<=t['balance_next']<=4)
                    else:self.assertNotIn('balance_next',t)
                live=sum((t['mass'] for t in traces if t['outcome']=='live'),F(0))
                self.assertEqual(live,sum(physical_row(self.p,policy,(z,bits,b)).values(),F(0)))

    def test_initial_cost_and_no_free_harvest(self):
        s=run_summary(self.p,Policy(),0)
        self.assertEqual(s['expected_spent_including_initialization'],1)
        self.assertEqual(s['expected_earned'],0)
        self.assertEqual(s['expected_completed_tasks'],0)
        s=run_summary(self.p,Policy(),5)
        self.assertEqual(s['expected_earned'],2*s['expected_completed_tasks'])
        self.assertLess(s['expected_completed_tasks'],5)

    def test_exact_stationary_library_optimum_and_blind_gap(self):
        rows=all_stationary(self.p,8)
        self.assertEqual(rows[0]['policy'],Policy())
        blind=[r for r in rows if r['policy'].at3 in ('skip','service') and r['policy'].at4 in ('skip','service')]
        target=F(183,200) # 91.5%
        self.assertGreater(rows[0]['value'],target)
        self.assertLess(max(r['value'] for r in blind),target)
        self.assertTrue(all(rows[0]['value']>=r['value'] for r in rows))

    def test_backward_forward_independent_recursions(self):
        for policy in policies():
            for n in (0,1,2,4):
                val=vector_value(self.p,policy,n)
                self.assertEqual(sum((w*val[s] for s,w in initial_phase(self.p).items()),F(0)),forward(self.p,policy,n)[0][-1])

    def test_diagnosis_ablation_changes_best_program(self):
        p=Model(diagnostic_error=F(1,2))
        rows=all_stationary(p,8)
        always=forward(p,Policy('service','service'),8)[0][-1]
        self.assertEqual(rows[0]['value'],always)
        self.assertLess(forward(p,Policy(),8)[0][-1],always)
        # Even fair reports do not erase physical Z-dependence of the faulty bank.
        means=[sum((voter(bits,p.rate(z)) for bits in BITS),F(0))/8 for z in (0,1)]
        self.assertNotEqual(means[0],means[1])

    def test_uniform_fatal_hazard_bounds_recurrence(self):
        bound=task_success(self.p,0)
        for pol in policies():
            for row in (reduced_row(self.p,pol,s) for s in self.p.phases()):
                self.assertLessEqual(sum(row.values(),F(0)),bound)
        for n,m in enumerate(forward(self.p,Policy(),8)[0]):self.assertLessEqual(m,bound**n)

    def test_more_repair_is_not_more_operational_survival(self):
        contingent=run_summary(self.p,Policy(),8)
        fixed=run_summary(self.p,Policy('service','service'),8)
        self.assertGreater(contingent['survival'],fixed['survival'])
        self.assertLess(contingent['expected_services'],fixed['expected_services'])

    def test_both_initial_contexts_benefit_in_the_declared_fixture(self):
        for prior in (F(0),F(1)):
            a=forward(self.p,Policy(),8,prior)[0][-1]
            b=forward(self.p,Policy('service','service'),8,prior)[0][-1]
            self.assertGreater(a,b)

    def test_aged_report_requires_health_before_drift(self):
        # Same current hidden health and b, yet report distributions differ.
        a=reduced_row(self.p,Policy(),(0,1,3))
        b=reduced_row(self.p,Policy(),(1,1,3))
        self.assertNotEqual(a,b)

    def test_invalid_probability_policy_and_horizon(self):
        for kw in ({'capacity':3},{'diagnostic_error':F(3,4)},{'healthy_error':F(1,10)},{'start_balance':0}):
            with self.assertRaises(ValueError):Model(**kw)
        with self.assertRaises(ValueError):Policy('health','vote')
        with self.assertRaises(ValueError):forward(self.p,Policy(),-1)

if __name__=='__main__':unittest.main()
