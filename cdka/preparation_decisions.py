"""Compact common decisions over a streamed or independently covered family.

The reference walks every fixed-length ordinary history depth first, keeping
only a path of signatures and per-program extrema/attainers. It never builds
the exponential preparation-by-program table or publishes every informed
value. A checked preparation hull can supply a smaller family to the same
decision logic. Its independent coverage proof is an explicit premise: the
enclosing pipeline must check that proof from the same raw physical inputs.

The certificate gives exact worst regret and minimum fidelity for every
supplied complete program, actual history attainers, and one minimax/maximin
choice. Universal inequalities are checked over the complete stream or the
independently certified hull; attainers are physically propagated separately.
A few attaining histories alone are not an optimality or coverage proof.

Physical program-response correctness and complete-program coverage remain
the existing family checker's obligation. This module binds those exact
ordered responses and identities, rather than assuming a digest proves them.
"""
from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json

from .preparation_families import make_preparation_model, preparation_binding as _preparation_binding
from .program_families import _exact, _rational
from .semantic_closure import dot, push
from .suffix_features import _model, check_features


SCHEMA = 'cdka.compact-preparation-decision/v1'
PROBLEM_SCHEMA = 'cdka.preparation-decision-problem/v1'
OUTPUT_CONTRACT = (
    'exact per-program worst same-preparation regret and minimum fidelity; '
    'actual history/comparator attainers; one minimax and one maximin; '
    'joint gates from these extrema; informed values by exact query, not an exhaustive output list'
)
_CERT_KEYS = {
    'schema', 'binding', 'preparation_binding', 'history_length', 'ordinary_updates',
    'plans', 'worst_regrets', 'minimum_fidelities', 'regret_attainers',
    'fidelity_attainers', 'minimax_plan', 'minimax_regret', 'maximin_plan',
    'maximin_fidelity',
}
_PROBLEM_KEYS = {
    'schema', 'operators', 'terminal', 'initial_law', 'history_length', 'frontier',
    'ordinary_updates', 'A', 'sparse_A', 'initial', 'offset', 'model_binding',
    'preparation_binding', 'contract', 'binding', 'codec',
}


