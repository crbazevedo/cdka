"""CDKA v16: a shared faulty bank selects, repairs itself, works and refreshes memory.

Finite operational closure, not universal or cost-free autonomy. Six NAND gates
are reused for maintenance selection and task execution, with fresh internal
faults conditional on the same persistent bank mode. Memory and acquisition
are paid; a reliable resource guard and installed routing table remain explicit.
Exact evaluator reduction is a stochastic emission interface, not readable health.
"""
from dataclasses import dataclass, asdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb

BITS = tuple(product((0, 1), repeat=3))
VOTER = ((0, 1), (0, 2), (1, 2), (3, 4), (6, 6), (5, 7))
MODES = ('skip', 'service', 'vote', 'inverse')


def add(row, key, value):
    if value:
        row[key] = row.get(key, F(0)) + value


def probability(x):
    x = F(x)
    if not 0 <= x <= 1:
        raise ValueError('probability outside [0,1]')
    return x


@dataclass(frozen=True)
class Model:
    healthy_error: F = F(1, 1000)
    degraded_error: F = F(1, 50)
    diagnostic_error: F = F(3, 20)
    task_sensor_error: F = F(1, 50)
    degradation: F = F(1, 20)
    restoration: F = F(4, 5)
    procedure_failure: F = F(1, 200)
    capacity: int = 4
    start_balance: int = 3

    def __post_init__(self):
        for key in ('healthy_error','degraded_error','diagnostic_error',
                    'task_sensor_error','degradation','restoration','procedure_failure'):
            object.__setattr__(self,key,probability(getattr(self,key)))
        if not 0<=self.healthy_error<=self.degraded_error<=F(1,2):
            raise ValueError('ordered bank BSC errors in [0,1/2] required')
        if not 0<=self.diagnostic_error<=F(1,2) or not 0<=self.task_sensor_error<=F(1,2):
            raise ValueError('sensor BSC rates in [0,1/2] required')
        if type(self.capacity) is not int or self.capacity != 4:
            raise ValueError('this frozen policy library has capacity 4')
        if type(self.start_balance) is not int or not 1<=self.start_balance<=self.capacity:
            raise ValueError('initial balance within reservoir')

    def rate(self,z): return (self.healthy_error,self.degraded_error)[z]
    def microstates(self): return tuple((z,bits,b) for z in (0,1) for bits in BITS for b in range(1,5))
    def phases(self):
        # (physical health when memory written, current physical health, resource).
        return tuple((v,z,b) for v,z in ((0,0),(0,1),(1,1)) for b in range(1,5))


@dataclass(frozen=True)
class Policy:
    at3: str = 'vote'
    at4: str = 'vote'

    def __post_init__(self):
        if self.at3 not in MODES or self.at4 not in MODES:
            raise ValueError('mode must belong to installed routing library')

    def mode(self,b): return 'skip' if b<3 else (self.at3 if b==3 else self.at4)
    @property
    def name(self): return self.at3+'/'+self.at4


def policies(): return tuple(Policy(a,b) for a,b in product(MODES,repeat=2))


def gate_execution(bits, faults):
    if tuple(bits) not in BITS or len(faults)!=6:
        raise ValueError('three cells and six flags required')
    wires=list(bits)
    for (a,b),e in zip(VOTER,faults):
        if e not in (0,1): raise ValueError('binary gate fault')
        wires.append((1-(wires[a]&wires[b]))^e)
    return wires[-1]


@lru_cache(None)
def fault_counts():
    table=[]
    for bits in BITS:
        row=[0]*7
        for flags in product((0,1),repeat=6):
            row[sum(flags)]+=gate_execution(bits,flags)
        table.append(tuple(row))
    return tuple(table)


@lru_cache(None)
def voter(bits,gamma):
    row=fault_counts()[BITS.index(tuple(bits))]
    g=probability(gamma)
    return sum((n*g**k*(1-g)**(6-k) for k,n in enumerate(row)),F(0))


def report_probability(bits, health, eta):
    d=sum(v!=health for v in bits)
    return eta**d*(1-eta)**(3-d)


@lru_cache(None)
def task_success(p,z):
    # New world bit W is fair each epoch, then three noisy physical sensor readings.
    result=F(0)
    for w in (0,1):
        for bits in BITS:
            report=report_probability(bits,w,p.task_sensor_error)
            one=voter(bits,p.rate(z))
            result+=F(1,2)*report*(one if w else 1-one)
    return result


