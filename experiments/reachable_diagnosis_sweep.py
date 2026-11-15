"""Reachable paid diagnosis: uniform certificates, controls and measured costs.

python -m experiments.reachable_diagnosis_sweep --write --check
python -m experiments.reachable_diagnosis_sweep --benchmark

Scientific output is deterministic exact rational data. Runtime measurements
are a separate artifact and are never equality-tested as scientific constants.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from statistics import median
from time import perf_counter

from cdka.maintenance_access import base_operators, base_probes, contract as old_contract
from cdka.maintenance_signatures import compile_one_maintenance, verify_one_maintenance
from cdka.reachable_diagnosis import (
    acquisition, preparation_laws, plan_words, response_table, contrast,
    execution_cost, common_reservation, contract, word_id, affine_sensor_value,
    joint_oracle,
)
from cdka.reachable_interfaces import (
    compile_reachable_interface, verify_reachable_interface, admissible_plans,
)
from cdka.reachable_restriction import (
    ORBIT_LAWS, compile_old_restriction, verify_old_restriction,
    restricted_signature, restricted_value, query_cache, orbit_response,
    projected_kernel, domain_preservation,
    contrast_signature, contrast_response, contrast_value, contrast_domain_preservation,
    compile_contrast_restriction, verify_contrast_restriction,
)
from cdka.semantic_closure import ExactBasis, dot, matrix, word_value

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/data'
RESULT_PATH = DATA / 'reachable-diagnosis-results.json'
PARENT_COMMIT = '61e25cc53d3aaaf37eecc1bde0cb9cf9e9821836'


def exact(value):
    if isinstance(value, F): return str(value)
    if isinstance(value, dict): return {str(k): exact(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [exact(v) for v in value]
    return value


def digest(value):
    return sha256(json.dumps(exact(value), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def dense_table(cohort, words, success=F(4,5)):
    rows = response_table(cohort, words, success)
    labels = [word_id(w) for w in words]
    return tuple(tuple(rows[h][p] for p in labels) for h in cohort)


@lru_cache(None)
def cached_queries(k, success=F(4,5), exact_updates=True):
    words = plan_words(k, exact_updates)
    cache = query_cache(base_operators(success), base_probes()['readout'], words)
    return words, cache


def instance(h=2, k=4, eta=F(1,10), success=F(4,5), exact_updates=True):
    cohort = preparation_laws(h, eta)
    words, cache = cached_queries(k, success, exact_updates)
    labels = [word_id(w) for w in words]
    table = dense_table(cohort, words, success)
    for law, row in zip(cohort.values(), table):
        sig = restricted_signature(*law)
        assert row == tuple(restricted_value(sig, q) for q in cache['restricted'])
        sig4 = contrast_signature(*law)
        assert row == tuple(contrast_value(sig4, q) for q in cache['contrast'])
    scope = contract(h, k, eta, success=success, exact_updates=exact_updates)
    scope['parent_commit'] = PARENT_COMMIT
    scope['physical_model_sha256'] = digest({
        'acquisition': acquisition(eta), 'kernels': base_operators(success),
        'terminal': base_probes()['readout'], 'words': words,
    })
    cert = compile_reachable_interface(table, preparation_labels=list(cohort),
                                      plan_labels=labels, contract=scope)
    assert verify_reachable_interface(cert, table, preparation_labels=list(cohort),
                                      plan_labels=labels, contract=scope)
    return cohort, words, table, scope, cert


def summary(cohort, words, table, scope, cert):
    labels = [word_id(w) for w in words]
    d, p = cert['decision'], cert['prediction']
    chosen, maximin = d['chosen_plan'], d['maximin_plan']
    nominal = max(range(len(words)), key=lambda j: sum(row[j] for row in table))
    at = d['plan_regret_witnesses'][chosen]
    rank = ExactBasis(16)
    for law in cohort.values(): rank.add(contrast(law)[1])
    return {
        'history_length': scope['history_length'],
        'ordinary_updates': scope['continuation_updates'],
        'exact_updates': scope['exact_updates'],
        'sensor_error': scope['sensor_error'],
        'maintenance_success': scope['maintenance_success'],
        'preparations': len(cohort), 'plans': len(words),
        'response_entries': len(cohort)*len(words),
        'contrast_row_rank': len(rank.originals),
        'common_optimal_plans': [labels[j] for j in d['common_optimal_plans']],
        'minimax_plan': labels[chosen], 'minimax_regret': d['minimax_regret'],
        'minimax_minimum_fidelity': p['lower'][chosen],
        'minimax_worst_regret_history': list(cohort)[at['preparation']],
        'minimax_witness_alternative': labels[at['comparator_plan']],
        'maximin_plan': labels[maximin], 'maximin_value': d['maximin_value'],
        'maximin_regret': d['plan_regrets'][maximin],
        'nominal_plan': labels[nominal], 'nominal_regret': d['plan_regrets'][nominal],
        'free_prediction_radius': p['free_radius'],
        'mean_law_prediction_radius': p['uniform_law_radius'],
        'minimax_individually_optimal_somewhere': any(
            row[chosen] == max(row) for row in table),
    }


def lifted(operators, probe):
    n = len(probe)
    ops = {name: matrix([{h*n+j: p for j,p in row.items()}
                          for h in (0,1) for row in kernel])
           for name, kernel in operators.items()}
    probes = {'mass': (F(1),)*(2*n),
              'correct': tuple(1-x for x in probe)+tuple(probe)}
    return ops, probes


def build():
    cohort, words, table, scope, cert = instance()
    plans, histories = [word_id(w) for w in words], list(cohort)
    zero_sensor = dense_table(preparation_laws(2, F(0)), words)
    for i,row in enumerate(table):
        for j,value in enumerate(row):
            assert value == affine_sensor_value(zero_sensor[i][j], F(1,10))
            assert value <= F(9,10)
    reservation = common_reservation(2,4)
    costs = {h:{p:execution_cost(h,w) for p,w in zip(plans,words)} for h in histories}
    for values in costs.values():
        for cost in values.values():
            assert all(value <= reservation[name] for name,value in cost.items())
    raw_checks = 0
    for h in histories:
        for p in plans:
            assert joint_oracle(h,p) == table[histories.index(h)][plans.index(p)]
            raw_checks += 1

    ops, probes = base_operators(), base_probes()
    old = json.loads((DATA/'maintenance-access-closed-certificate.json').read_text())
    assert verify_one_maintenance(old,{k:ops[k] for k in ('D','R')},ops['M'],
                                  probes,contract=old_contract())
    old_basis = tuple(tuple(map(F,v)) for v in old['old']['basis'])
    restriction = compile_old_restriction(old_basis, contract={'parent':PARENT_COMMIT})
    assert verify_old_restriction(restriction,old_basis,contract={'parent':PARENT_COMMIT})
    restriction4 = compile_contrast_restriction(old_basis,contract={'parent':PARENT_COMMIT})
    assert verify_contrast_restriction(restriction4,old_basis,contract={'parent':PARENT_COMMIT})

    wrong_ops = {name:projected_kernel(q) for name,q in ops.items()}
    wrong_columns = tuple(word_value(wrong_ops,w,orbit_response(probes['readout'])) for w in words)
    wrong_values = tuple(tuple(restricted_value(restricted_signature(*law),q)
                               for q in wrong_columns) for law in cohort.values())
    errors = [(abs(wrong_values[i][j]-table[i][j]),i,j)
              for i in range(len(cohort)) for j in range(len(words))]
    error, i, j = max(errors)
    assert error > 0

    lift_ops,lift_probes = lifted(ops,probes['readout'])
    lift_cert = compile_one_maintenance({k:lift_ops[k] for k in ('D','R')},
                                       lift_ops['M'],lift_probes,contract={'target':'readout=H'})
    assert verify_one_maintenance(lift_cert,{k:lift_ops[k] for k in ('D','R')},
                                  lift_ops['M'],lift_probes,contract={'target':'readout=H'})
    full_columns = [word_value(lift_ops,w,lift_probes['correct']) for w in words]
    for law,row in zip(cohort.values(),table):
        assert tuple(dot(law[0]+law[1],q) for q in full_columns) == row

    cases = []
    for h in (0,2,4,6):
        args = instance(h=h)
        cases.append(summary(*args))
    controls = {}
    for label,kwargs in (
        ('optional_updates',{'k':4,'exact_updates':False}),
        ('zero_repair',{'success':F(0)}),
        ('uninformative_sensor',{'eta':F(1,2)}),
    ):
        controls[label] = summary(*instance(**kwargs))

    gates = []
    for delta,floor in ((F(1,500),F(21,25)),(F(3,1000),F(21,25)),
                         (F(3,1000),F(17,20)),(F(1,200),F(17,20))):
        admissible = admissible_plans(cert,maximum_regret=delta,minimum_value=floor)
        gates.append({'maximum_regret':str(delta),'minimum_fidelity':str(floor),
                      'admissible_plans':[plans[j] for j in admissible]})
    return exact({
        'schema':'cdka.reachable-diagnosis-experiment/v1',
        'contract':scope,
        'fixture':{'histories':histories,'plans':plans,'values':table,
                   'values_sensor_zero':zero_sensor,'certificate':cert,
                   'summary':summary(cohort,words,table,scope,cert),
                   'costs':{'reservation':reservation,'executed':costs}},
        'reachability_restriction':{
            'scope':'all exchangeable input laws on (Z,bits), including mass',
            'orbit_dimension':8,'old_response_restriction_certificate':restriction,
            'domain_preservation':{k:domain_preservation(q) for k,q in ops.items()},
            'contrast_dimension':4,'old_contrast_restriction_certificate':restriction4,
            'contrast_domain_preservation':{k:contrast_domain_preservation(q) for k,q in ops.items()},
            'naive_projected_maintenance':{
                'maximum_fixture_error':error,'history':histories[i],'plan':plans[j],
                'correct_value':table[i][j],'incorrect_value':wrong_values[i][j]},
        },
        'target_change_control':{'unrestricted_states':32,
                                'old_rank':lift_cert['old']['dimension'],
                                'maintenance_rank':lift_cert['with_maintenance']['dimension'],
                                'certificate_verified':True},
        'history_scaling':cases,'controls':controls,'joint_gates':gates,
        'validation':{'raw_joint_plan_checks':raw_checks,
                      'full32_contrast16_boundary8_contrast4_equal_entries':len(cohort)*len(words),
                      'affine_sensor_equal_entries':len(cohort)*len(words),
                      'certificate_verified':True,'restriction_certificate_verified':True},
    })


def _timed(call, repeats=3):
    durations=[]; result=None
    for _ in range(repeats):
        start=perf_counter(); result=call(); durations.append(perf_counter()-start)
    return result, median(durations), durations


def _bits(values):
    return max(max(x.numerator.bit_length(),x.denominator.bit_length())
               for row in values for x in row)


def benchmark():
    """Fair cached-backward baselines, with compilation and reuse separated."""
    setup_started=perf_counter()
    ops,g = base_operators(),base_probes()['readout']
    setup_time=perf_counter()-setup_started
    words=plan_words(4)
    lift_started=perf_counter()
    lift_ops,lift_probes=lifted(ops,g)
    lift_time=perf_counter()-lift_started
    c32,t32,rep32=_timed(lambda:tuple(word_value(lift_ops,w,lift_probes['correct']) for w in words))
    c16,t16,rep16=_timed(lambda:tuple(word_value(ops,w,g) for w in words))
    c8,projection_time,projection_repeats=_timed(lambda:tuple(orbit_response(v) for v in c16))
    c4,projection4_time,projection4_repeats=_timed(lambda:tuple(contrast_response(v) for v in c16))
    preparation_started=perf_counter();cohort=preparation_laws(6)
    preparation_time=perf_counter()-preparation_started
    laws32,e32,er32=_timed(lambda:[law[0]+law[1] for law in cohort.values()])
    laws16,e16,er16=_timed(lambda:[contrast(law) for law in cohort.values()])
    laws8,e8,er8=_timed(lambda:[restricted_signature(*law) for law in cohort.values()])
    laws4,e4,er4=_timed(lambda:[contrast_signature(*law) for law in cohort.values()])
    def all32(): return tuple(tuple(dot(law,q) for q in c32) for law in laws32)
    def all16(): return tuple(tuple(offset+dot(law,q) for q in c16) for offset,law in laws16)
    def all8(): return tuple(tuple(offset+dot(law,q) for q in c8) for offset,law in laws8)
    def all4(): return tuple(tuple(offset+dot(law,q) for q in c4) for offset,law in laws4)
    v32,q32,r32=_timed(all32);v16,q16,r16=_timed(all16);v8,q8,r8=_timed(all8)
    v4,q4,r4=_timed(all4)
    assert v32==v16==v8==v4
    scope=contract(6,4)
    kwargs={'preparation_labels':list(cohort),'plan_labels':[word_id(w) for w in words],
            'contract':scope}
    cert,ct,cr=_timed(lambda:compile_reachable_interface(v8,**kwargs))
    _,vt,vr=_timed(lambda:verify_reachable_interface(cert,v8,**kwargs))
    cases=[]
    for name,cache,compile_time,encoding_time,query_time in (
        ('full_joint_32',c32,t32+lift_time,e32,q32),('contrast_16',c16,t16,e16,q16),
        ('reachable_boundary_8',c8,t16+projection_time,e8,q8),
        ('antisymmetric_contrast_4',c4,t16+projection4_time,e4,q4)):
        payload=json.dumps(exact(cache),separators=(',',':')).encode()
        cases.append({'method':name,'compile_seconds':compile_time,
                      'preparation_encoding_seconds':encoding_time,
                      'query_batch_seconds':query_time,
                      'cache_rational_entries':sum(map(len,cache)),
                      'cache_json_bytes':len(payload),'max_rational_bits':_bits(cache),
                      'total_seconds_for_query_batches':{
                          str(n):setup_time+preparation_time+encoding_time+compile_time+n*query_time
                          for n in (1,10,100)}})
    break_even=max(0.,(projection_time+e8-e16)/(q16-q8)) if q16>q8 else None
    break_even4=max(0.,(projection4_time+e4-e16)/(q16-q4)) if q16>q4 else None
    return {'schema':'cdka.reachable-diagnosis-benchmark/v1',
            'environment':{'python':platform.python_version(),'platform':platform.platform()},
            'parameters':{'history_length':6,'histories':64,'plans':96,
                          'responses_per_batch':6144,'repetitions':3,
                          'arithmetic':'fractions.Fraction, exact'},
            'shared_kernel_seconds':setup_time,
            'shared_preparation_seconds':preparation_time,
            'total_time_convention':'kernel+preparation+encoding+query compilation+N query batches; class certificate separately priced',
            'methods':cases,'boundary_vs_contrast_break_even_batches':break_even,
            'contrast4_vs_contrast16_break_even_batches':break_even4,
            'class_certificate':{'compile_seconds':ct,'verify_seconds':vt,
                                 'json_bytes':len(json.dumps(cert,separators=(',',':')).encode())},
            'all_responses_equal':True,
            'timing_samples':{'compile32':rep32,'compile16':rep16,'projection8':projection_repeats,
                              'projection4':projection4_repeats,
                              'encoding32':er32,'encoding16':er16,'encoding8':er8,'encoding4':er4,
                              'query32':r32,'query16':r16,'query8':r8,'query4':r4,
                              'certificate_compile':cr,'certificate_verify':vr},
            'limits':['local measured timings; no universal speedup claim',
                      'all 2^h histories and all (k+2)*2^k plans are enumerated',
                      'input-domain reduction is not a closed maintenance quotient'],
            }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--benchmark',action='store_true')
    args=parser.parse_args()
    if args.benchmark:
        measured=benchmark()
        path=DATA/'reachable-diagnosis-benchmark.json'
        path.write_text(json.dumps(measured,indent=2,sort_keys=True)+'\n')
        print(json.dumps(measured,indent=2));return
    result=build()
    if args.write: RESULT_PATH.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    if args.check:
        if json.loads(RESULT_PATH.read_text())!=result: raise AssertionError('stored reachable certificate/data differ')
    print(json.dumps({'summary':result['fixture']['summary'],
                      'gates':result['joint_gates'],'validation':result['validation']},indent=2))


if __name__=='__main__': main()
