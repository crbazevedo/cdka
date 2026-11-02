"""CDKA v6: declared component contracts and an exact observable quotient.

Known Markov aggregation/coupling instruments, not a novel agency theorem.
The world changes. Correction, sensing, writing, actuation and servicing are
fallible. Death is absorbing and never renormalized away. A readable health
flag, declared stage clock and perfect resource ledger remain assumptions.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb

DEAD = 'dead'
COST = {'hold': 0, 'correct': 1, 'refresh': 2, 'service': 2}


def add(row, key, value):
    if value:
        row[key] = row.get(key, F(0)) + value


def binom(n, p):
    p = F(p)
    return tuple(F(comb(n,j))*p**j*(1-p)**(n-j) for j in range(n+1))


def tv(p, q):
    if sum(p.values(),F(0)) != 1 or sum(q.values(),F(0)) != 1:
        raise ValueError('complete probability rows including death required')
    return sum((abs(p.get(k,F(0))-q.get(k,F(0)))
                for k in p.keys()|q.keys()),F(0))/2


@dataclass(frozen=True)
class Contract:
    capacity: int = 4
    harvest: int = 1
    world_flip: F = F(1,10)
    cell_flip: F = F(1,50)
    write_flip: F = F(1,100)
    correction_error: tuple = (F(1,100), F(1,5))
    sensor_error: tuple = (F(1,25), F(1,5))
    actuator_failure: tuple = (F(1,200), F(3,100))
    degradation: F = F(1,20)
    service_success: F = F(4,5)

    def __post_init__(self):
        if type(self.capacity) is not int or self.capacity<0:
            raise ValueError('nonnegative integer capacity')
        if type(self.harvest) is not int or self.harvest<0:
            raise ValueError('nonnegative integer harvest')
        for name in ('world_flip','cell_flip','write_flip','degradation','service_success'):
            p=F(getattr(self,name))
            if not 0<=p<=1: raise ValueError(name)
            object.__setattr__(self,name,p)
        for name in ('correction_error','sensor_error','actuator_failure'):
            ps=tuple(map(F,getattr(self,name)))
            if len(ps)!=2 or any(not 0<=p<=1 for p in ps): raise ValueError(name)
            object.__setattr__(self,name,ps)

    def actions(self,b):
        return tuple(a for a,cost in COST.items() if cost<=b)

    def states(self):
        return tuple(product((0,1),(0,1),range(self.capacity+1)))

    def micros(self):
        return tuple((w,m,h,b) for w in (0,1)
                     for m in product((0,1),repeat=3)
                     if sum(bit!=w for bit in m)<=1
                     for h in (0,1) for b in range(self.capacity+1))


def quotient(s):
    if s==DEAD: return DEAD
    w,m,h,b=s
    k=sum(x!=w for x in m)
    if k>1: raise ValueError('not a viable epoch-boundary state')
    return k,h,b


def readable(s):
    """Runtime input: disagreement, health and balance; no hidden W."""
    if s==DEAD: return DEAD
    _,m,h,b=s
    return int(sum(m) not in (0,3)),h,b


def health_row(p,h,a):
    base={0:1-p.degradation,1:p.degradation} if h==0 else {1:F(1)}
    if a!='service': return base
    result={}
    add(result,0,p.service_success)
    for h1,q in base.items(): add(result,h1,(1-p.service_success)*q)
    return result


@lru_cache(None)
def damage_row(p,k):
    """Independent binomial-convolution derivation, not raw-bit enumeration."""
    result={}
    for flipped_world,pw in ((0,1-p.world_flip),(1,p.world_flip)):
        old=3-k if flipped_world else k
        for repaired_wrong,pr in enumerate(binom(old,p.cell_flip)):
            for damaged_right,pd in enumerate(binom(3-old,p.cell_flip)):
                add(result,old-repaired_wrong+damaged_right,pw*pr*pd)
    return result


@lru_cache(None)
def macro_row(p,s,a):
    """Exact local contract composition on (disagreement,health,balance)."""
    k,h,b=s
    if s not in p.states() or a not in p.actions(b): raise ValueError('state/action')
    damaged=damage_row(p,k)
    if a in ('hold','service'):
        after=damaged
    else:
        if a=='correct':
            correct=sum((v for j,v in damaged.items() if j<=1),F(0))
        else:
            correct=1-p.sensor_error[h]
        c=p.correction_error[h]
        correct=correct*(1-c)+(1-correct)*c
        after={j:correct*x+(1-correct)*y
               for j,(x,y) in enumerate(zip(binom(3,p.write_flip),binom(3,1-p.write_flip)))}
    row={}
    b1=min(p.capacity,b-COST[a]+p.harvest)
    for k1,pk in after.items():
        if k1<=1:
            for h1,ph in health_row(p,h,a).items():
                add(row,(k1,h1,b1),pk*ph*(1-p.actuator_failure[h]))
    row[DEAD]=1-sum(row.values(),F(0))
    return row


def mask_law(ps):
    for mask in product((0,1),repeat=3):
        prob=F(1)
        for bit,p in zip(mask,ps): prob*=p if bit else 1-p
        if prob: yield mask,prob


@lru_cache(None)
def micro_row(p,s,a,site_noise=None):
    """Independent raw-state oracle. Explicit world and all bit-mask branches.

    Controller selects a BEFORE world movement and faults. After a write,
    actuation succeeds only if current majority matches current W and the
    execution mechanism does not fail. No sensor is assumed perfect.
    The service affects next-epoch corrector health, not this epoch's gate.
    """
    w,m,h,b=s
    if a not in p.actions(b): raise ValueError('unaffordable action')
    ps=(p.cell_flip,)*3 if site_noise is None else tuple(map(F,site_noise))
    if len(ps)!=3 or any(not 0<=x<=1 for x in ps): raise ValueError('site noise')
    row={}
    for f,pw in ((0,1-p.world_flip),(1,p.world_flip)):
        w1=w^f
        for upset,pu in mask_law(ps):
            damaged=tuple(x^y for x,y in zip(m,upset))
            outputs={}
            if a in ('hold','service'):
                outputs[damaged]=F(1)
            else:
                majority=int(sum(damaged)>=2)
                guesses=((majority,F(1)),) if a=='correct' else ((w1,1-p.sensor_error[h]),(1-w1,p.sensor_error[h]))
                for guess,pg in guesses:
                    for gate,pc in ((0,1-p.correction_error[h]),(1,p.correction_error[h])):
                        intended=guess^gate
                        for noise,pwrite in mask_law((p.write_flip,)*3):
                            out=tuple(intended^bit for bit in noise)
                            add(outputs,out,pg*pc*pwrite)
            for out,po in outputs.items():
                prob=pw*pu*po
                if int(sum(out)>=2)!=w1: continue
                for h1,ph in health_row(p,h,a).items():
                    b1=min(p.capacity,b-COST[a]+p.harvest)
                    add(row,(w1,out,h1,b1),prob*(1-p.actuator_failure[h])*ph)
    row[DEAD]=1-sum(row.values(),F(0))
    return row


def aggregate(row):
    result={}
    for s,q in row.items(): add(result,quotient(s),q)
    return result


def solve(p,n):
    """Finite-horizon policy over READABLE syndrome/health/resource only."""
    if type(n) is not int or n<0: raise ValueError('nonnegative horizon')
    v={s:F(1) for s in p.states()};values=[v];policies=[{}]
    for t in range(1,n+1):
        v1={};pi={}
        for s in p.states():
            candidates={a:sum((q*v[y] for y,q in macro_row(p,s,a).items() if y!=DEAD),F(0))
                        for a in p.actions(s[2])}
            action=max(candidates,key=candidates.get)
            pi[s]=action;v1[s]=candidates[action]
        values.append(v1);policies.append(pi);v=v1
    return {'values':values,'policies':policies}


def evaluate(p,policies):
    v={s:F(1) for s in p.states()}
    for pi in policies[1:]:
        v={s:sum((q*v[y] for y,q in macro_row(p,s,pi[s]).items() if y!=DEAD),F(0)) for s in p.states()}
    return v


def quotient_report(p):
    maximum=F(0);count=0
    for s in p.micros():
        assert readable(s)==quotient(s)
        for a in p.actions(s[3]):
            distance=tv(aggregate(micro_row(p,s,a)),macro_row(p,quotient(s),a))
            maximum=max(maximum,distance);count+=1
    return {'micro_states':len(p.micros()),'macro_states':len(p.states()),
            'rows_checked':count,'max_tv':maximum}


def composition_bound(deltas,horizon):
    """Finite-path discrepancy. Same policy/interfaces; NOT an infinite support theorem."""
    if type(horizon) is not int or horizon<0: raise ValueError('horizon')
    keep=F(1)
    for d in deltas:
        d=F(d)
        if not 0<=d<=1: raise ValueError('TV bound')
        keep*=1-d
    return 1-keep**horizon


def calibration_report(p,q,n=10):
    """Uniform exact row-TV certificate between two fully specified kernels."""
    if p.states()!=q.states(): raise ValueError('same interface/state space required')
    delta=max(tv(macro_row(p,s,a),macro_row(q,s,a)) for s in p.states() for a in p.actions(s[2]))
    vp,vq=solve(p,n),solve(q,n)
    deployed=evaluate(p,vq['policies'])
    return {'delta':delta,'bound':composition_bound([delta],n),
            'max_optimum_gap':max(abs(vp['values'][-1][s]-vq['values'][-1][s]) for s in p.states()),
            'max_regret':max(vp['values'][-1][s]-deployed[s] for s in p.states())}


def sensor_derivative_row(p,s,a):
    """Exact derivative when BOTH sensor errors increase by the same theta.

    The physical policy and all other component contracts are frozen.
    Only refresh uses this sensor; local derivative masses sum to zero.
    """
    if a not in p.actions(s[2]): raise ValueError('unaffordable action')
    if a!='refresh': return {DEAD:F(0)}
    k,h,b=s
    good=binom(3,p.write_flip);bad=binom(3,1-p.write_flip)
    row={};b1=min(p.capacity,b-COST[a]+p.harvest)
    for k1 in (0,1):
        derivative=(1-2*p.correction_error[h])*(bad[k1]-good[k1])
        for h1,ph in health_row(p,h,a).items():
            add(row,(k1,h1,b1),derivative*ph*(1-p.actuator_failure[h]))
    row[DEAD]=-sum(row.values(),F(0))
    return row


def sensor_sensitivity(p,policies):
    """Product-rule propagation for a fixed policy; not gradient through argmax."""
    v={s:F(1) for s in p.states()};d={s:F(0) for s in p.states()}
    for pi in policies[1:]:
        nv={};nd={}
        for s in p.states():
            row=macro_row(p,s,pi[s]);dr=sensor_derivative_row(p,s,pi[s])
            nv[s]=sum((q*v[y] for y,q in row.items() if y!=DEAD),F(0))
            nd[s]=(sum((q*d[y] for y,q in row.items() if y!=DEAD),F(0))+
                   sum((q*v[y] for y,q in dr.items() if y!=DEAD),F(0)))
        v,d=nv,nd
    return d
