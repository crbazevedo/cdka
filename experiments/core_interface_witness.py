"""Exact finite guards for value interfaces, emission families and selectors.

This three-state algebraic witness is not an extension of the CDKA hardware
benchmark. All words are fixed in advance; the added selector macros have an
explicitly enlarged installation/composition contract. Matrix identities give
the all-word claims. Bounded enumeration is an independent finite control.

python -S -O -m experiments.core_interface_witness --check
python -S -O -m experiments.core_interface_witness --write --check
"""
from fractions import Fraction as F
from itertools import product
import argparse
import json
from pathlib import Path


OUTPUT = Path(__file__).resolve().parents[1] / 'docs/data/core-interface-witness.json'


def matrix(rows):
    result = tuple(tuple(F(value) for value in row) for row in rows)
    if not result or not result[0] or any(len(row) != len(result[0]) for row in result):
        raise ValueError('nonempty rectangular matrix required')
    return result


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dot dimensions')
    return sum((x*y for x, y in zip(a, b)), F(0))


def matmul(a, b):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError('matrix product dimensions')
    return tuple(tuple(dot(row, column) for column in zip(*b)) for row in a)


def rowmul(row, kernel):
    return matmul((row,), kernel)[0]


def add(a, b):
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b)):
        raise ValueError('matrix sum dimensions')
    return tuple(tuple(x+y for x, y in zip(r, s)) for r, s in zip(a, b))


def diagonal(values):
    return matrix([[value if i == j else 0 for j in range(len(values))]
                   for i, value in enumerate(values)])


