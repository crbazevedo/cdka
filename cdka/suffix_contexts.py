"""Exact finite-horizon context covers for no-maintenance suffixes.

The checked feature map is a dual response evaluator, not a physical quotient.
Its D/R matrices may be signed.  Therefore coordinatewise order on those
features is not used.  A nested sequence of rational row cones supplies the
order: C_t T_a is contained in cone(C_(t+1)), and C_0 contains the rows of U
and V (the physical E and E M boundaries).  At suffix length n, a cover under
C_(k-n) may replace each candidate by one retained executable suffix.

Positive combinations below certify CONTEXT identities.  They never create a
mixture of controllers.  Every suffix and complete-program representative is
an original word with the same ordinary-update count and at most one M.

Only cone discovery optionally imports NumPy/SciPy.  The certificate checker
uses standard-library exact arithmetic and does not search for cones or
Pareto frontiers.  No polynomial bound on the number of context rays is claimed.
"""
from fractions import Fraction as F

from .program_families import _check_cover, _cover, _exact, _rational, binding
from .semantic_closure import ExactBasis, dot, push
from .suffix_features import action, check_features, compile_features


SCHEMA = 'cdka.finite-suffix-context-cover/v1'
_CONE_KEYS = {'rows', 'counts', 'initial', 'transitions'}
_COVER_KEYS = {'keep', 'cover'}


def _dense(rows, width):
    return tuple(tuple(row.get(j, F(0)) for j in range(width)) for row in rows)


def _combination(rows, witness, width):
    return tuple(sum((c * rows[j][i] for j, c in witness), F(0))
                 for i in range(width))


class _ConeDiscovery:
    """Numerical support proposals are accepted only after exact reconstruction."""

    def __init__(self, features, optimize):
        self.width = len(features['z'])
        self.operators = features['T']
        self.starts = _dense(features['U'], self.width) + _dense(features['V'], self.width)
        self.rows = []
        self.numeric_rows = []
        self.index = {}
        self.lp_calls = 0
        self.exact_support_failures = 0
        self.maximum_support_size = 0
        self.optimize = optimize
        if optimize:
            try:
                import numpy as np
                from scipy.optimize import linprog
            except ImportError as error:
                raise RuntimeError('optional NumPy/SciPy required for cone discovery; '
                                   'checking an existing certificate needs neither') from error
            self.np = np
            self.linprog = linprog

    def _membership(self, row):
        if not self.optimize or not self.rows:
            return None
        self.lp_calls += 1
        np = self.np
        rhs = np.array(row, dtype=float)
        matrix = np.array(self.numeric_rows, dtype=float).T
        scales = np.maximum(np.max(np.abs(matrix), axis=1), np.abs(rhs))
        scales = np.where(scales == 0, 1, scales)
        result = self.linprog(
            np.ones(len(self.rows)), A_eq=matrix / scales[:, None],
            b_eq=rhs / scales, bounds=(0, None), method='highs',
            options={'primal_feasibility_tolerance': 1e-9,
                     'dual_feasibility_tolerance': 1e-9})
        if not result.success:
            return None
        basis = ExactBasis(self.width)
        support = []
        for i, coefficient in enumerate(result.x):
            if coefficient > 0 and basis.add(self.rows[i]):
                support.append(i)
        try:
            coefficients = basis.coordinates(row)
        except ValueError:
            coefficients = None
        if coefficients is not None and all(c >= 0 for c in coefficients):
            witness = [(i, c) for i, c in zip(support, coefficients) if c]
            if _combination(self.rows, witness, self.width) == row:
                self.maximum_support_size = max(self.maximum_support_size, len(witness))
                return witness
        # Failed numerical guidance only enlarges the cone representation.
        self.exact_support_failures += 1
        return None

    def add(self, row):
        row = tuple(row)
        scale = max(map(abs, row), default=F(0))
        if not scale:
            return []
        normal = tuple(x / scale for x in row)
        if normal in self.index:
            return [(self.index[normal], scale)]
        witness = self._membership(normal)
        if witness is None:
            index = len(self.rows)
            self.rows.append(normal)
            self.numeric_rows.append([float(x) for x in normal])
            self.index[normal] = index
            witness = [(index, F(1))]
        return [(i, c * scale) for i, c in witness]

    def build(self, depth):
        initial = [self.add(row) for row in self.starts]
        counts = [len(self.rows)]
        transitions = []
        processed = 0
        for _ in range(depth):
            previous = counts[-1]
            for i in range(processed, previous):
                transitions.append({a: self.add(push(self.rows[i], self.operators[a]))
                                    for a in ('D', 'R')})
            processed = previous
            counts.append(len(self.rows))
        certificate = _exact({'rows': self.rows, 'counts': counts,
                              'initial': initial, 'transitions': transitions})
        stats = {'feature_dimension': self.width, 'context_rows': len(self.rows),
                 'context_rows_by_depth': counts, 'lp_calls': self.lp_calls,
                 'exact_support_failures': self.exact_support_failures,
                 'maximum_support_size': self.maximum_support_size,
                 'optimized': self.optimize}
        return certificate, stats


