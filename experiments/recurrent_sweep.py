"""Reproduce a bounded recurrent operational-closure experiment, not sampling."""
from fractions import Fraction as F
from pathlib import Path
from dataclasses import asdict
import argparse,json,time,hashlib
from cdka.recurrent_maintenance import *


def scalar(x):
    return {'exact':str(x),'value':float(x)} if isinstance(x,F) else x


def package(x):
    if isinstance(x,F):return scalar(x)
    if isinstance(x,Policy):return x.name
    if isinstance(x,dict):return {str(k):package(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [package(v) for v in x]
    return x


def certificate():
    p=Model();ranking=all_stationary(p,8)
    best=ranking[0];blind=max((r for r in ranking if r['policy'].at3 in ('skip','service') and r['policy'].at4 in ('skip','service')),key=lambda x:x['value'])
    reports={}
    for pol in (Policy(),Policy('service','service'),Policy('skip','skip')):
        r=run_summary(p,pol,8)
        r.pop('terminal_law');r['curve']=tuple(float(v) for v in forward(p,pol,64)[0])
        reports[pol.name]=r
    traces=[]
    sources=((0,(0,0,0),3),(1,(0,0,0),3),(1,(1,1,1),3),(1,(1,1,1),2))
    for i,s in enumerate(sources):
        traces.extend({'source_id':i,'source':s,**r} for r in event_traces(p,Policy(),s))
    # An independent direct row check is also enforced by the test suite.
    verified=0
    for policy in policies():
        for phase in p.phases():
            a=push(emission(p,phase),lambda s:physical_row(p,policy,s))
            b=push(reduced_row(p,policy,phase),lambda s:emission(p,s))
            if a!=b:raise AssertionError('intertwining failed')
            verified+=1
    ablated=Model(diagnostic_error=F(1,2))
    return package({
        'revision':'v16','date':'2026-11-05','base_commit':'2eb1da7b635da2165e3b767440371a69583df3d0',
        'model':asdict(p),'voter':VOTER,
        'scope':'Stationary resource-indexed physical routing library; no perfect health input. New recurrent task, not directly comparable to terminal v15 survival percentages.',
        'counts':{'microstates':64,'regenerative_phases':12,'joint_programs':16,'blind_programs':4,
                  'intertwining_rows':verified,'independent_micro_rows':192,'scientific_python_tests':17,
                  'task_flag_cases':2048,'conditional_trace_rows':len(traces)},
        'task_success_by_health':[task_success(p,z) for z in (0,1)],
        'horizon':8,'ranking':ranking,'best':best,'best_blind':blind,
        'illustrative_separator_target':F(183,200),
        'policy_reports':reports,
        'ablation_uninformative':{'vote_value':forward(ablated,Policy(),8)[0][-1],
                                'best_value':all_stationary(ablated,8)[0]['value']},
        'traces':traces,
        'theory':{'factorization':'K_pi=A_pi E; M_pi=E A_pi; E K_pi=M_pi E',
                  'future_invariance':'(lambda E) K_pi^n=(lambda M_pi^n) E',
                  'uniform_survival_bound':task_success(p,0),
                  'conditional_targets':'The 91.5% separating target is for the fair-prior average, not a per-health guarantee.'},
    })


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    data=certificate();text=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    path=Path('docs/lab/recurrent-certificate.json')
    if args.write:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if args.check and path.read_text()!=text:raise SystemExit('certificate mismatch')
    print(json.dumps({k:data[k] for k in ('counts','best','best_blind','ablation_uninformative')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
