"""Reproducible numeric certificates; formulas are proved separately."""
import json
from cdka.implementability import *


def main():
    document={
      'model':'T3.E/T4.D; normalized effort; no original theorem claim',
      'inflection':curvature_threshold(),'tangent':tangent_threshold(),
      'scarcity_example':{
        'n':4,'R':1,'uniform':exp(4*log_cycle(.25)),
        'concentrated':exp(log_cycle(1)+3*log_cycle(0)),
      },
      'ninety_percent_budget':[{ 'n':n,'R':minimum_high_reliability_budget(n,.9)}
                              for n in (1,10,100,1000)],
      'harvest_rates':[{ 'h':h,'rate_2500':harvesting_schedule(2500,h)['rate'],
                         'limit':concave_log_envelope(h)} for h in (0,.3,1,2,4)],
    }
    print(json.dumps(document,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
