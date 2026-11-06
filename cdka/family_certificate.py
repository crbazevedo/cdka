"""Exact all-horizon equivalence of local stochastic implementation choices.

Scope: fixed terminal observables, finite explicit substochastic rows. A
common continuation invariant can certify all state/time/history-dependent
selections, a stronger statement than merely checking each stationary model.
The certificate is an evaluator object, NOT free runtime knowledge.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from collections import deque
from itertools import product
import random


def matvec(rows, v):
    return tuple(sum((p*v[j] for j,p in row.items()),F(0)) for row in rows)

class Basis:
    def __init__(self,n):
        self.n=n; self.vectors=[]; self.pivots={}
    def reduce(self,v):
        r=list(v); c=[F(0)]*len(self.vectors)
        for i,(u,a) in sorted(self.pivots.items()):
            t=r[i]
            if t:
                r=[x-t*y for x,y in zip(r,u)]
                for j,b in enumerate(a): c[j]+=t*b
        return tuple(c),tuple(r)
    def add(self,v):
        v=tuple(map(F,v));c,r=self.reduce(v)
        i=next((i for i,x in enumerate(r) if x),None)
        if i is None:return False
        t=r[i]; self.pivots[i]=(tuple(x/t for x in r),tuple(-a/t for a in c)+(1/t,))
        self.vectors.append(v);return True
    def coordinates(self,v):
        c,r=self.reduce(v)
        if any(r):raise ValueError('outside continuation basis')
        return c

@dataclass
class Certificate:
    basis: tuple
    transition: tuple
    observable_coordinates: tuple
    row_count: int
    witnesses: tuple
    @property
    def rank(self):return len(self.basis)
    def values_float(self,horizon):
        import numpy as np
        if type(horizon)is not int or horizon<0:raise ValueError('nonnegative horizon')
        c=np.array(self.transition,dtype=float)
        v=np.array(self.observable_coordinates,dtype=float)
        y=np.linalg.matrix_power(c,horizon)@v
        return np.array(self.basis,dtype=float).T@y
    def values_exact(self,horizon):
        v=self.observable_coordinates
        for _ in range(horizon):
            v=tuple(sum((a*b for a,b in zip(row,v)),F(0)) for row in self.transition)
        return tuple(sum((b[i]*c for b,c in zip(self.basis,v)),F(0)) for i in range(len(self.basis[0])))

def compile_family(choices,observable=None,max_rank=None):
    """Discover reference invariant and verify ALL local alternatives exactly.

    First choice per state defines reference Q. Retained vectors are Q**k g;
    a failed alternative produces an executable separating experiment. A rank
    limit returns UNKNOWN, never a false equivalence. Arithmetic bit cost counts
    separately from the matrix-operation bound.
    """
    n=len(choices)
    if not n or any(not rows for rows in choices):raise ValueError('nonempty choices')
    for rows in choices:
        for row in rows:
            if any(j<0 or j>=n or p<0 for j,p in row.items()) or sum(row.values(),F(0))>1:
                raise ValueError('invalid substochastic row')
    q=tuple(rows[0] for rows in choices);g=tuple(map(F,observable or [1]*n))
    b=Basis(n);b.add(g);queue=deque([(g,0)]);depths=[0]
    while queue:
        v,k=queue.popleft();nxt=matvec(q,v)
        if b.add(nxt):
            depths.append(k+1);queue.append((nxt,k+1))
            if max_rank and len(b.vectors)>max_rank:
                return {'accepted':False,'reason':'rank_limit','rank_lower_bound':len(b.vectors)}
    columns=[b.coordinates(matvec(q,v)) for v in b.vectors]
    for i,rows in enumerate(choices):
        for a,row in enumerate(rows[1:],1):
            for v,k in zip(b.vectors,depths):
                ref=sum((p*v[j] for j,p in rows[0].items()),F(0))
                alt=sum((p*v[j] for j,p in row.items()),F(0))
                if ref!=alt:
                    return {'accepted':False,'reason':'separating_row','state':i,'choice':a,
                        'reference_steps_after':k,'total_horizon':k+1,
                        'reference_value':str(ref),'alternative_value':str(alt),'difference':str(alt-ref)}
    d=len(b.vectors)
    return Certificate(tuple(b.vectors),tuple(tuple(columns[j][i] for j in range(d)) for i in range(d)),
                       b.coordinates(g),sum(map(len,choices)),tuple(depths))

def workflow_family(n=64,seed=23,choices_per_state=2,leak_power=16,perturb=False):
    """Synthetic randomized regenerative workflow, explicitly not public data.

    Distinct immediate state-failure probabilities prevent strong bisimulation
    merging. Alternative sparse routes preserve a future moment. The compiler
    receives raw rows, not the known rank or a proposed basis. Random relabeling
    prevents exploiting index layout. Parameters are rational.
    """
    if n<4 or n%2 or choices_per_state<2:raise ValueError('even n>=4, >=2 choices')
    rng=random.Random(seed);order=list(range(1,n+1));rng.shuffle(order)
    inverse={a:i for i,a in enumerate(order)};den=(n+1)*(2**leak_power)
    q=tuple(F(den-a,den) for a in order)
    result=[]
    for i in range(n):
        chosen=rng.sample(range(1,n//2+1),min(choices_per_state,n//2));rows=[]
        for a in chosen:
            j=inverse[a];k=inverse[n+1-a];rows.append({j:q[i]/2,k:q[i]/2})
        result.append(tuple(rows))
    if perturb:
        rows=list(result[0]);r=dict(rows[1]);j,k=tuple(r)
        shift=q[0]/100;r[j]+=shift;r[k]-=shift;rows[1]=r;result[0]=tuple(rows)
    return tuple(result),{'states':n,'choices':len(result[0]),'seed':seed,'q':q,
          'r':F(1)-F(1,2**(leak_power+1)),'family_log2_size':n,
          'class':'synthetic_mean_preserving_workflow','perturb':perturb}

def cdka_elision_family():
    """Actual v18 safe-elision family. Statewise choices relax runtime access;
    certifying the superset certifies implementable policies, not extra sensors.
    """
    from .selective_acquisition import exact_kernel,Model,Policy,ELIDE
    q=exact_kernel(Model(),Policy(),(F(1),)*4)[0]
    t=exact_kernel(Model(),Policy(),tuple(map(F,ELIDE.truth())))[0]
    choices=tuple((a,) if a==b else (a,b) for a,b in zip(q,t))
    return choices,{'states':len(q),'variable_rows':sum(len(x)>1 for x in choices),'class':'original_cdka_v18'}

def sparse_family(choices):
    import numpy as np
    from scipy.sparse import csr_matrix
    n=len(choices);width=max(map(len,choices));mats=[]
    for a in range(width):
        row=[];col=[];values=[]
        for i,opts in enumerate(choices):
            for j,p in opts[min(a,len(opts)-1)].items():row.append(i);col.append(j);values.append(float(p))
        mats.append(csr_matrix((values,(row,col)),shape=(n,n)))
    return tuple(mats)

def bellman(mats,horizon):
    import numpy as np
    n=mats[0].shape[0];lo=np.ones(n);hi=np.ones(n)
    for _ in range(horizon):
        lo=np.minimum.reduce([m@lo for m in mats]);hi=np.maximum.reduce([m@hi for m in mats])
    return lo,hi

def independent_enumeration(choices,horizon):
    n=len(choices);vectors=[]
    for policy in product(*(range(len(x)) for x in choices)):
        rows=[choices[i][policy[i]] for i in range(n)];v=(F(1),)*n
        for _ in range(horizon):v=matvec(rows,v)
        vectors.append(v)
    return tuple(min(v[i] for v in vectors) for i in range(n)),tuple(max(v[i] for v in vectors) for i in range(n))
