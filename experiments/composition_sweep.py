"""Generate exact oracle certificates. Run from repository root."""
import json
from pathlib import Path
from dataclasses import replace
from fractions import Fraction as F
from cdka.composition import *

def run():
    p=Contract();s=(0,0,4);reduction=quotient_report(p)
    report={'reduction':{k:str(v) if isinstance(v,F) else v for k,v in reduction.items()},'fixtures':[]}
    for nu in (F(0),F(1,100),F(1,10),F(1,4)):
        model=replace(p,world_flip=nu)
        for n in (3,10):
            sol=solve(model,n)
            report['fixtures'].append({'world_flip':float(nu),'horizon':n,'initial':s,'value':float(sol['values'][n][s]),'exact':str(sol['values'][n][s]),'first_action':sol['policies'][n][s]})
    cal=calibration_report(p,replace(p,sensor_error=tuple(x+F(1,50) for x in p.sensor_error)),10)
    report['calibration']={k:float(v) for k,v in cal.items()}
    report['frozen_policy_sensor_derivative']=float(sensor_sensitivity(p,solve(p,10)['policies'])[s])
    a=(0,(1,0,0),0,4);b=(0,(0,1,0),0,4);site=(F(3,10),F(1,100),F(1,100))
    report['broken_symmetry_tv']=str(tv(aggregate(micro_row(p,a,'hold',site)),aggregate(micro_row(p,b,'hold',site))))
    ledger=json.loads(Path('registry/research-options.json').read_text())
    report['catalog']={'branches':len(ledger['branches']),'rejected':len(ledger['rejected_simplifications']),'active':[x['id'] for x in ledger['branches'] if x['status']=='active']}
    return report

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
