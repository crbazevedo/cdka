"""Certified dominance of complete-program families on a reachable contrast cone.

A response q dominates r when q<=r componentwise: the preparation's signed
four coordinates are nonpositive, so its physical value is larger for q.
D/R preserve this order because their exact contrast transports are nonnegative.
M is handled only by a checked 4-by-16 boundary map applied to a FULL sixteen
coordinate suffix response; it is never treated as a four-state transition.

The recursive cover retains one optimum and decision feasibility under the
common reserved resource box. It does not retain every response, every tied
optimum, or physical execution-cost Pareto tradeoffs. Physical kernels, source
acquisition, and preparation generation are supplied by the inherited model.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from .reachable_restriction import CONTRAST_BASIS, collapse, expand_contrast, contrast_response
from .semantic_closure import push, apply, dot
from .reachable_restriction import contrast_value

SCHEMA='cdka.positive-contrast-program-cover/v1'


def _rational(value):
    """Exact canonical values only; float and bool are never rationals here."""
    if type(value) is F:
        return value
    if type(value) is int:
        return F(value)
    if type(value) is str:
        try:
            result=F(value)
        except (ValueError, ZeroDivisionError) as error:
            raise ValueError('invalid exact rational') from error
        if str(result)!=value:
            raise ValueError('noncanonical exact rational')
        return result
    raise ValueError('exact rational required; float/bool forbidden')


def _exact(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):_exact(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [_exact(v) for v in value]
    return value

def binding(operators, terminal, k):
    value={'operators':operators,'terminal':terminal,'ordinary_updates':k,
           'grammar':'exactly k D/R updates, at most one additional M',
           'domain':'negative nonnegative cone in CONTRAST_BASIS; same mass offset per preparation'}
    return sha256(json.dumps(_exact(value),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def transports(operators):
    A={}
    for a in ('D','R'):
        rows=[]
        for v in CONTRAST_BASIS:
            masses=collapse(push(v,operators[a]))
            rows.append(tuple(masses[j] for j in (0,1,4,5)))
        A[a]=tuple(rows)
    A['M_boundary']=tuple(push(v,operators['M']) for v in CONTRAST_BASIS)
    verify_transports(A,operators)
    return A

def verify_transports(A, operators):
    if set(A)!=set(('D','R','M_boundary')): raise ValueError('transports')
    for a in ('D','R'):
        if len(A[a])!=4 or any(len(row)!=4 for row in A[a]): raise ValueError('transport shape')
        for e,row in zip(CONTRAST_BASIS,A[a]):
            if any(x<0 for x in row): raise ValueError('positive cone not invariant')
            if expand_contrast(row)!=push(e,operators[a]): raise ValueError('transport identity')
    if len(A['M_boundary'])!=4 or any(len(row)!=16 for row in A['M_boundary']):
        raise ValueError('maintenance bridge shape')
    for e,row in zip(CONTRAST_BASIS,A['M_boundary']):
        if tuple(row)!=push(e,operators['M']): raise ValueError('maintenance bridge identity')
    return True

def transport(A,r):
    return tuple(dot(row,r) for row in A)

def dominated(q,r):
    """q is at least as good as r on all signatures with signed4<=0."""
    return all(a<=b for a,b in zip(q,r))

def _cover(candidates,prune=True):
    if not prune:
        n=len(candidates)
        return candidates,{'keep':list(range(n)),'cover':list(range(n))}
    keep=[]
    for i,(_,q) in enumerate(candidates):
        if any(dominated(candidates[j][1],q) for j in keep): continue
        keep=[j for j in keep if not dominated(q,candidates[j][1])]
        keep.append(i)
    # Supply witnesses against the final retained frontier, not removed nodes.
    witness=[next(i for i,j in enumerate(keep) if dominated(candidates[j][1],q))
             for _,q in candidates]
    return [candidates[j] for j in keep],{'keep':keep,'cover':witness}

def _check_cover(candidates,level):
    keep,cover=level['keep'],level['cover']
    if (not isinstance(keep,list) or not keep or len(set(keep))!=len(keep) or
        any(type(j) is not int or not 0<=j<len(candidates) for j in keep)):
        raise ValueError('kept indices')
    if (not isinstance(cover,list) or len(cover)!=len(candidates) or
        any(type(j) is not int or not 0<=j<len(keep) for j in cover)):
        raise ValueError('cover indices')
    retained=[candidates[j] for j in keep]
    for (_,candidate),representative in zip(candidates,cover):
        if not dominated(retained[representative][1],candidate): raise ValueError('false dominance')
    return retained

def _candidates(n,S0,frontier,operators,g,A):
    seeds=[('M'+w,transport(A['M_boundary'],q)) for w,q in S0]
    if n==0: return [('',contrast_response(g))]+seeds
    return [(a+w,transport(A[a],r)) for w,r in frontier for a in ('D','R')]+seeds

def compile_family(operators,g,k,*,prune=True):
    if type(k) is not int or k<0: raise ValueError('ordinary updates')
    if type(prune) is not bool: raise ValueError('pruning flag')
    if len(g)!=16: raise ValueError('sixteen-coordinate terminal required')
    A=transports(operators)
    S0=[('',g)];frontier=[];layers=[];stats=[]
    for n in range(k+1):
        if n: S0=[(a+w,apply(operators[a],q)) for w,q in S0 for a in ('D','R')]
        candidates=_candidates(n,S0,frontier,operators,g,A)
        frontier,level=_cover(candidates,prune)
        layers.append(level)
        evaluated={w for w,_ in candidates}|{w for w,_ in S0}
        stats.append({'n':n,'no_m_suffixes':len(S0),'candidates':len(candidates),
                      'retained':len(frontier),'complete_words_generated':len(evaluated),
                      'complete_words_never_generated':(n+2)*2**n-len(evaluated)})
    cert={'schema':SCHEMA,'ordinary_updates':k,'binding':binding(operators,g,k),
          'transports':_exact(A),'layers':layers}
    return frontier,cert,stats

def _check_family(certificate,operators,g,k):
    if type(certificate) is not dict: raise ValueError('certificate object')
    if type(k) is not int or k<0: raise ValueError('ordinary updates')
    if (certificate['schema']!=SCHEMA or type(certificate['ordinary_updates']) is not int or
            certificate['ordinary_updates']!=k):
        raise ValueError('contract')
    if len(g)!=16: raise ValueError('sixteen-coordinate terminal required')
    if certificate['binding']!=binding(operators,g,k): raise ValueError('binding')
    supplied=certificate['transports']
    if type(supplied) is not dict or set(supplied)!=set(('D','R','M_boundary')):
        raise ValueError('transports')
    A={}
    for a,rows in supplied.items():
        width=16 if a=='M_boundary' else 4
        if (type(rows) is not list or len(rows)!=4 or
                any(type(row) is not list or len(row)!=width for row in rows)):
            raise ValueError('transport shape')
        A[a]=tuple(tuple(map(_rational,row)) for row in rows)
    verify_transports(A,operators)
    levels=certificate['layers']
    if type(levels) is not list or len(levels)!=k+1: raise ValueError('layers')
    S0=[('',g)];frontier=[]
    for n,level in enumerate(levels):
        if type(level) is not dict or set(level)!=set(('keep','cover')):
            raise ValueError('cover layer')
        if n: S0=[(a+w,apply(operators[a],q)) for w,q in S0 for a in ('D','R')]
        candidates=_candidates(n,S0,frontier,operators,g,A)
        frontier=_check_cover(candidates,level)
    return frontier

def check_family(certificate,operators,g,k):
    """Verify a supplied inductive cover without discovering a Pareto frontier."""
    try:
        return _check_family(certificate,operators,g,k)
    except (KeyError,TypeError,IndexError,ZeroDivisionError,AttributeError) as error:
        raise ValueError('malformed program-family certificate') from error


def unpruned_shared(operators,g,k):
    """Primary ablation: identical full16 suffix/4D prefix algebra, no pruning."""
    if type(k) is not int or k<0: raise ValueError('ordinary updates')
    A=transports(operators)
    S0=[('',g)];frontier=[]
    for n in range(k+1):
        if n: S0=[(a+w,apply(operators[a],q)) for w,q in S0 for a in ('D','R')]
        frontier=_candidates(n,S0,frontier,operators,g,A)
    return frontier

def evaluate_frontier(frontier,signatures):
    """Evaluate only signatures within the certified sign cone.

    Signature construction/physical reachability remain the caller's obligation.
    Values use an arbitrary common-per-preparation offset, which cancels from
    comparisons of complete programs. The current acquisition has offset1/2.
    """
    checked=[]
    for offset,signed in signatures:
        signed=tuple(map(_rational,signed))
        if len(signed)!=4 or any(x>0 for x in signed):
            raise ValueError('preparation outside certified negative contrast cone')
        checked.append((_rational(offset),signed))
    if not checked or not frontier: raise ValueError('nonempty problem required')
    if any(len(q)!=4 for _,q in frontier): raise ValueError('four-coordinate response required')
    responses=[tuple(map(_rational,q)) for _,q in frontier]
    return tuple(tuple(contrast_value(s,q) for q in responses) for s in checked)

def _values(values):
    values=tuple(tuple(map(_rational,row)) for row in values)
    if not values or not values[0] or any(len(row)!=len(values[0]) for row in values):
        raise ValueError('nonempty rectangular values')
    return values

def _identity_binding(values,preparation_labels,plan_labels,contract):
    payload={'values':_exact(values),'preparations':list(preparation_labels),
             'plans':list(plan_labels),'contract':_exact(contract)}
    return sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def _labels(values,preparation_labels,plan_labels):
    if (any(type(label) is not str or not label for label in preparation_labels) or
        any(type(label) is not str or not label for label in plan_labels) or
        len(preparation_labels)!=len(values) or len(plan_labels)!=len(values[0]) or
        len(set(preparation_labels))!=len(preparation_labels) or len(set(plan_labels))!=len(plan_labels)):
        raise ValueError('ordered labels')

def compile_decision(values,*,preparation_labels,plan_labels,contract=None):
    """Compact proof of informed values, one minimax and one maximin plan.

    This does not publish or preserve every response, prediction radius, tied
    optimum, or per-plan regret. Exact matrix entries, ordered identities and
    scope are bound by a digest. Numerical correctness is checked separately by
    supplied inequality witnesses. Physical evaluation must have been verified
    independently.
    """
    values=_values(values);_labels(values,preparation_labels,plan_labels)
    n=len(values[0]);h=len(values)
    best_indices=[max(range(n),key=lambda j:row[j]) for row in values]
    best=[row[j] for row,j in zip(values,best_indices)]
    regret_witness=[max(range(h),key=lambda i:best[i]-values[i][j]) for j in range(n)]
    regrets=[best[i]-values[i][j] for j,i in enumerate(regret_witness)]
    minimum_witness=[min(range(h),key=lambda i:values[i][j]) for j in range(n)]
    minima=[values[i][j] for j,i in enumerate(minimum_witness)]
    chosen=min(range(n),key=lambda j:regrets[j])
    maximin=max(range(n),key=lambda j:minima[j])
    return {'schema':'cdka.compact-program-decision/v1',
            'binding':_identity_binding(values,preparation_labels,plan_labels,contract),
            'preparation_best':[str(v) for v in best],'preparation_best_plans':best_indices,
            'minimax_plan':chosen,'minimax_regret':str(regrets[chosen]),
            'regret_lower_witness':regret_witness,
            'maximin_plan':maximin,'maximin_fidelity':str(minima[maximin]),
            'fidelity_upper_witness':minimum_witness}

def _check_decision(certificate,values,*,preparation_labels,plan_labels,contract=None):
    """Check supplied optimum witnesses without searching for optima."""
    values=_values(values);_labels(values,preparation_labels,plan_labels)
    if type(certificate) is not dict: raise ValueError('decision certificate object')
    c=certificate;h=len(values);n=len(values[0])
    if c['schema']!='cdka.compact-program-decision/v1': raise ValueError('decision schema')
    if c['binding']!=_identity_binding(values,preparation_labels,plan_labels,contract): raise ValueError('decision binding')
    if type(c['preparation_best']) is not list: raise ValueError('informed value vector')
    best=tuple(map(_rational,c['preparation_best']));attainers=c['preparation_best_plans']
    def indices(xs,count,upper):
        return type(xs) is list and len(xs)==count and all(type(i) is int and 0<=i<upper for i in xs)
    if len(best)!=h or not indices(attainers,h,n): raise ValueError('informed witnesses')
    for row,b,j in zip(values,best,attainers):
        if row[j]!=b or any(v>b for v in row): raise ValueError('informed upper bound')
    p=c['minimax_plan'];r=_rational(c['minimax_regret']);rw=c['regret_lower_witness']
    if not indices([p],1,n) or not indices(rw,n,h): raise ValueError('regret witnesses')
    if any(best[i]-row[p]>r for i,row in enumerate(values)): raise ValueError('minimax upper bound')
    if any(best[i]-values[i][j]<r for j,i in enumerate(rw)): raise ValueError('minimax lower bound')
    p=c['maximin_plan'];v=_rational(c['maximin_fidelity']);fw=c['fidelity_upper_witness']
    if not indices([p],1,n) or not indices(fw,n,h): raise ValueError('fidelity witnesses')
    if any(row[p]<v for row in values): raise ValueError('maximin lower bound')
    if any(values[i][j]>v for j,i in enumerate(fw)): raise ValueError('maximin upper bound')
    return True


def check_decision(certificate,values,*,preparation_labels,plan_labels,contract=None):
    """Validate compact decision witnesses, rejecting malformed certificate data."""
    try:
        return _check_decision(certificate,values,
            preparation_labels=preparation_labels,plan_labels=plan_labels,contract=contract)
    except (KeyError,TypeError,IndexError,ZeroDivisionError,AttributeError) as error:
        raise ValueError('malformed program-decision certificate') from error
