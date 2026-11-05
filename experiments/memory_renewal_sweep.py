"""Exact evidence for one frozen recurrent task and its acquisition grammar."""
from fractions import Fraction as F
from dataclasses import asdict
from pathlib import Path
import argparse,json,hashlib
from cdka.memory_renewal import *


def clean(x):
    if isinstance(x,F):return {'exact':str(x),'value':float(x)}
    if isinstance(x,Program):return x.name
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x


def certificate():
    p=Model();rank=ranking(p,8)
    best={a:max((r for r in rank if r['program'].acquisition==a),key=lambda r:r['value']) for a in ACQUISITIONS}
    fixed=[]
    for a in ACQUISITIONS:
        r=summary(p,Program(Policy(),a),8)
        law=r.pop('terminal_law')
        r['acquisition']=a
        r['degraded_with_majority_healthy_report']=sum((w for (z,m,b),w in law.items() if z==1 and sum(m)<2),F(0))
        r['healthy_with_majority_degraded_report']=sum((w for (z,m,b),w in law.items() if z==0 and sum(m)>=2),F(0))
        fixed.append(r)
    witness=symmetry_defect(p)
    traces={a+'-'+b:difference_trace(p,Program(Policy(),a),Program(Policy(),b),8)
            for a,b in [('renew','retain'),('after_skip','after_service')]}
    static=Model(degradation=F(0));src=emission(static,(0,0,3))
    ret=push(src,lambda s:row(static,Program(Policy(),'retain'),s))
    support=[]
    for m in BITS:
        support.append({'memory':m,'initial_mass':src[(0,m,3)],
                        'no_service_probability':1-voter(m,static.healthy_error),
                        'live_skip_mass':ret.get((0,m,4),F(0))})
    kernels={}
    st=macrostates(p);ix={s:i for i,s in enumerate(st)}
    for a in ACQUISITIONS:
        prog=Program(Policy(),a)
        kernels[a]=[[[ix[t],float(w)] for t,w in quotient_row(p,prog,s).items()] for s in st]
    initial=[[ix[s],float(w)] for s,w in aggregate(initial_micro(p)).items()]
    raw=Path('cdka/recurrent_maintenance.py').read_bytes()
    sourcehash=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert sourcehash=='0a01bbf40f78f314a56285c15822e7ac06c9848b'
    return clean({'version':'v17','date':'2026-11-05','base_commit':'d1877a33d5c011d3c11f2e1080dd20358a1178a5',
       'parent_source_blob':sourcehash,'model':asdict(p),'horizon':8,
       'scope':'64 whole stationary routing/acquisition programs; same paid operating bundle, ideal retention and noisy renewal; no history-policy or energy-optimal claim.',
       'counts':{'physical_states':64,'retention_quotient_states':48,'fresh_regenerative_phases':12,
                 'programs':64,'quotient_row_checks':4096,'old_fresh_row_checks':1024,
                 'independent_raw_rows':64,'scientific_tests':20},
       'fixed_routing':fixed,'best_per_acquisition':best,'ranking':rank,
       'emission_witness':witness,'static_trace':support,'temporal_contributions':traces,
       'browser':{'states':st,'initial':initial,'kernels':kernels},
       'precision':'Python values rational. Browser propagates generated transition probabilities in floating point; no optimization or generalization is inferred from chart sampling.'})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true')
    args=parser.parse_args();cert=certificate();text=json.dumps(cert,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    dest=Path('docs/lab/renewal-certificate.json')
    if args.write:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
    if args.check and dest.read_text()!=text:raise SystemExit('renewal certificate drift')
    print(json.dumps({'counts':cert['counts'],'best_per_acquisition':cert['best_per_acquisition'],'witness':cert['emission_witness']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
