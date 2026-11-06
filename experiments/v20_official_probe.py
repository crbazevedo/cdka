"""Bounded same-host Storm comparison on unmodified public Meeting inputs.

Independent children, fixed threads, explicit statuses and raw timing samples.
No SOTA claim follows from beating one engine on a recognized special class.
"""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, platform, re, resource, statistics
import subprocess, sys, time, urllib.request
from fractions import Fraction as F

PIN='b8d01443ab289fa4e70bda3b11bf3104f9d1c4b2'
RAW=f'https://raw.githubusercontent.com/tessa-cav26-ae/tessa-cav26-ae/{PIN}'
ROOT=pathlib.Path('v20_probe_evidence')


def certify(text):
    """Whole-text conservative recognizer, derived from the local v19 frontend."""
    source_hash=hashlib.sha256(text.encode()).hexdigest()
    text=re.sub(r'//[^\n]*','',text)
    text=re.sub(r'/\*.*?\*/','',text,flags=re.S).strip()
    if not text.startswith('dtmc'):raise ValueError('DTMC required')
    text=text[4:];parameters={}
    def decl(m):
        k,v=m.groups()
        if k in parameters:raise ValueError('duplicate constant')
        parameters[k]=F(v);return ''
    text=re.sub(r'const\s+double\s+([pq]\d+)\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*;',decl,text)
    first=re.search(r'module\s+P1\s+(.*?)\s+endmodule',text,re.S)
    expected="""s1 : [0.. 2] init 0;
    [step] s1 = 0 -> (1 - p1) : (s1' = 0) + p1 : (s1' = 1);
    [step] s1 = 1 -> (1 - q1) : (s1' = 0) + q1 : (s1' = 2);
    [step] s1 = 2 -> 1.0 : (s1' = 2);"""
    norm=lambda s:re.sub(r'\s+','',s)
    if first is None or norm(first.group(1))!=norm(expected):raise ValueError('unsupported local law')
    text=text[:first.start()]+text[first.end():];ids=[1]
    def clone(m):
        ns=list(map(int,m.groups()))
        if len(set(ns))!=1 or ns[0] in ids:raise ValueError('overlapping ownership')
        ids.append(ns[0]);return ''
    text=re.sub(r'module\s+P(\d+)\s*=\s*P1\[s1=s(\d+),p1=p(\d+),q1=q(\d+)\]\s*endmodule',clone,text)
    if sorted(ids)!=list(range(1,len(ids)+1)):raise ValueError('module IDs')
    goal=re.fullmatch(r'\s*label\s+"goal"\s*=\s*(.*?)\s*;\s*',text,re.S)
    if goal is None or norm(goal.group(1))!='&'.join(f'(s{i}=2)' for i in sorted(ids)):raise ValueError('noncartesian goal or unparsed syntax')
    if set(parameters)!={f'{a}{i}' for i in ids for a in 'pq'}:raise ValueError('constant set')
    kernels=[]
    for i in sorted(ids):
        p,q=parameters[f'p{i}'],parameters[f'q{i}']
        if not 0<=p<=1 or not 0<=q<=1:raise ValueError('invalid probabilities')
        K=((1-p,p,F(0)),(1-q,F(0),q),(F(0),F(0),F(1)))
        if any(sum(row)!=1 for row in K) or K[2]!=(0,0,1):raise ValueError('kernel guard')
        kernels.append(K)
    certificate={'sha256':source_hash,'components':len(kernels),'goal_absorbing':True,'scheduler':'single synchronous label','owned_reads':True}
    return kernels,certificate


def local_value(kernels,h):
    import numpy as np
    P=np.asarray(kernels,dtype=np.float64);mu=np.zeros((len(P),3));mu[:,0]=1
    while h:
        if h&1:mu=np.einsum('ni,nij->nj',mu,P,optimize=False)
        h>>=1
        if h:P=P@P
    return float(np.prod(mu[:,2]))


