"""Generate/check exact v13 physical update/circuit certificate."""
from fractions import Fraction as F
from pathlib import Path
import json,argparse
from cdka.physical_update import *


def clean(x):
    if isinstance(x,F):return {'exact':str(x),'value':float(x)}
    if isinstance(x,Surd):return {'a':str(x.a),'b':str(x.b),'d':str(x.d),'value':x.approximate()}
    if isinstance(x,Circuit):return {'truth':x.output,'gates':x.gates,'cost':x.cost}
    if isinstance(x,dict):return {str(k):clean(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v)for v in x]
    return x


def certificate():
    lib,profile=nand_library();cert=phase_certificate()
    rows=[]
    for p,q in ((F(0),F(0)),(F(1,100),F(0)),(F(1,10),F(0)),(F(1,100),F(1,100))):
        for k in range(5):
            rows.append({'p':p,'q':q,**synthesize(p,q,k)})
    a,b,D=family_constants()
    traces=[]
    for y,word in enumerate((3,0,0)):
        for received in range(4):
            for k in (0,1):
                traces.append({'diagnostic':y,'written':word,'received':received,'syndrome':k,
                    'transport_probability':transport_probability(word,received,F(1,100)),
                    'updated_bit':lib[191].execute(received,k),
                    'readable_inputs':[received&1,received>>1,k]})
    return clean({'revision':'v13','date':'2026-11-03','base_commit':'6cd99bb569b746bff6c354694387f15dfb17f50b',
        'physical_contract_blob':'d2b9ccc2253b326af5d494b6d14c5dac6666105c',
        'scope':'SERVICE first, b0=4, same v6 transitions; diagnostic E(Y) transported in two cells; actual NAND update writes one bit; only that bit drives HOLD/REFRESH.',
        'circuit_profile':profile,'certificate':cert,'examples':rows,
        'two_gate_witness':lib[187],'four_gate_witness':lib[191],
        'four_gate_encoding':[3,0,0],'traces':traces,
        'gate_fault_counterexample':gate_fault_falsifier(),
        'tests':{'scientific_python':14,'microstate_cases':24,'polynomial_evaluations':1092,
                 'continuous_inequalities':cert['dominance_checks'],'candidate_programs_largest':5824}})


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true')
    args=p.parse_args();out=certificate();text=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    dest=Path('docs/lab/physical-update-data.json')
    if args.write:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
    if args.check:
        if dest.read_text()!=text:raise SystemExit('physical update certificate drift')
    print(json.dumps({'profile':out['circuit_profile'],'thresholds':[out['certificate']['threshold_two_gates'],out['certificate']['threshold_four_gates']],
        'checks':out['certificate']['dominance_checks'],'examples':out['examples']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
