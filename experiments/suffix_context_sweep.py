"""Exact finite-horizon suffix covers and cold matched-output benchmarks.

python -m experiments.suffix_context_sweep --write --check
python -m experiments.suffix_context_sweep --check
python -m experiments.suffix_context_sweep --benchmark

Only --write and --benchmark optimize cone discovery with optional NumPy/SciPy.
--check verifies frozen rational witnesses with the standard library, and
independently reconstructs reference frontiers and conservative repair controls.
A single
maximum-depth cone is stored; each smaller horizon uses its checked prefix.
The family certificates are reconstructed as self-contained objects before
checking. No numerical solver participates in verification.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from importlib.metadata import version
import json
from pathlib import Path
import platform
from statistics import median
import subprocess
import sys
from time import perf_counter

from cdka.boundary_voting import raw_update, voter_profile
from cdka.maintenance_access import base_operators, base_probes, maintenance_row
from cdka.program_families import (
    compile_family as compile_parent, unpruned_shared, dominated,
    evaluate_frontier, compile_decision, check_decision,
)
from cdka.reachable_diagnosis import preparation_laws, plan_words, contract
from cdka.reachable_restriction import contrast_signature, contrast_response
from cdka.semantic_closure import word_value
from cdka.suffix_features import (
    compile_features, check_features, compile_feature_family,
    check_feature_family,
)
from cdka.suffix_contexts import discover_cone, check_cone, compile_family, check_family


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/data'
LIBRARY = DATA / 'suffix-context-certificates.json'
RESULT = DATA / 'suffix-context-results.json'
BENCHMARK = DATA / 'suffix-context-benchmark.json'
PARENT = 'ce252821be4fb5a5075ad12f71ee2da7f14acb7d'
HORIZONS = (0, 1, 2, 4, 6, 8, 10, 12, 14)
QUALITY_FIELDS = ('minimax_regret', 'maximin_fidelity', 'informed_values')


def exact(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): exact(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact(item) for item in value]
    return value


def encoded(value):
    return json.dumps(exact(value), sort_keys=True, separators=(',', ':')).encode()


def rational_bits(rows):
    return max((max(value.numerator.bit_length(), value.denominator.bit_length())
                for row in rows for value in row), default=0)


def certificate_rational_bits(value):
    if type(value) in (tuple, list):
        return max(map(certificate_rational_bits, value), default=0)
    if type(value) is dict:
        return max(map(certificate_rational_bits, value.values()), default=0)
    if type(value) in (int, str, F):
        try:
            item = F(value)
        except (ValueError, ZeroDivisionError):
            return 0
        return max(item.numerator.bit_length(), item.denominator.bit_length())
    return 0


def cone_prefix(cone, k):
    """Truncate a nested witness; the resulting cone is independently checked."""
    depth = max(0, k - 1)
    counts = cone['counts'][:depth + 1]
    if len(counts) != depth + 1:
        raise ValueError('stored cone does not cover requested horizon')
    return {'rows': cone['rows'][:counts[-1]], 'counts': counts,
            'initial': cone['initial'],
            'transitions': cone['transitions'][:counts[-2] if depth else 0]}


def family_certificate(library, k):
    return {**library['families'][str(k)], 'features': library['features'],
            'cone': cone_prefix(library['context_cone'], k)}


def construction_stats(certificate):
    """Count every generated candidate name, including discarded suffixes."""
    k = certificate['ordinary_updates']
    counts = certificate['cone']['counts']
    suffix, frontier, result = [''], [], []
    for n, layer in enumerate(certificate['layers']):
        candidates = [a + word for word in suffix for a in ('D', 'R')] if n else suffix
        suffix = [candidates[i] for i in layer['suffix']['keep']]
        complete = (([a + word for word in frontier for a in ('D', 'R')]
                     if n else ['']) + ['M' + word for word in suffix])
        frontier = [complete[i] for i in layer['front']['keep']]
        generated = len(set(candidates) | set(complete))
        result.append({'n': n, 'no_m_suffix_candidates': len(candidates),
                       'no_m_suffixes_retained': len(suffix),
                       'no_m_suffixes_never_generated': 2**n - len(candidates),
                       'context_rows_used': counts[k - n] if n else 0,
                       'candidates': len(complete), 'retained': len(frontier),
                       'complete_words_generated': generated,
                       'complete_words_never_generated': (n + 2)*2**n - generated})
    return result


def quality(certificate, frontier, values):
    minimax = certificate['minimax_plan']
    return {'minimax_plan': frontier[minimax][0] or 'I',
            'minimax_regret': certificate['minimax_regret'],
            'minimax_minimum_fidelity': str(min(row[minimax] for row in values)),
            'maximin_plan': frontier[certificate['maximin_plan']][0] or 'I',
            'maximin_fidelity': certificate['maximin_fidelity'],
            'informed_values': certificate['preparation_best']}


def decision(frontier, cohort, signatures, scope):
    values = evaluate_frontier(frontier, signatures)
    kwargs = {'preparation_labels': list(cohort),
              'plan_labels': [word or 'I' for word, _ in frontier], 'contract': scope}
    certificate = compile_decision(values, **kwargs)
    if not check_decision(json.loads(encoded(certificate)), values, **kwargs):
        raise ValueError('decision verification failed')
    return values, certificate, quality(certificate, frontier, values)


def gate_indices(values, maximum_regret, minimum_fidelity):
    best = [max(row) for row in values]
    return [j for j in range(len(values[0]))
            if max(b - row[j] for b, row in zip(best, values)) <= maximum_regret
            and min(row[j] for row in values) >= minimum_fidelity]


def discover_library():
    ops, terminal = base_operators(), base_probes()['readout']
    features = compile_features(ops, terminal)
    checked = check_features(features, ops, terminal)
    cone, stats = discover_cone(checked, max(HORIZONS) - 1)
    check_cone(cone, checked, max(HORIZONS) - 1)
    families = {}
    for k in HORIZONS:
        frontier, certificate, measured = compile_family(
            ops, terminal, k, feature_certificate=features,
            cone_certificate=cone_prefix(cone, k))
        if check_family(json.loads(encoded(certificate)), ops, terminal, k) != frontier:
            raise ValueError('new family certificate failed')
        if measured['layers'] != construction_stats(certificate):
            raise ValueError('candidate construction accounting failed')
        families[str(k)] = {key: value for key, value in certificate.items()
                            if key not in ('features', 'cone')}
    return {'schema': 'cdka.suffix-context-library/v1', 'parent_commit': PARENT,
            'maximum_horizon': max(HORIZONS), 'features': features,
            'context_cone': cone, 'families': families,
            'discovery': {'numpy': version('numpy'), 'scipy': version('scipy'),
                          'statistics': stats,
                          'numerical_proposals_are_proofs': False}}


def build(library):
    if (library['schema'] != 'cdka.suffix-context-library/v1' or
            library['parent_commit'] != PARENT or
            library['maximum_horizon'] != max(HORIZONS) or
            set(library['families']) != set(map(str, HORIZONS))):
        raise ValueError('frozen library contract')
    ops, terminal = base_operators(), base_probes()['readout']
    features = check_features(library['features'], ops, terminal)
    check_cone(library['context_cone'], features, max(HORIZONS) - 1)
    libraries, scaling = {}, []
    retained_checks = complete_checks = frontier_checks = parent_checks = 0
    principal_value_checks = 0
    for k in HORIZONS:
        certificate = family_certificate(library, k)
        frontier = check_family(certificate, ops, terminal, k)
        reference, reference_certificate, reference_stats = compile_feature_family(
            ops, terminal, k, feature_certificate=library['features'])
        if check_feature_family(reference_certificate, ops, terminal, k) != reference:
            raise ValueError('feature reference certificate failed')
        for left, right in ((frontier, reference), (reference, frontier)):
            for _, response in left:
                if not any(dominated(other, response) for _, other in right):
                    raise ValueError('two-way exact frontier dominance failed')
                frontier_checks += 1
        for word, response in frontier:
            if response != contrast_response(word_value(ops, tuple(word), terminal)):
                raise ValueError('retained response differs from sixteen-state physics')
            retained_checks += 1
        if k <= 8:
            parent, _, parent_stats = compile_parent(ops, terminal, k)
            if parent != reference or parent_stats != reference_stats:
                raise ValueError('shared eight-feature improvement changed parent behavior')
            parent_checks += len(parent)
        full = None
        if k <= 4:
            full = unpruned_shared(ops, terminal, k)
            if {word for word, _ in full} != {''.join(word) for word in plan_words(k)}:
                raise ValueError('small exhaustive grammar mismatch')
            for word, response in full:
                if response != contrast_response(word_value(ops, tuple(word), terminal)):
                    raise ValueError('small exhaustive physical mismatch')
                if not any(dominated(other, response) for _, other in frontier):
                    raise ValueError('small exhaustive program lacks a representative')
                complete_checks += 1
        stats = construction_stats(certificate)
        libraries[k] = frontier, certificate, stats, reference, reference_stats, full

    principal = None
    for h, k in ((2, 4), (4, 4), (4, 6), (4, 8), (4, 10), (4, 12), (4, 14)):
        cohort = preparation_laws(h)
        signatures = [contrast_signature(*law) for law in cohort.values()]
        frontier, certificate, stats, reference, reference_stats, full = libraries[k]
        scope = {**contract(h, k), 'parent_commit': PARENT,
                 'physical_feature_binding': features['binding']}
        values, dc, result = decision(frontier, cohort, signatures, scope)
        _, _, reference_result = decision(reference, cohort, signatures, scope)
        if any(result[key] != reference_result[key] for key in QUALITY_FIELDS):
            raise ValueError('matched exact decision failed')
        scaling.append({'history_length': h, 'ordinary_updates': k,
                        'preparations': len(cohort), 'legal_programs': (k + 2)*2**k,
                        'context_rows': len(certificate['cone']['rows']),
                        'suffix_context_stats': stats[-1],
                        'feature_reference_stats': reference_stats[-1],
                        'generated_candidate_names_all_levels': sum(
                            item['complete_words_generated'] for item in stats),
                        'certificate_bytes': len(encoded(certificate)),
                        'maximum_certificate_rational_bits': certificate_rational_bits(certificate),
                        'maximum_response_rational_bits': rational_bits([q for _, q in frontier]),
                        'maximum_value_rational_bits': rational_bits(values),
                        'decision': result})
        if (h, k) == (2, 4):
            full_values, _, full_result = decision(full, cohort, signatures, scope)
            if any(result[key] != full_result[key] for key in QUALITY_FIELDS):
                raise ValueError('principal exhaustive decision mismatch')
            previous = json.loads((DATA / 'reachable-diagnosis-results.json').read_text())['fixture']
            positions = {word or 'I': j for j, (word, _) in enumerate(full)}
            if (previous['histories'] != list(cohort) or
                    len(previous['plans']) != len(full) or
                    set(previous['plans']) != set(positions) or
                    len(previous['values']) != len(cohort) or
                    any(len(row) != len(full) for row in previous['values'])):
                raise ValueError('inherited principal identities or matrix dimensions changed')
            for i, old_row in enumerate(previous['values']):
                for word, value in zip(previous['plans'], old_row):
                    if F(value) != full_values[i][positions[word]]:
                        raise ValueError('inherited principal values changed')
                    principal_value_checks += 1
            gates = []
            for delta, floor in ((F(1, 500), F(21, 25)), (F(3, 1000), F(21, 25)),
                                 (F(3, 1000), F(17, 20)), (F(1, 200), F(17, 20))):
                reduced = gate_indices(values, delta, floor)
                exhaustive = gate_indices(full_values, delta, floor)
                if bool(reduced) != bool(exhaustive):
                    raise ValueError('joint feasibility changed')
                gates.append({'maximum_regret': delta, 'minimum_fidelity': floor,
                              'feasible': bool(reduced),
                              'retained_witnesses': [frontier[j][0] or 'I' for j in reduced],
                              'exhaustive_feasible_count': len(exhaustive)})
            principal = {'contract': scope, 'preparations': list(cohort),
                         'signatures': signatures, 'programs': [word or 'I' for word, _ in frontier],
                         'responses': [q for _, q in frontier], 'values': values,
                         'certificate_library': LIBRARY.name,
                         'decision_certificate': dc, 'summary': result,
                         'stats_by_level': stats, 'joint_gates': gates}

    controls = {}
    frontier = libraries[4][0]
    cohort = preparation_laws(2, F(1, 2))
    signatures = [contrast_signature(*law) for law in cohort.values()]
    values = evaluate_frontier(frontier, signatures)
    if not all(value == F(1, 2) for row in values for value in row):
        raise ValueError('uninformative sensor control failed')
    controls['uninformative_sensor'] = {'fidelity': '1/2', 'regret': '0',
                                      'all_original_programs_tie': 96,
                                      'all_original_identities_preserved': False}
    for success in (F(0), F(1)):
        other_ops = base_operators(success)
        other_features = compile_features(other_ops, terminal)
        other, cert, _ = compile_family(other_ops, terminal, 4,
                                       feature_certificate=other_features, optimize=False)
        if check_family(cert, other_ops, terminal, 4) != other:
            raise ValueError('repair boundary feature control failed')
        reference, _, _ = compile_feature_family(
            other_ops, terminal, 4, feature_certificate=other_features)
        for left, right in ((other, reference), (reference, other)):
            if not all(any(dominated(r, q) for _, r in right) for _, q in left):
                raise ValueError('repair boundary frontier control failed')
        controls['repair_success_' + str(success)] = {
            'features': 8, 'retained_programs': len(other),
            'two_way_reference_dominance': True, 'discovery_uses_scipy': False}

    return exact({'schema': 'cdka.suffix-context-experiment/v1', 'parent_commit': PARENT,
                  'physical_contract_changed': False, 'active_branches': ['R11', 'R14'],
                  'feature_dimension': 8, 'certificate_library': LIBRARY.name,
                  'discovery': library['discovery'], 'fixture': principal,
                  'scaling': scaling, 'controls': controls,
                  'validation': {'checked_horizons': list(HORIZONS),
                                 'small_exhaustive_physical_and_dominance_checks': complete_checks,
                                 'retained_full16_physical_checks': retained_checks,
                                 'two_way_feature_reference_dominance_checks': frontier_checks,
                                 'parent_frontier_agreements': parent_checks,
                                 'principal_parent_value_agreements': principal_value_checks,
                                 'checker_discovers_cones_or_pareto_frontiers': False,
                                 'checker_enumerates_pruned_suffixes': False,
                                 'frozen_check_requires_scipy': False},
                  'limits': [
                      'One representative and decision feasibility, not all tied identities or prediction envelopes.',
                      'No polynomial bound on context rows, frontier size, rational bit growth or total complexity.',
                      'Every 2^h preparation history remains explicit.',
                      'Physical execution cost is outside this response order; the prepaid common box is unchanged.',
                      'Feature coordinates and context mixtures are evaluator objects, not physical states or mixed programs.',
                      'Large horizons require mandatory work and can reduce absolute fidelity.',
                      'Certificate size may rise while program count and total runtime fall.',
                  ]})


def _cold_model():
    raw_update.cache_clear()
    maintenance_row.cache_clear()
    voter_profile.cache_clear()
    return base_operators(), base_probes()['readout']


def _measure(call):
    start = perf_counter()
    result = call()
    return result, perf_counter() - start


def benchmark_worker(spec):
    """One complete cold use per fresh interpreter, including solver startup."""
    method, h, k = spec['method'], spec['h'], spec['k']
    if method not in ('feature8_all_suffixes', 'finite_context8'):
        raise ValueError('benchmark method')
    if 'scipy' in sys.modules or 'numpy' in sys.modules:
        raise ValueError('worker did not start with cold numerical dependencies')
    components = {}
    (ops, terminal), components['physical_kernel'] = _measure(_cold_model)
    cohort, components['preparation'] = _measure(lambda: preparation_laws(h))
    signatures, components['encoding'] = _measure(
        lambda: [contrast_signature(*law) for law in cohort.values()])
    feature_certificate, components['feature_construction'] = _measure(
        lambda: compile_features(ops, terminal))
    compiler = compile_feature_family if method == 'feature8_all_suffixes' else compile_family
    checker = check_feature_family if method == 'feature8_all_suffixes' else check_family
    (frontier, certificate, stats), components['family_discovery_and_compile'] = _measure(
        lambda: compiler(ops, terminal, k, feature_certificate=feature_certificate))
    payload, components['family_serialization'] = _measure(lambda: encoded(certificate))
    checked, components['family_parse_and_check'] = _measure(
        lambda: checker(json.loads(payload), ops, terminal, k))
    if checked != frontier:
        raise ValueError('cold family checker mismatch')
    values, components['query'] = _measure(lambda: evaluate_frontier(frontier, signatures))
    scope = {**contract(h, k), 'parent_commit': PARENT,
             'physical_feature_binding': feature_certificate['binding']}
    kwargs = {'preparation_labels': list(cohort),
              'plan_labels': [word or 'I' for word, _ in frontier], 'contract': scope}
    dc, components['decision_construction'] = _measure(lambda: compile_decision(values, **kwargs))
    dc_payload, components['decision_serialization'] = _measure(lambda: encoded(dc))
    valid, components['decision_parse_and_check'] = _measure(
        lambda: check_decision(json.loads(dc_payload), values, **kwargs))
    if not valid:
        raise ValueError('cold decision checker mismatch')
    cache, cache_time = _measure(lambda: encoded(frontier))
    query_keys = ('query', 'decision_construction', 'decision_serialization', 'decision_parse_and_check')
    return {'method': method, 'history_length': h, 'ordinary_updates': k,
            'components_seconds': components, 'total_seconds': sum(components.values()),
            'reused_checked_frontier_new_cohort_seconds': sum(
                components[key] for key in ('preparation', 'encoding') + query_keys),
            'reused_checked_frontier_encoded_cohort_seconds': sum(components[key] for key in query_keys),
            'numerical_dependencies_imported': 'scipy.optimize' in sys.modules,
            'family_certificate_bytes': len(payload), 'decision_certificate_bytes': len(dc_payload),
            'optional_frontier_export_seconds': cache_time, 'frontier_cache_bytes': len(cache),
            'maximum_certificate_rational_bits': certificate_rational_bits(certificate),
            'maximum_response_rational_bits': rational_bits([q for _, q in frontier]),
            'maximum_value_rational_bits': rational_bits(values),
            'stats': stats, 'quality': quality(dc, frontier, values)}


def benchmark():
    output = {'schema': 'cdka.suffix-context-benchmark/v1', 'parent_commit': PARENT,
              'environment': {'python': platform.python_version(), 'platform': platform.platform(),
                              'numpy': version('numpy'), 'scipy': version('scipy')},
              'repeats': 3,
              'convention': 'Each observation is one complete use in a fresh Python process. '
              'Both methods pay cold physical kernels, preparation, encoding, shared exact8 feature '
              'construction, compilation, family JSON serialization/parsing/checking, queries and '
              'compact decision construction/serialization/parsing/checking. Only finite_context8 '
              'imports NumPy/SciPy, inside its timed compiler: cold imports, first solver initialization, '
              'all numerical cone proposals and exact rational support recovery are included. '
              'Methods alternate order within each of three repetitions. Report both the sum of '
              'component medians and the median of complete-use totals. Interpreter startup, common '
              'standard-library/project-module imports, process transport and optional frontier export '
              'are outside both totals. No precomputed cones enter either timed pipeline.',
              'outputs': ['informed values', 'one minimax program', 'one maximin program'],
              'reuse_estimate_convention': 'The reused_checked_frontier fields are component-based '
              'estimates formed from first-use observations, not separately executed reuse trials. '
              'They assume the verified frontier and physical model remain available and valid.',
              'cases': []}
    for h, k in ((2, 4), (4, 8), (4, 12), (4, 14)):
        samples = {name: [] for name in ('feature8_all_suffixes', 'finite_context8')}
        for repeat in range(3):
            names = list(samples)
            if repeat % 2:
                names.reverse()
            for name in names:
                spec = {'method': name, 'h': h, 'k': k}
                result = subprocess.run(
                    [sys.executable, '-m', 'experiments.suffix_context_sweep',
                     '--worker', json.dumps(spec)], cwd=ROOT, check=True,
                    text=True, capture_output=True)
                sample = json.loads(result.stdout)
                samples[name].append(sample)
                print(json.dumps({'sample': repeat + 1, 'h': h, 'k': k, 'method': name,
                                  'total_seconds': sample['total_seconds']}), flush=True)
        methods = []
        for name, observations in samples.items():
            first = observations[0]
            deterministic = ('quality', 'stats', 'family_certificate_bytes',
                             'decision_certificate_bytes', 'frontier_cache_bytes',
                             'maximum_certificate_rational_bits', 'maximum_response_rational_bits',
                             'maximum_value_rational_bits', 'numerical_dependencies_imported')
            if any(any(sample[key] != first[key] for key in deterministic) for sample in observations):
                raise ValueError('cold runs disagreed on deterministic outputs')
            medians = {key: median(sample['components_seconds'][key] for sample in observations)
                       for key in first['components_seconds']}
            methods.append({'method': name, **{key: first[key] for key in deterministic},
                            'components_median_seconds': medians,
                            'sum_component_medians_seconds': sum(medians.values()),
                            'median_complete_use_seconds': median(sample['total_seconds'] for sample in observations),
                            'minimum_complete_use_seconds': min(sample['total_seconds'] for sample in observations),
                            'maximum_complete_use_seconds': max(sample['total_seconds'] for sample in observations),
                            'reused_checked_frontier_new_cohort_median_seconds': median(
                                sample['reused_checked_frontier_new_cohort_seconds'] for sample in observations),
                            'reused_checked_frontier_encoded_cohort_median_seconds': median(
                                sample['reused_checked_frontier_encoded_cohort_seconds'] for sample in observations),
                            'raw_samples': observations})
        baseline, candidate = methods
        if any(baseline['quality'][key] != candidate['quality'][key] for key in QUALITY_FIELDS):
            raise ValueError('cold benchmark outputs disagree')
        case = {'history_length': h, 'ordinary_updates': k, 'preparations': 2**h,
                'legal_programs': (k + 2)*2**k, 'methods': methods,
                'total_speedup': baseline['sum_component_medians_seconds'] / candidate['sum_component_medians_seconds'],
                'complete_use_median_speedup': baseline['median_complete_use_seconds'] / candidate['median_complete_use_seconds']}
        output['cases'].append(case)
        print(json.dumps({'completed_h': h, 'k': k, 'speedup': case['total_speedup']}), flush=True)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--benchmark', action='store_true')
    parser.add_argument('--worker')
    args = parser.parse_args()
    if args.worker is not None:
        print(json.dumps(benchmark_worker(json.loads(args.worker))))
    else:
        if args.write:
            library = discover_library()
            LIBRARY.write_bytes(encoded(library) + b'\n')
            result = build(library)
            RESULT.write_text(json.dumps(result, indent=2) + '\n')
        if args.check or not (args.write or args.benchmark):
            library = json.loads(LIBRARY.read_text())
            result = build(library)
            if json.loads(RESULT.read_text()) != result:
                raise ValueError('stale suffix-context evidence')
        if args.write or args.check:
            print(json.dumps({'validation': result['validation'],
                              'principal': result['fixture']['summary']}, indent=2))
        if args.benchmark:
            BENCHMARK.write_text(json.dumps(benchmark(), indent=2) + '\n')
