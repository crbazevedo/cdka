"""Exact task signatures for one paid maintenance capability.

This module reuses the v12 response-space engine.  Its new contract is a
resource grammar: arbitrary old updates, at most ONE maintenance call, then
old updates again.  In particular it never infers a one-call result from a
closure that silently allows arbitrarily many maintenance calls.

Certificates contain actual continuation witnesses, coordinate identities,
and an invertible minor proving rank.  The verifier checks those identities
directly; it does not run closure discovery or Gaussian elimination.  The
signatures are evaluator coordinates of unnormalised laws, not readable
controller inputs, physical code states, or bits of memory.
"""
from __future__ import annotations

from collections import deque
from fractions import Fraction as F
from hashlib import sha256
import json
from typing import Mapping

from .semantic_closure import ExactBasis, apply, close_continuations, matrix, vector

SCHEMA = 'cdka.one-maintenance-signatures/v1'
FINITE_SCHEMA = 'cdka.finite-maintenance-signatures/v1'


def _prepare(base_operators, maintenance, probes, maintenance_label):
    if not isinstance(maintenance_label, str) or not maintenance_label:
        raise ValueError('a nonempty maintenance label is required')
    if not base_operators or not probes:
        raise ValueError('at least one old update and one probe are required')
    if any(not isinstance(k, str) or not k for k in (*base_operators, *probes)):
        raise ValueError('operator and probe labels must be nonempty strings')
    if maintenance_label in base_operators:
        raise ValueError('maintenance must not be an old update label')
    ops = {k: matrix(base_operators[k]) for k in sorted(base_operators)}
    maint = matrix(maintenance)
    ps = {k: vector(probes[k]) for k in sorted(probes)}
    n = len(next(iter(ps.values())))
    if not n or len(maint) != n or any(len(q) != n for q in ops.values()) \
            or any(len(v) != n for v in ps.values()):
        raise ValueError('common positive finite dimension required')
    return ops, maint, ps, n


