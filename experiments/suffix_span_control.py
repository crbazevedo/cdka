"""Rejected exploratory control: full16 suffix cover with a uniform span ledger.

Run the short exact checks by default, or reproduce the exploratory sweep with
--sweep. Historical observations are preserved in docs/data/suffix-span-control.json;
this script never overwrites them. Its timing is not the central PF8 benchmark.
"""
from argparse import ArgumentParser
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cdka.maintenance_access import base_operators, base_probes
from cdka.program_families import (
    _candidates, _check_cover, _cover, _rational, binding, compile_family,
    evaluate_frontier, transports,
)
from cdka.reachable_diagnosis import plan_words, preparation_laws
from cdka.reachable_restriction import contrast_response, contrast_signature
from cdka.semantic_closure import apply, word_value


SCHEMA = 'cdka.exploratory-suffix-span/v1'


def span_difference(a, b):
    if len(a) != len(b) or not a:
        raise ValueError('nonempty equal vector dimensions required')
    differences = [x-y for x, y in zip(a, b)]
    return max(differences)-min(differences)


def _contract(operators, terminal, k, epsilon):
    if type(k) is not int or k < 0:
        raise ValueError('ordinary updates')
    epsilon = _rational(epsilon)
    if epsilon < 0:
        raise ValueError('nonnegative epsilon required')
    if type(operators) is not dict or set(operators) != {'D', 'R', 'M'}:
        raise ValueError('D/R/M physical operators required')
    checked = {}
    for label, rows in operators.items():
        if type(rows) not in (tuple, list) or len(rows) != 16:
            raise ValueError('sixteen physical rows required')
        result = []
        for row in rows:
            if type(row) is not dict or any(type(j) is not int or not 0 <= j < 16 for j in row):
                raise ValueError('physical row indices')
            parsed = {j: _rational(value) for j, value in row.items()}
            if any(value < 0 for value in parsed.values()) or sum(parsed.values(), F(0)) != 1:
                raise ValueError('span contraction requires stochastic rows')
            result.append({j: value for j, value in parsed.items() if value})
        checked[label] = tuple(result)
    if type(terminal) not in (tuple, list) or len(terminal) != 16:
        raise ValueError('sixteen-coordinate terminal required')
    return checked, tuple(map(_rational, terminal)), epsilon


def _binding(operators, terminal, k, epsilon):
    payload = {'schema': SCHEMA, 'physical_program_binding': binding(operators, terminal, k),
               'epsilon': str(epsilon), 'local_budget': 'epsilon/k for each ordinary level',
               'value_domain': 'fair source; negative contrast cone; one terminal readout'}
    return sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def span_cover(candidates, budget):
    """Float screening proposes merges; an exact inequality accepts every merge."""
    retained, keep, cover, float_responses = [], [], [], []
    threshold, actual = float(2*budget), F(0)
    for i, (word, response) in enumerate(candidates):
        proposed, assigned = tuple(map(float, response)), None
        for j, (_, representative) in enumerate(retained):
            differences = [x-y for x, y in zip(proposed, float_responses[j])]
            if max(differences)-min(differences) <= threshold*(1+1e-10)+1e-15:
                gap = span_difference(response, representative)
                if gap <= 2*budget:
                    actual = max(actual, gap/2)
                    assigned = j
                    break
        if assigned is None:
            assigned = len(retained)
            retained.append((word, response)); keep.append(i); float_responses.append(proposed)
        cover.append(assigned)
    return retained, {'keep': keep, 'cover': cover, 'maximum_actual_error': str(actual)}


