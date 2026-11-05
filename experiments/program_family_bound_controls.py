"""Rejected residual-bound controls for the fixed reachable-diagnosis workload.

python -m experiments.program_family_bound_controls --h 2 --k 4
python -m experiments.program_family_bound_controls --h 2 --k 6 --out results.json

These are experiments, not production optimizers. The physical contract and
complete-program grammar are unchanged. The optimistic hidden-state controller
used by a Bellman bound is never executed or exposed to the continuation. M is
always applied in16 physical coordinates; only D/R transport uses the certified
four-coordinate contrast cone. Initial exploratory timings rejected all three
bounds on total cost despite fewer complete leaves. Such timings are instance-
specific, not a universal complexity result; rerun controls sequentially.

The checker verifies a supplied grammar-cover certificate without optimizing.
Both enumerators and searches include certificate serialization and checking in
their total cost. Counts distinguish terminal words formed before pruning from
complete words never formed in either discovery search or seed evaluation.
"""
from fractions import Fraction as F
from time import perf_counter
import argparse, json
from pathlib import Path

from cdka.maintenance_access import base_operators, base_probes
from cdka.semantic_closure import apply, push, dot, word_value
from cdka.reachable_diagnosis import (
    preparation_laws, plan_words, word_id, contract as physical_contract,
)
from cdka.reachable_restriction import (
    CONTRAST_BASIS, collapse, expand_contrast, contrast_signature,
    contrast_response, contrast_value, contrast_domain_preservation,
)
from cdka.reachable_interfaces import compile_reachable_interface, verify_reachable_interface

SEARCH_MODES = ('physical32', 'signed16', 'four_mix')
MODES = ('baseline4_existing', 'baseline4_shared') + SEARCH_MODES
SCHEMA = 'cdka.rejected-program-family-bounds/v1'


def _count(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(name + ' must be a nonnegative integer')
    return value


def _modes(values):
    values = tuple(values)
    if not values or len(set(values)) != len(values) or any(v not in MODES for v in values):
        raise ValueError('modes must be distinct members of ' + ','.join(MODES))
    return values


def _scope(cohort, K):
    if not cohort:
        raise ValueError('a nonempty preparation cohort is required')
    h = len(next(iter(cohort))) if next(iter(cohort)) != 'I' else 0
    return physical_contract(h, K)


def _json_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      default=str, allow_nan=False).encode()


def _proof(cert):
    return {key: cert[key] for key in (
        'schema', 'mode', 'contract', 'preparations', 'max_cert', 'min_cert',
        'best', 'witness', 'word', 'regret',
    )}


def maximum(a,b): return tuple(map(max,a,b))
def minimum(a,b): return tuple(map(min,a,b))


def residuals(ops,g,K):
    lo,hi = {},{}
    for k in range(K+1):
        if k==0: lo[k,0]=hi[k,0]=g
        else:
            a,b=(apply(ops[z],lo[k-1,0]) for z in 'DR')
            lo[k,0]=minimum(a,b)
            a,b=(apply(ops[z],hi[k-1,0]) for z in 'DR')
            hi[k,0]=maximum(a,b)
        aa=[apply(ops['M'],lo[k,0])]
        bb=[apply(ops['M'],hi[k,0])]
        if k==0: aa.append(g);bb.append(g)
        else:
            aa.extend(apply(ops[z],lo[k-1,1]) for z in 'DR')
            bb.extend(apply(ops[z],hi[k-1,1]) for z in 'DR')
        lo[k,1]=tuple(map(min,zip(*aa)))
        hi[k,1]=tuple(map(max,zip(*bb)))
    return lo,hi


def compile_four(ops,g,K,lo,hi):
    C={}
    for z in 'DR':
        assert contrast_domain_preservation(ops[z])['preserved']
        rows=[]
        for b in CONTRAST_BASIS:
            c=collapse(push(b,ops[z]))
            rows.append({i:p for i,p in enumerate((c[0],c[1],c[4],c[5])) if p})
        assert all(p>=0 for row in rows for p in row.values())
        C[z]=tuple(rows)
    # Positive weights x=-contrast multiply the signed basis B=-CONTRAST_BASIS.
    Bm=tuple(push(tuple(-v for v in b),ops['M']) for b in CONTRAST_BASIS)
    t=tuple(-v for v in contrast_response(g))
    ub={}
    for k in range(K+1):
        if k==0: ub[k,0]=t
        else: ub[k,0]=maximum(*(apply(C[z],ub[k-1,0]) for z in 'DR'))
        seed=tuple(sum((v*(hi[k,0][i] if v>=0 else lo[k,0][i])
                        for i,v in enumerate(b)),F(0)) for b in Bm)
        vals=[seed]
        if k==0: vals.append(t)
        else: vals.extend(apply(C[z],ub[k-1,1]) for z in 'DR')
        ub[k,1]=tuple(map(max,zip(*vals)))
    return C,ub


