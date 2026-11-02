"""CDKA v11: exact trace microscope over the unchanged v6/v9/v10 plant.

Traces belong to the mathematical controller, not an LLM reasoning process.
Runtime reads (received diagnostic word, k, balance, stage), never hidden H/Y.
Stop labels are first failed predicates of an explicit execution ordering,
not claims of unique causal responsibility. Marginal transition laws alone
are insufficient to identify pathwise cross-policy counterfactuals.
"""
from collections import defaultdict
from dataclasses import dataclass, asdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib
import json

from .composition import (Contract, COST, DEAD, macro_row, micro_row,
                          health_row, mask_law, quotient)
from .continuation_interfaces import plans, equal_signal_joint, survival
from .joint_compilation import channel_row, evaluate_witness


@dataclass(frozen=True)
class Step:
    """Trace projection sufficient to replay a two-epoch controller."""
    before: tuple
    action: str
    after: object
    stop: str
    probability: F


@lru_cache(None)
def physical_events(p, state, action):
    """Raw event oracle on a canonical representative of the symmetric plant.

    Fixed order: world drift -> cell upset -> optional sensing/correction/
    writing -> majority gate -> execution -> health update. Failed mass
    stops at the first failed predicate, with later variables integrated out.
    """
    if state not in p.states() or action not in p.actions(state[2]):
        raise ValueError('invalid physical state or unaffordable action')
    k,h,b=state
    memory=(0,0,0) if k==0 else (1,0,0)
    rows=[]
    for fw,pw in ((0,1-p.world_flip),(1,p.world_flip)):
        for upset,pu in mask_law((p.cell_flip,)*3):
            damaged=tuple(m^e for m,e in zip(memory,upset))
            if action in ('hold','service'):
                writes=[(damaged,F(1),None,None,None)]
            else:
                majority=int(sum(damaged)>=2)
                guesses=((majority,F(1)),) if action=='correct' else (
                    (fw,1-p.sensor_error[h]),(1-fw,p.sensor_error[h]))
                writes=[]
                for guess,pg in guesses:
                    for fault,pc in ((0,1-p.correction_error[h]),(1,p.correction_error[h])):
                        for mask,pm in mask_law((p.write_flip,)*3):
                            writes.append((tuple((guess^fault)^x for x in mask),
                                           pg*pc*pm,guess,fault,mask))
            for out,po,guess,fault,mask in writes:
                base=pw*pu*po
                if not base: continue
                event={'world_flip':fw,'cell_mask':upset,'sensor_guess':guess,
                       'correction_fault':fault,'write_mask':mask,
                       'cells_after':out,'health_before':h}
                if int(sum(out)>=2)!=fw:
                    rows.append((base,DEAD,'majority_mismatch',event))
                    continue
                pf=p.actuator_failure[h]
                if pf:
                    rows.append((base*pf,DEAD,'executor_failure',event))
                for hn,ph in health_row(p,h,action).items():
                    q=base*(1-pf)*ph
                    if q:
                        after=(sum(x!=fw for x in out),hn,min(p.capacity,b-COST[action]+p.harvest))
                        rows.append((q,after,'live',dict(event,health_after=hn)))
    if sum((x[0] for x in rows),F(0))!=1:
        raise AssertionError('raw event mass not preserved')
    return tuple(rows)


@lru_cache(None)
def step_branches(p, state, action):
    grouped=defaultdict(F)
    for mass,after,stop,_ in physical_events(p,state,action):
        grouped[(after,stop)]+=mass
    branches=tuple(Step(state,action,after,stop,mass)
                   for (after,stop),mass in grouped.items())
    row=defaultdict(F)
    for x in branches: row[x.after]+=x.probability
    if dict(row)!=macro_row(p,state,action):
        raise AssertionError('trace projection differs from canonical plant')
    return branches