@lru_cache(None)
def select_probability(p,z,bits,mode):
    if mode=='skip':return F(0)
    if mode=='service':return F(1)
    if mode not in ('vote','inverse'):raise ValueError('unknown mode')
    one=voter(bits,p.rate(z))
    return one if mode=='vote' else 1-one


def health_after_service(p,z,repair):
    if not repair or z==0:return ((z,F(1)),)
    return ((0,p.restoration),(1,1-p.restoration))


def next_health(p,z):
    return ((0,1-p.degradation),(1,p.degradation)) if z==0 else ((1,F(1)),)


@lru_cache(None)
def micro_to_phase(p,policy,state):
    """A[i,j]: successful-cycle law before drawing next report.

    Common operating/acquisition debit=1 at START. Service debit=2, allowed
    only b>=3. Correct task returns 2 at END. Nothing is harvested on failure.
    Diagnostic is written about post-service health BEFORE end-of-cycle drift.
    """
    z,bits,b=state
    if state not in p.microstates():raise ValueError('invalid physical state')
    pr=select_probability(p,z,bits,policy.mode(b));row={}
    for repair,pdec in ((0,1-pr),(1,pr)):
        if not pdec:continue
        spent=1+2*repair
        if b<spent:raise AssertionError('illegal pathwise budget')
        b1=min(p.capacity,b-spent+2)
        survive_procedure=1-p.procedure_failure if repair else F(1)
        for h,ph in health_after_service(p,z,repair):
            live=pdec*survive_procedure*ph*task_success(p,h)
            for z1,pz in next_health(p,h):add(row,(h,z1,b1),live*pz)
    return row


@lru_cache(None)
def emission(p,phase):
    v,z,b=phase
    if phase not in p.phases():raise ValueError('invalid regeneration phase')
    return {(z,bits,b):report_probability(bits,v,p.diagnostic_error) for bits in BITS
            if report_probability(bits,v,p.diagnostic_error)}


@lru_cache(None)
def reduced_row(p,policy,phase):
    """E A. No hidden condition is passed to the runtime routing policy."""
    row={}
    for micro,w in emission(p,phase).items():
        for target,pt in micro_to_phase(p,policy,micro).items():add(row,target,w*pt)
    return row


@lru_cache(None)
def physical_row(p,policy,state):
    """A E. This is an optimized row; raw_row is an independent gate-level oracle."""
    row={}
    for phase,w in micro_to_phase(p,policy,state).items():
        for target,pt in emission(p,phase).items():add(row,target,w*pt)
    return row


def push(law,kernel):
    row={}
    for s,w in law.items():
        for t,pt in kernel(s).items():add(row,t,w*pt)
    return row


def initial_phase(p,prior=F(1,2)):
    prior=probability(prior)
    return {(0,0,p.start_balance):1-prior,(1,1,p.start_balance):prior}


def initial_micro(p,prior=F(1,2)):
    return push(initial_phase(p,prior),lambda s:emission(p,s))


def forward(p,policy,horizon,prior=F(1,2),raw=False):
    if type(horizon) is not int or horizon<0:raise ValueError('finite nonnegative horizon')
    law=initial_micro(p,prior) if raw else initial_phase(p,prior)
    curve=[F(1)]
    for _ in range(horizon):
        law=push(law,(lambda s:physical_row(p,policy,s)) if raw else (lambda s:reduced_row(p,policy,s)))
        curve.append(sum(law.values(),F(0)))
    return tuple(curve),law


@lru_cache(None)
def raw_task_success(p,z):
    """Independent scalar event oracle, no voter_profile reused."""
    total=F(0);g=p.rate(z)
    for world in (0,1):
        for noise in BITS:
            pw=F(1,2)*p.task_sensor_error**sum(noise)*(1-p.task_sensor_error)**(3-sum(noise))
            bits=tuple(world^v for v in noise)
            for flags in product((0,1),repeat=6):
                if gate_execution(bits,flags)==world:
                    total+=pw*g**sum(flags)*(1-g)**(6-sum(flags))
    return total


