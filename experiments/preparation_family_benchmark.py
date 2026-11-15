"""Fresh-process, matched-output preparation coverage benchmark.

python -m experiments.preparation_family_benchmark

Each observation constructs the physical model and both relevant program and
preparation machinery from scratch, encodes the complete certificate, parses
and independently checks it, and answers the same informed query/joint gates.
Both methods receive the verified two-amplitude/trailing-D arithmetic codec.
The reference streams histories in depth-first order and never exports their
full value table or informed profile. Optional imports and first solver use
are inside compilation. No frozen discovery result enters either worker.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
from statistics import median
import subprocess
import sys
from time import perf_counter

from cdka.boundary_voting import raw_update, voter_profile
from cdka.maintenance_access import base_operators, base_probes, maintenance_row
from cdka.preparation_decisions import query_informed
from cdka.preparation_pipeline import compile_task, check_task, OUTPUT_CONTRACT
from cdka.reachable_diagnosis import acquisition, contract
from experiments.preparation_family_sweep import (
    PARENT, encoded, exact, quality, semantic_decision, certificate_rational_bits,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/data/preparation-family-benchmark.json'
CASES = ((2, 4), (8, 4), (12, 4), (16, 4), (12, 12))
METHODS = ('stream', 'convex_cover')


def timed(call):
    start = perf_counter()
    value = call()
    return value, perf_counter()-start


def cold_model():
    raw_update.cache_clear(); voter_profile.cache_clear(); maintenance_row.cache_clear()
    return base_operators(), base_probes()['readout'], acquisition()


def worker(spec):
    method, h, k = spec['method'], spec['h'], spec['k']
    if method not in METHODS:
        raise ValueError('preparation benchmark method')
    if 'numpy' in sys.modules or 'scipy' in sys.modules:
        raise ValueError('numerical discovery dependencies were not cold')
    pm = 'feature8' if k == 4 else 'finite_context8'
    scope = {**contract(h, k), 'parent_commit': PARENT}
    components = {}
    start = perf_counter()
    (ops, g, law), components['physical_kernel_and_acquisition'] = timed(cold_model)
    (certificate, stats), components['all_discovery_encoding_and_decision_compile'] = timed(
        lambda: compile_task(ops, g, law, h, k, program_method=pm,
                             preparation_method=method, contract=scope))
    payload, components['complete_certificate_serialization'] = timed(lambda: encoded(certificate))
    checked, components['parse_and_independent_complete_check'] = timed(
        lambda: check_task(json.loads(payload), ops, g, law, h, k, contract=scope))
    answer, components['informed_query_and_joint_gates'] = timed(
        lambda: {'quality': quality(certificate),
                 'informed_query': exact(query_informed(checked['problem'], 'D'*h)),
                 'per_program_extrema_sha256': sha256(encoded(semantic_decision(certificate))).hexdigest()})
    answer_payload, components['compact_answer_serialization'] = timed(lambda: encoded(answer))
    complete_seconds = perf_counter()-start
    # Audit measurements below are outside the paid task and identical in scope.
    return {'method': method, 'history_length': h, 'ordinary_updates': k,
            'program_method': pm, 'components_seconds': components,
            'complete_use_seconds': complete_seconds,
            'component_sum_seconds': sum(components.values()),
            'complete_certificate_bytes': len(payload),
            'preparation_certificate_bytes': (len(encoded(certificate['preparation_certificate']))
                                              if certificate['preparation_certificate'] is not None else 0),
            'decision_certificate_bytes': len(encoded(certificate['decision'])),
            'compact_answer_bytes': len(answer_payload),
            'maximum_certificate_rational_bits': certificate_rational_bits(certificate),
            'numerical_dependencies_imported': 'scipy.optimize' in sys.modules,
            'query_coordinates': 2 if checked['problem']['codec'] is not None else 4,
            'stats': stats, 'answer': answer}


def benchmark():
    environment = {**os.environ, 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
                   'MKL_NUM_THREADS': '1'}
    output = {'schema': 'cdka.preparation-family-benchmark/v1', 'parent_commit': PARENT,
              'environment': {'python': platform.python_version(), 'platform': platform.platform(),
                              'numpy': version('numpy'), 'scipy': version('scipy'),
                              'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'},
              'repeats': 3, 'output_contract': OUTPUT_CONTRACT,
              'convention': 'Each observation is one complete first use in a fresh process. '
              'Both pay physical kernels/acquisition, the same program-cover compiler for that K, '
              'preparation encoding or hull discovery, the shared exact two-amplitude/trailing-D codec, '
              'compact decisions, full JSON serialization/parsing, independent program/preparation/decision '
              'checking, one informed query at D^h, three same-program threshold pairs '
              '(six gate scans: feasibility and feasible identities separately) and answer serialization. '
              'All needed NumPy/SciPy imports and first HiGHS initialization occur inside the timed compiler. '
              'No previously discovered cover enters either method. Stream uses a depth-first stack and one '
              'value row; it is checked by a second full stream, with no full output table or informed list. '
              'Worker interpreter startup, common stdlib/project imports, transport and post-task audit '
              'measurements are outside both totals. Complete-use wall time includes instrumentation gaps; '
              'sum of component medians is reported separately. Methods alternate order by repetition. '
              'No reuse trial, resident-memory benefit or universal crossover is inferred.',
              'cases': []}
    deterministic = ('program_method', 'complete_certificate_bytes', 'preparation_certificate_bytes',
                     'decision_certificate_bytes', 'compact_answer_bytes',
                     'maximum_certificate_rational_bits', 'numerical_dependencies_imported',
                     'query_coordinates', 'stats', 'answer')
    for h, k in CASES:
        observations = {name: [] for name in METHODS}
        for repeat in range(3):
            order = METHODS if repeat % 2 == 0 else tuple(reversed(METHODS))
            for method in order:
                spec = {'method': method, 'h': h, 'k': k}
                process = subprocess.run(
                    [sys.executable, '-m', 'experiments.preparation_family_benchmark',
                     '--worker', json.dumps(spec)], cwd=ROOT, env=environment,
                    capture_output=True, text=True)
                if process.returncode:
                    raise RuntimeError(process.stderr)
                sample = json.loads(process.stdout)
                observations[method].append(sample)
                print(json.dumps({'sample': repeat+1, 'h': h, 'k': k, 'method': method,
                                  'seconds': sample['complete_use_seconds']}), flush=True)
        methods = []
        for method in METHODS:
            samples = observations[method]
            first = samples[0]
            if any(any(sample[key] != first[key] for key in deterministic) for sample in samples):
                raise ValueError('fresh runs disagree on exact output or discovery structure')
            medians = {key: median(sample['components_seconds'][key] for sample in samples)
                       for key in first['components_seconds']}
            methods.append({'method': method, **{key: first[key] for key in deterministic},
                            'components_median_seconds': medians,
                            'sum_component_medians_seconds': sum(medians.values()),
                            'median_complete_use_seconds': median(s['complete_use_seconds'] for s in samples),
                            'minimum_complete_use_seconds': min(s['complete_use_seconds'] for s in samples),
                            'maximum_complete_use_seconds': max(s['complete_use_seconds'] for s in samples),
                            'raw_samples': samples})
        baseline, candidate = methods
        if baseline['answer'] != candidate['answer']:
            raise ValueError('candidate changed exact per-program bounds, decision, gates or query')
        case = {'history_length': h, 'ordinary_updates': k, 'original_histories': 2**h,
                'legal_programs': (k+2)*2**k, 'methods': methods,
                'complete_use_median_speedup': baseline['median_complete_use_seconds']/candidate['median_complete_use_seconds'],
                'component_median_sum_speedup': baseline['sum_component_medians_seconds']/candidate['sum_component_medians_seconds']}
        output['cases'].append(case)
        OUTPUT.write_text(json.dumps(output, indent=2)+'\n')
        print(json.dumps({'completed_h': h, 'k': k,
                          'median_speedup': case['complete_use_median_speedup']}), flush=True)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker')
    args = parser.parse_args()
    if args.worker is not None:
        print(json.dumps(worker(json.loads(args.worker))))
    else:
        OUTPUT.write_text(json.dumps(benchmark(), indent=2)+'\n')
