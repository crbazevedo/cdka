"""CDKA v17: retained or renewed diagnosis under the unchanged v16 loop.

Every successful task uses the SAME paid operating/acquisition bundle. A
preinstalled two-row acquisition table chooses refresh/retain from the actual
service command, NOT hidden repair success. Retention is ideal (no bit decay).
Renewal is the old v16 sensor. Trusted guard/routing, common cell capacity and
installation prices are explicit fixed primitives, not a full autonomous agent.
All decisive calculations are exact Fractions; no survivor renormalization.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
from .recurrent_maintenance import (
    Model, Policy, BITS, add, policies, gate_execution, voter, report_probability,
    task_success, raw_task_success, select_probability, health_after_service,
    next_health, initial_micro, push, emission, micro_to_phase,
)

ACQUISITIONS={'retain':(False,False),'renew':(True,True),
              'after_service':(False,True),'after_skip':(True,False)}


@dataclass(frozen=True)
class Program:
    routing: Policy = Policy()
    acquisition: str = 'renew'

    def __post_init__(self):
        if self.acquisition not in ACQUISITIONS:
            raise ValueError('unknown acquisition program')

    def refresh(self,repair): return ACQUISITIONS[self.acquisition][repair]
    @property
    def name(self): return self.routing.name+'|'+self.acquisition


def programs():
    return tuple(Program(p,a) for p in policies() for a in ACQUISITIONS)


def macro(state):
    z,(a,b,c),balance=state
    return z,a,b+c,balance


def macrostates(p):
    return tuple(product((0,1),(0,1),range(3),range(1,p.capacity+1)))


def aggregate(law):
    result={}
    for s,mass in law.items():add(result,macro(s),mass)
    return result


@lru_cache(None)
def row(p,program,state):
    """Physical 64-state kernel; fresh & retained branches remain distinct."""
    z,bits,b=state
    if state not in p.microstates():raise ValueError('invalid live state')
    pr=select_probability(p,z,bits,program.routing.mode(b));out={}
    for repair,pd in ((0,1-pr),(1,pr)):
        if not pd:continue
        spent=1+2*repair
        if spent>b:raise AssertionError('resource overspend')
        b1=min(p.capacity,b-spent+2)
        proc=1-p.procedure_failure if repair else F(1)
        for h,ph in health_after_service(p,z,repair):
            live=pd*proc*ph*task_success(p,h)
            mem=((m,report_probability(m,h,p.diagnostic_error)) for m in BITS) if program.refresh(repair) else ((bits,F(1)),)
            for m,pm in mem:
                for z1,pz in next_health(p,h):add(out,(z1,m,b1),live*pm*pz)
    return out


@lru_cache(None)
def quotient_row(p,program,state):
    """Independent 48-state algebraic row: distinguish first port; count last2.

    Only the b<->c symmetry of the actual six-NAND voter is used. The health
    coordinate is evaluator-only. No arbitrary point collapse to 12 phases.
    """
    z,a,n,b=state
    if state not in macrostates(p):raise ValueError('invalid quotient state')
    representative=(a,int(n>=1),int(n==2))
    pr=select_probability(p,z,representative,program.routing.mode(b));out={}
    for repair,pd in ((0,1-pr),(1,pr)):
        if not pd:continue
        if 1+2*repair>b:raise AssertionError('resource overspend')
        balance=min(p.capacity,b+1-2*repair)
        proc=1-p.procedure_failure if repair else F(1)
        for h,ph in health_after_service(p,z,repair):
            common=pd*proc*ph*task_success(p,h)
            if program.refresh(repair):
                one=p.diagnostic_error if h==0 else 1-p.diagnostic_error
                distribution=tuple((aa,nn,(one if aa else 1-one)*comb(2,nn)*one**nn*(1-one)**(2-nn)) for aa in (0,1) for nn in range(3))
            else:distribution=((a,n,F(1)),)
            for aa,nn,pm in distribution:
                for z1,pz in next_health(p,h):add(out,(z1,aa,nn,balance),common*pm*pz)
    return out


@lru_cache(None)
def oracle_row(p,program,state):
    """Independent raw-event oracle: scalar gates and physical cell errors."""
    z,bits,b=state;mode=program.routing.mode(b);choose={}
    if mode in ('skip','service'):choose[int(mode=='service')]=F(1)
    else:
        for flags in product((0,1),repeat=6):
            decision=gate_execution(bits,flags)^(mode=='inverse')
            g=p.rate(z);weight=g**sum(flags)*(1-g)**(6-sum(flags))
            add(choose,int(decision),weight)
    out={}
    for repair,pd in choose.items():
        after=b-1-2*repair
        if after<0:raise AssertionError('overspend')
        for restored,ps in ((0,1-p.restoration),(1,p.restoration)) if repair else ((0,F(1)),):
            h=0 if restored else z
            common=pd*ps*raw_task_success(p,h)*(1-p.procedure_failure if repair else 1)
            memory=[]
            if program.refresh(repair):
                for flips in BITS:
                    w=p.diagnostic_error**sum(flips)*(1-p.diagnostic_error)**(3-sum(flips))
                    memory.append((tuple(h^bit for bit in flips),w))
            else:memory=[(bits,F(1))]
            for m,pm in memory:
                if h==0:
                    add(out,(0,m,min(4,after+2)),common*pm*(1-p.degradation))
                    add(out,(1,m,min(4,after+2)),common*pm*p.degradation)
                else:add(out,(1,m,min(4,after+2)),common*pm)
    return out


def forward(p,program,horizon,prior=F(1,2),micro=False):
    if type(horizon)is not int or horizon<0:raise ValueError('finite nonnegative horizon')
    law=initial_micro(p,prior);law=law if micro else aggregate(law)
    transition=row if micro else quotient_row
    curve=[F(1)]
    for _ in range(horizon):
        law=push(law,lambda s:transition(p,program,s))
        curve.append(sum(law.values(),F(0)))
    return tuple(curve),law


def ranking(p,horizon):
    rows=[]
    for pr in programs():
        v={s:F(1) for s in macrostates(p)}
        for _ in range(horizon):
            v={s:sum((q*v[t] for t,q in quotient_row(p,pr,s).items()),F(0)) for s in v}
        values=[]
        for prior in (F(0),F(1)):
            law=aggregate(initial_micro(p,prior))
            values.append(sum((mass*v[s] for s,mass in law.items()),F(0)))
        rows.append({'program':pr,'value':sum(values)/2,'healthy':values[0],'degraded':values[1]})
    return sorted(rows,key=lambda r:(r['value'],r['program'].name),reverse=True)


def summary(p,program,horizon):
    law=initial_micro(p);curve=[F(1)];services=F(0);renewals=F(0)
    for _ in range(horizon):
        for (z,m,b),weight in law.items():
            pr=select_probability(p,z,m,program.routing.mode(b));services+=weight*pr
            for repair,pd in ((0,1-pr),(1,pr)):
                if not program.refresh(repair):continue
                proc=1-p.procedure_failure if repair else F(1)
                success=sum((ph*task_success(p,h) for h,ph in health_after_service(p,z,repair)),F(0))
                renewals+=weight*pd*proc*success
        law=push(law,lambda s:row(p,program,s));curve.append(sum(law.values(),F(0)))
    return {'value':curve[-1],'curve':tuple(curve),'services':services,
            'renewals_after_success':renewals,'live_healthy_mass':sum((w for (z,m,b),w in law.items() if z==0),F(0)),
            'terminal_law':law}


def stale_projection_row(p,policy,phase):
    """Deliberately invalid reference: retain register but pretend E re-emits it.
    It is the old fresh-memory row; not used as a valid reduction of retention.
    """
    start=emission(p,phase)
    actual=push(start,lambda s:row(p,Program(policy,'retain'),s))
    projected=push(push(start,lambda s:micro_to_phase(p,policy,s)),lambda s:emission(p,s))
    return actual,projected


def symmetry_defect(p=None):
    """No mixture of exchangeable original diagnostic laws can match this law."""
    p=Model() if p is None else p
    law=emission(p,(0,0,3))
    retained=push(law,lambda s:row(p,Program(Policy(),'retain'),s))
    refreshed=push(law,lambda s:row(p,Program(Policy(),'renew'),s))
    x=(0,(0,1,1),4);y=(0,(1,0,1),4)
    g=p.healthy_error
    expected=-p.diagnostic_error**2*(1-p.diagnostic_error)*task_success(p,0)*(1-p.degradation)*2*g*(1-g)*(1-2*g)**2
    gap=retained.get(x,F(0))-retained.get(y,F(0))
    assert gap==expected
    return {'source':(0,0,3),'left':x,'right':y,'retained_left':retained.get(x,F(0)),
            'retained_right':retained.get(y,F(0)),'retained_difference':gap,
            'formula':expected,'fresh_difference':refreshed.get(x,F(0))-refreshed.get(y,F(0))}


def difference_trace(p,left,right,horizon):
    """Exact expected telescoping contrast; not individual counterfactual rescue.
    mu L^n1-mu R^n1 = sum_t mu R^t (L-R) L^(n-1-t)1.
    """
    states=macrostates(p);future=[{s:F(1) for s in states}]
    for _ in range(horizon):
        future.append({s:sum((w*future[-1][t] for t,w in quotient_row(p,left,s).items()),F(0)) for s in states})
    law=aggregate(initial_micro(p));parts=[]
    for t in range(horizon):
        continuation=future[horizon-1-t];part=F(0)
        for s,mass in law.items():
            a=quotient_row(p,left,s);b=quotient_row(p,right,s)
            part+=mass*sum(((a.get(v,F(0))-b.get(v,F(0)))*continuation[v] for v in a.keys()|b.keys()),F(0))
        parts.append(part);law=push(law,lambda s:quotient_row(p,right,s))
    return tuple(parts)