def baseline(ops,g,cohort,K,shared=False):
    _count(K, 'ordinary update count')
    start=perf_counter();words=plan_words(K);scope=_scope(cohort,K)
    sigs=[contrast_signature(*law) for law in cohort.values()]
    encoded=perf_counter()
    if shared:
        cache={():g}
        def response(w):
            if w not in cache: cache[w]=apply(ops[w[0]],response(w[1:]))
            return cache[w]
        columns=tuple(contrast_response(response(w)) for w in words)
    else:
        columns=tuple(contrast_response(word_value(ops,w,g)) for w in words)
    compiled=perf_counter()
    values=tuple(tuple(contrast_value(s,q) for q in columns) for s in sigs)
    valued=perf_counter()
    labels=[word_id(w) for w in words]
    cert=compile_reachable_interface(values,preparation_labels=list(cohort),plan_labels=labels,contract=scope)
    certified=perf_counter()
    encoded_cert=_json_bytes(cert);serialized=perf_counter()
    decoded_cert=json.loads(encoded_cert);decoded=perf_counter()
    verify_reachable_interface(decoded_cert,values,preparation_labels=list(cohort),plan_labels=labels,contract=scope)
    checked=perf_counter()
    best=tuple(max(row) for row in values)
    regrets=tuple(max(b-row[j] for b,row in zip(best,values)) for j in range(len(words)))
    optimum=min(regrets);j=regrets.index(optimum)
    return {'method':'baseline4_shared' if shared else 'baseline4_existing',
            'K':K,'histories':len(cohort),'plans':len(words),
            'encoding_s':encoded-start,'compile_s':compiled-encoded,
            'query_s':valued-compiled,'certificate_compile_s':certified-valued,
            'serialization_s':serialized-certified,'deserialization_s':decoded-serialized,
            'certificate_bytes':len(encoded_cert),'check_s':checked-decoded,'total_s':checked-start,
            'decision_s':valued-start,
            'constructed':len(words),'never_constructed':0,
            'best':list(map(str,best)),'word':labels[j],'regret':str(optimum)},best,optimum


