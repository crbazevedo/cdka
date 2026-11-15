"""Exact optional-blind-startup synthesis and diagnostic-channel interventions.

The inherited grid, rates, program grammar and H8 endpoints are fixed. Physical
candidates comprise 336 paid preparations and 84 explicitly blind preparations
that omit acquisition. Two separately labelled nonphysical controls destroy
the initial correlation, or every acquired report's correlation, respectively.
Neither analytical intervention is offered as a free physical random source.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
import time

from cdka.recurrent_maintenance import policies
from cdka.selective_acquisition import FRESH, RETAIN, library
from cdka.shared_budget import Contract, Prices
from cdka.optional_startup import blind, run_exact
from cdka.diagnostic_ablation import run_exact as run_all_null
from experiments.shared_budget_sweep import (
    HORIZON, PRICE_GRID, TOLERANCES, exact_json, program_id,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/data/optional-startup-results.json'
FROZEN = ROOT / 'docs/data/shared-budget-results.json'
INDEPENDENT = ROOT / 'docs/data/optional-startup-independent.json'
MODEL_SOURCES = (
    'cdka/recurrent_maintenance.py', 'cdka/selective_acquisition.py',
    'cdka/shared_budget.py', 'cdka/optional_startup.py',
    'cdka/diagnostic_ablation.py', 'experiments/shared_budget_sweep.py',
    'experiments/optional_startup_sweep.py',
)


def source_hashes():
    return {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in MODEL_SOURCES}


def packed(row):
    return {k: row[k] for k in ('program', 'base_program', 'preparation',
                               'policy', 'enable', 'survival', 'spent')}


def best(rows):
    return min(rows, key=lambda r: (-r['survival'], r['spent'], r['program']))


def frontier(rows):
    ordered = sorted(rows, key=lambda r: (-r['survival'], r['spent'], r['program']))
    out, least = [], None
    for row in ordered:
        if least is None or row['spent'] < least:
            out.append(packed(row))
            least = row['spent']
    return out


def response_hash(rows, lexical=False):
    # Same base-program order and response encoding as the frozen SB scan.
    ordered = sorted(rows, key=lambda r: r['base_program']) if lexical else rows
    response = [(r['base_program'], str(r['survival']), str(r['spent'])) for r in ordered]
    return sha256(json.dumps(response, separators=(',', ':')).encode()).hexdigest()


def make_row(policy, e, preparation, summary):
    base = program_id(policy, e)
    return dict(program=f'{preparation}:{base}', base_program=base,
                preparation=preparation, policy=policy.name, enable=e,
                survival=summary.survival, spent=summary.spent, summary=summary)


def diagnostics(row):
    s = row['summary']
    return dict(packed(row), selection_gate_events=s.gate_events['selection'],
                enable_gate_events=s.gate_events['enable'], writes=s.writes,
                services=s.services, spend_by_stage=s.spend_by_stage,
                remaining=s.remaining, earned=s.earned, spilled=s.spilled,
                failures_by_cause=s.failures_by_cause)


def summarize(groups, enables, frozen, independent):
    paid, omitted = groups['fresh'], groups['omit']
    physical = paid + omitted
    blind_rows = [r for r in physical if r['policy'] in
                  ('skip/skip', 'skip/service', 'service/skip', 'service/service')]
    initial_world = groups['initial_null'] + omitted
    all_world = groups['all_null'] + omitted
    references = {
        'physical': best(physical), 'paid_only': best(paid),
        'blind_optional': best(blind_rows), 'blind_omitted': best(omitted),
        'initial_null_world': best(initial_world),
        'all_null_world': best(all_world),
        'no_enable_nand': best([r for r in physical if enables[r['enable']].cost == 0]),
        'never_renew': best([r for r in physical if enables[r['enable']] == RETAIN]),
        'always_fresh': best([r for r in physical if enables[r['enable']] == FRESH]),
        'no_maintenance': best([r for r in physical if r['policy'] == 'skip/skip']),
    }
    optimum = references['physical']
    if optimum['survival'] < references['blind_optional']['survival']:
        raise AssertionError('the physical union must include its blind comparator')
    hashes = {name: response_hash(rows, lexical=name == 'omit') for name, rows in groups.items()}
    if hashes['fresh'] != frozen['complete_response_sha256']:
        raise AssertionError('the inherited paid preparation responses changed')
    if hashes['omit'] != independent['complete_response_sha256']:
        raise AssertionError('omitted responses disagree with the independent raw-physics oracle')
    by_group = {name: {r['base_program']: r for r in rows}
                for name, rows in groups.items()}
    blind_invariance_count = 0
    for row in omitted:
        original = by_group['fresh'][row['base_program']]['summary']
        for name in ('initial_null', 'all_null'):
            counterfactual = by_group[name][row['base_program']]['summary']
            for attribute in ('survival', 'spent', 'spend_by_stage', 'failures_by_cause',
                              'gate_events', 'writes', 'services', 'earned', 'spilled',
                              'failed_remaining', 'remaining', 'task_successes',
                              'completed_cycles', 'balance_distribution', 'curve'):
                if getattr(original, attribute) != getattr(counterfactual, attribute):
                    raise AssertionError('report intervention changed blind projected dynamics')
            blind_invariance_count += 1
    paired = {}
    for name in ('initial_null', 'all_null'):
        control = (optimum if optimum['preparation'] == 'omit' else
                   by_group[name][optimum['base_program']])
        paired[name] = dict(control=diagnostics(control),
                            survival_effect=optimum['survival'] - control['survival'],
                            spent_effect=optimum['spent'] - control['spent'])
    differences = []
    for row in omitted:
        paid_row = by_group['fresh'][row['base_program']]
        differences.append(dict(program=row['base_program'],
                                survival_effect=row['survival'] - paid_row['survival'],
                                spent_effect=row['spent'] - paid_row['spent'],
                                paid=packed(paid_row), omitted=packed(row)))
    thresholds = []
    for tolerance in TOLERANCES:
        feasible = [r for r in physical if r['survival'] >= optimum['survival'] - tolerance]
        winner = min(feasible, key=lambda r: (r['spent'], -r['survival'], r['program']))
        thresholds.append(dict(loss_tolerance=tolerance, feasible_count=len(feasible),
                               winner=packed(winner)))
    return {
        'program_counts': {**{name: len(rows) for name, rows in groups.items()},
                           'physical_union': len(physical), 'blind_union': len(blind_rows)},
        'complete_response_sha256': hashes, 'frozen_paid_certificate_agrees': True,
        'independent_omitted_certificate_agrees': True,
        'blind_channel_invariance_comparisons': blind_invariance_count,
        'best': {name: diagnostics(row) for name, row in references.items()},
        'physical_gap_over_optional_blind': optimum['survival'] - references['blind_optional']['survival'],
        'physical_gain_over_paid_only': optimum['survival'] - references['paid_only']['survival'],
        'gain_over_no_enable_nand': optimum['survival'] - references['no_enable_nand']['survival'],
        'reoptimized_initial_channel_effect': optimum['survival'] - references['initial_null_world']['survival'],
        'reoptimized_all_channel_effect': optimum['survival'] - references['all_null_world']['survival'],
        'physical_winner_interventions': paired,
        'blind_omission_comparison': {
            'programs': len(differences),
            'improved': sum(r['survival_effect'] > 0 for r in differences),
            'unchanged': sum(r['survival_effect'] == 0 for r in differences),
            'worsened': sum(r['survival_effect'] < 0 for r in differences),
            'largest_gain': max(differences, key=lambda r: (r['survival_effect'], r['program'])),
            'largest_loss': min(differences, key=lambda r: (r['survival_effect'], r['program'])),
        },
        'cost_at_survival_tolerance': thresholds, 'physical_frontier': frontier(physical),
    }


def one_case(prices, frozen_case, independent_case):
    contract = Contract(prices=Prices(*prices))
    enables, _ = library(2)
    results = {}
    for objective in ('tasks', 'cycles'):
        groups = {name: [] for name in ('fresh', 'omit', 'initial_null', 'all_null')}
        for policy in policies():
            for e, enable in enumerate(enables):
                for name, preparation in (('fresh', 'fresh'), ('initial_null', 'independent')):
                    s = run_exact(contract, policy, enable, horizon=HORIZON,
                                  objective=objective, preparation=preparation)
                    groups[name].append(make_row(policy, e, name, s))
                s = run_all_null(contract, policy, enable, horizon=HORIZON, objective=objective)
                groups['all_null'].append(make_row(policy, e, 'all_null', s))
                if blind(policy):
                    s = run_exact(contract, policy, enable, horizon=HORIZON,
                                  objective=objective, preparation='omit')
                    groups['omit'].append(make_row(policy, e, 'omit', s))
        results[objective] = summarize(groups, enables, frozen_case[objective], independent_case[objective])
    return exact_json(dict(prices=dict(zip(('gate', 'write', 'setup'), prices)), **results))


def metadata():
    enables, stats = library(2)
    return {
        'schema': 'cdka.optional-startup/v1', 'date': '2026-11-15', 'date_basis': 'Europe/Lisbon',
        'parent_commit': '24d1e35ecde75defd495b5272bfb653f427bf528',
        'physical_baseline_commit': 'c8eb621acf04c6581795662596c3c41cf2cac43c',
        'question': 'Does paid diagnostic acquisition add decision value after blind programs can decline startup acquisition?',
        'horizon': HORIZON, 'primary_objective': 'tasks', 'secondary_objective': 'cycles',
        'initial_degraded_prior': F(1, 2),
        'endowment': 96, 'capacity': 96, 'commissioning': 24,
        'predeclared_grid': [dict(zip(('gate', 'write', 'setup'), p)) for p in PRICE_GRID],
        'physical_family': '336 original paid programs plus 84 omitted-startup programs with both maintenance bins restricted to skip/service',
        'family_boundary': 'Does not include nonblind programs that defer their first read until a later acquired report, arbitrary history-dependent control or additional memory/clock hardware',
        'raw_physical_programs': (16 + 4) * sum(s['netlists'] for s in stats),
        'physical_programs_per_point': 420,
        'intervention_programs_per_point': 672,
        'evaluations_per_point_and_objective': 1092,
        'initial_null': 'Same paid startup debit and full three-cell report marginal, independent of initial hidden health; subsequent acquisition law unchanged',
        'all_null': 'At startup and every paid acquisition, replace the diagnostic channel by the fixed prior-mixture joint report marginal; all other physical laws unchanged',
        'intervention_boundary': 'Analytical interventions, not installed alternative sensors or free randomness. Hidden health still affects bank faults and task/service dynamics; endogenous report marginals need not match after the first report.',
        'selection_tie_break': 'highest survival, then least incurred spend, then lexical preparation:program identifier',
        'cost_warning': 'Spend includes failed prefixes; comparisons impose an explicit survival tolerance.',
        'enable_library': [dict(id=f'e{e:02d}', gate_count=c.cost, gates=c.gates,
                                output=c.output, fault_free_truth=c.truth()) for e, c in enumerate(enables)],
        'source_sha256': source_hashes(),
        'frozen_paid_data_sha256': sha256(FROZEN.read_bytes()).hexdigest(),
        'independent_omitted_data_sha256': sha256(INDEPENDENT.read_bytes()).hexdigest(),
    }


def run(cache_dir=None, verbose=False):
    frozen = json.loads(FROZEN.read_text())
    by_price = {tuple(c['prices'][k] for k in ('gate', 'write', 'setup')): c for c in frozen['cases']}
    independent = json.loads(INDEPENDENT.read_text())
    independent_by_price = {tuple(c['prices'][k] for k in ('gate', 'write', 'setup')): c for c in independent['cases']}
    hashes = dict(source_hashes(), **{
        'frozen_paid_data': sha256(FROZEN.read_bytes()).hexdigest(),
        'independent_omitted_data': sha256(INDEPENDENT.read_bytes()).hexdigest(),
    })
    cases = []
    for prices in PRICE_GRID:
        path = None if cache_dir is None else cache_dir / ('g%d-w%d-i%d.json' % prices)
        cached = json.loads(path.read_text()) if path is not None and path.exists() else None
        if cached is not None and cached.get('source_sha256') == hashes:
            case = cached['case']
        else:
            started = time.perf_counter()
            case = one_case(prices, by_price[prices], independent_by_price[prices])
            if path is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({'source_sha256': hashes, 'case': case},
                                           ensure_ascii=False, sort_keys=True) + '\n')
            if verbose:
                print(json.dumps(dict(prices=prices, seconds=round(time.perf_counter()-started, 3),
                                      best=case['tasks']['best']['physical']['program'],
                                      survival=case['tasks']['best']['physical']['survival']['value'],
                                      blind_gap=case['tasks']['physical_gap_over_optional_blind']['value'],
                                      channel_effect=case['tasks']['reoptimized_all_channel_effect']['value'])), flush=True)
        cases.append(case)
    return exact_json(dict(metadata(), cases=cases))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--cache-dir', type=Path)
    args = parser.parse_args()
    result = run(args.cache_dir, verbose=True)
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.write:
        OUTPUT.write_text(text)
    if args.check and (not OUTPUT.exists() or OUTPUT.read_text() != text):
        raise ValueError('Stale or missing optional-startup results')
    print(json.dumps(dict(price_points=len(result['cases']), evaluations=24 * 2 * 1092,
                          positive_physical_blind_gaps=sum(F(c['tasks']['physical_gap_over_optional_blind']['exact']) > 0 for c in result['cases']),
                          positive_all_channel_effects=sum(F(c['tasks']['reoptimized_all_channel_effect']['exact']) > 0 for c in result['cases']))))


if __name__ == '__main__':
    main()
