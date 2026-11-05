"""Exact structural and negative controls for finite suffix-context pruning.

Run with only the standard library, including with Python assertions disabled:

    python -S -O -m experiments.suffix_context_controls

This is deterministic evidence, not a benchmark. It verifies a physical
E-order reversal through M, the finite identities behind the all-horizon
lineality obstruction, exact degraded-response class counts, and rejection
of the earlier empty-cone attack. No LP, Pareto discovery for checking, or
enumeration of long complete-program libraries is required.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from cdka.boundary_voting import BITS
from cdka.maintenance_access import base_operators, base_probes
from cdka.program_families import dominated, transports
from cdka.reachable_diagnosis import acquisition, advance_updates, evaluate
from cdka.reachable_restriction import CONTRAST_BASIS, contrast_response, contrast_signature
from cdka.semantic_closure import ExactBasis, dot, push, word_value
from cdka.suffix_contexts import check_family, compile_family


PARENT = 'ce252821be4fb5a5075ad12f71ee2da7f14acb7d'
BETA = F(-97789249826403799024011653198517846528,
         736008414410103325506140176870361328125)
EXPECTED_BAD_CLASSES = (1, 2, 4, 7, 12, 19, 30, 45, 67, 97, 139, 195, 272)


def require(condition, message):
    """Control failures remain active with python -O."""
    if not condition:
        raise ValueError(message)


def exact(value):
    if type(value) is F:
        return str(value)
    if type(value) is dict:
        return {str(key): exact(item) for key, item in value.items()}
    if type(value) in (tuple, list):
        return [exact(item) for item in value]
    return value


def order_reversal(operators, terminal):
    p, q = 'RDDRRD', 'RDRDDR'
    physical_p = word_value(operators, p, terminal)
    physical_q = word_value(operators, q, terminal)
    difference = tuple(a-b for a, b in zip(physical_p, physical_q))
    e_delta = contrast_response(difference)
    boundary = tuple(push(row, operators['M']) for row in CONTRAST_BASIS)
    b_delta = tuple(dot(row, difference) for row in boundary)
    require(e_delta[0] < 0 and e_delta[1] < 0 and e_delta[2:] == (F(0), F(0)),
            'ordinary E-dominance witness changed')
    require(b_delta[0] < 0 and b_delta[1] < 0 and b_delta[2] > 0 and b_delta[3] > 0,
            'maintenance boundary must reverse two coordinates')

    history = 'D'*32
    law = advance_updates(acquisition(F(1, 10), F(0)), history)
    signature = contrast_signature(*law)
    require(all(coordinate <= 0 for coordinate in signature[1]),
            'physical preparation left the inherited contrast cone')
    values = {word: evaluate(law, word) for word in (p, q, 'M'+p, 'M'+q)}
    plain = values[p]-values[q]
    repaired = values['M'+p]-values['M'+q]
    require(plain == dot(signature[1], e_delta) and plain > 0,
            'physical ordinary advantage must be positive')
    require(repaired == dot(signature[1], b_delta) and repaired < 0,
            'physical prefixed-M advantage must be negative')
    return {
        'dominant_without_M': p, 'dominated_without_M': q,
        'preparation': history,
        'sensor_error': F(1, 10), 'initial_bad_probability': F(0),
        'repair_success': F(4, 5),
        'E_difference': e_delta, 'EM_difference': b_delta,
        'physical_values': values,
        'plain_advantage': plain, 'maintenance_prefixed_advantage': repaired,
        'scope': 'Counterexample to E-order preservation through M; '
                 'not a global-optimizer failure or shortest-history theorem.',
    }


def lineality_witness(operators, terminal):
    A = transports(operators)
    boundary = tuple(push(row, operators['M']) for row in CONTRAST_BASIS)
    a = A['R'][0][0]+A['R'][1][1]
    b = A['R'][2][2]+A['R'][3][3]
    h, lam = F(19, 20), F(24, 25)
    require(0 < b < a < h < lam < 1, 'strict spectral ordering')
    v = push(boundary[2], operators['R'])
    v = tuple(x-a*y for x, y in zip(push(v, operators['R']), v))
    v = tuple(x-b*y for x, y in zip(push(v, operators['R']), v))
    v = tuple(x/(h*(h-a)*(h-b)) for x in v)
    require(push(v, operators['R']) == tuple(h*x for x in v),
            'exact R spectral projection identity')
    # Together with the polynomial construction, this is the square-free
    # cyclic annihilator B2 R(R-aI)(R-bI)(R-hI)=0. Hence B2 R^m/h^m -> v.

    w = (F(0),)*8 + tuple(F(sum((-1)**bit for bit in bits), 8) for bits in BITS)
    require(push(w, operators['D']) == tuple(lam*x for x in w),
            'exact dominant D eigenrow')
    first_moments = []
    for row, expected in ((boundary[0], F(2)), (v, BETA)):
        require(sum(row, F(0)) == 0, 'D-limit row must have total mass zero')
        moments = tuple(sum((row[z*8+i]*((-1)**bits[j])
                             for z in (0, 1) for i, bits in enumerate(BITS)), F(0))
                        for j in range(3))
        require(moments == (expected,)*3, 'equal symmetric first Walsh moments')
        first_moments.append(moments)
    require(BETA < 0, 'negative D-limit coefficient')

    # These sixteen full physical identities imply the formula for every
    # signed row and every m. No numerical large-m limit is used as evidence.
    walsh_identities = 0
    for mask in product((0, 1), repeat=3):
        subset = tuple(i for i, used in enumerate(mask) if used)
        row = tuple(F((-1)**sum(bits[j] for j in subset), 8) for bits in BITS)
        scale = lam**len(subset)
        healthy = row+(F(0),)*8
        degraded = (F(0),)*8+row
        require(push(healthy, operators['D']) ==
                tuple(scale*h*x for x in row)+tuple(scale*(1-h)*x for x in row),
                'healthy Walsh D block identity')
        require(push(degraded, operators['D']) ==
                (F(0),)*8+tuple(scale*x for x in row),
                'degraded Walsh D block identity')
        walsh_identities += 2

    line = ExactBasis(16)
    require(line.add(w) and line.add(push(w, operators['R'])),
            'lineality witness must have rank two')
    coordinates = tuple(line.coordinates(row) for row in CONTRAST_BASIS[2:])
    expected_coordinates = (
        (F(-49, 288), F(3814697265625, 2147235028992)),
        (F(817, 288), F(-3814697265625, 2147235028992)),
    )
    require(coordinates == expected_coordinates, 'degraded E rows in lineality span')
    return {
        'ordinary_R_roots': (F(0), b, a, h),
        'D_degree_one_eigenvalue': lam,
        'R_limit_row': v, 'D_limit_row': w,
        'B0_total_degree_one_moments': first_moments[0],
        'R_limit_total_degree_one_moments': first_moments[1],
        'negative_projection_coefficient': BETA,
        'D_health_Walsh_block_identities_checked': walsh_identities,
        'E_bad_coordinates_in_w_wR': coordinates,
        'scope': 'Any closed D/R-invariant row cone containing E M contains '
                 'both signs of both degraded E rows; its dominance requires '
                 'equality of the degraded response pair.',
    }


def degraded_response_classes(operators, terminal):
    A = transports(operators)
    require(all(not any(A[letter][i][:2]) for letter in ('D', 'R') for i in (2, 3)),
            'degraded two-coordinate response must be closed')
    matrices = {letter: tuple(tuple(row[2:]) for row in A[letter][2:])
                for letter in ('D', 'R')}
    pairs = {contrast_response(terminal)[2:]}
    records = []
    for k, expected in enumerate(EXPECTED_BAD_CLASSES):
        if k:
            pairs = {tuple(dot(row, pair) for row in matrices[letter])
                     for pair in pairs for letter in ('D', 'R')}
        require(len(pairs) == expected, 'exact degraded-response class count')
        records.append({'K': k, 'ordinary_words': 2**k,
                        'distinct_degraded_response_pairs': len(pairs)})
    return {
        'records': records,
        'method': 'Exact set recurrence on the closed degraded response pair; '
                  'equal pairs are deduplicated before extending them.',
        'scope': 'Finite lower bounds for a universal-context cover; '
                 'no asymptotic lower-bound claim.',
    }


def empty_cone_regression(operators, terminal):
    frontier, certificate, _ = compile_family(operators, terminal, 1, optimize=False)
    certificate = json.loads(json.dumps(certificate))
    require(check_family(certificate, operators, terminal, 1) == frontier,
            'legitimate portable K1 certificate')
    attacks = {}
    empty = deepcopy(certificate)
    empty['cone'] = {'rows': [], 'counts': [0], 'initial': [], 'transitions': []}
    truncated = deepcopy(certificate)
    truncated['cone']['initial'].pop()
    for label, payload in (('empty_cone', empty), ('truncated_initial_witnesses', truncated)):
        try:
            check_family(payload, operators, terminal, 1)
        except ValueError as error:
            attacks[label] = {'rejected': True, 'reason': str(error)}
        else:
            raise ValueError('malformed context certificate accepted: '+label)

    unsafe_words = ('D', 'R', 'DM', 'RM')
    omitted = contrast_response(word_value(operators, 'MR', terminal))
    unsafe = {word: contrast_response(word_value(operators, word, terminal))
              for word in unsafe_words}
    require(not any(dominated(response, omitted) for response in unsafe.values()),
            'earlier empty-cone output must fail to cover MR')
    return {
        'checked_safe_frontier': [word for word, _ in frontier],
        'rejected_payloads': attacks,
        'earlier_unsafe_frontier': unsafe_words,
        'uncovered_legal_word': 'MR',
        'unsafe_frontier_responses': unsafe,
        'uncovered_response': omitted,
        'scope': 'An empty witness list must not erase required identities; '
                 'local equalities alone do not certify grammar coverage.',
    }


def run():
    operators, terminal = base_operators(), base_probes()['readout']
    return exact({
        'schema': 'cdka.suffix-context-structural-controls/v1',
        'parent_commit': PARENT,
        'order_reversal': order_reversal(operators, terminal),
        'lineality': lineality_witness(operators, terminal),
        'degraded_response_classes': degraded_response_classes(operators, terminal),
        'empty_cone_regression': empty_cone_regression(operators, terminal),
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='write exact JSON evidence to this path')
    arguments = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True)+'\n'
    if arguments.output is not None:
        arguments.output.write_text(payload)
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
