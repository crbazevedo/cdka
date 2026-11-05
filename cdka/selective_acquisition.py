"""CDKA v18: continuation-certified acquisition with a priced, fallible enable.

Fixed v16 physical plant. The extra circuit sees only (executed repair,
pre-cycle balance==3), never health or memory contents. One fresh output
fault per installed NAND, with shared-wire dependencies retained. It is invoked
only after work succeeds, then selects refresh vs physical retention.

The old token ledger is unchanged; write/gate workload is separately priced in
write-equivalent units. No implicit refund or conversion of tokens into joules.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from math import comb,lcm
from .recurrent_maintenance import Model,Policy,MODES,BITS,probability,select_probability,health_after_service,next_health,task_success,initial_micro,gate_execution,raw_task_success

CONTEXTS=tuple(product((0,1),repeat=2)) # (repair, balance==3)
MACRO=tuple(product((0,1),(0,1),range(3),range(1,5)))
IX={s:i for i,s in enumerate(MACRO)}

@dataclass(frozen=True)
class Enable:
    gates: tuple=()
    output: int=1
    def __post_init__(self):
        if not 0<=self.output<4+len(self.gates):raise ValueError('bad output')
        for i,pair in enumerate(self.gates):
            if len(pair)!=2 or not 0<=pair[0]<=pair[1]<4+i:raise ValueError('noncausal gate')
    @property
    def cost(self):return len(self.gates)
    def run(self,repair,b3,faults=()):
        if len(faults)!=len(self.gates):raise ValueError('one flag per physical gate')
        if repair not in (0,1) or b3 not in (0,1) or any(e not in (0,1) for e in faults):raise ValueError('binary input')
        w=[0,1,repair,b3]
        for (a,b),e in zip(self.gates,faults):w.append((1-(w[a]&w[b]))^e)
        return w[self.output]
    def truth(self):return tuple(self.run(*x,(0,)*self.cost) for x in CONTEXTS)
    def probabilities(self,gamma=F(0)):
        g=probability(gamma)
        if g>F(1,2):raise ValueError('gate flip <=1/2')
        return tuple(sum((g**sum(e)*(1-g)**(self.cost-sum(e))*self.run(*x,e)
                          for e in product((0,1),repeat=self.cost)),F(0)) for x in CONTEXTS)
    def profile(self):
        return tuple(tuple(sum(self.run(*x,e) for e in product((0,1),repeat=self.cost) if sum(e)==k)
                           for k in range(self.cost+1)) for x in CONTEXTS)

FRESH=Enable((),1)
RETAIN=Enable((),0)
ELIDE=Enable(((2,3),),4) # only omit after SERVICE at pre-balance3

def rooted(gates):
    needed={3+len(gates)}
    for i in reversed(range(len(gates))):
        if 4+i in needed:needed.update(j for j in gates[i] if j>=4)
    return all(4+i in needed for i in range(len(gates)))

@lru_cache(None)
def library(capacity=2):
    if type(capacity) is not int or not 0<=capacity<=2:raise ValueError('bounded exact capacity0..2')
    entries=[Enable((),i) for i in range(4)];stats=[dict(gates=0,netlists=4,channels=4)]
    def generate(d,prefix=()):
        if len(prefix)==d:
            if rooted(prefix):yield Enable(prefix,3+d)
            return
        for pair in combinations_with_replacement(range(4+len(prefix)),2):yield from generate(d,prefix+(pair,))
    for d in range(1,capacity+1):
        by={};raw=0
        for c in generate(d):
            raw+=1;by.setdefault(c.profile(),c)
        entries.extend(by.values());stats.append(dict(gates=d,netlists=raw,channels=len(by)))
    return tuple(entries),tuple(stats)


def projection(s):
    z,(a,b,c),balance=s
    return z,a,b+c,balance

@lru_cache(None)
def branch_rows(p,policy,label,repair,xi=F(0)):
    """One branch: full contribution K_ret, K_fresh, successful mass, attempt mass."""
    z,a,k,b=label;bits=(a,int(k>=1),int(k==2));out_r={};out_f={}
    pr=select_probability(p,z,bits,policy.mode(b));pd=pr if repair else 1-pr
    if not pd:return out_r,out_f,F(0),F(0)
    if b<1+2*repair:raise AssertionError('overspend')
    b1=min(4,b+1-2*repair);live_sum=F(0)
    for h,ph in health_after_service(p,z,repair):
        live=pd*ph*task_success(p,h)*(1-p.procedure_failure if repair else 1)
        live_sum+=live
        for z1,pz in next_health(p,h):
            one=p.diagnostic_error if h==0 else 1-p.diagnostic_error
            for aa in (0,1):
                for kk in range(3):
                    pf=(one if aa else 1-one)*comb(2,kk)*one**kk*(1-one)**(2-kk)
                    key=(z1,aa,kk,b1);j=IX[key]
                    out_f[j]=out_f.get(j,F(0))+live*pz*pf
            for aa in (0,1):
                pa=1-xi if aa==a else xi
                for erased in range(k+1):
                    for inserted in range(3-k):
                        kk=k-erased+inserted
                        pt=F(comb(k,erased)*comb(2-k,inserted))*xi**(erased+inserted)*(1-xi)**(2-erased-inserted)
                        j=IX[(z1,aa,kk,b1)];v=live*pz*pa*pt
                        if v:out_r[j]=out_r.get(j,F(0))+v
    return out_r,out_f,live_sum,pd

@lru_cache(None)
def exact_kernel(p,policy,probabilities,xi=F(0)):
    """Exact48-state row construction. Returns Q and write/service reward vectors."""
    if len(probabilities)!=4 or any(not 0<=f<=1 for f in probabilities):raise ValueError('four probabilities')
    rows=[];writes=[];services=[]
    for label in MACRO:
        row={};wr=F(0);sr=F(0)
        for r in (0,1):
            kr,kf,live,attempt=branch_rows(p,policy,label,r,xi)
            f=probabilities[2*r+int(label[3]==3)]
            wr+=f*live;sr+=r*attempt
            for j in kr.keys()|kf.keys():
                v=(1-f)*kr.get(j,F(0))+f*kf.get(j,F(0))
                if v:row[j]=row.get(j,F(0))+v
        if sum(row.values(),F(0))>1:raise AssertionError('superstochastic')
        rows.append(row);writes.append(wr);services.append(sr)
    return tuple(rows),tuple(writes),tuple(services)


def initial_vector(p,prior=F(1,2)):
    row=[F(0)]*48
    for s,v in initial_micro(p,prior).items():row[IX[projection(s)]]+=v
    return tuple(row)


def integer_evaluate(p,policy,probs,horizon=8,xi=F(0),prior=F(1,2),curve=False):
    """Exact integer propagation with common denominators. No float ranking."""
    if type(horizon)is not int or horizon<0:raise ValueError('nonnegative horizon')
    rows,wr,sr=exact_kernel(p,policy,tuple(map(F,probs)),F(xi))
    den=lcm(*(v.denominator for row in rows for v in row.values()),*(v.denominator for v in wr),*(v.denominator for v in sr))
    Q=tuple(tuple((j,int(v*den)) for j,v in row.items()) for row in rows)
    W=tuple(int(v*den) for v in wr);S=tuple(int(v*den) for v in sr)
    mu=initial_vector(p,prior);md=lcm(*(v.denominator for v in mu));law=tuple(int(v*md) for v in mu)
    work=md;gate_events=0;service=0;out=[F(1)]
    for _ in range(horizon):
        work=work*den+sum(a*b for a,b in zip(law,W))
        service=service*den+sum(a*b for a,b in zip(law,S))
        nxt=[0]*48
        for i,a in enumerate(law):
            if a:
                for j,b in Q[i]:nxt[j]+=a*b
        gate_events=gate_events*den+sum(nxt)
        law=tuple(nxt);md*=den
        if curve:out.append(F(sum(law),md))
    ans={'survival':F(sum(law),md),'writes':F(work,md),'services':F(service,md),
         'successful_epochs':F(gate_events,md)}
    if curve:ans['curve']=tuple(out)
    return ans


def evaluate(circuit=ELIDE,gamma=F(0),horizon=8,p=Model(),policy=Policy(),xi=F(0),prior=F(1,2)):
    r=integer_evaluate(p,policy,circuit.probabilities(gamma),horizon,xi,prior)
    return dict(r,gates=circuit.cost,gate_executions=circuit.cost*r['successful_epochs'])


def total_cost(result,write_price=F(1),gate_price=F(1,100),installation_price=F(1,10)):
    """Expected acquisition-workload charge. Original actuator tokens unchanged."""
    return write_price*result['writes']+gate_price*result['gate_executions']+installation_price*result['gates']


def raw_row(p,policy,circuit,gamma,state,xi=F(0)):
    """Independent explicit six-NAND decision, enable-fault and cell event oracle."""
    from .recurrent_maintenance import report_probability,next_health,raw_task_success
    z,m,b=state;mode=policy.mode(b);choices={}
    if mode in ('skip','service'):choices[int(mode=='service')]=F(1)
    else:
        for e in product((0,1),repeat=6):
            r=gate_execution(m,e)^int(mode=='inverse');mass=p.rate(z)**sum(e)*(1-p.rate(z))**(6-sum(e))
            choices[r]=choices.get(r,F(0))+mass
    out={}
    for r,pd in choices.items():
        if b<1+2*r:raise AssertionError('overspend')
        for restored,ph in ((0,1-p.restoration),(1,p.restoration)) if r else ((0,F(1)),):
            h=0 if restored else z;v=pd*ph*(1-p.procedure_failure if r else 1)*raw_task_success(p,h)
            for flags in product((0,1),repeat=circuit.cost):
                enable=circuit.run(r,int(b==3),flags)
                pf=gamma**sum(flags)*(1-gamma)**(circuit.cost-sum(flags))
                for noise in BITS:
                    rate=p.diagnostic_error if enable else xi
                    target=tuple((h if enable else old)^f for old,f in zip(m,noise))
                    pm=rate**sum(noise)*(1-rate)**(3-sum(noise))
                    for zz,pz in next_health(p,h):
                        key=(zz,target,min(4,b+1-2*r));mass=v*pf*pm*pz
                        if mass:out[key]=out.get(key,F(0))+mass
    return out


def annihilation_certificate(p=Model(),policy=Policy()):
    Q,_,_=exact_kernel(p,policy,(F(1),)*4)
    T,_,_=exact_kernel(p,policy,tuple(map(F,ELIDE.truth())))
    checked=0
    for a,b in zip(Q,T):
        d={j:b.get(j,F(0))-a.get(j,F(0)) for j in a.keys()|b.keys()}
        if sum(d.values(),F(0)):return False
        for P in (Q,T):
            product_row={}
            for j,w in d.items():
                if w:
                    for k,v in P[j].items():product_row[k]=product_row.get(k,F(0))+w*v
            if any(product_row.values()):return False
            checked+=1
    return checked #96 row identities


def safe_extra_write_kernel(p,policy,gamma):
    """Missed omission only: extra writes on the safe branch, never false omit."""
    return exact_kernel(p,policy,(F(1),F(1),F(1),F(gamma)))[0]


def ranking(p=Model(),gamma=F(0),horizon=8,capacity=2,policy=Policy(),xi=F(0)):
    # Complete physical channel/cost library. Duplicate zero-noise truth maps at
    # equal cost evaluated once; at positive noise retain output profiles.
    out=[];seen=set()
    for c in library(capacity)[0]:
        f=c.probabilities(gamma);key=(c.cost,f)
        if key in seen:continue
        seen.add(key)
        value=evaluate(c,gamma,horizon,p,policy,xi)
        out.append(dict(value,circuit=c,truth=c.truth(),probabilities=f))
    return tuple(out)


def poly_eval(coeff,x):
    out=F(0)
    for c in reversed(coeff):out=out*x+c
    return out


def elision_polynomials(horizon=8,p=Model(),policy=Policy()):
    """Exact power coefficients in common output-flip gamma of the one NAND.
    Q_gamma=Q_0+gamma*(Q_1-Q_0). Gamma=1 is algebraic endpoint only;
    the physical gate-error experiments use [0,1/2].
    """
    q0,w0,sr=exact_kernel(p,policy,(F(1),F(1),F(1),F(0)))
    q1,w1,_=exact_kernel(p,policy,(F(0),F(0),F(0),F(1)))
    den=lcm(*(v.denominator for row in q0+q1 for v in row.values()),*(v.denominator for v in w0+w1))
    A=tuple(tuple((j,int(v*den)) for j,v in row.items()) for row in q0)
    B=tuple(tuple((j,int((y.get(j,F(0))-x.get(j,F(0)))*den)) for j in x.keys()|y.keys() if y.get(j,F(0))!=x.get(j,F(0))) for x,y in zip(q0,q1))
    W=tuple(int(w*den) for w in w0);DW=tuple(int((b-a)*den) for a,b in zip(w0,w1))
    mu=initial_vector(p);md=lcm(*(x.denominator for x in mu));law=[[int(x*md) for x in mu]];cost=[md];events=[0]
    for t in range(horizon):
        nxt=[[0]*48 for _ in range(len(law)+1)]
        newcost=[x*den for x in cost]+[0]
        newevents=[x*den for x in events]+[0]
        for k,coeff in enumerate(law):
            newcost[k]+=sum(a*b for a,b in zip(coeff,W))
            newcost[k+1]+=sum(a*b for a,b in zip(coeff,DW))
            for i,a in enumerate(coeff):
                if a:
                    for j,b in A[i]:nxt[k][j]+=a*b
                    for j,b in B[i]:nxt[k+1][j]+=a*b
        for k,row in enumerate(nxt):newevents[k]+=sum(row)
        law=nxt;cost=newcost;events=newevents;md*=den
    return {'survival':tuple(F(sum(c),md) for c in law),'writes':tuple(F(c,md) for c in cost),'events':tuple(F(c,md) for c in events)}


def bernstein(power,left,right):
    """Exact power-to-Bernstein coefficients on [left,right]."""
    d=len(power)-1
    local=[sum((F(power[k])*comb(k,j)*left**(k-j)*(right-left)**j for k in range(j,d+1)),F(0)) for j in range(d+1)]
    return tuple(sum((local[j]*F(comb(i,j),comb(d,j)) for j in range(i+1)),F(0)) for i in range(d+1))


def noise_certificate(horizon=8,tolerance=F(1,10000)):
    p=elision_polynomials(horizon);base=evaluate(FRESH,horizon=horizon)['survival']
    loss=tuple((base if i==0 else F(0))-c for i,c in enumerate(p['survival']))
    derivative=tuple((i+1)*loss[i+1] for i in range(len(loss)-1))
    positive=bernstein(derivative,F(0),F(1,10))
    if min(positive)<=0:raise AssertionError('no monotonic certificate')
    lo,hi=F(0),F(1,10)
    if not poly_eval(loss,hi)>tolerance:raise ValueError('threshold outside bracket')
    for _ in range(70):
        mid=(lo+hi)/2
        if poly_eval(loss,mid)<=tolerance:lo=mid
        else:hi=mid
    return dict(polynomials=p,loss=loss,derivative_bernstein=positive,domain=(F(0),F(1,10)),tolerance=tolerance,threshold=(lo,hi))


def refunded_evaluate(credit=1,horizon=8,p=Model(),policy=Policy()):
    """Adversarial DIFFERENT ledger: omitted acquisition refunds balance credit.
    The old DQ=0 proof cannot be transported to this new physical contract.
    """
    if credit not in (0,1):raise ValueError('credit0/1 only')
    rows=[]
    for label in MACRO:
        row={}
        for r in (0,1):
            kr,kf,_,_=branch_rows(p,policy,label,r)
            omit=r and label[3]==3
            src=kr if omit else kf
            for j,v in src.items():
                target=MACRO[j]
                jj=IX[target[:3]+(min(4,target[3]+credit),)] if omit else j
                row[jj]=row.get(jj,F(0))+v
        rows.append(row)
    mu=initial_vector(p)
    for _ in range(horizon):
        nxt=[F(0)]*48
        for i,m in enumerate(mu):
            if m:
                for j,q in rows[i].items():nxt[j]+=m*q
        mu=tuple(nxt)
    return sum(mu,F(0))


def localized_gate_sensitivity(horizon=8,p=Model(),policy=Policy()):
    f=tuple(map(F,ELIDE.truth()));Q=exact_kernel(p,policy,f)[0]
    diffs=[]
    for j in range(4):
        altered=list(f);altered[j]=1-altered[j]
        alt=exact_kernel(p,policy,tuple(altered))[0]
        diffs.append(tuple({k:b.get(k,F(0))-a.get(k,F(0)) for k in a.keys()|b.keys() if b.get(k,F(0))!=a.get(k,F(0))} for a,b in zip(Q,alt)))
    v=[[F(1)]*48]
    for _ in range(horizon):v.append([sum((w*v[-1][k] for k,w in row.items()),F(0)) for row in Q])
    mu=initial_vector(p);out=[]
    for t in range(horizon):
        future=v[horizon-1-t]
        contributions=[sum((mu[i]*sum((w*future[k] for k,w in row.items()),F(0)) for i,row in enumerate(d)),F(0)) for d in diffs]
        out.append({'epoch':t+1,'by_input':tuple(contributions),'sum':sum(contributions,F(0))})
        nxt=[F(0)]*48
        for i,mass in enumerate(mu):
            if mass:
                for k,w in Q[i].items():nxt[k]+=mass*w
        mu=tuple(nxt)
    return tuple(out)
