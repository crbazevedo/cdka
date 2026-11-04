"""Exact envelopes and complete-plan regret on finite reachable generators.

Rows of ``values`` are physically declared preparation laws; columns are
complete plans legal for every row.  Their reachability, resource accounting
and response values must be checked by the physical experiment.  This module
certifies what follows from the resulting rational response table.

The convex hull is an evaluator domain.  No historical row identifier,
posterior law, random choice of preparation, or numerical center is thereby
made readable or executable by the controller.  The optimized choice is one
common complete plan from the supplied list, including its already realized
internal stochastic routing.  No extra randomization among plans is assumed.

Public API:
    compile_reachable_interface(values, *, preparation_labels=None,
                                plan_labels=None, contract=None) -> dict
    verify_reachable_interface(certificate, values, same keywords) -> True
    table_binding(values, same keywords) -> SHA-256 string
    admissible_plans(certificate, *, maximum_regret=None,
                     minimum_value=None) -> list[int]
    contrast_value(mu_zero, mu_one, readout_response,
                   *, mass_response=None) -> Fraction

The certificate is JSON portable.  Its checker verifies attaining witnesses
and inequalities without invoking the optimizer, an LP solver, or a search
for a center.  Exact fractions, integers and rational strings are accepted;
binary floating-point table entries are rejected.
"""
from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction as F
from hashlib import sha256
import json


SCHEMA = 'cdka.reachable-response-interface/v1'


