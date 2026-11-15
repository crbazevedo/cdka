"""Paid acquisition, reachable preparations and shared complete continuations.

One binary sensor samples a fixed, fair source bit H. Its ONE noisy output Y
is broadcast to three independently faulty writes; Y is not resampled for
each cell. The inherited health channel then advances for the acquisition
interval. H and substrate health Z are evaluator-only variables.

After h ordinary D/R updates, every length-h history gives a physically
generated preparation. A shared continuation is installed for their entire
declared class; the history identifier is not a free controller input.
The principal workload requires exactly k further D/R updates and permits
at most one additional prepaid maintenance interval. Optional-update words
remain available as an explicitly different control workload.

Evaluation reuses the 16-state physical kernels through two submeasures:
P(readout=H) = mass(mu_0) + (mu_1-mu_0) K_word g. No 32-by-32 kernel or
readable posterior is needed. The separate joint oracle carries H explicitly
and executes the inherited raw physical channels.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import product

from .boundary_voting import (
    BITS, HEALTH, RATE, STATES, add, execute_voter, probability, raw_update,
)
from .maintenance_access import (
    SUCCESS, WRITE_ERROR, base_operators, base_probes, raw_maintenance_row,
)
from .semantic_closure import dot, push, vector, word_value

SENSOR_ERROR = F(1, 10)
INITIAL_BAD = F(0)
SOURCE_PRIOR_ONE = F(1, 2)
STATE_INDEX = {state: i for i, state in enumerate(STATES)}


def _count(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(name + ' must be a nonnegative integer')
    return value


def _word(word, *, history=False):
    # Table identifiers may round-trip through the public numerical API.
    result = () if isinstance(word, str) and word == 'I' else tuple(word)
    allowed = ('D', 'R') if history else ('D', 'R', 'M')
    if any(letter not in allowed for letter in result):
        raise ValueError('history uses only D/R' if history else 'unknown physical primitive')
    if not history and result.count('M') > 1:
        raise ValueError('only one prepaid maintenance interval is available')
    return result


def word_id(word):
    """A display identifier; I denotes the empty word, not an extra action."""
    return ''.join(_word(word)) or 'I'


def _parameters(eta, initial_bad):
    return probability(eta, F(1, 2)), probability(initial_bad)


def _law(law):
    if len(law) != 2:
        raise ValueError('two H-indexed submeasures are required')
    rows = tuple(vector(row) for row in law)
    if any(len(row) != len(STATES) for row in rows):
        raise ValueError('each submeasure uses the inherited 16-state order')
    if any(p < 0 for row in rows for p in row) or sum(map(sum, rows), F(0)) != 1:
        raise ValueError('a normalized nonnegative joint law is required')
    return rows


def acquisition(eta=SENSOR_ERROR, initial_bad=INITIAL_BAD):
    """Return (mu_0, mu_1) after ONE shared observation and three writes.

    The source prior is fair and independent of initial substrate health.
    Sensor noise is independent of the write flags conditional on H,Y.
    All three cells share the same realized Y. HEALTH is applied once after
    acquisition; the sensor itself is a declared, separately counted channel.
    """
    eta, bad = _parameters(eta, initial_bad)
    e = WRITE_ERROR
    rows = []
    for h in (0, 1):
        row = []
        for z, bits in STATES:
            pz = (1-bad)*HEALTH[0][z] + bad*HEALTH[1][z]
            cells = F(0)
            for y in (0, 1):
                distance = sum(bit != y for bit in bits)
                cells += (1-eta if y == h else eta) * e**distance * (1-e)**(3-distance)
            row.append(F(1, 2)*pz*cells)
        rows.append(tuple(row))
    return tuple(rows)


def acquisition_traces(eta=SENSOR_ERROR, initial_bad=INITIAL_BAD):
    """Independent raw H/Z/sensor/write/health event paths.

    Exactly one sensor fault is drawn per path. Replacing this by three
    sensor draws changes the physical experiment and its information price.
    """
    eta, bad = _parameters(eta, initial_bad)
    e = WRITE_ERROR
    traces = []
    for h, z0, sensor_fault in product((0, 1), repeat=3):
        pz = bad if z0 else 1-bad
        ps = eta if sensor_fault else 1-eta
        y = h ^ sensor_fault
        for mask in BITS:
            pw = e**sum(mask) * (1-e)**(3-sum(mask))
            bits = tuple(y ^ flag for flag in mask)
            for z1, ph in enumerate(HEALTH[z0]):
                mass = F(1, 2)*pz*ps*pw*ph
                if mass:
                    traces.append({
                        'source': h, 'initial_health': z0,
                        'sensor_fault': sensor_fault, 'sensor_output': y,
                        'write_faults': mask, 'target': (h, z1, bits),
                        'probability': mass,
                    })
    return traces


def raw_acquisition(eta=SENSOR_ERROR, initial_bad=INITIAL_BAD):
    """Joint law on (H,Z,bits), obtained only by summing raw event paths."""
    result = {}
    for trace in acquisition_traces(eta, initial_bad):
        add(result, trace['target'], trace['probability'])
    return result


@lru_cache(None)
def _operators(success=SUCCESS):
    return base_operators(probability(success))


def advance_updates(law, history):
    """Transport each H-submeasure through the same executable D/R history."""
    rows = _law(law)
    for letter in _word(history, history=True):
        rows = tuple(push(row, _operators()[letter]) for row in rows)
    return rows


def preparation_laws(h=2, eta=SENSOR_ERROR, initial_bad=INITIAL_BAD):
    """All histories of the SAME length, from one fixed acquisition protocol.

    Keys document the researcher-selected preparation history. They are not
    exposed to a continuation controller, and mixtures describe uncertainty
    over this preparation class rather than an unpriced runtime randomizer.
    """
    _count(h, 'history length')
    states = {(): acquisition(eta, initial_bad)}
    for _ in range(h):
        states = {
            history+(letter,): tuple(push(row, _operators()[letter]) for row in law)
            for history, law in states.items() for letter in ('D', 'R')
        }
    return {word_id(history): law for history, law in states.items()}


def plan_words(k=4, exact_updates=True):
    """Complete words with k mandatory ordinary updates and at most one M.

    For exact_updates=False the distinct workload permits 0..k updates.
    M is an ADDITIONAL interval in either convention. The terminal readout
    is implicit and counted by execution_cost, not a letter in the word.
    """
    _count(k, 'ordinary update count')
    if type(exact_updates) is not bool:
        raise ValueError('exact_updates must be a boolean')
    words = set()
    counts = (k,) if exact_updates else range(k+1)
    for n in counts:
        for word in product(('D', 'R'), repeat=n):
            words.add(word)
            for position in range(n+1):
                words.add(word[:position]+('M',)+word[position:])
    return tuple(sorted(words, key=lambda word: (len(word), word)))


@lru_cache(None)
def _response(word, success):
    return word_value(_operators(success), word, base_probes()['readout'])


def contrast(law):
    """Return mass(mu_0), mu_1-mu_0 for the existing signature compiler."""
    mu0, mu1 = _law(law)
    return sum(mu0, F(0)), tuple(b-a for a, b in zip(mu0, mu1))


def evaluate(law, word, success=SUCCESS):
    """Fidelity of the complete physical word; H is an evaluator target."""
    word = _word(word)
    success = probability(success)
    offset, signed = contrast(law)
    return offset + dot(signed, _response(word, success))


def response_table(cohort, words, success=SUCCESS):
    """Exact table indexed by preparation and complete-plan identifiers."""
    words = tuple(_word(word) for word in words)
    labels = tuple(word_id(word) for word in words)
    if len(set(labels)) != len(labels):
        raise ValueError('duplicate complete plans')
    success = probability(success)
    columns = tuple(_response(word, success) for word in words)
    result = {}
    for name, law in cohort.items():
        offset, signed = contrast(law)
        result[name] = {label: offset+dot(signed, column)
                        for label, column in zip(labels, columns)}
    return result


@lru_cache(None)
def _raw_channel(z, bits, letter, success):
    if letter == 'M':
        result = raw_maintenance_row((z, bits), success)
    else:
        mode = {'D': 'diffuse', 'R': 'regenerate'}[letter]
        result = raw_update((z, bits), mode, WRITE_ERROR)
    return tuple(result.items())


def _raw_advance(joint, word, success):
    for letter in word:
        after = {}
        for (h, z, bits), mass in joint.items():
            for (z1, bits1), conditional in _raw_channel(z, bits, letter, success):
                add(after, (h, z1, bits1), mass*conditional)
        joint = after
    return joint


def raw_history_law(history, eta=SENSOR_ERROR, initial_bad=INITIAL_BAD):
    """Raw joint preparation for checking acquisition and transport together."""
    history = _word(history, history=True)
    return _raw_advance(raw_acquisition(eta, initial_bad), history, SUCCESS)


@lru_cache(None)
def _raw_readout_one(z, bits):
    error = RATE[z]
    return sum((error**sum(mask)*(1-error)**(6-sum(mask))
                * execute_voter(bits, mask)
                for mask in product((0, 1), repeat=6)), F(0))


def joint_oracle(history, word, eta=SENSOR_ERROR, initial_bad=INITIAL_BAD,
                 success=SUCCESS):
    """Independent joint-state oracle, with an explicitly enumerated readout.

    It does not use the contrast identity, response columns or compiled
    signatures. Existing raw D/R and M channels enumerate their physical
    faults; this oracle separately checks the new H transport and acquisition.
    """
    history = _word(history, history=True)
    word = _word(word)
    success = probability(success)
    joint = _raw_advance(raw_acquisition(eta, initial_bad), history+word, success)
    total = F(0)
    for (h, z, bits), mass in joint.items():
        p_one = _raw_readout_one(z, bits)
        total += mass * (p_one if h else 1-p_one)
    return total


def execution_cost(history, word):
    """Executed physical counts, including acquisition and terminal readout.

    D is a channel update, not a cell write. Three acquisition writes share
    one sensor output. Conditional no-repair still consumes the whole M slot.
    """
    history = _word(history, history=True)
    word = _word(word)
    regenerations = history.count('R')+word.count('R')
    maintenance = word.count('M')
    updates = len(history)+len(word)-maintenance
    votes = regenerations+maintenance+1
    return {
        'installed_sensors': 1,
        'sensor_readings': 1,
        'installed_nands': 6,
        'retained_cells': 3,
        'voter_evaluations': votes,
        'nand_evaluations': 6*votes,
        'cell_writes': 3*(1+regenerations),
        'cell_channel_updates': 3*(1+updates),
        'prepaid_service_slots': maintenance,
        'clock_intervals': 1+len(history)+len(word)+1,
    }


def common_reservation(h=2, k=4):
    """Common worst-case reservation before any acquisition or history.

    Every permitted history and complete word fits this same resource box.
    Unused preparation capacity does not enlarge the declared continuation
    grammar; the exact-k workload remains fixed for every history.
    """
    _count(h, 'history length')
    _count(k, 'ordinary update count')
    return execution_cost(('R',)*h, ('M',)+('R',)*k)


def affine_sensor_value(value_at_zero, eta=SENSOR_ERROR):
    """Exact fair-source identity for one shared BSC observation.

    Subsequent channels depend on H only through Y. Thus every complete
    word satisfies V_eta=1/2+(1-2*eta)(V_0-1/2), including hidden repairs.
    """
    eta = probability(eta, F(1, 2))
    return F(1, 2)+(1-2*eta)*(probability(value_at_zero)-F(1, 2))


def sensor_ceiling(eta=SENSOR_ERROR):
    """Bayes fidelity ceiling from one fair-source BSC observation alone."""
    return 1-probability(eta, F(1, 2))


def contract(h=2, k=4, eta=SENSOR_ERROR, initial_bad=INITIAL_BAD,
             success=SUCCESS, exact_updates=True):
    """Serializable physical and informational scope for a class certificate."""
    _count(h, 'history length')
    _count(k, 'ordinary update count')
    eta, initial_bad = _parameters(eta, initial_bad)
    success = probability(success)
    if type(exact_updates) is not bool:
        raise ValueError('exact_updates must be a boolean')
    return {
        'name': 'reachable-paid-diagnosis-complete-plans',
        'source': 'fair constant H, independent of initial substrate health',
        'source_prior_one': str(SOURCE_PRIOR_ONE),
        'sensor_error': str(eta),
        'sensor_readings': 1,
        'acquisition': 'one Y=H xor sensor fault; broadcast Y; three independent '
                       'writes; then one HEALTH interval',
        'write_error': str(WRITE_ERROR),
        'initial_bad_probability': str(initial_bad),
        'maintenance_success': str(success),
        'history_length': h,
        'history_alphabet': ['D', 'R'],
        'preparation_control': 'researcher-selected history; identifier is not '
                               'available to the continuation controller',
        'continuation_updates': k,
        'exact_updates': exact_updates,
        'maintenance_intervals_at_most': 1,
        'horizon_convention': 'M occupies one additional interval',
        'runtime_access': 'physical three-cell input to inherited voter; '
                          'fixed complete word and phase control',
        'hidden': ['H', 'Z', 'sensor output after acquisition', 'gate faults',
                   'repair result', 'preparation history identifier'],
        'objective': 'terminal voter output equals fixed source H',
        'mixtures': 'uncertainty over reachable preparations; no runtime '
                    'randomizer or mixture label is supplied',
        'evaluation': 'mass(mu0)+(mu1-mu0) K_word g on inherited 16-state kernels',
        'reservation': common_reservation(h, k),
        'sensor_fidelity_ceiling': str(sensor_ceiling(eta)),
    }
