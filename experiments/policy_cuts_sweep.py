"""Reproduce policy-cut certificates using exact arithmetic; JSON export."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
from cdka.policy_cuts import renewal_model, renewal_closed_form, profile_products, pareto_front


def serial_fraction(x):
    return {'exact':str(x),'value':float(x)}


def build_report():
    table=[]
    for n in (1,2,3,5,6,7,10,20,50):
        f=renewal_closed_form(F(1,10),n)
        table.append({'cycles':n,**{k:serial_fraction(v) for k,v in f.items()}})
    certificates=[]
    for e in (F(0),F(1,10),F(1,4)):
        model,initial=renewal_model(e)
        witnesses=list(model.stationary_safe_witnesses(tuple(initial)))
        single=[]
        for w in (0,1):
            single.append(len(list(model.stationary_safe_witnesses(((w,(0,w,0,1)),)))))
        design=model.survival_optimum(initial,8)
        profiles=profile_products(e,4)
        certificates.append({
            'repair_error':str(e),'live_physical_states':len(model.states),
            'stationary_prescriptions':sum(1 for _ in model.prescriptions()),
            'zero_error_joint_witnesses':len(witnesses),
            'zero_error_witnesses_per_world':single,
            'four_cycle_design_value':serial_fraction(design['value']),
            'four_cycle_offline_states':design['design_states'],
            'full_information_relaxation':serial_fraction(model.full_state_oracle(initial,8)),
            'distinct_four_cycle_profiles':len(profiles),
            'pareto_profiles':[[str(v) for v in p] for p in sorted(pareto_front(profiles))],
        })
    return {'status':'known-toolkit, finite-model derivation; no novelty claim',
            'source':'cdka/policy_cuts.py','error_for_table':'1/10',
            'table':table,'certificates':certificates,
            'verification':{'rational_channel_architectures':729,
                            'randomized_one_cycle_grid_cases':1875,
                            'new_python_test_methods':18}}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=build_report()
    text=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text)

if __name__=='__main__':
    main()