def check_span(candidates, level, budget):
    if type(level) is not dict or set(level) != {'keep', 'cover', 'maximum_actual_error'}:
        raise ValueError('span-cover layer')
    keep, cover = level['keep'], level['cover']
    if (type(keep) is not list or not keep or
            any(type(j) is not int or not 0 <= j < len(candidates) for j in keep) or
            len(set(keep)) != len(keep)):
        raise ValueError('span-cover kept indices')
    if (type(cover) is not list or len(cover) != len(candidates) or
            any(type(j) is not int or not 0 <= j < len(keep) for j in cover)):
        raise ValueError('span-cover witness indices')
    retained = [candidates[j] for j in keep]
    actual = F(0)
    for (_, response), j in zip(candidates, cover):
        gap = span_difference(response, retained[j][1])
        if gap > 2*budget:
            raise ValueError('false exact span bound')
        actual = max(actual, gap/2)
    if actual != _rational(level['maximum_actual_error']):
        raise ValueError('false local error ledger')
    return retained


def _build(operators, terminal, k, epsilon, supplied=None):
    A = transports(operators)
    suffixes, frontier, layers, stats, error = [('', terminal)], [], [], [], F(0)
    budget = epsilon/k if k else F(0)
    for n in range(k+1):
        layer = supplied[n] if supplied is not None else None
        if supplied is not None and (type(layer) is not dict or set(layer) != {'suffix', 'family'}):
            raise ValueError('control layer')
        if n:
            suffix_candidates = [(a+word, apply(operators[a], q))
                                 for word, q in suffixes for a in ('D', 'R')]
            if supplied is None:
                suffixes, suffix_level = span_cover(suffix_candidates, budget)
            else:
                suffix_level = layer['suffix']
                suffixes = check_span(suffix_candidates, suffix_level, budget)
            error += _rational(suffix_level['maximum_actual_error'])
        else:
            suffix_candidates, suffix_level = suffixes, None
            if supplied is not None and layer['suffix'] is not None:
                raise ValueError('zero-horizon suffix witness')
        candidates = _candidates(n, suffixes, frontier, operators, terminal, A)
        if supplied is None:
            frontier, family_level = _cover(candidates)
        else:
            family_level = layer['family']
            if type(family_level) is not dict or set(family_level) != {'keep', 'cover'}:
                raise ValueError('outer cover layer')
            frontier = _check_cover(candidates, family_level)
        if error > epsilon:
            raise ValueError('accumulated error exceeds epsilon')
        layers.append({'suffix': suffix_level, 'family': family_level})
        generated = {word for word, _ in suffix_candidates} | {word for word, _ in candidates}
        stats.append({'n': n, 'suffix_candidates': len(suffix_candidates),
                      'retained_suffixes': len(suffixes), 'program_candidates': len(candidates),
                      'retained_programs': len(frontier), 'complete_words_constructed': len(generated),
                      'complete_words_avoided': (n+2)*2**n-len(generated), 'uniform_error': str(error)})
    return frontier, layers, stats


def compile_control(operators, terminal, k, epsilon):
    operators, terminal, epsilon = _contract(operators, terminal, k, epsilon)
    frontier, layers, stats = _build(operators, terminal, k, epsilon)
    certificate = {'schema': SCHEMA, 'ordinary_updates': k, 'epsilon': str(epsilon),
                   'binding': _binding(operators, terminal, k, epsilon), 'layers': layers}
    return frontier, certificate, stats


def check_control(certificate, operators, terminal, k, epsilon):
    """Replay physical responses and exact supplied bounds, without merge search."""
    try:
        operators, terminal, epsilon = _contract(operators, terminal, k, epsilon)
        if (type(certificate) is not dict or
                set(certificate) != {'schema', 'ordinary_updates', 'epsilon', 'binding', 'layers'}):
            raise ValueError('control certificate object')
        if (certificate['schema'] != SCHEMA or type(certificate['ordinary_updates']) is not int or
                certificate['ordinary_updates'] != k or _rational(certificate['epsilon']) != epsilon or
                certificate['binding'] != _binding(operators, terminal, k, epsilon)):
            raise ValueError('control contract or binding')
        if type(certificate['layers']) is not list or len(certificate['layers']) != k+1:
            raise ValueError('control layers')
        frontier, _, stats = _build(operators, terminal, k, epsilon, certificate['layers'])
        return frontier, stats
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed exploratory span certificate') from error


