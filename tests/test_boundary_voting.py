from fractions import Fraction as F
from itertools import product
import unittest
from cdka.boundary_voting import *
from cdka.faulty_updates import last_gate_bound


class BoundaryVotingTests(unittest.TestCase):
    def test_noiseless_voter_truth_table(self):
        for bits in BITS:self.assertEqual(execute_voter(bits),int(sum(bits)>=2))

    def test_polynomial_topology_separation_whole_interval(self):
        for j in range(51):
            g=F(j,100);v=voter_table(g)
            self.assertEqual(v[BITS.index((0,1,1))]-v[BITS.index((1,0,1))],topology_gap(g))
            if 0<j<50:self.assertGreater(topology_gap(g),0)

    def test_topology_separation_is_an_exact_polynomial_identity(self):
        p=voter_power_profile()
        diff=tuple(a-b for a,b in zip(p[BITS.index((0,1,1))],p[BITS.index((1,0,1))]))
        self.assertEqual(diff,(0,2,-10,16,-8,0,0))

    def test_raw_voter_distribution_matches_profile(self):
        for g in (F(0),F(1,100),F(1,5),F(1,2)):
            for bits,table_value in zip(BITS,voter_table(g)):
                total=F(0)
                for flags in product((0,1),repeat=6):
                    w=g**sum(flags)*(1-g)**(6-sum(flags))
                    total+=w*execute_voter(bits,flags)
                self.assertEqual(total,table_value)

    def test_independent_raw_replica_voter_oracle(self):
        tiny=PhysicalCircuit(((2,4),),5)
        for inp in ((0,0),(1,0),(2,1),(3,1)):
            for shared in (False,True):
                value=raw_replica_vote(tiny,inp,F(1,10),F(1,20),shared)
                channel=circuit_triplet_channel(tiny,F(1,10),F(1,20),shared)
                self.assertEqual(value,channel[2*inp[0]+inp[1]])

    def test_ideal_tmr_is_cubic_not_relabeling(self):
        for r in (F(0),F(1,5),F(1,2),F(9,10),F(1)):
            self.assertEqual(iid_vote_output(r,0),3*r*r-2*r**3)
        c=SEQUENTIAL;r=output_probabilities(c,F(1,10))
        shared=circuit_triplet_channel(c,F(1,10),0,True)
        self.assertEqual(shared,r)
        self.assertNotEqual(shared,circuit_triplet_channel(c,F(1,10),0,False))

    def test_actual_shared_voter_cost_and_values(self):
        values={r['id']:r for r in portfolio()}
        self.assertEqual(values['triple']['nand_slots'],18)
        self.assertEqual(values['shared_output_voted']['nand_slots'],10)
        self.assertLess(values['triple']['value'],values['bypass']['value'])
        self.assertGreater(values['triple_voter_maintained']['value'],values['bypass']['value'])
        self.assertGreater(values['single_maintained']['value'],values['triple_voter_maintained']['value'])

    def test_service_dominance_for_entire_success_interval(self):
        for s in (F(0),F(1)):
            values={r['id']:r['value'] for r in portfolio(success=s)}
            self.assertGreater(values['single_maintained'],values['triple_voter_maintained'])
        threshold=voter_maintenance_threshold()
        values={r['id']:r['value'] for r in portfolio(success=threshold)}
        self.assertEqual(values['triple_voter_maintained'],values['bypass'])

    def test_last_port_bound_is_not_bypassed(self):
        for g in (F(1,100),F(1,50),F(1,20)):
            x=task_value(circuit_triplet_channel(SEQUENTIAL,g,g))
            self.assertLessEqual(x,last_gate_bound(F(1,100),g))
        upper=F(4,5)*last_gate_bound(F(1,100),F(1,1000))+F(1,5)*last_gate_bound(F(1,100),F(1,50))
        maintained={r['id']:r['value'] for r in portfolio()}['triple_voter_maintained']
        self.assertLessEqual(maintained,upper)

    def test_two_updates_raw_and_quotient(self):
        report=boundary_certificate()
        self.assertEqual(report['rows_verified'],192)
        self.assertEqual(report['two_update_cases'],384)
        self.assertGreater(report['count_failure_one'],0)
        self.assertGreater(report['count_failure_two'],0)
        self.assertGreater(report['hidden_health_failure'],0)

    def test_minimal_partition_and_smaller_linear_signature(self):
        r=signature_certificate()
        self.assertEqual(r['abstract']['classes'],8)
        self.assertEqual(r['physical']['classes'],12)
        self.assertEqual(r['abstract']['rank'],5)
        self.assertEqual(r['physical']['rank'],10)
        self.assertEqual(r['physical']['profile'],(2,4,7,9,10,10))

    def test_actual_symmetry_is_b_c_not_all_ports(self):
        for z in (0,1):
            for bits in BITS:
                swapped=(bits[0],bits[2],bits[1])
                for mode in ('diffuse','regenerate'):
                    self.assertEqual(aggregate(raw_update((z,bits),mode)),aggregate(raw_update((z,swapped),mode)))

    def test_latent_health_not_runtime_information(self):
        old=(0,(0,0,0));other=(1,(0,0,0))
        self.assertEqual(state_label(old,latent=False),state_label(other,latent=False))
        self.assertNotEqual(aggregate(raw_update(old),latent=False),aggregate(raw_update(other),latent=False))

    def test_more_controls_can_invalidate_a_smaller_interface(self):
        x=(1,(0,1,1));y=(1,(1,0,1))
        self.assertEqual(aggregate(raw_update(x,symmetric=True),False),aggregate(raw_update(y,symmetric=True),False))
        self.assertNotEqual(aggregate(raw_update(x),False),aggregate(raw_update(y),False))

    def test_preserve_death_and_procedure_failure(self):
        channel=output_probabilities(SEQUENTIAL,F(1,100))
        self.assertEqual(task_value(channel,procedure_failure=F(1,10)),F(9,10)*task_value(channel))

    def test_invalid_probabilities(self):
        for g in (F(-1,10),F(3,4)):
            with self.assertRaises(ValueError):voter_table(g)
        with self.assertRaises(ValueError):execute_voter((0,0,2))
        with self.assertRaises(ValueError):raw_update((0,(0,0,0)),'invented')

if __name__=='__main__':unittest.main()