class Search:
    def __init__(self,ops,g,cohort,K,mode):
        _count(K, 'ordinary update count')
        if mode not in SEARCH_MODES: raise ValueError('unknown bound mode')
        self.ops=ops;self.g=g;self.K=K;self.mode=mode
        self.scope=_scope(cohort,K);self.preparations=list(cohort)
        self.sigs=[contrast_signature(*law) for law in cohort.values()]
        self.constructed=set();self.bound_calls=0;self.pushes=0
        self.lo,self.hi=residuals(ops,g,K)
        self.C,self.u4=(compile_four(ops,g,K,self.lo,self.hi)
                       if mode=='four_mix' else (None,None))
        if mode=='physical32': self.initial=tuple(cohort.values())
        elif mode=='signed16': self.initial=tuple(tuple(b-a for a,b in zip(*law)) for law in cohort.values())
        else:
            self.initial=tuple(tuple(-x for x in s[1]) for s in self.sigs)
            assert all(x>=0 for row in self.initial for x in row)

    def upper(self,states,k,m):
        self.bound_calls+=1
        if self.mode=='physical32':
            return tuple(F(1,2)+dot(b,self.hi[k,m])-dot(a,self.lo[k,m]) for a,b in states)
        if self.mode=='four_mix' and m:
            return tuple(F(1,2)+dot(s,self.u4[k,m]) for s in states)
        return tuple(F(1,2)+sum((v*(self.hi[k,m][i] if v>=0 else self.lo[k,m][i])
                               for i,v in enumerate(s)),F(0)) for s in states)

    def advance(self,states,a,m):
        self.pushes+=1
        if self.mode=='physical32': return tuple(tuple(push(row,self.ops[a]) for row in law) for law in states)
        if self.mode=='four_mix' and m:
            if a!='M': return tuple(push(s,self.C[a]) for s in states)
            return tuple(push(expand_contrast(tuple(-v for v in s)),self.ops[a]) for s in states)
        return tuple(push(s,self.ops[a]) for s in states)

    def exact(self,states,m):
        if self.mode=='physical32': return tuple(F(1,2)+dot(b,self.g)-dot(a,self.g) for a,b in states)
        if self.mode=='four_mix' and m:
            q=tuple(-v for v in contrast_response(self.g))
            return tuple(F(1,2)+dot(s,q) for s in states)
        return tuple(F(1,2)+dot(s,self.g) for s in states)

    def values(self,w):
        self.constructed.add(w)
        q=contrast_response(word_value(self.ops,w,self.g))
        return tuple(contrast_value(s,q) for s in self.sigs)

    def solve(self):
        seeds=[tuple('D'*self.K+'M')]
        if self.K: seeds.append(tuple('R'+'D'*(self.K-1)+'M'))
        if self.K>=2:seeds.append(tuple('DR'+'D'*(self.K-2)+'M'))
        seedv=[self.values(w) for w in seeds]
        best=[max(row[h] for row in seedv) for h in range(len(self.sigs))]
        witness=[seeds[max(range(len(seeds)),key=lambda j:seedv[j][h])] for h in range(len(best))]
        maxstats={'visits':0,'prunes':0,'evaluated':0,'family_leaves_pruned':0}
        maxcert=[]
        def count(k,m):return ((k+2) if m else 1)*2**k
        def inform(states,k,m,w):
            maxstats['visits']+=1
            if k==0:self.constructed.add(w)
            ub=self.upper(states,k,m)
            if all(u<=b for u,b in zip(ub,best)):
                maxstats['prunes']+=1;maxstats['family_leaves_pruned']+=count(k,m)
                maxcert.append((w,k,m,'prune'));return
            maxcert.append((w,k,m,'expand'))
            if k==0:
                val=self.exact(states,m);maxstats['evaluated']+=1
                for h,v in enumerate(val):
                    if v>best[h]:best[h]=v;witness[h]=w
            if k:
                for a in 'DR':inform(self.advance(states,a,m),k-1,m,w+(a,))
            if m:inform(self.advance(states,'M',m),k,0,w+('M',))
        t0=perf_counter();inform(self.initial,self.K,1,());t1=perf_counter()
        candidate_words=sorted(set(seeds+witness),key=lambda w:(len(w),w))
        candidate_values=[self.values(w) for w in candidate_words]
        rs=[max(b-v for b,v in zip(best,vs)) for vs in candidate_values]
        j=min(range(len(rs)),key=rs.__getitem__)
        incumbent=rs[j];chosen=candidate_words[j]
        minstats={'visits':0,'prunes':0,'evaluated':0,'family_leaves_pruned':0}
        mincert=[]
        def common(states,k,m,w):
            nonlocal incumbent,chosen
            minstats['visits']+=1
            if k==0:self.constructed.add(w)
            ub=self.upper(states,k,m)
            if max(b-u for b,u in zip(best,ub))>=incumbent:
                minstats['prunes']+=1;minstats['family_leaves_pruned']+=count(k,m)
                mincert.append((w,k,m,'prune'));return
            mincert.append((w,k,m,'expand'))
            if k==0:
                vs=self.exact(states,m);r=max(b-v for b,v in zip(best,vs));minstats['evaluated']+=1
                if r<incumbent:incumbent=r;chosen=w
            if k:
                for a in 'DR':common(self.advance(states,a,m),k-1,m,w+(a,))
            if m:common(self.advance(states,'M',m),k,0,w+('M',))
        common(self.initial,self.K,1,());t2=perf_counter()
        return {'schema':SCHEMA,'mode':self.mode,'contract':self.scope,
                'preparations':self.preparations,
                'max_cert':maxcert,'min_cert':mincert,'best':best,'witness':witness,
                'word':chosen,'regret':incumbent,'informed_s':t1-t0,'common_s':t2-t1,
                'informed':maxstats,'common':minstats,'constructed':len(self.constructed),
                'never_constructed':(self.K+2)*2**self.K-len(self.constructed),
                'bound_calls':self.bound_calls,'pushes':self.pushes}

    def check(self,cert):
        # Recompute each residual envelope from physical kernels; complete coverage
        # is checked recursively.  The verifier does not discover another optimum.
        lo,hi=residuals(self.ops,self.g,self.K)
        assert cert['schema']==SCHEMA and cert['mode']==self.mode
        assert cert['contract']==self.scope and cert['preparations']==self.preparations
        C,u4=(compile_four(self.ops,self.g,self.K,lo,hi)
              if self.mode=='four_mix' else (None,None))
        assert (lo,hi,C,u4)==(self.lo,self.hi,self.C,self.u4)
        best=tuple(map(F,cert['best']));r=F(cert['regret'])
        assert len(best)==len(self.sigs)==len(cert['witness'])
        def legal(w):
            w=tuple(w)
            assert all(a in ('D','R','M') for a in w)
            assert w.count('D')+w.count('R')==self.K and w.count('M')<=1
            return w
        for h,w in enumerate(cert['witness']): assert self.values(legal(w))[h]==best[h]
        assert max(b-v for b,v in zip(best,self.values(legal(cert['word']))))==r
        for records,kind in [(cert['max_cert'],'max'),(cert['min_cert'],'min')]:
            recordmap={tuple(w):(k,m,status) for w,k,m,status in records}
            assert len(recordmap)==len(records)
            seen=set()
            def check_node(states,k,m,w):
                assert recordmap[w][:2]==(k,m);seen.add(w)
                status=recordmap[w][2]
                if status=='prune':
                    ub=self.upper(states,k,m)
                    if kind=='max':assert all(u<=b for u,b in zip(ub,best))
                    else:assert max(b-u for b,u in zip(best,ub))>=r
                    return
                assert status=='expand'
                if k==0:
                    vals=self.exact(states,m)
                    if kind=='max':assert all(v<=b for v,b in zip(vals,best))
                    else:assert max(b-v for b,v in zip(best,vals))>=r
                if k:
                    for a in 'DR':check_node(self.advance(states,a,m),k-1,m,w+(a,))
                if m:check_node(self.advance(states,'M',m),k,0,w+('M',))
            check_node(self.initial,self.K,1,());assert seen==set(recordmap)
        return True


