"""Two-sided exact coverage with compact common-program decisions.

python -m experiments.preparation_family_sweep --write --check
python -S -O -m experiments.preparation_family_sweep --check

Discovery alone uses optional numerical geometry. Frozen checking reconstructs
physical D/R children, convex identities and program covers with exact rational
arithmetic. The h=16 full streamed comparison is in the separately recorded
cold benchmark; this repeatable check streams through h=12 and checks the h=16
cover and all extrema with independently propagated actual-history attainers.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from importlib.metadata import version
import json
from pathlib import Path

from cdka.maintenance_access import base_operators, base_probes
from cdka.preparation_decisions import joint_gate, query_informed
from cdka.preparation_families import (
    compile_family, check_family, make_preparation_model, preparation_binding,
)
from cdka.preparation_pipeline import compile_task, check_task, OUTPUT_CONTRACT
from cdka.reachable_diagnosis import (
    acquisition, advance_updates, contract, evaluate, joint_oracle, plan_words,
    preparation_laws,
)
from cdka.reachable_restriction import contrast_signature, contrast_response
from cdka.semantic_closure import dot, word_value
from cdka.suffix_features import compile_feature_family
from experiments.suffix_context_sweep import (
    encoded, exact, certificate_rational_bits, rational_bits,
    family_certificate as context_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/data'
LIBRARY = DATA / 'preparation-family-certificates.json'
RESULT = DATA / 'preparation-family-results.json'
PARENT = '2f9abfd01b5298de1a1889cc7c57776fa0f86572'
HORIZONS = (0, 1, 2, 4, 8, 12, 16)
DECISION_FIELDS = ('plans', 'worst_regrets', 'minimum_fidelities', 'minimax_plan',
                   'minimax_regret', 'maximin_plan', 'maximin_fidelity')
GATES = ((F(3, 1000), F(17, 20)), (F(3, 1000), F(21, 25)),
         (F(1, 200), F(17, 20)))


def prefix(certificate, model, h):
    """Preparation levels do not depend on the final horizon or continuation."""
    if not 0 <= h <= certificate['history_length']:
        raise ValueError('stored preparation family does not cover requested horizon')
    return {**certificate, 'history_length': h, 'binding': preparation_binding(model, h),
            'layers': certificate['layers'][:h+1]}


def quality(certificate):
    d = certificate['decision'] if 'decision' in certificate else certificate
    p, q = d['minimax_plan'], d['maximin_plan']
    return {'minimax_plan': d['plans'][p], 'minimax_regret': d['minimax_regret'],
            'minimax_minimum_fidelity': d['minimum_fidelities'][p],
            'maximin_plan': d['plans'][q], 'maximin_fidelity': d['maximin_fidelity'],
            'joint_gates': [{'maximum_regret': str(delta), 'minimum_fidelity': str(floor),
                             'feasible': bool(joint_gate(d, delta, floor)),
                             'retained_feasible_plans': [d['plans'][i] for i in joint_gate(d, delta, floor)]}
                            for delta, floor in GATES]}


def semantic_decision(certificate):
    d = certificate['decision'] if 'decision' in certificate else certificate
    return {key: d[key] for key in DECISION_FIELDS}


def discover_library():
    ops, law = base_operators(), acquisition()
    frontier, certificate, stats = compile_family(ops, law, max(HORIZONS))
    if check_family(json.loads(encoded(certificate)), ops, law, max(HORIZONS)) != frontier:
        raise ValueError('new preparation certificate failed exact replay')
    return {'schema': 'cdka.preparation-cover-library/v1', 'parent_commit': PARENT,
            'maximum_history_length': max(HORIZONS), 'certificate': certificate,
            'discovery': {'numpy': version('numpy'), 'scipy': version('scipy'),
                          'statistics': stats, 'numerical_proposals_are_proofs': False}}


def build(library):
    if (library['schema'] != 'cdka.preparation-cover-library/v1' or
            library['parent_commit'] != PARENT or
            library['maximum_history_length'] != max(HORIZONS)):
        raise ValueError('preparation library contract')
    ops, g, law = base_operators(), base_probes()['readout'], acquisition()
    model = make_preparation_model(ops, law)
    _, program4, _ = compile_feature_family(ops, g, 4)
    prior = json.loads((DATA / 'suffix-context-certificates.json').read_text())
    program12 = context_certificate(prior, 12)
    scaling = []
    physical_signature_checks = stream_value_checks = query_checks = 0
    principal = None
    for h, k in [(h, 4) for h in HORIZONS] + [(12, 12)]:
        method = 'feature8' if k == 4 else 'finite_context8'
        pc = program4 if k == 4 else program12
        hc = prefix(library['certificate'], model, h)
        scope = {**contract(h, k), 'parent_commit': PARENT}
        composite, stats = compile_task(ops, g, law, h, k, program_method=method,
                                        contract=scope, program_certificate=pc,
                                        preparation_certificate=hc)
        payload = encoded(composite)
        checked = check_task(json.loads(payload), ops, g, law, h, k, contract=scope)
        reps, frontier, decision = checked['preparations'], checked['frontier'], checked['decision']
        if h <= 12:
            reference, reference_stats = compile_task(
                ops, g, law, h, k, program_method=method, preparation_method='stream',
                contract=scope, program_certificate=pc)
            check_task(json.loads(encoded(reference)), ops, g, law, h, k, contract=scope)
            if semantic_decision(reference) != semantic_decision(decision):
                raise ValueError('convex cover changed a per-program extremum')
            stream_value_checks += reference_stats['decision']['values_evaluated']

        # Independent full16 propagation for every small retained signature,
        # and all extrema plus endpoint/interior representatives at large h.
        names = ({word for word, _ in reps} if h <= 8 else
                 {reps[0][0], reps[len(reps)//2][0], reps[-1][0]} |
                 set(decision['fidelity_attainers']) |
                 {w['history'] for w in decision['regret_attainers']})
        by_name = dict(reps)
        for word in sorted(names):
            offset, signed = contrast_signature(*advance_updates(law, word))
            actual = tuple(-x for x in signed)
            if offset != F(1, 2) or word in by_name and actual != by_name[word]:
                raise ValueError('physical preparation signature mismatch')
            for j in {decision['minimax_plan'], decision['maximin_plan']}:
                p, response = frontier[j]
                if offset-dot(actual, response) != evaluate(advance_updates(law, word), p):
                    raise ValueError('physical selected-program value mismatch')
            physical_signature_checks += 1

        query_names = {'D'*h, 'R'*h, ('DR'*((h+1)//2))[:h]}
        retained_names = {word for word, _ in reps}
        for index in range(2**h):
            word = ''.join('R' if index >> bit & 1 else 'D' for bit in range(h-1, -1, -1))
            if word not in retained_names:
                query_names.add(word)
                break
        queries = []
        for word in sorted(query_names):
            query = query_informed(checked['problem'], word)
            full_law = advance_updates(law, word)
            full_words = plan_words(k) if k <= 4 else [p for p, _ in frontier]
            if query['best_value'] != max(evaluate(full_law, p) for p in full_words):
                raise ValueError('informed query interpolated rather than evaluated its envelope')
            queries.append(exact(query))
            query_checks += 1

        layers = library['discovery']['statistics'][:h+1]
        # Structural work is independently recoverable from the cover itself.
        previous = 1
        for depth, layer in enumerate(hc['layers']):
            candidates = 1 if depth == 0 else 2*previous
            row = layers[depth]
            if (len(layer['cover']) != candidates or row['history_candidates'] != candidates or
                    row['retained'] != len(layer['keep']) or
                    row['histories_never_generated'] != 2**depth-candidates):
                raise ValueError('false preparation construction accounting')
            previous = len(layer['keep'])
        row = {'history_length': h, 'ordinary_updates': k, 'program_method': method,
               'original_histories': 2**h, 'legal_programs': (k+2)*2**k,
               'retained_preparations': len(reps), 'retained_programs': len(frontier),
               'final_history_candidates': layers[-1]['history_candidates'],
               'histories_never_generated_at_final_level': layers[-1]['histories_never_generated'],
               'all_levels_history_candidates': sum(x['history_candidates'] for x in layers),
               'values_evaluated': stats['decision']['values_evaluated'],
               'full_stream_reference_checked_here': h <= 12,
               'preparation_certificate_bytes': len(encoded(hc)),
               'composite_certificate_bytes': len(payload),
               'decision_certificate_bytes': len(encoded(decision)),
               'maximum_preparation_certificate_rational_bits': certificate_rational_bits(hc),
               'maximum_signature_rational_bits': rational_bits([x for _, x in reps]),
               'quality': quality(decision), 'decision': decision, 'informed_queries': queries}
        scaling.append(row)
        if (h, k) == (2, 4):
            principal = row

    # Independent joint32 trace oracle against all inherited 4x96 values.
    principal_checks = 0
    for history, initial in preparation_laws(2).items():
        offset, signed = contrast_signature(*initial)
        for p in plan_words(4):
            response = contrast_response(word_value(ops, p, g))
            value = offset + dot(signed, response)
            if value != joint_oracle(history, p):
                raise ValueError('inherited joint32 physical oracle mismatch')
            principal_checks += 1
    if (principal['quality']['minimax_plan'] != 'DRDDM' or
            principal['quality']['maximin_plan'] != 'DDDDM' or
            [q['feasible'] for q in principal['quality']['joint_gates']] != [False, True, True]):
        raise ValueError('principal physical decision changed')

    controls = []
    for eta, bad in ((F(1, 2), F(0)), (F(1, 10), F(1))):
        alternate_law = acquisition(eta, bad)
        for success in (F(0), F(1)):
            alternate_ops = base_operators(success)
            # Conservative frozen-check path; duplicate/interval covers are exact.
            candidate, _ = compile_task(alternate_ops, g, alternate_law, 4, 2, optimize=False)
            check_task(candidate, alternate_ops, g, alternate_law, 4, 2)
            reference, _ = compile_task(alternate_ops, g, alternate_law, 4, 2,
                                        preparation_method='stream')
            check_task(reference, alternate_ops, g, alternate_law, 4, 2)
            if semantic_decision(candidate) != semantic_decision(reference):
                raise ValueError('degenerate sensor/health/repair control disagreement')
            if eta == F(1, 2) and (F(candidate['decision']['minimax_regret']) != 0 or
                                   F(candidate['decision']['maximin_fidelity']) != F(1, 2)):
                raise ValueError('uninformative sensor produced source knowledge')
            controls.append({'sensor_error': str(eta), 'initial_bad': str(bad),
                             'repair_success': str(success), 'quality': quality(candidate)})

    return exact({'schema': 'cdka.preparation-family-results/v1', 'parent_commit': PARENT,
                  'output_contract': OUTPUT_CONTRACT, 'discovery': library['discovery'],
                  'preparation_certificate_library': LIBRARY.name, 'scaling': scaling,
                  'principal': principal['quality'], 'controls': controls,
                  'validation': {'checked_history_lengths': list(HORIZONS),
                                 'stream_reference_values_through_h12': stream_value_checks,
                                 'inherited_joint32_oracle_values': principal_checks,
                                 'independent_full16_preparation_checks': physical_signature_checks,
                                 'independent_informed_queries': query_checks,
                                 'all_per_program_extrema_preserved_through_h12': True,
                                 'h16_full_stream_comparison': 'separate fresh-process benchmark',
                                 'frozen_check_requires_scipy': False,
                                 'checker_discovers_geometry': False},
                  'limits': ['No polynomial bound on hull size, exact bit length or total time.',
                             'Contrast signatures, not full preparation laws, are convexly covered.',
                             'One common executable program; no access to the hidden history label.',
                             'Compact extrema and queries; all 2^h informed values are not an output.',
                             'No claim to preserve all tied programs or physical execution-cost Pareto sets.',
                             'Offline decision acceleration does not improve physical source fidelity.']})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.write:
        LIBRARY.write_bytes(encoded(discover_library())+b'\n')
    library = json.loads(LIBRARY.read_text())
    result = build(library)
    if args.write:
        RESULT.write_text(json.dumps(result, indent=2)+'\n')
    if args.check or not args.write:
        if result != json.loads(RESULT.read_text()):
            raise ValueError('stale preparation-family exact evidence')
    print(json.dumps({'validation': result['validation'], 'principal': result['principal']}, indent=2))
