"""Matched-model local baselines and optional official Storm subprocesses.
Every method reads exactly the same PRISM source; no ratio across hosts.
"""
from __future__ import annotations
import sys,os,time,json,statistics,subprocess,platform,resource,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
MARKER='CDKA_V21_RESULT '

def child(method,path,h):
    start=time.perf_counter()
    if method in ('cdka','tensor','subset'):
        from cdka.regenerative import parse_prism,tensor_baseline,renewal_subset_baseline
        imports=time.perf_counter()-start;t0=time.perf_counter()
        comp=parse_prism(path.read_text());t1=time.perf_counter()
        if method=='cdka':out=comp.evaluate(h);value=out['probability']
        elif method=='tensor':value=tensor_baseline(comp.model,h);out={}
        else:out=renewal_subset_baseline(comp.model,h);value=out['probability']
        t2=time.perf_counter()
        result={'value':value,'parse_build_s':t1-t0,'check_s':t2-t1,'total_s':t2-t0,
                'import_s':imports,'detail':out,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    else:
        import stormpy
        imports=time.perf_counter()-start;t0=time.perf_counter()
        prism=stormpy.parse_prism_program(str(path))
        props=stormpy.parse_properties(f'P=? [ F<={h} "goal" ]',prism)
        t1=time.perf_counter()
        if method=='storm_symbolic':model=stormpy.build_symbolic_model(prism,props)
        else:model=stormpy.build_model(prism,props)
        before=model.nr_states;t2=time.perf_counter()
        if method=='storm_bisim':model=stormpy.perform_bisimulation(model,props,stormpy.BisimulationType.STRONG)
        t3=time.perf_counter()
        out=stormpy.model_checking(model,props[0])
        if method=='storm_symbolic':
            f=stormpy.create_filter_initial_states_symbolic(model);out.filter(f);value=float(out.get_min())
        else:value=float(out.at(model.initial_states[0]))
        t4=time.perf_counter()
        result={'value':value,'parse_s':t1-t0,'build_s':t2-t1,'bisim_s':t3-t2,'check_s':t4-t3,
                'total_s':t4-t0,'import_s':imports,'states_before':before,'states':model.nr_states,
                'transitions':model.nr_transitions,'stormpy_version':stormpy.__version__,
                'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(MARKER+json.dumps(result,sort_keys=True),flush=True)

def run_official(out_path=None):
    from cdka.regenerative import meeting_restart,render_prism,compile_model
    folder=ROOT/'evidence'/'official';folder.mkdir(parents=True,exist_ok=True)
    rows=[];env={'python':sys.version,'platform':platform.platform(),
        'cpu':Path('/proc/cpuinfo').read_text().split('model name',1)[-1].split('\n',1)[0],
        'source_commit':os.getenv('GITHUB_SHA'),
        'threads':{x:os.environ.get(x) for x in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
        'timing':'same PRISM read/parse/validate-build/check included; imports and process wall separately retained',
        'scope':'new execution on this host; synthetic common-reset extension of first12 published Meeting parameter pairs'}
    cases=((2,10),(4,10),(6,10),(8,10),(4,20))
    order=('cdka','storm_sparse','storm_bisim','storm_symbolic','subset')
    for n,h in cases:
        path=folder/f'restart-meeting-{n}.prism';path.write_text(render_prism(meeting_restart(n)))
        expected=compile_model(meeting_restart(n)).evaluate(h)['probability']
        disabled=set()
        for rep in range(3):
            for method in (order if rep%2==0 else tuple(reversed(order))):
                if method in disabled:continue
                t=time.perf_counter()
                try:
                    r=subprocess.run([sys.executable,__file__,'child',method,str(path),str(h)],capture_output=True,text=True,timeout=60)
                    log=folder/f'{n}-{h}-{method}-{rep}.log';log.write_text(r.stdout+'\nSTDERR\n'+r.stderr)
                    parsed=[x[len(MARKER):] for x in r.stdout.splitlines() if x.startswith(MARKER)]
                    if r.returncode or not parsed:raise RuntimeError(f'exit {r.returncode}: '+r.stderr[-1200:])
                    d=json.loads(parsed[-1]);d.update(n=n,horizon=h,method=method,rep=rep,status='ok',process_wall_s=time.perf_counter()-t)
                    d['absolute_error']=abs(d['value']-expected)
                    if not math.isclose(d['value'],expected,rel_tol=1e-8,abs_tol=1e-13):d['status']='value_mismatch'
                except subprocess.TimeoutExpired:
                    d={'n':n,'horizon':h,'method':method,'rep':rep,'status':'timeout','limit_s':60};disabled.add(method)
                except Exception as e:
                    d={'n':n,'horizon':h,'method':method,'rep':rep,'status':'error','error':str(e)};disabled.add(method)
                rows.append(d);print('BENCH_ROW '+json.dumps(d,sort_keys=True),flush=True)
                (folder/'results.json').write_text(json.dumps({'environment':env,'rows':rows},sort_keys=True,indent=2)+'\n')
    ok=[r for r in rows if r['status']=='ok'];summary=[]
    for n,h in cases:
        for method in order:
            rr=[r for r in ok if (r['n'],r['horizon'],r['method'])==(n,h,method)]
            if rr:summary.append({'n':n,'horizon':h,'method':method,'repeats':len(rr),
                **{key:statistics.median(x[key] for x in rr) for key in ('value','total_s','process_wall_s','peak_rss_kib')}})
    data={'environment':env,'rows':rows,'medians':summary}
    (folder/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    (folder/'summary.json').write_text(json.dumps({'environment':env,'medians':summary,'failures':[r for r in rows if r['status']!='ok']},sort_keys=True,indent=2)+'\n')
    print('BENCH_SUMMARY '+json.dumps({'environment':env,'medians':summary,'failures':[r for r in rows if r['status']!='ok']},sort_keys=True),flush=True)
    if any(r['status'] in ('error','value_mismatch') for r in rows):raise RuntimeError('benchmark has unresolved errors (recorded, not hidden)')
    return data

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='child':child(sys.argv[2],Path(sys.argv[3]),int(sys.argv[4]))
    else:run_official()
