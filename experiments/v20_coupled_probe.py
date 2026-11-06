"""Same-PRISM coupled-context comparison: official Storm and certified counts.
This is a generated extension of the public Meeting family, NOT an unmodified
paper benchmark. The environment starts at0; all methods use the identical
current-environment synchronous tick and goal. No initial dummy step.
"""
import sys,os,re,json,time,hashlib,pathlib,statistics,subprocess,resource,platform,urllib.request
from fractions import Fraction as F
import v20_official_probe as original
ROOT=pathlib.Path('v20_coupled_evidence')


def parse(text):
    """Full-input small-grammar validation: no hidden annotations are trusted."""
    source=hashlib.sha256(text.encode()).hexdigest();s=text.strip()
    if not s.startswith('dtmc'):raise ValueError('DTMC')
    s=s[4:];modules=[]
    pattern=r'module\s+(\w+)\s+(.*?)\s+endmodule'
    blocks=list(re.finditer(pattern,s,re.S))
    leftover=re.sub(pattern,'',s,flags=re.S)
    for name,body in (m.groups() for m in blocks):
        decl=re.match(r'\s*(\w+)\s*:\s*\[0\.\.(\d+)\]\s+init\s+0\s*;',body)
        if decl is None:raise ValueError('state declaration')
        var,upper=decl.groups();size=int(upper)+1;body=body[decl.end():]
        commands=[]
        for command in body.split(';'):
            if not command.strip():continue
            m=re.fullmatch(r'\s*\[step\]\s*(.*?)\s*->\s*(.*?)\s*',command,re.S)
            if m is None:raise ValueError('sync command')
            guard,updates=m.groups();row=[F(0)]*size
            for branch in updates.split('+'):
                m=re.fullmatch(r'\s*\(([0-9]+/[0-9]+)\)\s*:\s*\(\s*'+re.escape(var)+r"'\s*=\s*(\d+)\s*\)\s*",branch)
                if m is None:raise ValueError('local write/probability')
                probability,target=m.groups();j=int(target)
                if j>=size:raise ValueError('domain')
                row[j]+=F(probability)
            if sum(row)!=1 or min(row)<0:raise ValueError('stochasticity')
            commands.append((re.sub(r'\s+','',guard),tuple(row)))
        modules.append((name,var,size,commands))
    if not modules or modules[0][1:3]!=('e',2):raise ValueError('environment interface')
    env=modules[0][3]
    if [g for g,r in env]!=['e=0','e=1']:raise ValueError('environment guard')
    R=tuple(row for g,row in env);Ps=[]
    for i,(name,var,size,commands) in enumerate(modules[1:],1):
        if (name,var,size)!=(f'P{i}',f's{i}',3):raise ValueError('ownership')
        if [g for g,r in commands]!=[f'e={z}&s{i}={a}' for z in (0,1) for a in range(3)]:raise ValueError('context/local guards')
        mats=(tuple(r for g,r in commands[:3]),tuple(r for g,r in commands[3:]))
        if any(p[2]!=(0,0,1) for p in mats):raise ValueError('nonabsorbing target')
        for a in range(3):
            for b in range(3):
                if sum(mats[0][a][k]*mats[1][k][b] for k in range(3))!=sum(mats[1][a][k]*mats[0][k][b] for k in range(3)):raise ValueError('not commuting: use general semantic compiler')
        Ps.append(mats)
    expected='label"goal"='+'&'.join(f'(s{i}=2)' for i in range(1,len(Ps)+1))+';'
    if re.sub(r'\s+','',leftover)!=expected:raise ValueError('goal/trailing input')
    return Ps,R,{'sha256':source,'components':len(Ps),'context_modes':2,'initial_context':0,'commutation':'exact full matrices','scheduler':'use current context then transition environment','goal':'all absorbing local goals'}


def counts(Ps,R,H):
    import numpy as np
    P=np.array(Ps,float);R=np.array(R,float);N=len(P)
    if H==0:return 0.
    w=np.zeros((2,H+1));w[0,0]=1
    for t in range(1,H):
        new=np.zeros_like(w)
        new[0,:t+1]=w[0,:t+1]*R[0,0]+w[1,:t+1]*R[1,0]
        new[1,1:t+2]=w[0,:t+1]*R[0,1]+w[1,:t+1]*R[1,1]
        w=new
    L=np.zeros((H+1,N,3));U=np.zeros_like(L);L[0,:,0]=1;U[0,:,2]=1
    for t in range(H):
        L[t+1]=np.einsum('ni,nij->nj',L[t],P[:,0],optimize=False)
        U[t+1]=np.einsum('nij,nj->ni',P[:,1],U[t],optimize=False)
    local=np.einsum('tni,tni->tn',L[::-1],U,optimize=False)
    return float(w.sum(axis=0)@np.prod(local,axis=1))


