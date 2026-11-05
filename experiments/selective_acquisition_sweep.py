"""Reproducible full priced library and exact finite-horizon noise certificate."""
from fractions import Fraction as F
from dataclasses import asdict
from pathlib import Path
import json,argparse
from cdka.selective_acquisition import *
from cdka.recurrent_maintenance import policies

def jsonable(x):
    if isinstance(x,F):return {'exact':str(x),'value':float(x)}
    if isinstance(x,Enable):return {'gates':x.gates,'output':x.output,'cost':x.cost,'truth':x.truth()}
    if isinstance(x,dict):return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [jsonable(v) for v in x]
    return x

def certificate():
    p=Model();base=evaluate(FRESH);noise=noise_certificate();checks=[]
    selected=[];exact_cases=[]
    for gamma in (F(0),F(1,200),F(1,100),F(1,20)):
        rows=[]
        for pol in policies():rows.extend(dict(r,policy=pol.name) for r in ranking(gamma=gamma,policy=pol))
        best_v=max(r['survival'] for r in rows)
        for eps in (F(0),F(1,10000),F(1,1000),F(1,100)):
            feasible=[r for r in rows if r['survival']>=base['survival']-eps]
            opt=min(feasible,key=total_cost)
            selected.append({'gamma':gamma,'tolerance':eps,'count':len(rows),'best_possible_survival':best_v,'winner':opt,'cost':total_cost(opt)})
        exact_cases.append({'gamma':gamma,'programs_evaluated':len(rows)})
    one=evaluate(ELIDE);critical=(base['writes']-one['writes']-F(1,10))/one['gate_executions']
    # UI recomputes prices on a fixed exact gamma=.01 library; numbers below
    # are floating projections, not reproof for arbitrary gamma.
    table=[]
    for pol in policies():
        for r in ranking(gamma=F(1,100),policy=pol):
            table.append({'policy':pol.name,'truth':r['truth'],'gates':r['gates'],
                'survival':float(r['survival']),'writes':float(r['writes']),'gate_events':float(r['gate_executions']),
                'netlist':{'gates':r['circuit'].gates,'output':r['circuit'].output}})
    sensitivity=localized_gate_sensitivity()
    return jsonable({'revision':'v18','date':'2026-11-05','base_commit':'a32b9a4bf7ecf558ce9bd7fadd90385698ba759f',
        'model':asdict(p),'scope':'Fixed48-state physical evaluator;16 maintenance programs;write-enable NAND grammar at most2 gates;priced workload is NOT an operational-token refund.',
        'baseline':base,'ideal_elision':one,'physical_library':library()[1],
        'hardware_contexts':CONTEXTS,'selection_inputs':'executed service and pre-cycle balance==3 only',
        'cost_example':{'write_price':F(1),'gate_execution_price':F(1,100),'gate_installation_price':F(1,10),
            'baseline':total_cost(base),'ideal_selective':total_cost(one),'critical_gate_execution_price':critical},
        'selected_programs':selected,'exact_cases':exact_cases,'noise_certificate':noise,
        'safe_branch_derivative':sum((r['by_input'][3] for r in sensitivity),F(0)),
        'sensitivity':sensitivity,'noisy_example':evaluate(ELIDE,F(1,200)),
        'refund_counterexample':{'without':refunded_evaluate(0),'with_one_token_credit':refunded_evaluate(1)},
        'verification':{'scientific_tests':16,'catalog_tests':1,'raw_kernel_rows':256,
            'v16_fresh_rows':1024,'annihilation_row_identities':16*96,
            'physical_joint_netlists':16*64,'maximum_channel_programs_per_point':336},
        'ui_fixed_noise':.01,'ui_library':table})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');a=ap.parse_args()
    d=certificate();text=json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n';path=Path('docs/lab/selective-certificate.json')
    if a.write:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if a.check and path.read_text()!=text:raise SystemExit('certificate mismatch')
    print(json.dumps({k:d[k] for k in ('verification','cost_example','safe_branch_derivative')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
