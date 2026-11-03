"""CDKA v13: synthesize a readable one-bit continuation update in NAND hardware.

The v6 plant is unchanged. Initial diagnosis is encoded in two priced-common
latches. The first physical action is SERVICE for every diagnosis. Immediately
before the final command, a shared combinational circuit reads the transported
two-bit word and the new readable syndrome, then writes ONE action bit. Only
that updated bit reaches the final actuator (0=HOLD, 1=REFRESH).

NAND gates are noiseless in the synthesis contract; final write noise is a
separate uniform BSC. Faulty gates are treated in an explicit falsifier, not
silently merged under noiseless truth-table equivalence. Gate slots measure
capacity, not joules or the plant's consumable resource tokens.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import lcm
from .composition import Contract, DEAD, macro_row, micro_row
from .continuation_interfaces import equal_signal_joint
from .joint_compilation import Surd, quadratic_roots, quadratic_nonnegative

# Input index x=2*m+k. Bit masks encode truth tables on all eight readable rows.
INPUTS = (
    sum(((x//2)&1)<<x for x in range(8)),
    sum((((x//2)>>1)&1)<<x for x in range(8)),
    sum((x%2)<<x for x in range(8)),
)
BASE = tuple(sorted(set((0,255)+INPUTS)))
CHANNEL_POLY=((1,-2,1),(0,1,-1),(0,0,1))


@dataclass(frozen=True)
class Circuit:
    """A deterministic DAG, with wires named by their exact truth functions."""
    output: int
    gates: tuple[tuple[int,int,int], ...] = ()

    @property
    def cost(self):
        return len(self.gates)

    def execute(self, word: int, syndrome: int, faults: tuple[int,...] | None = None) -> int:
        if word not in range(4) or syndrome not in (0,1):
            raise ValueError('readable word and binary syndrome required')
        if faults is None:
            faults=(0,)*self.cost
        if len(faults)!=self.cost or any(e not in (0,1) for e in faults):
            raise ValueError('one binary fault flag per gate required')
        x=2*word+syndrome
        values={t:(t>>x)&1 for t in BASE}
        for (a,b,t),e in zip(self.gates,faults):
            if a not in values or b not in values:
                raise ValueError('noncausal circuit edge')
            values[t]=(1-(values[a]&values[b]))^e
        return values[self.output]


@lru_cache(None)
def nand_library(max_gates=4):
    """Exact noiseless DAG synthesis via sets of available functions.

    Two partial netlists with the same available functions and cost admit the
    same ideal-gate extensions: retain one witness per signal set. This is a
    certified continuation quotient of the circuit search, not a heuristic.
    Unlimited fanout, wires and constants are common primitives. Repeating an
    existing ideal truth function cannot improve any later implementation.
    Do NOT reuse this quotient for gate-fault reliability or analog timing.
    """
    if type(max_gates) is not int or not 0<=max_gates<=5:
        raise ValueError('max_gates must be an integer in [0,5]')
    states={BASE:()}
    best={t:Circuit(t) for t in BASE}
    profile=[{'gates':0,'signal_sets':1,'functions':len(best)}]
    for depth in range(1,max_gates+1):
        nxt={}
        for available,witness in states.items():
            for a,b in combinations_with_replacement(available,2):
                t=255^(a&b)
                if t in available:
                    continue
                key=tuple(sorted((*available,t)))
                path=witness+((a,b,t),)
                if key not in nxt:
                    nxt[key]=path
                if t not in best:
                    best[t]=Circuit(t,nxt[key])
        states=nxt
        profile.append({'gates':depth,'signal_sets':len(states),'functions':len(best)})
    return best,tuple(profile)


@lru_cache(None)
def payoff_table(tail=F(1,100)):
    """Joint live weights after SERVICE times terminal success of each action.

    Table[y][k][u] already includes sensor prior and first-stage failures.
    H and initial Y are evaluator-only. The real update receives only (m,k).
    Resource: start b=4; SERVICE costs 2, then successful harvest 1 gives b=3.
    Both terminal commands, including a wrong REFRESH, are therefore affordable.
    """
    joint=equal_signal_joint(tail)
    p=Contract()
    out=[[[F(0),F(0)] for k in (0,1)] for y in range(3)]
    for y in range(3):
        for h in (0,1):
            for s,mass in macro_row(p,(0,h,4),'service').items():
                if s==DEAD:
                    continue
                k,h1,b=s
                for u,a in enumerate(('hold','refresh')):
                    out[y][k][u]+=joint[y][h]*mass*(1-macro_row(p,s,a)[DEAD])
    return tuple(tuple(tuple(row) for row in y) for y in out)


def _prob(p):
    p=F(p)
    if not 0<=p<=F(1,2):
        raise ValueError('BSC error must be in [0,1/2]')
    return p


def transport_probability(source,target,p):
    d=(source^target).bit_count()
    return p**d*(1-p)**(2-d)


def margins(encoding,p=F(0),tail=F(1,100)):
    p=_prob(p)
    encoding=tuple(encoding)
    if len(encoding)!=3 or any(c not in range(4) for c in encoding):
        raise ValueError('one two-bit codeword per diagnostic required')
    T=payoff_table(tail)
    mass=[[F(0),F(0)] for x in range(8)]
    for y,word in enumerate(encoding):
        for received in range(4):
            prob=transport_probability(word,received,p)
            for k in (0,1):
                for u in (0,1):
                    mass[2*received+k][u]+=prob*T[y][k][u]
    return tuple(tuple(x) for x in mass)


def evaluate(encoding,truth,p=F(0),q=F(0),tail=F(1,100)):
    """Exact end-to-end value, including noisy newly written action bit."""
    q=_prob(q)
    if type(truth) is not int or truth not in range(256):
        raise ValueError('eight-row truth table required')
    row=margins(encoding,p,tail)
    return sum(((1-q)*w[(truth>>x)&1]+q*w[1-((truth>>x)&1)]
                for x,w in enumerate(row)),F(0))


def bypass_value(tail=F(1,100)):
    T=payoff_table(tail)
    return max(sum((T[y][k][u] for y in range(3) for k in (0,1)),F(0)) for u in (0,1))


def raw_value(encoding,circuit,p=F(0),q=F(0),tail=F(1,100)):
    """Independent physical-bit/state oracle; never reads hidden health in policy."""
    p=_prob(p);q=_prob(q);model=Contract();joint=equal_signal_joint(tail)
    total=F(0)
    for y in range(3):
        for h in (0,1):
            for s,mass in micro_row(model,(0,(0,0,0),h,4),'service').items():
                if s==DEAD:
                    continue
                w,cells,h1,b=s;k=int(sum(cells)not in (0,3))
                for received in range(4):
                    prob=transport_probability(encoding[y],received,p)
                    requested=circuit.execute(received,k)
                    for flip,pf in ((0,1-q),(1,q)):
                        action=('hold','refresh')[requested^flip]
                        total+=joint[y][h]*mass*prob*pf*(1-micro_row(model,s,action)[DEAD])
    return total


@lru_cache(None)
def program_polynomial(encoding,truth,tail=F(1,100)):
    """Quadratic in old-register noise p, before the final write BSC."""
    T=payoff_table(tail)
    base=sum((T[y][k][0] for y in range(3) for k in (0,1)),F(0))
    c=[base,F(0),F(0)]
    for y,word in enumerate(encoding):
        for received in range(4):
            basis=CHANNEL_POLY[(word^received).bit_count()]
            for k in (0,1):
                if (truth>>(2*received+k))&1:
                    d=T[y][k][1]-T[y][k][0]
                    for i in range(3):c[i]+=d*basis[i]
    return tuple(c)


@lru_cache(None)
def candidates(max_gates=4):
    library,_=nand_library(max_gates)
    result=[]
    for enc in product(range(4),repeat=3):
        for t,circuit in library.items():
            result.append((enc,circuit,program_polynomial(enc,t)))
    return tuple(result)


def synthesize(p=F(1,100),q=F(0),budget=4,allow_bypass=True):
    p=_prob(p);q=_prob(q)
    if type(budget)is not int or not 0<=budget<=4:raise ValueError('gate budget 0..4')
    T=payoff_table();base=sum((T[y][k][0] for y in range(3) for k in (0,1)),F(0))
    total_margin=sum((T[y][k][1]-T[y][k][0] for y in range(3) for k in (0,1)),F(0))
    best=None
    for enc,circ,c in candidates(budget):
        w0=c[0]+p*c[1]+p*p*c[2]
        value=base+q*total_margin+(1-2*q)*(w0-base)
        key=(value,-circ.cost,-len(set(enc)),tuple(-v for v in enc),-circ.output)
        if best is None or key>best[0]:best=(key,enc,circ)
    key,enc,circ=best
    bypass=bypass_value()
    return {'value':max(key[0],bypass) if allow_bypass else key[0],
            'update_value':key[0],'bypass_value':bypass,
            'uses_bypass':bool(allow_bypass and bypass>=key[0]),
            'encoding':enc,'circuit':circ,'gate_budget':budget}


def family_constants():
    T=payoff_table()
    a=T[0][0][0]-T[0][0][1]
    b=sum((T[y][0][1]-T[y][0][0] for y in (1,2)),F(0))
    D=sum((T[y][k][1]-T[y][k][0] for y in range(3) for k in (0,1)),F(0))
    if not (0<a<b and D>0 and all(T[y][1][1]>T[y][1][0] for y in range(3))):
        raise ValueError('calibrated margin regime no longer holds')
    return a,b,D


def analytical_value(p,q,budget):
    p=_prob(p);q=_prob(q)
    if budget not in range(5):raise ValueError('gate budget 0..4')
    a,b,D=family_constants()
    gain=F(0) if budget<2 else (a*(1-p)-b*p if budget<4 else a*(1-p)**2-b*p*p)
    return bypass_value()+max(F(0),(1-2*q)*gain-q*D)


def phase_certificate():
    """Exact continuous certification for all p in [0,1/2], all uniform q.

    At q<=1/2 ordering of programs is unchanged (positive affine transform).
    Compare each candidate quadratic to the claimed envelope for q=0;
    add the common physical bypass afterward. No sampled-grid optimality claim.
    """
    a,b,D=family_constants();v=bypass_value()
    r1=Surd(a/(a+b))
    r2=quadratic_roots((a,-2*a,a-b))[1]
    checks=0;stats=[]
    for budget in range(5):
        if budget<2:
            segments=[((v,F(0),F(0)),Surd(0),Surd(F(1,2)))]
        elif budget<4:
            segments=[((v+a,-a-b,F(0)),Surd(0),r1),((v,F(0),F(0)),r1,Surd(F(1,2)))]
        else:
            segments=[((v+a,-2*a,a-b),Surd(0),r2),((v,F(0),F(0)),r2,Surd(F(1,2)))]
        unique={row[2] for row in candidates(budget)}
        for winner,left,right in segments:
            for c in unique:
                difference=tuple(winner[i]-c[i] for i in range(3))
                if not quadratic_nonnegative(difference,left,right):
                    raise AssertionError('candidate exceeds claimed global frontier')
                checks+=1
        stats.append({'budget':budget,'programs':len(candidates(budget)),
                      'distinct_curves':len(unique),'segments':len(segments)})
    return {'a':a,'b':b,'total_margin':D,'baseline':v,
            'threshold_two_gates':r1,'threshold_four_gates':r2,
            'dominance_checks':checks,'budgets':tuple(stats)}


def gate_fault_falsifier(error=F(1,10)):
    """Identity wire vs two NAND inverters: same truth, different noise law."""
    error=_prob(error)
    t=INPUTS[0];n=255^t
    circuit=Circuit(t,((t,t,n),(n,n,t)))
    outputs=[]
    for bit in (0,1):
        wrong=F(0)
        for e in product((0,1),repeat=2):
            prob=F(1)
            for f in e:prob*=error if f else 1-error
            wrong+=prob*(circuit.execute(bit,0,e)!=bit)
        outputs.append(wrong)
    return {'wire_error':F(0),'double_inverter_error':tuple(outputs),
            'formula':2*error*(1-error)}
