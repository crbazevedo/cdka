"""Exact finite continuation audits after a physical resource transition changes.

Inputs are already compiled joint physical kernels. This module does not prove
observation access, shared-noise fidelity, program completeness, or pathwise
affordability. Row kernels are substochastic on live states; reward vectors
include charges incurred on failed branches. No survivor normalization occurs.

The finite audit also supports an explicit terminal stage and different paid
startup laws. Exact all-horizon response equality is a separate, opt-in Krylov
closure check. It makes no all-horizon cost-inequality or low-rank promise.
"""

from fractions import Fraction as F
from typing import Mapping


def _rational(value, name="value"):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError(name + " must be an int or Fraction, not a float")
    return F(value)


def _vector(values, size, name, default=0):
    if values is None:
        return (F(default),) * size
    result = tuple(_rational(x, name) for x in values)
    if len(result) != size:
        raise ValueError(name + " has the wrong length")
    return result


def _cost(values, size, name):
    result = _vector(values, size, name)
    if any(x < 0 for x in result):
        raise ValueError(name + " must be nonnegative incurred charges")
    return result


def _law(values, size, name):
    result = _vector(values, size, name)
    if any(x < 0 for x in result) or sum(result, F(0)) > 1:
        raise ValueError(name + " must be an unnormalized live subprobability")
    return result


def sparse_kernel(rows):
    """Validate indexed sparse live rows and copy them to exact rational rows.

    Death is the missing row mass, not an extra destination index. Empty rows
    are valid. The matrix itself must have a nonempty, explicitly ordered state
    domain. Float inputs are rejected rather than silently rationalized.
    """
    rows = tuple(rows)
    if not rows:
        raise ValueError("a nonempty finite state domain is required")
    size = len(rows)
    result = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise TypeError("each sparse row must map column indices to mass")
        clean = {}
        for j, value in row.items():
            if type(j) is not int or not 0 <= j < size:
                raise ValueError("destination index is outside the common state domain")
            mass = _rational(value, "transition mass")
            if mass < 0:
                raise ValueError("negative transition mass")
            if mass:
                clean[j] = mass
        if sum(clean.values(), F(0)) > 1:
            raise ValueError("live kernel is not substochastic")
        result.append(clean)
    return tuple(result)


def index_sparse(rows, states=None):
    """Adapt labelled rows to (indexed rows, ordered states, index mapping).

    Every declared source row and every nonzero destination must be present.
    Silently dropping successors would change the continuation problem.
    """
    if not isinstance(rows, Mapping):
        raise TypeError("labelled rows must be a mapping")
    states = tuple(rows) if states is None else tuple(states)
    if not states or len(set(states)) != len(states):
        raise ValueError("states must be nonempty and distinct")
    index = {state: i for i, state in enumerate(states)}
    if set(rows) != set(index):
        raise ValueError("every declared source row must be supplied exactly once")
    result = []
    for state in states:
        row = {}
        for destination, mass in rows[state].items():
            mass = _rational(mass, "transition mass")
            if mass and destination not in index:
                raise ValueError("successor is outside the declared state domain")
            if mass:
                row[index[destination]] = mass
        result.append(row)
    return sparse_kernel(result), states, index


def index_vector(values, states, default=None):
    """Order a labelled vector; missing values need an explicit default.

    Use ``default=0`` for a sparse initial live law. Requiring explicit reward
    entries by default prevents a missing failed-prefix charge becoming free.
    """
    states = tuple(states)
    if not isinstance(values, Mapping) or set(values) - set(states):
        raise ValueError("vector has labels outside the declared state domain")
    if default is None and any(state not in values for state in states):
        raise ValueError("missing vector entry; supply it or an explicit default")
    return tuple(_rational(values.get(state, default), "vector entry") for state in states)


def row_from_branches(branches):
    """Aggregate (probability, live destination or None, incurred charge).

    Probabilities must sum to one, including failure. Charge is paid on every
    branch, even when its destination is None. This helper cannot infer the
    feasibility of the preceding physical charges; the branch oracle owns it.
    """
    row, spent, total = {}, F(0), F(0)
    for probability, destination, charge in branches:
        probability = _rational(probability, "branch probability")
        charge = _rational(charge, "branch charge")
        if probability < 0 or charge < 0:
            raise ValueError("branch probabilities and charges must be nonnegative")
        total += probability
        spent += probability * charge
        if destination is not None and probability:
            row[destination] = row.get(destination, F(0)) + probability
    if total != 1:
        raise ValueError("complete branch probabilities must sum to one")
    return row, spent