def run(h,K,modes):
    _count(h, 'history length');_count(K, 'ordinary update count');modes=_modes(modes)
    t=perf_counter();ops=base_operators();g=base_probes()['readout'];cohort=preparation_laws(h)
    shared_s=perf_counter()-t
    out={'schema':SCHEMA,'h':h,'K':K,'shared_setup_s':shared_s,'results':[]}
    reference=None
    for mode in modes:
        if mode in ('baseline4_existing','baseline4_shared'):
            row,best,opt=baseline(ops,g,cohort,K,shared=mode.endswith('shared'))
        else:
            t0=perf_counter();search=Search(ops,g,cohort,K,mode);t1=perf_counter()
            cert=search.solve();t2=perf_counter()
            encoded_cert=_json_bytes(_proof(cert));serialized=perf_counter()
            decoded_cert=json.loads(encoded_cert);decoded=perf_counter()
            search.check(decoded_cert);t3=perf_counter()
            best,opt=tuple(cert['best']),cert['regret']
            row={key:value for key,value in cert.items() if key not in (
                'schema','mode','contract','preparations','max_cert','min_cert','witness','best')}
            row.update({'method':mode,'compile_s':t1-t0,'search_s':t2-t1,
                        'serialization_s':serialized-t2,'deserialization_s':decoded-serialized,
                        'certificate_bytes':len(encoded_cert),
                        'check_s':t3-decoded,'total_s':t3-t0,'decision_s':t2-t0,
                        'word':word_id(cert['word']),'regret':str(cert['regret']),
                        'best':list(map(str,cert['best'])),
                        'certificate_nodes':len(cert['max_cert'])+len(cert['min_cert'])})
        if reference is not None:assert (best,opt)==reference
        else:reference=(best,opt)
        row['total_including_shared_s']=row['total_s']+shared_s
        out['results'].append(row)
        print(json.dumps({'h':h,'K':K,**row},default=str),flush=True)
    return out


if __name__=='__main__':
    def nonnegative(value):
        try: return _count(int(value),'count')
        except ValueError as error: raise argparse.ArgumentTypeError(str(error)) from error
    def mode_list(value):
        try: return _modes(value.split(','))
        except ValueError as error: raise argparse.ArgumentTypeError(str(error)) from error
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--h',type=nonnegative,default=2);p.add_argument('--k',type=nonnegative,default=4)
    p.add_argument('--modes',type=mode_list,default=MODES)
    p.add_argument('--out');a=p.parse_args()
    result=run(a.h,a.k,a.modes)
    if a.out:Path(a.out).write_text(json.dumps(result,indent=2,default=str)+'\n')