def discover_cone(features, depth, *, optimize=True):
    """Build nested contexts from parsed, physically checked features.

    The default discovers small conic representations with an optional LP
    solver, then checks each proposed support with rational arithmetic.  The
    conservative optimize=False control retains every new normalized row and
    requires no third-party packages; it has no context-count speed claim.
    Cost measurements must include discovery and the optional cold imports.
    """
    if type(depth) is not int or depth < 0:
        raise ValueError('context depth')
    if type(optimize) is not bool:
        raise ValueError('optimization flag')
    return _ConeDiscovery(features, optimize).build(depth)


def _parse_cone(certificate, features, depth):
    if type(certificate) is not dict or set(certificate) != _CONE_KEYS:
        raise ValueError('context cone object')
    width = len(features['z'])
    raw_rows = certificate['rows']
    if (type(raw_rows) is not list or not raw_rows or
            any(type(row) is not list or len(row) != width for row in raw_rows)):
        raise ValueError('nonempty context rows of feature dimension required')
    rows = tuple(tuple(map(_rational, row)) for row in raw_rows)
    if any(not any(row) for row in rows):
        raise ValueError('zero context generator')
    counts = certificate['counts']
    if (type(counts) is not list or len(counts) != depth + 1 or
            any(type(n) is not int or not 0 < n <= len(rows) for n in counts) or
            any(b < a for a, b in zip(counts, counts[1:])) or counts[-1] != len(rows)):
        raise ValueError('positive nested context counts')

    def witness(raw, limit):
        if type(raw) is not list:
            raise ValueError('context witness list')
        result = []
        for pair in raw:
            if type(pair) is not list or len(pair) != 2:
                raise ValueError('context witness pair')
            index, value = pair
            coefficient = _rational(value)
            if type(index) is not int or not 0 <= index < limit or coefficient < 0:
                raise ValueError('nonnegative context coefficient and in-cone index required')
            result.append((index, coefficient))
        return tuple(result)

    raw_initial = certificate['initial']
    # An empty or truncated list must never turn required identities into a
    # vacuous zip.  There are four E rows and four E M boundary rows.
    if type(raw_initial) is not list or len(raw_initial) != 8:
        raise ValueError('exactly eight initial context witnesses required')
    initial = tuple(witness(raw, counts[0]) for raw in raw_initial)
    raw_transitions = certificate['transitions']
    expected = counts[-2] if depth else 0
    if type(raw_transitions) is not list or len(raw_transitions) != expected:
        raise ValueError('context transition count')
    transitions = []
    for i, raw in enumerate(raw_transitions):
        if type(raw) is not dict or set(raw) != {'D', 'R'}:
            raise ValueError('context transition letters')
        birth = next(t for t, size in enumerate(counts) if i < size)
        transitions.append({a: witness(raw[a], counts[birth + 1]) for a in ('D', 'R')})
    return {'rows': rows, 'counts': tuple(counts), 'initial': initial,
            'transitions': tuple(transitions)}


def check_cone(certificate, features, depth):
    """Check supplied finite closure identities in the verified feature basis.

    features must be the parsed output of check_features.  The public family
    checker establishes that obligation itself.  Empty witnesses are allowed
    only when the exact target row is zero; empty cones are always rejected.
    """
    try:
        if type(depth) is not int or depth < 0:
            raise ValueError('context depth')
        cone = _parse_cone(certificate, features, depth)
        rows = cone['rows']
        width = len(features['z'])
        starts = _dense(features['U'], width) + _dense(features['V'], width)
        for i in range(8):
            if _combination(rows, cone['initial'][i], width) != starts[i]:
                raise ValueError('false initial context identity')
        for i, witnesses in enumerate(cone['transitions']):
            for a in ('D', 'R'):
                target = push(rows[i], features['T'][a])
                if _combination(rows, witnesses[a], width) != target:
                    raise ValueError('false context transition identity')
        return cone
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError,
            StopIteration) as error:
        raise ValueError('malformed finite context certificate') from error


def _layer_candidates(n, k, suffix, frontier, features, cone):
    if n:
        suffix_candidates = [(a + word, action(features['T'][a], response))
                             for word, response in suffix for a in ('D', 'R')]
        contexts = cone['rows'][:cone['counts'][k - n]]
        context_responses = [(word, tuple(dot(row, response) for row in contexts))
                             for word, response in suffix_candidates]
    else:
        suffix_candidates = suffix
        context_responses = suffix
    return suffix_candidates, context_responses


