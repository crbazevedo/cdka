"""Exact convex covers of physically generated ordinary preparation histories.

The preparation's fair-source contrast is -x E with x>=0. Ordinary physical
updates transport x by x A_D/R. At each depth, the compiler constructs only
the children of retained actual histories. Every discarded candidate has a
nonnegative rational combination, of total weight one, of the final retained
candidates. Induction preserves the convex hull of all original signatures.

Equality is in the task-sufficient contrast representation. It need not be
equality of full source/register probability laws. Histories remain evaluator
witnesses; their labels do not become controller observations. The cover does
not linearly interpolate informed optima or bound the number of hull vertices.

Optional numerical geometry proposes retained points and convex supports.
Every accepted replacement is recovered exactly. Checking is standard-library
only and never discovers a hull or solves a numerical optimization problem.
"""
from fractions import Fraction as F
from hashlib import sha256
import json

from .program_families import _exact, _rational
from .reachable_restriction import (
    CONTRAST_BASIS, collapse, contrast_signature, expand_contrast,
)
from .semantic_closure import ExactBasis, push


MODEL_SCHEMA = 'cdka.fair-source-preparation-model/v1'
SCHEMA = 'cdka.preparation-convex-cover/v1'
DOMAIN = 'fair source; negative nonnegative E contrast cone; fixed D/R histories'


def _hash(value):
    return sha256(json.dumps(_exact(value), sort_keys=True,
                             separators=(',', ':')).encode()).hexdigest()


