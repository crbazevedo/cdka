"""CDKA v10: jointly compile a diagnostic code and a bounded plan library.

Known joint source/channel and state-assignment tools; no novelty claim.
The v6/v9 plant stays fixed. A paid library is installed before Y is known;
Y is encoded in two physical latches. Each bit may flip once, BEFORE any
plant action. The resulting word is retained during both plant epochs.
It is the entire diagnostic memory: no free original Y or plan pointer.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import lcm, sqrt
from .composition import Contract
from .continuation_interfaces import plans, upper_envelope, equal_signal_joint


@dataclass(frozen=True)
class Surd:
    """Exact a + b sqrt(d), d>=0; comparisons to rationals never use floats."""
    a: F
    b: F = F(0)
    d: F = F(0)

    def __post_init__(self):
        for key in ('a','b','d'):
            object.__setattr__(self,key,F(getattr(self,key)))
        if self.d<0: raise ValueError('real radical required')

    def sign(self):
        a,b,d=self.a,self.b,self.d
        s=lambda x: int(x>0)-int(x<0)
        if not b or not d:return s(a)
        if not a:return s(b)
        if s(a)==s(b):return s(a)
        diff=a*a-b*b*d
        return s(a)*s(diff)  # zero when cancellation is exact

    def compare_rational(self, x):
        return Surd(self.a-F(x),self.b,self.d).sign()

    def approximate(self):
        return float(self.a)+float(self.b)*sqrt(float(self.d))

    def evaluate(self, coefficients):
        c0,c1,c2=map(F,coefficients)
        return Surd(c0+c1*self.a+c2*(self.a*self.a+self.b*self.b*self.d),
                    c1*self.b+2*c2*self.a*self.b,self.d)


def quadratic_roots(c):
    c0,c1,c2=map(F,c)
    if not c2:
        if not c1:raise ValueError('nonconstant polynomial required')
        root=Surd(-c0/c1);return root,root
    discriminant=c1*c1-4*c2*c0
    if discriminant<0:raise ValueError('real roots required')
    a=-c1/(2*c2);b=1/(2*abs(c2))
    return Surd(a,-b,discriminant),Surd(a,b,discriminant)


def quadratic_nonnegative(c, left, right):
    """Certificate on a declared ordered interval: endpoints + interior vertex."""
    c=tuple(map(F,c))
    if left.evaluate(c).sign()<0 or right.evaluate(c).sign()<0:return False
    if c[2]>0:
        vertex=-c[1]/(2*c[2])
        if left.compare_rational(vertex)<0 and right.compare_rational(vertex)>0:
            return c[0]+c[1]*vertex+c[2]*vertex*vertex>=0
    return True


def channel_row(word, p, bits=2):
    p=F(p)
    if bits not in (1,2) or not 0<=p<=F(1,2) or not 0<=word<2**bits:
        raise ValueError('one/two bits, valid input, 0<=p<=1/2')
    return tuple(p**(word^out).bit_count()*(1-p)**(bits-(word^out).bit_count())
                 for out in range(2**bits))


@lru_cache(None)
def continuation_table(balance=4, tail=F(1,100), reduced=True):
    p=Contract();lib=plans(p,b=balance)
    ids=tuple(seg[2] for seg in upper_envelope(lib)) if reduced else tuple(range(len(lib)))
    joint=equal_signal_joint(tail)
    table=tuple(tuple(mu[0]*lib[i].alpha[0]+mu[1]*lib[i].alpha[1] for i in ids)
                for mu in joint)
    return ids,table


def evaluate_witness(encoding, decoder, error, balance=4, tail=F(1,100)):
    """Exact value of actual encoder and decoded TWO-EPOCH physical plans."""
    encoding=tuple(encoding);decoder=tuple(decoder)
    bits={2:1,4:2}.get(len(decoder))
    if bits is None or len(encoding)!=3:raise ValueError('three signals and binary hardware')
    ids,table=continuation_table(balance,tail,False)
    if any(i not in ids for i in decoder):raise ValueError('plan not in installed plant library')
    total=F(0)
    for y,word in enumerate(encoding):
        for r,prob in enumerate(channel_row(word,error,bits)):
            total+=prob*table[y][decoder[r]]
    return total


def best_decoder(encoding,error,max_templates=3,balance=4,tail=F(1,100),reduced=True):
    """A joint program constraint: all output words share <=L installed plans.

    Envelope replacement proves pruning exact for cardinality-only library
    charges. It is NOT valid for arbitrary unequal or shared circuit costs.
    """
    if type(max_templates)is not int or max_templates<1:raise ValueError('positive library cap')
    if len(encoding)!=3 or any(x not in range(4) for x in encoding):raise ValueError('two-bit words')
    ids,table=continuation_table(balance,tail,reduced)
    masses=[tuple(sum((channel_row(encoding[y],error)[r]*table[y][j]
                       for y in range(3)),F(0)) for j in range(len(ids))) for r in range(4)]
    best=None
    for k in range(1,min(max_templates,len(ids))+1):
        for subset in combinations(range(len(ids)),k):
            choices=tuple(max(subset,key=lambda j:masses[r][j]) for r in range(4))
            val=sum((masses[r][choices[r]] for r in range(4)),F(0))
            decoder=tuple(ids[j] for j in choices)
            key=(val,-len(set(decoder)),tuple(-x for x in decoder))
            if best is None or key>best[0]:best=(key,decoder)
    return {'value':best[0][0],'encoding':tuple(encoding),'decoder':best[1],
            'templates':len(set(best[1])),'code_states':len(set(encoding)),
            'balance':balance}


def synthesize(error,max_templates=3,balance=4,tail=F(1,100),injective=False):
    """All 4^3 physical encoders, with an optimal jointly limited plan table."""
    best=None
    for enc in product(range(4),repeat=3):
        if injective and len(set(enc))!=3:continue
        ans=best_decoder(enc,error,max_templates,balance,tail)
        key=(ans['value'],-ans['templates'],-ans['code_states'],tuple(-x for x in enc))
        if best is None or key>best[0]:best=key,ans
    return best[1]


def funded_synthesis(error,total_balance=4,price=1,tail=F(1,100)):
    """Preinstall L templates for price*(L-1), then run SAME plant law.

    L counts installed plans, not stochastic action rows. This is an
    explicit ROM-library contract. Tokens are not joules; the two latches
    and base decoder are common/sunk. No signal-dependent resource trace.
    """
    if type(total_balance)is not int or total_balance not in range(5):raise ValueError('balance 0..4')
    if type(price)is not int or price<0:raise ValueError('integer price >=0')
    choices=[]
    for installed in range(1,4):
        fee=price*(installed-1)
        if fee>total_balance:continue
        ans=synthesize(error,installed,total_balance-fee,tail)
        choices.append(dict(ans,installed=installed,fee=fee))
    # Max slots may go unused. An unused installed slot still costs its fee.
    return max(choices,key=lambda x:(x['value'],-x['fee'])),tuple(choices)


@lru_cache(None)
def polynomial_candidates():
    """All 64 physical encoders × 81 decoders over three envelope plans.

    Exact integer coefficients share one positive denominator. The finite
    list certifies a continuum of bit errors when paired with the quadratic
    interval checker. No floating-point value is used for dominance.
    """
    ids,table=continuation_table()
    denominator=lcm(*(v.denominator for row in table for v in row))
    integer=[[int(v*denominator) for v in row] for row in table]
    polynomials=((1,-2,1),(0,1,-1),(0,0,1))
    unique={}
    for enc in product(range(4),repeat=3):
        for dec in product(range(len(ids)),repeat=4):
            coeff=[0,0,0]
            for y in range(3):
                for r in range(4):
                    v=integer[y][dec[r]];basis=polynomials[(enc[y]^r).bit_count()]
                    for k in range(3):coeff[k]+=v*basis[k]
            key=tuple(coeff)
            if key not in unique:unique[key]=(enc,tuple(ids[x] for x in dec))
    return denominator,unique


def witness_polynomial(enc,dec):
    # Three exact values determine the quadratic; independent of above enumeration.
    f0=evaluate_witness(enc,dec,F(0))
    fh=evaluate_witness(enc,dec,F(1,2))
    fq=evaluate_witness(enc,dec,F(1,4))
    c2=8*(fh-2*fq+f0);c1=4*(fq-f0)-c2/4
    return f0,c1,c2


def phase_certificate():
    witnesses=(((0,1,3),(50,58,58,42)),((0,0,3),(58,58,58,42)),
               ((0,0,0),(58,58,58,58)))
    curves=tuple(witness_polynomial(*w) for w in witnesses)
    diff=lambda a,b:tuple(x-y for x,y in zip(a,b))
    first=quadratic_roots(diff(curves[0],curves[1]))[0]
    second=quadratic_roots(diff(curves[1],curves[2]))[1]
    if not (first.compare_rational(0)>0 and first.compare_rational(F(1,100))<0
            and second.compare_rational(F(1,5))>0 and second.compare_rational(F(1,4))<0):
        raise AssertionError('root isolation/order failed')
    intervals=((Surd(0),first),(first,second),(second,Surd(F(1,2))))
    denominator,candidates=polynomial_candidates();count=0
    for curve,(lo,hi) in zip(curves,intervals):
        for c in candidates:
            difference=tuple(curve[k]-F(c[k],denominator) for k in range(3))
            if not quadratic_nonnegative(difference,lo,hi):
                raise AssertionError('uncertified phase: competitor crosses envelope')
            count+=1
    return {'phase_curves':curves,'thresholds':(first,second),'intervals':intervals,
            'witnesses':witnesses,'joint_programs':64*81,'distinct_polynomials':len(candidates),
            'dominance_checks':count}


def phase_value(error):
    p=F(error)
    if not 0<=p<=F(1,2):raise ValueError('error probability')
    # Return the maximum, not a floating threshold comparison.
    curves=(((0,1,3),(50,58,58,42)),((0,0,3),(58,58,58,42)),
            ((0,0,0),(58,58,58,58)))
    return max(evaluate_witness(e,d,p) for e,d in curves)