def _apply(rows, vector):
    return tuple(sum((mass * vector[j] for j, mass in row.items()), F(0))
                 for row in rows)


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def _difference(reference, candidate):
    result = []
    for q, t in zip(reference, candidate):
        row = {j: t.get(j, F(0)) - q.get(j, F(0)) for j in q.keys() | t.keys()}
        result.append({j: x for j, x in row.items() if x})
    return tuple(result)


def _witness(vectors, predicate):
    for steps, vector in enumerate(vectors):
        for state, value in enumerate(vector):
            if predicate(value):
                return {"continuation_steps": steps, "state_index": state, "value": value}
    return None


def finite_residual_audit(reference, candidate, reference_cost=None,
                          candidate_cost=None, horizon=1, *, terminal=None,
                          candidate_terminal=None, terminal_cost=None,
                          candidate_terminal_cost=None, initial=None,
                          candidate_initial=None, initial_cost=0,
                          candidate_initial_cost=None, include_vectors=False):
    """Audit exact responses and incurred cost for n=0,...,horizon.

    ``horizon`` counts ordinary transitions BEFORE the terminal response/cost.
    For H tasks with no renewal after the final task, pass horizon=H-1 and the
    final-stage live probability/spend as terminal/terminal_cost. The ordinary
    kernel includes every earlier shared-bank, acquisition, and resource event.

    Defaults are terminal=1, terminal_cost=0, and zero ordinary costs. Candidate
    terminal data inherit reference data unless explicitly supplied. The local
    certificates are uniform over the entire supplied state domain. They are
    sufficient for the stated inequalities, not necessary. Exact differences
    remain available when a local certificate fails.

    Separate startup live laws and already incurred startup costs are optional.
    Their paired differences are reported separately from the uniform same-
    state certificate. No normalization or free reinitialization occurs.
    """
    if type(horizon) is not int or horizon < 0:
        raise ValueError("horizon must be a nonnegative integer")
    q, t = sparse_kernel(reference), sparse_kernel(candidate)
    size = len(q)
    if len(t) != size:
        raise ValueError("kernels must share the same ordered state domain")
    cq = _cost(reference_cost, size, "reference_cost")
    ct = _cost(candidate_cost, size, "candidate_cost")
    gq = _vector(terminal, size, "terminal", default=1)
    gt = gq if candidate_terminal is None else _vector(candidate_terminal, size, "candidate_terminal")
    bq = _cost(terminal_cost, size, "terminal_cost")
    bt = bq if candidate_terminal_cost is None else _cost(candidate_terminal_cost, size, "candidate_terminal_cost")
    if initial is None and candidate_initial is not None:
        raise ValueError("candidate_initial requires a reference initial law")
    zq = _rational(initial_cost, "initial_cost")
    zt = zq if candidate_initial_cost is None else _rational(candidate_initial_cost, "candidate_initial_cost")
    if zq < 0 or zt < 0:
        raise ValueError("startup incurred costs must be nonnegative")
    if initial is None and (zq or zt):
        raise ValueError("startup cost offsets require explicit initial laws")

    d, dc = _difference(q, t), _subtract(ct, cq)
    vq, vt, costs_q, costs_t = [gq], [gt], [bq], [bt]
    residual_v, residual_c = [], []
    difference_v, difference_c = [_subtract(gt, gq)], [_subtract(bt, bq)]
    telescoped_v, telescoped_c = difference_v[:], difference_c[:]
    for _ in range(horizon):
        rv = _apply(d, vq[-1])
        rc = _add(dc, _apply(d, costs_q[-1]))
        residual_v.append(rv)
        residual_c.append(rc)
        vq.append(_apply(q, vq[-1]))
        vt.append(_apply(t, vt[-1]))
        costs_q.append(_add(cq, _apply(q, costs_q[-1])))
        costs_t.append(_add(ct, _apply(t, costs_t[-1])))
        difference_v.append(_subtract(vt[-1], vq[-1]))
        difference_c.append(_subtract(costs_t[-1], costs_q[-1]))
        telescoped_v.append(_add(_apply(t, telescoped_v[-1]), rv))
        telescoped_c.append(_add(_apply(t, telescoped_c[-1]), rc))
        if telescoped_v[-1] != difference_v[-1] or telescoped_c[-1] != difference_c[-1]:
            raise ArithmeticError("exact residual telescoping identity failed")

    nonzero = lambda x: x != 0
    negative = lambda x: x < 0
    positive = lambda x: x > 0
    cert_v = [difference_v[0], *residual_v]
    cert_c = [difference_c[0], *residual_c]
    result = {
        "scope": "finite horizon on the supplied compiled state domain",
        "ordinary_horizon": horizon,
        "state_count": size,
        "shared_terminal_response": gt == gq,
        "shared_terminal_cost": bt == bq,
        "telescoping_verified": True,
        "certificate": {
            "equal_response_through_horizon": _witness(cert_v, nonzero) is None,
            "nondecreasing_response_through_horizon": _witness(cert_v, negative) is None,
            "nonincreasing_cost_through_horizon": _witness(cert_c, positive) is None,
        },
        "exact_comparison": {
            "equal_response_through_horizon": _witness(difference_v, nonzero) is None,
            "nondecreasing_response_through_horizon": _witness(difference_v, negative) is None,
            "nonincreasing_cost_through_horizon": _witness(difference_c, positive) is None,
            "equal_terminal_response": all(x == 0 for x in difference_v[-1]),
            "nondecreasing_terminal_response": all(x >= 0 for x in difference_v[-1]),
            "nonincreasing_terminal_cost": all(x <= 0 for x in difference_c[-1]),
        },
        "first_nonzero_response_residual": _witness(residual_v, nonzero),
        "first_negative_response_residual": _witness(residual_v, negative),
        "first_positive_cost_residual": _witness(residual_c, positive),
        "first_response_difference": _witness(difference_v, nonzero),
        "first_cost_increase": _witness(difference_c, positive),
    }
    if initial is not None:
        muq = _law(initial, size, "initial")
        mut = muq if candidate_initial is None else _law(candidate_initial, size, "candidate_initial")
        dm = _subtract(mut, muq)
        values_q = tuple(_dot(muq, vector) for vector in vq)
        values_t = tuple(_dot(mut, vector) for vector in vt)
        totals_q = tuple(zq + _dot(muq, vector) for vector in costs_q)
        totals_t = tuple(zt + _dot(mut, vector) for vector in costs_t)
        values_difference = _subtract(values_t, values_q)
        totals_difference = _subtract(totals_t, totals_q)
        paired_v = tuple(_dot(mut, residual) + _dot(dm, ref)
                         for residual, ref in zip(telescoped_v, vq))
        paired_c = tuple(zt - zq + _dot(mut, residual) + _dot(dm, ref)
                         for residual, ref in zip(telescoped_c, costs_q))
        if paired_v != values_difference or paired_c != totals_difference:
            raise ArithmeticError("paid-startup telescoping identity failed")
        result["initial_comparison"] = {
            "same_startup_law": muq == mut,
            "reference_live_mass": sum(muq, F(0)),
            "candidate_live_mass": sum(mut, F(0)),
            "reference_responses": values_q,
            "candidate_responses": values_t,
            "response_differences": values_difference,
            "reference_costs": totals_q,
            "candidate_costs": totals_t,
            "cost_differences": totals_difference,
            "telescoped_response_differences": paired_v,
            "telescoped_cost_differences": paired_c,
            "equal_response_through_horizon": all(x == 0 for x in values_difference),
            "nondecreasing_response_through_horizon": all(x >= 0 for x in values_difference),
            "nonincreasing_cost_through_horizon": all(x <= 0 for x in totals_difference),
        }
    if include_vectors:
        result["vectors"] = {
            "reference_responses": tuple(vq), "candidate_responses": tuple(vt),
            "reference_costs": tuple(costs_q), "candidate_costs": tuple(costs_t),
            "response_residuals": tuple(residual_v), "cost_residuals": tuple(residual_c),
            "response_differences": tuple(difference_v), "cost_differences": tuple(difference_c),
            "telescoped_response_differences": tuple(telescoped_v),
            "telescoped_cost_differences": tuple(telescoped_c),
        }
    return result