def trace_program(encoding, decoder, error=F(0), tail=F(1,100), balance=4,p=None):
    """Complete exact prefix tree; failed branches are never completed/reweighted."""
    p=Contract() if p is None else p
    enc=tuple(encoding);dec=tuple(decoder);lib=plans(p,b=balance)
    if len(enc)!=3 or any(x not in range(4) for x in enc) or len(dec)!=4:
        raise ValueError('three diagnostic signals encoded into two physical bits')
    if any(type(i)is not int or i not in range(len(lib)) for i in dec):
        raise ValueError('invalid continuation index')
    traces=[]
    for y,mu in enumerate(equal_signal_joint(tail)):
        for h in (0,1):
            for r,pr in enumerate(channel_row(enc[y],error)):
                q=mu[h]*pr
                if not q:continue
                plan=lib[dec[r]]
                for x in step_branches(p,(0,h,balance),plan.first):
                    base={'signal_evaluator_only':y,'health_initial_evaluator_only':h,
                          'sent_word':enc[y],'noise_mask':enc[y]^r,'readable_word':r,
                          'plan':dec[r]}
                    if x.after==DEAD:
                        traces.append(dict(base,steps=(x,),probability=q*x.probability,
                                           terminal=DEAD,outcome='failed',failed_epoch=1))
                        continue
                    s=x.after
                    a=plan.action_after((s[0],s[2]))
                    for z in step_branches(p,s,a):
                        traces.append(dict(base,steps=(x,z),probability=q*x.probability*z.probability,
                            terminal=z.after,outcome='alive' if z.after!=DEAD else 'failed',
                            failed_epoch=None if z.after!=DEAD else 2))
    if sum((t['probability'] for t in traces),F(0))!=1:
        raise AssertionError('complete trace tree loses mass')
    return tuple(traces)


def trace_summary(traces):
    bins=defaultdict(F);terminal=defaultdict(F);groups=defaultdict(F)
    for t in traces:
        q=t['probability'];terminal[t['terminal']]+=q
        key='alive' if t['outcome']=='alive' else f"epoch{t['failed_epoch']}_{t['steps'][-1].stop}"
        bins[key]+=q
        if t['outcome']=='alive':
            groups[(t['signal_evaluator_only'],t['health_initial_evaluator_only'])]+=q
    return {'value':bins['alive'],'event_bins':dict(bins),'terminal':dict(terminal),
            'alive_by_signal_health':dict(groups),'count':len(traces),'mass':sum(bins.values(),F(0))}


def terminal_law(plan_id,prior=F(1,2),p=None):
    """No diagnostic in this experiment. Internal health remains hidden."""
    p=Contract() if p is None else p;plan=plans(p)[plan_id]
    mu={(0,h,4):(F(prior) if h==0 else 1-F(prior)) for h in (0,1)}
    fail=F(0)
    for epoch in range(2):
        nxt=defaultdict(F)
        for s,q in mu.items():
            a=plan.first if epoch==0 else plan.action_after((s[0],s[2]))
            for z,m in macro_row(p,s,a).items():
                if z==DEAD:fail+=q*m
                else:nxt[z]+=q*m
        mu=dict(nxt)
    mu[DEAD]=fail
    return mu


def extend_readably(mu,p=None):
    """One more stage: one shared action per actual readable (k,b)."""
    p=Contract() if p is None else p;groups=defaultdict(lambda:[F(0),F(0)])
    for s,m in mu.items():
        if s!=DEAD:groups[(s[0],s[2])][s[1]]+=m
    value=F(0);policy={}
    for (k,b),mass in groups.items():
        scores={a:sum((mass[h]*survival(p,(k,h,b),a) for h in (0,1)),F(0)) for a in p.actions(b)}
        a=max(scores,key=scores.get);value+=scores[a];policy[(k,b)]=a
    return value,policy


def endpoint_alias_witness(prior=F(1,2)):
    """Equal two-stage alphas can hide unequal future-capability laws."""
    p=Contract();lib=plans(p);a,b=48,63
    if lib[a].alpha!=lib[b].alpha:raise AssertionError('alias fixture changed')
    laws=[terminal_law(i,prior) for i in (a,b)]
    rows=[]
    for i,mu in zip((a,b),laws):
        live=1-mu[DEAD];healthy=sum((m for s,m in mu.items() if s!=DEAD and s[1]==0),F(0))
        v3,pi=extend_readably(mu,p)
        rows.append({'plan':i,'two_stage_survival':live,'healthy_live_mass':healthy,
                     'healthy_given_alive':healthy/live,'balances':sorted({s[2] for s in mu if s!=DEAD}),
                     'third_stage_survival':v3,'third_policy':pi,
                     'fixed_refresh_value':sum((m*survival(p,s,'refresh') for s,m in mu.items() if s!=DEAD),F(0))})
    delta=rows[1]['third_stage_survival']-rows[0]['third_stage_survival']
    payoff_gap=survival(p,(0,0,4),'refresh')-survival(p,(0,1,4),'refresh')
    mass_gap=rows[1]['healthy_live_mass']-rows[0]['healthy_live_mass']
    fixed_delta=rows[1]['fixed_refresh_value']-rows[0]['fixed_refresh_value']
    if fixed_delta!=mass_gap*payoff_gap:raise AssertionError('fixed-policy health mediator identity failed')
    return {'rows':rows,'third_gain':delta,'fixed_refresh_gain':fixed_delta,'health_mass_gain':mass_gap,'health_payoff_gap':payoff_gap,
            'equal_alpha':lib[a].alpha}


