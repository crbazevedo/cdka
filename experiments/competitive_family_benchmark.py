"""Pilot vs whole-family sparse Bellman and Storm, not per-policy enumeration.

Explicit synthetic positives, independent fixed CDKA case, negative controls.
Construction, exact compilation and hot queries are reported separately.
All compared algorithms use the same process/CPU. No SOTA claim is embedded.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,platform,statistics,time,sys,resource
from pathlib import Path
import numpy as np
from cdka.family_certificate import *

def timed(fn,reps=3):
    ts=[];out=None
    for _ in range(reps):
        t=time.perf_counter();out=fn();ts.append(time.perf_counter()-t)
    return out,{'median':statistics.median(ts),'samples':ts}

def storm_build(choices):
    import stormpy as st
    ds=getattr(st,'datastructures',st);md=getattr(st,'models',getattr(st,'storage',st))
    n=len(choices);b=ds.SparseMatrixBuilder(rows=0,columns=0,entries=0,force_dimensions=False,has_custom_row_grouping=True,row_groups=0);k=0
    for i,rows in enumerate(choices):
        b.new_row_group(k)
        for row in rows:
            for j,p in sorted(row.items()):b.add_next_value(k,j,float(p))
            failure=1-sum(row.values(),F(0))
            if failure:b.add_next_value(k,n,float(failure))
            k+=1
    b.new_row_group(k);b.add_next_value(k,n,1.0)
    labels=md.StateLabeling(n+1)
    for lab in ('init','fail'):labels.add_label(lab)
    labels.add_label_to_state('init',0);labels.add_label_to_state('fail',n)
    comp=md.SparseModelComponents(transition_matrix=b.build(),state_labeling=labels)
    return md.SparseMdp(comp)

def scalar_result(st,result,model):
    if hasattr(st,'filter_initial_states'):
        st.filter_initial_states(result,model);value=result.get_min()
    elif hasattr(result,'at'):value=result.at(0)
    else:value=result.get_values()[0]
    try:return float(value)
    except (TypeError,ValueError):
        for name in ('value','midpoint','get_value'):
            if hasattr(value,name):
                v=getattr(value,name);return float(v() if callable(v) else v)
        for ln,un in [('lower','upper'),('lower_bound','upper_bound')]:
            if hasattr(value,ln) and hasattr(value,un):
                lo=getattr(value,ln);hi=getattr(value,un)
                lo=float(lo() if callable(lo) else lo);hi=float(hi() if callable(hi) else hi)
                if hi-lo>1e-7:raise AssertionError('Storm bound too loose')
                return (lo+hi)/2
        raise TypeError('Unsupported result '+str(type(value))+': '+repr(value))

def storm_query(model,horizon):
    import stormpy as st
    vals=[]
    for direction in ('min','max'):
        text=f'P{direction}=? [ F<={horizon} "fail" ]'
        prop=st.parse_property(text) if hasattr(st,'parse_property') else st.parse_properties(text)[0]
        result=st.model_checking(model,prop)
        vals.append(1-scalar_result(st,result,model))
    return tuple(vals)

def run_instance(n,seed,horizons,reps,use_storm,cdka=False):
    start=time.perf_counter();choices,meta=cdka_elision_family() if cdka else workflow_family(n,seed)
    gen=time.perf_counter()-start
    cert,tc=timed(lambda:compile_family(choices),reps);assert isinstance(cert,Certificate),cert
    mats,tb=timed(lambda:sparse_family(choices),reps);model=None;ts=None
    if use_storm:model,ts=timed(lambda:storm_build(choices),reps)
    res={'n':len(choices),'seed':seed,'class':meta['class'],'rank':cert.rank,
       'local_choices':cert.row_count,'nnz_all_choices':sum(len(r) for rows in choices for r in rows),
       'variable_rows':sum(len(r)>1 for r in choices),'generation_seconds':gen,
       'compile':tc,'sparse_build':tb,'storm_build':ts,'queries':[]}
    for h in horizons:
        compiled,tq=timed(lambda:cert.values_float(h),reps)
        (lo,hi),td=timed(lambda:bellman(mats,h),reps)
        err=float(max(np.max(np.abs(lo-compiled)),np.max(np.abs(hi-compiled))))
        assert err<1e-8,(h,err)
        q={'horizon':h,'compiled_query':tq,'family_bellman':td,'max_abs_error_bellman':err,'value_initial':float(compiled[0]),'storm_query':None}
        if use_storm:
            values,tsq=timed(lambda:storm_query(model,h),reps)
            q['storm_query']=tsq;q['storm_survival']=values
            q['storm_max_abs_error']=float(max(abs(v-compiled[0]) for v in values));assert q['storm_max_abs_error']<1e-8,q
        res['queries'].append(q)
        print('BENCH_ROW '+json.dumps({'class':res['class'],'n':len(choices),'seed':seed,'rank':cert.rank,'H':h,'compile_s':tc['median'],'cdka_hot_s':tq['median'],'sparse_s':td['median'],'storm_build_s':ts['median'] if ts else None,'storm_query_s':q['storm_query']['median'] if use_storm else None,'error':q.get('storm_max_abs_error',err)}),flush=True)
    return res

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--storm',action='store_true');ap.add_argument('--output',default='evidence/competitive-benchmark.json');ap.add_argument('--quick',action='store_true');ap.add_argument('--repeats',type=int,default=3);a=ap.parse_args()
    info={'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'cpu':platform.processor(),'threads':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS')},'storm_requested':a.storm,'imports_excluded_from_timing':True,'repetitions':a.repeats,'numerical_tolerance_abs':1e-8}
    if a.storm:
        import stormpy
        info['stormpy']=stormpy.__version__
        try:info['storm']=stormpy.info.storm_version()
        except Exception as e:info['storm_info_error']=str(e)
    results=[];sizes=(16,64) if a.quick else (16,64,512,4096)
    horizons=(8,100,1000) if a.quick else (8,1000,10000,100000);seeds=(23,) if a.quick else (23,71)
    for n in sizes:
        for seed in seeds:results.append(run_instance(n,seed,horizons,a.repeats,a.storm))
    results.append(run_instance(48,0,(8,100,1000),a.repeats,a.storm,cdka=True))
    negatives=[compile_family(workflow_family(16,s,perturb=True)[0]) for s in (23,71)]
    assert all(isinstance(x,dict) and x['reason']=='separating_row' for x in negatives)
    doc={'protocol':'CDKA-v19-competitive-pilot','class':'families with a certified common continuation restriction','state_of_art_claim':False,'metadata':info,'results':results,'negative_controls':negatives,'max_rss_kib_process':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'memory_scope':'process high-water mark, NOT per-method peak memory','limitations':['synthetic scaling fixtures','one actual CDKA family','no PAYNT/PRISM/APEX competition yet','numeric projection of exact certificate; arithmetic bit costs separated','Storm lifted-family sparse engine, not all engine choices']}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(doc,indent=2)+'\n')
    print('BENCH_COMPLETE '+json.dumps({'output':str(out),'instances':len(results),'metadata':info}),flush=True)
if __name__=='__main__':main()
