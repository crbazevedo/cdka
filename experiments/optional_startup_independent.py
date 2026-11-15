"""Independent raw-physics oracle for every omitted-startup blind program.

This evaluator projects away the unread diagnostic register before propagation.
It does not import shared_budget or optional_startup, nor their event, row,
initialization or probability helpers.  The inherited Model supplies parameters
and the inherited Enable library supplies the declared circuit representatives;
sensor and NAND fault events are enumerated directly here.  Both endpoints keep
charges incurred before every stopped branch.  Output hashes cover every exact
survival/spending pair, not only the selected winner.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json

from cdka.recurrent_maintenance import Model
from cdka.selective_acquisition import library


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/data/optional-startup-independent.json'
SOURCES = ('experiments/optional_startup_independent.py',
           'cdka/recurrent_maintenance.py', 'cdka/selective_acquisition.py')
PRICE_GRID = tuple(product((0, 1, 2), (0, 6, 12, 24), (0, 6)))
MODES = ('skip', 'service')
VOTER = ((0, 1), (0, 2), (1, 2), (3, 4), (6, 6), (5, 7))
PLANT = Model()
ENABLES, _ = library(2)


@lru_cache(None)
def flags(size, error):
    return tuple((f, error ** sum(f) * (1 - error) ** (size - sum(f)))
                 for f in product((0, 1), repeat=size))


def execute(wires, gates, output, faults):
    wires = list(wires)
    for (left, right), fault in zip(gates, faults):
        wires.append((1 - (wires[left] & wires[right])) ^ fault)
    return wires[output]


@lru_cache(None)
def task_probability(health):
    result = F(0)
    for world in (0, 1):
        for sensor_flags, ps in flags(3, PLANT.task_sensor_error):
            readings = tuple(world ^ f for f in sensor_flags)
            for gate_flags, pg in flags(6, PLANT.rate(health)):
                if execute(readings, VOTER, 8, gate_flags) == world:
                    result += ps * pg / 2
    return result


@lru_cache(None)
def projected_row(gate, write, at3, at4, enable_index, state, terminal):
    """Return the projected live kernel and unconditional incurred row cost."""
    health, balance = state
    circuit = ENABLES[enable_index]
    middle = int(72 <= balance < 96)
    mode = 'skip' if balance < 72 else (at3 if middle else at4)
    service = int(mode == 'service' and balance >= 72 + 6 * gate)
    expense = F(48 * service)
    after_service = balance - 48 * service
    procedure = 1 - PLANT.procedure_failure if service else F(1)
    health_law = ((0, PLANT.restoration), (health, 1 - PLANT.restoration)) \
        if service else ((health, F(1)),)
    out = defaultdict(F)
    for post_health, ph in health_law:
        mass = procedure * ph
        task_cost = 24 + 6 * gate
        if after_service < task_cost:
            continue
        expense += mass * task_cost
        after_task = after_service - task_cost
        mass *= task_probability(post_health)
        if terminal:
            out[(post_health, after_task)] += mass
            continue
        enable_cost = circuit.cost * gate
        if after_task < enable_cost:
            continue
        expense += mass * enable_cost
        after_enable = after_task - enable_cost
        for fault_flags, pf in flags(circuit.cost, PLANT.rate(post_health)):
            enabled = execute((0, 1, service, middle), circuit.gates,
                              circuit.output, fault_flags)
            branch_mass = mass * pf
            if enabled and after_enable < write:
                continue
            write_cost = enabled * write
            expense += branch_mass * write_cost
            successor_balance = min(96, after_enable - write_cost + 48)
            # The sampled diagnostic law sums to one and no future primitive
            # can read it in this syntactically blind controller family.
            if post_health == 0:
                out[(0, successor_balance)] += branch_mass * (1 - PLANT.degradation)
                out[(1, successor_balance)] += branch_mass * PLANT.degradation
            else:
                out[(1, successor_balance)] += branch_mass
    return tuple(out.items()), expense


def evaluate(prices, at3, at4, enable_index, objective, horizon=8):
    gate, write, setup = prices
    if prices not in PRICE_GRID or at3 not in MODES or at4 not in MODES:
        raise ValueError('only the declared price grid and blind grammar apply')
    if objective not in ('tasks', 'cycles') or type(horizon) is not int or horizon < 0:
        raise ValueError('finite task/cycle endpoint required')
    circuit = ENABLES[enable_index]
    balance = 72 - circuit.cost * setup
    law = {(0, balance): F(1, 2), (1, balance): F(1, 2)}
    spent = F(24 + circuit.cost * setup)
    for step in range(horizon):
        following = defaultdict(F)
        for state, mass in law.items():
            targets, row_cost = projected_row(gate, write, at3, at4,
                enable_index, state, objective == 'tasks' and step == horizon - 1)
            spent += mass * row_cost
            for successor, probability in targets:
                following[successor] += mass * probability
        law = dict(following)
    return sum(law.values(), F(0)), spent


def rows(prices, objective, horizon=8):
    result = []
    for at3, at4 in product(MODES, repeat=2):
        for enable_index in range(len(ENABLES)):
            survival, spent = evaluate(prices, at3, at4, enable_index, objective, horizon)
            result.append(dict(program=f'{at3}/{at4}:e{enable_index:02d}',
                               survival=survival, spent=spent))
    return result


def response_hash(responses):
    values = [(r['program'], str(r['survival']), str(r['spent']))
              for r in sorted(responses, key=lambda r: r['program'])]
    return sha256(json.dumps(values, separators=(',', ':')).encode()).hexdigest()


def packed(response):
    return dict(program=response['program'], **{k: dict(exact=str(response[k]),
                value=float(response[k])) for k in ('survival', 'spent')})


def run():
    cases = []
    for prices in PRICE_GRID:
        case = dict(prices=dict(zip(('gate', 'write', 'setup'), prices)))
        for objective in ('tasks', 'cycles'):
            responses = rows(prices, objective)
            winner = min(responses, key=lambda r: (-r['survival'], r['spent'], r['program']))
            case[objective] = dict(program_count=len(responses),
                complete_response_sha256=response_hash(responses),
                best_survival=packed(winner))
        cases.append(case)
    return dict(schema='cdka.optional-startup-independent/v1', date='2026-11-15',
        date_basis='Europe/Lisbon', parent_commit='24d1e35ecde75defd495b5272bfb653f427bf528',
        purpose='Independent exact physical check of all omitted-startup blind responses',
        physical_baseline='Fixed SB prices, plant, event order, gross capital and task/cycle endpoints',
        independence='Direct sensor and NAND flags; projected health/balance law; no shared_budget or optional_startup evaluator imports',
        scope='84 blind representatives per price; no initial acquisition; later paid writes allowed but never read',
        source_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES},
        horizon=8, endpoints=['tasks', 'cycles'], price_points=24,
        exact_response_count=24 * 84 * 2,
        digest_order='Lexical base program identifier; JSON tuples(program, exact survival, exact spending), compact separators',
        cases=cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.write:
        OUTPUT.write_text(text)
    if args.check and (not OUTPUT.exists() or OUTPUT.read_text() != text):
        raise ValueError('Stale or missing independent optional-startup certificate')
    print(json.dumps(dict(price_points=24, exact_responses=24 * 84 * 2,
                          endpoint_certificates=48)))


if __name__ == '__main__':
    main()
