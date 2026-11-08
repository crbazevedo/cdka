"""Exact structural compilation of noncommuting common-reset processes.

Work and restart DO NOT generally commute, even on the goal. A restart maps
all surviving non-goal states to the same local distribution alpha, while
keeping completed work absorbing. Work runs become scalar survival factors.
The full binary Markov history is summed by work-run histogram, not occupancy.

Structural validation and small oracles use Fraction. Production values use
float64 log arithmetic; they are not rigorous numeric interval enclosures.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from hashlib import sha256
import json, math, re
import numpy as np

Matrix=tuple[tuple[F,...],...]
Vector=tuple[F,...]
class ContractError(ValueError):pass

def mat(x):return tuple(tuple(F(v) for v in row) for row in x)
def vector(x):return tuple(F(v) for v in x)
def horizon_ok(h):
    if type(h) is not int or h<0:raise ContractError('nonnegative integer horizon required')
def stochastic(q):
    n=len(q)
    if n==0 or any(len(r)!=n for r in q):raise ContractError('nonempty square matrix required')
    if any(x<0 for r in q for x in r) or any(sum(r,F(0))!=1 for r in q):raise ContractError('exact stochastic rows required')
def law_ok(v,n):
    if len(v)!=n or any(x<0 for x in v) or sum(v,F(0))!=1:raise ContractError('invalid probability law')
def mv(q,v):return tuple(sum((x*y for x,y in zip(r,v)),F(0)) for r in q)
def vm(v,q):return tuple(sum((v[i]*q[i][j] for i in range(len(v))),F(0)) for j in range(len(v)))
def mm(a,b):return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))) for i in range(len(a)))

@dataclass(frozen=True)
class Local:
    work: Matrix
    restart: Matrix
    initial: Vector
    target: tuple[int,...]
    @property
    def kernels(self):return (self.work,self.restart)

@dataclass(frozen=True)
class Model:
    components: tuple[Local,...]
    environment: Matrix=((F(9,10),F(1,10)),(F(1,5),F(4,5)))
    initial_environment: Vector=(F(1),F(0))
    exogenous_environment: bool=True
    conditional_product_noise: bool=True
    independent_initial: bool=True
    synchronous: bool=True


def validate(model):
    if not model.components:raise ContractError('at least one component required')
    if not all((model.exogenous_environment,model.conditional_product_noise,model.independent_initial,model.synchronous)):
        raise ContractError('unsupported dependence, control, initialization or timing')
    stochastic(model.environment)
    if len(model.environment)!=2:raise ContractError('binary work/restart environment')
    law_ok(model.initial_environment,2)
    details=[]
    for i,c in enumerate(model.components):
        stochastic(c.work);stochastic(c.restart);n=len(c.work)
        if len(c.restart)!=n:raise ContractError('kernel dimension mismatch')
        law_ok(c.initial,n)
        if not c.target or len(set(c.target))!=len(c.target) or any(type(x)is not int or not 0<=x<n for x in c.target):raise ContractError('invalid target set')
        transient=tuple(x for x in range(n) if x not in c.target)
        if not transient:raise ContractError('nonempty transient region required')
        if any(c.initial[x] for x in c.target):raise ContractError('initial law must equal restart law outside goal')
        for q in c.kernels:
            if any(q[g][j] for g in c.target for j in transient):raise ContractError('completion is not absorbing')
        for s in transient:
            if c.restart[s]!=c.initial:
                raise ContractError(f'component {i}: restart row {s} is not common initial law')
        details.append({'component':i,'states':n,'transient_states':len(transient),
                        'rank_one_restart_verified':True,'global_commutation':mm(c.work,c.restart)==mm(c.restart,c.work)})
    encoded=json.dumps({'model':model},default=lambda x:str(x),sort_keys=True).encode()
    return {'sha256':sha256(encoded).hexdigest(),'local_certificates':details,
            'components':len(model.components),'implicit_states':2*math.prod(len(c.initial) for c in model.components),
            'identity':'T_i^l (1 alpha_i) = (T_i^l 1) alpha_i; local noncompletion over runs is product alpha_i T_i^l 1',
            'scope':'exact structural contract; float64 output is not an interval certificate'}


def partition_number(n):
    """Euler DP, O(n^2); used for exact class-count certificate, not evaluation."""
    horizon_ok(n);p=[1]+[0]*n
    for k in range(1,n+1):
        for t in range(k,n+1):p[t]+=p[t-k]
    return p[n]


def run_partitions(h):
    """All nonempty work-run histograms feasible in H binary symbols.

    Sorted lengths lambda satisfy sum(lambda)+len(lambda)-1 <= H.
    They biject to partitions into parts >=2 with sum <= H+1, via lambda+1.
    Count = p(H+1)-1. Empty all-restart word is separate.
    """
    horizon_ok(h)
    def visit(prefix,total,min_length,last_count,mult):
        r=len(prefix)
        for ell in range(min_length,h-total-r+1):
            repeat=last_count+1 if prefix and ell==prefix[-1] else 1
            m=mult*(r+1)//repeat
            new=prefix+(ell,)
            yield new,m
            yield from visit(new,total+ell,ell,repeat,m)
    yield from visit((),0,1,0,1)


def compositions_count(total,parts):
    if parts==0:return int(total==0)
    return math.comb(total-1,parts-1) if total>=parts else 0


def base_weight_exact(model,h,n,r):
    """Probability per work-length permutation, summing reset run compositions."""
    m=h-n;R=model.environment;nu=model.initial_environment;out=F(0)
    if r<1 or n<r or m<0:return out
    for start,end,k,wr,rw in ((0,0,r-1,r-1,r-1),(0,1,r,r,r-1),
                              (1,0,r,r-1,r),(1,1,r+1,r,r)):
        ways=compositions_count(m,k)
        if ways:
            out+=nu[start]*ways*R[0][0]**(n-r)*R[1][1]**(m-k)*R[0][1]**wr*R[1][0]**rw
    return out


def _logpow(x,n):
    if n==0:return 0.
    return n*math.log(x) if x>0 else -math.inf

def _logsum(values):
    values=[x for x in values if x!=-math.inf]
    if not values:return -math.inf
    top=max(values);return top+math.log(math.fsum(math.exp(x-top) for x in values))


def base_logweights(model,h):
    R=np.asarray(model.environment,float);nu=np.asarray(model.initial_environment,float)
    out=np.full((h+1,h//2+2),-np.inf)
    for n in range(1,h+1):
        m=h-n
        for r in range(1,min(n,m+1)+1):
            values=[]
            for start,end,k,wr,rw in ((0,0,r-1,r-1,r-1),(0,1,r,r,r-1),(1,0,r,r-1,r),(1,1,r+1,r,r)):
                count=compositions_count(m,k)
                if count and nu[start]>0:
                    values.append(math.log(nu[start])+math.log(count)+_logpow(R[0,0],n-r)
                                  +_logpow(R[1,1],m-k)+_logpow(R[0,1],wr)+_logpow(R[1,0],rw))
            out[n,r]=_logsum(values)
    return out


def local_survival_exact(c,h):
    transient=tuple(i for i in range(len(c.initial)) if i not in c.target)
    T=tuple(tuple(c.work[i][j] for j in transient) for i in transient)
    v=tuple(c.initial[i] for i in transient);out=[F(1)]
    for _ in range(h):
        v=vm(v,T);out.append(sum(v,F(0)))
    return tuple(out)


def local_survival_float(c,h):
    transient=tuple(i for i in range(len(c.initial)) if i not in c.target)
    T=np.asarray(c.work,float)[np.ix_(transient,transient)]
    v=np.asarray(c.initial,float)[list(transient)];out=np.ones(h+1)
    for t in range(1,h+1):
        v=v@T;out[t]=min(1.,max(0.,float(v.sum())))
    return out


def exact_histogram_value(model,h,return_mass=False):
    validate(model);horizon_ok(h)
    if h==0:return (F(0),F(1)) if return_mass else F(0)
    f=[local_survival_exact(c,h) for c in model.components];value=F(0)
    mass=model.initial_environment[1]*model.environment[1][1]**(h-1)
    for lengths,multiplicity in run_partitions(h):
        weight=multiplicity*base_weight_exact(model,h,sum(lengths),len(lengths));mass+=weight
        if weight:
            response=math.prod(1-math.prod(fs[l] for l in lengths) for fs in f)
            value+=weight*response
    if mass!=1:raise AssertionError('histogram weights fail to sum to one')
    return (value,mass) if return_mass else value

@dataclass(frozen=True)
class Compiled:
    model: Model
    certificate: dict

    def evaluate(self,h,*,details=False):
        horizon_ok(h)
        if h==0:return {'probability':0.,'log_probability':-math.inf,'histogram_classes':1,'nonempty_classes':0,'path_mass':1.}
        if h>120:raise ContractError('H>120 requires a different backend; partition growth is explicit')
        count=partition_number(h+1)
        if count>2_000_000:raise ContractError(f'{count} run histograms exceed this implementation limit; use renewal/inclusion-exclusion or fallback')
        f=np.asarray([local_survival_float(c,h) for c in self.model.components])
        with np.errstate(divide='ignore'):logs=np.log(f)
        weights=base_logweights(self.model,h)
        result=-math.inf;totalmass=0.;classes=0;positive=0
        ncomp=len(self.model.components)
        trace=[]
        def dfs(lengths,total,minimum,last_count,mult,logsurv):
            nonlocal result,totalmass,classes,positive
            r=len(lengths)
            for ell in range(minimum,h-total-r+1):
                repeat=last_count+1 if lengths and ell==lengths[-1] else 1
                mult1=mult*(r+1)//repeat;n=total+ell;rr=r+1
                ls=logsurv+logs[:,ell]
                lw=weights[n,rr]+math.log(mult1)
                classes+=1
                if math.isfinite(lw):
                    totalmass+=math.exp(lw)
                    completed=-np.expm1(ls)
                    if np.all(completed>0):
                        lv=lw+float(np.log(completed).sum())
                        result=float(np.logaddexp(result,lv));positive+=1
                        if details:trace.append({'lengths':lengths+(ell,),'weight':math.exp(lw),'log_response':lv-lw})
                dfs(lengths+(ell,),n,ell,repeat,mult1,ls)
        dfs((),0,1,0,1,np.zeros(ncomp))
        totalmass+=float(self.model.initial_environment[1])*float(self.model.environment[1][1])**(h-1)
        if classes!=count-1:raise AssertionError('partition enumeration count disagreement')
        if abs(totalmass-1)>5e-10:raise ArithmeticError('float histogram mass check failed')
        out={'probability':math.exp(result) if result>-745 else 0.,'log_probability':result,
             'histogram_classes':count,'nonempty_classes':classes,'positive_contributions':positive,'path_mass':totalmass}
        if details:out['contributions']=trace
        return out

def compile_model(model):return Compiled(model,validate(model))


def work_runs(word):
    lengths=[];run=0
    for z in word:
        if z==0:run+=1
        else:
            if run:lengths.append(run);run=0
    if run:lengths.append(run)
    return tuple(lengths)


def word_probability(model,word):
    if not word:return F(1)
    p=model.initial_environment[word[0]]
    for a,b in zip(word,word[1:]):p*=model.environment[a][b]
    return p


def word_response(model,word):
    """Independent direct local matrix evolution; no regenerative identity."""
    result=F(1)
    for c in model.components:
        v=c.initial
        for z in word:v=vm(v,c.kernels[z])
        result*=sum((v[i] for i in c.target),F(0))
    return result


def path_oracle(model,h,return_groups=False):
    horizon_ok(h)
    if h>18:raise ContractError('small history oracle only')
    total=F(0);groups={}
    for word in product((0,1),repeat=h):
        p=word_probability(model,word)
        if not p:continue
        response=word_response(model,word);total+=p*response
        if return_groups:
            key=tuple(sorted(work_runs(word)));entry=groups.setdefault(key,{'weight':F(0),'response':response,'words':[]})
            if entry['response']!=response:raise AssertionError('histogram is not sufficient')
            entry['weight']+=p;entry['words'].append((word,p))
    return (total,groups) if return_groups else total


def joint_oracle(model,h):
    horizon_ok(h)
    states=list(product(*(range(len(c.initial)) for c in model.components)))
    if len(states)>100:raise ContractError('small microstate oracle only')
    law={(z,x):pz*math.prod(c.initial[j] for c,j in zip(model.components,x)) for z,pz in enumerate(model.initial_environment) for x in states}
    for _ in range(h):
        nxt={}
        for (z,x),p in law.items():
            if not p:continue
            for y in states:
                pw=math.prod(c.kernels[z][a][b] for c,a,b in zip(model.components,x,y))
                if not pw:continue
                for zz,pz in enumerate(model.environment[z]):
                    if pz:nxt[(zz,y)]=nxt.get((zz,y),F(0))+p*pw*pz
        law=nxt
    return sum((p for (z,x),p in law.items() if all(j in c.target for j,c in zip(x,model.components))),F(0))


def tensor_baseline(model,h):
    """Global matrix-free tensor DP, NOT Tessa; generic for these two kernels."""
    horizon_ok(h);dims=tuple(len(c.initial) for c in model.components)
    if math.prod(dims)>2_000_000:raise ContractError('explicit tensor safety cap')
    base=np.array(1.)
    for c in model.components:base=np.multiply.outer(base,np.asarray(c.initial,float))
    law=np.stack([float(x)*base for x in model.initial_environment]);R=np.asarray(model.environment,float)
    for _ in range(h):
        new=np.zeros_like(law)
        for z in (0,1):
            v=law[z]
            for axis,c in enumerate(model.components):
                v=np.moveaxis(np.tensordot(v,np.asarray(c.kernels[z],float),axes=([axis],[0])),-1,axis)
            for zz in (0,1):new[zz]+=v*R[z,zz]
        law=new
    v=law.sum(axis=0)
    for axis in reversed(range(len(dims))):v=np.take(v,model.components[axis].target,axis=axis).sum(axis=axis)
    return float(v)


def renewal_subset_baseline(model,h,exact=False):
    """Informed independent algorithm: subset inclusion-exclusion + renewal DP.
    O(2^N H^2) arithmetic, O(NH+H) workspace apart from subset enumeration.
    Float cancellation is reported rather than clipped silently.
    """
    horizon_ok(h);n=len(model.components)
    if n>16:raise ContractError('subset oracle limit N<=16')
    if h==0:return F(0) if exact else {'probability':0.,'condition_estimate':1.}
    f=[local_survival_exact(c,h) if exact else local_survival_float(c,h) for c in model.components]
    R=model.environment if exact else np.asarray(model.environment,float)
    nu=model.initial_environment if exact else np.asarray(model.initial_environment,float)
    zero=F(0) if exact else 0.;one=F(1) if exact else 1.;terms=[]
    for mask in range(1<<n):
        q=[one]*(h+1)
        for i in range(n):
            if mask>>i&1:q=[a*b for a,b in zip(q,f[i])]
        C=[zero]+[q[l]*R[0][0]**(l-1) for l in range(1,h+1)]
        W=[zero]*(h+1);B=[zero]*(h+1)
        for t in range(1,h+1):
            W[t]=nu[0]*C[t]+R[1][0]*sum((B[t-l]*C[l] for l in range(1,t)),zero)
            B[t]=(nu[1] if t==1 else R[1][1]*B[t-1]+R[0][1]*W[t-1])
        terms.append((-1 if mask.bit_count()%2 else 1)*(W[h]+B[h]))
    if exact:return sum(terms,F(0))
    ans=math.fsum(terms);cond=math.fsum(abs(v) for v in terms)/abs(ans) if ans else math.inf
    return {'probability':ans,'condition_estimate':cond,'numeric_warning':bool(cond*np.finfo(float).eps>1e-7)}


def noncommutation_witness(c):
    """BFS invariant goal-space certificate, used only to show v20 rejects."""
    n=len(c.initial);goal=tuple(F(i in c.target) for i in range(n));basis=[];pivots={};queue=[]
    def add(v,word):
        x=list(v)
        for p,row in sorted(pivots.items()):
            coeff=x[p];x=[a-coeff*b for a,b in zip(x,row)]
        pos=next((i for i,a in enumerate(x) if a),None)
        if pos is None:return
        scale=x[pos];pivots[pos]=tuple(a/scale for a in x);basis.append((v,word));queue.append((v,word))
    add(goal,());head=0
    while head<len(queue):
        v,word=queue[head];head+=1
        for z,q in enumerate(c.kernels):add(mv(q,v),(z,)+word)
    for v,word in basis:
        a=mv(c.work,mv(c.restart,v));b=mv(c.restart,mv(c.work,v))
        if a!=b:
            s=next(i for i in range(n) if a[i]!=b[i])
            return {'state':s,'left_word':(0,1)+word,'right_word':(1,0)+word,'left':str(a[s]),'right':str(b[s]),'continuation_rank':len(basis)}
    return None


def meeting_restart(n,environment=None,initial_environment=(F(1),F(0))):
    if type(n)is not int or n<1:raise ContractError('positive component count')
    components=[]
    for i in range(n):
        # First 12 immutable published pairs; further heterogeneous pairs are synthetic, distinct and explicitly labeled.
        j=i
        if i<12:p=F(5+2*j,100);q=F(54+2*j,100)
        else:p=F(5,100)+F(25*(i-11),100*(n+1));q=F(54,100)+F(30*(i-11),100*(n+1))
        P=mat([[1-p,p,0],[1-q,0,q],[0,0,1]])
        reset=mat([[1,0,0],[1,0,0],[0,0,1]])
        components.append(Local(P,reset,vector([1,0,0]),(2,)))
    R=mat([[F(9,10),F(1,10)],[F(1,5),F(4,5)]]) if environment is None else mat(environment)
    return Model(tuple(components),R,vector(initial_environment))


def render_prism(model):
    validate(model)
    if model.initial_environment!=(F(1),F(0)) or any(c.initial!=(F(1),F(0),F(0)) or c.target!=(2,) for c in model.components):raise ContractError('renderer supports fixed Meeting initial/goal')
    term=lambda x:f'({x.numerator}/{x.denominator})'
    out=['dtmc','module environment',' e : [0..1] init 0;']
    for z,row in enumerate(model.environment):out.append(f' [step] e={z} -> '+' + '.join(f"{term(v)} : (e'={j})" for j,v in enumerate(row) if v)+';')
    out.append('endmodule')
    for i,c in enumerate(model.components,1):
        out.extend([f'module P{i}',f' s{i} : [0..2] init 0;'])
        for z,q in enumerate(c.kernels):
            for s,row in enumerate(q):out.append(f' [step] e={z} & s{i}={s} -> '+' + '.join(f"{term(v)} : (s{i}'={j})" for j,v in enumerate(row) if v)+';')
        out.append('endmodule')
    out.append('label "goal" = '+' & '.join(f'(s{i}=2)' for i in range(1,len(model.components)+1))+';')
    return '\n'.join(out)+'\n'


def parse_prism(text):
    """Full-input conservative grammar. Derive ownership/exogeneity from code.
    No claim to parse arbitrary PRISM or trust unverified independence flags.
    """
    s=text.strip()
    if not s.startswith('dtmc'):raise ContractError('DTMC declaration required')
    s=s[4:];pattern=r'module\s+(\w+)\s+(.*?)\s+endmodule';blocks=list(re.finditer(pattern,s,re.S));res=re.sub(pattern,'',s,flags=re.S);mods=[]
    for block in blocks:
        name,body=block.groups();decl=re.match(r'\s*(\w+)\s*:\s*\[0\.\.(\d+)\]\s+init\s+0\s*;',body)
        if decl is None:raise ContractError('variable declaration')
        var,upper=decl.groups();size=int(upper)+1;commands=[]
        for cmd in body[decl.end():].split(';'):
            if not cmd.strip():continue
            p=re.fullmatch(r'\s*\[step\]\s*(.*?)\s*->\s*(.*?)\s*',cmd,re.S)
            if p is None:raise ContractError('synchronized command required')
            guard,branches=p.groups();row=[F(0)]*size
            for branch in branches.split('+'):
                t=re.fullmatch(r'\s*\(([0-9]+/[0-9]+)\)\s*:\s*\(\s*'+re.escape(var)+r"'\s*=\s*(\d+)\s*\)\s*",branch)
                if t is None:raise ContractError('nonlocal write, malformed probability or syntax')
                value,target=t.groups();j=int(target)
                if j>=size:raise ContractError('write outside variable range')
                row[j]+=F(value)
            commands.append((re.sub(r'\s+','',guard),tuple(row)))
        mods.append((name,var,size,commands))
    if not mods or mods[0][0:3]!=('environment','e',2):raise ContractError('environment declaration')
    if [g for g,r in mods[0][3]]!=['e=0','e=1']:raise ContractError('endogenous environment or ambiguous commands')
    components=[]
    for i,(name,var,size,cmds) in enumerate(mods[1:],1):
        if (name,var,size)!=(f'P{i}',f's{i}',3):raise ContractError('ownership or component schema')
        if [g for g,r in cmds]!=[f'e={z}&s{i}={a}' for z in (0,1) for a in range(3)]:raise ContractError('cross read, timing or guard outside contract')
        components.append(Local(tuple(r for g,r in cmds[:3]),tuple(r for g,r in cmds[3:]),vector([1,0,0]),(2,)))
    expected='label"goal"='+'&'.join(f'(s{i}=2)' for i in range(1,len(components)+1))+';'
    if re.sub(r'\s+','',res)!=expected:raise ContractError('unparsed input or noncartesian goal')
    model=Model(tuple(components),tuple(r for g,r in mods[0][3]));compiled=compile_model(model)
    compiled.certificate['source_sha256']=sha256(text.encode()).hexdigest()
    return compiled