@lru_cache(None)
def raw_row(p,policy,state):
    """Full event-derived row; no E/A factorization, forward value or reduced row.

    Repeated fault flags are summed by mode before later conditional branches;
    the task stage is independently enumerated in raw_task_success. Conditional
    health, including unobserved service outcome, is never averaged prematurely.
    """
    z,bits,b=state;mode=policy.mode(b);choose={}
    if mode in ('skip','service'):choose[int(mode=='service')]=F(1)
    else:
        for flags in product((0,1),repeat=6):
            decision=gate_execution(bits,flags)^(mode=='inverse')
            pr=p.rate(z)**sum(flags)*(1-p.rate(z))**(6-sum(flags))
            add(choose,int(decision),pr)
    row={}
    for repair,pdec in choose.items():
        after=b-1-2*repair
        if after<0:raise AssertionError('overspending')
        balance=min(4,after+2)
        for success,ps in ((0,1-p.restoration),(1,p.restoration)) if repair else ((0,F(1)),):
            h=0 if success else z
            live=pdec*ps*raw_task_success(p,h)*(1-p.procedure_failure if repair else 1)
            for noise in BITS:
                word=tuple(h^v for v in noise)
                pm=p.diagnostic_error**sum(noise)*(1-p.diagnostic_error)**(3-sum(noise))
                if h==0:
                    add(row,(0,word,balance),live*pm*(1-p.degradation))
                    add(row,(1,word,balance),live*pm*p.degradation)
                else:add(row,(1,word,balance),live*pm)
    return row


def vector_value(p,policy,horizon):
    states=p.phases();v={s:F(1) for s in states}
    for _ in range(horizon):
        v={s:sum((w*v[t] for t,w in reduced_row(p,policy,s).items()),F(0)) for s in states}
    return v


def all_stationary(p,horizon):
    result=[]
    for policy in policies():
        v=vector_value(p,policy,horizon)
        low=v[(0,0,p.start_balance)];high=v[(1,1,p.start_balance)]
        result.append({'policy':policy,'value':(low+high)/2,'healthy':low,'degraded':high})
    return sorted(result,key=lambda r:(r['value'],r['policy'].name),reverse=True)


def event_traces(p,policy,state):
    """Aggregate named causal branches, retaining probability mass and resources.

    Returns complete successful branch traces with the procedure+task failures
    separately. Not samples and not designer beliefs fed to the controller.
    """
    z,bits,b=state;pr=select_probability(p,z,bits,policy.mode(b));rows=[]
    for repair,pd in ((0,1-pr),(1,pr)):
        if not pd:continue
        proc=1-p.procedure_failure if repair else F(1)
        if pd*(1-proc):rows.append({'repair':repair,'outcome':'procedure_failure','mass':pd*(1-proc),'balance_after_debit':b-1-2*repair})
        for h,ph in health_after_service(p,z,repair):
            pc=pd*proc*ph
            if pc*(1-task_success(p,h)):rows.append({'repair':repair,'health_after':h,'outcome':'task_failure','mass':pc*(1-task_success(p,h)),'balance_after_debit':b-1-2*repair})
            for target,pt in next_health(p,h):
                for word in BITS:
                    pm=report_probability(word,h,p.diagnostic_error)
                    w=pc*task_success(p,h)*pt*pm
                    if w:rows.append({'repair':repair,'health_after':h,'next_health':target,'word':word,'outcome':'live','mass':w,'balance_after_debit':b-1-2*repair,'balance_next':min(4,b+1-2*repair)})
    assert sum((r['mass'] for r in rows),F(0))==1
    return tuple(rows)


def run_summary(p,policy,horizon,prior=F(1,2)):
    """Unnormalized accounting over every alive prefix; no survivor-only reward."""
    law=initial_phase(p,prior);mass=F(1);curves=[mass]
    attempts=F(0);spent=F(1);earned=F(0);completed=F(0) # initialization debit 1
    for _ in range(horizon):
        repair=F(0)
        for phase,w in law.items():
            for micro,pm in emission(p,phase).items():
                z,bits,b=micro
                repair+=w*pm*select_probability(p,z,bits,policy.mode(b))
        attempts+=repair;spent+=mass+2*repair
        law=push(law,lambda x:reduced_row(p,policy,x))
        mass=sum(law.values(),F(0));earned+=2*mass;completed+=mass;curves.append(mass)
    return {'survival':mass,'curve':tuple(curves),'expected_services':attempts,
            'expected_spent_including_initialization':spent,
            'expected_earned':earned,'expected_completed_tasks':completed,
            'alive_healthy_mass':sum((w for (v,z,b),w in law.items() if z==0),F(0)),
            'alive_resource_mass':sum((b*w for (v,z,b),w in law.items()),F(0)),
            'terminal_law':law}
