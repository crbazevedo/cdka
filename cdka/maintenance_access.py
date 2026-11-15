"""Paid maintenance changes the distinctions required by a continuation.

Extension of the pinned CDKA v15 register grammar, not a new plant kernel.
The six-NAND voter reads the existing three cells and triggers a hidden repair.
A whole diagnostic/service slot is prepaid, including when the vote is zero.
The result of maintenance is not a readable observation. Resource and phase
are declared control inputs; latent substrate health is an evaluator variable.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import product

from .boundary_voting import (
    BITS, STATES, RATE, HEALTH, VOTER, voter_table, execute_voter,
    raw_update, quotient_update, state_label, probability, add,
)
from .semantic_closure import matrix, vector, dot, word_value

BASE_COMMIT = '2eb1da7b635da2165e3b767440371a69583df3d0'
SUCCESS = F(4, 5)
WRITE_ERROR = F(1, 50)
PAID_STATES = tuple((r, z, bits) for r in (0, 1) for z, bits in STATES)
PAID_INDEX = {s: i for i, s in enumerate(PAID_STATES)}
MACRO_STATES = tuple((r, z, a, t) for r in (0, 1) for z in (0, 1)
                     for a in (0, 1) for t in range(3))
MACRO_INDEX = {s: i for i, s in enumerate(MACRO_STATES)}


def contract(success=SUCCESS):
    return {
        'name': 'maintenance-enabled-continuation-signatures',
        'base_commit': BASE_COMMIT,
        'rates': list(map(str, RATE)),
        'health': [[str(p) for p in row] for row in HEALTH],
        'write_error': str(WRITE_ERROR),
        'maintenance_success': str(probability(success)),
        'voter_nand_pairs': [list(pair) for pair in VOTER],
        'maintenance': 'prepay one slot; actual voter output 1 requests repair; '
                       'hidden success sets Z=0; retain cells; then HEALTH',
        'budget_zero': 'M is inadmissible and represented by zero live mass',
        'readable': ['one terminal voter output', 'prepaid slot balance',
                     'declared phase clock'],
        'internal_only': ['three physical cells feed the installed voter',
                          'M voter output drives repair but is not returned',
                          'D/R return no intermediate observation'],
        'hidden': ['substrate health', 'internal gate faults', 'repair success',
                   'intermediate voter output'],
        'terminal_event': 'actual six-NAND readout equals one',
        'cost_model': 'component counts and library service slots, not joules',
        'common_infrastructure': 'three retained cells, fixed routing and phase '
                                 'controller, resource reservation; these are '
                                 'declared ideal primitives, not an autonomous '
                                 'model of every component',
    }


@lru_cache(None)
def maintenance_row(state, success=SUCCESS):
    """Algebraic 16-state kernel. The repair trigger is physically noisy.

    The selector is evaluated BEFORE its possible repair. The single hidden
    repair outcome is shared by all future gates through Z; it is never
    replaced by a mean independent per-gate error probability.
    """
    z, bits = state
    s = probability(success)
    p_request = voter_table(RATE[z])[BITS.index(bits)]
    p_repair = p_request * s
    after_service = {0: F(1)} if z == 0 else {0: p_repair, 1: 1-p_repair}
    out = {}
    for repaired_z, ps in after_service.items():
        for next_z, ph in enumerate(HEALTH[repaired_z]):
            add(out, (next_z, bits), ps*ph)
    return out


def maintenance_traces(state, success=SUCCESS):
    """Raw gate/repair/health event paths, independent of maintenance_row."""
    z, bits = state
    s = probability(success)
    g = RATE[z]
    traces = []
    for mask in product((0, 1), repeat=6):
        pm = g**sum(mask) * (1-g)**(6-sum(mask))
        request = execute_voter(bits, mask)
        outcomes = ((0, F(1)),) if request == 0 else ((0, 1-s), (1, s))
        for repaired, pr in outcomes:
            service_z = 0 if repaired else z
            for next_z, ph in enumerate(HEALTH[service_z]):
                mass = pm*pr*ph
                if mass:
                    traces.append({'fault_mask': mask, 'request': request,
                                   'repair_succeeded': repaired,
                                   'post_service_health': service_z,
                                   'target': (next_z, bits), 'probability': mass})
    return traces


def raw_maintenance_row(state, success=SUCCESS):
    out = {}
    for row in maintenance_traces(state, success):
        add(out, row['target'], row['probability'])
    return out


def base_operators(success=SUCCESS):
    ix = {s: i for i, s in enumerate(STATES)}
    ops = {}
    for label, mode in (('D', 'diffuse'), ('R', 'regenerate')):
        ops[label] = matrix([{ix[t]: p for t, p in raw_update(s, mode, WRITE_ERROR).items()}
                             for s in STATES])
    ops['M'] = matrix([{ix[t]: p for t, p in maintenance_row(s, success).items()}
                       for s in STATES])
    return ops


def base_probes():
    return {'mass': vector([1]*16),
            'readout': vector(voter_table(RATE[z])[BITS.index(bits)]
                              for z, bits in STATES)}


def paid_operators(success=SUCCESS):
    """32-state resource-aware kernels; a second M fails closed.

    Admissible words have at most one M from budget one. There is no policy
    access to Z and no choice of repair based on a designer posterior.
    """
    small = base_operators(success)
    out = {}
    for label, q in small.items():
        rows = []
        for r, z, bits in PAID_STATES:
            if label == 'M' and r == 0:
                rows.append({})
                continue
            r1 = r - int(label == 'M')
            row = q[STATES.index((z, bits))]
            rows.append({PAID_INDEX[(r1, STATES[j][0], STATES[j][1])]: p
                         for j, p in row.items()})
        out[label] = matrix(rows)
    return out


def paid_probes():
    small = base_probes()
    return {'mass': vector([1]*32),
            'readout': vector(list(small['readout'])*2),
            'budget_zero': vector([1]*16+[0]*16),
            'budget_one': vector([0]*16+[1]*16)}


def paid_label(state):
    r, z, (a, b, c) = state
    return r, z, a, b+c


def macro_operators(success=SUCCESS):
    """Independent algebraic 24-state quotient, retaining shared health."""
    s = probability(success)
    out = {}
    for label, mode in (('D', 'diffuse'), ('R', 'regenerate'), ('M', None)):
        rows = []
        for r, z, a, t in MACRO_STATES:
            if label == 'M':
                if not r:
                    rows.append({})
                    continue
                representative = (a, int(t >= 1), int(t == 2))
                p = voter_table(RATE[z])[BITS.index(representative)]*s
                service = {0: F(1)} if z == 0 else {0: p, 1: 1-p}
                row = {}
                for z0, p0 in service.items():
                    for z1, p1 in enumerate(HEALTH[z0]):
                        add(row, MACRO_INDEX[(0, z1, a, t)], p0*p1)
                rows.append(row)
            else:
                q = quotient_update((z, a, t), mode, WRITE_ERROR)
                rows.append({MACRO_INDEX[(r,)+target]: p for target, p in q.items()})
        out[label] = matrix(rows)
    return out


def witness_laws(paid=False, budget=1):
    """Two explicit laws with equal responses to every old D/R continuation."""
    den = 1458626
    left_weights = {(1, (1, 0, 0)): 736513, (1, (1, 0, 1)): 722113}
    right_weights = {(1, (0, 0, 0)): 30625, (1, (0, 0, 1)): 736513,
                     (1, (0, 1, 1)): 691488}
    if paid:
        laws = []
        for weights in (left_weights, right_weights):
            laws.append(vector(F(weights.get((z, bits), 0), den) if r == budget else 0
                               for r, z, bits in PAID_STATES))
        return tuple(laws)
    return tuple(vector(F(weights.get(state, 0), den) for state in STATES)
                 for weights in (left_weights, right_weights))


def word_cost(word, terminal_readout=True):
    """Exact prefix-safe library prices. Six installed NANDs are reused.

    A service slot is prepaid even when no repair is requested. Gate calls,
    cell writes, service slots and clock intervals are different resources.
    """
    w = tuple(word)
    if any(x not in ('D', 'R', 'M') for x in w):
        raise ValueError('unknown primitive')
    return {'installed_nands': 6, 'retained_cells': 3,
            'voter_evaluations': w.count('R')+w.count('M')+int(terminal_readout),
            'nand_evaluations': 6*(w.count('R')+w.count('M')+int(terminal_readout)),
            'cell_writes': 3*w.count('R'),
            'cell_channel_updates': 3*(w.count('D')+w.count('R')),
            'prepaid_service_slots': w.count('M'),
            'clock_intervals': len(w)+int(terminal_readout),
            'admissible_from_one_slot': w.count('M') <= 1}


def evaluate_word(law, word, success=SUCCESS, paid=True):
    ops = paid_operators(success) if paid else base_operators(success)
    probes = paid_probes() if paid else base_probes()
    return dot(law, word_value(ops, word, probes['readout']))