def render(kernels):
    R=((F(9,10),F(1,10)),(F(1,5),F(4,5)))
    f=lambda x:f'({x.numerator}/{x.denominator})'
    lines=['dtmc','module environment',' e : [0..1] init 0;']
    for z,row in enumerate(R):lines.append(f' [step] e={z} -> '+' + '.join(f'{f(p)} : (e\'={j})' for j,p in enumerate(row) if p)+';')
    lines+=['endmodule']
    for i,P in enumerate(kernels,1):
        lines += [f'module P{i}',f' s{i} : [0..2] init 0;']
        for z,a in enumerate((F(1,4),F(1))):
            Q=tuple(tuple((1-a)*int(j==k)+a*P[j][k] for k in range(3)) for j in range(3))
            for j,row in enumerate(Q):lines.append(f' [step] e={z} & s{i}={j} -> '+' + '.join(f'{f(p)} : (s{i}\'={k})' for k,p in enumerate(row) if p)+';')
        lines+=['endmodule']
    lines+=['label "goal" = '+' & '.join(f'(s{i}=2)' for i in range(1,len(kernels)+1))+';']
    return '\n'.join(lines)+'\n'


def child(method,path,H):
    start=time.perf_counter()
    if method=='cdka_counts':
        import numpy as np
        imports=time.perf_counter()-start;t0=time.perf_counter()
        Ps,R,cert=parse(path.read_text());t1=time.perf_counter();value=counts(Ps,R,H);t2=time.perf_counter()
        direct=[]
        for _ in range(30):
            t=time.perf_counter();counts(Ps,R,H);direct.append(time.perf_counter()-t)
        out={'value':value,'parse_build_s':t1-t0,'check_s':t2-t1,'total_s':t2-t0,'import_s':imports,'certificate':cert,'informed_count_median_s':statistics.median(direct)}
    else:
        import stormpy
        imports=time.perf_counter()-start;t0=time.perf_counter()
        model=stormpy.parse_prism_program(str(path));prop=stormpy.parse_property(f'P=? [ F<={H} "goal" ]',model);t1=time.perf_counter()
        model=stormpy.build_model(model,prop) if method=='storm_sparse' else stormpy.build_symbolic_model(model,prop);t2=time.perf_counter()
        result=stormpy.model_checking(model,prop)
        if method=='storm_sparse':value=float(result[model.initial_states[0]])
        else:stormpy.filter_initial_states(result,model);value=float(result.get_min())
        t3=time.perf_counter();out={'value':value,'parse_s':t1-t0,'build_s':t2-t1,'check_s':t3-t2,'total_s':t3-t0,'import_s':imports,'states':model.nr_states,'transitions':model.nr_transitions,'stormpy_version':stormpy.__version__}
    out['maxrss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('V20_COUPLED_CHILD '+json.dumps(out,sort_keys=True),flush=True)


def main():
    if len(sys.argv)>1:child(sys.argv[1],pathlib.Path(sys.argv[2]),int(sys.argv[3]));return
    ROOT.mkdir(exist_ok=True);rows=[]
    env={'python':sys.version,'platform':platform.platform(),'cpu':pathlib.Path('/proc/cpuinfo').read_text().split('model name',1)[-1].split('\n',1)[0],'threads':{k:os.getenv(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},'input':'same generated PRISM per case; source Meeting parameters pinned, added exogenous binary Markov environment','timing':'read+parse+validate/compile+solve; imports and process wall also retained'}
    for n,H in ((2,10),(4,10),(6,10),(8,10),(6,50)):
        path=ROOT/f'context-meeting-{n}.prism'
        if not path.exists():
            raw=urllib.request.urlopen(f'{original.RAW}/benchmarks/meeting/meeting-{n}.prism',timeout=30).read().decode()
            base,_=original.certify(raw);path.write_text(render(base))
        expected=None
        for method in ('cdka_counts','storm_symbolic','storm_sparse'):
            for rep in range(3):
                t=time.perf_counter()
                try:
                    run=subprocess.run([sys.executable,__file__,method,str(path),str(H)],capture_output=True,text=True,timeout=45)
                    (ROOT/f'{n}-{H}-{method}-{rep}.log').write_text(run.stdout+'\nSTDERR\n'+run.stderr)
                    lines=[l[len('V20_COUPLED_CHILD '):] for l in run.stdout.splitlines() if l.startswith('V20_COUPLED_CHILD ')]
                    if run.returncode or not lines:raise RuntimeError(f'child exit={run.returncode}: '+run.stderr[-800:])
                    out=json.loads(lines[-1]);out.update(n=n,H=H,method=method,rep=rep,status='ok',process_wall_s=time.perf_counter()-t)
                    if expected is None:expected=out['value']
                    out['absolute_error']=abs(out['value']-expected)
                    if out['absolute_error']>1e-10:out['status']='value_mismatch'
                except subprocess.TimeoutExpired:out={'n':n,'H':H,'method':method,'rep':rep,'status':'timeout','limit_s':45}
                except Exception as e:out={'n':n,'H':H,'method':method,'rep':rep,'status':'error','error':str(e)}
                rows.append(out);print('V20_COUPLED_ROW '+json.dumps(out,sort_keys=True),flush=True)
                (ROOT/'results.json').write_text(json.dumps({'environment':env,'rows':rows},indent=2,sort_keys=True))
                if out['status']!='ok':break
    print('V20_COUPLED_COMPLETE '+json.dumps({'environment':env,'rows':rows},sort_keys=True),flush=True)
    if not any(r['method'].startswith('storm') and r['status']=='ok' for r in rows):raise RuntimeError('no official solver results')
    if any(r['status'] in ('error','value_mismatch') for r in rows):raise RuntimeError('benchmark has unresolved errors')
if __name__=='__main__':main()
