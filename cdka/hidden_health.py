"""CDKA v7: hidden corrector health, paid diagnosis, and costed conditional selector.

Exact finite-horizon decision instruments, NOT original general theorems.
Source kernel: cdka.composition.Contract/macro_row (v6). Both diagnosed
and undiagnosed paths have a shared delay during which hidden health
may drift; the initial state, deadline and failure event remain fixed.

The diagnosis stores a bit in physical readable memory, and its signal
cannot choose an action unless a selector architecture is purchased. Its
price is fixed independent of signal, so remaining resources cannot
secretly encode health. All costs are normalized integer tokens.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from typing import Mapping
from .composition import Contract, macro_row, DEAD, COST, solve


def _fraction(x, lower=F(0), upper=F(1)):
    y=F(x)
    if not lower<=y<=upper: raise ValueError(f'probability out of [{lower},{upper}]')
    return y


@dataclass(frozen=True)
class DiagnosticContract:
    physical: Contract=Contract()
    syndrome: int=0
    budget: int=4
    prior_degraded: F=F(1,2)
    sensor_error: F=F(0)
    health_drift: F=F(0)
    inspection_failure: F=F(0)
    inspection_cost: int=1
    selector_cost: int=1

    def __post_init__(self):
        if self.syndrome not in (0,1) or type(self.budget) is not int or not 0<=self.budget<=self.physical.capacity:
            raise ValueError('invalid syndrome or physical budget')
        for key,upper in [('prior_degraded',F(1)),('sensor_error',F(1,2)),
                          ('health_drift',F(1,2)),('inspection_failure',F(1))]:
            object.__setattr__(self,key,_fraction(getattr(self,key),upper=upper))
        for key in ['inspection_cost','selector_cost']:
            v=getattr(self,key)
            if type(v) is not int or v<0:raise ValueError('invalid cost')


def action_survival(p:Contract,k:int,h:int,b:int,action:str)->F:
    if action not in p.actions(b): raise ValueError('unavailable action')
    row=macro_row(p,(k,h,b),action)
    return F(1)-row[DEAD]


def hidden_joint(contract: DiagnosticContract)->dict[tuple[int,int],F]:
    """Joint probability P(H_final=h,Y=y) after diagnosis and same delay.
    Initial health prior P(H0=1)=p, initial diagnosis BSC eta,
    and health flips during the mandatory interval with probability nu.
    The latent health moves by the same law in the no-diagnosis arm.
    """
    p=contract.prior_degraded;eta=contract.sensor_error;nu=contract.health_drift
    out={(h,y):F(0) for h in (0,1) for y in (0,1)}
    for h0 in (0,1):
        prior=p if h0 else 1-p
        for y in (0,1):
            likelihood=1-eta if y==h0 else eta
            for h in (0,1):
                drift=1-nu if h==h0 else nu
                out[h,y]+=prior*likelihood*drift
    assert sum(out.values(),F(0))==1
    return out


def undiagnosed_value(c:DiagnosticContract)->dict:
    """One constant action; health is hidden to the physical controller."""
    joint=hidden_joint(c)
    prior={h:sum((joint[h,y] for y in (0,1)),F(0)) for h in (0,1)}
    b=c.budget;p=c.physical;k=c.syndrome
    scores={a:sum((prior[h]*action_survival(p,k,h,b,a) for h in (0,1)),F(0))
            for a in p.actions(b)}
    best=max(scores,key=scores.get)
    oracle=sum((prior[h]*max(action_survival(p,k,h,b,a) for a in p.actions(b))
                for h in (0,1)),F(0))
    return {'value':scores[best],'policy':best,'scores':scores,
            'health_prior_at_action':prior,'health_oracle':oracle}


def inspected_value(c:DiagnosticContract,conditional=True)->dict:
    """Exact exhaustive post-diagnosis decoder, including physical budget.

    Inspection and selector are paid BEFORE the operation; the runtime
    policy reads only the stored diagnosis Y, not hidden health H.
    If conditional=False, all Y must choose the same action.
    """
    cost=c.inspection_cost+(c.selector_cost if conditional else 0)
    if c.budget<cost:
        return {'feasible':False,'value':F(0),'decoder':{},'post_budget':None}
    remaining=c.budget-cost
    acts=c.physical.actions(remaining)
    joint=hidden_joint(c);scores={}
    for plan in product(acts,repeat=2):
        if not conditional and plan[0]!=plan[1]:continue
        success=sum((joint[h,y]*action_survival(c.physical,c.syndrome,h,remaining,plan[y])
                     for h in (0,1) for y in (0,1)),F(0))
        scores[plan]=(1-c.inspection_failure)*success
    best=max(scores,key=scores.get)
    return {'feasible':True,'value':scores[best],
            'decoder':dict(zip((0,1),best)), 'post_budget':remaining,
            'scores':scores}


def optimal_inspection(c:DiagnosticContract)->dict:
    base=undiagnosed_value(c)
    inspected=inspected_value(c)
    constant=inspected_value(c,conditional=False)
    use=(inspected['feasible'] and inspected['value']>base['value'])
    return {'base':base,'inspection':inspected,'diagnosis_without_selector':constant,
            'choice':'inspect' if use else 'skip',
            'value':max(base['value'],inspected['value']) if inspected['feasible'] else base['value'],
            'gain':max(F(0),inspected['value']-base['value']) if inspected['feasible'] else F(0)}


def binary_threshold(c:DiagnosticContract):
    """Special exact scalar formula: fair H prior and one-step actions.
    Assumes the default v6 physical one-step ordering: healthy prefers
    refresh, degraded prefers hold, and hold is best without diagnosis.
    Requires enough post-diagnosis resources to afford refresh.
    """
    if c.prior_degraded!=F(1,2):raise ValueError('fair prior required')
    p=c.physical;k=c.syndrome;b=c.budget
    if b<2:raise ValueError('must afford refresh in baseline')
    bh=action_survival(p,k,0,b,'hold');br=action_survival(p,k,0,b,'refresh')
    dh=action_survival(p,k,1,b,'hold');dr=action_survival(p,k,1,b,'refresh')
    g=br-bh;loss=dh-dr
    if not (g>0 and loss>=g):raise ValueError('two-action geometry not satisfied')
    base=(bh+dh)/2
    eta=c.sensor_error;nu=c.health_drift
    eta_eff=eta+nu-2*eta*nu
    threshold=g/(g+loss)
    # Potential benefit assuming the two relevant actions remain affordable.
    raw_gain=max(F(0),g-eta_eff*(g+loss))/2
    affordable=(b>=c.inspection_cost+c.selector_cost+2)
    if affordable:
        chosen_diagnosis_value=(1-c.inspection_failure)*(base+raw_gain)
        net_gain=max(F(0),chosen_diagnosis_value-base)
    else:
        net_gain=F(0)
    return {'g':g,'loss':loss,'critical_error':threshold,
            'effective_error':eta_eff,'base':base,
            'raw_information_value':raw_gain,'affordable':affordable,
            'actual_net_gain':net_gain}


def hidden_health_occupancy(p:Contract,k:int,b:int,steps:int,
                            prior_degraded=F(1,2)) ->dict:
    """Exact designer optimization for STAGE-DEPENDENT OBSERVATION-MEMORYLESS
    physical prescriptions (k,b)->a, with hidden h. No free belief at
    execution; an offline occupancy oracle designs a fixed time-indexed
    prescription. This is stricter than general history-based POMDPs.
    """
    if k not in (0,1) or b not in range(p.capacity+1) or type(steps)is not int or steps<0:
        raise ValueError('state or horizon')
    prior_degraded=_fraction(prior_degraded)
    states=p.states();index={s:i for i,s in enumerate(states)}
    initial=[F(0)]*len(states)
    initial[index[k,0,b]]=1-prior_degraded
    initial[index[k,1,b]]=prior_degraded
    @lru_cache(None)
    def recur(t,mass):
        if t==0:return sum(mass,F(0)),()
        present=sorted({(s[0],s[2]) for s,x in zip(states,mass) if x})
        best=F(-1);best_plan=()
        for commands in product(*(p.actions(b_) for _,b_ in present)):
            prescribed=dict(zip(present,commands))
            nxt=[F(0)]*len(states)
            for s,x in zip(states,mass):
                if not x:continue
                a=prescribed[s[0],s[2]]
                for new,y in macro_row(p,s,a).items():
                    if new!=DEAD:nxt[index[new]]+=x*y
            value,tail=recur(t-1,tuple(nxt))
            if value>best:
                best=value;best_plan=(prescribed,)+tail
        return best,best_plan
    value,plan=recur(steps,tuple(initial))
    full=solve(p,steps)['values'][-1]
    oracle=(1-prior_degraded)*full[k,0,b]+prior_degraded*full[k,1,b]
    return {'value':value,'plan':plan,'health_oracle':oracle,'gap':oracle-value,
            'design_nodes':recur.cache_info().currsize}
