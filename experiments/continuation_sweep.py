"""Reproduce exact continuation-interface certificates from the v6 kernel."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from cdka.continuation_interfaces import (
    Contract,plans,upper_envelope,equal_signal_joint,best_code,
    exact_code_count,regret_breakdown,
)


def payload():
    tables={}
    for horizon in (1,2):
        library=plans(horizon=horizon);hull=upper_envelope(library)
        tables[str(horizon)]={
            'enumerated':len(library),
            'plans':[{'id':i,'first':library[i].first,
                      'second':[[list(obs),a] for obs,a in library[i].second],
                      'alpha':[float(x) for x in library[i].alpha],
                      'exact_alpha':[str(x) for x in library[i].alpha]}
                     for _,_,i in hull],
            'intervals':[{'lo':float(lo),'hi':float(hi),'id':i,
                          'exact_lo':str(lo),'exact_hi':str(hi)} for lo,hi,i in hull],
        }
    joint=equal_signal_joint();lib=plans();best=[]
    for cap in (1,2,3):
        r=best_code(lib,joint,cap);d=regret_breakdown(Contract(),lib,joint,r)
        best.append({'capacity':cap,'value':float(r['value']),'exact_value':str(r['value']),
                     'loss':float(r['loss']),'exact_loss':str(r['loss']),
                     'encoding':list(r['labels']),
                     'selected_plans':{str(k):v for k,v in r['plans'].items()},
                     'root_loss':float(d['initial_action_loss']),
                     'tail_loss':float(d['continuation_loss'])})
    cardinality=[]
    for tail in (F(0),F(1,100),F(3,100),F(1,10),F(3,20),F(1,5),F(1,2)):
        j=equal_signal_joint(tail)
        cardinality.append({'tail':float(tail),
                            'one_epoch':exact_code_count(plans(horizon=1),j),
                            'two_epochs':exact_code_count(lib,j)})
    return {'revision':'v9','base_commit':'b0176b3d6fbdded67caad1cbe5cb4ae4521a5d1a',
            'contract':'v6 Contract; k=0,b=4; hidden health; physical syndrome/resources after each step',
            'scope':'K is diagnostic-code states, not all controller memory; two-epoch exact library',
            'tables':tables,'default':best,'cardinality':cardinality}


def main():
    cli=argparse.ArgumentParser();cli.add_argument('--write',action='store_true');cli.add_argument('--check',action='store_true');args=cli.parse_args()
    data=payload();root=Path(__file__).resolve().parents[1]
    dest=root/'docs/lab/continuation-data.mjs'
    text='// Generated from exact Fraction certificates; do not hand-edit.\nexport const DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n'
    if args.write:
        dest.write_text(text);print('Written:',dest)
    elif args.check:
        if dest.read_text()!=text:raise AssertionError('Continuation fixtures are stale: run --write')
        print('Exact Python and browser fixtures match.')
    else:
        print(json.dumps({'default':data['default'],'cardinality':data['cardinality']},indent=2))

if __name__=='__main__':main()