def _front_candidates(n, suffix, frontier, features):
    seeds = [('M' + word, action(features['V'], response)) for word, response in suffix]
    if n == 0:
        return [('', action(features['U'], features['z']))] + seeds
    return [(a + word, action(features['A'][a], response))
            for word, response in frontier for a in ('D', 'R')] + seeds


def compile_family(operators, terminal, k, *, feature_certificate=None,
                   cone_certificate=None, optimize=True):
    """Discover an exact suffix/program cover and a self-contained certificate.

    A supplied cone is checked before use.  Otherwise cone discovery is part
    of this call, including any first optional-dependency import.  The result
    covers the same reserved-resource response objectives as program_families:
    one optimum, informed values, minimax/maximin and joint feasibility; not
    all ties, prediction envelopes, or actual execution-cost Pareto tradeoffs.
    """
    if type(k) is not int or k < 0:
        raise ValueError('ordinary updates')
    if type(optimize) is not bool:
        raise ValueError('optimization flag')
    if feature_certificate is None:
        feature_certificate = compile_features(operators, terminal)
    features = check_features(feature_certificate, operators, terminal)
    depth = max(0, k - 1)
    if cone_certificate is None:
        cone_certificate, cone_stats = discover_cone(features, depth, optimize=optimize)
        cone = _parse_cone(cone_certificate, features, depth)
    else:
        cone = check_cone(cone_certificate, features, depth)
        cone_stats = {'supplied': True, 'context_rows': len(cone['rows']),
                      'context_rows_by_depth': list(cone['counts'])}
    suffix = [('', features['z'])]
    frontier = []
    layers = []
    stats = []
    for n in range(k + 1):
        candidates, responses = _layer_candidates(n, k, suffix, frontier, features, cone)
        _, suffix_cover = _cover(responses)
        suffix = [candidates[i] for i in suffix_cover['keep']]
        complete = _front_candidates(n, suffix, frontier, features)
        frontier, front_cover = _cover(complete)
        layers.append({'suffix': suffix_cover, 'front': front_cover})
        generated = len({word for word, _ in candidates} | {word for word, _ in complete})
        stats.append({'n': n, 'no_m_suffix_candidates': len(candidates),
                      'no_m_suffixes_retained': len(suffix),
                      'no_m_suffixes_never_generated': 2 ** n - len(candidates),
                      'context_rows_used': cone['counts'][k - n] if n else 0,
                      'candidates': len(complete), 'retained': len(frontier),
                      'complete_words_generated': generated,
                      'complete_words_never_generated': (n + 2) * 2 ** n - generated})
    certificate = {'schema': SCHEMA, 'ordinary_updates': k,
                   'binding': binding(operators, terminal, k),
                   'features': feature_certificate, 'cone': cone_certificate,
                   'layers': layers}
    return frontier, certificate, {'cone': cone_stats, 'layers': stats}


def _check_family(certificate, operators, terminal, k):
    if type(k) is not int or k < 0:
        raise ValueError('ordinary updates')
    if (type(certificate) is not dict or
            set(certificate) != {'schema', 'ordinary_updates', 'binding', 'features', 'cone', 'layers'}):
        raise ValueError('suffix family certificate object')
    if (certificate['schema'] != SCHEMA or type(certificate['ordinary_updates']) is not int or
            certificate['ordinary_updates'] != k):
        raise ValueError('suffix family contract')
    if certificate['binding'] != binding(operators, terminal, k):
        raise ValueError('suffix family binding')
    features = check_features(certificate['features'], operators, terminal)
    cone = check_cone(certificate['cone'], features, max(0, k - 1))
    layers = certificate['layers']
    if type(layers) is not list or len(layers) != k + 1:
        raise ValueError('suffix family layer count')
    suffix = [('', features['z'])]
    frontier = []
    for n, layer in enumerate(layers):
        if type(layer) is not dict or set(layer) != {'suffix', 'front'}:
            raise ValueError('suffix family layer')
        for level in (layer['suffix'], layer['front']):
            if type(level) is not dict or set(level) != _COVER_KEYS:
                raise ValueError('suffix family cover')
        candidates, responses = _layer_candidates(n, k, suffix, frontier, features, cone)
        _check_cover(responses, layer['suffix'])
        suffix = [candidates[i] for i in layer['suffix']['keep']]
        frontier = _check_cover(_front_candidates(n, suffix, frontier, features), layer['front'])
    return frontier


def check_family(certificate, operators, terminal, k):
    """Verify physical closure, finite contexts and coverage without discovery."""
    try:
        return _check_family(certificate, operators, terminal, k)
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError,
            StopIteration) as error:
        raise ValueError('malformed suffix-family certificate') from error