def child(method,path,h):
    # Imports are reported separately; warm interpreter/model caches not reused.
    started=time.perf_counter()
    if method.startswith('storm'):
        import stormpy
        imports=time.perf_counter()-started;t0=time.perf_counter()
        program=stormpy.parse_prism_program(str(path))
        props=stormpy.parse_properties_for_prism_program(f'P=? [ F<={h} "goal" ]',program)
        t1=time.perf_counter()
        if method=='storm_sparse':model=stormpy.build_sparse_model(program,props)
        else:model=stormpy.build_symbolic_model(program,props)
        t2=time.perf_counter();result=stormpy.model_checking(model,props[0])
        if method=='storm_sparse':value=float(result.at(model.initial_states[0]))
        else:
            result.filter(stormpy.create_filter_initial_states_symbolic(model))
            value=float(result.min if not callable(result.min) else result.min())
        t3=time.perf_counter()
        out={'method':method,'value':value,'parse_s':t1-t0,'build_s':t2-t1,'check_s':t3-t2,'total_s':t3-t0,'import_s':imports,
             'states':model.nr_states,'transitions':model.nr_transitions,'stormpy_version':stormpy.__version__}
    else:
        import numpy as np
        imports=time.perf_counter()-started;t0=time.perf_counter()
        text=path.read_text();kernels,certificate=certify(text);t1=time.perf_counter()
        value=local_value(kernels,h);t2=time.perf_counter()
        # A structure-informed competitor uses the SAME prevalidated kernels.
        direct=[]
        for _ in range(100):
            a=time.perf_counter();local_value(kernels,h);direct.append(time.perf_counter()-a)
        out={'method':method,'value':value,'parse_build_s':t1-t0,'check_s':t2-t1,'total_s':t2-t0,'import_s':imports,
             'direct_prevalidated_s':statistics.median(direct),'certificate':certificate,'numpy_version':np.__version__}
    out['maxrss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('V20_CHILD '+json.dumps(out,sort_keys=True),flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--child',choices=['storm_sparse','storm_symbolic','cdka_product']);ap.add_argument('--path');ap.add_argument('--h',type=int,default=10);a=ap.parse_args()
    if a.child:
        child(a.child,pathlib.Path(a.path),a.h);return
    ROOT.mkdir(exist_ok=True)
    env={'platform':platform.platform(),'python':sys.version,'cpu':platform.processor(),'threads':{k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},'source_pin':PIN,'timing':'fresh child, imports separately; parse+model-build+check; no compilation excluded'}
    env['cpuinfo']=pathlib.Path('/proc/cpuinfo').read_text().split('model name',1)[-1].split('\n',1)[0]
    rows=[]
    for n,h in ((2,10),(4,10),(8,10),(12,10),(8,100)):
        path=ROOT/f'meeting-{n}.prism'
        if not path.exists():
            raw=urllib.request.urlopen(f'{RAW}/benchmarks/meeting/meeting-{n}.prism',timeout=30).read()
            path.write_bytes(raw)
            if n==12:
                assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='8ce3669983634429218820743cf951568747065a'
        expected=None
        for method in ('cdka_product','storm_symbolic','storm_sparse'):
            for rep in range(3):
                t=time.perf_counter()
                try:
                    r=subprocess.run([sys.executable,__file__,'--child',method,'--path',str(path),'--h',str(h)],text=True,capture_output=True,timeout=45)
                    log=ROOT/f'{n}-{h}-{method}-{rep}.log';log.write_text(r.stdout+'\nSTDERR\n'+r.stderr)
                    lines=[s[len('V20_CHILD '):] for s in r.stdout.splitlines() if s.startswith('V20_CHILD ')]
                    if r.returncode!=0 or not lines:raise RuntimeError(f'child failed code={r.returncode}: '+r.stderr[-1200:])
                    out=json.loads(lines[-1]);out.update(n=n,h=h,rep=rep,status='ok',process_wall_s=time.perf_counter()-t)
                    if expected is None:expected=out['value']
                    out['absolute_error_vs_product']=abs(out['value']-expected)
                    if out['absolute_error_vs_product']>1e-10:out['status']='value_mismatch'
                except subprocess.TimeoutExpired as exc:
                    out={'n':n,'h':h,'method':method,'rep':rep,'status':'timeout','limit_s':45}
                except Exception as exc:
                    out={'n':n,'h':h,'method':method,'rep':rep,'status':'error','error':str(exc)}
                rows.append(out);print('V20_ROW '+json.dumps(out,sort_keys=True),flush=True)
                (ROOT/'results.json').write_text(json.dumps({'environment':env,'rows':rows},indent=2,sort_keys=True))
                if out['status']!='ok':break
    print('V20_COMPLETE '+json.dumps({'environment':env,'rows':rows},sort_keys=True),flush=True)

if __name__=='__main__':main()
