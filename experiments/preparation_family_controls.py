"""Exact physical controls for convex preparation-family certificates.

Run without optional packages and with assertions disabled:

    python -S -O -m experiments.preparation_family_controls
    python -S -O -m experiments.preparation_family_controls --output PATH

These are deterministic counterexamples, not runtime measurements. They
preserve the inherited kernels, acquisition and complete-program grammar.
The conic-only counterexample declares initially bad health explicitly;
the informed-envelope and correlated-regret controls use the default case.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path

from cdka.maintenance_access import base_operators, base_probes
from cdka.reachable_diagnosis import evaluate, plan_words, preparation_laws
from cdka.reachable_restriction import contrast_response, contrast_signature
from cdka.semantic_closure import dot, word_value


PARENT = '2f9abfd01b5298de1a1889cc7c57776fa0f86572'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    if type(value) is F:
        return str(value)
    if type(value) is dict:
        return {str(key): exact(item) for key, item in value.items()}
    if type(value) in (tuple, list):
        return [exact(item) for item in value]
    return value


def positive_signature(law):
    offset, signed = contrast_signature(*law)
    require(offset == F(1, 2), 'the fair-source offset must remain one half')
    result = tuple(-value for value in signed)
    require(len(result) == 4 and all(value >= 0 for value in result),
            'preparation must belong to the certified contrast cone')
    return result


def physical_library(operators, terminal, k):
    words = tuple(''.join(word) for word in plan_words(k))
    require(len(words) == (k+2)*2**k and len(set(words)) == len(words),
            'complete physical grammar size')
    return tuple((word, contrast_response(word_value(operators, word, terminal)))
                 for word in words)


def table(cohort, library):
    result = {}
    for history, law in cohort.items():
        x = positive_signature(law)
        values = tuple(F(1, 2)-dot(x, q) for _, q in library)
        require(all(F(0) <= value <= F(1) for value in values),
                'physical fidelity must be a probability')
        result[history] = values
    return result


def optimum(rows, library):
    values = tuple(rows.values())
    best = tuple(max(row) for row in values)
    regrets = tuple(max(b-row[j] for b, row in zip(best, values))
                    for j in range(len(library)))
    minima = tuple(min(row[j] for row in values) for j in range(len(library)))
    minimax = min(regrets)
    maximin = max(minima)
    return {
        'minimax_regret': minimax,
        'minimax_programs': [word for (word, _), value in zip(library, regrets)
                             if value == minimax],
        'maximin_fidelity': maximin,
        'maximin_programs': [word for (word, _), value in zip(library, minima)
                            if value == maximin],
    }


def conic_is_not_convex(library):
    """A nonnegative identity with mass below one can falsify a fidelity floor."""
    cohort = preparation_laws(2, F(1, 10), F(1))
    signatures = {history: positive_signature(law) for history, law in cohort.items()}
    alpha = signatures['RR'][2]/signatures['DR'][2]
    expected = F(65551895140387323168, 75155083711181640625)
    require(alpha == expected and F(0) < alpha < F(1), 'proper conic scale')
    require(signatures['RR'] == tuple(alpha*x for x in signatures['DR']),
            'exact conic-only identity')
    retained = ('DD', 'DR', 'RD')
    rows = table(cohort, library)
    reduced = {history: rows[history] for history in retained}
    word = 'DDDDM'
    j = next(i for i, (label, _) in enumerate(library) if label == word)
    physical_values = {history: evaluate(law, word) for history, law in cohort.items()}
    require(all(physical_values[history] == rows[history][j] for history in cohort),
            'full physical query must agree with the contrast calculation')
    true_minimum = min(physical_values.values())
    false_minimum = min(physical_values[history] for history in retained)
    require(true_minimum < false_minimum, 'dropping RR must overestimate the floor')
    selected_floor = (true_minimum+false_minimum)/2
    require(true_minimum < selected_floor < false_minimum, 'strict false positive floor')

    full_optimum, reduced_optimum = optimum(rows, library), optimum(reduced, library)
    require(full_optimum['maximin_fidelity'] < reduced_optimum['maximin_fidelity'],
            'conic-only removal must also change global maximin value')
    gate_floor = (full_optimum['maximin_fidelity']+
                  reduced_optimum['maximin_fidelity'])/2
    # The regret ceiling one is satisfied by every plan because all fidelities
    # lie in [0,1]; this isolates the incorrect absolute-fidelity decision.
    return {
        'preparation_updates': 2, 'ordinary_continuation_updates': 4,
        'sensor_error': F(1, 10), 'initial_bad_probability': F(1),
        'repair_success': F(4, 5),
        'retained_actual_histories': retained, 'discarded_actual_history': 'RR',
        'signatures': signatures,
        'invalid_convex_witness': {'terms': [['DR', alpha]], 'coefficient_sum': alpha},
        'vector_identity_is_exact': True, 'coefficients_are_nonnegative': True,
        'coefficients_sum_to_one': False,
        'fixed_program': word, 'physical_values': physical_values,
        'true_minimum_fidelity': true_minimum,
        'incorrect_retained_only_minimum': false_minimum,
        'fixed_program_false_positive_floor': selected_floor,
        'full_library_optimum': full_optimum,
        'incorrect_retained_only_optimum': reduced_optimum,
        'false_joint_gate': {'maximum_regret': F(1), 'minimum_fidelity': gate_floor,
                             'full_feasible': False, 'incorrect_retained_only_feasible': True},
        'scope': 'Same acquisition and history length within this explicitly all-bad '
                 'control. Conic coverage alone does not imply the claimed affine '
                 'or convex coverage; it can remove the physically worst preparation.',
    }


def informed_value_is_not_affine(cohort, library):
    left, right = 'DD', 'DR'
    mixture = tuple(tuple((a+b)/2 for a, b in zip(mu, nu))
                    for mu, nu in zip(cohort[left], cohort[right]))
    x_left, x_right, x_mid = (positive_signature(law)
                              for law in (cohort[left], cohort[right], mixture))
    require(x_mid == tuple((a+b)/2 for a, b in zip(x_left, x_right)),
            'mixture signature must be affine')
    rows = table({left: cohort[left], right: cohort[right], 'midpoint': mixture}, library)
    require(all(c == (a+b)/2 for a, b, c in
                zip(rows[left], rows[right], rows['midpoint'])),
            'each fixed physical program value must be affine')
    best = {history: max(row) for history, row in rows.items()}
    attaining = {history: [word for (word, _), value in zip(library, row)
                            if value == best[history]] for history, row in rows.items()}
    interpolated = (best[left]+best[right])/2
    gap = interpolated-best['midpoint']
    require(gap > 0, 'strict Jensen gap for the informed envelope')
    require(attaining[left] == ['RDDDM'] and attaining[right] == ['DDDDM'],
            'different endpoint optima must remain physical witnesses')
    for word in set(attaining[left]+attaining[right]+attaining['midpoint']):
        j = next(i for i, (label, _) in enumerate(library) if label == word)
        require(evaluate(mixture, word) == rows['midpoint'][j],
                'full physical mixed-law query')
    return {
        'preparation_updates': 2, 'ordinary_continuation_updates': 4,
        'sensor_error': F(1, 10), 'initial_bad_probability': F(0),
        'actual_endpoint_histories': (left, right), 'weights': (F(1, 2), F(1, 2)),
        'endpoint_signatures': (x_left, x_right), 'mixture_signature': x_mid,
        'fixed_program_affine_identities_checked': len(library),
        'informed_values': best, 'informed_attaining_programs': attaining,
        'incorrect_interpolated_informed_value': interpolated,
        'interpolation_overstatement': gap,
        'scope': 'The endpoints are actual histories. The midpoint is an uncertainty '
                 'mixture in the convexified evaluator domain, not a new free physical '
                 'preparation routine. This refutes interpolation of informed maxima; '
                 'it does not assert that this midpoint is an omitted actual history.',
    }


def attaining_is_not_optimal(cohort, library):
    rows = table(cohort, library)
    best = {history: max(row) for history, row in rows.items()}
    selected = 'DDDDM'
    j = next(i for i, (word, _) in enumerate(library) if word == selected)
    differences = {history: best[history]-row[j] for history, row in rows.items()}
    selected_regret = max(differences.values())
    attainers = [history for history, value in differences.items() if value == selected_regret]
    reference = optimum(rows, library)
    require(reference['minimax_programs'] == ['DRDDM'], 'principal physical minimax control')
    require(reference['minimax_regret'] < selected_regret,
            'an exactly attained worst case must not imply global optimality')
    true_j = next(i for i, (word, _) in enumerate(library) if word == 'DRDDM')
    true_differences = {history: best[history]-row[true_j] for history, row in rows.items()}
    correlated = max(true_differences.values())
    independent = max(best.values())-min(row[true_j] for row in rows.values())
    require(correlated == reference['minimax_regret'] and independent > correlated,
            'separate extrema must lose the same-preparation correlation')
    return {
        'preparation_updates': 2, 'ordinary_continuation_updates': 4,
        'selected_suboptimal_program': selected,
        'correct_selected_worst_regret': selected_regret,
        'actual_attaining_histories': attainers,
        'better_common_programs': reference['minimax_programs'],
        'true_minimax_regret': reference['minimax_regret'],
        'uncorrelated_envelope_subtraction_for_DRDDM': independent,
        'same_history_differences_for_DRDDM': true_differences,
        'scope': 'An attaining history establishes a lower bound or an exact worst '
                 'case when paired with a universal upper bound. It does not exclude '
                 'a better common program; global optimality needs complete candidate '
                 'coverage. The comparator and chosen program must use the same history.',
    }


def run():
    operators, terminal = base_operators(), base_probes()['readout']
    library = physical_library(operators, terminal, 4)
    cohort = preparation_laws(2)
    return exact({
        'schema': 'cdka.preparation-family-structural-controls/v1',
        'parent_commit': PARENT,
        'physical_model_changed': False,
        'complete_programs': len(library),
        'conic_is_not_convex': conic_is_not_convex(library),
        'informed_value_is_not_affine': informed_value_is_not_affine(cohort, library),
        'attaining_is_not_optimal': attaining_is_not_optimal(cohort, library),
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True)+'\n'
    if arguments.output is None:
        print(payload, end='')
    else:
        arguments.output.write_text(payload)


if __name__ == '__main__':
    main()