def _json_value(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Mapping):
        return {str(k): _json_value(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(v) for v in value]
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise TypeError('contract metadata must be JSON serializable')


def _binding(ops, maintenance, probes, maintenance_label, contract):
    def kernel(q):
        return [[[j, str(p)] for j, p in sorted(row.items())] for row in q]
    payload = {
        'base_operators': {k: kernel(q) for k, q in ops.items()},
        'maintenance_label': maintenance_label,
        'maintenance': kernel(maintenance),
        'probes': {k: list(map(str, v)) for k, v in probes.items()},
        'physical_contract': _json_value({} if contract is None else contract),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=True, allow_nan=False).encode()
    return sha256(encoded).hexdigest()


def contract_binding(base_operators, maintenance, probes, *,
                     maintenance_label='M', contract=None):
    """Bind a certificate to every rational kernel entry and its stated scope."""
    ops, maint, ps, _ = _prepare(base_operators, maintenance, probes, maintenance_label)
    return _binding(ops, maint, ps, maintenance_label, contract)


def _inverse(a):
    """Generator-only exact inversion; the checker only multiplies the result."""
    n = len(a)
    rows = [[F(x) for x in row] + [F(i == j) for j in range(n)]
            for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            raise ValueError('claimed basis minor is singular')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                scale = rows[i][j]
                rows[i] = [x - scale*y for x, y in zip(rows[i], rows[j])]
    return tuple(tuple(row[n:]) for row in rows)


def _encode_matrix(rows):
    return [list(map(str, row)) for row in rows]


def _coordinate_matrix(basis, values):
    """Columns encode the supplied values in the original accepted basis."""
    columns = [basis.coordinates(v) for v in values]
    return [[str(column[i]) for column in columns]
            for i in range(len(basis.originals))]


def _layer_payload(basis, witnesses, probes):
    d = len(basis.originals)
    pivots = tuple(sorted(basis.pivots))
    minor = tuple(tuple(basis.originals[j][i] for j in range(d)) for i in pivots)
    return {
        'dimension': d,
        'basis': [list(map(str, v)) for v in basis.originals],
        'witnesses': [{'word': list(word), 'probe': probe}
                      for word, probe in witnesses],
        'rank_certificate': {'state_indices': list(pivots),
                             'inverse_minor': _encode_matrix(_inverse(minor))},
        'probe_coordinates': {name: list(map(str, basis.coordinates(v)))
                              for name, v in probes.items()},
    }


def compile_one_maintenance(base_operators, maintenance, probes, *,
                            maintenance_label='M', contract=None):
    """Construct W0=inv_old(probes), W1=inv_old(W0 + M W0).

    Every accepted column is a REAL response of a word with at most one M.
    M is applied only to W0; only old updates extend newly accepted columns.
    Consequently the construction respects the paid one-call grammar.
    """
    ops, maint, ps, n = _prepare(base_operators, maintenance, probes, maintenance_label)
    old = close_continuations(ops, ps)
    new = ExactBasis(n)
    witnesses = []
    for value, witness in zip(old.basis.originals, old.witnesses):
        assert new.add(value)
        witnesses.append(witness)
    queue = deque()
    maintenance_attempts = 0
    prefix_attempts = 0
    for value, (word, probe) in zip(old.basis.originals, old.witnesses):
        maintenance_attempts += 1
        candidate = apply(maint, value)
        if new.add(candidate):
            witness = ((maintenance_label,) + word, probe)
            witnesses.append(witness)
            queue.append((candidate, witness))
    while queue:
        value, (word, probe) = queue.popleft()
        for label, q in ops.items():
            prefix_attempts += 1
            candidate = apply(q, value)
            if new.add(candidate):
                witness = ((label,) + word, probe)
                witnesses.append(witness)
                queue.append((candidate, witness))
    old_payload = _layer_payload(old.basis, old.witnesses, ps)
    new_payload = _layer_payload(new, witnesses, ps)
    for payload, basis in ((old_payload, old.basis), (new_payload, new)):
        payload['old_operator_coordinates'] = {
            label: _coordinate_matrix(basis, [apply(q, v) for v in basis.originals])
            for label, q in ops.items()
        }
    return {
        'schema': SCHEMA,
        'contract_sha256': _binding(ops, maint, ps, maintenance_label, contract),
        'state_count': n,
        'old_labels': list(ops),
        'maintenance_label': maintenance_label,
        'old': old_payload,
        'with_maintenance': new_payload,
        'old_embedding': _coordinate_matrix(new, old.basis.originals),
        'maintenance_image': _coordinate_matrix(new,
                                                [apply(maint, v) for v in old.basis.originals]),
        'construction': {
            'old_candidates': old.attempts,
            'old_rank_profile': list(old.profile),
            'maintenance_candidates': maintenance_attempts,
            'old_prefix_candidates_after_maintenance': prefix_attempts,
            'new_independent_coordinates': len(new.originals) - old.dimension,
            'maximum_maintenance_calls_per_witness': max(
                (word.count(maintenance_label) for word, _ in witnesses), default=0),
        },
    }


def _require(condition, message):
    if not condition:
        raise ValueError('invalid signature certificate: ' + message)


def _read_dense(data, rows, columns, path):
    _require(isinstance(data, (tuple, list)) and len(data) == rows, path + ' rows')
    result = []
    for row in data:
        _require(isinstance(row, (tuple, list)) and len(row) == columns, path + ' columns')
        result.append(tuple(F(x) for x in row))
    return tuple(result)


def _action(q, value):
    """Checker arithmetic, independent of closure discovery and coordinates."""
    return tuple(sum((p*value[j] for j, p in row.items()), F(0)) for row in q)


def _combine(basis, coefficients, n):
    _require(len(coefficients) == len(basis), 'coordinate length')
    return tuple(sum((column[i]*coefficient for column, coefficient
                      in zip(basis, coefficients)), F(0)) for i in range(n))


def _check_layer(payload, n, operators, probes, maintenance_label,
                 max_maintenance, max_updates=None):
    d = payload['dimension']
    _require(isinstance(d, int) and 0 <= d <= n, 'dimension')
    basis = _read_dense(payload['basis'], d, n, 'basis')
    witnesses = payload['witnesses']
    _require(len(witnesses) == d, 'witness count')
    for column, witness in zip(basis, witnesses):
        word, probe = tuple(witness['word']), witness['probe']
        _require(probe in probes and all(label in operators for label in word),
                 'unknown witness label')
        _require(word.count(maintenance_label) <= max_maintenance,
                 'witness exceeds maintenance permission')
        if max_updates is not None:
            _require(sum(x != maintenance_label for x in word) <= max_updates,
                     'witness exceeds update horizon')
        actual = probes[probe]
        for label in reversed(word):
            actual = _action(operators[label], actual)
        _require(actual == column, 'witness is not its declared physical response')
    rank = payload['rank_certificate']
    indices = rank['state_indices']
    _require(len(indices) == d and len(set(indices)) == d
             and all(isinstance(i, int) and 0 <= i < n for i in indices),
             'rank minor indices')
    inverse = _read_dense(rank['inverse_minor'], d, d, 'inverse minor')
    minor = tuple(tuple(basis[j][i] for j in range(d)) for i in indices)
    for i in range(d):
        for j in range(d):
            _require(sum((minor[i][k]*inverse[k][j] for k in range(d)), F(0)) == (i == j),
                     'minor right-inverse identity')
            _require(sum((inverse[i][k]*minor[k][j] for k in range(d)), F(0)) == (i == j),
                     'minor left-inverse identity')
    _require(set(payload['probe_coordinates']) == set(probes), 'probe coverage')
    for name, value in probes.items():
        coordinates = tuple(F(x) for x in payload['probe_coordinates'][name])
        _require(_combine(basis, coordinates, n) == value, 'probe representation')
    return basis


def _check_image(target_basis, source_values, encoded, n, path):
    coefficients = _read_dense(encoded, len(target_basis), len(source_values), path)
    for j, value in enumerate(source_values):
        column = tuple(row[j] for row in coefficients)
        _require(_combine(target_basis, column, n) == value, path + ' identity')


def verify_one_maintenance(certificate, base_operators, maintenance, probes, *,
                           maintenance_label='M', contract=None):
    """Check an externally supplied certificate without rediscovering a basis.

    Kernel generation is outside this checker.  A separate raw-event oracle
    must validate that the supplied kernels implement the physical contract.
    """
    ops, maint, ps, n = _prepare(base_operators, maintenance, probes, maintenance_label)
    _require(certificate['schema'] == SCHEMA, 'schema')
    _require(certificate['contract_sha256'] == _binding(ops, maint, ps, maintenance_label, contract),
             'physical contract binding')
    _require(certificate['state_count'] == n, 'state count')
    _require(certificate['old_labels'] == list(ops), 'old update alphabet')
    _require(certificate['maintenance_label'] == maintenance_label, 'maintenance alphabet')
    all_ops = dict(ops, **{maintenance_label: maint})
    old = _check_layer(certificate['old'], n, all_ops, ps, maintenance_label, 0)
    new = _check_layer(certificate['with_maintenance'], n, all_ops, ps, maintenance_label, 1)
    for name, basis in (('old', old), ('with_maintenance', new)):
        coordinates = certificate[name]['old_operator_coordinates']
        _require(set(coordinates) == set(ops), 'old operator coverage')
        for label, q in ops.items():
            _check_image(basis, [_action(q, v) for v in basis], coordinates[label], n,
                         name + ':' + label)
    _check_image(new, old, certificate['old_embedding'], n, 'old embedding')
    _check_image(new, [_action(maint, v) for v in old],
                 certificate['maintenance_image'], n, 'paid maintenance image')
    _require(certificate['construction']['new_independent_coordinates'] == len(new)-len(old),
             'reported dimension increment')
    return True


def signature(certificate, law, *, layer='with_maintenance'):
    """Evaluate a certified linear signature; the law is a design-time object."""
    n = certificate['state_count']
    mu = vector(law)
    if len(mu) != n:
        raise ValueError('law dimension differs')
    columns = [tuple(F(x) for x in row) for row in certificate[layer]['basis']]
    return tuple(sum((a*b for a, b in zip(mu, v)), F(0)) for v in columns)


def separator(certificate, left, right, *, layer='with_maintenance'):
    """Return a retained actual continuation that distinguishes two laws."""
    a, b = signature(certificate, left, layer=layer), signature(certificate, right, layer=layer)
    for x, y, witness in zip(a, b, certificate[layer]['witnesses']):
        if x != y:
            return {'word': list(witness['word']), 'probe': witness['probe'],
                    'left': str(x), 'right': str(y), 'difference': str(y-x)}
    return None


def finite_horizon(base_operators, maintenance, probes, *, max_updates=2,
                   maintenance_label='M', contract=None):
    """Exact signatures for <=h old updates and <=r maintenance calls, r=0,1.

    The horizon counts D/R-like updates.  An M call is an additional clock
    interval, not one of these updates.  This distinction is in the output.
    Construction uses graded bases rather than all operator words.
    """
    ops, maint, ps, n = _prepare(base_operators, maintenance, probes, maintenance_label)
    if not isinstance(max_updates, int) or not 0 <= max_updates <= 100:
        raise ValueError('max_updates must be an integer between zero and 100')
    bases, witnesses, layers = {}, {}, {}
    attempts = 0
    for h in range(max_updates + 1):
        for permission in (0, 1):
            basis = ExactBasis(n)
            retained = []

            def admit(value, witness):
                nonlocal attempts
                attempts += 1
                if basis.add(value):
                    retained.append(witness)

            for name, probe in ps.items():
                admit(probe, ((), name))
            if h:
                child = bases[h-1, permission]
                for label, q in ops.items():
                    for value, (word, probe) in zip(child.originals, witnesses[h-1, permission]):
                        admit(apply(q, value), ((label,) + word, probe))
            if permission:
                child = bases[h, 0]
                for value, (word, probe) in zip(child.originals, witnesses[h, 0]):
                    admit(apply(maint, value), ((maintenance_label,) + word, probe))
            payload = _layer_payload(basis, retained, ps)
            payload['updates_at_most'] = h
            payload['maintenance_calls_at_most'] = permission
            payload['old_images'] = {
                label: _coordinate_matrix(basis,
                    [apply(q, v) for v in bases[h-1, permission].originals])
                for label, q in ops.items()
            } if h else {}
            payload['maintenance_images'] = _coordinate_matrix(basis,
                [apply(maint, v) for v in bases[h, 0].originals]) if permission else None
            bases[h, permission] = basis
            witnesses[h, permission] = retained
            layers[f'{h}:{permission}'] = payload
    return {
        'schema': FINITE_SCHEMA,
        'contract_sha256': _binding(ops, maint, ps, maintenance_label, contract),
        'state_count': n,
        'old_labels': list(ops),
        'maintenance_label': maintenance_label,
        'max_updates': max_updates,
        'horizon_convention': 'old updates <= h; one additional paid M interval when r=1',
        'layers': layers,
        'candidate_evaluations': attempts,
    }


def verify_finite_horizon(certificate, base_operators, maintenance, probes, *,
                          maintenance_label='M', contract=None):
    """Check the graded grammar certificate without search or word enumeration."""
    ops, maint, ps, n = _prepare(base_operators, maintenance, probes, maintenance_label)
    _require(certificate['schema'] == FINITE_SCHEMA, 'finite schema')
    _require(certificate['contract_sha256'] == _binding(ops, maint, ps, maintenance_label, contract),
             'physical contract binding')
    _require(certificate['state_count'] == n and certificate['old_labels'] == list(ops),
             'finite state/alphabet declaration')
    _require(certificate['maintenance_label'] == maintenance_label, 'maintenance alphabet')
    hmax = certificate['max_updates']
    _require(isinstance(hmax, int) and 0 <= hmax <= 100, 'finite horizon')
    expected = {f'{h}:{r}' for h in range(hmax+1) for r in (0, 1)}
    _require(set(certificate['layers']) == expected, 'complete layer coverage')
    all_ops = dict(ops, **{maintenance_label: maint})
    bases = {}
    for h in range(hmax + 1):
        for permission in (0, 1):
            payload = certificate['layers'][f'{h}:{permission}']
            _require(payload['updates_at_most'] == h
                     and payload['maintenance_calls_at_most'] == permission,
                     'layer labels')
            basis = _check_layer(payload, n, all_ops, ps, maintenance_label, permission, h)
            _require(set(payload['old_images']) == (set(ops) if h else set()),
                     'finite update coverage')
            if h:
                for label, q in ops.items():
                    _check_image(basis, [_action(q, v) for v in bases[h-1, permission]],
                                 payload['old_images'][label], n, f'{h}:{permission}:{label}')
            if permission:
                _check_image(basis, [_action(maint, v) for v in bases[h, 0]],
                             payload['maintenance_images'], n, f'{h}:{permission}:maintenance')
            else:
                _require(payload['maintenance_images'] is None, 'unauthorized maintenance edge')
            bases[h, permission] = basis
    return True