def harmful_route_witness(error=F(1,10)):
    """Exact fixed-witness identity; global optimality at p=.1 is inherited
    from v10, not asserted for these witnesses at every other p."""
    p=F(error)
    if not 0<=p<=F(1,2):raise ValueError('error in [0,1/2]')
    plant=Contract();lib=plans(plant);mu=equal_signal_joint()[1]
    enc_inj=(0,1,3);enc_merge=(0,0,3);dec=(58,58,58,42)
    conditional_gap=(lib[58].alpha[0]+lib[58].alpha[1]-lib[42].alpha[0]-lib[42].alpha[1])/2
    predicted=F(1,3)*p*(1-2*p)*conditional_gap
    exact=evaluate_witness(enc_merge,dec,p)-evaluate_witness(enc_inj,dec,p)
    split=tuple(mu[h]*p*(1-2*p)*(lib[58].alpha[h]-lib[42].alpha[h]) for h in (0,1))
    if exact!=predicted or sum(split,F(0))!=exact:raise AssertionError('route identity failed')
    return {'error':p,'injective_route':p*(1-p),'merged_route':p*p,
            'conditional_plan_margin':conditional_gap,'net_gain':exact,'signed_health_contributions':split,
            'injective_encoding':enc_inj,'merged_encoding':enc_merge,'decoder':dec}


def suffix_conflict():
    """Shortest v9 interface collision: discarded diagnostic matters later."""
    p=Contract();out=[]
    for y in (0,1):
        mu=equal_signal_joint()[y];mass=[F(0),F(0)]
        for h in (0,1):
            for s,q in macro_row(p,(0,h,4),'service').items():
                if s!=DEAD and s[0]==0:mass[s[1]]+=mu[h]*q
        scores={a:sum((mass[h]*survival(p,(0,h,3),a)for h in (0,1)),F(0))for a in p.actions(3)}
        best=max(scores,key=scores.get)
        out.append({'discarded_signal':y,'runtime_input':(0,0,3),'action_prefix':'service',
                    'live_mass':sum(mass,F(0)),'healthy_given_prefix':mass[0]/sum(mass,F(0)),
                    'reference_next':best,'merged_next':'refresh','deficit':max(scores.values())-scores['refresh']})
    return out


def semantic_distance(encoding,decoder,values,bits=2):
    """Leading continuation regret A*p**d for one independent bit-fault interval.
    Nonnegative task margins prevent cancellation. An already suboptimal
    zero-noise decoder has d=0; this is not an error-correction guarantee."""
    result=[]
    for y,x in enumerate(encoding):
        best=max(values[y]);margins=[best-values[y][decoder[r]]for r in range(2**bits)]
        bad=[r for r,m in enumerate(margins)if m>0]
        if not bad:result.append({'distance':None,'leading':F(0)});continue
        d=min((x^r).bit_count() for r in bad)
        lead=sum((margins[r]for r in bad if (x^r).bit_count()==d),F(0))
        result.append({'distance':d,'leading':lead})
    return result


def coupling_guard():
    """Identical 80%-success marginals, different individual rescue counts.
    A cross-world structural coupling is not identified by marginal kernels."""
    return {
        'shared_fault':{(1,1):F(4,5),(0,0):F(1,5)},
        'disjoint_faults':{(1,1):F(3,5),(1,0):F(1,5),(0,1):F(1,5)}
    }


def to_json(value):
    if isinstance(value,F):return {'exact':str(value),'value':float(value)}
    if isinstance(value,Step):return to_json(asdict(value))
    if isinstance(value,dict):return {str(k):to_json(v)for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [to_json(x)for x in value]
    return value


def write_trace_jsonl(traces,path):
    """Stable IDs bind exact projected traces, not sampled realizations."""
    import pathlib
    target=pathlib.Path(path);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('w',encoding='utf8')as stream:
        for t in traces:
            record=to_json(t)
            raw=json.dumps(record,sort_keys=True,separators=(',',':'))
            record['trace_id']=hashlib.sha256(raw.encode()).hexdigest()[:20]
            stream.write(json.dumps(record,sort_keys=True,ensure_ascii=False)+'\n')
