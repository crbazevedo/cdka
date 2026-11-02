"""CDKA v8: diagnosis through compulsory repair and a maintained selector.

Finite exact Bayes/FSC instruments, not a novel general agency theorem.
The diagnostic register is the ONLY runtime input to the installed terminal
truth table. H (corrector health) and S (selector health) are hidden. All
repair/protection/servicing choices are precommitted and their full costs
are reserved before seeing the signal. There is no free history or seed.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import log2
from .composition import Contract, macro_row, DEAD

ERASED = 2
SIGNALS = (0, 1, ERASED)
# 0 is HOLD, 1 is REFRESH. Both are feasible after worst-case reservation.

@lru_cache(None)
def terminal_table() -> tuple[tuple[F, F], tuple[F, F]]:
    """The original v6/v7 physical event, not a fitted surrogate payoff."""
    p = Contract()
    return tuple(tuple(1-macro_row(p, (0, h, 2), a)[DEAD]
                       for a in ('hold', 'refresh')) for h in (0, 1))


def _prob(x, upper=F(1)):
    x=F(x)
    if not 0 <= x <= upper: raise ValueError('invalid probability')
    return x


@dataclass(frozen=True)
class TransportContract:
    budget: int = 6
    ticks: int = 1
    prior_degraded: F = F(1, 2)
    sensor_error: F = F(1, 20)
    health_drift: F = F(0)
    memory_flip: F = F(0)
    erasure: F = F(3, 5)
    selector_bad: F = F(1, 2)
    selector_wear: F = F(0)
    selector_errors: tuple[F, F] = (F(0), F(3, 10))
    service_success: F = F(4, 5)
    diagnostic_failure: F = F(0)
    driver: str = 'flip'  # alternatively 'silent': faults force HOLD

    def __post_init__(self):
        if type(self.budget) is not int or self.budget < 0:
            raise ValueError('nonnegative integer budget')
        if type(self.ticks) is not int or self.ticks < 1:
            raise ValueError('positive integer compulsory repair count')
        for key in ('prior_degraded','erasure','selector_bad','selector_wear',
                    'service_success','diagnostic_failure'):
            object.__setattr__(self,key,_prob(getattr(self,key)))
        for key in ('sensor_error','health_drift','memory_flip'):
            object.__setattr__(self,key,_prob(getattr(self,key),F(1,2)))
        a,b=(_prob(x,F(1,2)) for x in self.selector_errors)
        if a>b: raise ValueError('healthy selector must be no worse')
        object.__setattr__(self,'selector_errors',(a,b))
        if self.driver not in ('flip','silent'): raise ValueError('unknown driver')


def reservation(c:TransportContract,protect=False,service=False)->int:
    # one token per compulsory repair in BOTH arms; diagnostic=1;
    # contingent selector=1; worst-case terminal refresh=2;
    # protection costs one extra per repair; selector service costs one.
    return c.ticks+4+(c.ticks if protect else 0)+(1 if service else 0)


def summaries(c:TransportContract,protect=False,service=False):
    eta,nu,omega=c.sensor_error,c.health_drift,c.memory_flip
    error=(1-(1-2*eta)*((1-2*nu)*(1-2*omega))**c.ticks)/2
    keep=F(1) if protect else (1-c.erasure)**c.ticks
    bad=1-(1-c.selector_bad)*(1-c.selector_wear)**c.ticks
    if service: bad*=1-c.service_success
    th=c.selector_errors[0]+bad*(c.selector_errors[1]-c.selector_errors[0])
    return {'error':error,'keep':keep,'theta':th,'bad_selector':bad,
            'cost':reservation(c,protect,service)}


def _add(out,k,p):
    if p: out[k]=out.get(k,F(0))+p


def terminal_joint(c:TransportContract,protect=False,service=False):
    """Independent forward micro-oracle for P(H_current,M,S,procedure alive).

    Faults and health transitions are independent conditional on parents.
    Flagged erasure remains erased. Protection prevents erasure only, not
    flipping or obsolescence. Late service repairs S probabilistically.
    """
    dist={}
    for h,y,s in product((0,1),repeat=3):
        ph=c.prior_degraded if h else 1-c.prior_degraded
        py=1-c.sensor_error if y==h else c.sensor_error
        ps=c.selector_bad if s else 1-c.selector_bad
        _add(dist,(h,y,s),ph*py*ps*(1-c.diagnostic_failure))
    rho=F(0) if protect else c.erasure
    for _ in range(c.ticks):
        nxt={}
        for (h,m,s),mass in dist.items():
            memory=((ERASED,F(1)),) if m==ERASED else (
                (ERASED,rho),(m,(1-rho)*(1-c.memory_flip)),
                (1-m,(1-rho)*c.memory_flip))
            selector=((1,F(1)),) if s else ((0,1-c.selector_wear),(1,c.selector_wear))
            for h2,ph in ((h,1-c.health_drift),(1-h,c.health_drift)):
                for m2,pm in memory:
                    for s2,ps in selector:
                        _add(nxt,(h2,m2,s2),mass*ph*pm*ps)
        dist=nxt
    if service:
        nxt={}
        for (h,m,s),mass in dist.items():
            outcomes=((0,F(1)),) if not s else ((0,c.service_success),(1,1-c.service_success))
            for s2,p in outcomes: _add(nxt,(h,m,s2),mass*p)
        dist=nxt
    assert sum(dist.values(),F(0))==1-c.diagnostic_failure
    return dist


def policy_value(joint,plan,errors,driver='flip',table=None):
    table=terminal_table() if table is None else table
    if len(plan)!=3 or any(a not in (0,1) for a in plan):
        raise ValueError('three-symbol binary truth table required')
    result=F(0)
    for (h,m,s),mass in joint.items():
        requested=plan[m];theta=errors[s]
        failed=1-requested if driver=='flip' else 0
        result+=mass*((1-theta)*table[h][requested]+theta*table[h][failed])
    return result


def optimize_terminal(joint,errors,driver='flip',table=None):
    """Enumerates all eight executable truth tables, no hidden inputs."""
    scores={p:policy_value(joint,p,errors,driver,table) for p in product((0,1),repeat=3)}
    best=max(scores,key=scores.get)
    return {'value':scores[best],'plan':best,'scores':scores}


def skip_value(c:TransportContract):
    if c.budget<c.ticks: return F(0)
    # Same mandatory drift/repair interval, but no diagnostic and no new
    # contingent output driver. A direct constant HOLD/REFRESH is the
    # original v7 physical bypass; its execution can still fail in v6.
    ph=(1-(1-2*c.prior_degraded)*(1-2*c.health_drift)**c.ticks)/2
    table=terminal_table()
    actions=(0,1) if c.budget>=c.ticks+2 else (0,)
    return max((1-ph)*table[0][a]+ph*table[1][a] for a in actions)


def margin_identity(joint,errors,table=None):
    """Exact weighted-decision formula, even if H and S are correlated.

    Only for a symmetric flip driver. Lifting must preserve the complete
    physically observed symbol and the set of implementable truth tables.
    """
    table=terminal_table() if table is None else table
    hold=F(0);offset=F(0);margins={m:F(0) for m in SIGNALS}
    for (h,m,s),mass in joint.items():
        delta=table[h][1]-table[h][0];theta=errors[s]
        hold+=mass*table[h][0]
        offset+=mass*theta*delta
        margins[m]+=mass*(1-2*theta)*delta
    return {'value':hold+offset+sum((max(F(0),d) for d in margins.values()),F(0)),
            'hold_mass_value':hold,'selector_offset':offset,'margins':margins}


def closed_value(c:TransportContract,protect=False,service=False):
    """Exact special-case formula: fair H, independent selector and noise."""
    if c.prior_degraded!=F(1,2): raise ValueError('fair health prior required')
    table=terminal_table();base=(table[0][0]+table[1][0])/2
    g=table[0][1]-table[0][0];loss=table[1][0]-table[1][1]
    if not loss>=g>0: raise ValueError('action geometry changed')
    m=summaries(c,protect,service);u=max(F(0),g-m['error']*(g+loss))
    if c.driver=='flip':
        raw=base-m['theta']*(loss-g)/2+m['keep']*(1-2*m['theta'])*u/2
    else:
        raw=base+m['keep']*(1-m['theta'])*u/2
    return (1-c.diagnostic_failure)*raw


def optimize_architecture(c:TransportContract):
    options={'skip':{'value':skip_value(c),'cost':c.ticks,'plan':None}}
    for protect,service in product((False,True),repeat=2):
        cost=reservation(c,protect,service)
        if cost>c.budget: continue
        name=('protect+' if protect else '')+('service' if service else 'diagnose')
        scored=optimize_terminal(terminal_joint(c,protect,service),c.selector_errors,c.driver)
        options[name]={'value':scored['value'],'cost':cost,'plan':scored['plan'],
                      **summaries(c,protect,service)}
    best=max(options,key=lambda k:options[k]['value'])
    return {'choice':best,'value':options[best]['value'],'gain':options[best]['value']-options['skip']['value'],
            'options':options}


def information_before_selector(c:TransportContract,protect=False):
    """I(H_current;M) in bits, conditional on diagnostic procedure survival.
    This is deliberately not claimed to measure success or implementation.
    """
    if c.prior_degraded!=F(1,2): raise ValueError('fair prior required')
    m=summaries(c,protect);e=float(m['error'])
    entropy=0. if e in (0.,1.) else -e*log2(e)-(1-e)*log2(1-e)
    return float(m['keep'])*(1-entropy)


def sign_partition_oracle(margins,flip=F(0),erasure=F(0),theta=F(0)):
    """Task-specific 1-bit encoder before a symmetric physical channel.

    Maximizes only the positive decision-margin term. Checks ALL encoders
    and decoders independently; mode choices carry no extra metadata.
    An efficient sign encoder attains the same optimum under these laws.
    """
    margins=tuple(F(x) for x in margins);flip=_prob(flip,F(1,2));erasure=_prob(erasure)
    theta=_prob(theta,F(1,2));n=len(margins)
    def value(enc):
        out=[F(0)]*3
        for d,z in zip(margins,enc):
            out[z]+=(1-erasure)*(1-flip)*d
            out[1-z]+=(1-erasure)*flip*d
            out[2]+=erasure*d
        return max(sum((out[m]*(theta+(1-2*theta)*dec[m]) for m in SIGNALS),F(0))
                   for dec in product((0,1),repeat=3))
    sign=tuple(int(d>0) for d in margins)
    full=max(value(e) for e in product((0,1),repeat=n))
    return {'enumerated':full,'sign':value(sign),'encoding':sign}
