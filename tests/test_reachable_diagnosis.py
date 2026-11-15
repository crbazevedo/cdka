"""Physical acquisition, transport and budget checks for reachable diagnosis."""
import unittest
from fractions import Fraction as F
from itertools import product

from cdka.boundary_voting import HEALTH, STATES
from cdka.maintenance_access import WRITE_ERROR, base_probes
from cdka.reachable_diagnosis import (
    acquisition, acquisition_traces, advance_updates, affine_sensor_value,
    common_reservation, contract, contrast, evaluate, execution_cost,
    joint_oracle, plan_words, preparation_laws, raw_acquisition,
    raw_history_law, response_table, sensor_ceiling, word_id,
)
from cdka.semantic_closure import dot


class ReachableDiagnosisPhysicsTests(unittest.TestCase):
    def test_one_sensor_event_is_shared_by_all_three_writes(self):
        eta, e = F(1, 10), WRITE_ERROR
        joint = raw_acquisition(eta)
        all_wrong = sum((mass for (h, z, bits), mass in joint.items()
                         if bits == (1-h,)*3), F(0))
        self.assertEqual(all_wrong, eta*(1-e)**3+(1-eta)*e**3)
        marginal_error = eta+e-2*eta*e
        self.assertNotEqual(all_wrong, marginal_error**3)
        self.assertEqual(len(acquisition_traces(eta)), 64)
        for trace in acquisition_traces(eta):
            h, z, bits = trace['target']
            y = trace['sensor_output']
            self.assertEqual(y, h ^ trace['sensor_fault'])
            self.assertEqual(bits, tuple(y ^ flag for flag in trace['write_faults']))

    def test_folded_acquisition_matches_raw_sensor_write_health_events(self):
        for eta, bad in product((F(0), F(1, 10), F(1, 2)), (F(0), F(1, 2), F(1))):
            with self.subTest(eta=eta, initial_bad=bad):
                folded = acquisition(eta, bad)
                raw = raw_acquisition(eta, bad)
                self.assertEqual(sum(raw.values(), F(0)), 1)
                for h in (0, 1):
                    self.assertEqual(sum(folded[h], F(0)), F(1, 2))
                    self.assertEqual(folded[h], tuple(raw.get((h, z, bits), F(0))
                                                      for z, bits in STATES))

    def test_acquisition_uses_one_health_interval(self):
        for bad in (F(0), F(1, 2), F(1)):
            joint = raw_acquisition(initial_bad=bad)
            degraded = sum((mass for (h, z, bits), mass in joint.items() if z), F(0))
            self.assertEqual(degraded, (1-bad)*HEALTH[0][1]+bad*HEALTH[1][1])
        self.assertEqual(sum((mass for (h, z, bits), mass in raw_acquisition().items()
                              if z), F(0)), F(1, 20))

    def test_reachable_histories_preserve_the_source_and_match_joint_transport(self):
        cohort = preparation_laws(h=2)
        self.assertEqual(tuple(cohort), ('DD', 'DR', 'RD', 'RR'))
        self.assertEqual(len(set(cohort.values())), 4)
        for history, law in cohort.items():
            raw = raw_history_law(history)
            self.assertEqual(law, advance_updates(acquisition(), history))
            for h in (0, 1):
                self.assertEqual(sum(law[h], F(0)), F(1, 2))
                self.assertEqual(law[h], tuple(raw.get((h, z, bits), F(0))
                                                for z, bits in STATES))

    def test_contrast_evaluator_matches_raw_joint_oracle_for_competing_plans(self):
        cohort = preparation_laws(h=2)
        # Earliest, intermediate and latest regeneration under the same
        # four-update workload; all use the same physical maintenance rule.
        for history, law in cohort.items():
            for word in ('DDDDM', 'RDDDM', 'DRDDM', 'MRDDD'):
                with self.subTest(history=history, word=word):
                    self.assertEqual(evaluate(law, word), joint_oracle(history, word))

    def test_joint_oracle_covers_repair_endpoints_and_mixed_initial_health(self):
        for success in (F(0), F(1)):
            law = advance_updates(acquisition(F(1, 5), F(1, 2)), 'DR')
            for word in ('MDR', 'DRM', 'RD'):
                self.assertEqual(evaluate(law, word, success),
                                 joint_oracle('DR', word, F(1, 5), F(1, 2), success))

    def test_fidelity_uses_the_source_target_and_correct_mass_offset(self):
        law = acquisition()
        readout = base_probes()['readout']
        physical_output_one = dot(tuple(a+b for a, b in zip(*law)), readout)
        self.assertGreater(evaluate(law, ()), F(4, 5))
        self.assertLess(physical_output_one, F(3, 5))
        for h in (0, 1):
            point = [F(0)]*len(STATES)
            index = STATES.index((0, (h,)*3))
            point[index] = F(1)
            zero = tuple(F(0) for _ in STATES)
            joint = (tuple(point), zero) if not h else (zero, tuple(point))
            offset, signed = contrast(joint)
            self.assertEqual(offset, 1-h)
            self.assertEqual(evaluate(joint, ()), readout[index] if h else 1-readout[index])

    def test_mandatory_and_optional_workloads_are_distinct_and_resource_safe(self):
        mandatory = plan_words(4)
        self.assertEqual(len(mandatory), 96)
        self.assertEqual(len(set(mandatory)), 96)
        self.assertEqual(len(plan_words(2, exact_updates=False)), 24)
        self.assertEqual(set(plan_words(0)), {(), ('M',)})
        self.assertNotIn(('M',), mandatory)
        self.assertIn(('M',), plan_words(2, exact_updates=False))
        for word in mandatory:
            self.assertEqual(sum(letter in ('D', 'R') for letter in word), 4)
            self.assertLessEqual(word.count('M'), 1)
        reservation = common_reservation(2, 4)
        for history in preparation_laws(2):
            for word in mandatory:
                cost = execution_cost(history, word)
                self.assertEqual(set(cost), set(reservation))
                self.assertTrue(all(cost[k] <= reservation[k] for k in cost))

    def test_costs_charge_acquisition_and_separate_diffusion_from_writes(self):
        cost = execution_cost('DD', 'DRDDM')
        self.assertEqual(cost, {
            'installed_sensors': 1, 'sensor_readings': 1,
            'installed_nands': 6, 'retained_cells': 3,
            'voter_evaluations': 3, 'nand_evaluations': 18,
            'cell_writes': 6, 'cell_channel_updates': 21,
            'prepaid_service_slots': 1, 'clock_intervals': 9,
        })
        rr = execution_cost('RR', 'DRDDM')
        self.assertEqual(rr['cell_writes']-cost['cell_writes'], 6)
        self.assertEqual(rr['nand_evaluations']-cost['nand_evaluations'], 12)
        reservation = common_reservation(2, 4)
        self.assertEqual(reservation['nand_evaluations'], 48)
        self.assertEqual(reservation['cell_writes'], 21)
        self.assertEqual(reservation['clock_intervals'], 9)
        self.assertEqual(reservation['prepaid_service_slots'], 1)

    def test_shared_sensor_affine_law_and_information_ceiling_hold_for_all_plans(self):
        words = plan_words(4)
        zero = response_table(preparation_laws(2, eta=F(0)), words)
        for eta in (F(1, 10), F(1, 2)):
            table = response_table(preparation_laws(2, eta=eta), words)
            for history, row in table.items():
                for word, value in row.items():
                    self.assertEqual(value, affine_sensor_value(zero[history][word], eta))
                    self.assertLessEqual(value, sensor_ceiling(eta))
                    self.assertGreaterEqual(value, eta)
        self.assertEqual(sensor_ceiling(F(1, 10)), F(9, 10))
        self.assertEqual(joint_oracle('DR', 'MRDDD', eta=F(1, 2)), F(1, 2))

    def test_identity_and_contract_record_the_actual_protocol(self):
        self.assertEqual(preparation_laws(0), {'I': acquisition()})
        self.assertEqual(word_id(()), 'I')
        self.assertEqual(evaluate(acquisition(), 'I'), evaluate(acquisition(), ()))
        self.assertEqual(execution_cost('I', 'I')['clock_intervals'], 2)
        scope = contract(h=2, k=4, eta=F(1, 5), initial_bad=F(1, 3), success=F(1, 4))
        self.assertEqual(scope['sensor_error'], '1/5')
        self.assertEqual(scope['initial_bad_probability'], '1/3')
        self.assertEqual(scope['maintenance_success'], '1/4')
        self.assertTrue(scope['exact_updates'])
        self.assertEqual(scope['reservation'], common_reservation(2, 4))

    def test_invalid_acquisition_and_unpaid_actions_are_rejected(self):
        for eta in (-F(1, 10), F(3, 5)):
            with self.assertRaises(ValueError):
                acquisition(eta)
        for bad in (-1, 2):
            with self.assertRaises(ValueError):
                acquisition(initial_bad=bad)
        for bad_count in (-1, True, F(1, 2)):
            with self.assertRaises(ValueError):
                preparation_laws(bad_count)
            with self.assertRaises(ValueError):
                plan_words(bad_count)
        for word in ('MM', 'DMRM', 'X'):
            with self.assertRaises(ValueError):
                evaluate(acquisition(), word)
            with self.assertRaises(ValueError):
                execution_cost('DD', word)
        with self.assertRaises(ValueError):
            advance_updates(acquisition(), 'DM')
        with self.assertRaises(ValueError):
            response_table({'a': acquisition()}, [('M',), ('M',)])


if __name__ == '__main__':
    unittest.main()