def audit_summary(audit):
    """Compact exact report: certificate flags, first witnesses, final values."""
    result = {key: value for key, value in audit.items()
              if key not in ("vectors", "initial_comparison")}
    if "initial_comparison" in audit:
        initial = audit["initial_comparison"]
        result["initial_comparison"] = {
            key: value[-1] if isinstance(value, tuple) else value
            for key, value in initial.items()
            if not key.startswith("telescoped_")
        }
    return result


class _ColumnBasis:
    def __init__(self, size):
        self.size, self.pivots, self.columns = size, {}, []

    def residual(self, vector):
        work = list(vector)
        for pivot in sorted(self.pivots):
            scale = work[pivot]
            if scale:
                work = [x - scale * y for x, y in zip(work, self.pivots[pivot])]
        return tuple(work)

    def add(self, vector):
        residue = self.residual(vector)
        pivot = next((i for i, value in enumerate(residue) if value), None)
        if pivot is None:
            return False
        scale = residue[pivot]
        self.pivots[pivot] = tuple(value / scale for value in residue)
        self.columns.append(tuple(vector))
        return True


def column_rank(columns):
    """Exact column rank; used for finite witnesses, not a scaling claim."""
    columns = tuple(tuple(column) for column in columns)
    if not columns:
        return 0
    size = len(columns[0])
    basis = _ColumnBasis(size)
    for column in columns:
        basis.add(_vector(column, size, "column"))
    return len(basis.columns)


