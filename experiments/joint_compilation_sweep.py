"""Recompute exact v10 certificates and generate browser data from the kernel."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
from cdka.joint_compilation import (phase_certificate,synthesize,funded_synthesis,
 continuation_table,polynomial_candidates)


def certificate():
 r=phase_certificate();examples=[]
 for error in (F(0),F(1,100),F(1,20),F(1,10),F(1,2)):
  joint=synthesize(error);inj=synthesize(error,injective=True)
  examples.append({'p':str(error),'value_exact':str(joint['value']),
   'value':float(joint['value']),'encoder':joint['encoding'],'decoder':joint['decoder'],
   'injective_exact':str(inj['value']),'injective_value':float(inj['value'])})
 paid,options=funded_synthesis(F(0))
 return {'scope':'v6 plant/v9 continuations unchanged; two noisy diagnostic latches before first action',
  'joint_programs':r['joint_programs'],'distinct_quadratics':r['distinct_polynomials'],
  'exact_interval_certificates':r['dominance_checks'],
  'phase_coefficients':[[str(x) for x in curve] for curve in r['phase_curves']],
  'thresholds':[{'a':str(t.a),'b':str(t.b),'d':str(t.d),'approximation':t.approximate()} for t in r['thresholds']],
  'examples':examples,'installed_price_one_at_zero_error':[
   {'slots':x['installed'],'fee':x['fee'],'remaining':x['balance'],
    'value_exact':str(x['value']),'value':float(x['value'])} for x in options]}


def browser_data():
 r=phase_certificate();tables={}
 for balance in range(5):
  ids,table=continuation_table(balance)
  tables[str(balance)]={'ids':ids,'weighted':[[float(x) for x in row] for row in table]}
 denominator,candidates=polynomial_candidates()
 # An injective code always uses three distinct physical labels.
 # The dictionary witness for a polynomial may be noninjective, so derive
 # the injective envelope directly in the browser, not by filtering it.
 return {'tables':tables,'phase':[[float(v) for v in curve] for curve in r['phase_curves']],
         'thresholds':[t.approximate() for t in r['thresholds']],
         'fixtures':certificate()}


def main():
 c=certificate();print(json.dumps(c,indent=2))
 if '--write' in sys.argv:
  root=Path(__file__).resolve().parents[1]
  folder=root/'docs/lab';folder.mkdir(parents=True,exist_ok=True)
  (folder/'joint-compilation-data.mjs').write_text('export const DATA = '+json.dumps(browser_data(),indent=2)+';\n')
  (folder/'joint-compilation-certificate.json').write_text(json.dumps(c,indent=2)+'\n')

if __name__=='__main__':main()
