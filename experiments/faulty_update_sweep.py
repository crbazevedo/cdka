"""Exact v14 certificate, terminal channels and complete gate-fault traces."""
from fractions import Fraction as F
from pathlib import Path
from dataclasses import is_dataclass,asdict
import json,argparse
from cdka.faulty_updates import *


def clean(x):
    if isinstance(x,F):return {'exact':str(x),'value':float(x)}
    if is_dataclass(x):return clean(asdict(x))
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x


def certificate():
    lib,stats=complete_library();proof=fixed_input_certificate()
    balanced=PhysicalCircuit(((1,4),(2,3),(1,6),(5,7)),8)
    winner=proof['circuit'];encoding=(3,0,0)
    examples=[]
    for p,g,q in ((F(0),F(0),F(0)),(F(1,100),F(0),F(0)),
                  (F(1,100),F(1,1000),F(0)),(F(1,100),F(1,100),F(0)),
                  (F(1,100),F(1,50),F(0)),(F(1,10),F(1,1000),F(0)),
                  (F(1,100),F(1,1000),F(1,1000))):
        for cap in (0,2,3,4):examples.append(synthesize(p,g,q,cap))
    return clean({'revision':'v14','date':'2026-11-03',
        'parent_commit':'10d963c5dd190ce10f90270b88e0ee6373ea2efe',
        'scope':'v13 SERVICE-first task unchanged; 0..4 independent faulty NANDs, common input and output BSCs; fixed command bypass retained. No recurrent gate-maintenance claim.',
        'payoff_table':payoff_table(),'baseline':bypass_value(),
        'library':stats,'channels':[{'circuit':c,'profile':profile} for c,profile in lib],
        'continuous_certificate':proof,'examples':examples,
        'shared_fault':shared_fault_witness(),
        'same_function':{'encoding':encoding,'p':F(1,100),'gamma':F(1,100),
                         'balanced':balanced,'sequential':winner,
                         'balanced_value':evaluate(balanced,encoding,F(1,100),F(1,100)),
                         'sequential_value':evaluate(winner,encoding,F(1,100),F(1,100)),
                         'balanced_influences':first_order_influences(balanced,encoding),
                         'sequential_influences':first_order_influences(winner,encoding)},
        'last_gate_cutoffs':[{'p':p,'gamma_cutoff':last_gate_cutoff(p)} for p in (F(0),F(1,100),F(1,10))],
        'traces':[{'word':w,'syndrome':k,'events':runtime_fault_traces(winner,w,k,F(1,100))}
                  for w in range(4) for k in range(2)],
        'evidence':{'scientific_python_tests':15,'scalar_gate_fault_checks':3120,
                    'complete_conditional_traces':128,'rooted_netlists':12395,
                    'terminal_channels':611,'encoder_channel_programs':39104,
                    'continuous_rational_polynomial_checks':8854}})


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    data=certificate();text=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    path=Path('docs/lab/faulty-update-data.json')
    if args.write:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if args.check and path.read_text()!=text:raise SystemExit('exact certificate drift')
    print(json.dumps({key:data[key] for key in ('revision','library','last_gate_cutoffs','same_function','evidence')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
