"""Independent exact checks for the continuation audit; runs under -S -O."""

from fractions import Fraction as F
import random
import unittest

from cdka.budget_continuation import (
    all_horizon_equal, audit_summary, column_rank, continuation_basis,
    finite_residual_audit, index_sparse, index_vector, negative_controls,
    rank_one_growth_control, residual_extension, row_from_branches, sparse_kernel,
)


def dense(rows):
    return tuple(tuple(row.get(j, F(0)) for j in range(len(rows))) for row in rows)


def mv(matrix, vector):
    return tuple(sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix)


def forward(law, matrix):
    return tuple(sum((law[i] * matrix[i][j] for i in range(len(law))), F(0))
                 for j in range(len(law)))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def minus(a, b):
    return tuple(x - y for x, y in zip(a, b))


def response(matrix, terminal, horizon):
    value = terminal
    for _ in range(horizon):
        value = mv(matrix, value)
    return value


def forward_value_and_cost(matrix, cost, terminal, terminal_cost, initial, setup, horizon):
    law, spent = initial, setup
    for _ in range(horizon):
        spent += dot(law, cost)
        law = forward(law, matrix)
    return dot(law, terminal), spent + dot(law, terminal_cost)


class BudgetContinuationTests(unittest.TestCase):
    def test_four_negative_controls(self):
        control = negative_controls()
        self.assertEqual(control['immediate_survival_not_enough']['two_step_Q_T_from_state0'], (1, 0))
        self.assertEqual(control['immediate_saving_not_enough']['one_step_Q_T'], (1, 0))
        self.assertEqual(control['immediate_saving_not_enough']['two_step_Q_T'], (2, 3))
        self.assertEqual(control['failed_branch_spend']['expected_cost_A_B'], (F(1, 2), 1))
        for result in control['rank_one_update']:
            self.assertEqual(result['old_dimension_with_mass'], 2)
            self.assertEqual(result['update_rank'], 1)
            self.assertEqual(result['seed_residual_rank'], 1)
            self.assertEqual(result['new_dimension_with_mass'], result['states'])

    def test_exact_telescoping_against_explicit_dense_sums(self):
        rng = random.Random(20261115)
        for _ in range(4):
            size = 3
            kernels = []
            for _ in range(2):
                rows = []
                for _ in range(size):
                    counts = [rng.randrange(4) for _ in range(size)]
                    denominator = sum(counts) + 2
                    rows.append({j: F(x, denominator) for j, x in enumerate(counts) if x})
                kernels.append(tuple(rows))
            q, t = kernels
            cq = tuple(F(rng.randrange(4), 2) for _ in range(size))
            ct = tuple(F(rng.randrange(4), 2) for _ in range(size))
            gq, gt = (F(1), F(1, 2), F(0)), (F(0), F(1), F(1, 3))
            bq, bt = (F(2), F(0), F(1)), (F(0), F(1), F(3))
            report = finite_residual_audit(q, t, cq, ct, 6, terminal=gq,
                       candidate_terminal=gt, terminal_cost=bq,
                       candidate_terminal_cost=bt, include_vectors=True)
            vectors = report['vectors']
            qq, tt = dense(q), dense(t)
            dd = tuple(minus(rt, rq) for rq, rt in zip(qq, tt))
            for horizon in range(7):
                rv = response(tt, minus(gt, gq), horizon)
                rc = response(tt, minus(bt, bq), horizon)
                for j in range(horizon):
                    k = horizon - 1 - j
                    sv = mv(dd, vectors['reference_responses'][k])
                    sc = plus(minus(ct, cq), mv(dd, vectors['reference_costs'][k]))
                    rv = plus(rv, response(tt, sv, j))
                    rc = plus(rc, response(tt, sc, j))
                self.assertEqual(rv, vectors['response_differences'][horizon])
                self.assertEqual(rc, vectors['cost_differences'][horizon])
                self.assertEqual(rv, vectors['telescoped_response_differences'][horizon])
                self.assertEqual(rc, vectors['telescoped_cost_differences'][horizon])
            self.assertTrue(report['telescoping_verified'])

    def test_paid_startup_terminal_stage_and_failed_mass_against_forward_oracle(self):
        q = ({0: F(1, 2), 1: F(1, 4)}, {1: F(2, 3)})
        t = ({1: F(3, 4)}, {0: F(1, 3)})
        cq, ct = (F(2), F(1)), (F(1), F(3))
        gq, gt = (F(1), F(1, 2)), (F(1, 3), F(1))
        bq, bt = (F(1), F(0)), (F(0), F(2))
        muq, mut = (F(1, 2), F(1, 4)), (F(0), F(1, 2))
        zq, zt = F(3), F(2)
        report = finite_residual_audit(q, t, cq, ct, 4, terminal=gq,
                   candidate_terminal=gt, terminal_cost=bq, candidate_terminal_cost=bt,
                   initial=muq, candidate_initial=mut, initial_cost=zq,
                   candidate_initial_cost=zt)
        paired = report['initial_comparison']
        self.assertFalse(paired['same_startup_law'])
        self.assertEqual(paired['reference_live_mass'], F(3, 4))
        self.assertEqual(paired['candidate_live_mass'], F(1, 2))
        for horizon in range(5):
            vq, sq = forward_value_and_cost(dense(q), cq, gq, bq, muq, zq, horizon)
            vt, st = forward_value_and_cost(dense(t), ct, gt, bt, mut, zt, horizon)
            self.assertEqual((vq, vt), (paired['reference_responses'][horizon], paired['candidate_responses'][horizon]))
            self.assertEqual((sq, st), (paired['reference_costs'][horizon], paired['candidate_costs'][horizon]))
            self.assertEqual(vt - vq, paired['telescoped_response_differences'][horizon])
            self.assertEqual(st - sq, paired['telescoped_cost_differences'][horizon])

    def test_local_cost_certificate_is_sufficient_not_necessary(self):
        q, t = ({0: F(1)}, {1: F(1)}), ({1: F(1)}, {0: F(1)})
        audit = finite_residual_audit(q, t, (2, 1), (0, 1), 2)
        self.assertFalse(audit['certificate']['nonincreasing_cost_through_horizon'])
        self.assertTrue(audit['exact_comparison']['nonincreasing_cost_through_horizon'])
        self.assertEqual(audit['first_positive_cost_residual'],
                         {'continuation_steps': 1, 'state_index': 1, 'value': F(1)})
        self.assertIsNone(audit['first_cost_increase'])

    def test_terminal_only_equality_does_not_certify_all_prefixes(self):
        q, t = ({0: F(1)}, {1: F(1)}), ({1: F(1)}, {0: F(1)})
        audit = finite_residual_audit(q, t, horizon=2, terminal=(1, 0))
        self.assertTrue(audit['exact_comparison']['equal_terminal_response'])
        self.assertFalse(audit['exact_comparison']['equal_response_through_horizon'])
        self.assertFalse(audit['certificate']['equal_response_through_horizon'])

    def test_survival_certificate_and_actual_startup_gate_are_separate(self):
        q = ({0: F(1)}, {1: F(1)})
        audit = finite_residual_audit(q, q, horizon=3, initial=(1, 0),
                                      candidate_initial=(F(1, 2), 0))
        self.assertTrue(audit['certificate']['equal_response_through_horizon'])
        self.assertFalse(audit['initial_comparison']['equal_response_through_horizon'])
        self.assertEqual(audit['initial_comparison']['candidate_responses'], (F(1, 2),) * 4)

    def test_failed_charge_is_paid_once_then_dead_mass_is_absent(self):
        audit = finite_residual_audit(({},), ({},), (1,), (2,), 4, initial=(1,))
        paired = audit['initial_comparison']
        self.assertEqual(paired['reference_responses'], (1, 0, 0, 0, 0))
        self.assertEqual(paired['reference_costs'], (0, 1, 1, 1, 1))
        self.assertEqual(paired['candidate_costs'], (0, 2, 2, 2, 2))

    def test_stabilized_all_horizon_equality_is_task_specific(self):
        q, t = ({0: F(1)}, {1: F(1)}), ({1: F(1)}, {0: F(1)})
        mass = all_horizon_equal(q, t)
        target = all_horizon_equal(q, t, (1, 0))
        self.assertTrue(mass['stabilized'])
        self.assertTrue(mass['equal'])
        self.assertEqual(mass['dimension'], 1)
        self.assertFalse(target['equal'])
        self.assertEqual(target['first_obstruction']['reference_power'], 0)
        late = all_horizon_equal(({0: F(1)}, {}), ({1: F(1)}, {}))
        self.assertFalse(late['equal'])
        self.assertEqual(late['first_obstruction']['reference_power'], 1)

    def test_capped_unstabilized_basis_never_claims_infinite_equality(self):
        q = ({0: F(1)}, {0: F(1)}, {1: F(1)})
        partial = all_horizon_equal(q, q, (1, 0, 0), max_dimension=1)
        self.assertFalse(partial['stabilized'])
        self.assertIsNone(partial['equal'])
        full = continuation_basis(q, ((1, 0, 0),))
        self.assertTrue(full['stabilized'])
        self.assertEqual(full['dimension'], 3)
        self.assertTrue(all_horizon_equal(q, q, (1, 0, 0))['equal'])

    def test_residual_extension_rejects_noninvariant_old_interface(self):
        q = ({1: F(1)}, {0: F(1)})
        with self.assertRaises(ValueError):
            residual_extension(q, q, ((1, 0),))
        self.assertEqual(rank_one_growth_control(6)['new_dimension_with_mass'], 6)
        self.assertEqual(column_rank(((1, 2, 3), (2, 4, 6), (0, 1, 0))), 2)

    def test_labelled_adapter_keeps_closed_state_domain(self):
        rows, states, index = index_sparse({'b': {'a': F(1, 2)}, 'a': {'b': F(1)}}, ('a', 'b'))
        self.assertEqual(rows, ({1: F(1)}, {0: F(1, 2)}))
        self.assertEqual(states, ('a', 'b'))
        self.assertEqual(index, {'a': 0, 'b': 1})
        self.assertEqual(index_vector({'b': F(1, 2)}, states, default=0), (0, F(1, 2)))
        with self.assertRaises(ValueError):
            index_sparse({'a': {'b': F(1)}})
        with self.assertRaises(ValueError):
            index_sparse({'a': {}}, ('a', 'b'))
        with self.assertRaises(ValueError):
            index_vector({'a': 1}, states)
        with self.assertRaises(ValueError):
            index_vector({'c': 1}, states, default=0)

    def test_invalid_inputs_and_exact_arithmetic_boundary(self):
        for rows in ((), ({0: F(3, 2)},), ({0: F(-1)},), ({1: F(1)},), ({True: F(1)},)):
            with self.assertRaises(ValueError):
                sparse_kernel(rows)
        with self.assertRaises(TypeError):
            sparse_kernel(({0: .5},))
        q = ({0: F(1)},)
        for kwargs in ({'horizon': -1}, {'horizon': True}, {'reference_cost': (-1,)},
                       {'initial': (2,)}, {'initial': (F(-1),)},
                       {'candidate_initial': (1,)}, {'initial_cost': 1},
                       {'terminal': (1, 0)}, {'candidate_initial_cost': -1}):
            with self.assertRaises(ValueError):
                finite_residual_audit(q, q, **kwargs)
        with self.assertRaises(TypeError):
            finite_residual_audit(q, q, reference_cost=(.5,))
        with self.assertRaises(ValueError):
            finite_residual_audit(q, ({0: 1}, {}))
        with self.assertRaises(ValueError):
            row_from_branches(((F(1, 2), 0, 1),))
        with self.assertRaises(ValueError):
            row_from_branches(((1, None, -1),))
        with self.assertRaises(ValueError):
            continuation_basis(q, max_dimension=0)

    def test_horizon_zero_and_compact_output(self):
        audit = finite_residual_audit(({0: 1},), ({0: 1},), horizon=0,
                                      terminal=(F(1, 2),), terminal_cost=(3,),
                                      initial=(F(1, 2),), initial_cost=2,
                                      include_vectors=True)
        self.assertEqual(audit['initial_comparison']['reference_responses'], (F(1, 4),))
        self.assertEqual(audit['initial_comparison']['reference_costs'], (F(7, 2),))
        self.assertTrue(audit['certificate']['equal_response_through_horizon'])
        summary = audit_summary(audit)
        self.assertNotIn('vectors', summary)
        self.assertNotIn('telescoped_cost_differences', summary['initial_comparison'])
        self.assertEqual(summary['initial_comparison']['reference_responses'], F(1, 4))

    def test_reachable_ideal_enable_resource_feedback_witness(self):
        from cdka.shared_budget import Contract, Prices
        from experiments.shared_budget_controls import physical_case
        result = physical_case('test_ideal', Contract(Prices(0, 6, 0),
                               enable_noise='decoupled', decoupled_error=F(0)), 5)
        witness = result['delayed_common_state_witness']
        self.assertTrue(result['same_startup_law'])
        self.assertEqual(witness['state'], (1, 1, 2, 84))
        self.assertEqual(witness['prefix_cycles'], 1)
        self.assertEqual(witness['total_tasks'], 5)
        self.assertGreater(F(witness['reference_prefix_probability']['exact']), 0)
        self.assertGreater(F(witness['candidate_prefix_probability']['exact']), 0)
        self.assertEqual(witness['immediate_live_mass_residual']['exact'], '0')
        self.assertEqual(witness['earlier_response_residuals'], ('0', '0'))
        self.assertGreater(F(witness['response_residual']['exact']), 0)
        self.assertEqual(witness['next_balances_on_executed_service_and_completed_cycle'],
                         {'reference': [54], 'candidate': [60]})
        self.assertTrue(all(h['survival_difference']['exact'] == '0' for h in result['horizons'][:4]))
        self.assertGreater(F(result['horizons'][4]['survival_difference']['exact']), 0)
        self.assertTrue(result['selected_witness_raw_branch_and_failed_cost_check'])

    def test_shared_health_cheaper_short_run_can_fail_survival_gate(self):
        from cdka.shared_budget import Contract, Prices
        from experiments.shared_budget_controls import physical_case
        result = physical_case('test_shared', Contract(Prices(1, 6, 0)), 3)
        last = result['horizons'][-1]
        self.assertLess(F(last['survival_difference']['exact']), 0)
        self.assertLess(F(last['spent_difference']['exact']), 0)
        witness = result['first_negative_response_residual']
        self.assertEqual(witness['state'], (0, 0, 0, 66))
        self.assertEqual(witness['prefix_cycles'], 0)
        self.assertGreater(F(witness['reference_prefix_probability']['exact']), 0)
        self.assertTrue(last['integer_forward_verified'])
        self.assertTrue(last['telescoping_verified'])

    def test_physical_audit_preserves_distinct_paid_startup_laws(self):
        from cdka.shared_budget import Contract, Prices
        from experiments.shared_budget_controls import physical_case
        result = physical_case('test_setup', Contract(Prices(1, 6, 6)), 2)
        self.assertFalse(result['same_startup_law'])
        self.assertEqual(result['initial_balances_reference'], [66])
        self.assertEqual(result['initial_balances_candidate'], [60])
        self.assertEqual(result['reference_startup_spend'], '30')
        self.assertEqual(result['candidate_startup_spend'], '36')
        self.assertTrue(all(h['integer_forward_verified'] and h['telescoping_verified']
                            for h in result['horizons']))

    def test_blind_continuation_ignores_record_interventions_but_pays_startup(self):
        from itertools import product
        from cdka.shared_budget import Contract, Prices, Policy, RETAIN, compile_kernel
        from experiments.shared_budget_controls import blind_diagnostic_case
        contract, policy = Contract(Prices(1, 6, 0)), Policy('service', 'service')
        # Balance84 occurs on the actual blind live path after the first cycle.
        # Change the report while holding hidden health and resource fixed.
        for terminal in (False, True):
            kernel = compile_kernel(contract, policy, RETAIN, terminal)
            for health in (0, 1):
                reference = None
                for first, tail in product((0, 1), range(3)):
                    row = kernel.row((health, first, tail, 84))
                    projected = {}
                    for state, mass in row.transitions.items():
                        key = state[0], state[3]
                        projected[key] = projected.get(key, F(0)) + mass
                    signature = (projected, row.spend_by_stage, row.failures_by_cause,
                                 row.services, row.gate_events)
                    if reference is None:
                        reference = signature
                    self.assertEqual(signature, reference)
                    self.assertEqual(row.gate_events['selection'], 0)
        case = blind_diagnostic_case(Prices(1, 6, 0))
        self.assertTrue(case['all_positive_branches_have_zero_selection_invocations'])
        self.assertEqual(case['mandatory_initial_writes'], '1')
        self.assertEqual(case['initial_write_spend'], '6')
        self.assertEqual(case['startup_spend'], '30')
        self.assertGreater(case['positive_branch_traces_checked'], 0)
        self.assertTrue(all(step[-1] == 0 for step in case['ordinary_live_path']))

    def test_controls_cli_checks_bytes_without_overwriting_stale_artifact(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        from experiments import shared_budget_controls as controls
        minimal = {'physical_cases': (), 'blind_diagnostic_use': {'global_comparison': {}}}
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'controls.json'
            with patch.object(controls, 'run', return_value=minimal), redirect_stdout(StringIO()):
                with self.assertRaisesRegex(ValueError, 'Stale or missing'):
                    controls.main(['--check', '--output', str(path)])
                self.assertFalse(path.exists())
                controls.main(['--write', '--output', str(path)])
                expected = path.read_bytes()
                self.assertNotIn(b'elapsed_seconds', expected)
                controls.main(['--check', '--output', str(path)])
                self.assertEqual(path.read_bytes(), expected)
                path.write_bytes(expected + b' ')
                stale = path.read_bytes()
                with self.assertRaisesRegex(ValueError, 'Stale or missing'):
                    controls.main(['--check', '--output', str(path)])
                self.assertEqual(path.read_bytes(), stale)


if __name__ == '__main__':
    unittest.main()
