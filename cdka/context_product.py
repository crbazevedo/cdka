"""Certified shared-context reachability without enumerating context words.

Two context modes evolve by an exogenous Markov chain. Component transitions
are conditionally independent given the ENTIRE context path, not merely its
current mode. Exact rational checks certify that order can be discarded on the
local terminal-observable closure. Dynamics and path weights remain distinct.

Numerical queries use float64; exact structural certificates are not floating-
point error enclosures. Exact small oracles use Fraction. No general PRISM parser
or optimal-policy claim is made.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import prod
import hashlib, json, re
import numpy as np


class ContractViolation(ValueError):
    pass


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def mv(A, x):
    return tuple(sum((a*b for a, b in zip(row,x)), F(0)) for row in A)


def vm(x, A):
    return tuple(sum((x[i]*A[i][j] for i in range(len(x))), F(0)) for j in range(len(x)))


def mm(A,B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(len(B))),F(0))
                       for j in range(len(B))) for i in range(len(A)))


def probability_vector(v, n, label):
    if len(v)!=n or any(x<0 for x in v) or sum(v,F(0))!=1:
        raise ContractViolation('invalid '+label)


def stochastic(A, n, label):
    if len(A)!=n or any(len(row)!=n for row in A):
        raise ContractViolation('non-square '+label)
    for row in A: probability_vector(row,n,label+' row')


@dataclass(frozen=True)
class Component:
    name: str
    kernels: tuple
    initial: tuple
    target: tuple

    @staticmethod
    def make(name,P0,P1,initial,target):
        return Component(str(name),(mat(P0),mat(P1)),tuple(map(F,initial)),tuple(target))


@dataclass(frozen=True)
class ContextIR:
    components: tuple[Component,...]
    environment: tuple=((F(9,10),F(1,10)),(F(1,5),F(4,5)))
    context_initial: tuple=(F(1),F(0))
    scheduler: str='current-context-then-environment'
    initial_product: bool=True
    conditional_noise_independent: bool=True
    exogenous_environment: bool=True
    cartesian_goal: bool=True


def observable_closure(kernels, goal):
    """Exact independent-vector worklist with shortest generator witnesses.

    Keeps actual generated vectors, with echelon residuals only for rank tests.
    At most 1+2*d candidate vector evaluations. Coefficient bit complexity is
    separate. This space belongs to the evaluator, not to a physical agent.
    """
    pivots={};basis=[];words=[];queue=[];attempts=0
    def add(value,word):
        nonlocal attempts
        attempts+=1;v=list(value)
        for p,row in sorted(pivots.items()):
            if v[p]:
                c=v[p];v=[a-c*b for a,b in zip(v,row)]
        p=next((i for i,a in enumerate(v) if a),None)
        if p is None:return
        c=v[p];pivots[p]=tuple(a/c for a in v)
        basis.append(tuple(value));words.append(word);queue.append((tuple(value),word))
    add(goal,())
    head=0
    while head<len(queue):
        v,w=queue[head];head+=1
        for z,P in enumerate(kernels):add(mv(P,v),(z,)+w)
    return tuple(basis),tuple(words),attempts


def horizon_check(H):
    if type(H)is not int or H<0:raise ValueError('horizon must be a nonnegative integer')


def occupation_weights(R,alpha,H,exact=False):
    """P(number of context1 uses=k) for z0,...,z(H-1).

    Dynamic path weights depend on order; current context is retained inside
    this DP. Only the local RESPONSE, not the Markov probability, forgets order.
    """
    horizon_check(H)
    if H==0:return (F(1),) if exact else np.ones(1)
    if exact:
        law={(0,0):F(alpha[0]),(1,1):F(alpha[1])}
        for _ in range(1,H):
            nxt={}
            for (z,k),p in law.items():
                if p:
                    for zz in (0,1):
                        key=(zz,k+zz);nxt[key]=nxt.get(key,F(0))+p*F(R[z][zz])
            law=nxt
        return tuple(sum((law.get((z,k),F(0)) for z in (0,1)),F(0)) for k in range(H+1))
    R=np.asarray(R,float);alpha=np.asarray(alpha,float)
    w=np.zeros((2,H+1));w[0,0]=alpha[0];w[1,1]=alpha[1]
    for t in range(1,H):
        v=np.zeros_like(w)
        v[0,:t+1]=w[0,:t+1]*R[0,0]+w[1,:t+1]*R[1,0]
        v[1,1:t+2]=w[0,:t+1]*R[0,1]+w[1,:t+1]*R[1,1]
        w=v
    return w.sum(axis=0)


@dataclass
class CompiledContext:
    ir: ContextIR
    certificate: dict
    groups: tuple

    def evaluate(self,H):
        horizon_check(H)
        weights=occupation_weights(self.ir.environment,self.ir.context_initial,H)
        response=np.ones(H+1)
        for P,mu,g in self.groups:
            L=np.empty((H+1,)+mu.shape);U=np.empty_like(L)
            L[0]=mu;U[0]=g
            for t in range(H):
                L[t+1]=np.einsum('ni,nij->nj',L[t],P[:,0],optimize=False)
                U[t+1]=np.einsum('nij,nj->ni',P[:,1],U[t],optimize=False)
            local=np.einsum('tni,tni->tn',L[::-1],U,optimize=False)
            if np.min(local)<-1e-12 or np.max(local)>1+1e-10:
                raise ArithmeticError('floating result violates probability range')
            response*=np.prod(np.clip(local,0,1),axis=1)
        value=float(weights@response)
        return {'probability':value,'occupation_weights':weights,'conditional_response':response,
                'arithmetic':'float64, structurally exact reduction; no interval rounding certificate'}

    def exact(self,H):
        horizon_check(H)
        if H>150:raise ValueError('exact research oracle limited to H<=150')
        weights=occupation_weights(self.ir.environment,self.ir.context_initial,H,True)
        response=[F(1)]*(H+1)
        for c in self.ir.components:
            goal=tuple(F(i in c.target) for i in range(len(c.initial)))
            L=[c.initial];U=[goal]
            for _ in range(H):
                L.append(vm(L[-1],c.kernels[0]));U.append(mv(c.kernels[1],U[-1]))
            for k in range(H+1):response[k]*=sum((a*b for a,b in zip(L[H-k],U[k])),F(0))
        return sum((a*b for a,b in zip(weights,response)),F(0))


def compile_context(ir,task_relative=True):
    if not isinstance(ir,ContextIR) or not ir.components:raise ContractViolation('nonempty ContextIR required')
    if ir.scheduler!='current-context-then-environment':raise ContractViolation('unsupported scheduler')
    if not(ir.initial_product and ir.conditional_noise_independent and ir.exogenous_environment and ir.cartesian_goal):
        raise ContractViolation('initial/conditional independence, exogenous environment and Cartesian goal required')
    R=mat(ir.environment);alpha=tuple(map(F,ir.context_initial))
    stochastic(R,2,'environment');probability_vector(alpha,2,'initial environment')
    if len({c.name for c in ir.components})!=len(ir.components):raise ContractViolation('duplicate ownership')
    records=[];groups={}
    for c in ir.components:
        n=len(c.initial)
        if n==0 or len(c.kernels)!=2:raise ContractViolation('two nonempty local modes required')
        for P in c.kernels:stochastic(P,n,'local kernel')
        probability_vector(c.initial,n,'initial local distribution')
        if not c.target or len(set(c.target))!=len(c.target) or any(type(j)is not int or not 0<=j<n for j in c.target):
            raise ContractViolation('invalid target')
        for P in c.kernels:
            if any(P[i][j] for i in c.target for j in range(n) if j not in c.target):
                raise ContractViolation('nonabsorbing target: endpoint is not bounded reachability')
        A,B=c.kernels;AB=mm(A,B);BA=mm(B,A)
        if AB==BA:kind='full-matrix commutation';dim=None;tests=n
        else:
            if not task_relative:raise ContractViolation('full matrices do not commute')
            goal=tuple(F(i in c.target) for i in range(n))
            basis,words,attempts=observable_closure(c.kernels,goal)
            for v,w in zip(basis,words):
                if mv(A,mv(B,v))!=mv(B,mv(A,v)):
                    raise ContractViolation(f'order affects goal after suffix {w}; occupation counts insufficient')
            kind='commutation on invariant goal space';dim=len(basis);tests=attempts
        records.append({'name':c.name,'states':n,'certificate':kind,'goal_space_dimension':dim,'checks':tests})
        groups.setdefault(n,[]).append(c)
    arrays=[]
    for n,cs in groups.items():
        arrays.append((np.array([c.kernels for c in cs],float),np.array([c.initial for c in cs],float),
                       np.array([[float(j in c.target) for j in range(n)] for c in cs],float)))
    serial={'components':[{'name':c.name,'kernels':c.kernels,'initial':c.initial,'target':c.target} for c in ir.components],
            'environment':R,'context_initial':alpha}
    sha=hashlib.sha256(json.dumps(serial,sort_keys=True,default=str,separators=(',',':')).encode()).hexdigest()
    cert={'ir_sha256':sha,'components':len(ir.components),'global_state_count':2*prod(len(c.initial) for c in ir.components),
          'local_records':records,'query_bound':'O(H^2 + H sum_i s_i^2) arithmetic after certification; binary context',
          'conditional_contract':'independent local sampling conditional on whole shared Markov context path',
          'proof':'sum_k w_H(k) product_i mu_i A_i^(H-k) B_i^k g_i',
          'scope':'explicit IR checks; parser separately verifies its grammar; rational structural checks, float64 query'}
    return CompiledContext(ContextIR(ir.components,R,alpha),cert,tuple(arrays))


def parse_prism(text):
    """Fail-closed parser of the exact generated contextual Meeting grammar.
    Unlike IR flags, local read/write ownership and context exogeneity are
    established syntactically here. Not a general PRISM/JANI frontend.
    """
    if not isinstance(text,str):raise TypeError('PRISM text required')
    m=re.match(r'\s*dtmc\b',text)
    if m is None:raise ContractViolation('expected DTMC')
    source=text[m.end():];pattern=r'module\s+(\w+)\s+(.*?)\s+endmodule'
    blocks=list(re.finditer(pattern,source,re.S));left=re.sub(pattern,'',source,flags=re.S)
    modules=[]
    for block in blocks:
        name,body=block.groups();decl=re.match(r'\s*(\w+)\s*:\s*\[0\.\.(\d+)\]\s+init\s+0\s*;',body)
        if decl is None:raise ContractViolation('state declaration')
        var,upper=decl.groups();size=int(upper)+1;commands=[]
        for cmd in body[decl.end():].split(';'):
            if not cmd.strip():continue
            p=re.fullmatch(r'\s*\[step\]\s*(.*?)\s*->\s*(.*?)\s*',cmd,re.S)
            if p is None:raise ContractViolation('one synchronized step label required')
            guard,terms=p.groups();row=[F(0)]*size
            for term in terms.split('+'):
                r=re.fullmatch(r'\s*\(([0-9]+/[0-9]+)\)\s*:\s*\(\s*'+re.escape(var)+r"'\s*=\s*(\d+)\s*\)\s*",term)
                if r is None:raise ContractViolation('local rational update required')
                prob,target=r.groups();j=int(target)
                if j>=size:raise ContractViolation('target outside local domain')
                row[j]+=F(prob)
            probability_vector(row,size,'command')
            commands.append((re.sub(r'\s+','',guard),tuple(row)))
        modules.append((name,var,size,commands))
    if len(modules)<2 or modules[0][:3]!=('environment','e',2):raise ContractViolation('one environment and participants required')
    if [g for g,_ in modules[0][3]]!=['e=0','e=1']:raise ContractViolation('environment reads must be exogenous')
    R=tuple(r for g,r in modules[0][3]);cs=[]
    for i,(name,var,size,cmds) in enumerate(modules[1:],1):
        if (name,var,size)!=(f'P{i}',f's{i}',3):raise ContractViolation('participant ownership/order')
        if [g for g,r in cmds]!=[f'e={z}&s{i}={x}' for z in (0,1) for x in range(3)]:raise ContractViolation('local guards / dynamic context required')
        cs.append(Component.make(name,[r for _,r in cmds[:3]],[r for _,r in cmds[3:]],(1,0,0),(2,)))
    expected='label"goal"='+'&'.join(f'(s{i}=2)' for i in range(1,len(cs)+1))+';'
    if re.sub(r'\s+','',left)!=expected:raise ContractViolation('goal or trailing commands outside grammar')
    return ContextIR(tuple(cs),R)


def render_prism(ir):
    if ir.context_initial!=(1,0) or any(c.initial!=(1,0,0) or c.target!=(2,) for c in ir.components):
        raise ValueError('render supports only the benchmark start/goal')
    fmt=lambda x:f'({x.numerator}/{x.denominator})'
    lines=['dtmc','module environment',' e : [0..1] init 0;']
    for z,row in enumerate(ir.environment):lines.append(f' [step] e={z} -> '+' + '.join(f"{fmt(p)} : (e'={j})" for j,p in enumerate(row) if p)+';')
    lines.append('endmodule')
    for i,c in enumerate(ir.components,1):
        lines.extend([f'module P{i}',f' s{i} : [0..2] init 0;'])
        for z,P in enumerate(c.kernels):
            for x,row in enumerate(P):lines.append(f' [step] e={z} & s{i}={x} -> '+' + '.join(f"{fmt(p)} : (s{i}'={j})" for j,p in enumerate(row) if p)+';')
        lines.append('endmodule')
    lines.append('label "goal" = '+' & '.join(f'(s{i}=2)' for i in range(1,len(ir.components)+1))+';')
    return '\n'.join(lines)+'\n'


def meeting(n):
    if type(n)is not int or n<1:raise ValueError('positive component count')
    q_values=[54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,95,96,97,98,99,93,91,89,87]
    cs=[]
    for k in range(n):
        p,q=F(5+2*(k%30),100),F(q_values[k%30],100)
        P=mat([[1-p,p,0],[1-q,0,q],[0,0,1]])
        A=tuple(tuple(F(3,4)*int(i==j)+F(1,4)*P[i][j] for j in range(3)) for i in range(3))
        cs.append(Component.make(f'P{k+1}',A,P,(1,0,0),(2,)))
    return ContextIR(tuple(cs))


def raw_global_exact(ir,H):
    """Independent explicit probability oracle; no occupation counts or commutation."""
    horizon_check(H)
    dims=[len(c.initial) for c in ir.components]
    if 2*prod(dims)>180:raise ValueError('raw rational oracle limited to 180 states')
    states=tuple(product((0,1),*(range(s) for s in dims)))
    law={s:F(ir.context_initial[s[0]])*prod(c.initial[x] for c,x in zip(ir.components,s[1:])) for s in states}
    for _ in range(H):
        nxt={s:F(0) for s in states}
        for s,p in law.items():
            if not p:continue
            z=s[0]
            for t in states:
                q=F(ir.environment[z][t[0]])*prod(c.kernels[z][i][j] for c,i,j in zip(ir.components,s[1:],t[1:]))
                if q:nxt[t]+=p*q
        law=nxt
    return sum((p for s,p in law.items() if all(x in c.target for c,x in zip(ir.components,s[1:]))),F(0))


def path_exact(ir,H):
    """Independent environment-path enumeration, never reorders operators."""
    horizon_check(H)
    if H>16:raise ValueError('enumeration restricted to H<=16')
    if H==0:return prod(sum((c.initial[j] for j in c.target),F(0)) for c in ir.components)
    result=F(0)
    for path in product((0,1),repeat=H):
        w=F(ir.context_initial[path[0]])
        for a,b in zip(path,path[1:]):w*=ir.environment[a][b]
        if not w:continue
        for c in ir.components:
            mu=c.initial
            for z in path:mu=vm(mu,c.kernels[z])
            w*=sum((mu[j] for j in c.target),F(0))
        result+=w
    return result


def global_tensor(ir,H):
    """Strong local baseline, not Tessa: full joint tensor, no global matrix."""
    horizon_check(H)
    dims=[len(c.initial) for c in ir.components]
    if 2*prod(dims)>2_000_000:raise MemoryError('controlled tensor bound')
    joint=np.array(ir.context_initial,float)
    for c in ir.components:joint=np.multiply.outer(joint,np.array(c.initial,float))
    P=[np.array(c.kernels,float) for c in ir.components];R=np.asarray(ir.environment,float)
    for _ in range(H):
        new=np.zeros_like(joint)
        for z in (0,1):
            x=joint[z]
            for i,modes in enumerate(P):x=np.moveaxis(np.tensordot(x,modes[z],axes=([i],[0])),-1,i)
            new[0]+=R[z,0]*x;new[1]+=R[z,1]*x
        joint=new
    for i in reversed(range(len(dims))):joint=np.take(joint,ir.components[i].target,axis=i+1).sum(axis=i+1)
    return float(joint.sum())
