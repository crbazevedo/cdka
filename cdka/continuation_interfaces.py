"""CDKA v9: finite physical continuation interfaces, not a new POMDP theorem.

We retain the v6 kernel. A finite diagnostic Y is encoded BEFORE any action.
Only the physical code, readable (syndrome, resource), and stage clock are
available afterward. H is never a runtime policy argument. This module
prices representational capacity as a number of distinguishable code states,
NOT joules or circuit cost. Code retention and the decoder library are
explicit idealizations. All mathematical reference values use Fraction.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from typing import Hashable, Mapping, Sequence
from .composition import Contract, DEAD, macro_row, micro_row


@dataclass(frozen=True)
class Plan:
    first: str
    second: tuple  # ((readable (k,b), physical action), ...)
    alpha: tuple  # P(alive at deadline | initial H=healthy/degraded)

    def action_after(self, observation):
        return dict(self.second)[observation]


def survival(p, s, a):
    return F(1)-macro_row(p,s,a)[DEAD]


@lru_cache(None)
def plans(p=Contract(), k=0, b=4, horizon=2):
    """Enumerate ALL deterministic two-stage physical policy trees.

    At the second epoch the policy may read fresh (k,b), not H. Its tree
    identity is represented by the initial physical code, not free history.
    For two epochs retaining that code is sufficient; no posterior is passed
    to runtime. Every first action and affordable second-stage truth table
    is included. One-stage plans are included for the horizon counterexample.
    """
    if horizon not in (1,2) or k not in (0,1) or b not in range(p.capacity+1):
        raise ValueError('one/two epochs, a readable syndrome and affordable budget required')
    answer=[]
    for action in p.actions(b):
        rows=[macro_row(p,(k,h,b),action) for h in (0,1)]
        if horizon==1:
            answer.append(Plan(action,(),tuple(1-row[DEAD] for row in rows)))
            continue
        observed=sorted({(s[0],s[2]) for row in rows for s,mass in row.items()
                         if s!=DEAD and mass>0})
        for commands in product(*(p.actions(ob[1]) for ob in observed)):
            continuation=dict(zip(observed,commands))
            alpha=tuple(sum((mass*survival(p,s,continuation[s[0],s[2]])
                             for s,mass in row.items() if s!=DEAD),F(0))
                        for row in rows)
            answer.append(Plan(action,tuple(zip(observed,commands)),alpha))
    return tuple(answer)


def micro_alpha(p, plan, k=0, b=4):
    """Independent oracle: raw three-cell masks, not quotient propagation."""
    register=(0,0,0) if k==0 else (1,0,0)
    result=[]
    for health in (0,1):
        initial=(0,register,health,b)  # global bit-complement symmetry
        first=micro_row(p,initial,plan.first)
        if not plan.second:
            result.append(1-first[DEAD]);continue
        total=F(0)
        for state,mass in first.items():
            if state==DEAD:continue
            w,cells,h1,b1=state
            readable=(int(sum(cells) not in (0,3)),b1)
            action=plan.action_after(readable)
            total+=mass*(1-micro_row(p,state,action)[DEAD])
        result.append(total)
    return tuple(result)


def score(plan, prob_healthy):
    t=F(prob_healthy)
    if not 0<=t<=1:raise ValueError('probability')
    return t*plan.alpha[0]+(1-t)*plan.alpha[1]


def upper_envelope(library):
    """Exact upper hull on the design-time health-prior line [0,1].

    Each alpha is an affine survival function. Duplicate slopes keep only
    their largest intercept. Rational intersections certify the CONTINUOUS
    envelope; no grid is used to claim a switching threshold.
    """
    best_slope={}
    for i,plan in enumerate(library):
        a,b=plan.alpha[0]-plan.alpha[1],plan.alpha[1]
        if a not in best_slope or b>best_slope[a][0]:best_slope[a]=(b,i)
    hull=[]  # (slope, intercept, index, start; None means -infinity)
    for a,(b,i) in sorted(best_slope.items()):
        start=None
        while hull:
            a0,b0,_,s0=hull[-1]
            start=(b0-b)/(a-a0)
            if s0 is None or start>s0:break
            hull.pop()
        hull.append((a,b,i,start if hull else None))
    segments=[]
    for j,(_,_,i,left) in enumerate(hull):
        right=hull[j+1][3] if j+1<len(hull) else None
        lo=max(F(0),left) if left is not None else F(0)
        hi=min(F(1),right) if right is not None else F(1)
        if lo<hi:segments.append((lo,hi,i))
    return tuple(segments)


def equal_signal_joint(tail=F(1,100)):
    """A three-outcome diagnostic, NOT a free observation of true health.

    All Y have weight 1/3 and healthy posteriors tail, 1/2, 1-tail.
    Consequently prior P(H=healthy)=1/2 for every tail. This specifies a
    generative sensor: P(Y=y|H=h)=2*joint[y][h]. Diagnosis acquisition costs
    are common/sunk in this comparison; available balance starts at b.
    """
    tail=F(tail)
    if not 0<=tail<=F(1,2):raise ValueError('tail in [0,1/2]')
    return tuple((x/3,(1-x)/3) for x in (tail,F(1,2),1-tail))


def validate_joint(joint):
    result=tuple(tuple(F(v) for v in row) for row in joint)
    if not result or any(len(row)!=2 or any(v<0 for v in row) for row in result):
        raise ValueError('nonempty binary-health nonnegative live masses required')
    if sum((sum(row,F(0)) for row in result),F(0))>1:
        raise ValueError('live mass above one')
    return result


def weighted_table(library, joint):
    joint=validate_joint(joint)
    return tuple(tuple(mu[0]*pi.alpha[0]+mu[1]*pi.alpha[1] for pi in library)
                 for mu in joint)


def partitions(n, max_codes=None):
    """Restricted-growth encodings; exact set partitions without relabeling."""
    if type(n)is not int or n<1:raise ValueError('positive signal count')
    if max_codes is None:max_codes=n
    if type(max_codes)is not int or max_codes<1:raise ValueError('positive code count')
    def visit(prefix,highest):
        if len(prefix)==n:
            yield tuple(prefix);return
        for c in range(min(highest+1,max_codes-1)+1):
            yield from visit(prefix+[c],max(highest,c))
    yield from visit([0],0)


def evaluate_code(library, joint, labels):
    """Optimal decoder for each physical code; shared continuation in a cell.

    This assumes an installed decoder library can realize the complete
    map from code to plan and the code persists to epoch two. Coupled
    circuit constraints require optimizing over that smaller global map set.
    """
    table=weighted_table(library,joint);labels=tuple(labels)
    if not library or len(labels)!=len(table):raise ValueError('code length/library')
    choices={};value=F(0)
    for label in dict.fromkeys(labels):
        scores=[sum((table[y][j] for y in range(len(table)) if labels[y]==label),F(0))
                for j in range(len(library))]
        winner=max(range(len(library)),key=lambda j:scores[j])
        choices[label]=winner;value+=scores[winner]
    full=sum((max(row) for row in table),F(0))
    return {'value':value,'full':full,'loss':full-value,
            'labels':labels,'plans':choices,'codes':len(choices)}


def lossless_witness(library,joint,labels):
    """Exact common-maximizer certificate, including ties and zero mass."""
    table=weighted_table(library,joint);out={};bad={}
    if len(labels)!=len(table):raise ValueError('length')
    for label in dict.fromkeys(labels):
        members=[y for y,z in enumerate(labels) if z==label]
        common=set(range(len(library)))
        for y in members:
            maximum=max(table[y]);common&={j for j,v in enumerate(table[y]) if v==maximum}
        if common:out[label]=min(common)
        else:bad[label]=tuple(members)
    return {'lossless':not bad,'common_plans':out,'conflicting_cells':bad}


def best_code(library,joint,capacity):
    if type(capacity)is not int or capacity<1:raise ValueError('positive capacity')
    best=None
    for labels in partitions(len(joint),capacity):
        current=evaluate_code(library,joint,labels)
        if best is None or current['value']>best['value']:best=current
    return best


def exact_code_count(library,joint):
    for capacity in range(1,len(joint)+1):
        if best_code(library,joint,capacity)['loss']==0:return capacity
    raise AssertionError('full diagnostic code failed')


def transported_code_value(library,joint,labels,rho):
    """Flagged erasure BEFORE plan selection, independent of hidden health.

    No state drift, action, or resource differences across this calibration
    arm. The erasure flag is an additional readable physical symbol.
    Unflagged corruption/selector failure requires the full joint oracle.
    """
    rho=F(rho)
    if not 0<=rho<=1:raise ValueError('erasure probability')
    encoded=evaluate_code(library,joint,labels)['value']
    baseline=evaluate_code(library,joint,(0,)*len(joint))['value']
    return (1-rho)*encoded+rho*baseline


def regret_breakdown(p,library,joint,encoding,k=0,b=4):
    """Exact two-stage Bellman residual identity under ACTUAL live mass.

    The reference remembers Y and all physical observations but never H.
    This is an explicitly stronger finite memory architecture, not oracle
    health. Separate root action loss from continuation-decoder loss.
    """
    if any(not pi.second for pi in library):raise ValueError('two-stage library required')
    table=weighted_table(library,joint);root=F(0);tail=F(0);by_signal=[]
    for y,mu in enumerate(validate_joint(joint)):
        pi=library[encoding['plans'][encoding['labels'][y]]]
        full=max(table[y])
        best_root=max(table[y][j] for j,x in enumerate(library) if x.first==pi.first)
        initial=full-best_root
        grouped={}
        for h in (0,1):
            for s,mass in macro_row(p,(k,h,b),pi.first).items():
                if s==DEAD:continue
                obs=(s[0],s[2]);arr=grouped.setdefault(obs,[F(0),F(0)])
                arr[s[1]]+=mu[h]*mass
        suffix=F(0)
        for (k1,b1),mass in grouped.items():
            scores={a:sum((mass[h]*survival(p,(k1,h,b1),a) for h in (0,1)),F(0))
                    for a in p.actions(b1)}
            suffix+=max(scores.values())-scores[pi.action_after((k1,b1))]
        actual=table[y][encoding['plans'][encoding['labels'][y]]]
        assert initial+suffix==full-actual
        root+=initial;tail+=suffix;by_signal.append((initial,suffix))
    assert root+tail==encoding['loss']
    return {'initial_action_loss':root,'continuation_loss':tail,'total':root+tail,
            'by_signal':tuple(by_signal)}


def update_witness(current_codes:Mapping,next_codes:Mapping,edges:Sequence):
    """Can a desired next code be computed from (current code, action, signal)?

    Edges are (history,action,NEW readable signal,next_history). Histories
    are design-time names, never runtime data. This is a deterministic
    congruence check; affordability/library membership is a separate gate.
    """
    table={};source={}
    for history,action,signal,next_history in edges:
        key=(current_codes[history],action,signal);target=next_codes[next_history]
        if key in table and table[key]!=target:
            return {'realizable':False,'conflict':(source[key],(history,action,signal,next_history)),
                    'shared_input':key,'required_outputs':(table[key],target)}
        table[key]=target;source[key]=(history,action,signal,next_history)
    return {'realizable':True,'table':table}
