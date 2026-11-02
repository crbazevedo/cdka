"""CDKA v5: joint noise, recoverable faults and financed reconfiguration.

Model-specific results from classical channel, coding, absorbing-chain and
resource-constrained reachability theory; no originality claim. All finite
oracles use exact rational arithmetic. The controller sees architecture and
resource, not W or a free transcript. Only successful operations harvest.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import log, sqrt
from typing import Mapping, Sequence


def probability(x) -> F:
    x = F(x)
    if not 0 <= x <= 1:
        raise ValueError('probability must lie in [0,1]')
    return x


def coupled_errors(a, b, joint) -> dict[tuple[int,int], F]:
    """Joint Bernoulli errors, with all Frechet constraints explicit."""
    a,b,joint=map(probability,(a,b,joint))
    if not max(F(0),a+b-1) <= joint <= min(a,b):
        raise ValueError('joint error violates the Frechet bounds')
    return {(0,0):1-a-b+joint,(1,0):a-joint,
            (0,1):b-joint,(1,1):joint}


def xor_failure(a,b,joint) -> F:
    law=coupled_errors(a,b,joint)
    return law[0,1]+law[1,0]


def xor_error_interval(a,b) -> tuple[F,F]:
    a,b=map(probability,(a,b))
    return abs(a-b), min(a+b,2-a-b)


def masks(size: int) -> tuple[tuple[int,...],...]:
    if type(size) is not int or size<1:
        raise ValueError('positive integer register size required')
    return tuple(product((0,1),repeat=size))


def independent_masks(size:int,p) -> dict[tuple[int,...],F]:
    p=probability(p)
    return {e:p**sum(e)*(1-p)**(size-sum(e)) for e in masks(size)}


def common_masks(size:int,p) -> dict[tuple[int,...],F]:
    p=probability(p)
    return {(0,)*size:1-p,(1,)*size:p}


def repetition_success(error_law: Mapping[tuple[int,...],F]) -> F:
    """Correct majority after an upset, with an explicitly ideal corrector.

    W has previously been correctly encoded as 000 or 111. No new reading
    of W is supplied. Correction and logical actuation follow the observed
    register only. A wrong logical response is absorbing failure.
    """
    if not error_law or sum(error_law.values(),F(0)) != 1:
        raise ValueError('normalized error law required')
    sizes={len(e) for e in error_law}
    if len(sizes)!=1 or next(iter(sizes))%2!=1:
        raise ValueError('odd common register size required')
    n=next(iter(sizes))
    if any(p<0 or any(x not in (0,1) for x in e) for e,p in error_law.items()):
        raise ValueError('invalid mask law')
    return sum((p for e,p in error_law.items() if 2*sum(e)<n),F(0))


def bounded_single_upset(p) -> dict[tuple[int,...],F]:
    """Positive noise, but never two simultaneous bit errors."""
    p=probability(p)
    return {(0,0,0):1-p,(1,0,0):p/3,(0,1,0):p/3,(0,0,1):p/3}


def repetition_certificate(size:int, max_errors:int=1) -> dict:
    """Explicit possible readings for the two repetition codewords."""
    if type(max_errors) is not int or not 0<=max_errors<=size:
        raise ValueError('invalid error radius')
    support=[e for e in masks(size) if sum(e)<=max_errors]
    readings=[]
    for w in (0,1):
        readings.append(frozenset(tuple(w^bit for bit in e) for e in support))
    collision=readings[0]&readings[1]
    return {'readings':tuple(readings),'collision':collision,
            'zero_error':not collision,'distance':size}


def safe_support(matrix: Sequence[Sequence[F]]) -> frozenset[int]:
    """Largest closed live set of a FIXED finite physical policy.

    This is not a fully observable synthesis oracle for hidden worlds.
    Row sums below one are lost/failure mass, never renormalized.
    """
    n=len(matrix)
    if any(len(row)!=n or any(v<0 for v in row) or sum(row)>1 for row in matrix):
        raise ValueError('square sub-stochastic live kernel required')
    good=set(range(n))
    while True:
        keep={i for i in good if sum(matrix[i])==1 and
              all(j in good for j,p in enumerate(matrix[i]) if p>0)}
        if keep==good:
            return frozenset(keep)
        good=keep


def redundant_kernel(damage,repair) -> tuple[tuple[F,F],tuple[F,F]]:
    """States: H=two intact copies; D=one intact copy; failure is missing mass.

    H: both components exposed independently to damage d during this epoch.
    D: repairing succeeds with probability r and returns H for next epoch;
       if it fails, the remaining component is exposed to damage d.
    Repair and exposure occupy declared phases, not simultaneous operations.
    """
    d,r=map(probability,(damage,repair))
    return (( (1-d)**2, 2*d*(1-d)),(r,(1-r)*(1-d)))


def propagate_live(matrix, initial:Sequence[F],steps:int) -> tuple[F,...]:
    if type(steps) is not int or steps<0:
        raise ValueError('nonnegative integer steps required')
    safe_support(matrix)
    if len(initial)!=len(matrix) or any(x<0 for x in initial) or sum(initial)>1:
        raise ValueError('invalid initial live law')
    mu=tuple(initial)
    for _ in range(steps):
        mu=tuple(sum((mu[i]*matrix[i][j] for i in range(len(mu))),F(0))
                 for j in range(len(mu)))
    return mu


def redundant_lifetime(damage,repair) -> F:
    """Expected number of epochs through and including the failure epoch."""
    d,r=map(probability,(damage,repair))
    if d==0:
        raise ValueError('infinite lifetime when damage=0')
    return (d*(3-2*d)+r*(1-d))/(d*d*((2-d)-r*(1-d)))


def redundant_radius(damage,repair) -> float:
    q=redundant_kernel(damage,repair)
    a,b=map(float,q[0]);c,d=map(float,q[1])
    return (a+d+sqrt((a-d)**2+4*b*c))/2


def old_success(tokens:int) -> F:
    """v4 optimal split at total normalized effort 2*tokens*log(2).

    Dyadic calibration: q_j=1-2^-j+0.5*4^-j. This is not joules.
    """
    if type(tokens) is not int or tokens<0:
        raise ValueError('nonnegative integer effort tokens required')
    x=F(1,2**tokens)
    return 1-x+x*x/2


@dataclass(frozen=True)
class Retrofit:
    """Symmetric robust macro-model with an endogenous resource ledger.

    Old architecture: spending j<=b survives with q_j; only then harvest h.
    Switch: if b>=K, spends K and installs with probability s, consuming
    the current epoch; it enters the upgraded architecture. Thereafter its
    funded maintenance loop has per-epoch reliability q_new. This supplied
    q_new must come from a separately specified physical fault/correction law.

    On every successful old epoch the physical latch is W. The copying
    operation uses that latch, never direct access to hidden W. Resource
    choices depend only on the readable b and a declared finite-horizon
    clock. Private seeds and resource signaling of W are not allowed here.
    """
    capacity:int=8
    cost:int=8
    harvest:int=5
    install:F=F(9,10)
    upgraded:F=F(1)

    def __post_init__(self):
        if any(type(x) is not int or x<0 for x in (self.capacity,self.harvest)):
            raise ValueError('finite capacity and harvest must be nonnegative integers')
        if type(self.cost) is not int or self.cost<1:
            raise ValueError('positive integer reconfiguration cost required')
        object.__setattr__(self,'install',probability(self.install))
        object.__setattr__(self,'upgraded',probability(self.upgraded))

    def _balance(self,b):
        if type(b) is not int or not 0<=b<=self.capacity:
            raise ValueError('balance outside physical reservoir')

    def next_balance(self,b,j):
        self._balance(b)
        if type(j) is not int or not 0<=j<=b:
            raise ValueError('cannot spend unharvested resources')
        return min(self.capacity,b-j+self.harvest)

    def finite(self,epochs:int):
        if type(epochs) is not int or epochs<0:
            raise ValueError('nonnegative horizon required')
        values=[tuple(F(1) for _ in range(self.capacity+1))]
        plans=[tuple('done' for _ in range(self.capacity+1))]
        for n in range(1,epochs+1):
            row=[];pol=[]
            for b in range(self.capacity+1):
                choices=[(old_success(j)*values[-1][self.next_balance(b,j)],f'run:{j}')
                         for j in range(b+1)]
                if b>=self.cost:
                    choices.append((self.install*self.upgraded**(n-1),'switch'))
                best=max(choices,key=lambda x:x[0])
                row.append(best[0]);pol.append(best[1])
            values.append(tuple(row));plans.append(tuple(pol))
        return tuple(values),tuple(plans)

    def brute_value(self,n:int,b:int) -> F:
        """Independent un-memoized path enumeration for small horizons."""
        self._balance(b)
        if n==0:return F(1)
        scores=[]
        for j in range(b+1):
            nxt=min(self.capacity,b-j+self.harvest)
            scores.append(old_success(j)*self.brute_value(n-1,nxt))
        if b>=self.cost:scores.append(self.install*self.upgraded**(n-1))
        return max(scores)

    def infinite(self):
        """Exact reach-safe probability if q_new=1, otherwise zero.

        With q_new=1, nonprogressing resource steps are dominated because
        q_j<1 and achievable reach probability is monotone in b. The optimal
        path uses only j<h before switching. Backward recursion is a DAG.
        """
        cap,K,h=self.capacity,self.cost,self.harvest
        values=[F(0)]*(cap+1);pol=['no-safe-limit']*(cap+1)
        if self.upgraded<1 or self.install==0 or cap<K:
            return tuple(values),tuple(pol)
        for b in range(K,cap+1):values[b]=self.install;pol[b]='switch'
        if h>0:
            for b in range(K-1,-1,-1):
                choices=[(old_success(j)*values[min(cap,b-j+h)],f'run:{j}')
                         for j in range(min(b,h-1)+1)]
                values[b],pol[b]=max(choices,key=lambda x:x[0])
        return tuple(values),tuple(pol)

    def infinite_path(self,b:int) -> list[dict]:
        self._balance(b)
        values,pol=self.infinite()
        if values[b]==0:return []
        path=[];mass=F(1)
        for _ in range(self.capacity+2):
            action=pol[b]
            if action=='switch':
                mass*=self.install
                path.append({'balance':b,'action':action,'mass':mass})
                return path
            j=int(action.split(':')[1]);mass*=old_success(j)
            nxt=self.next_balance(b,j)
            path.append({'balance':b,'action':action,'mass':mass,'next':nxt})
            b=nxt
        raise AssertionError('optimal infinite path must strictly progress before switch')

    def log_path_cost(self,b:int) -> float:
        v=self.infinite()[0][b]
        return -log(float(v)) if v>0 else float('inf')


def rational_solve(A:Sequence[Sequence[F]],b:Sequence[F]) -> tuple[F,...]:
    """Small independent exact linear-system oracle (Gauss-Jordan)."""
    n=len(A)
    if len(b)!=n or any(len(row)!=n for row in A):
        raise ValueError('square system required')
    M=[[F(x) for x in row]+[F(rhs)] for row,rhs in zip(A,b)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if M[i][k]),None)
        if pivot is None:raise ValueError('singular rational system')
        M[k],M[pivot]=M[pivot],M[k]
        scale=M[k][k];M[k]=[x/scale for x in M[k]]
        for i in range(n):
            if i==k:continue
            factor=M[i][k]
            M[i]=[a-factor*c for a,c in zip(M[i],M[k])]
    return tuple(row[-1] for row in M)


def infinite_survival_fixed(matrix:Sequence[Sequence[F]]) -> tuple[F,...]:
    """Exact eventual live mass for a fixed finite physical controller.

    Equals the probability of reaching the closed non-killing support
    before failure, NOT the indicator of already starting in that support.
    """
    G=safe_support(matrix);n=len(matrix)
    if not G:return (F(0),)*n
    T=tuple(i for i in range(n) if i not in G)
    A=[[F(i==j)-matrix[i][j] for j in T] for i in T]
    b=[sum((matrix[i][g] for g in G),F(0)) for i in T]
    vals=rational_solve(A,b)
    result=[F(1) if i in G else F(0) for i in range(n)]
    for i,v in zip(T,vals):result[i]=v
    return tuple(result)


def matmul(a,b):
    n=len(a)
    if len(b)!=n or any(len(row)!=n for row in (*a,*b)):
        raise ValueError('equal square matrices required')
    return tuple(tuple(sum((a[i][k]*b[k][j] for k in range(n)),F(0))
                       for j in range(n)) for i in range(n))


def switching_witness() -> dict:
    """Two individually nilpotent modes compose into a safe periodic path.

    Any persistent clock/phase or state-feedback circuit that implements
    switching must be part of the actual physical architecture.
    """
    A=((F(0),F(1)),(F(0),F(0)))
    B=((F(0),F(0)),(F(1),F(0)))
    averaged=tuple(tuple((A[i][j]+B[i][j])/2 for j in range(2)) for i in range(2))
    return {'A':A,'B':B,'A2':matmul(A,A),'B2':matmul(B,B),
            'AB':matmul(A,B),'average':averaged,
            'closed_loop':((F(0),F(1)),(F(1),F(0)))}