def rank(rows):
    work = [list(row) for row in matrix(rows)]
    pivot = 0
    for column in range(len(work[0])):
        selected = next((i for i in range(pivot, len(work)) if work[i][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [value/scale for value in work[pivot]]
        for i in range(len(work)):
            if i != pivot:
                scale = work[i][column]
                work[i] = [a-scale*b for a, b in zip(work[i], work[pivot])]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def exact(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: exact(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact(item) for item in value]
    return value


def need(condition, message):
    if not condition:
        raise ValueError(message)


def model():
    e = matrix(((F(1, 2), F(1, 2), 0), (0, 0, 1)))
    operators = {
        'I': diagonal((1, 1, 1)),
        'T': matrix(((0, 1, 0), (1, 0, 0), (0, 0, 1))),
        'R': (e[0], e[0], e[1]),
        'S': (e[1], e[1], e[0]),
        'C': matrix(((1, 0, 0), (1, 0, 0), (0, 0, 1))),
    }
    return {'states': ('A0', 'A1', 'B'), 'emission': e, 'operators': operators,
            'terminal': (F(1), F(1), F(0)),
            'feature': (F(1, 2), F(1, 2), F(-1, 2)),
            'reset_factors': {'R': matrix(((1, 0), (1, 0), (0, 1))),
                              'S': matrix(((0, 1), (0, 1), (1, 0)))},
            'old_phases': {'I': diagonal((1, 1)), 'T': diagonal((1, 1)),
                           'R': diagonal((1, 1)), 'S': matrix(((0, 1), (1, 0)))},
            'selector_masks': (diagonal((1, 0, 1)), diagonal((0, 1, 0)))}


def advance(law, word, operators):
    for action in word:
        law = rowmul(law, operators[action])
    return law


def decisions(values, labels, maximum_regret=F(1, 10), minimum_value=F(2, 3)):
    best = [max(row) for row in values]
    regrets = [max(opt-row[j] for opt, row in zip(best, values)) for j in range(len(labels))]
    minima = [min(row[j] for row in values) for j in range(len(labels))]
    minimax = min(range(len(labels)), key=regrets.__getitem__)
    maximin = max(range(len(labels)), key=minima.__getitem__)
    return {'labels': labels, 'informed_values': best, 'worst_regrets': regrets,
            'minimum_values': minima, 'minimax_program': labels[minimax],
            'minimax_regret': regrets[minimax], 'maximin_program': labels[maximin],
            'maximin_value': minima[maximin], 'gate': {
                'maximum_regret': maximum_regret, 'minimum_value': minimum_value,
                'feasible_programs': [labels[j] for j in range(len(labels))
                                      if regrets[j] <= maximum_regret and minima[j] >= minimum_value]}}


def run(horizon=4):
    if type(horizon) is not int or horizon < 0:
        raise ValueError('nonnegative finite control horizon required')
    m = model()
    e, ops, g, feature = m['emission'], m['operators'], m['terminal'], m['feature']
    for k in ops.values():
        need(all(all(p >= 0 for p in row) and sum(row, F(0)) == 1 for row in k),
             'stochastic physical matrix')
    for name, phase in m['old_phases'].items():
        need(matmul(e, ops[name]) == matmul(phase, e), 'old emission intertwining')
    for name, a in m['reset_factors'].items():
        need(ops[name] == matmul(a, e), 'fresh reset factorization')

    annihilator = (F(1), F(-1), F(0))
    after_c = matmul(e, ops['C'])
    need(all(dot(row, annihilator) == 0 for row in e), 'old emission invariant')
    need(tuple(dot(row, annihilator) for row in after_c) == (F(1), F(0)),
         'new operation must leave even the old linear emission span')
    need(rank((*e, after_c[0])) == 3, 'three independent reachable full laws')
    need(rank(((1, 1, 1), g)) == 2, 'old response span including mass')
    for action, k in ops.items():
        sign = -1 if action == 'S' else 1
        need(tuple(dot(row, feature) for row in k) == tuple(sign*x for x in feature),
             'one-scalar task transport identity')

    # Every physical basis law is checked. Linearity also covers all mixtures.
    alphabet = tuple(ops)
    words = values_checked = 0
    for depth in range(horizon+1):
        for letters in product(alphabet, repeat=depth):
            word = ''.join(letters)
            words += 1
            sign = (-1)**word.count('S')
            for initial in ops['I']:
                actual = dot(advance(initial, word, ops), g)
                expected = F(1, 2) + sign*dot(initial, feature)
                need(actual == expected, 'bounded fixed-word physical control')
                values_checked += 1

    d0, d1 = m['selector_masks']
    need(add(d0, d1) == ops['I'], 'complete selector masks')
    need(add(matmul(d0, ops['I']), matmul(d1, ops['T'])) == ops['C'],
         'weakly invariant primitives combine into the counterexample')
    incompatible = matmul(e, d0)
    need(dot(incompatible[0], annihilator) == F(1, 2),
         'selector fails even linear compatibility with E')

    # A selector compatible with E uses one weight on the whole A block.
    c0, c1 = diagonal((1, 1, 0)), diagonal((0, 0, 1))
    h0, h1 = diagonal((1, 0)), diagonal((0, 1))
    need(matmul(e, c0) == matmul(h0, e) and matmul(e, c1) == matmul(h1, e),
         'compatible selector identities')
    compatible = add(matmul(c0, ops['I']), matmul(c1, ops['S']))
    compatible_phase = add(matmul(h0, m['old_phases']['I']),
                           matmul(h1, m['old_phases']['S']))
    need(matmul(e, compatible) == matmul(compatible_phase, e),
         'compatible selector preserves weak closure')

    # U is a newly installed conditional macro; opaque C does not export its flag.
    u = add(matmul(d0, ops['S']), matmul(d1, ops['R']))
    a_u = add(matmul(d0, m['reset_factors']['S']),
              matmul(d1, m['reset_factors']['R']))
    phase_u = matmul(e, a_u)
    need(u == matmul(a_u, e) and matmul(e, u) == matmul(phase_u, e),
         'common reset survives the incompatible selector')
    response_u = tuple(dot(row, g) for row in u)
    need(response_u == (F(0), F(1), F(1)), 'new macro response')
    need(rank(((1, 1, 1), g, response_u)) == 3, 'new task response separation')

    acquisition = (F(3, 10), F(3, 10), F(2, 5))
    cohort = (advance(acquisition, 'I', ops), advance(acquisition, 'C', ops))
    need(cohort == (acquisition, (F(3, 5), F(0), F(2, 5))), 'actual equal-length histories')
    signatures = tuple(dot(mu, feature) for mu in cohort)
    need(signatures == (F(1, 10), F(1, 10)), 'same old task feature')
    labels, actions = ('R', 'S', 'U'), (ops['R'], ops['S'], u)
    actual_values = tuple(tuple(dot(rowmul(mu, k), g) for k in actions) for mu in cohort)
    need(actual_values == ((F(3, 5), F(2, 5), F(7, 10)),
                           (F(3, 5), F(2, 5), F(2, 5))), 'exact decision reversal')
    actual = decisions(actual_values, labels)
    need(actual['minimax_program'] == 'R' and actual['minimax_regret'] == F(1, 10)
         and actual['maximin_value'] == F(3, 5) and not actual['gate']['feasible_programs'],
         'true common decision and joint infeasibility')
    # The false decoder reconstructs a fresh law from x=P(A), losing selection.
    naive_laws = tuple(rowmul((z+F(1, 2), F(1, 2)-z), e) for z in signatures)
    naive_values = tuple(tuple(dot(rowmul(mu, k), g) for k in actions) for mu in naive_laws)
    naive = decisions(naive_values, labels)
    need(naive['minimax_program'] == 'U' and naive['minimax_regret'] == 0
         and naive['maximin_value'] == F(7, 10) and naive['gate']['feasible_programs'] == ['U'],
         'stale emission reuse must falsely certify the joint gate')

    # The four rules exhaust deterministic maps from the binary flag to R/S.
    # The fourth rule is terminally dominated, but not in every suffix context.
    w = add(matmul(d0, ops['R']), matmul(d1, ops['S']))
    a_w = add(matmul(d0, m['reset_factors']['R']),
              matmul(d1, m['reset_factors']['S']))
    need(w == matmul(a_w, e), 'fourth routing rule regenerates E')
    response_w = tuple(dot(row, g) for row in w)
    response_r = tuple(dot(row, g) for row in ops['R'])
    need(all(r >= v for r, v in zip(response_r, response_w)),
         'R dominates W for the terminal task at every physical input')
    full_labels = (*labels, 'W')
    full_values = tuple((*row, dot(rowmul(mu, w), g))
                        for mu, row in zip(cohort, actual_values))
    full_decision = decisions(full_values, full_labels)
    for key in ('informed_values', 'minimax_regret', 'maximin_value', 'gate'):
        need(full_decision[key] == actual[key], 'one-step deterministic program cover')

    # Changing the deadline changes the program class. Check both alphabets:
    # terminal domination does not license replacing W before the suffix U.
    continuation_ops = dict(ops, U=u, W=w)
    two_labels = tuple(''.join(letters) for letters in product(full_labels, repeat=2))
    two_values = tuple(tuple(dot(advance(mu, word, continuation_ops), g)
                             for word in two_labels) for mu in cohort)
    two_decision = decisions(two_values, two_labels)
    selected_two = {word: tuple(row[two_labels.index(word)] for row in two_values)
                    for word in ('RU', 'SU', 'WU')}
    need(selected_two == {'RU': (F(7, 10), F(7, 10)),
                          'SU': (F(4, 5), F(4, 5)),
                          'WU': (F(17, 20), F(7, 10))}, 'two-step exact controls')
    need(two_decision['minimax_program'] == 'SU'
         and two_decision['minimax_regret'] == F(1, 20)
         and two_decision['maximin_value'] == F(4, 5)
         and two_decision['gate']['feasible_programs'] == ['SU', 'WU'],
         'complete two-step class changes both envelope and joint feasibility')
    restricted_two_labels = tuple(''.join(letters) for letters in product(labels, repeat=2))
    restricted_two_values = tuple(tuple(row[two_labels.index(word)]
                                        for word in restricted_two_labels) for row in two_values)
    restricted_two_decision = decisions(restricted_two_values, restricted_two_labels)
    need(restricted_two_decision['minimax_regret'] == 0
         and restricted_two_decision['gate']['feasible_programs'] == ['RU', 'SU'],
         'the restricted two-step control is a different library')

    # This common external random choice is absent from the one-step contract.
    # It is an exact improvement control, not a randomized-optimality claim.
    mixture_values = tuple(F(2, 3)*row[0]+F(1, 3)*row[2] for row in actual_values)
    mixture_regrets = tuple(best-value for best, value in
                            zip(actual['informed_values'], mixture_values))
    need(mixture_values == (F(19, 30), F(8, 15))
         and mixture_regrets == (F(1, 15), F(1, 15)), 'external-coin control')

    return exact({'schema': 'cdka.core-interface-witness/v1',
                  'scope': 'finite algebraic audit witness; not new CDKA hardware or a priority claim',
                  'model': m, 'old_fixed_word_grammar': ['I', 'T', 'R', 'S'],
                  'first_extended_fixed_word_grammar': list(alphabet),
                  'decision_contract': {
                      'preparation_slots': 1, 'remaining_continuation_slots': 1,
                      'preparation_histories': ['I', 'C'],
                      'matched_resource': 'I is padded/charged to the same preparation slot as C; both leave one macro slot.',
                      'complete_deterministic_continuation_library': list(full_labels),
                      'retained_continuation_library': list(labels),
                      'external_controller_coin_available': False,
                      'preparation_history_identifier_available': False,
                      'controller_input': 'One current binary flag, followed by one deterministic R/S selection; no later decision in that slot.',
                      'C_status': 'Opaque baseline primitive; its algebraic selector decomposition does not export an observation.',
                      'U_W_status': 'Separately installed conditional R/S rules using the declared binary flag; no new observation alphabet is logically required.',
                      'resource_scope': 'Abstract matched-slot/deadline contract, not a CDKA hardware price or access grant.'},
                  'old_emission_failure': {'annihilator': annihilator, 'E_C': after_c,
                                          'E_annihilator': [F(0), F(0)],
                                          'E_C_annihilator': [F(1), F(0)],
                                          'reachable_full_law_span_rank': 3,
                                          'sufficient_full_law_emission': ops['I']},
                  'task_interface': {'known_mass': F(1), 'affine_scalar': 'z=mu(A0)+mu(A1)-1/2',
                                     'response_span_rank_including_mass': 2,
                                     'free_affine_coordinates': 1,
                                     'all_word_value': '1/2+(-1)^number_of_S*z',
                                     'global_after_U_response_rank_including_mass': 3},
                  'selectors': {'weak_invariance_counterexample': {
                      'primitives': ['I', 'T'], 'masks': [d0, d1], 'result': ops['C'],
                      'E_D0_annihilator': [F(1, 2), F(0)]},
                      'compatible_control': {'primitives': ['I', 'S'], 'masks': [c0, c1],
                                             'phase_masks': [h0, h1], 'kernel': compatible,
                                             'phase_kernel': compatible_phase},
                      'common_reset_control': {'primitives': ['S', 'R'], 'masks': [d0, d1],
                                               'kernel_U': u, 'factor_A_U': a_u,
                                               'phase_kernel_U': phase_u,
                                               'post_U_phase_weights': [rowmul(mu, a_u) for mu in cohort]}},
                  'decision_reversal': {'acquisition': acquisition, 'histories': ['I', 'C'],
                                        'preparations': cohort, 'old_signatures': signatures,
                                        'actual_values': actual_values, 'actual': actual,
                                        'false_fresh_reconstructions': naive_laws,
                                        'false_values': naive_values, 'false_decision': naive},
                  'deterministic_policy_cover': {
                      'observation_by_state': [0, 1, 0],
                      'routing_by_observation': {'R': ['R', 'R'], 'S': ['S', 'S'],
                                                 'U': ['S', 'R'], 'W': ['R', 'S']},
                      'labels': full_labels, 'kernel_W': w, 'factor_A_W': a_w,
                      'W_values': [row[-1] for row in full_values],
                      'response_R': response_r, 'response_W': response_w,
                      'R_dominates_W_at_every_physical_input': True,
                      'retained_cover': {'R': 'R', 'S': 'S', 'U': 'U', 'W': 'R'},
                      'actual_values': full_values, 'full_decision': full_decision,
                      'scope': 'Complete one-step deterministic binary-observation R/S policy class; terminal dominance only.'},
                  'two_step_positive_control': {
                      'remaining_continuation_slots': 2, 'within_actual_contract': False,
                      'labels': two_labels, 'actual_values': two_values, 'decision': two_decision,
                      'selected_values': selected_two,
                      'restricted_RSU_library': {'labels': restricted_two_labels,
                                                 'actual_values': restricted_two_values,
                                                 'decision': restricted_two_decision},
                      'scope': 'A changed deadline. One-step terminal dominance of W by R does not justify deleting W before U.'},
                  'randomization_boundary_control': {
                      'within_actual_contract': False, 'external_coin': {'R': F(2, 3), 'U': F(1, 3)},
                      'values': mixture_values, 'same_input_regrets': mixture_regrets,
                      'worst_regret': max(mixture_regrets), 'minimum_value': min(mixture_values),
                      'deterministic_minimax_regret': actual['minimax_regret'],
                      'strict_regret_improvement': max(mixture_regrets) < actual['minimax_regret'],
                      'maximin_value_with_any_mixture': F(3, 5),
                      'maximin_bound_reason': 'At mu_1 every deterministic rule has value at most 3/5; R attains 3/5 on both inputs.',
                      'joint_gate_feasible_with_any_mixture': False,
                      'scope': 'Independent externally available common coin changes the policy class; no randomized minimax optimality claim.'},
                  'bounded_control': {'maximum_word_length': horizon, 'words': words,
                                      'physical_basis_laws': 3, 'value_comparisons': values_checked,
                                      'all_horizons_guaranteed_by_matrix_identities': True},
                  'limits': ['All-word old sufficiency concerns the declared terminal task and fixed-word grammar.',
                             'U/W require verified selector access and installed conditional composition; opaque C alone does not grant this capability.',
                             'The decision certificate has exactly one remaining macro slot and deterministic routing; extra time or a common external coin changes its class.',
                             'No contradiction to a PSR that already covers those observations and policy contingencies.',
                             'One scalar uses known unit mass; linear response span has dimension two.',
                             'The rank-three full-law bound concerns this reachable law family, not controller bits or T4R48.',
                             'Output regeneration does not recover input distinctions or phase weights lost by an old code.',
                             'A row-selector mixture must be the verified joint physical kernel; shared causes cannot be factored away.']})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    if args.write:
        OUTPUT.write_text(json.dumps(result, indent=2)+'\n')
    if args.check:
        need(result == json.loads(OUTPUT.read_text()), 'stale core-interface witness')
    print(json.dumps({'bounded_control': result['bounded_control'],
                      'actual': result['decision_reversal']['actual'],
                      'false': result['decision_reversal']['false_decision']}, indent=2))