def continuation_basis(kernel, probes=None, *, max_dimension=None):
    """Exact invariant closure under one supplied kernel, with explicit status.

    Returning a finite collection of independent columns is not itself a proof
    of closure: ``stabilized`` becomes true only after every retained column's
    image has been checked. A dimension cap returns an unresolved image.
    """
    rows = sparse_kernel(kernel)
    size = len(rows)
    if max_dimension is None:
        max_dimension = size
    if type(max_dimension) is not int or not 1 <= max_dimension <= size:
        raise ValueError("max_dimension must be between one and the state count")
    seeds = ((F(1),) * size,) if probes is None else tuple(probes)
    if not seeds:
        raise ValueError("at least one response probe is required")
    basis, depths = _ColumnBasis(size), []
    for probe in seeds:
        probe = _vector(probe, size, "probe")
        if any(basis.residual(probe)):
            if len(basis.columns) == max_dimension:
                return {"basis": tuple(basis.columns), "depths": tuple(depths),
                        "dimension": len(basis.columns), "stabilized": False,
                        "unresolved_image": probe}
            basis.add(probe)
            depths.append(0)
    cursor = 0
    while cursor < len(basis.columns):
        image = _apply(rows, basis.columns[cursor])
        if any(basis.residual(image)):
            if len(basis.columns) == max_dimension:
                return {"basis": tuple(basis.columns), "depths": tuple(depths),
                        "dimension": len(basis.columns), "stabilized": False,
                        "unresolved_image": image}
            basis.add(image)
            depths.append(depths[cursor] + 1)
        cursor += 1
    return {"basis": tuple(basis.columns), "depths": tuple(depths),
            "dimension": len(basis.columns), "stabilized": True,
            "unresolved_image": None}


def all_horizon_equal(reference, candidate, terminal=None, *, max_dimension=None):
    """Exact same-state, common-probe equality after checked stabilization.

    If no residual is found but closure was capped, ``equal`` is None, not True.
    This is response equality only; it does not certify cost inequalities or
    physical feasibility. The default probe is live mass.
    """
    q, t = sparse_kernel(reference), sparse_kernel(candidate)
    if len(q) != len(t):
        raise ValueError("kernels must share the same ordered state domain")
    g = _vector(terminal, len(q), "terminal", default=1)
    closure = continuation_basis(q, (g,), max_dimension=max_dimension)
    d = _difference(q, t)
    residuals = tuple(_apply(d, vector) for vector in closure["basis"])
    obstruction = _witness(residuals, lambda x: x != 0)
    if obstruction is not None:
        column = obstruction.pop("continuation_steps")
        obstruction["reference_power"] = closure["depths"][column]
        obstruction["basis_column"] = column
    return {"scope": "all finite horizons, same state and common terminal response",
            "equal": False if obstruction is not None else True if closure["stabilized"] else None,
            "stabilized": closure["stabilized"], "dimension": closure["dimension"],
            "first_obstruction": obstruction}


