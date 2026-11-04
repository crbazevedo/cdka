"""v15: exact two-update interfaces and explicitly paid, faulty voting.

Same SERVICE-first plant/payoff as v13/v14. New register-regeneration
experiments have a separately declared physical grammar. Latent voter health
is never a runtime observation. Gate slots, bank maintenance operations and
writes are reported separately; they are not energy units.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from math import comb
from .faulty_updates import PhysicalCircuit, output_probabilities, task_weights
from .physical_update import bypass_value

BITS=tuple(product((0,1), repeat=3))
# Initial wires 0,1,2. Nodes 3..8. Distinguishes a=0 from exchangeable b,c.
VOTER=((0,1),(0,2),(1,2),(3,4),(6,6),(5,7))
SEQUENTIAL=PhysicalCircuit(((1,4),(2,5),(1,6),(3,7)),8)
PARALLEL=PhysicalCircuit(((1,4),(2,3),(1,6),(5,7)),8)


def probability(x, upper=F(1)):
    x=F(x)
    if not 0<=x<=upper: raise ValueError('probability outside declared range')
    return x


def add(row,key,value):
    if value: row[key]=row.get(key,F(0))+value


def execute_voter(bits,faults=(0,)*6):
    if tuple(bits) not in BITS or len(faults)!=6 or any(x not in (0,1) for x in faults):
        raise ValueError('three binary inputs and six physical fault flags required')
    wires=list(bits)
    for (a,b),error in zip(VOTER,faults):
        wires.append((1-(wires[a]&wires[b]))^error)
    return wires[-1]


@lru_cache(None)
def voter_profile():
    out=[]
    for bits in BITS:
        count=[0]*7
        for faults in product((0,1), repeat=6):
            count[sum(faults)]+=execute_voter(bits,faults)
        out.append(tuple(count))
    return tuple(out)


def voter_table(gamma):
    g=probability(gamma,F(1,2))
    return tuple(sum((F(n)*g**k*(1-g)**(6-k) for k,n in enumerate(row)),F(0))
                 for row in voter_profile())


def iid_vote_output(one_probability,voter_error):
    r=probability(one_probability)
    return sum((r**sum(bits)*(1-r)**(3-sum(bits))*v
                for bits,v in zip(BITS,voter_table(voter_error))),F(0))


def circuit_triplet_channel(circuit,gate_error,voter_error,shared=False):
    """Independent module faults conditional on the SAME received physical input.
    Shared=True instead fans out one physical result; no independent resampling.
    """
    outputs=output_probabilities(circuit,gate_error)
    v=voter_table(voter_error)
    if shared: return tuple((1-r)*v[0]+r*v[-1] for r in outputs)
    return tuple(iid_vote_output(r,voter_error) for r in outputs)


def task_value(channel,p=F(1,100),encoding=(3,0,0),procedure_failure=F(0)):
    if len(channel)!=8 or len(encoding)!=3 or any(c not in range(4) for c in encoding):
        raise ValueError('eight runtime inputs and three physical codewords required')
    weights,den,base=task_weights(F(p))
    value=base+sum((F(weights[4*y+encoding[y]][x],den)*channel[x]
                     for y in range(3) for x in range(8)),F(0))
    return (1-probability(procedure_failure))*value


def maintain_mix(good,bad,success):
    s=probability(success)
    return tuple(s*a+(1-s)*b for a,b in zip(good,bad))


def portfolio(p=F(1,100),gamma=F(1,50),healthy=F(1,1000),success=F(4,5)):
    """Exact comparison of declared architectures, NOT all circuits of 18 gates.

    A maintenance operation services ONE declared gate bank before reading:
    full 4-gate selector bank or full 6-gate voter bank. A successful operation
    puts that bank at healthy; otherwise it stays at gamma. Its result is hidden.
    Costs are (installed NANDs, maintenance-bank operations, retained outputs).
    Module banks are not all serviced for one token in the triplicated design.
    """
    p=probability(p,F(1,2));g=probability(gamma,F(1,2));v=probability(healthy,F(1,2));s=probability(success)
    single=output_probabilities(SEQUENTIAL,g)
    good_single=output_probabilities(SEQUENTIAL,v)
    trip=circuit_triplet_channel(SEQUENTIAL,g,g)
    good_trip=circuit_triplet_channel(SEQUENTIAL,g,v)
    maintained=maintain_mix(good_trip,trip,s)
    single_m=maintain_mix(good_single,single,s)
    specs=[('bypass',0,0,1,None),('single',4,0,1,single),
           ('single_maintained',4,1,1,single_m),
           ('triple',18,0,3,trip),('triple_voter_maintained',18,1,3,maintained),
           ('shared_output_voted',10,0,3,circuit_triplet_channel(SEQUENTIAL,g,g,True))]
    return tuple({'id':name,'nand_slots':gates,'bank_services':services,'ports':ports,
                  'value':bypass_value() if channel is None else task_value(channel,p),
                  'channel':channel} for name,gates,services,ports,channel in specs)


def voter_maintenance_threshold(p=F(1,100),gamma=F(1,50),healthy=F(1,1000)):
    bad=task_value(circuit_triplet_channel(SEQUENTIAL,gamma,gamma),p)
    good=task_value(circuit_triplet_channel(SEQUENTIAL,gamma,healthy),p)
    if good==bad:return None
    return (bypass_value()-bad)/(good-bad)


def raw_replica_vote(circuit,bits_input,gate_error,voter_error,shared=False):
    """Independent raw oracle for small modules, enumerates all physical flags.
    For a 1-gate module: 2^(3+6)=512 branches, not product of output marginals.
    """
    word,k=bits_input;g=F(gate_error);v=F(voter_error)
    copies=1 if shared else 3;out=F(0)
    for flags in product((0,1),repeat=copies*circuit.cost):
        w=g**sum(flags)*(1-g)**(len(flags)-sum(flags))
        values=[circuit.execute(word,k,flags[j*circuit.cost:(j+1)*circuit.cost]) for j in range(copies)]
        if shared:values*=3
        for vf in product((0,1),repeat=6):
            out+=w*v**sum(vf)*(1-v)**(6-sum(vf))*execute_voter(values,vf)
    return out


# Two successive physical register updates, independent of an agent belief.
# Z is a hidden substrate mode controlling current gate rates, not a readable bit.
STATES=tuple((z,bits) for z in (0,1) for bits in BITS)
RATE=(F(1,1000),F(1,50))
HEALTH=((F(19,20),F(1,20)),(F(0),F(1)))


def state_label(state, refined=True, latent=True):
    z,(a,b,c)=state
    label=(a,b+c) if refined else (a+b+c,)
    return (z,)+label if latent else label


@lru_cache(None)
def raw_update(state,mode='regenerate',write_error=F(1,50),symmetric=False):
    """Exact physical microkernel, explicit flags, no quotient used.
    'diffuse': independent bit faults. 'regenerate': six noisy NAND voter,
    broadcast its actual output and write three independently faulty cells.
    Symmetric=True substitutes an explicitly abstract majority+BSC operation.
    After either operation hidden health degrades by HEALTH.
    """
    z,bits=state;e=probability(write_error,F(1,2));row={}
    if mode=='diffuse':
        guesses=((bits,F(1)),)
    elif mode=='regenerate':
        guesses=[]
        if symmetric:
            m=int(sum(bits)>=2)
            guesses=[((m,m,m),1-RATE[z]),((1-m,)*3,RATE[z])]
        else:
            for faults in product((0,1),repeat=6):
                requested=execute_voter(bits,faults)
                w=RATE[z]**sum(faults)*(1-RATE[z])**(6-sum(faults))
                guesses.append(((requested,)*3,w))
    else: raise ValueError('unknown operation')
    for source,ps in guesses:
        for mask in BITS:
            prob=e**sum(mask)*(1-e)**(3-sum(mask))
            target=tuple(a^b for a,b in zip(source,mask))
            for z1,pz in enumerate(HEALTH[z]):add(row,(z1,target),ps*prob*pz)
    return row


@lru_cache(None)
def quotient_update(label,mode='regenerate',write_error=F(1,50),symmetric=False):
    """Independent algebraic construction using binomial convolutions.
    Actual voter: (Z,a,b+c), abstract symmetric primitive: (Z,a+b+c).
    """
    e=F(write_error);z=label[0];out={}
    if symmetric:
        count=label[1]; representative=(1,)*count+(0,)*(3-count)
    else:
        a,t=label[1:];representative=(a,1 if t>=1 else 0,1 if t==2 else 0)
    if mode=='regenerate':
        if symmetric:
            p1=RATE[z] if sum(representative)<2 else 1-RATE[z]
        else:p1=voter_table(RATE[z])[BITS.index(representative)]
        for bit,pbit in ((0,1-p1),(1,p1)):
            one=e if bit==0 else 1-e
            for z1,pz in enumerate(HEALTH[z]):
                if symmetric:
                    for k in range(4):add(out,(z1,k),pbit*pz*F(comb(3,k))*one**k*(1-one)**(3-k))
                else:
                    for a1 in (0,1):
                        pa=one if a1 else 1-one
                        for t1 in range(3):add(out,(z1,a1,t1),pbit*pz*pa*F(comb(2,t1))*one**t1*(1-one)**(2-t1))
    elif mode=='diffuse':
        def count_law(n,k):
            r={}
            for erased in range(k+1):
                for introduced in range(n-k+1):
                    p=F(comb(k,erased)*comb(n-k,introduced))*e**(erased+introduced)*(1-e)**(n-erased-introduced)
                    add(r,k-erased+introduced,p)
            return r
        for z1,pz in enumerate(HEALTH[z]):
            if symmetric:
                for k1,pk in count_law(3,label[1]).items():add(out,(z1,k1),pz*pk)
            else:
                a,t=label[1:]
                for a1,pa in ((a,1-e),(1-a,e)):
                    for t1,pt in count_law(2,t).items():add(out,(z1,a1,t1),pz*pa*pt)
    else:raise ValueError('unknown operation')
    return out


def aggregate(row,refined=True,latent=True):
    out={}
    for state,p in row.items():add(out,state_label(state,refined,latent),p)
    return out


def push(law,transition):
    out={}
    for state,p in law.items():
        for target,pt in transition(state).items():add(out,target,p*pt)
    return out


def tv(a,b):
    return sum((abs(a.get(k,F(0))-b.get(k,F(0))) for k in a.keys()|b.keys()),F(0))/2


def boundary_certificate():
    checked=0;two=0
    for symmetric in (False,True):
        for e in (F(0),F(1,50),F(1,5)):
            for state in STATES:
                label=state_label(state,not symmetric)
                for mode in ('diffuse','regenerate'):
                    raw=raw_update(state,mode,e,symmetric)
                    reduced=quotient_update(label,mode,e,symmetric)
                    assert aggregate(raw,not symmetric)==reduced
                    assert sum(raw.values(),F(0))==1
                    checked+=1
                for modes in product(('diffuse','regenerate'),repeat=2):
                    micro={state:F(1)};macro={label:F(1)}
                    for mode in modes:
                        micro=push(micro,lambda s:raw_update(s,mode,e,symmetric))
                        macro=push(macro,lambda s:quotient_update(s,mode,e,symmetric))
                    assert aggregate(micro,not symmetric)==macro
                    two+=1
    a=(1,(0,1,1));b=(1,(1,0,1))
    first=tv(aggregate(raw_update(a),False),aggregate(raw_update(b),False))
    second=tv(aggregate(push(raw_update(a),lambda s:raw_update(s)),False),
              aggregate(push(raw_update(b),lambda s:raw_update(s)),False))
    latent=tv(aggregate(raw_update((0,(0,0,0))),True,False),
              aggregate(raw_update((1,(0,0,0))),True,False))
    return {'micro_states':16,'abstract_symmetric_states':8,'actual_voter_states':12,
            'rows_verified':checked,'two_update_cases':two,
            'count_failure_one':first,'count_failure_two':second,'hidden_health_failure':latent}


def topology_gap(gamma):
    """P(1|011)-P(1|101), exact polynomial for the six-NAND voter."""
    g=probability(gamma,F(1,2))
    return 2*g*(1-g)*(1-2*g)**2


def signature_certificate():
    """Algebraic/evaluator statistics; not a newly readable latent health flag."""
    from .semantic_closure import matrix,close_continuations,refine_lumping
    result={};ix={s:i for i,s in enumerate(STATES)}
    for symmetric in (True,False):
        ops={mode:matrix([{ix[t]:p for t,p in raw_update(s,mode,symmetric=symmetric).items()}
                         for s in STATES]) for mode in ('diffuse','regenerate')}
        values=[(RATE[z] if sum(bits)<2 else 1-RATE[z]) if symmetric
                else voter_table(RATE[z])[BITS.index(bits)] for z,bits in STATES]
        closure=close_continuations(ops,{'mass':[1]*16,'readout':values})
        partition=refine_lumping(ops,values)
        assert closure.verify()
        result['abstract' if symmetric else 'physical']={
            'rank':closure.dimension,'profile':closure.profile,
            'classes':len(partition['blocks']),'refinement_history':partition['history'],
            'blocks':partition['blocks'],'witnesses':closure.witnesses,
            'candidate_evaluations':closure.attempts}
    return result


def voter_power_profile():
    """Exact coefficients in powers of gamma, via fault-count binomial expansion."""
    out=[]
    for row in voter_profile():
        power=[0]*7
        for k,n in enumerate(row):
            for j in range(7-k):power[k+j]+=n*comb(6-k,j)*(-1)**j
        out.append(tuple(power))
    return tuple(out)
