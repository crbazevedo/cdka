"""CDKA v14: exact physical continuation synthesis with fallible NAND gates.

No ideal truth-table quotient is used for intermediate circuits. Physical
nodes have unique IDs, so duplicate gates and fanout retain their actual
fault dependence. Only COMPLETED single-output conditional probability
polynomials are merged, where the task sees no other port. A separate joint
port-law routine demonstrates the stronger signature needed for extension.
Independent output flips of each gate have rate gamma; a common final latch
has independent error q. Initial encoding and physical task match v13.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import comb, lcm
from .physical_update import (INPUTS, payoff_table, transport_probability,
                              bypass_value, family_constants, analytical_value)

BASE = (0, 255, *INPUTS)


def error_probability(x):
    x = F(x)
    if not 0 <= x <= F(1,2):
        raise ValueError('error probability must be in [0,1/2]')
    return x


@dataclass(frozen=True)
class PhysicalCircuit:
    gates: tuple[tuple[int,int], ...] = ()
    output: int = 1

    def __post_init__(self):
        if any(not (0<=a<=b<5+i) for i,(a,b) in enumerate(self.gates)):
            raise ValueError('gates must be ordered causal NAND wire pairs')
        if not 0<=self.output<5+len(self.gates):
            raise ValueError('invalid physical output port')

    @property
    def cost(self): return len(self.gates)

    def all_truths(self, faults=()):
        if len(faults)!=self.cost or any(f not in (0,1) for f in faults):
            raise ValueError('one fault bit per gate required')
        wires=list(BASE)
        for (a,b),fault in zip(self.gates,faults):
            wires.append((255^(wires[a]&wires[b]))^(255 if fault else 0))
        return tuple(wires)

    def execute(self, word, syndrome, faults=None):
        if word not in range(4) or syndrome not in (0,1):
            raise ValueError('only physical received word and syndrome are inputs')
        if faults is None: faults=(0,)*self.cost
        return (self.all_truths(faults)[self.output]>>(2*word+syndrome))&1

    def fault_profile(self):
        """N[x,k] counts k-fault masks producing output1 for input x.

        P(1|x)=sum N[x,k] gamma^k (1-gamma)^(d-k). This is a terminal
        conditional channel, not a safe prefix signature when other ports
        remain accessible to later computation.
        """
        counts=[[0]*(self.cost+1) for _ in range(8)]
        for mask in range(1<<self.cost):
            truth=self.all_truths(tuple((mask>>i)&1 for i in range(self.cost)))[self.output]
            weight=mask.bit_count()
            for x in range(8): counts[x][weight]+=(truth>>x)&1
        return tuple(tuple(row) for row in counts)


def rooted(gates):
    if not gates: return False
    needed={4+len(gates)}
    for i in reversed(range(len(gates))):
        if 5+i in needed:
            needed.update(x for x in gates[i] if x>=5)
    return all(5+i in needed for i in range(len(gates)))


def rooted_netlists(depth):
    """Complete bounded grammar, with duplicate gates and shared fanout.

    Only gates not ancestral to the output are discarded; their independent
    faults cannot influence the output and they cost extra installation.
    """
    if type(depth) is not int or not 1<=depth<=4:
        raise ValueError('bounded exact grammar requires depth in 1..4')
    def visit(prefix):
        if len(prefix)==depth:
            if rooted(prefix): yield PhysicalCircuit(prefix,4+depth)
            return
        for pair in combinations_with_replacement(range(5+len(prefix)),2):
            yield from visit(prefix+(pair,))
    return visit(())


@lru_cache(None)
def complete_library(max_gates=4):
    if type(max_gates) is not int or not 0<=max_gates<=4:
        raise ValueError('gate capacity must be in 0..4')
    entries=[];statistics=[]
    for d in range(max_gates+1):
        circuits=(PhysicalCircuit((),i) for i in range(5)) if d==0 else rooted_netlists(d)
        representatives={};raw=0
        for c in circuits:
            raw+=1;key=c.fault_profile()
            representatives.setdefault(key,c)
        entries.extend((c,profile) for profile,c in representatives.items())
        statistics.append({'gates':d,'rooted_netlists':raw,'terminal_channels':len(representatives)})
    return tuple(entries),tuple(statistics)


def channel_numerators(profile,gamma):
    """One common exact denominator for a conditional output channel."""
    gamma=error_probability(gamma);d=len(profile[0])-1
    r,s=gamma.numerator,gamma.denominator
    weights=tuple(r**k*(s-r)**(d-k) for k in range(d+1))
    return tuple(sum(n*w for n,w in zip(row,weights)) for row in profile),s**d


def output_probabilities(circuit,gamma=F(0),q=F(0)):
    q=error_probability(q);n,den=channel_numerators(circuit.fault_profile(),gamma)
    return tuple(q+(1-2*q)*F(a,den) for a in n)


def joint_ports(circuit,ports,word,syndrome,gamma=F(1,10)):
    """Full joint boundary distribution conditional on actual readable input."""
    gamma=error_probability(gamma);ports=tuple(ports);x=2*word+syndrome
    if word not in range(4) or syndrome not in (0,1) or any(i not in range(5+circuit.cost) for i in ports):
        raise ValueError('invalid ports/readable input')
    result={}
    for mask in range(1<<circuit.cost):
        fault=tuple((mask>>i)&1 for i in range(circuit.cost))
        wires=circuit.all_truths(fault);out=tuple((wires[i]>>x)&1 for i in ports)
        p=gamma**sum(fault)*(1-gamma)**(circuit.cost-sum(fault))
        if p:result[out]=result.get(out,F(0))+p
    return result


def append_nand(law,pair,gamma):
    """Extend a full joint port law with a fresh independent faulty gate."""
    gamma=error_probability(gamma);out={};a,b=pair
    for values,p in law.items():
        requested=1-(values[a]&values[b])
        for error,weight in ((0,1-gamma),(1,gamma)):
            key=values+(requested^error,)
            if p*weight:out[key]=out.get(key,F(0))+p*weight
    return out


@lru_cache(None)
def task_weights(p):
    """Separability requires v13's equally priced independent encoder rows."""
    p=error_probability(p);T=payoff_table();rows=[]
    for y in range(3):
        for encoded in range(4):
            rows.append(tuple(transport_probability(encoded,x//2,p)*(T[y][x%2][1]-T[y][x%2][0]) for x in range(8)))
    den=lcm(*(z.denominator for row in rows for z in row))
    integer=tuple(tuple(int(z*den) for z in row) for row in rows)
    base=sum((T[y][k][0] for y in range(3) for k in range(2)),F(0))
    return integer,den,base


def evaluate(circuit,encoding,p=F(0),gamma=F(0),q=F(0)):
    if len(encoding)!=3 or any(e not in range(4) for e in encoding):
        raise ValueError('physical two-bit code for each of three diagnostics')
    rows,den,base=task_weights(p);h=output_probabilities(circuit,gamma,q)
    return base+sum((F(rows[4*y+encoding[y]][x],den)*h[x] for y in range(3) for x in range(8)),F(0))


def synthesize(p=F(1,100),gamma=F(0),q=F(0),capacity=4):
    p=error_probability(p);gamma=error_probability(gamma);q=error_probability(q)
    rows,task_den,base=task_weights(p)
    entries,profile=complete_library(capacity);best=None
    for circuit,law in entries:
        nums,den=channel_numerators(law,gamma)
        qn,qd=q.numerator,q.denominator
        nums=tuple(qn*den+(qd-2*qn)*a for a in nums);den*=qd
        subtotal=0;encoding=[]
        for y in range(3):
            scores=[sum(a*b for a,b in zip(rows[4*y+code],nums)) for code in range(4)]
            winner=max(range(4),key=lambda code:(scores[code],-code))
            subtotal+=scores[winner];encoding.append(winner)
        value=base+F(subtotal,task_den*den)
        key=(value,-circuit.cost,tuple(-e for e in encoding),tuple((-a,-b) for a,b in circuit.gates),-circuit.output)
        if best is None or key>best[0]:best=(key,circuit,tuple(encoding))
    key,circuit,encoding=best;baseline=bypass_value()
    return {'value':max(baseline,key[0]),'update_value':key[0],
            'uses_bypass':baseline>=key[0],'baseline':baseline,
            'encoding':encoding,'circuit':circuit,'capacity':capacity,
            'p':p,'gamma':gamma,'q':q,'library_profile':profile}


def last_gate_bound(p,gamma,q=F(0)):
    """Upper bound for ANY single-output DAG with fresh independent last fault.

    Relax upstream to any Boolean table and best equally priced encoding.
    Additional outputs/voting/correlated faults change this contract.
    """
    p=error_probability(p);gamma=error_probability(gamma);q=error_probability(q)
    effective=gamma+q-2*gamma*q
    return analytical_value(p,effective,4)


def last_gate_cutoff(p):
    p=error_probability(p);a,b,D=family_constants()
    gain=max(F(0),a*(1-p)**2-b*p*p)
    return gain/(D+2*gain) if gain else F(0)


def shared_fault_witness(gamma=F(1,10)):
    shared=PhysicalCircuit(((0,0),(5,5)),6)
    separate=PhysicalCircuit(((0,0),(0,0),(5,6)),7)
    g=error_probability(gamma)
    a=joint_ports(shared,(5,5),0,0,g);b=joint_ports(separate,(5,6),0,0,g)
    marg=lambda law:tuple(sum((mass for bits,mass in law.items() if bits[j]),F(0)) for j in range(2))
    return {'shared_circuit':shared,'separate_circuit':separate,
            'shared_joint':a,'separate_joint':b,
            'shared_marginals':marg(a),'separate_marginals':marg(b),
            'shared_output_error':output_probabilities(shared,g)[0],
            'separate_output_error':output_probabilities(separate,g)[0],
            'shared_formula':2*g*(1-g),'separate_formula':g+(1-2*g)*(2*g-g*g)}


def runtime_fault_traces(circuit,word,syndrome,gamma):
    """Complete conditional physical traces, not samples or agent thoughts."""
    g=error_probability(gamma);rows=[]
    for mask in range(1<<circuit.cost):
        e=tuple((mask>>i)&1 for i in range(circuit.cost));weight=g**sum(e)*(1-g)**(circuit.cost-sum(e))
        vals=tuple((t>>(2*word+syndrome))&1 for t in circuit.all_truths(e))
        rows.append({'input':(word,syndrome),'faults':e,'probability':weight,'wires':vals,
                     'output':vals[circuit.output],'command':('hold','refresh')[vals[circuit.output]]})
    return tuple(rows)


def power_channel(profile):
    """Exact integer coefficients of output probability, powers of gamma."""
    d=len(profile[0])-1;rows=[]
    for counts in profile:
        a=[0]*5
        for k,count in enumerate(counts):
            for j in range(d-k+1):
                a[k+j]+=count*comb(d-k,j)*(-1)**j
        rows.append(tuple(a))
    return tuple(rows)


@lru_cache(None)
def program_polynomials(p=F(1,100),capacity=4):
    """All64 encoders, all completed channels, exact polynomial values."""
    p=error_probability(p);weights,den,base=task_weights(p)
    final_den=lcm(den,base.denominator,bypass_value().denominator)
    weights=tuple(tuple(x*(final_den//den) for x in row) for row in weights)
    entries={};raw_programs=0
    for c,profile in complete_library(capacity)[0]:
        rows=power_channel(profile);local=[]
        for w in weights:
            local.append(tuple(sum(w[x]*rows[x][j] for x in range(8)) for j in range(5)))
        for encoding in product(range(4),repeat=3):
            coeff=list(sum((local[4*y+encoding[y]][j] for y in range(3)),0) for j in range(5))
            coeff[0]+=int(base*final_den);coeff=tuple(coeff)
            entries.setdefault(coeff,(encoding,c));raw_programs+=1
    bypass=(int(bypass_value()*final_den),0,0,0,0)
    entries.setdefault(bypass,(None,None))
    return entries,final_den,raw_programs


def bernstein_coefficients(power,left,right):
    """Exact Bernstein coefficients after mapping [left,right] to [0,1]."""
    left=F(left);right=F(right)
    if right<left:raise ValueError('ordered interval required')
    d=len(power)-1;local=[]
    for j in range(d+1):
        local.append(sum((F(power[k])*comb(k,j)*left**(k-j)*(right-left)**j for k in range(j,d+1)),F(0)))
    return tuple(sum((local[j]*F(comb(i,j),comb(d,j)) for j in range(i+1)),F(0)) for i in range(d+1))


def prove_nonnegative(power,left,right,max_depth=12):
    """Sufficient exact interval certificate; unresolved is NOT a falsifier."""
    nodes=0
    def prove(a,b,depth):
        nonlocal nodes
        coeff=bernstein_coefficients(power,a,b)
        if min(coeff)>=0:nodes+=1;return
        if depth==0:raise ValueError('Bernstein certificate unresolved at depth limit')
        mid=(a+b)/2;prove(a,mid,depth-1);prove(mid,b,depth-1)
    prove(F(left),F(right),max_depth)
    return nodes


def fixed_input_certificate():
    """Global capacity4 optimum at p=.01, gamma∈[0,.01]; not a 2D claim."""
    p=F(1,100);left=F(0);right=F(1,100)
    candidate=PhysicalCircuit(((1,4),(2,5),(1,6),(3,7)),8);encoding=(3,0,0)
    polys,den,program_count=program_polynomials(p,4)
    weights,wden,base=task_weights(p);scale=den//wden
    cp=power_channel(candidate.fault_profile())
    winner=[sum(weights[4*y+encoding[y]][x]*scale*cp[x][j] for y in range(3) for x in range(8)) for j in range(5)]
    winner[0]+=int(base*den);winner=tuple(winner)
    if winner not in polys:raise AssertionError('attaining circuit absent from grammar')
    leaves=0
    for rival in polys:
        diff=tuple(a-b for a,b in zip(winner,rival))
        leaves+=prove_nonnegative(diff,left,right)
    return {'p':p,'gamma_interval':(left,right),'capacity':4,
            'circuit':candidate,'encoding':encoding,
            'rational_power_coefficients':tuple(F(x,den) for x in winner),
            'programs_checked':program_count,'distinct_polynomials':len(polys),
            'certified_leaves':leaves,'output_q_extension':'common affine transform for any q<=1/2, then compare bypass'}


def fixed_fault_value(circuit,encoding,p,faults):
    """Freeze one gate-fault mask; average the other declared task events."""
    w,den,base=task_weights(p)
    truth=circuit.all_truths(tuple(faults))[circuit.output]
    return base+sum((F(w[4*y+encoding[y]][x],den)*((truth>>x)&1)
                     for y in range(3) for x in range(8)),F(0))


def first_order_influences(circuit,encoding,p=F(1,100)):
    base=fixed_fault_value(circuit,encoding,p,(0,)*circuit.cost);rows=[]
    for i in range(circuit.cost):
        faults=tuple(int(j==i) for j in range(circuit.cost))
        altered=fixed_fault_value(circuit,encoding,p,faults)
        rows.append({'gate':i,'value_if_only_this_gate_flips':altered,'signed_effect':altered-base})
    return {'fault_free_value':base,'gates':tuple(rows),
            'uniform_noise_derivative_at_zero':sum((r['signed_effect'] for r in rows),F(0))}