def residual_extension(reference, candidate, old_basis, *, max_dimension=None):
    """Smallest new invariant extension CONTAINING the supplied old interface.

    First verifies old invariance. Seeds are the old columns and their update
    residuals. Closure is exact but may reach the full physical dimension.
    This is not a claim of global minimality after replacing the old problem.
    """
    q, t = sparse_kernel(reference), sparse_kernel(candidate)
    if len(q) != len(t):
        raise ValueError("kernels must share the same ordered state domain")
    old = _ColumnBasis(len(q))
    for vector in old_basis:
        old.add(_vector(vector, len(q), "old basis column"))
    if not old.columns:
        raise ValueError("old interface must have a nonzero column")
    if any(any(old.residual(_apply(q, vector))) for vector in old.columns):
        raise ValueError("supplied old interface is not reference-invariant")
    d = _difference(q, t)
    seeds = tuple(_apply(d, vector) for vector in old.columns)
    closure = continuation_basis(t, (*old.columns, *seeds), max_dimension=max_dimension)
    return dict(closure, old_dimension=len(old.columns), seed_residual_rank=column_rank(seeds))


def _require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def rank_one_growth_control(size=8):
    """Rank-one update can expand a two-column task interface to all states."""
    if type(size) is not int or size < 3:
        raise ValueError("at least three states required")
    q = ({0: F(1)},) + tuple({i + 1 if i + 1 < size else 1: F(1)}
                              for i in range(1, size))
    t = tuple({0: F(1)} if i == 1 else row for i, row in enumerate(q))
    mass, target = (F(1),) * size, (F(1),) + (F(0),) * (size - 1)
    old = continuation_basis(q, (mass, target))
    extension = residual_extension(q, t, old["basis"])
    d = _difference(q, t)
    update_rank = column_rank(tuple(tuple(row.get(j, F(0)) for row in d)
                                    for j in range(size)))
    _require(old["stabilized"] and old["dimension"] == 2, "old interface dimension")
    _require(extension["stabilized"] and extension["dimension"] == size, "full new closure")
    _require(update_rank == extension["seed_residual_rank"] == 1, "rank-one update/seed")
    return {"states": size, "old_dimension_with_mass": old["dimension"],
            "update_rank": update_rank, "seed_residual_rank": extension["seed_residual_rank"],
            "new_dimension_with_mass": extension["dimension"]}


def negative_controls():
    """Four executable algebraic controls, not physical budget simulations."""
    q, t = ({0: F(1)}, {}), ({1: F(1)}, {})
    survival = finite_residual_audit(q, t, horizon=2, initial=(1, 0), include_vectors=True)
    _require(survival["vectors"]["response_residuals"] == ((F(0), F(0)), (F(-1), F(0))),
             "D1=0 is not a continuation certificate")
    q2 = ({1: F(1)}, {1: F(1)}, {2: F(1)})
    t2 = ({2: F(1)}, {1: F(1)}, {2: F(1)})
    cost = finite_residual_audit(q2, t2, (1, 1, 3), (0, 1, 3), 2, initial=(1, 0, 0))
    costs = cost["initial_comparison"]
    _require(costs["reference_costs"] == (0, 1, 2) and costs["candidate_costs"] == (0, 0, 3),
             "immediate saving can reverse")
    early = row_from_branches(((F(1, 2), None, 0), (F(1, 2), 0, 1)))
    late = row_from_branches(((F(1, 2), None, 1), (F(1, 2), 0, 1)))
    _require(early[0] == late[0] == {0: F(1, 2)} and early[1] == F(1, 2) and late[1] == 1,
             "failed branches must retain incurred spending")
    return {
        "scope": "algebraic negative controls, not physical budget simulations",
        "rank_one_update": tuple(rank_one_growth_control(n) for n in (3, 4, 8, 16)),
        "immediate_survival_not_enough": {"D1": (F(0), F(0)), "DQ1": (F(-1), F(0)),
            "two_step_Q_T_from_state0": (survival["initial_comparison"]["reference_responses"][-1],
                                          survival["initial_comparison"]["candidate_responses"][-1])},
        "immediate_saving_not_enough": {"one_step_Q_T": (costs["reference_costs"][1], costs["candidate_costs"][1]),
            "two_step_Q_T": (costs["reference_costs"][2], costs["candidate_costs"][2]),
            "first_positive_cost_residual": cost["first_positive_cost_residual"]},
        "failed_branch_spend": {"same_live_probability": F(1, 2), "expected_cost_A_B": (early[1], late[1])},
    }


if __name__ == "__main__":
    import json
    print(json.dumps(negative_controls(), default=str, indent=2))
