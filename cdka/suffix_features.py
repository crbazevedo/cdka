"""Exact signed dual features for ordinary suffixes before one maintenance step.

The eight rows C are physical sixteen-coordinate linear functionals, not eight
states. A supplied certificate proves C K_a = T_a C for a in {D,R}, E = U C,
and E K_M = V C. Thus an ordinary suffix q can be propagated as z = C q and
cross the maintenance boundary as V z without assuming four-dimensional M
closure. T_a may have negative coefficients. Only their E-to-E blocks A_a
are required to be nonnegative for the existing outer program-family order.

The feature-family ablation keeps every ordinary suffix and changes only its
algebra from sixteen coordinates to eight. It uses the same grammar and the
same positive four-coordinate outer cover as program_families.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json

from .program_families import _cover, _check_cover
from .reachable_restriction import CONTRAST_BASIS
from .semantic_closure import ExactBasis, dot, push


SCHEMA = 'cdka.suffix_features.v1'
FAMILY_SCHEMA = 'cdka.feature-program-cover/v1'


def _walsh(subset):
    return tuple(F((-1)**sum(bits[j] for j in subset), 8)
                 for bits in product((0, 1), repeat=3))


def _fixed_basis():
    w0, w1, w2 = (_walsh((j,)) for j in range(3))
    extras = (
        _walsh(()),
        tuple(a-(b+c)/2 for a, b, c in zip(w0, w1, w2)),
        tuple(a+b for a, b in zip(_walsh((0, 1)), _walsh((0, 2)))),
        _walsh((1, 2)),
    )
    return CONTRAST_BASIS + tuple(row+tuple(-x for x in row) for row in extras)


# Independent of repair success, including success zero. Physical state order
# is health first, followed by the lexicographic three-bit register order.
FEATURE_BASIS = _fixed_basis()


def _rational(value):
    if type(value) is F:
        return value
    if type(value) is int:
        return F(value)
    if type(value) is str:
        try:
            result = F(value)
        except (ValueError, ZeroDivisionError) as error:
            raise ValueError('invalid exact rational') from error
        if str(result) != value:
            raise ValueError('noncanonical exact rational')
        return result
    raise ValueError('exact rational required; float/bool forbidden')


def _exact(value):
    if type(value) is F:
        return str(value)
    if type(value) is dict:
        return {str(k): _exact(v) for k, v in value.items()}
    if type(value) in (list, tuple):
        return [_exact(v) for v in value]
    return value


def _model(operators, terminal):
    """Validate and canonicalize the physical inputs before hashing or algebra."""
    if type(operators) is not dict or set(operators) != {'D', 'R', 'M'}:
        raise ValueError('D/R/M physical operators required')
    checked = {}
    for label in ('D', 'R', 'M'):
        rows = operators[label]
        if type(rows) not in (tuple, list) or len(rows) != 16:
            raise ValueError('sixteen physical rows required')
        result = []
        for row in rows:
            if type(row) is not dict or any(type(j) is not int or not 0 <= j < 16 for j in row):
                raise ValueError('physical row indices')
            parsed = {j: _rational(value) for j, value in row.items()}
            if any(value < 0 for value in parsed.values()) or sum(parsed.values(), F(0)) > 1:
                raise ValueError('nonnegative substochastic physical rows required')
            result.append({j: value for j, value in parsed.items() if value})
        checked[label] = tuple(result)
    if type(terminal) not in (tuple, list) or len(terminal) != 16:
        raise ValueError('sixteen-coordinate terminal required')
    return checked, tuple(map(_rational, terminal))


def _binding(operators, terminal):
    payload = {'schema': SCHEMA, 'operators': operators, 'terminal': terminal,
               'physical_basis': FEATURE_BASIS}
    return sha256(json.dumps(_exact(payload), sort_keys=True,
                             separators=(',', ':')).encode()).hexdigest()


def _sparse(rows):
    return tuple({j: x for j, x in enumerate(row) if x} for row in rows)


def action(rows, vector):
    """Apply already-checked sparse signed rows; rectangular maps are allowed."""
    return tuple(sum((value*vector[j] for j, value in row.items()), F(0)) for row in rows)


def _mixture(coefficients, basis):
    return tuple(sum((coefficient*basis[j][i]
                      for j, coefficient in enumerate(coefficients) if coefficient), F(0))
                 for i in range(16))


def _positive_outer(T):
    result = {}
    for label in ('D', 'R'):
        rows = T[label][:4]
        if any(any(row[4:]) or any(value < 0 for value in row[:4]) for row in rows):
            raise ValueError('ordinary positive contrast cone not invariant')
        result[label] = _sparse(tuple(row[:4] for row in rows))
    return result


def compile_features(operators, terminal):
    """Discover exact coefficients in the fixed basis; return a portable proof.

    Construction uses rational row reduction. check_features instead verifies
    the supplied physical identities directly and does not rerun discovery.
    """
    operators, terminal = _model(operators, terminal)
    basis = ExactBasis(16)
    for row in FEATURE_BASIS:
        if not basis.add(row):
            raise ValueError('fixed feature basis must be independent')
    T = {label: tuple(basis.coordinates(push(row, operators[label])) for row in FEATURE_BASIS)
         for label in ('D', 'R')}
    _positive_outer(T)
    U = tuple(basis.coordinates(row) for row in CONTRAST_BASIS)
    V = tuple(basis.coordinates(push(row, operators['M'])) for row in CONTRAST_BASIS)
    z = tuple(dot(row, terminal) for row in FEATURE_BASIS)
    return {'schema': SCHEMA, 'binding': _binding(operators, terminal),
            'C': _exact(FEATURE_BASIS), 'T': _exact(T),
            'U': _exact(U), 'V': _exact(V), 'z': _exact(z)}


def _dense(rows, height, width):
    if (type(rows) is not list or len(rows) != height or
            any(type(row) is not list or len(row) != width for row in rows)):
        raise ValueError('feature matrix shape')
    return tuple(tuple(map(_rational, row)) for row in rows)


def _check_features(certificate, operators, terminal):
    if (type(certificate) is not dict or
            set(certificate) != {'schema', 'binding', 'C', 'T', 'U', 'V', 'z'}):
        raise ValueError('feature certificate object')
    operators, terminal = _model(operators, terminal)
    if certificate['schema'] != SCHEMA or certificate['binding'] != _binding(operators, terminal):
        raise ValueError('feature contract or binding')
    C = _dense(certificate['C'], 8, 16)
    if C != FEATURE_BASIS:
        raise ValueError('fixed physical feature basis')
    supplied = certificate['T']
    if type(supplied) is not dict or set(supplied) != {'D', 'R'}:
        raise ValueError('ordinary feature transports')
    T = {label: _dense(supplied[label], 8, 8) for label in ('D', 'R')}
    U, V = (_dense(certificate[key], 4, 8) for key in ('U', 'V'))
    if type(certificate['z']) is not list or len(certificate['z']) != 8:
        raise ValueError('terminal feature shape')
    z = tuple(map(_rational, certificate['z']))
    for label in ('D', 'R'):
        for row, coefficients in zip(C, T[label]):
            if push(row, operators[label]) != _mixture(coefficients, C):
                raise ValueError('false ordinary feature closure')
    for row, u, v in zip(CONTRAST_BASIS, U, V):
        if row != _mixture(u, C):
            raise ValueError('false contrast extraction')
        if push(row, operators['M']) != _mixture(v, C):
            raise ValueError('false maintenance boundary')
    if z != tuple(dot(row, terminal) for row in C):
        raise ValueError('false terminal feature contraction')
    A = _positive_outer(T)
    return {'C': C, 'T': {label: _sparse(rows) for label, rows in T.items()},
            'U': _sparse(U), 'V': _sparse(V), 'z': z,
            'A': A, 'binding': certificate['binding']}


def check_features(certificate, operators, terminal):
    """Check full sixteen-coordinate identities; return exact sparse features.

    No stochastic meaning is assigned to the eight signed features. The
    physical D/R/M kernels and terminal observable are all digest-bound.
    """
    try:
        return _check_features(certificate, operators, terminal)
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed suffix-feature certificate') from error


def _family_binding(feature_binding, k):
    payload = {'features': feature_binding, 'ordinary_updates': k,
               'schema': FAMILY_SCHEMA,
               'grammar': 'exactly k D/R updates, at most one additional M',
               'domain': 'negative nonnegative cone in CONTRAST_BASIS; common mass offset'}
    return sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _candidates(n, suffixes, frontier, features):
    seeds = [('M'+word, action(features['V'], q)) for word, q in suffixes]
    if n == 0:
        return [('', action(features['U'], features['z']))] + seeds
    return [(label+word, action(features['A'][label], q))
            for word, q in frontier for label in ('D', 'R')] + seeds


def compile_feature_family(operators, terminal, k, *, feature_certificate=None, prune=True):
    """Parent-family ablation with all 2**k suffixes evaluated in shared 8D.

    A supplied feature_certificate is reused, checked and embedded. Its
    construction cost must be included once when comparing complete pipelines.
    """
    if type(k) is not int or k < 0:
        raise ValueError('ordinary updates')
    if type(prune) is not bool:
        raise ValueError('pruning flag')
    if feature_certificate is None:
        feature_certificate = compile_features(operators, terminal)
    features = check_features(feature_certificate, operators, terminal)
    suffixes = [('', features['z'])]
    frontier, layers, stats = [], [], []
    for n in range(k+1):
        if n:
            suffixes = [(label+word, action(features['T'][label], q))
                        for word, q in suffixes for label in ('D', 'R')]
        candidates = _candidates(n, suffixes, frontier, features)
        frontier, layer = _cover(candidates, prune)
        layers.append(layer)
        evaluated = {word for word, _ in candidates} | {word for word, _ in suffixes}
        stats.append({'n': n, 'no_m_suffixes': len(suffixes), 'candidates': len(candidates),
                      'retained': len(frontier), 'complete_words_generated': len(evaluated),
                      'complete_words_never_generated': (n+2)*2**n-len(evaluated)})
    certificate = {'schema': FAMILY_SCHEMA, 'ordinary_updates': k,
                   'binding': _family_binding(features['binding'], k),
                   'features': feature_certificate, 'layers': layers}
    return frontier, certificate, stats


def _check_feature_family(certificate, operators, terminal, k):
    if type(k) is not int or k < 0:
        raise ValueError('ordinary updates')
    if (type(certificate) is not dict or
            set(certificate) != {'schema', 'ordinary_updates', 'binding', 'features', 'layers'}):
        raise ValueError('feature-family certificate object')
    if (certificate['schema'] != FAMILY_SCHEMA or type(certificate['ordinary_updates']) is not int or
            certificate['ordinary_updates'] != k):
        raise ValueError('feature-family contract')
    features = check_features(certificate['features'], operators, terminal)
    if certificate['binding'] != _family_binding(features['binding'], k):
        raise ValueError('feature-family binding')
    layers = certificate['layers']
    if type(layers) is not list or len(layers) != k+1:
        raise ValueError('feature-family layers')
    suffixes, frontier = [('', features['z'])], []
    for n, layer in enumerate(layers):
        if type(layer) is not dict or set(layer) != {'keep', 'cover'}:
            raise ValueError('feature-family cover layer')
        if n:
            suffixes = [(label+word, action(features['T'][label], q))
                        for word, q in suffixes for label in ('D', 'R')]
        candidates = _candidates(n, suffixes, frontier, features)
        frontier = _check_cover(candidates, layer)
    return frontier


def check_feature_family(certificate, operators, terminal, k):
    """Verify the feature proof and supplied cover; never rediscover a frontier."""
    try:
        return _check_feature_family(certificate, operators, terminal, k)
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed feature-family certificate') from error
