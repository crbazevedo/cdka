"""Generate reproducible rational fixture and phase data for CDKA v7."""
import json
from fractions import Fraction as F
from pathlib import Path
from cdka.hidden_health import (DiagnosticContract,optimal_inspection,binary_threshold,
                                hidden_health_occupancy,action_survival)
from cdka.composition import Contract


def main():
    root=Path(__file__).resolve().parents[1]
    c=DiagnosticContract();t=binary_threshold(c)
    scores={name:{str(h):str(action_survival(c.physical,k,h,c.budget,name))
                  for h in (0,1)} for k in (0,1) for name in c.physical.actions(c.budget)}
    payoffs={str(k):{a:[float(action_survival(c.physical,k,h,c.budget,a)) for h in (0,1)]
                     for a in c.physical.actions(c.budget)} for k in (0,1)}
    horizons={str(n):{name:float(v) for name,v in hidden_health_occupancy(Contract(),0,4,n).items()
                      if name in ('value','health_oracle','gap')} for n in (1,2,3)}
    out={'model':'CDKA-v6 macro physical kernel; v7 paid diagnosis',
         'hypotheses':['diagnosis and no-diagnosis share a health-drift interval',
                       'fixed outcome-independent costs','health hidden','readable syndrome and budget',
                       'no free posterior memory'],
         'payoffs':payoffs,
         'critical_error_fraction':str(t['critical_error']),
         'critical_error_float':float(t['critical_error']),
         'base_value_fraction':str(t['base']),
         'base_value_float':float(t['base']),
         'perfect_gain_fraction':str(t['raw_information_value']),
         'perfect_gain_float':float(t['raw_information_value']),
         'horizon_reference':horizons,
         'surface':[]}
    for budget in range(5):
        row=[]
        for ix in range(51):
            eta=F(ix,100)
            x=optimal_inspection(DiagnosticContract(budget=budget,sensor_error=eta))
            row.append(float(x['gain']))
        out['surface'].append(row)
    dest=root/'docs'/'lab'/'diagnosis-fixtures.json'
    dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print('Wrote',dest,'critical error',float(t['critical_error']))
    for n,vals in horizons.items():print('horizon',n,vals)

if __name__=='__main__':main()
