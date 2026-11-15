"""Exact bounded synthesis for one pathwise resource budget.

The price grid was fixed before evaluation. Each point enumerates all 16
stationary maintenance tables and the 21 cost/profile classes covering the
64 rooted enable netlists with at most two NANDs. No floating point ranks a
program. Run from the repository root; --cache-dir is an optional scratch
checkpoint directory. Timings are deliberately outside the scientific data.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import time

from cdka.recurrent_maintenance import Policy, policies
from cdka.selective_acquisition import ELIDE, FRESH, RETAIN, library
from cdka.shared_budget import Contract, Prices, run_exact


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/data/shared-budget-results.json'
HORIZON = 8
PRICE_GRID = tuple(product((0, 1, 2), (0, 6, 12, 24), (0, 6)))
TOLERANCES = (F(0), F(1, 10000), F(1, 1000), F(1, 100))
MODEL_SOURCES = ('cdka/shared_budget.py', 'cdka/selective_acquisition.py',
                 'cdka/recurrent_maintenance.py', 'experiments/shared_budget_sweep.py')


def exact_json(value):
    if isinstance(value, F):
        return {'exact': str(value), 'value': float(value)}
    if isinstance(value, dict):
        return {str(k): exact_json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_json(v) for v in value]
    return value


def source_hashes():
    return {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in MODEL_SOURCES}


def program_id(policy, enable_index):
    return f'{policy.name}:e{enable_index:02d}'


def packed(row):
    # Keep exact decision outputs here. Full branch accounting is returned by
    # run_exact and audited on every run; representative stage diagnostics are
    # recorded separately in shared-budget-controls.json instead of duplicated
    # under every reference and tolerance that selects the same program.
    return {'program': row['program'], 'policy': row['policy'],
            'enable': row['enable'], 'survival': row['survival'],
            'spent': row['spent']}


def best(rows):
    return min(rows, key=lambda r: (-r['survival'], r['spent'], r['program']))


def frontier(rows):
    # Equal output pairs have one deterministic original representative.
    ordered = sorted(rows, key=lambda r: (-r['survival'], r['spent'], r['program']))
    out, least_cost = [], None
    for row in ordered:
        if least_cost is None or row['spent'] < least_cost:
            out.append(row)
            least_cost = row['spent']
    return out


def summarize(rows, enables):
    optimum = best(rows)
    references = {
        'always_fresh': best([r for r in rows if enables[r['enable']] == FRESH]),
        'never_renew': best([r for r in rows if enables[r['enable']] == RETAIN]),
        'no_enable_nand': best([r for r in rows if enables[r['enable']].cost == 0]),
        'one_nand_elision': best([r for r in rows if enables[r['enable']] == ELIDE]),
        'no_maintenance': best([r for r in rows if r['policy'] == 'skip/skip']),
    }
    thresholds = []
    for tolerance in TOLERANCES:
        feasible = [r for r in rows if r['survival'] >= optimum['survival'] - tolerance]
        winner = min(feasible, key=lambda r: (r['spent'], -r['survival'], r['program']))
        thresholds.append({'loss_tolerance': tolerance, 'feasible_count': len(feasible),
                           'winner': packed(winner)})
    digest_rows = [(r['program'], str(r['survival']), str(r['spent'])) for r in rows]
    digest = sha256(json.dumps(digest_rows, separators=(',', ':')).encode()).hexdigest()
    return {
        'program_count': len(rows), 'complete_response_sha256': digest,
        'best_survival': packed(optimum),
        'references': {name: packed(row) for name, row in references.items()},
        'gain_over_best_no_enable_nand': optimum['survival'] - references['no_enable_nand']['survival'],
        'cost_at_survival_tolerance': thresholds,
        'frontier': [{k: r[k] for k in ('program', 'policy', 'enable', 'survival', 'spent')}
                     for r in frontier(rows)],
    }


def one_case(prices, horizon=HORIZON):
    g, w, i = prices
    contract = Contract(prices=Prices(gate=g, write=w, setup=i))
    enables, _ = library(2)
    rows = {'tasks': [], 'cycles': []}
    for policy in policies():
        for e, enable in enumerate(enables):
            for objective in rows:
                summary = run_exact(contract, policy, enable, horizon=horizon,
                                    objective=objective)
                rows[objective].append({'program': program_id(policy, e),
                                        'policy': policy.name, 'enable': e,
                                        'survival': summary.survival,
                                        'spent': summary.spent, 'summary': summary})
    return exact_json({'prices': {'gate': g, 'write': w, 'setup': i},
                       'horizon': horizon,
                       **{objective: summarize(values, enables)
                          for objective, values in rows.items()}})


def metadata():
    enables, stats = library(2)
    return {
        'schema': 'cdka.shared-budget/v1', 'date': '2026-11-15',
        'date_basis': 'UTC',
        'parent_commit': 'e54de20fedd50358ad75328c336ce07e8492283b',
        'physical_baseline_commit': 'c8eb621acf04c6581795662596c3c41cf2cac43c',
        'question': 'Does selective acquisition help when its actual execution and writes use the actuator reserve?',
        'scientific_status': 'exact bounded model synthesis; physical parameter values are illustrative',
        'horizon': HORIZON, 'primary_objective': 'tasks',
        'primary_objective_definition': 'H-1 complete cycles then one terminal task; no final enable or write charged to any program',
        'secondary_objective': 'H complete maintenance/work/acquisition cycles',
        'predeclared_grid': [dict(zip(('gate', 'write', 'setup'), p)) for p in PRICE_GRID],
        'grid_selection': 'Fixed before outcomes; includes free-resource limit and adverse prices, not fitted to produce a gain',
        'endowment_and_capacity': 96, 'commissioning': 24,
        'per_task_overhead': 24, 'service': 48, 'successful_cycle_harvest': 48,
        'resource_unit': 'one old operational token equals 24 integer quanta',
        'maintenance_policies': [p.name for p in policies()],
        'enable_library': [dict(id=f'e{e:02d}', gates=c.gates, output=c.output,
                                gate_count=c.cost, fault_free_truth=c.truth(),
                                exact_noise_profile=c.profile()) for e, c in enumerate(enables)],
        'library_count_by_depth': list(stats),
        'raw_complete_programs': 16 * sum(s['netlists'] for s in stats),
        'distinct_cost_profile_programs': 16 * len(enables),
        'selection_tie_break': 'highest survival, then least incurred spend, then lexical program identifier',
        'cost_warning': 'Expected spend includes failed prefixes. A cheap early failure is not an efficiency improvement; survival tolerance is explicit.',
        'reference_scope': 'Each reference is optimized over its complete declared subfamily at the same prices and endowment.',
        'source_sha256': source_hashes(),
    }


def run(cache_dir=None, verbose=False):
    cases = []
    hashes = source_hashes()
    for prices in PRICE_GRID:
        path = None if cache_dir is None else cache_dir / ('g%d-w%d-i%d.json' % prices)
        cached = json.loads(path.read_text()) if path is not None and path.exists() else None
        if cached is not None and cached.get('source_sha256') == hashes:
            result = cached['case']
        else:
            started = time.perf_counter()
            result = one_case(prices)
            if path is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({'source_sha256': hashes, 'case': result},
                                           ensure_ascii=False, sort_keys=True) + '\n')
            if verbose:
                print(json.dumps({'prices': prices, 'seconds': round(time.perf_counter()-started, 3),
                                  'task_best': result['tasks']['best_survival']['program'],
                                  'task_survival': result['tasks']['best_survival']['survival']['value']}), flush=True)
        cases.append(result)
    return dict(metadata(), cases=cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--cache-dir', type=Path)
    parser.add_argument('--point', nargs=3, type=int, metavar=('GATE', 'WRITE', 'SETUP'))
    args = parser.parse_args()
    if args.point is not None:
        prices = tuple(args.point)
        if prices not in PRICE_GRID:
            raise ValueError('Point is outside the declared price grid')
        started = time.perf_counter()
        case = one_case(prices)
        if args.cache_dir is not None:
            args.cache_dir.mkdir(parents=True, exist_ok=True)
            (args.cache_dir / ('g%d-w%d-i%d.json' % prices)).write_text(
                json.dumps({'source_sha256': source_hashes(), 'case': case},
                           ensure_ascii=False, sort_keys=True) + '\n')
        print(json.dumps({'prices': prices, 'seconds': time.perf_counter()-started,
                          'tasks': case['tasks']['best_survival'],
                          'cycles': case['cycles']['best_survival']}, ensure_ascii=False))
        return
    result = run(args.cache_dir, verbose=True)
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text)
    if args.check and (not OUTPUT.exists() or OUTPUT.read_text() != text):
        raise ValueError('Stale or missing shared-budget results')
    print(json.dumps({'price_points': len(result['cases']),
                      'programs_per_point': result['distinct_cost_profile_programs'],
                      'objectives': ['tasks', 'cycles'],
                      'positive_nand_gain_points_tasks': sum(
                          F(c['tasks']['gain_over_best_no_enable_nand']['exact']) > 0
                          for c in result['cases'])}))


if __name__ == '__main__':
    main()
