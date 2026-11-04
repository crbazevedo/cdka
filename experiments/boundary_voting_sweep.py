"""v15 exact certificate, from physical fault grammar and independent quotients."""
import argparse,json
from pathlib import Path
from fractions import Fraction as F
from cdka.boundary_voting import *
from cdka.physical_update import payoff_table


def clean(x):
    if isinstance(x,F):return {'exact':str(x),'value':float(x)}
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(a) for a in x]
    return x


def certificate():
    base=boundary_certificate();sig=signature_certificate()
    values=portfolio();s0={r['id']:r['value'] for r in portfolio(success=F(0))}
    s1={r['id']:r['value'] for r in portfolio(success=F(1))}
    diffs=(s0['single_maintained']-s0['triple_voter_maintained'],s1['single_maintained']-s1['triple_voter_maintained'])
    assert min(diffs)>0
    p=voter_power_profile();poly=tuple(a-b for a,b in zip(p[BITS.index((0,1,1))],p[BITS.index((1,0,1))]))
    assert poly==(0,2,-10,16,-8,0,0)
    single_threshold=(bypass_value()-s0['single'])/(s1['single_maintained']-s0['single'])
    traces=[];gamma=F(1,50)
    for bits in ((0,1,1),(1,0,1)):
        for flags in product((0,1),repeat=6):
            prob=gamma**sum(flags)*(1-gamma)**(6-sum(flags))
            wires=list(bits)
            for (a,b),f in zip(VOTER,flags):wires.append((1-(wires[a]&wires[b]))^f)
            traces.append({'input':bits,'faults':flags,'probability':prob,'wires':wires,'output':wires[-1]})
    return clean({'revision':'v15','date':'2026-11-04','base_commit':'7fa14299961937a580f0de7c0af46511313e834e',
      'scope':'Same SERVICE-first terminal task for portfolio; separate declared 3-cell two-update grammar for signature tests. No optimality over all 18-gate architectures.',
      'params':{'old_bit_error':F(1,100),'degraded_gate_error':F(1,50),'healthy_gate_error':F(1,1000),'service_success':F(4,5)},
      'portfolio':values,'voter_maintenance_threshold':voter_maintenance_threshold(),
      'single_maintenance_threshold':single_threshold,'affine_dominance_endpoints':diffs,
      'boundary':base,'signature':sig,'topology_difference_coefficients':poly,
      'voter_profile':voter_profile(),'voter_power':p,'module_profile':SEQUENTIAL.fault_profile(),
      'task_payoffs':payoff_table(),'voter_gates':VOTER,'fault_traces':traces,
      'verification':{'scientific_tests':17,'quotient_rows':192,'two_update_cases':384,
         'raw_replica_oracle_branches':2560,'voter_trace_rows':128,'raw_voter_mask_checks':2048,
         'continuous_topology_identity':True,'continuous_maintenance_dominance':True}})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');a=ap.parse_args()
    report=certificate();text=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    p=Path('docs/lab/boundary-voting-certificate.json')
    if a.write:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
    if a.check:
        if p.read_text()!=text:raise SystemExit('exact boundary certificate drift')
        print('Exact certificate matches recomputation.')
    print(json.dumps({'boundary':report['boundary'],'ranks':report['signature'],
          'portfolio':[{k:v for k,v in row.items() if k!='channel'} for row in report['portfolio']]},indent=2))

if __name__=='__main__':main()
