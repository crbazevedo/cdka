"""Exact program-family coverage, controls, and matched-output cost comparison.

python -m experiments.program_family_sweep --write --check
python -m experiments.program_family_sweep --benchmark

Deterministic rational evidence is separate from local runtime measurements.
The benchmark asks both methods for informed values, one minimax program and
one maximin program; neither is asked to publish prediction envelopes.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import platform
from statistics import median
from time import perf_counter

from cdka.boundary_voting import raw_update, voter_profile
from cdka.maintenance_access import base_operators, base_probes, maintenance_row
from cdka.program_families import (
    binding, compile_family, check_family, unpruned_shared, dominated,
    evaluate_frontier, compile_decision, check_decision,
)
from cdka.reachable_diagnosis import (
    preparation_laws, plan_words, contract,
    acquisition, advance_updates, evaluate,
)
from cdka.reachable_restriction import contrast_signature, contrast_response
from cdka.semantic_closure import word_value

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/data'
RESULT = DATA / 'program-family-results.json'
BENCHMARK = DATA / 'program-family-benchmark.json'
PARENT = '5972303fb8728fe0d0bbea9beed796c8209f9b40'


def exact(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): exact(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact(v) for v in value]
    return value


def encoded(value):
    return json.dumps(exact(value), sort_keys=True, separators=(',', ':')).encode()


def quality(certificate, frontier, values):
    p = certificate['minimax_plan']
    return {
        'minimax_plan': frontier[p][0] or 'I',
        'minimax_regret': certificate['minimax_regret'],
        'minimax_minimum_fidelity': str(min(row[p] for row in values)),
        'maximin_plan': frontier[certificate['maximin_plan']][0] or 'I',
        'maximin_fidelity': certificate['maximin_fidelity'],
        'informed_values': certificate['preparation_best'],
    }


def decision(frontier, cohort, signatures, scope):
    values = evaluate_frontier(frontier, signatures)
    kwargs = {
        'preparation_labels': list(cohort),
        'plan_labels': [w or 'I' for w, _ in frontier],
        'contract': scope,
    }
    cert = compile_decision(values, **kwargs)
    assert check_decision(json.loads(encoded(cert)), values, **kwargs)
    return values, cert, quality(cert, frontier, values)


def gate_indices(values, maximum_regret, minimum_fidelity):
    best = [max(row) for row in values]
    return [j for j in range(len(values[0]))
            if max(b-row[j] for b, row in zip(best, values)) <= maximum_regret
            and min(row[j] for row in values) >= minimum_fidelity]


def build():
    ops, g = base_operators(), base_probes()['readout']
    libraries = {}
    cases = []
    coverage_checks = physical_retained_checks = 0
    for k in (0, 1, 2, 4, 6, 8):
        front, cert, stats = compile_family(ops, g, k)
        assert check_family(json.loads(encoded(cert)), ops, g, k) == front
        full = unpruned_shared(ops, g, k)
        assert set(w for w, _ in full) == {''.join(w) for w in plan_words(k)}
        for word, response in front:
            assert response == contrast_response(word_value(ops, tuple(word), g))
            physical_retained_checks += 1
        for _, response in full:
            assert any(dominated(other, response) for _, other in front)
            coverage_checks += 1
        if k <= 4:
            assert dict(full) == {
                ''.join(w): contrast_response(word_value(ops, w, g))
                for w in plan_words(k)
            }
        libraries[k] = (front, cert, stats, full)

    principal = None
    for h, k in ((2, 4), (4, 4), (6, 4), (2, 6), (4, 6), (2, 8), (4, 8)):
        cohort = preparation_laws(h)
        signatures = [contrast_signature(*law) for law in cohort.values()]
        front, cert, stats, full = libraries[k]
        scope = {**contract(h, k), 'parent_commit': PARENT,
                 'program_cover_binding': cert['binding']}
        values, dc, result = decision(front, cohort, signatures, scope)
        full_values, _, reference = decision(full, cohort, signatures, scope)
        for name in ('minimax_regret', 'maximin_fidelity', 'informed_values'):
            assert result[name] == reference[name]
        cases.append({'history_length': h, 'ordinary_updates': k,
                      'preparations': len(cohort), 'programs': len(full),
                      'retained_programs': len(front), 'stats': stats[-1],
                      'decision': result})
        if (h, k) == (2, 4):
            previous = json.loads((DATA/'reachable-diagnosis-results.json').read_text())['fixture']
            positions = {w or 'I': j for j, (w, _) in enumerate(full)}
            for i, old_row in enumerate(previous['values']):
                assert all(F(value) == full_values[i][positions[p]]
                           for p, value in zip(previous['plans'], old_row))
            gates = []
            for delta, floor in ((F(1, 500), F(21, 25)), (F(3, 1000), F(21, 25)),
                                 (F(3, 1000), F(17, 20)), (F(1, 200), F(17, 20))):
                reduced = gate_indices(values, delta, floor)
                exhaustive = gate_indices(full_values, delta, floor)
                assert bool(reduced) == bool(exhaustive)
                gates.append({'maximum_regret': delta, 'minimum_fidelity': floor,
                              'feasible': bool(reduced),
                              'retained_witnesses': [front[j][0] or 'I' for j in reduced],
                              'exhaustive_feasible_count': len(exhaustive)})
            principal = {'contract': scope, 'preparations': list(cohort),
                         'signatures': signatures, 'programs': [w or 'I' for w, _ in front],
                         'responses': [q for _, q in front], 'values': values,
                         'family_certificate': cert, 'decision_certificate': dc,
                         'stats_by_level': stats, 'joint_gates': gates,
                         'summary': result}

    controls = {}
    for name, eta, success in (
        ('uninformative_sensor', F(1, 2), F(4, 5)),
        ('zero_repair', F(1, 10), F(0)),
    ):
        operators = base_operators(success)
        front, cert, stats = compile_family(operators, g, 4)
        assert check_family(cert, operators, g, 4) == front
        full = unpruned_shared(operators, g, 4)
        cohort = preparation_laws(2, eta)
        signatures = [contrast_signature(*law) for law in cohort.values()]
        scope = contract(2, 4, eta, success=success)
        values, dc, result = decision(front, cohort, signatures, scope)
        full_values, _, reference = decision(full, cohort, signatures, scope)
        assert all(result[k] == reference[k]
                   for k in ('minimax_regret', 'maximin_fidelity', 'informed_values'))
        controls[name] = {'retained': len(front), 'decision': result}
        if eta == F(1, 2):
            assert all(v == F(1, 2) for row in values for v in row)
            controls[name]['all_original_programs_tie'] = len(full)
            controls[name]['all_original_ties_preserved'] = False

    law = advance_updates(acquisition(), 'DDDD')
    early, late = evaluate(law, 'MR'), evaluate(law, 'RM')
    assert early > late
    controls['maintenance_not_always_last'] = {
        'history': 'DDDD', 'ordinary_updates': 1,
        'MR': early, 'RM': late, 'advantage_of_MR': early-late,
    }
    return exact({
        'schema': 'cdka.program-family-experiment/v1', 'parent_commit': PARENT,
        'physical_change': False, 'active_branches': ['R11', 'R14'],
        'fixture': principal, 'scaling': cases, 'controls': controls,
        'validation': {
            'checked_horizons': [0, 1, 2, 4, 6, 8],
            'complete_program_dominance_checks': coverage_checks,
            'retained_physical_response_checks': physical_retained_checks,
            'principal_parent_response_agreements': 384,
            'checker_enumerates_pruned_complete_words': False,
        },
        'limits': [
            'Every 2^K no-maintenance suffix remains in full16.',
            'Every 2^h preparation history remains explicit.',
            'One optimum and feasibility are preserved, not all ties or prediction envelopes.',
            'Executed physical cost is not an objective of this response dominance.',
        ],
    })


def timed(call, repeats=3):
    samples = []
    result = None
    for _ in range(repeats):
        start = perf_counter()
        result = call()
        samples.append(perf_counter()-start)
    return result, median(samples), samples


def rational_bits(rows):
    return max(max(v.numerator.bit_length(), v.denominator.bit_length())
               for row in rows for v in row)


def benchmark():
    def cold_model():
        # These physical primitives cache their raw channels. Rebuild them for
        # every setup sample, even when --benchmark follows --write --check.
        raw_update.cache_clear()
        maintenance_row.cache_clear()
        voter_profile.cache_clear()
        return base_operators(), base_probes()['readout']
    (ops, g), kernel, kernel_samples = timed(cold_model)
    output = {
        'schema': 'cdka.program-family-benchmark/v1', 'parent_commit': PARENT,
        'environment': {'python': platform.python_version(), 'platform': platform.platform()},
        'repeats': 3, 'shared_kernel_seconds': kernel,
        'shared_kernel_samples': kernel_samples,
        'convention': 'Sum of median component times from three sequential runs, '
            'including a cold physical-kernel construction with its channel caches reset. '
            'Both methods return informed values, one minimax and one maximin. '
            'The enumerator receives the same suffix sharing,4D prefixes and4x16 M contraction. '
            'Only the pruned method pays the independent family checker. '
            'Totals include kernel/preparation/encoding/compilation, certificate serialization '
            'and parsing, queries and both decision certificate construction/checking. '
            'Optional query-cache export is measured but excluded from the decision-only total.',
        'cases': [],
    }
    cohorts = {}
    for h in (2, 4):
        cohort, prep, prep_samples = timed(lambda: preparation_laws(h))
        signatures, enc, enc_samples = timed(
            lambda: [contrast_signature(*law) for law in cohort.values()])
        cohorts[h] = cohort, signatures, prep, enc, prep_samples, enc_samples

    for k in (4, 6, 8):
        (front, cert, stats), compile_time, compile_samples = timed(lambda: compile_family(ops, g, k))
        payload, family_serialize, family_serialize_samples = timed(lambda: encoded(cert))
        checked, family_check, family_check_samples = timed(
            lambda: check_family(json.loads(payload), ops, g, k))
        assert checked == front
        full, baseline_compile, baseline_compile_samples = timed(lambda: unpruned_shared(ops, g, k))
        assert len(full) == (k+2)*2**k
        for h, (cohort, signatures, prep, enc, prep_samples, enc_samples) in cohorts.items():
            scope = {**contract(h, k), 'program_cover_binding': cert['binding']}
            case = {'history_length': h, 'ordinary_updates': k, 'preparations': len(cohort),
                    'programs': len(full), 'stats': stats[-1], 'preparation_seconds': prep,
                    'encoding_seconds': enc, 'preparation_samples': prep_samples,
                    'encoding_samples': enc_samples, 'methods': []}
            for name, entries, ct, csamples, fs, fssamples, fv, fvsamples, family_bytes in (
                ('shared4_no_pruning', full, baseline_compile, baseline_compile_samples,
                 0.0, [], 0.0, [], 0),
                ('certified_cone_frontier', front, compile_time, compile_samples,
                 family_serialize, family_serialize_samples, family_check, family_check_samples, len(payload)),
            ):
                values, query, query_samples = timed(lambda: evaluate_frontier(entries, signatures))
                kwargs = {'preparation_labels': list(cohort),
                          'plan_labels': [w or 'I' for w, _ in entries], 'contract': scope}
                dc, construct, construct_samples = timed(lambda: compile_decision(values, **kwargs))
                dcbytes, serialize, serialize_samples = timed(lambda: encoded(dc))
                _, check, check_samples = timed(lambda: check_decision(json.loads(dcbytes), values, **kwargs))
                cache, cache_serialize, cache_samples = timed(lambda: encoded(entries))
                total = kernel+prep+enc+ct+fs+fv+query+construct+serialize+check
                case['methods'].append({
                    'method': name, 'evaluated_programs': len(entries), 'compile_seconds': ct,
                    'family_serialize_seconds': fs, 'family_check_seconds': fv,
                    'family_certificate_bytes': family_bytes, 'query_seconds': query,
                    'decision_compile_seconds': construct, 'decision_serialize_seconds': serialize,
                    'decision_check_seconds': check, 'decision_certificate_bytes': len(dcbytes),
                    'total_seconds': total, 'optional_cache_export_seconds': cache_serialize,
                    'cache_bytes': len(cache), 'maximum_response_rational_bits': rational_bits([r for _, r in entries]),
                    'maximum_value_rational_bits': rational_bits(values),
                    'quality': quality(dc, entries, values),
                    'samples': {'compile': csamples, 'family_serialize': fssamples,
                                'family_check': fvsamples, 'query': query_samples,
                                'decision_compile': construct_samples, 'decision_serialize': serialize_samples,
                                'decision_check': check_samples, 'optional_cache_export': cache_samples},
                })
            a, b = case['methods']
            assert all(a['quality'][field] == b['quality'][field]
                       for field in ('minimax_regret', 'maximin_fidelity', 'informed_values'))
            case['total_speedup'] = a['total_seconds']/b['total_seconds']
            output['cases'].append(case)
            print(json.dumps({'h': h, 'k': k, 'full': len(full), 'retained': len(front),
                              'never_generated': stats[-1]['complete_words_never_generated'],
                              'baseline_seconds': a['total_seconds'], 'frontier_seconds': b['total_seconds'],
                              'speedup': case['total_speedup']}), flush=True)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--benchmark', action='store_true')
    args = parser.parse_args()
    if args.write or args.check or not args.benchmark:
        result = build()
        if args.write:
            RESULT.write_text(json.dumps(result, indent=2)+'\n')
        if args.check:
            assert json.loads(RESULT.read_text()) == result, 'stale program-family evidence'
        print(json.dumps({'validation': result['validation'],
                          'principal': result['fixture']['summary']}, indent=2))
    if args.benchmark:
        BENCHMARK.write_text(json.dumps(benchmark(), indent=2)+'\n')