def _fraction(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError('exact rational values are required; floats are not accepted')
    return F(value)


def _labels(labels, count, prefix):
    result = tuple(f'{prefix}_{i}' for i in range(count)) if labels is None else tuple(labels)
    if len(result) != count or any(not isinstance(x, str) for x in result) \
            or len(set(result)) != count:
        raise ValueError('labels must be distinct strings with the declared count')
    return result


def _prepare(values, preparation_labels, plan_labels):
    if isinstance(values, (str, bytes)):
        raise ValueError('a nonempty rectangular rational table is required')
    rows = []
    for row in values:
        if isinstance(row, (str, bytes)):
            raise ValueError('table rows must be sequences of exact values')
        rows.append(tuple(_fraction(x) for x in row))
    result = tuple(rows)
    if not result or not result[0] or any(len(row) != len(result[0]) for row in result):
        raise ValueError('a nonempty rectangular rational table is required')
    return (result, _labels(preparation_labels, len(result), 'preparation'),
            _labels(plan_labels, len(result[0]), 'plan'))


def _metadata(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValueError('contract keys must be strings')
        return {key: _metadata(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_metadata(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError('contract metadata must be JSON serializable')


def _binding(values, preparation_labels, plan_labels, contract):
    payload = {
        'schema': SCHEMA,
        'preparation_labels': list(preparation_labels),
        'plan_labels': list(plan_labels),
        'values': [list(map(str, row)) for row in values],
        'contract': _metadata({} if contract is None else contract),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=True, allow_nan=False).encode()
    return sha256(encoded).hexdigest()


def table_binding(values, *, preparation_labels=None, plan_labels=None, contract=None):
    """Bind exact values, their ordered identities, and the physical contract."""
    table, rows, columns = _prepare(values, preparation_labels, plan_labels)
    return _binding(table, rows, columns, contract)


def _argmax(values):
    """Generator-only optimization, with the first index breaking ties."""
    return max(range(len(values)), key=values.__getitem__)


def _argmin(values):
    """Generator-only optimization, with the first index breaking ties."""
    return min(range(len(values)), key=values.__getitem__)


def compile_reachable_interface(values, *, preparation_labels=None,
                                plan_labels=None, contract=None):
    """Compile exact uniform prediction and deterministic common-plan bounds.

    The free response center minimizes maximum absolute prediction error
    among arbitrary common vectors.  The uniform-law center is the response
    of the arithmetic mean of the input laws; its error is measured, without
    claiming that this is the best center constrained to be a law or that
    the averaged preparation is physically attainable.

    Regret uses the same row for the chosen plan and its comparator.  The
    chosen plan minimizes worst-case regret among the supplied complete
    plans.  All optimization is a finite rational scan; no LP is needed.
    """
    table, rows, columns = _prepare(values, preparation_labels, plan_labels)
    m, k = len(table), len(table[0])
    transposed = tuple(tuple(table[i][j] for i in range(m)) for j in range(k))
    lower_witnesses = [_argmin(column) for column in transposed]
    upper_witnesses = [_argmax(column) for column in transposed]
    lower = tuple(table[lower_witnesses[j]][j] for j in range(k))
    upper = tuple(table[upper_witnesses[j]][j] for j in range(k))
    center = tuple((a+b)/2 for a, b in zip(lower, upper))
    widths = tuple(b-a for a, b in zip(lower, upper))
    diameter_plan = _argmax(widths)
    radius = widths[diameter_plan]/2

    uniform_center = tuple(sum(column, F(0))/m for column in transposed)
    uniform_errors = tuple(abs(table[i][j]-uniform_center[j])
                           for i in range(m) for j in range(k))
    uniform_witness = _argmax(uniform_errors)

    best_plan = tuple(_argmax(row) for row in table)
    best_values = tuple(table[i][best_plan[i]] for i in range(m))
    regret_columns = tuple(tuple(best_values[i]-table[i][j] for i in range(m))
                           for j in range(k))
    regret_witnesses = tuple(_argmax(column) for column in regret_columns)
    plan_regrets = tuple(regret_columns[j][regret_witnesses[j]] for j in range(k))
    chosen = _argmin(plan_regrets)
    maximin = _argmax(lower)

    return {
        'schema': SCHEMA,
        'contract_sha256': _binding(table, rows, columns, contract),
        'preparation_count': m,
        'plan_count': k,
        'preparation_labels': list(rows),
        'plan_labels': list(columns),
        'prediction': {
            'lower': list(map(str, lower)),
            'upper': list(map(str, upper)),
            'lower_witnesses': lower_witnesses,
            'upper_witnesses': upper_witnesses,
            'free_center': list(map(str, center)),
            'free_radius': str(radius),
            'diameter_plan': diameter_plan,
            'uniform_law_center': list(map(str, uniform_center)),
            'uniform_law_radius': str(uniform_errors[uniform_witness]),
            'uniform_law_radius_witness': {
                'preparation': uniform_witness//k,
                'plan': uniform_witness % k,
            },
        },
        'decision': {
            'preparation_optima': list(map(str, best_values)),
            'preparation_optimal_plans': list(best_plan),
            'plan_regrets': list(map(str, plan_regrets)),
            'plan_regret_witnesses': [
                {'preparation': i, 'comparator_plan': best_plan[i]}
                for i in regret_witnesses
            ],
            'chosen_plan': chosen,
            'minimax_regret': str(plan_regrets[chosen]),
            'maximin_plan': maximin,
            'maximin_value': str(lower[maximin]),
            'common_optimal_plans': [j for j, loss in enumerate(plan_regrets) if loss == 0],
        },
    }


def _require(condition, message):
    if not condition:
        raise ValueError('invalid reachable-interface certificate: '+message)


def _index(value, size, name):
    _require(type(value) is int and 0 <= value < size, name+' index')
    return value


def _vector(values, size, name):
    _require(isinstance(values, (tuple, list)) and len(values) == size, name+' length')
    return tuple(_fraction(x) for x in values)


def _indices(values, size, upper, name):
    _require(isinstance(values, (tuple, list)) and len(values) == size, name+' length')
    return tuple(_index(x, upper, name) for x in values)


def _verify(certificate, table, rows, columns, contract):
    m, k = len(table), len(table[0])
    _require(isinstance(certificate, Mapping), 'certificate object')
    _require(certificate['schema'] == SCHEMA, 'schema')
    _require(certificate['contract_sha256'] == _binding(table, rows, columns, contract),
             'table or contract binding')
    _require(type(certificate['preparation_count']) is int
             and certificate['preparation_count'] == m, 'preparation count')
    _require(type(certificate['plan_count']) is int
             and certificate['plan_count'] == k, 'plan count')
    _require(certificate['preparation_labels'] == list(rows), 'preparation identities')
    _require(certificate['plan_labels'] == list(columns), 'complete-plan identities')

    prediction = certificate['prediction']
    lower = _vector(prediction['lower'], k, 'lower')
    upper = _vector(prediction['upper'], k, 'upper')
    low_indices = _indices(prediction['lower_witnesses'], k, m, 'lower witness')
    high_indices = _indices(prediction['upper_witnesses'], k, m, 'upper witness')
    center = _vector(prediction['free_center'], k, 'free center')
    radius = _fraction(prediction['free_radius'])
    diameter = _index(prediction['diameter_plan'], k, 'diameter plan')
    _require(radius >= 0, 'negative free radius')
    for j in range(k):
        _require(table[low_indices[j]][j] == lower[j], 'lower endpoint does not attain bound')
        _require(table[high_indices[j]][j] == upper[j], 'upper endpoint does not attain bound')
        _require(center[j] == (lower[j]+upper[j])/2, 'free center is not midpoint of bounds')
        _require(upper[j]-lower[j] <= 2*radius, 'free radius too small')
        for row in table:
            _require(lower[j] <= row[j] <= upper[j], 'response outside certified envelope')
    _require(upper[diameter]-lower[diameter] == 2*radius,
             'diameter does not attain free radius')

    uniform = _vector(prediction['uniform_law_center'], k, 'uniform-law center')
    uniform_radius = _fraction(prediction['uniform_law_radius'])
    _require(uniform_radius >= 0, 'negative uniform-law radius')
    for j in range(k):
        _require(m*uniform[j] == sum((row[j] for row in table), F(0)),
                 'uniform-law center is not the mean response')
        for row in table:
            _require(abs(row[j]-uniform[j]) <= uniform_radius, 'uniform-law radius too small')
    witness = prediction['uniform_law_radius_witness']
    i = _index(witness['preparation'], m, 'uniform-law preparation witness')
    j = _index(witness['plan'], k, 'uniform-law plan witness')
    _require(abs(table[i][j]-uniform[j]) == uniform_radius,
             'uniform-law radius not attained')

    decision = certificate['decision']
    best = _vector(decision['preparation_optima'], m, 'preparation optima')
    best_plan = _indices(decision['preparation_optimal_plans'], m, k, 'optimal plan')
    for i, row in enumerate(table):
        _require(row[best_plan[i]] == best[i], 'preparation optimum not attained')
        for value in row:
            _require(value <= best[i], 'preparation optimum is not an upper bound')

    regrets = _vector(decision['plan_regrets'], k, 'plan regrets')
    witnesses = decision['plan_regret_witnesses']
    _require(isinstance(witnesses, (tuple, list)) and len(witnesses) == k,
             'plan regret witness count')
    for p, loss in enumerate(regrets):
        _require(loss >= 0, 'negative plan regret')
        for i, row in enumerate(table):
            _require(best[i]-row[p] <= loss, 'plan regret is not an upper bound')
        i = _index(witnesses[p]['preparation'], m, 'regret preparation witness')
        q = _index(witnesses[p]['comparator_plan'], k, 'regret comparator witness')
        _require(table[i][q] == best[i], 'regret comparator not optimal at its preparation')
        _require(table[i][q]-table[i][p] == loss, 'regret lower witness does not attain bound')

    chosen = _index(decision['chosen_plan'], k, 'chosen complete plan')
    optimum = _fraction(decision['minimax_regret'])
    _require(regrets[chosen] == optimum, 'chosen plan does not attain minimax bound')
    for loss in regrets:
        _require(optimum <= loss, 'another complete plan has smaller worst-case regret')
    maximin = _index(decision['maximin_plan'], k, 'maximin complete plan')
    maximin_value = _fraction(decision['maximin_value'])
    _require(lower[maximin] == maximin_value, 'maximin plan does not attain its value')
    for value in lower:
        _require(value <= maximin_value, 'another complete plan has a larger minimum value')
    common = decision['common_optimal_plans']
    _require(isinstance(common, (tuple, list)) and all(type(j) is int for j in common),
             'common-plan indices')
    _require(list(common) == [j for j, loss in enumerate(regrets) if loss == 0],
             'common complete-plan set is incorrect')
    return True


def verify_reachable_interface(certificate, values, *, preparation_labels=None,
                               plan_labels=None, contract=None):
    """Check exact upper bounds and attaining lower witnesses independently.

    The physical experiment remains responsible for checking that every
    table row is reachable, every column is a complete legal plan, and every
    entry is its physical response.  Their scope and resource declarations
    should be included in ``contract`` so that they are bound to this proof.
    """
    table, rows, columns = _prepare(values, preparation_labels, plan_labels)
    try:
        return _verify(certificate, table, rows, columns, contract)
    except (KeyError, TypeError, IndexError, ZeroDivisionError) as exc:
        raise ValueError('invalid reachable-interface certificate: malformed data') from exc


def admissible_plans(certificate, *, maximum_regret=None, minimum_value=None):
    """Query an already verified certificate for joint regret/value guarantees.

    ``prediction.lower`` is the per-plan minimum absolute value, attained by
    its corresponding ``lower_witnesses`` entry.  This shares the exact
    extrema with the prediction certificate instead of storing a second
    copy.  A returned plan satisfies BOTH supplied inclusive thresholds.
    This helper does not authenticate a certificate; call the verifier with
    its physical response table and contract first.
    """
    k = certificate['plan_count']
    _require(type(k) is int and k > 0, 'plan count')
    lower = _vector(certificate['prediction']['lower'], k, 'lower')
    regret = _vector(certificate['decision']['plan_regrets'], k, 'plan regrets')
    bound = None if maximum_regret is None else _fraction(maximum_regret)
    floor = None if minimum_value is None else _fraction(minimum_value)
    return [j for j in range(k) if (bound is None or regret[j] <= bound)
            and (floor is None or lower[j] >= floor)]


def contrast_value(mu_zero, mu_one, readout_response, *, mass_response=None):
    """Success probability for a hidden, constant bit with shared dynamics.

    ``mu_zero`` and ``mu_one`` are nonnegative submeasures over physical
    states, jointly representing H=0 and H=1.  ``readout_response`` is K_w g.
    For a legal mass-preserving word, the success probability is

        mass(mu_zero) + (mu_one-mu_zero) K_w g.

    For a substochastic word, supply ``mass_response=K_w 1``; the general
    first term is mu_zero K_w 1.  This preserves the hidden-bit dependence
    without constructing a doubled physical transition matrix.  The signed
    contrast is an evaluator quantity, never a physical probability law.
    """
    zero = tuple(_fraction(x) for x in mu_zero)
    one = tuple(_fraction(x) for x in mu_one)
    response = tuple(_fraction(x) for x in readout_response)
    mass = tuple(F(1) for _ in zero) if mass_response is None \
        else tuple(_fraction(x) for x in mass_response)
    if not zero or len(one) != len(zero) or len(response) != len(zero) \
            or len(mass) != len(zero):
        raise ValueError('submeasures and response vectors need a common positive dimension')
    if any(x < 0 for x in zero+one) or any(not 0 <= x <= t <= 1
                                          for x, t in zip(response, mass)):
        raise ValueError('nonnegative submeasures and valid success/mass responses are required')
    return sum((a*t+(b-a)*x for a, b, x, t in zip(zero, one, response, mass)), F(0))
