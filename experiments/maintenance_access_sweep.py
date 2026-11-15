"""Rebuild exact maintenance-access evidence and its portable certificates.

Run: python -m experiments.maintenance_access_sweep --write --check
No sampling, external solver, or third-party scientific dependency is used.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from cdka.maintenance_access import (
    BASE_COMMIT, SUCCESS, STATES, PAID_STATES, PAID_INDEX, MACRO_STATES,
    MACRO_INDEX, contract, base_operators, base_probes, paid_operators,
    paid_probes, macro_operators, paid_label, maintenance_row,
    raw_maintenance_row, witness_laws, word_cost,
)
from cdka.maintenance_signatures import (
    compile_one_maintenance, verify_one_maintenance, finite_horizon,
    verify_finite_horizon, separator,
)
from cdka.semantic_closure import close_continuations, dot, word_value, matrix, vector


def words(max_updates=2):
    """All <=h D/R updates with zero or one additional M, no duplicates."""
    for n in range(max_updates+1):
        for w in product(('D', 'R'), repeat=n):
            yield w
            for k in range(n+1):
                yield w[:k]+('M',)+w[k:]


def exact(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): exact(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [exact(v) for v in x]
    return x


def build():
    ops=base_operators(); probes=base_probes(); old={k:ops[k] for k in ('D','R')}
    scope=contract()
    cert=compile_one_maintenance(old,ops['M'],probes,contract=scope)
    assert verify_one_maintenance(cert,old,ops['M'],probes,contract=scope)
    finite=finite_horizon(old,ops['M'],probes,max_updates=2,contract=scope)
    assert verify_finite_horizon(finite,old,ops['M'],probes,contract=scope)
    zero_ops=base_operators(F(0))
    zero=compile_one_maintenance(old,zero_ops['M'],probes,contract=contract(F(0)))
    assert verify_one_maintenance(zero,old,zero_ops['M'],probes,contract=contract(F(0)))
    assert zero['old']['dimension']==zero['with_maintenance']['dimension']==10

    end_ops=base_operators(F(1))
    affine_entries=0
    for i,row in enumerate(ops['M']):
        for j in range(16):
            assert row.get(j,F(0)) == zero_ops['M'][i].get(j,F(0)) + SUCCESS*(
                end_ops['M'][i].get(j,F(0))-zero_ops['M'][i].get(j,F(0)))
            affine_entries+=1

    raw_rows=0
    for s in (F(0),SUCCESS,F(1)):
        for state in STATES:
            assert maintenance_row(state,s)==raw_maintenance_row(state,s)
            raw_rows+=1
    paid=paid_operators(); pp=paid_probes(); mac=macro_operators()
    quotient_rows=0
    for label,q in paid.items():
        for i,state in enumerate(PAID_STATES):
            aggregated={}
            for j,p in q[i].items():
                target=MACRO_INDEX[paid_label(PAID_STATES[j])]
                aggregated[target]=aggregated.get(target,F(0))+p
            assert aggregated==mac[label][MACRO_INDEX[paid_label(state)]]
            quotient_rows+=1
    full=close_continuations(paid,pp)
    assert full.verify() and full.dimension==22

    left,right=witness_laws()
    ordinary=close_continuations(old,probes)
    assert ordinary.equivalent(left,right)
    bounded=[]
    for word in words(2):
        response=word_value(ops,word,probes['readout'])
        x,y=dot(left,response),dot(right,response)
        e0=word_value(zero_ops,word,probes['readout'])
        e1=word_value(end_ops,word,probes['readout'])
        l0,r0=dot(left,e0),dot(right,e0)
        l1,r1=dot(left,e1),dot(right,e1)
        assert l0==r0
        assert x==l0+SUCCESS*(l1-l0) and y==r0+SUCCESS*(r1-r0)
        bounded.append({'word':word,'left':x,'right':y,'difference':x-y,
                        'left_at_zero':l0,'right_at_zero':r0,
                        'left_at_one':l1,'right_at_one':r1,'cost':word_cost(word)})
    worst=max(bounded,key=lambda row:abs(row['difference']))
    gap=abs(worst['difference']); unit_gap=gap/SUCCESS
    tolerance=F(1,200)
    threshold=2*tolerance/unit_gap
    assert F(0)<threshold<F(1)

    g=probes['readout']
    extra=dict(old)
    extra['read1']=matrix([{i:p} for i,p in enumerate(g)])
    extra['read0']=matrix([{i:1-p} for i,p in enumerate(g)])
    reading=close_continuations(extra,probes)
    assert reading.dimension==12
    read_gap=dot(left,vector(x*x for x in g))-dot(right,vector(x*x for x in g))

    report={
        'schema':'cdka.maintenance-access-results/v1','base_commit':BASE_COMMIT,
        'contract':scope,
        'result':{'physical_states':32,'markov_classes':24,'linear_coordinates':22,
                  'old_closed_rank':cert['old']['dimension'],
                  'one_maintenance_closed_rank':cert['with_maintenance']['dimension'],
                  'two_ordinary_updates_ranks':{'without_M':7,'at_most_one_M':12},
                  'zero_success_global_rank':20,
                  'nonzero_success_global_rank':22,
                  'nonzero_success_scope':'all rational/real s in (0,1], by affine kernel and invariant-span argument',
                  'known_mass':'ranks include mass for unnormalized laws; not physical bits'},
        'construction':cert['construction'],
        'finite_candidate_evaluations':finite['candidate_evaluations'],
        'paid_closure':{'profile':full.profile,'candidate_evaluations':full.attempts},
        'witness':{'left':left,'right':right,
                   'old_terminal_value':dot(left,g),
                   'separator':separator(cert,left,right),
                   'maximum_gap_bounded':gap,'maximizer_word':worst['word']},
        'bounded_words':bounded,
        'approximation':{'scope':'only the two displayed laws and the 24 declared words',
                         'common_prediction_minimax_error':gap/2,
                         'attaining_predictor':'midpoint law (left+right)/2',
                         'error_tolerance':tolerance,
                         'success_threshold':threshold,
                         'gap_per_unit_success':unit_gap},
        'negative_controls':{'zero_repair_success_gap':F(0),
                              'intermediate_read_rank':reading.dimension,
                              'intermediate_read_joint_event_gap':read_gap,
                              'intermediate_read_in_main_library':False},
        'verification':{'raw_maintenance_rows':raw_rows,
                         'paid_to_macro_rows':quotient_rows,
                         'affine_kernel_entries':affine_entries,
                         'bounded_words':len(bounded),
                         'exact_arithmetic':'fractions.Fraction',
                         'old_certificate_valid':True,'finite_certificate_valid':True,
                         'zero_success_certificate_valid':True},
    }
    return {'maintenance-access-results.json':exact(report),
            'maintenance-access-closed-certificate.json':cert,
            'maintenance-access-finite-certificate.json':finite,
            'maintenance-access-zero-certificate.json':zero}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    output=Path(__file__).resolve().parents[1]/'docs'/'data'
    generated=build()
    if args.write: output.mkdir(parents=True,exist_ok=True)
    for name,data in generated.items():
        rendered=json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
        path=output/name
        if args.write:path.write_text(rendered)
        if args.check and (not path.exists() or path.read_text()!=rendered):
            raise SystemExit('certificate differs: '+str(path))
    r=generated['maintenance-access-results.json']
    print(json.dumps({'ranks':r['result'],'verification':r['verification'],
                      'construction':r['construction'],
                      'pair_tolerance_threshold':r['approximation']['success_threshold']},
                     ensure_ascii=False,indent=2))


if __name__=='__main__':main()
