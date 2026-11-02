"""Reproduce v8 exact decision/implementation certificates, not simulations."""
from dataclasses import replace
from fractions import Fraction as F
import json
from cdka.diagnostic_transport import (
 TransportContract,terminal_table,closed_value,optimize_architecture,
 optimize_terminal,information_before_selector,skip_value)

def certificates():
 c=TransportContract()
 budgets=[]
 for b in range(4,8):
  r=optimize_architecture(replace(c,budget=b))
  budgets.append({'budget':b,'choice':r['choice'],'value':str(r['value']),
                  'value_decimal':float(r['value']),'gain':float(r['gain']),
                  'programs':{k:float(v['value']) for k,v in r['options'].items()}})
 delays=[]
 for t in range(1,11):
  cc=TransportContract(budget=20,ticks=t,selector_bad=F(1,6),erasure=F(1,5),sensor_error=0)
  delays.append({'ticks':t,'diagnosis_net':float(closed_value(cc)-skip_value(cc)),
                 'mutual_information_bits':information_before_selector(cc)})
 corr=[]
 for rev in (False,True):
  j={(h,h,1-h if rev else h):F(1,2) for h in (0,1)}
  corr.append({'opposite_health':rev,'value':float(optimize_terminal(j,(F(0),F(2,5)))['value'])})
 return {'source':'cdka.composition.Contract (v6) terminal event, retained in v7',
         'date':'2026-11-02','action_table':[[str(x) for x in row] for row in terminal_table()],
         'budgets':budgets,'expiration':delays,'correlation':corr,
         'status':'Known finite Bayes/FSC tools; no originality claim.'}

if __name__=='__main__':print(json.dumps(certificates(),indent=2,ensure_ascii=False))
