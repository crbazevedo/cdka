"""Independent same-host replication of frozen selection and sound enclosures.
No holdout timing is used by prediction. All attempts and exact endpoints saved.
"""
import os,sys,time,json,hashlib,random,statistics,platform
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
from scipy.optimize import nnls
from vendor.v21.cdka.regenerative import Model,Local,mat,vector,meeting_restart,validate,exact_histogram_value,renewal_subset_baseline
from cdka22.enclosures import certified_solve
from cdka22.portfolio import FrozenSelector,features,solve
E=ROOT/'evidence';E.mkdir(exist_ok=True)
def dump(p,v):p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifests():
    train=[dict(id=f'train-m-{n}-{h}',family='meeting',n=n,h=h,seed=1000+n*100+h,r00=9,r10=2,nu0=10) for n in (2,4,6,8) for h in (6,10,14,20,26,32)]
    test=[]
    for family in ('sequential','dense'):
        for n in (3,5,7,9):
            for h in (8,12,18,24,30):
                seed=20261108+len(test)*37
                test.append(dict(id=f'test-{family}-{n}-{h}',family=family,n=n,h=h,seed=seed,r00=5+seed%5,r10=1+(seed//3)%7,nu0=2+(seed//7)%7))
    for n,h,e in ((2,24,25),(3,18,10),(4,12,8),(5,10,6),(6,8,5),(8,4,4),(9,6,3),(10,3,3)):
        test.append(dict(id=f'test-rare-{n}-{h}-{e}',family='rare',n=n,h=h,seed=7000+n,r00=9,r10=2,nu0=10,exponent=e))
    return train,test

def model(spec):
    n=spec['n'];rng=random.Random(spec['seed']);family=spec['family']
    R=mat([[F(spec['r00'],10),1-F(spec['r00'],10)],[F(spec['r10'],10),1-F(spec['r10'],10)]]);nu=vector([F(spec['nu0'],10),1-F(spec['nu0'],10)])
    if family=='meeting':return Model(meeting_restart(n).components,R,nu)
    cs=[]
    for i in range(n):
        if family=='sequential':
            p,q=F(rng.randrange(5,55),100),F(rng.randrange(35,95),100)
            P=mat([[1-p,p,0],[1-q,0,q],[0,0,1]]);alpha=vector([1,0,0])
        elif family=='dense':
            d=2+spec['seed']%3;rows=[]
            for j in range(d):
                v=[rng.randrange(1,10) for k in range(d+1)];s=sum(v);rows.append([F(a,s) for a in v])
            rows.append([0]*d+[1]);P=mat(rows);a=[rng.randrange(1,6) for k in range(d)];s=sum(a);alpha=vector([F(x,s) for x in a]+[0])
        elif family=='rare':
            p=F(100+i,100*10**spec['exponent']);q=F(1,2)
            P=mat([[1-p,p,0],[1-q,0,q],[0,0,1]]);alpha=vector([1,0,0])
        else:raise ValueError(family)
        d=len(alpha)-1;reset=tuple(alpha for k in range(d))+(tuple(F(j==d) for j in range(d+1)),)
        cs.append(Local(P,reset,alpha,(d,)))
    return Model(tuple(cs),R,nu)

def forced(m,h,b):
    t=time.perf_counter();validate(m);r=certified_solve(m,h,b,checked=True)
    r['end_to_end_s']=time.perf_counter()-t;return r

def train():
    tr,te=manifests();dump(E/'training_manifest.json',tr);dump(E/'holdout_manifest.json',te)
    dump(E/'protocol.json',{'train':len(tr),'holdout':len(te),'rtol':'1/100000000','atol':'0','start_bits':64,'step_bits':32,'max_bits':512,
        'timing':'same process; input generation/imports excluded equally; validation/choice/all interval retries included;3 rotations',
        'source_commit':os.getenv('GITHUB_SHA'),'training_manifest_sha256':sha(E/'training_manifest.json'),'holdout_manifest_sha256':sha(E/'holdout_manifest.json'),
        'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        'scope':'generated held-out parameter/topology families, not curated external benchmark; no new Storm comparison'})
    rows=[]
    for spec in tr:
        m=model(spec);h=spec['h'];samples={'histogram':[],'subset':[]}
        for b in samples:forced(m,h,b)
        for rep in range(3):
            for b in (('histogram','subset') if rep%2==0 else ('subset','histogram')):samples[b].append(forced(m,h,b)['end_to_end_s'])
        for b,v in samples.items():rows.append({'id':spec['id'],'backend':b,'features':features(m,h,b).tolist(),'samples_s':v,'median_s':statistics.median(v)})
    dump(E/'calibration.json',rows);coef={}
    for b in ('histogram','subset'):
        rr=[r for r in rows if r['backend']==b];X=np.array([r['features'] for r in rr]);y=np.array([r['median_s'] for r in rr]);scale=np.maximum(X.max(axis=0),1.);w=1/np.maximum(y,1e-9)
        beta,_=nnls(X/scale*w[:,None],y*w);coef[b]=(beta/scale).tolist()
    selector=FrozenSelector(tuple(coef['histogram']),tuple(coef['subset']),sha(E/'training_manifest.json'),sha(E/'calibration.json'))
    dump(E/'frozen_selector.json',selector.as_dict())
    freeze={'selector_sha256':sha(E/'frozen_selector.json'),'holdout_sha256':sha(E/'holdout_manifest.json'),'heldout_timing_read':False,'frozen_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    dump(E/'freeze.json',freeze);print('FROZEN '+json.dumps(freeze),flush=True)

def evaluate():
    f=json.loads((E/'freeze.json').read_text())
    if sha(E/'frozen_selector.json')!=f['selector_sha256'] or sha(E/'holdout_manifest.json')!=f['holdout_sha256']:raise RuntimeError('frozen files changed')
    selector=FrozenSelector.read(E/'frozen_selector.json');rows=[]
    for spec in json.loads((E/'holdout_manifest.json').read_text()):
        m=model(spec);h=spec['h'];chosen,pred=selector.choose(m,h);times={b:[] for b in ('histogram','subset','portfolio')};answers={}
        for b in ('histogram','subset'):forced(m,h,b)
        for rep in range(3):
            order=('histogram','subset','portfolio');order=order[rep:]+order[:rep]
            for b in order:
                r=solve(m,h,selector) if b=='portfolio' else forced(m,h,b);times[b].append(r['end_to_end_s']);answers[b]=r
        a,b=answers['histogram']['enclosure'],answers['subset']['enclosure']
        if a.lower>b.upper or b.lower>a.upper:raise RuntimeError('disjoint bounds')
        exact=exact_histogram_value(m,h) if spec['family']=='rare' or h<=12 else None
        for r in answers.values():
            if not r['enclosure'].meets():raise RuntimeError('tolerance failure')
            if exact is not None and not r['enclosure'].contains(exact):raise RuntimeError('invalid exact containment')
        row={**spec,'chosen':chosen,'predictions_s':pred,'samples_s':times,'medians_s':{b:statistics.median(v) for b,v in times.items()},
             'enclosures':{b:r['enclosure'].as_dict() for b,r in answers.items()},'attempts':{b:r['attempts'] for b,r in answers.items()},
             'exact_checked':exact is not None,'exact_probability':str(exact) if exact is not None else None,'interval_overlap':True,
             'raw_float_subset':renewal_subset_baseline(m,h),'selector_sha256':f['selector_sha256']}
        rows.append(row);dump(E/'heldout_rows.json',rows);print('HOLDOUT '+json.dumps({'id':row['id'],'chosen':chosen,'medians_s':row['medians_s']}),flush=True)
    def stats(rs):
        ratios=[r['medians_s']['portfolio']/min(r['medians_s']['histogram'],r['medians_s']['subset']) for r in rs]
        return {'cases':len(rs),'winner_agreement':sum(r['chosen']==min(('histogram','subset'),key=lambda b:r['medians_s'][b]) for r in rs),
            'gmean_slowdown_vs_oracle':float(np.exp(np.mean(np.log(ratios)))),'worst_slowdown':max(ratios),
            'total_s':{b:sum(r['medians_s'][b] for r in rs) for b in ('histogram','subset','portfolio')},
            'exact_checked':sum(r['exact_checked'] for r in rs),'max_bits':max(r['enclosures']['portfolio']['bits'] for r in rs)}
    out={'all':stats(rows),'ordinary':stats([r for r in rows if r['family']!='rare']),'rare':stats([r for r in rows if r['family']=='rare']),
         'new_official_solver_comparison':False,'certificate_violations':0,'selector_sha256':f['selector_sha256'],'source_commit':os.getenv('GITHUB_SHA')}
    dump(E/'summary.json',out);print('SUMMARY '+json.dumps(out),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='train':train()
    elif sys.argv[1]=='evaluate':evaluate()
    else:raise SystemExit('train/evaluate')