def _count(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(name + ' must be a nonnegative integer')
    return value


def _physical_operators(operators):
    if type(operators) is not dict or not {'D', 'R'} <= set(operators):
        raise ValueError('physical D/R operators required')
    checked = {}
    for letter in ('D', 'R'):
        rows = operators[letter]
        if type(rows) not in (list, tuple) or len(rows) != 16:
            raise ValueError('sixteen physical rows required')
        result = []
        for row in rows:
            if (type(row) is not dict or
                    any(type(j) is not int or not 0 <= j < 16 for j in row)):
                raise ValueError('physical row indices')
            parsed = {j: _rational(value) for j, value in row.items()}
            if any(value < 0 for value in parsed.values()) or sum(parsed.values(), F(0)) != 1:
                raise ValueError('stochastic nonnegative physical rows required')
            result.append({j: value for j, value in parsed.items() if value})
        checked[letter] = tuple(result)
    return checked


def _initial_law(law):
    if (type(law) not in (list, tuple) or len(law) != 2 or
            any(type(row) not in (list, tuple) or len(row) != 16 for row in law)):
        raise ValueError('two sixteen-coordinate source submeasures required')
    rows = tuple(tuple(map(_rational, row)) for row in law)
    if any(any(value < 0 for value in row) or sum(row, F(0)) != F(1, 2) for row in rows):
        raise ValueError('nonnegative fair-source submeasures required')
    return rows


def make_preparation_model(operators, initial_law):
    """Validate raw physical inputs and return the shared exact preparation model.

    The physical acquisition mechanism supplying initial_law is an enclosing
    experiment obligation. This function checks the supplied law, fair source,
    task domain and all sixteen-coordinate D/R closure identities. It does not
    treat a dictionary of alleged reduced matrices as a physical certificate.

    Only D/R and the full initial law bind this model. Other continuation
    operators, its terminal observable and program frontier do not affect the
    preparation family and belong to the separate decision binding.
    """
    try:
        physical = _physical_operators(operators)
        law = _initial_law(initial_law)
        offset, signed = contrast_signature(*law)
        initial = tuple(-value for value in signed)
        if offset != F(1, 2) or any(value < 0 for value in initial):
            raise ValueError('initial law outside certified negative contrast cone')
        A = {}
        for letter in ('D', 'R'):
            rows = []
            for basis_row in CONTRAST_BASIS:
                actual = push(basis_row, physical[letter])
                masses = collapse(actual)
                coordinates = tuple(masses[j] for j in (0, 1, 4, 5))
                if expand_contrast(coordinates) != actual:
                    raise ValueError('ordinary physical update leaves the contrast domain')
                if any(value < 0 for value in coordinates):
                    raise ValueError('ordinary contrast cone is not positively invariant')
                rows.append(coordinates)
            A[letter] = tuple(rows)
        digest = _hash({'schema': MODEL_SCHEMA, 'domain': DOMAIN,
                        'operators': physical, 'initial_law': law})
        sparse = {letter: tuple({j: value for j, value in enumerate(row) if value}
                                 for row in rows) for letter, rows in A.items()}
        return {'A': A, 'sparse_A': sparse, 'initial': initial,
                'offset': offset, 'binding': digest}
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed physical preparation model') from error


def preparation_binding(model, h):
    """Bind a checked model to one history length and the convex-cover contract."""
    _count(h, 'history length')
    if (type(model) is not dict or type(model.get('binding')) is not str or
            len(model['binding']) != 64):
        raise ValueError('checked preparation model required')
    return _hash({'schema': SCHEMA, 'model': model['binding'],
                  'history_length': h, 'domain': DOMAIN,
                  'coverage': 'convex hull of signatures of all fixed-length D/R histories'})


def _affine_dimension(points):
    basis = ExactBasis(4)
    for point in points[1:]:
        basis.add(tuple(a-b for a, b in zip(point, points[0])))
    return len(basis.originals)


def _exact_support(points, target, proposed):
    """Recover one proposed convex support in five augmented exact coordinates."""
    basis = ExactBasis(5)
    support = []
    for index in proposed:
        if basis.add((F(1),) + points[index]):
            support.append(index)
    try:
        coefficients = basis.coordinates((F(1),) + target)
    except ValueError:
        return None
    if any(value < 0 for value in coefficients) or sum(coefficients, F(0)) != 1:
        return None
    witness = [(index, weight) for index, weight in zip(support, coefficients) if weight]
    if tuple(sum((weight * points[index][j] for index, weight in witness), F(0))
             for j in range(4)) != target:
        return None
    return witness


def _numeric_cover(points, unique, rank):
    """Numerical proposals only: every missing exact support retains its point."""
    try:
        import numpy as np
        from scipy.optimize import linprog
        from scipy.spatial import ConvexHull, QhullError
    except ImportError as error:
        raise RuntimeError('optional NumPy/SciPy required for nontrivial hull discovery; '
                           'checking and optimize=False need neither') from error

    work = {'lp_calls': 0, 'exact_support_failures': 0, 'lp_failures': 0,
            'geometry_failures': 0}
    unique_points = [points[index] for index in unique]
    # Subtract in exact arithmetic before conversion, so nearby physical
    # points do not disappear merely through floating-point cancellation.
    values = np.array([[float(a-b) for a, b in zip(point, unique_points[0])]
                       for point in unique_points])
    scales = np.max(np.abs(values), axis=0)
    scales = np.where(scales == 0, 1, scales)
    values /= scales
    try:
        _, singular, rotations = np.linalg.svd(values, full_matrices=False)
        if len(singular) < rank or not np.all(np.isfinite(singular[:rank])) or np.any(singular[:rank] <= 0):
            raise ValueError('numerically singular affine coordinates')
        transformed = (values @ rotations[:rank].T) / singular[:rank]
        proposal = ConvexHull(transformed)
        keep = [unique[int(index)] for index in proposal.vertices]
    except (QhullError, np.linalg.LinAlgError, ValueError, FloatingPointError):
        work['geometry_failures'] = 1
        return unique[:], {index: [(index, F(1))] for index in unique}, work

    witnesses = {index: [(index, F(1))] for index in keep}
    numeric_index = {index: i for i, index in enumerate(unique)}
    proposed_count = len(keep)
    for index in unique:
        if index in witnesses:
            continue
        work['lp_calls'] += 1
        numeric = transformed[[numeric_index[i] for i in keep]]
        target = np.concatenate(([1.0], transformed[numeric_index[index]]))
        constraints = np.vstack((np.ones(len(keep)), numeric.T))
        proposal = linprog(np.zeros(len(keep)), A_eq=constraints, b_eq=target,
                           bounds=(0, None), method='highs',
                           options={'primal_feasibility_tolerance': 1e-9,
                                    'dual_feasibility_tolerance': 1e-9})
        witness = None
        if proposal.success:
            support = [keep[i] for i, value in enumerate(proposal.x) if value > 0]
            witness = _exact_support(points, points[index], support)
            if witness is None:
                work['exact_support_failures'] += 1
        else:
            work['lp_failures'] += 1
        if witness is None:
            keep.append(index)
            witness = [(index, F(1))]
        witnesses[index] = witness
    work['proposed_vertices'] = proposed_count
    return keep, witnesses, work


def _discover_cover(candidates, optimize):
    points = [point for _, point in candidates]
    first, unique = {}, []
    for index, point in enumerate(points):
        if point not in first:
            first[point] = index
            unique.append(index)
    rank = _affine_dimension([points[index] for index in unique])
    work = {'distinct_candidates': len(unique), 'affine_dimension': rank,
            'proposed_vertices': len(unique), 'lp_calls': 0,
            'exact_support_failures': 0, 'lp_failures': 0, 'geometry_failures': 0}
    if not optimize or len(unique) <= rank+1:
        keep = unique[:]
        witnesses = {index: [(index, F(1))] for index in unique}
    elif rank == 1:
        coordinate = next(j for j in range(4)
                          if points[unique[0]][j] != points[unique[1]][j])
        low = min(unique, key=lambda index: points[index][coordinate])
        high = max(unique, key=lambda index: points[index][coordinate])
        keep = sorted((low, high))
        witnesses = {}
        denominator = points[high][coordinate] - points[low][coordinate]
        for index in unique:
            weight = (points[index][coordinate] - points[low][coordinate]) / denominator
            witnesses[index] = [(j, value) for j, value in ((low, 1-weight), (high, weight)) if value]
        work['proposed_vertices'] = 2
    else:
        keep, witnesses, numerical_work = _numeric_cover(points, unique, rank)
        work.update(numerical_work)
    keep.sort()
    retained_position = {index: position for position, index in enumerate(keep)}
    cover = [[(retained_position[index], weight)
              for index, weight in witnesses[first[point]]] for point in points]
    work['maximum_support'] = max(map(len, cover))
    return [candidates[index] for index in keep], {'keep': keep, 'cover': cover}, work


def _children(frontier, model):
    return [(history+letter, push(point, model['sparse_A'][letter]))
            for history, point in frontier for letter in ('D', 'R')]


def compile_family(operators, initial_law, h, *, optimize=True):
    """Discover a finite preparation cover and return actual retained histories.

    Returns (frontier, portable_certificate, per_level_statistics). The default
    imports optional numerical packages only when a nontrivial hull proposal
    is needed. Simplexes, duplicate points and affine intervals are handled
    exactly without those packages. optimize=False retains every distinct
    child and is the conservative standard-library control.

    The certificate is independent of continuation K, terminal g, maintenance
    and the ordered program frontier. Reuse still requires the same checked
    physical D/R model, initial full law and preparation horizon.
    """
    _count(h, 'history length')
    if type(optimize) is not bool:
        raise ValueError('optimization flag')
    model = make_preparation_model(operators, initial_law)
    frontier = [('', model['initial'])]
    layers, statistics = [], []
    for depth in range(h+1):
        candidates = _children(frontier, model) if depth else frontier
        frontier, certificate, work = _discover_cover(candidates, optimize)
        layers.append(certificate)
        statistics.append({'h': depth, 'history_candidates': len(candidates),
                           'retained': len(frontier),
                           'histories_never_generated': 2**depth-len(candidates),
                           **work})
    certificate = {'schema': SCHEMA, 'history_length': h,
                   'binding': preparation_binding(model, h),
                   'model_binding': model['binding'], 'layers': _exact(layers)}
    return frontier, certificate, statistics


def _check_cover(candidates, certificate):
    if type(certificate) is not dict or set(certificate) != {'keep', 'cover'}:
        raise ValueError('convex cover object')
    keep = certificate['keep']
    if (type(keep) is not list or not keep or
            any(type(index) is not int or not 0 <= index < len(candidates) for index in keep) or
            len(set(keep)) != len(keep)):
        raise ValueError('distinct kept candidate indices')
    cover = certificate['cover']
    if type(cover) is not list or len(cover) != len(candidates):
        raise ValueError('complete convex candidate coverage required')
    frontier = [candidates[index] for index in keep]
    for (_, target), raw_witness in zip(candidates, cover):
        if type(raw_witness) is not list or not raw_witness:
            raise ValueError('nonempty convex witness required')
        witness, seen = [], set()
        for pair in raw_witness:
            if type(pair) is not list or len(pair) != 2:
                raise ValueError('convex witness pair')
            index, raw_weight = pair
            if type(index) is not int or not 0 <= index < len(frontier) or index in seen:
                raise ValueError('distinct retained witness indices')
            weight = _rational(raw_weight)
            if weight < 0:
                raise ValueError('nonnegative convex coefficient required')
            seen.add(index)
            witness.append((index, weight))
        if sum((weight for _, weight in witness), F(0)) != 1:
            raise ValueError('convex coefficients must sum to one')
        reconstructed = tuple(sum((weight * frontier[index][1][coordinate]
                                   for index, weight in witness), F(0))
                              for coordinate in range(4))
        if reconstructed != target:
            raise ValueError('false convex preparation identity')
    return frontier


def _check_family(certificate, operators, initial_law, h):
    _count(h, 'history length')
    if (type(certificate) is not dict or
            set(certificate) != {'schema', 'history_length', 'binding', 'model_binding', 'layers'}):
        raise ValueError('preparation family certificate object')
    if (certificate['schema'] != SCHEMA or type(certificate['history_length']) is not int or
            certificate['history_length'] != h):
        raise ValueError('preparation family contract')
    model = make_preparation_model(operators, initial_law)
    if (certificate['model_binding'] != model['binding'] or
            certificate['binding'] != preparation_binding(model, h)):
        raise ValueError('preparation model or horizon binding')
    layers = certificate['layers']
    if type(layers) is not list or len(layers) != h+1:
        raise ValueError('complete preparation layer sequence required')
    frontier = [('', model['initial'])]
    for depth, layer in enumerate(layers):
        candidates = _children(frontier, model) if depth else frontier
        frontier = _check_cover(candidates, layer)
    return frontier


def check_family(certificate, operators, initial_law, h):
    """Verify physical preparation inputs and all convex covers without discovery.

    Every returned history is regenerated from the original acquisition label
    and its actual D/R children. Hash binding is checked in addition to, never
    instead of, exact physical transport and convex-combination identities.
    """
    try:
        return _check_family(certificate, operators, initial_law, h)
    except (KeyError, TypeError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise ValueError('malformed preparation-family certificate') from error
