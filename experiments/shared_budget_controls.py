"""Reachable finite residual controls for the shared-budget physical compiler.

No all-state or all-horizon claim is made from the reachable truncation. Lazy
backward responses query the actual full physical row oracle as needed; no
successor is deleted. Independent integer forward runs check every H-task value.
Use --write to regenerate the deterministic scientific artifact and --check to
recompute it without writing. Runtime measurements appear only on stdout.
"""

import argparse
from dataclasses import asdict
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from time import perf_counter

from cdka.budget_continuation import negative_controls, row_from_branches
from cdka.shared_budget import (
    Contract, Prices, Policy, FRESH, ELIDE, RETAIN, PRICE_GRID, compile_kernel, initialize,
    event_traces, run_exact,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/data/shared-budget-controls.json'


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def inner(law, function):
    return sum((mass * function(state) for state, mass in law.items()), F(0))


def advance(law, kernel):
    result = {}
    for state, mass in law.items():
        for target, probability in kernel[state].items():
            result[target] = result.get(target, F(0)) + mass * probability
    return {state: mass for state, mass in result.items() if mass}


def number(value):
    return {"exact": str(value), "approx": float(value)}


def physical_case(name, contract, horizon=8):
    """Audit a fixed vote/vote FRESH-vs-ELIDE pair on reachable finite contexts.

    The case supports distinct installation/startup laws and terminal stages.
    Local residual contexts are an algebraic decomposition of the complete
    pair, not authorization to switch installed programs midway through a run.
    """
    if type(horizon) is not int or horizon < 1:
        raise ValueError("at least one terminal task required")
    policy = Policy()
    q, t = (compile_kernel(contract, policy, enable) for enable in (FRESH, ELIDE))
    qfinal, tfinal = (compile_kernel(contract, policy, enable, True) for enable in (FRESH, ELIDE))
    iq, it = (initialize(contract, enable) for enable in (FRESH, ELIDE))
    setup_q = sum(iq.spend_by_stage.values(), F(0))
    setup_t = sum(it.spend_by_stage.values(), F(0))
    muq, mut = iq.measure, it.measure

    @lru_cache(None)
    def q_response(state, steps):
        if steps == 0:
            row = qfinal.row(state)
            return row.survival, row.spent
        row = q.row(state)
        response, cost = F(0), row.spent
        for target, mass in row.transitions.items():
            tail_value, tail_cost = q_response(target, steps - 1)
            response += mass * tail_value
            cost += mass * tail_cost
        return response, cost

    @lru_cache(None)
    def t_response(state, steps):
        if steps == 0:
            row = tfinal.row(state)
            return row.survival, row.spent
        row = t.row(state)
        response, cost = F(0), row.spent
        for target, mass in row.transitions.items():
            tail_value, tail_cost = t_response(target, steps - 1)
            response += mass * tail_value
            cost += mass * tail_cost
        return response, cost

    @lru_cache(None)
    def residual(state, steps):
        qr, tr = q.row(state), t.row(state)
        rv, rc = F(0), tr.spent - qr.spent
        for target in qr.transitions.keys() | tr.transitions.keys():
            mass = tr.transitions.get(target, F(0)) - qr.transitions.get(target, F(0))
            if mass:
                value, cost = q_response(target, steps)
                rv += mass * value
                rc += mass * cost
        return rv, rc

    layers_q, layers_t = [muq], [mut]
    for _ in range(horizon - 1):
        layers_q.append(advance(layers_q[-1], q))
        layers_t.append(advance(layers_t[-1], t))
    reports = []
    for tasks in range(1, horizon + 1):
        steps = tasks - 1
        vq = inner(muq, lambda state: q_response(state, steps)[0])
        vt = inner(mut, lambda state: t_response(state, steps)[0])
        cq = setup_q + inner(muq, lambda state: q_response(state, steps)[1])
        ct = setup_t + inner(mut, lambda state: t_response(state, steps)[1])
        differences = {state: mut.get(state, F(0)) - muq.get(state, F(0))
                       for state in muq.keys() | mut.keys()}
        initial_value = inner(differences, lambda state: q_response(state, steps)[0])
        initial_cost = setup_t - setup_q + inner(differences, lambda state: q_response(state, steps)[1])
        boundary_value = inner(layers_t[steps], lambda state: tfinal.row(state).survival - qfinal.row(state).survival)
        boundary_cost = inner(layers_t[steps], lambda state: tfinal.row(state).spent - qfinal.row(state).spent)
        value_terms, cost_terms = [], []
        for prefix in range(steps):
            suffix = steps - 1 - prefix
            value_terms.append(inner(layers_t[prefix], lambda state: residual(state, suffix)[0]))
            cost_terms.append(inner(layers_t[prefix], lambda state: residual(state, suffix)[1]))
        tel_value = initial_value + boundary_value + sum(value_terms, F(0))
        tel_cost = initial_cost + boundary_cost + sum(cost_terms, F(0))
        require(tel_value == vt - vq and tel_cost == ct - cq, "reachable residual identity")
        forward_q = run_exact(contract, policy, FRESH, tasks, "tasks")
        forward_t = run_exact(contract, policy, ELIDE, tasks, "tasks")
        require((vq, cq) == (forward_q.survival, forward_q.spent), "reference backward/forward agreement")
        require((vt, ct) == (forward_t.survival, forward_t.spent), "candidate backward/forward agreement")
        report = {
            "tasks": tasks, "ordinary_steps": steps,
            "reference_survival": number(vq), "candidate_survival": number(vt),
            "survival_difference": number(vt - vq),
            "reference_spent": number(cq), "candidate_spent": number(ct),
            "spent_difference": number(ct - cq),
            "telescoping_verified": True, "integer_forward_verified": True,
            "initial_survival_term": str(initial_value), "terminal_survival_term": str(boundary_value),
            "initial_cost_term": str(initial_cost), "terminal_cost_term": str(boundary_cost),
        }
        # Exact final-horizon decomposition plus checked direct values at every
        # earlier horizon avoids serializing overlapping long rational vectors.
        if tasks == horizon:
            report["survival_residual_terms_by_candidate_prefix"] = tuple(map(str, value_terms))
            report["cost_residual_terms_by_candidate_prefix"] = tuple(map(str, cost_terms))
        reports.append(report)

    # Search only states on actual Q or T prefix supports, with enough task
    # budget left for the ordinary omission and its requested continuation.
    first_response = first_negative = first_cost_increase = None
    delayed_common_witness = None
    checked_contexts = 0
    for total_tasks in range(2, horizon + 1):
        for prefix in range(total_tasks - 1):
            suffix = total_tasks - 2 - prefix
            reachable = sorted(layers_q[prefix].keys() | layers_t[prefix].keys())
            for state in reachable:
                rv, rc = residual(state, suffix)
                checked_contexts += 1
                witness = {
                    "state": state, "prefix_cycles": prefix,
                    "remaining_reference_cycles_after_omission": suffix,
                    "total_tasks": total_tasks,
                    "reference_prefix_probability": number(layers_q[prefix].get(state, F(0))),
                    "candidate_prefix_probability": number(layers_t[prefix].get(state, F(0))),
                    "response_residual": number(rv), "cost_residual": number(rc),
                    "immediate_live_mass_residual": number(t.row(state).survival - q.row(state).survival),
                }
                if rv and first_response is None:
                    first_response = witness
                if rv < 0 and first_negative is None:
                    first_negative = witness
                if rc > 0 and first_cost_increase is None:
                    first_cost_increase = witness
                if (delayed_common_witness is None and state == (1, 1, 2, 84)
                        and layers_q[prefix].get(state, 0) > 0
                        and layers_t[prefix].get(state, 0) > 0
                        and t.row(state).survival == q.row(state).survival
                        and rv and suffix >= 1):
                    witness = dict(witness)
                    witness["earlier_response_residuals"] = tuple(
                        str(residual(state, k)[0]) for k in range(suffix))
                    witness["next_balances_on_executed_service_and_completed_cycle"] = {
                        label: sorted({trace.successor[3] for trace in
                                       event_traces(contract, policy, enable, state)
                                       if trace.executed_service and trace.cycle_complete})
                        for label, enable in (("reference", FRESH), ("candidate", ELIDE))}
                    delayed_common_witness = witness

    chosen = delayed_common_witness or first_response
    branch_checked = False
    if chosen is not None:
        state = tuple(chosen["state"])
        for kernel in (q, t, qfinal, tfinal):
            traces = event_traces(contract, policy, kernel.enable, state, kernel.terminal, raw=True)
            row, spent = row_from_branches((trace.probability, trace.successor, trace.spent)
                                           for trace in traces)
            require(row == kernel[state] and spent == kernel.row(state).spent,
                    "raw physical branch aggregation/reward agreement")
        branch_checked = True
    return {
        "name": name, "scope": "actual reachable finite prefixes; at most %d tasks" % horizon,
        "prices": asdict(contract.prices), "unit": contract.unit,
        "enable_noise": contract.enable_noise, "decoupled_error": contract.decoupled_error,
        "policy": policy.name, "initial_endowment": contract.endowment,
        "reference_startup_spend": str(setup_q), "candidate_startup_spend": str(setup_t),
        "same_startup_law": muq == mut,
        "initial_balances_reference": sorted({state[3] for state in muq}),
        "initial_balances_candidate": sorted({state[3] for state in mut}),
        "reachable_layer_sizes_reference": tuple(map(len, layers_q)),
        "reachable_layer_sizes_candidate": tuple(map(len, layers_t)),
        "reachable_contexts_checked": checked_contexts,
        "first_nonzero_response_residual": first_response,
        "first_negative_response_residual": first_negative,
        "first_positive_cost_residual": first_cost_increase,
        "delayed_common_state_witness": delayed_common_witness,
        "selected_witness_raw_branch_and_failed_cost_check": branch_checked,
        "horizons": reports,
        "finite_response_rank_measured": False,
        "all_horizon_claim": False,
        "backward_reference_contexts_cached": q_response.cache_info().currsize,
        "backward_candidate_contexts_cached": t_response.cache_info().currsize,
    }


def blind_diagnostic_case(prices, horizon=8, global_case=None):
    """One fixed report-blind program; verify its actual positive live traces.

    The initial report is still acquired and paid for. No proposal to remove
    that mandatory operation is made. This control identifies whether stored
    report contents influence the winning continuation in the frozen grammar.
    """
    contract, policy = Contract(prices), Policy('service', 'service')
    initial = initialize(contract, RETAIN)
    regular = compile_kernel(contract, policy, RETAIN)
    terminal = compile_kernel(contract, policy, RETAIN, True)
    law = initial.measure
    path, state_checks, branch_checks = [], 0, 0
    task_final = None

    def check_step(current, kernel, epoch):
        nonlocal state_checks, branch_checks
        balances = {state[3] for state, mass in current.items() if mass > 0}
        require(len(balances) == 1, 'blind positive live balance must be deterministic')
        observed_modes, requested, executed, next_balances, selection_calls = set(), set(), set(), set(), set()
        for state, mass in current.items():
            if mass <= 0:
                continue
            state_checks += 1
            observed_modes.add(contract.mode(policy, state[3]))
            for trace in event_traces(contract, policy, RETAIN, state, kernel.terminal):
                if trace.probability <= 0:
                    continue
                branch_checks += 1
                requested.add(trace.requested_service)
                executed.add(trace.executed_service)
                selection_calls.add(trace.gates[0])
                if trace.successor is not None:
                    next_balances.add(trace.successor[3])
        require(observed_modes <= {'skip', 'service'}, 'stored report must not select an action')
        require(selection_calls == {0}, 'every positive branch must avoid diagnostic selection gates')
        require(len(observed_modes) == len(requested) == len(executed) == len(next_balances) == 1,
                'live balance/mode/service path must be deterministic')
        return (epoch, next(iter(balances)), next(iter(observed_modes)),
                next(iter(requested)), next(iter(executed)), next(iter(next_balances)), 0)

    for epoch in range(1, horizon + 1):
        if epoch == horizon:
            task_final = check_step(law, terminal, epoch)
        path.append(check_step(law, regular, epoch))
        law = advance(law, regular)
    endpoints = {}
    for objective in ('tasks', 'cycles'):
        result = run_exact(contract, policy, RETAIN, horizon, objective)
        require(result.gate_events['selection'] == 0, 'blind program has zero aggregate report reads')
        outcome = {
            'survival': number(result.survival), 'spent': number(result.spent),
            'selection_gate_invocations': str(result.gate_events['selection']),
        }
        if global_case is not None:
            require(global_case['horizon'] == horizon, 'global comparison horizon differs')
            best = global_case[objective]['best_survival']
            maximum = F(best['survival']['exact'])
            selected_spend = F(best['spent']['exact'])
            require(result.survival <= maximum, 'blind candidate exceeds frozen complete-library maximum')
            if result.survival == maximum:
                require(result.spent >= selected_spend, 'blind cost improves frozen optimum tie-break')
            outcome.update({
                'matches_global_max_survival': result.survival == maximum,
                'matches_selected_global_response_pair': (result.survival, result.spent) == (maximum, selected_spend),
                'global_best_program': best['program'],
                'global_survival_gap': number(maximum - result.survival),
            })
        endpoints[objective] = outcome
    return {
        'prices': asdict(prices), 'horizon': horizon, 'policy': policy.name,
        'enable': 'RETAIN', 'initial_endowment': contract.endowment,
        'mandatory_initial_writes': str(initial.writes),
        'startup_spend': str(sum(initial.spend_by_stage.values(), F(0))),
        'initial_write_spend': str(initial.spend_by_stage['initial_write']),
        'initial_balance': next(iter({state[3] for state in initial.measure})),
        'all_positive_branches_have_zero_selection_invocations': True,
        'positive_prefix_states_checked': state_checks,
        'positive_branch_traces_checked': branch_checks,
        'ordinary_live_path': tuple(path), 'tasks_final_step': task_final,
        **endpoints,
    }


def blind_diagnostic_control(horizon=8, global_data=None):
    by_price = {}
    if global_data is not None:
        require(global_data['horizon'] == horizon, 'global comparison horizon differs')
        by_price = {tuple(case['prices'][key] for key in ('gate', 'write', 'setup')): case
                    for case in global_data['cases']}
        require(set(by_price) == set(PRICE_GRID), 'global comparison must cover the fixed 24-point grid')
    cases = tuple(blind_diagnostic_case(Prices(*point), horizon, by_price.get(point))
                  for point in PRICE_GRID)
    comparison = {}
    if global_data is not None:
        comparison = {
            objective: {
                'matches_global_max_points': sum(case[objective]['matches_global_max_survival'] for case in cases),
                'matches_selected_response_pair_points': sum(case[objective]['matches_selected_global_response_pair'] for case in cases),
            }
            for objective in ('tasks', 'cycles')
        }
    return {
        'scope': 'fixed service/service+RETAIN candidate; actual positive traces, not a new policy search',
        'stored_report_use': 'no positive branch invokes diagnostic selection; task sensors remain active',
        'startup_scope': 'mandatory fresh initial acquisition is retained and paid at every price',
        'path_columns': ('epoch', 'entry_balance', 'mode', 'requested_service', 'executed_service',
                         'successful_exit_balance', 'selection_gate_invocations'),
        'path_scope': 'ordinary prefix shared by both endpoints; tasks replaces only the final step',
        'global_comparison': comparison,
        'global_comparison_source': None if global_data is None else 'docs/data/shared-budget-results.json',
        'cases': cases,
    }


def run(horizon=8):
    root = Path(__file__).resolve().parents[1]
    cases = (
        ("ideal_enable_budget_feedback", Contract(Prices(0, 6, 0), enable_noise="decoupled", decoupled_error=F(0))),
        ("actual_shared_health", Contract(Prices(1, 6, 0))),
    )
    scan_path = root / 'docs/data/shared-budget-results.json'
    scan = json.loads(scan_path.read_text()) if scan_path.exists() and horizon == 8 else None
    if scan is not None:
        require(scan['source_sha256']['cdka/shared_budget.py'] == hashlib.sha256(
            (root / 'cdka/shared_budget.py').read_bytes()).hexdigest(), 'global scan physical source is stale')
    return {
        "format": "shared-budget-continuation-controls-v1",
        "scope": "finite physical pair audits plus algebraic negative controls; no library optimum claim",
        "source_sha256": {path: hashlib.sha256((root / path).read_bytes()).hexdigest()
                          for path in ("cdka/shared_budget.py", "cdka/budget_continuation.py",
                                       "experiments/shared_budget_controls.py")},
        "algebraic_negative_controls": negative_controls(),
        "physical_cases": tuple(physical_case(name, contract, horizon) for name, contract in cases),
        "blind_diagnostic_use": blind_diagnostic_control(horizon, scan),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--horizon", type=int, default=8)
    parser.add_argument("--write", action="store_true", help="write the recomputed scientific artifact")
    parser.add_argument("--check", action="store_true", help="recompute and reject a missing or stale artifact")
    args = parser.parse_args(argv)
    started = perf_counter()
    result = run(args.horizon)
    destination = args.output
    payload = (json.dumps(result, default=str, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if args.write:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
    if args.check and (not destination.exists() or destination.read_bytes() != payload):
        raise ValueError("Stale or missing shared-budget controls: " + str(destination))
    summary = []
    for case in result["physical_cases"]:
        final = case["horizons"][-1]
        witness = case["delayed_common_state_witness"] or case["first_nonzero_response_residual"]
        summary.append({"case": case["name"], "tasks": final["tasks"],
                        "survival_Q_T": (final["reference_survival"]["approx"], final["candidate_survival"]["approx"]),
                        "spent_Q_T": (final["reference_spent"]["approx"], final["candidate_spent"]["approx"]),
                        "witness_state": None if witness is None else witness["state"],
                        "witness_tasks": None if witness is None else witness["total_tasks"],
                        "response_residual": None if witness is None else witness["response_residual"]["approx"],
                        "checked_contexts": case["reachable_contexts_checked"]})
    print(json.dumps({"output": str(destination), "physical_cases": summary,
                      "blind_diagnostic_comparison": result['blind_diagnostic_use']['global_comparison'],
                      "bytes": len(payload), "written": args.write, "checked": args.check,
                      "elapsed_seconds_nonbenchmark": perf_counter() - started}, indent=2))


if __name__ == "__main__":
    main()
