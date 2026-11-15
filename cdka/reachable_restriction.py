"""Exact boundary restriction to exchangeable reachable register laws.

This is a restriction of INPUT distributions, not a claim that the faulty
voter is invariant under all port permutations. D/R preserve this domain;
maintenance generally does not. Queries are therefore propagated through
the full inherited kernel BEFORE averaging at the preparation boundary.
"""
from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from json import dumps
from math import comb

from .boundary_voting import STATES
from .semantic_closure import ExactBasis, dot, matrix, push, word_value

ORBITS = tuple((z, count) for z in (0, 1) for count in range(4))
ORBIT_INDEX = {label: i for i, label in enumerate(ORBITS)}


def collapse(law):
    if len(law) != len(STATES):
        raise ValueError('sixteen register entries required')
    out = [F(0)] * len(ORBITS)
    for weight, (z, bits) in zip(law, STATES):
        out[ORBIT_INDEX[z, sum(bits)]] += F(weight)
    return tuple(out)


def expand(weights):
    if len(weights) != len(ORBITS):
        raise ValueError('eight exchangeable orbit entries required')
    return tuple(F(weights[ORBIT_INDEX[z, sum(bits)]]) / comb(3, sum(bits))
                 for z, bits in STATES)


ORBIT_LAWS = tuple(expand(tuple(F(i == j) for i in range(8))) for j in range(8))


def expand_contrast(weights):
    if len(weights) != 4:
        raise ValueError('four antisymmetric contrast entries required')
    a, b, c, d = map(F, weights)
    return expand((a, b, -b, -a, c, d, -d, -c))


CONTRAST_BASIS = tuple(expand_contrast(tuple(F(i == j) for i in range(4)))
                       for j in range(4))


def contrast_response(response):
    averaged = orbit_response(response)
    return (averaged[0]-averaged[3], averaged[1]-averaged[2],
            averaged[4]-averaged[7], averaged[5]-averaged[6])


def contrast_signature(mu_zero, mu_one):
    signed = tuple(F(b)-F(a) for a, b in zip(mu_zero, mu_one))
    if len(mu_zero) != 16 or len(mu_one) != 16:
        raise ValueError('sixteen entries per source submeasure required')
    masses = collapse(signed)
    four = (masses[0], masses[1], masses[4], masses[5])
    if expand_contrast(four) != signed:
        raise ValueError('contrast is outside the exchangeable antisymmetric domain')
    return sum(map(F, mu_zero), F(0)), four


def contrast_domain_preservation(kernel):
    for index, signed in enumerate(CONTRAST_BASIS):
        actual = push(signed, kernel)
        masses = collapse(actual)
        rebuilt = expand_contrast((masses[0], masses[1], masses[4], masses[5]))
        for state, (a, b) in enumerate(zip(actual, rebuilt)):
            if a != b:
                return {'preserved': False, 'basis_vector': index, 'state': state,
                        'actual': str(a), 'projected': str(b), 'difference': str(a-b)}
    return {'preserved': True}


def is_exchangeable(law):
    return tuple(map(F, law)) == expand(collapse(law))


def orbit_response(response):
    if len(response) != 16:
        raise ValueError('sixteen response entries required')
    return tuple(dot(law, response) for law in ORBIT_LAWS)


def restricted_signature(mu_zero, mu_one):
    """Eight signed orbit masses; H is a hidden target, not a control input."""
    if not is_exchangeable(mu_zero) or not is_exchangeable(mu_one):
        raise ValueError('preparation is outside the certified input domain')
    contrast = tuple(F(b)-F(a) for a, b in zip(mu_zero, mu_one))
    return sum(map(F, mu_zero), F(0)), collapse(contrast)


def query_cache(operators, terminal, words):
    """Compile exact full-kernel responses and their initial-domain restriction."""
    full = tuple(word_value(operators, w, terminal) for w in words)
    return {'full': full, 'restricted': tuple(orbit_response(v) for v in full),
            'contrast': tuple(contrast_response(v) for v in full)}


def restricted_value(signature, response):
    mass_zero, contrast = signature
    if len(contrast) != 8 or len(response) != 8:
        raise ValueError('eight boundary coordinates required')
    return F(mass_zero) + dot(contrast, response)


def contrast_value(signature, response):
    mass_zero, signed = signature
    if len(signed) != 4 or len(response) != 4:
        raise ValueError('four contrast boundary coordinates required')
    return F(mass_zero) + dot(signed, response)


def projected_kernel(kernel):
    """Q K A. Safe forward propagation requires the separate Q K = Q K A Q check."""
    return matrix([{j: p for j, p in enumerate(collapse(push(q, kernel))) if p}
                   for q in ORBIT_LAWS])


