"""One-query same-host audit: certified contextual compiler vs official Storm.
Fresh processes, randomized order, read+parse+build+check and full process wall.
"""
import sys,os,json,pathlib,time,subprocess,statistics,random,platform,resource
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))

def child(method,path,H):
    t0=time.perf_counter()
    if method=='cdka_context':
        from cdka.context_product import parse_prism,compile_context
        import numpy as np
        imports=time.perf_counter()-t0;start=time.perf_counter()
        ir=parse_prism(pathlib.Path(path).read_text());parsed=time.perf_counter()
        model=compile_context(ir);built=time.perf_counter()
        result=model.evaluate(H);done=time.perf_counter()
        ans={'value':result['probability'],'parse_s':parsed-start,'build_s':built-parsed,
             'check_s':done-built,'total_s':done-start,'import_s':imports,'numpy':np.__version__,
             'implicit_states':model.certificate['global_state_count']}
    else:
        import stormpy
        imports=time.perf_counter()-t0;start=time.perf_counter()
        program=stormpy.parse_prism_program(str(path))
        prop=stormpy.parse_property(f'P=? [ F<={H} "goal" ]',program);parsed=time.perf_counter()
        model=(stormpy.build_model(program,prop) if method=='storm_sparse'
               else stormpy.build_symbolic_model(program,prop));built=time.perf_counter()
        result=stormpy.model_checking(model,prop)
        if method=='storm_sparse':value=float(result[model.initial_states[0]])
        else:stormpy.filter_initial_states(result,model);value=float(result.get_min())
        done=time.perf_counter()
        ans={'value':value,'parse_s':parsed-start,'build_s':built-parsed,'check_s':done-built,
             'total_s':done-start,'import_s':imports,'stormpy':stormpy.__version__,
             'states':model.nr_states,'transitions':model.nr_transitions}
        try:ans['storm_core']=stormpy.info.storm_version()
        except (AttributeError,TypeError):ans['storm_core']='not exposed by binding'
    ans['maxrss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('AUDIT_CHILD '+json.dumps(ans,sort_keys=True),flush=True)

def main(out):
    from cdka.context_product import meeting,render_prism,compile_context,parse_prism
    import numpy as np,hashlib
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    cases=((2,10),(4,10),(6,10),(8,10),(6,50));rows=[]
    environment={'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),
      'cpu':pathlib.Path('/proc/cpuinfo').read_text().split('model name',1)[-1].split('\n',1)[0],
      'threads':{k:os.getenv(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
      'case_order':'within-case seeded random method/repetition order; fresh child per observation',
      'timing':'one query: read+parse+certification or model build+check; imports excluded from total_s, included in process_wall_s',
      'scope':'CPU, Storm default sparse/symbolic calls, no backend tuning; not Tessa GPU or Dice',
      'source_commit':os.getenv('GITHUB_SHA','local')}
    hashes={}
    for n,H in cases:
        path=out/f'context-meeting-{n}.prism';text=render_prism(meeting(n));path.write_text(text)
        hashes[str(n)]=hashlib.sha256(text.encode()).hexdigest()
        expected=compile_context(parse_prism(text)).evaluate(H)['probability']
        order=[(method,rep) for method in ('cdka_context','storm_sparse','storm_symbolic') for rep in range(3)]
        random.Random(1000+n+H).shuffle(order)
        for method,rep in order:
            t=time.perf_counter()
            try:
                run=subprocess.run([sys.executable,__file__,'--child',method,str(path),str(H)],capture_output=True,text=True,timeout=45)
                (out/f'{n}-{H}-{method}-{rep}.log').write_text(run.stdout+'\nSTDERR\n'+run.stderr)
                lines=[x[len('AUDIT_CHILD '):] for x in run.stdout.splitlines() if x.startswith('AUDIT_CHILD ')]
                if run.returncode or not lines:raise RuntimeError(f'child exited {run.returncode}: {run.stderr[-400:]}')
                row=json.loads(lines[-1]);row.update(n=n,H=H,method=method,rep=rep,status='ok',process_wall_s=time.perf_counter()-t)
                row['absolute_error']=abs(row['value']-expected)
                if row['absolute_error']>1e-11+1e-10*abs(expected):row['status']='value_mismatch'
            except subprocess.TimeoutExpired:row=dict(n=n,H=H,method=method,rep=rep,status='timeout',limit_s=45)
            except Exception as e:row=dict(n=n,H=H,method=method,rep=rep,status='error',error=str(e))
            rows.append(row);print(json.dumps(row,sort_keys=True),flush=True)
            (out/'results.json').write_text(json.dumps({'environment':environment,'hashes':hashes,'rows':rows},indent=2,sort_keys=True)+'\n')
    summary=[]
    for n,H in cases:
        item={'n':n,'H':H,'methods':{}}
        for method in ('cdka_context','storm_sparse','storm_symbolic'):
            r=[x for x in rows if (x['n'],x['H'],x['method'])==(n,H,method) and x['status']=='ok']
            if len(r)==3:
                item['methods'][method]={k:statistics.median(x[k] for x in r) for k in ('total_s','check_s','process_wall_s','maxrss_kib')}
                item['methods'][method]['max_abs_error']=max(x['absolute_error'] for x in r)
            else:item['methods'][method]={'complete_repetitions':len(r)}
        summary.append(item)
    (out/'summary.json').write_text(json.dumps({'environment':environment,'cases':summary},indent=2,sort_keys=True)+'\n')
    print('AUDIT_COMPLETE '+json.dumps(summary,sort_keys=True),flush=True)
    if any(x['status'] in ('error','value_mismatch') for x in rows):raise RuntimeError('unresolved benchmark error; retained all evidence')

if __name__=='__main__':
    if sys.argv[1:2]==['--child']:child(sys.argv[2],sys.argv[3],int(sys.argv[4]))
    else:main(sys.argv[1] if len(sys.argv)>1 else 'evidence/official_audit')