def sanity():
    operators, terminal = base_operators(), base_probes()['readout']
    # A rounded proposal just above the boundary must still be rejected exactly.
    zero = (F(0),)*16
    candidate = zero[:-1]+(F(1, 50)+F(1, 10**30),)
    retained, level = span_cover([('', zero), ('D', candidate)], F(1, 100))
    assert len(retained) == 2
    assert check_span([('', zero), ('D', candidate)], level, F(1, 100)) == retained
    bad = {'keep': [0], 'cover': [0, 0], 'maximum_actual_error': '1/100'}
    try:
        check_span([('', zero), ('D', candidate)], bad, F(1, 100))
    except ValueError:
        pass
    else:
        raise AssertionError('false exact span bound accepted')
    direction = tuple(F((7*j) % 11, 11) for j in range(16))
    for kernel in operators.values():
        assert span_difference(apply(kernel, direction), zero) <= span_difference(direction, zero)
    changed = deepcopy(operators)
    changed['D'] = list(changed['D'])
    changed['D'][0] = {j: value/2 for j, value in changed['D'][0].items()}
    try:
        compile_control(changed, terminal, 2, F(1, 100))
    except ValueError:
        pass
    else:
        raise AssertionError('substochastic kernel accepted')
    signatures = [contrast_signature(*law) for law in preparation_laws(2).values()]
    full = [(''.join(word), contrast_response(word_value(operators, word, terminal)))
            for word in plan_words(3)]
    full_values = evaluate_frontier(full, signatures)
    full_best = tuple(max(row) for row in full_values)
    optimum_regret = min(max(best-row[j] for best, row in zip(full_best, full_values))
                         for j in range(len(full)))
    results = []
    for epsilon in (F(0), F(1, 20)):
        frontier, certificate, stats = compile_control(operators, terminal, 3, epsilon)
        checked, checked_stats = check_control(json.loads(json.dumps(certificate)),
                                              operators, terminal, 3, epsilon)
        assert checked == frontier and checked_stats == stats
        error = F(stats[-1]['uniform_error'])
        values = evaluate_frontier(frontier, signatures)
        best = tuple(max(row) for row in values)
        assert all(0 <= a-b <= error for a, b in zip(full_best, best))
        chosen = min(range(len(frontier)), key=lambda j: max(b-row[j] for b, row in zip(best, values)))
        actual_regret = max(b-row[chosen] for b, row in zip(full_best, values))
        assert actual_regret <= optimum_regret+2*error
        for j in range(len(full)):
            assert any(all(row[r] >= full_row[j]-error for row, full_row in zip(values, full_values))
                       for r in range(len(frontier)))
        results.append({'epsilon': str(epsilon), 'retained_suffixes': stats[-1]['retained_suffixes'],
                        'uniform_error': str(error), 'retained_programs': len(frontier)})
    return {'sanity': 'passed', 'physical_horizon': 3, 'preparation_horizon': 2, 'cases': results}


def sweep():
    operators, terminal = base_operators(), base_probes()['readout']
    for k in (4, 6, 8, 10):
        started = perf_counter(); reference = compile_family(operators, terminal, k)
        elapsed = perf_counter()-started
        yield {'k': k, 'old_compile': elapsed, 'old_retained': len(reference[0])}
        for epsilon in (F(1, 100000), F(1, 10000), F(1, 1000)):
            started = perf_counter(); frontier, certificate, stats = compile_control(operators, terminal, k, epsilon)
            compile_time = perf_counter()-started
            started = perf_counter(); checked, checked_stats = check_control(certificate, operators, terminal, k, epsilon)
            check_time = perf_counter()-started
            assert frontier == checked and stats == checked_stats
            yield {'k': k, 'epsilon': str(epsilon), 'compile': compile_time, 'check': check_time,
                   'last': stats[-1], 'suffix_counts': [row['retained_suffixes'] for row in stats]}


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--sweep', action='store_true', help='reproduce all historical parameter settings')
    args = parser.parse_args()
    if args.sweep:
        for row in sweep():
            print(json.dumps(row, sort_keys=True), flush=True)
    else:
        print(json.dumps(sanity(), sort_keys=True))
