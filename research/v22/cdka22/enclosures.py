"""Outward dyadic enclosures for both regenerative response algorithms.

Integer arithmetic, not guessed float error bars. All inputs are exact rational
model data. Prediction of algorithm cost has no authority over answer accuracy.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import time
from vendor.v21.cdka.regenerative import Model,ContractError,validate,horizon_ok,partition_number,compositions_count

class PrecisionExhausted(ArithmeticError):pass

class Dyadic:
    def __init__(self,bits):
        if type(bits)is not int or bits<8:raise ValueError('bits must be integer >=8')
        self.bits=bits;self.scale=1<<bits;self.zero=(0,0);self.one=(self.scale,self.scale)
        self.multiplications=0;self.additions=0
    def rational(self,x):
        x=F(x);a=x.numerator*self.scale;b=x.denominator
        return a//b,-((-a)//b)
    def add(self,a,b):
        self.additions+=1;return a[0]+b[0],a[1]+b[1]
    def mul(self,a,b):
        if a[0]<0 or b[0]<0:raise ValueError('nonnegative multiplication only')
        self.multiplications+=1
        if a==(0,0) or b==(0,0):return self.zero
        return (a[0]*b[0])>>self.bits,(a[1]*b[1]+self.scale-1)>>self.bits
    def times_int(self,a,k):
        if k<0:raise ValueError('nonnegative multiplier')
        return a[0]*k,a[1]*k
    def sum(self,terms):
        lo=hi=0
        for a,b in terms:lo+=a;hi+=b;self.additions+=1
        return lo,hi
    def product(self,terms):
        out=self.one
        for term in terms:out=self.mul(out,term)
        return out
    def probability(self,a):
        lo=max(0,a[0]);hi=min(self.scale,a[1])
        if lo>hi:raise ArithmeticError('invalid probability enclosure')
        return lo,hi
    def complement(self,a):
        a=self.probability(a);return self.scale-a[1],self.scale-a[0]
    def powers(self,a,n):
        out=[self.one]
        for _ in range(n):out.append(self.mul(out[-1],a))
        return out
    def signed_sum(self,terms):
        lo=hi=0
        for sign,(a,b) in terms:
            if sign==1:lo+=a;hi+=b
            elif sign==-1:lo-=b;hi-=a
            else:raise ValueError('invalid sign')
            self.additions+=1
        return lo,hi

@dataclass(frozen=True)
class Enclosure:
    lower_numerator:int
    upper_numerator:int
    bits:int
    backend:str
    multiplications:int
    additions:int
    @property
    def lower(self):return F(self.lower_numerator,1<<self.bits)
    @property
    def upper(self):return F(self.upper_numerator,1<<self.bits)
    @property
    def midpoint(self):return (self.lower+self.upper)/2
    @property
    def radius(self):return (self.upper-self.lower)/2
    def contains(self,x):return self.lower<=F(x)<=self.upper
    def meets(self,rtol=F(1,10**8),atol=F(0)):
        rtol,atol=F(rtol),F(atol)
        if rtol<0 or atol<0:raise ValueError('nonnegative tolerances')
        return self.radius<=atol+rtol*self.lower
    def as_dict(self):
        return {'backend':self.backend,'bits':self.bits,'lower_numerator':str(self.lower_numerator),
                'upper_numerator':str(self.upper_numerator),'denominator_power_of_two':self.bits,
                'midpoint_decimal':format(float(self.midpoint),'.17g'),'width_decimal':format(float(self.upper-self.lower),'.17g'),
                'multiplications':self.multiplications,'additions':self.additions}

def local_tables(model,h,a):
    out=[]
    for c in model.components:
        transient=[i for i in range(len(c.initial)) if i not in c.target]
        T=[[a.rational(c.work[i][j]) for j in transient] for i in transient]
        v=[a.rational(c.initial[i]) for i in transient];f=[a.one]
        for _ in range(h):
            v=[a.probability(a.sum(a.mul(v[i],T[i][j]) for i in range(len(v)))) for j in range(len(v))]
            f.append(a.probability(a.sum(v)))
        out.append(f)
    return out

def histogram(model,h,bits=64,*,checked=False):
    horizon_ok(h)
    if not checked:validate(model)
    if partition_number(h+1)>100000:raise ContractError('interval histogram class limit')
    a=Dyadic(bits)
    if h==0:return Enclosure(0,0,bits,'histogram',0,0)
    f=local_tables(model,h,a);R=[[a.rational(x) for x in row] for row in model.environment];nu=[a.rational(x) for x in model.initial_environment]
    powers=[[a.powers(R[i][j],h) for j in (0,1)] for i in (0,1)];weights={}
    for n in range(1,h+1):
        m=h-n
        for r in range(1,min(n,m+1)+1):
            terms=[]
            for start,k,wr,rw in ((0,r-1,r-1,r-1),(0,r,r,r-1),(1,r,r-1,r),(1,r+1,r,r)):
                ways=compositions_count(m,k)
                if ways:
                    v=a.product((nu[start],powers[0][0][n-r],powers[1][1][m-k],powers[0][1][wr],powers[1][0][rw]))
                    terms.append(a.times_int(v,ways))
            weights[n,r]=a.probability(a.sum(terms))
    total=a.zero
    def visit(lengths,n,minimum,repeat,mult,survivals):
        nonlocal total
        r=len(lengths)
        for ell in range(minimum,h-n-r+1):
            rep=repeat+1 if lengths and ell==lengths[-1] else 1;m1=mult*(r+1)//rep
            s1=[a.mul(x,tab[ell]) for x,tab in zip(survivals,f)]
            weight=a.probability(a.times_int(weights[n+ell,r+1],m1))
            total=a.add(total,a.mul(weight,a.product(a.complement(x) for x in s1)))
            visit(lengths+(ell,),n+ell,ell,rep,m1,s1)
    visit((),0,1,0,1,[a.one]*len(f))
    lo,hi=a.probability(total)
    return Enclosure(lo,hi,bits,'histogram',a.multiplications,a.additions)

def subset(model,h,bits=64,*,checked=False):
    horizon_ok(h)
    if not checked:validate(model)
    n=len(model.components)
    if n>16:raise ContractError('interval subset limit N<=16')
    a=Dyadic(bits)
    if h==0:return Enclosure(0,0,bits,'subset',0,0)
    f=local_tables(model,h,a);R=[[a.rational(x) for x in row] for row in model.environment];nu=[a.rational(x) for x in model.initial_environment]
    pow00=a.powers(R[0][0],h);terms=[]
    for mask in range(1<<n):
        q=[a.one]*(h+1)
        for i in range(n):
            if mask>>i&1:q=[a.mul(x,y) for x,y in zip(q,f[i])]
        C=[a.zero]+[a.mul(q[l],pow00[l-1]) for l in range(1,h+1)]
        W=[a.zero]*(h+1);B=[a.zero]*(h+1)
        for t in range(1,h+1):
            W[t]=a.probability(a.add(a.mul(nu[0],C[t]),a.mul(R[1][0],a.sum(a.mul(B[t-l],C[l]) for l in range(1,t)))))
            B[t]=nu[1] if t==1 else a.probability(a.add(a.mul(R[1][1],B[t-1]),a.mul(R[0][1],W[t-1])))
        terms.append((-1 if mask.bit_count()%2 else 1,a.probability(a.add(W[h],B[h]))))
    lo,hi=a.probability(a.signed_sum(terms))
    return Enclosure(lo,hi,bits,'subset',a.multiplications,a.additions)

def shortest_work_completion(c):
    current={i for i,p in enumerate(c.initial) if p};seen=set(current);distance=0
    while current:
        if any(i in c.target for i in current):return distance
        current={j for i in current for j,p in enumerate(c.work[i]) if p and j not in seen}
        seen.update(current);distance+=1
    return None

def certified_solve(model,h,backend,*,rtol=F(1,10**8),atol=F(0),initial_bits=64,max_bits=512,checked=False):
    horizon_ok(h)
    if backend not in ('histogram','subset'):raise ValueError('unknown backend')
    if not checked:validate(model)
    if type(initial_bits)is not int or type(max_bits)is not int or not 8<=initial_bits<=max_bits:raise ValueError('invalid precision budget')
    rtol,atol=F(rtol),F(atol)
    if rtol<0 or atol<0:raise ValueError('invalid tolerance')
    start=time.perf_counter();trace=[]
    if any(l is None or l>h for l in [shortest_work_completion(c) for c in model.components]):
        return {'enclosure':Enclosure(0,0,initial_bits,backend,0,0),'attempts':[],'elapsed_s':time.perf_counter()-start,'structural_zero':True}
    b=initial_bits
    while b<=max_bits:
        t=time.perf_counter();e=globals()[backend](model,h,b,checked=True)
        trace.append({'bits':b,'elapsed_s':time.perf_counter()-t,'accepted':e.meets(rtol,atol),**e.as_dict()})
        if e.meets(rtol,atol):return {'enclosure':e,'attempts':trace,'elapsed_s':time.perf_counter()-start,'structural_zero':False}
        b+=32
    raise PrecisionExhausted(f'no certified answer at <= {max_bits} bits; {backend}, N={len(model.components)}, H={h}')