def domain_preservation(kernel):
    """Exact witness when pushing an exchangeable law leaves the domain."""
    for index, law in enumerate(ORBIT_LAWS):
        actual = push(law, kernel)
        projected = expand(collapse(actual))
        for state, (a, b) in enumerate(zip(actual, projected)):
            if a != b:
                return {'preserved': False, 'orbit': index, 'state': state,
                        'actual': str(a), 'projected': str(b),
                        'difference': str(a-b)}
    return {'preserved': True}


def _inverse(rows):
    n = len(rows)
    a = [list(map(F, row)) + [F(i == j) for j in range(n)]
         for i, row in enumerate(rows)]
    if any(len(row) != 2*n for row in a):
        raise ValueError('square matrix required')
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            raise ValueError('singular restricted basis')
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x/scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[j])]
    return tuple(tuple(row[n:]) for row in a)


def _binding(old_basis, contract, domain='exchangeable'):
    payload = {'old_basis': [[str(F(x)) for x in v] for v in old_basis],
               'orbits': ORBITS, 'domain': domain, 'contract': contract}
    return sha256(dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def compile_old_restriction(old_basis, *, contract=None):
    """Prove that old responses already identify every exchangeable input law."""
    basis = ExactBasis(8)
    selected = []
    for i, response in enumerate(old_basis):
        if basis.add(orbit_response(response)):
            selected.append(i)
    if len(selected) != 8:
        raise ValueError('old responses do not separate the whole input domain')
    columns = [orbit_response(old_basis[i]) for i in selected]
    rows = tuple(tuple(column[i] for column in columns) for i in range(8))
    return {'schema': 'cdka.exchangeable-boundary/v1',
            'binding': _binding(old_basis, contract),
            'dimension': 8, 'old_indices': selected,
            'inverse': [[str(x) for x in row] for row in _inverse(rows)]}


def compile_contrast_restriction(old_basis, *, contract=None):
    basis = ExactBasis(4)
    selected = []
    for i, response in enumerate(old_basis):
        if basis.add(contrast_response(response)):
            selected.append(i)
    if len(selected) != 4:
        raise ValueError('old responses do not identify the contrast domain')
    columns = [contrast_response(old_basis[i]) for i in selected]
    rows = tuple(tuple(column[i] for column in columns) for i in range(4))
    return {'schema': 'cdka.antisymmetric-contrast-boundary/v1',
            'binding': _binding(old_basis, contract, 'antisymmetric contrast'),
            'dimension': 4, 'old_indices': selected,
            'inverse': [[str(x) for x in row] for row in _inverse(rows)]}


def verify_contrast_restriction(certificate, old_basis, *, contract=None):
    try:
        if certificate['schema'] != 'cdka.antisymmetric-contrast-boundary/v1':
            raise ValueError('schema')
        if certificate['binding'] != _binding(old_basis, contract, 'antisymmetric contrast'):
            raise ValueError('binding')
        selected = certificate['old_indices']
        if (certificate['dimension'] != 4 or len(selected) != 4 or
                len(set(selected)) != 4 or
                any(type(i) is not int or not 0 <= i < len(old_basis) for i in selected)):
            raise ValueError('basis indices')
        inverse = tuple(tuple(map(F, row)) for row in certificate['inverse'])
        if len(inverse) != 4 or any(len(row) != 4 for row in inverse):
            raise ValueError('inverse shape')
        columns = [contrast_response(old_basis[i]) for i in selected]
        for i in range(4):
            for j in range(4):
                if sum((columns[k][i]*inverse[k][j] for k in range(4)),F(0)) != F(i == j):
                    raise ValueError('inverse identity')
    except (KeyError,TypeError,IndexError,ZeroDivisionError) as error:
        raise ValueError('malformed contrast restriction certificate') from error
    return True


def verify_old_restriction(certificate, old_basis, *, contract=None):
    """Check a supplied inverse; no rank discovery or elimination is performed."""
    try:
        if certificate['schema'] != 'cdka.exchangeable-boundary/v1':
            raise ValueError('schema')
        if certificate['binding'] != _binding(old_basis, contract):
            raise ValueError('binding')
        selected = certificate['old_indices']
        if (certificate['dimension'] != 8 or len(selected) != 8 or
                len(set(selected)) != 8 or
                any(type(i) is not int or not 0 <= i < len(old_basis) for i in selected)):
            raise ValueError('basis indices')
        inverse = tuple(tuple(map(F, row)) for row in certificate['inverse'])
        if len(inverse) != 8 or any(len(row) != 8 for row in inverse):
            raise ValueError('inverse shape')
        columns = [orbit_response(old_basis[i]) for i in selected]
        for i in range(8):
            for j in range(8):
                value = sum((columns[k][i]*inverse[k][j] for k in range(8)), F(0))
                if value != F(i == j):
                    raise ValueError('inverse identity')
    except (KeyError, TypeError, IndexError, ZeroDivisionError) as error:
        raise ValueError('malformed restriction certificate') from error
    return True