def _count(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(name + ' must be a nonnegative integer')
    return value


def _metadata(value):
    """Portable contract metadata; no implicit float-to-rational conversion."""
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is F:
        return str(value)
    if type(value) in (tuple, list):
        return [_metadata(item) for item in value]
    if type(value) is dict and all(type(key) is str for key in value):
        return {key: _metadata(item) for key, item in value.items()}
    raise ValueError('exact JSON-compatible contract metadata required')


def _digest(value):
    return sha256(json.dumps(_exact(value), sort_keys=True,
                             separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def _law(value):
    if (type(value) not in (tuple, list) or len(value) != 2 or
            any(type(row) not in (tuple, list) or len(row) != 16 for row in value)):
        raise ValueError('two sixteen-coordinate source submeasures required')
    return tuple(tuple(map(_rational, row)) for row in value)


def _history(value, h):
    if type(value) is not str:
        raise ValueError('history word must be a string')
    if value == 'I' and h == 0:
        return ''
    if len(value) != h or any(letter not in ('D', 'R') for letter in value):
        raise ValueError('history must have exactly h ordinary updates')
    return value


def _frontier(value):
    if type(value) not in (tuple, list) or not value:
        raise ValueError('nonempty complete-program response frontier required')
    result = []
    ordinary = None
    seen = set()
    for entry in value:
        if type(entry) not in (tuple, list) or len(entry) != 2:
            raise ValueError('program-response pair required')
        word, response = entry
        if type(word) is not str:
            raise ValueError('complete program identity must be a string')
        word = '' if word == 'I' else word
        if any(letter not in ('D', 'R', 'M') for letter in word) or word.count('M') > 1:
            raise ValueError('complete programs use D/R and at most one M')
        if word in seen:
            raise ValueError('duplicate complete program identity')
        seen.add(word)
        n = len(word) - word.count('M')
        if ordinary is None:
            ordinary = n
        elif n != ordinary:
            raise ValueError('one mandatory ordinary workload required')
        if type(response) not in (tuple, list) or len(response) != 4:
            raise ValueError('four-coordinate program response required')
        result.append((word, tuple(map(_rational, response))))
    return tuple(result), ordinary


def _matrix_product_row(row, matrix):
    return tuple(sum((row[i]*matrix[i][j] for i in range(len(row)) if row[i]), F(0))
                 for j in range(len(matrix[0])))


def _shape(kappa):
    a, b = (3+kappa)/4, 3*(1-kappa)/4
    return ((a, b, F(0), F(0)), (F(0), F(0), a, b))


def _amplitudes(x):
    return x[0]+x[1]/3, x[2]+x[3]/3


def _codec(A, initial, h, frontier):
    """Recognize, then verify, a shared exact two-amplitude arithmetic codec.

    In the inherited model the shape parameter is (24/25)^(2(t+1)), where t
    counts trailing D updates. For both health blocks, full row identities at
    kappa=0 and1 prove the affine formulas for every kappa. R resets shape;
    D multiplies it by the fixed ratio. Failed identities select the generic
    four-coordinate path. No approximation or unverified stochastic quotient
    is introduced. Both streamed and covered queries receive this cache.
    """
    ratio = F(24, 25)**2
    zero, one = _shape(F(0)), _shape(F(1))
    D = tuple(_amplitudes(_matrix_product_row(row, A['D'])) for row in zero)
    R0 = tuple(_amplitudes(_matrix_product_row(row, A['R'])) for row in zero)
    R1 = tuple(_amplitudes(_matrix_product_row(row, A['R'])) for row in one)
    for kappa, rows, R in ((F(0), zero, R0), (F(1), one, R1)):
        for i, row in enumerate(rows):
            if (_matrix_product_row(row, A['D']) != _matrix_product_row(D[i], _shape(ratio*kappa)) or
                    _matrix_product_row(row, A['R']) != _matrix_product_row(R[i], _shape(ratio))):
                return None
    amplitudes = _amplitudes(initial)
    if _matrix_product_row(amplitudes, _shape(ratio)) != initial:
        return None
    kappas = tuple(ratio**(t+1) for t in range(h+1))
    R = tuple(tuple(tuple(a+kappa*(b-a) for a, b in zip(row0, row1))
                    for row0, row1 in zip(R0, R1)) for kappa in kappas)
    responses = tuple(tuple(tuple(dot(row, q) for row in _shape(kappa))
                            for _, q in frontier) for kappa in kappas)
    return {'ratio': ratio, 'initial': amplitudes, 'D': D, 'R': R,
            'kappas': kappas, 'responses': responses}


def make_problem(operators, terminal, initial_law, h, frontier, *,
                 feature_certificate=None, contract=None):
    """Validate and bind the raw physical decision problem.

    D/R preparation closure and the actual initial law are checked by the
    shared preparation model. The optional observer certificate is checked
    when supplied; it is not required for the standalone preparation algebra.
    The exact program frontier must separately be established by its physical
    family checker. Its identities, responses, workload and order are bound
    here. Hull coverage is reusable across program frontiers and terminal g;
    the decision binding additionally fixes them and all D/R/M operators.
    """
    _count(h, 'history length')
    operators, terminal = _model(operators, terminal)
    if any(sum(row.values(), F(0)) != 1 for rows in operators.values() for row in rows):
        raise ValueError('source fidelity requires stochastic physical operators')
    if any(not 0 <= value <= 1 for value in terminal):
        raise ValueError('terminal readout probabilities required')
    law = _law(initial_law)
    model = make_preparation_model(operators, law)
    if feature_certificate is not None:
        features = check_features(feature_certificate, operators, terminal)
        if any(tuple(tuple(row.get(j, F(0)) for j in range(4)) for row in features['A'][a])
               != model['A'][a] for a in ('D', 'R')):
            raise ValueError('observer and preparation transports disagree')
    frontier, k = _frontier(frontier)
    metadata = _metadata(contract)
    prep_binding = _preparation_binding(model, h)
    payload = {'schema': PROBLEM_SCHEMA, 'operators': operators, 'terminal': terminal,
               'initial_law': law, 'history_length': h, 'frontier': frontier,
               'ordinary_updates': k, 'preparation_binding': prep_binding,
               'contract': metadata, 'output_contract': OUTPUT_CONTRACT}
    return {'schema': PROBLEM_SCHEMA, 'operators': operators, 'terminal': terminal,
            'initial_law': law, 'history_length': h, 'frontier': frontier,
            'ordinary_updates': k, 'A': model['A'], 'sparse_A': model['sparse_A'],
            'initial': model['initial'], 'offset': model['offset'],
            'model_binding': model['binding'], 'preparation_binding': prep_binding,
            'contract': metadata, 'binding': _digest(payload),
            'codec': _codec(model['A'], model['initial'], h, frontier)}


def _checked_problem(problem):
    """Rebuild physical closure and derived data; a supplied dict is not authority."""
    if type(problem) is not dict or set(problem) != _PROBLEM_KEYS:
        raise ValueError('checked preparation-decision problem required')
    rebuilt = make_problem(problem['operators'], problem['terminal'], problem['initial_law'],
                           problem['history_length'], problem['frontier'], contract=problem['contract'])
    if problem != rebuilt or _digest(problem) != _digest(rebuilt):
        raise ValueError('problem binding or derived physical data changed')
    return rebuilt


def _word(index, h):
    return ''.join('R' if index >> bit & 1 else 'D' for bit in range(h-1, -1, -1))


def _walk(initial, h, advance):
    """Lexicographic depth-first traversal; at most h+1 state vectors live."""
    states, choices, index = [initial], [0], 0
    while states:
        depth = len(states)-1
        if depth == h:
            yield index, states[-1]
            index += 1
            states.pop(); choices.pop()
        elif choices[-1] == 2:
            states.pop(); choices.pop()
        else:
            letter = ('D', 'R')[choices[-1]]
            choices[-1] += 1
            states.append(advance(states[-1], letter))
            choices.append(0)


def _iter_preparations(problem):
    A = problem['sparse_A']
    for index, x in _walk(problem['initial'], problem['history_length'],
                          lambda x, a: push(x, A[a])):
        yield index, x


def iter_preparations(problem):
    """Yield actual (history,positive_x) pairs without a breadth-first table.

    The public iterator explicitly emits each requested history label. Compact
    decision compilation instead creates labels only for retained attainers.
    """
    try:
        problem = _checked_problem(problem)
        for index, x in _iter_preparations(problem):
            yield _word(index, problem['history_length']), x
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed preparation problem') from error


def _signature(problem, history):
    x = problem['initial']
    for letter in history:
        x = push(x, problem['sparse_A'][letter])
    return x


def _values(problem, x):
    return tuple(problem['offset']-dot(x, response) for _, response in problem['frontier'])


def _point(point, h):
    if type(point) not in (tuple, list) or len(point) != 2:
        raise ValueError('history-signature pair required')
    history, coordinates = point
    history = _history(history, h)
    if type(coordinates) not in (tuple, list) or len(coordinates) != 4:
        raise ValueError('four positive contrast coordinates required')
    x = tuple(map(_rational, coordinates))
    if any(value < 0 for value in x):
        raise ValueError('preparation outside nonnegative contrast cone')
    return history, x


def _rows(problem, preparations, supplied_binding):
    """Yield identifiers and one row at a time; use shared codec when verified."""
    h, codec = problem['history_length'], problem['codec']
    if preparations is None:
        if supplied_binding is not None and supplied_binding != problem['preparation_binding']:
            raise ValueError('preparation binding')
        if codec is None:
            for index, x in _iter_preparations(problem):
                yield index, _values(problem, x)
        else:
            def advance(state, letter):
                amplitudes, trailing = state
                matrix = codec['D'] if letter == 'D' else codec['R'][trailing]
                return _matrix_product_row(amplitudes, matrix), trailing+1 if letter == 'D' else 0
            for index, (amplitudes, trailing) in _walk((codec['initial'], 0), h, advance):
                yield index, tuple(problem['offset']-dot(amplitudes, response)
                                   for response in codec['responses'][trailing])
        return
    if supplied_binding != problem['preparation_binding']:
        raise ValueError('independently checked hull binding required for supplied preparations')
    for point in preparations:
        history, x = _point(point, h)
        if codec is None:
            yield history, _values(problem, x)
        else:
            trailing = len(history)-len(history.rstrip('D'))
            amplitudes = _amplitudes(x)
            # A hull's actual representative must have the same physical
            # shape as its named history. Full coverage is checked elsewhere.
            if _matrix_product_row(amplitudes, _shape(codec['kappas'][trailing])) != x:
                raise ValueError('history signature violates the verified shape codec')
            yield history, tuple(problem['offset']-dot(amplitudes, response)
                                 for response in codec['responses'][trailing])


def compile_decision(problem, preparations=None, *, preparation_binding=None):
    """Return (portable certificate,work counts), retaining one value row.

    Supplied preparations must be the representatives returned by an
    independent hull checker invoked on the same raw operators, initial law
    and h. Pass that checked family's binding explicitly. This identity guard
    is not a replacement for its coverage proof. The complete enclosing
    pipeline must recheck that proof before calling check_decision below.
    """
    try:
        problem = _checked_problem(problem)
        n, h = len(problem['frontier']), problem['history_length']
        regrets, minima = [None]*n, [None]*n
        regret_attainers, fidelity_attainers = [None]*n, [None]*n
        count = 0
        for identifier, values in _rows(problem, preparations, preparation_binding):
            count += 1
            best_index = max(range(n), key=values.__getitem__)
            best = values[best_index]
            named = None
            for j, value in enumerate(values):
                regret = best-value
                if regrets[j] is None or regret > regrets[j]:
                    if named is None:
                        named = _word(identifier, h) if type(identifier) is int else identifier
                    regrets[j] = regret
                    regret_attainers[j] = {'history': named, 'comparator': best_index}
                if minima[j] is None or value < minima[j]:
                    if named is None:
                        named = _word(identifier, h) if type(identifier) is int else identifier
                    minima[j] = value
                    fidelity_attainers[j] = named
        if not count:
            raise ValueError('nonempty preparation family required')
        if preparations is None and count != 2**h:
            raise ValueError('incomplete streamed grammar')
        minimax = min(range(n), key=regrets.__getitem__)
        maximin = max(range(n), key=minima.__getitem__)
        certificate = {
            'schema': SCHEMA, 'binding': problem['binding'],
            'preparation_binding': problem['preparation_binding'],
            'history_length': h, 'ordinary_updates': problem['ordinary_updates'],
            'plans': [word or 'I' for word, _ in problem['frontier']],
            'worst_regrets': list(map(str, regrets)),
            'minimum_fidelities': list(map(str, minima)),
            'regret_attainers': regret_attainers, 'fidelity_attainers': fidelity_attainers,
            'minimax_plan': minimax, 'minimax_regret': str(regrets[minimax]),
            'maximin_plan': maximin, 'maximin_fidelity': str(minima[maximin]),
        }
        return certificate, {'preparations_evaluated': count, 'program_count': n,
                             'values_evaluated': count*n, 'explicit_value_table': False,
                             'explicit_informed_profile': False,
                             'maximum_live_signature_vectors': h+1 if preparations is None else 1,
                             'query_coordinates': 2 if problem['codec'] is not None else 4,
                             'codec_response_pairs': (h+1)*n if problem['codec'] is not None else 0}
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed compact decision input') from error


def _parse_certificate(certificate, problem=None):
    if type(certificate) is not dict or set(certificate) != _CERT_KEYS:
        raise ValueError('compact preparation decision certificate object')
    if certificate['schema'] != SCHEMA:
        raise ValueError('compact decision schema')
    _count(certificate['history_length'], 'history length')
    _count(certificate['ordinary_updates'], 'ordinary workload')
    plans = certificate['plans']
    if (type(plans) is not list or not plans or
            any(type(word) is not str or not word for word in plans) or len(set(plans)) != len(plans)):
        raise ValueError('ordered complete-program labels')
    n, h = len(plans), certificate['history_length']
    if problem is not None:
        if (certificate['binding'] != problem['binding'] or
                certificate['preparation_binding'] != problem['preparation_binding'] or
                h != problem['history_length'] or
                certificate['ordinary_updates'] != problem['ordinary_updates'] or
                plans != [word or 'I' for word, _ in problem['frontier']]):
            raise ValueError('compact decision identity or contract binding')
    elif any(type(certificate[key]) is not str or len(certificate[key]) != 64
             for key in ('binding', 'preparation_binding')):
        raise ValueError('bound decision digests required')
    vectors = []
    for key in ('worst_regrets', 'minimum_fidelities'):
        if type(certificate[key]) is not list or len(certificate[key]) != n:
            raise ValueError('one exact extremum per complete program required')
        vectors.append(tuple(map(_rational, certificate[key])))
    regrets, minima = vectors
    if any(value < 0 for value in regrets):
        raise ValueError('regret is nonnegative')
    raw_r, raw_f = certificate['regret_attainers'], certificate['fidelity_attainers']
    if (type(raw_r) is not list or len(raw_r) != n or
            type(raw_f) is not list or len(raw_f) != n):
        raise ValueError('one attaining history per extremum required')
    regret_attainers = []
    for witness in raw_r:
        if type(witness) is not dict or set(witness) != {'history', 'comparator'}:
            raise ValueError('history and informed comparator required')
        j = witness['comparator']
        if type(j) is not int or not 0 <= j < n:
            raise ValueError('informed comparator index')
        regret_attainers.append((_history(witness['history'], h), j))
    fidelity_attainers = tuple(_history(word, h) for word in raw_f)
    p, q = certificate['minimax_plan'], certificate['maximin_plan']
    if any(type(j) is not int or not 0 <= j < n for j in (p, q)):
        raise ValueError('selected complete-program indices')
    r, f = _rational(certificate['minimax_regret']), _rational(certificate['maximin_fidelity'])
    if regrets[p] != r or any(value < r for value in regrets):
        raise ValueError('minimax extremum comparison')
    if minima[q] != f or any(value > f for value in minima):
        raise ValueError('maximin extremum comparison')
    return regrets, minima, tuple(regret_attainers), fidelity_attainers


def check_decision(certificate, problem, preparations=None, *, preparation_binding=None):
    """Verify universal bounds, physical attainers and optimality, without search.

    The default replays every physical preparation history. For a smaller
    supplied family, the enclosing verifier must first establish its hull
    coverage from the same raw inputs and pass its matching preparation_binding.
    This checker then verifies the shared compact decision relative to that
    established coverage. It never infers coverage from a digest or samples.
    """
    try:
        problem = _checked_problem(problem)
        regrets, minima, regret_attainers, fidelity_attainers = _parse_certificate(certificate, problem)
        n, h = len(problem['frontier']), problem['history_length']
        count = 0
        for _, values in _rows(problem, preparations, preparation_binding):
            count += 1
            best = max(values)
            if any(best-value > regrets[j] or value < minima[j] for j, value in enumerate(values)):
                raise ValueError('false universal regret or fidelity bound')
        if not count or preparations is None and count != 2**h:
            raise ValueError('nonempty complete preparation coverage required')
        # Attaining histories are independently propagated, even if they are
        # absent from a particular equivalent hull representative list.
        histories = {word for word, _ in regret_attainers} | set(fidelity_attainers)
        attaining_rows = {word: _values(problem, _signature(problem, word)) for word in histories}
        for j, (word, comparator) in enumerate(regret_attainers):
            values = attaining_rows[word]
            if values[comparator] != max(values) or values[comparator]-values[j] != regrets[j]:
                raise ValueError('false same-history regret attainer or informed comparator')
        for j, word in enumerate(fidelity_attainers):
            if attaining_rows[word][j] != minima[j]:
                raise ValueError('false minimum-fidelity attainer')
        return True
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed compact preparation decision certificate') from error


def query_informed(problem, history):
    """Read and propagate one actual history, then evaluate its informed value."""
    try:
        problem = _checked_problem(problem)
        history = _history(history, problem['history_length'])
        x = _signature(problem, history)
        values = _values(problem, x)
        best = max(range(len(values)), key=values.__getitem__)
        return {'history': history, 'signature': x, 'best_value': values[best],
                'best_plan': best, 'plan': problem['frontier'][best][0] or 'I'}
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed informed-value query') from error


def query_informed_x(problem, x):
    """Evaluate B(x) directly from the checked frontier, never by interpolation.

    The query accepts any nonnegative four-coordinate contrast signature,
    including a convex mixture of preparations. It does not certify that an
    arbitrary input signature is itself an executable preparation history.
    """
    try:
        problem = _checked_problem(problem)
        if type(x) not in (tuple, list) or len(x) != 4:
            raise ValueError('four exact contrast coordinates required')
        x = tuple(map(_rational, x))
        if any(value < 0 for value in x):
            raise ValueError('informed query outside the nonnegative contrast cone')
        values = _values(problem, x)
        best = max(range(len(values)), key=values.__getitem__)
        return {'signature': x, 'best_value': values[best], 'best_plan': best,
                'plan': problem['frontier'][best][0] or 'I'}
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed informed-signature query') from error


def joint_gate(certificate, maximum_regret, minimum_fidelity):
    """Return feasible retained indices from an already verified certificate.

    This scan does not replace check_decision or either coverage certificate.
    Its extrema enforce both requirements on the same complete program.
    """
    try:
        regrets, minima, _, _ = _parse_certificate(certificate)
        delta, floor = _rational(maximum_regret), _rational(minimum_fidelity)
        if delta < 0:
            raise ValueError('nonnegative maximum regret required')
        return [j for j, (regret, fidelity) in enumerate(zip(regrets, minima))
                if regret <= delta and fidelity >= floor]
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed joint decision gate') from error
