"""CDKA v12: exact constructive continuation closure and falsifiable quotients.

Finite substochastic operators act on column observables; lost mass is death.
The basis is a design-time certificate, NOT a free runtime memory or posterior.
Observation masks must be included to certify observation-contingent control.
Classical Krylov/weighted-automata instruments are adapted to physical task,
policy-interface, resource and witness contracts. Exact Fraction arithmetic.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from collections import deque
from itertools import product
from typing import Mapping, Iterable

Vector = tuple[F, ...]
Matrix = tuple[dict[int, F], ...]


def vector(values):
    return tuple(map(F, values))


def matrix(rows):
    n = len(rows)
    result = tuple({int(j): F(x) for j, x in row.items() if x} for row in rows)
    for row in result:
        if any(j < 0 or j >= n or x < 0 for j, x in row.items()):
            raise ValueError('nonnegative square finite kernel required')
        if sum(row.values(), F(0)) > 1:
            raise ValueError('row mass must not exceed one')
    return result


def apply(q: Matrix, v: Vector) -> Vector:
    if len(q) != len(v):
        raise ValueError('dimensions differ')
    return tuple(sum((p*v[j] for j, p in row.items()), F(0)) for row in q)


def push(mu: Vector, q: Matrix) -> Vector:
    result = [F(0)] * len(mu)
    for i, p in enumerate(mu):
        for j, value in q[i].items():
            result[j] += p*value
    return tuple(result)


def dot(u, v):
    return sum((a*b for a, b in zip(u, v)), F(0))


def word_value(operators, word, terminal):
    """Q_word g, where word is in physical chronological order."""
    result = vector(terminal)
    for label in reversed(tuple(word)):
        result = apply(operators[label], result)
    return result


class ExactBasis:
    """Incremental row echelon with representations in original accepted vectors."""
    def __init__(self, n):
        self.n = n
        self.originals: list[Vector] = []
        # pivot -> (normalized residual, coefficients of original accepted vectors)
        self.pivots: dict[int, tuple[Vector, tuple[F, ...]]] = {}

    def decompose(self, value):
        v = list(map(F, value))
        if len(v) != self.n:
            raise ValueError('vector dimension differs')
        coefficients = [F(0)] * len(self.originals)
        for pivot, (row, rep) in sorted(self.pivots.items()):
            scale = v[pivot]
            if not scale:
                continue
            v = [x-scale*y for x, y in zip(v, row)]
            for j, y in enumerate(rep):
                coefficients[j] += scale*y
        return tuple(coefficients), tuple(v)

    def add(self, value):
        v = vector(value)
        coefficients, residual = self.decompose(v)
        pivot = next((i for i, x in enumerate(residual) if x), None)
        if pivot is None:
            return False
        scale = residual[pivot]
        normalized = tuple(x/scale for x in residual)
        rep = tuple(-x/scale for x in coefficients) + (1/scale,)
        self.pivots[pivot] = normalized, rep
        self.originals.append(v)
        return True

    def coordinates(self, value):
        coefficients, residual = self.decompose(value)
        if any(residual):
            raise ValueError('observable outside certified continuation space')
        return coefficients


@dataclass
class Closure:
    operators: dict[str, Matrix]
    probes: dict[str, Vector]
    basis: ExactBasis
    witnesses: list[tuple[tuple[str, ...], str]]
    attempts: int
    profile: tuple[int, ...]

    @property
    def dimension(self):
        return len(self.basis.originals)

    def signature(self, mu):
        return tuple(dot(mu, v) for v in self.basis.originals)

    def equivalent(self, left, right):
        return self.signature(left) == self.signature(right)

    def separator(self, left, right):
        """A retained real branch/probe distinguishes, or a closure certificate.

        Witnesses are BFS-ordered operator words, not arbitrary learned vectors.
        Minimality is in this generator alphabet; masks are not time steps.
        """
        for v, (word, probe) in zip(self.basis.originals, self.witnesses):
            a, b = dot(left, v), dot(right, v)
            if a != b:
                return {'word': word, 'probe': probe, 'left': a, 'right': b,
                        'difference': b-a}
        return None

    def state_classes(self):
        groups = {}
        for i in range(self.basis.n):
            key = tuple(v[i] for v in self.basis.originals)
            groups.setdefault(key, []).append(i)
        return tuple(tuple(g) for g in groups.values())

    def reduced_operator(self, label):
        # Column j gives coordinates of Q F[:,j]. Thus QF=F B_Q.
        columns = [self.basis.coordinates(apply(self.operators[label], v))
                   for v in self.basis.originals]
        return tuple(tuple(columns[j][i] for j in range(self.dimension))
                     for i in range(self.dimension))

    def verify(self):
        for label, q in self.operators.items():
            b = self.reduced_operator(label)
            for j, v in enumerate(self.basis.originals):
                rebuilt = tuple(sum((self.basis.originals[k][i]*b[k][j]
                                     for k in range(self.dimension)), F(0))
                                for i in range(self.basis.n))
                if rebuilt != apply(q, v):
                    raise AssertionError('invalid intertwining certificate: '+label)
        for value in self.probes.values():
            self.basis.coordinates(value)
        for v, (word, probe) in zip(self.basis.originals, self.witnesses):
            if v != word_value(self.operators, word, self.probes[probe]):
                raise AssertionError('invalid constructive witness')
        return True


def close_continuations(operators: Mapping[str, Matrix], probes: Mapping[str, Iterable]) -> Closure:
    """Generate the least invariant span without enumerating all words.

    From each accepted vector apply each operator once. Rejecting a dependent
    vector discards its whole subtree because all maps are linear. At most
    N accepted vectors and |probes|+|operators|*rank candidate evaluations.
    This counts algebraic operations, not arbitrary-precision bit complexity.
    """
    ops = dict(operators)
    base = {key: vector(v) for key, v in probes.items()}
    if not base:
        raise ValueError('at least one terminal observable is required')
    n = len(next(iter(base.values())))
    if not n or any(len(v)!=n for v in base.values()) or any(len(q)!=n for q in ops.values()):
        raise ValueError('common positive finite dimension required')
    basis = ExactBasis(n)
    witnesses = []
    queue = deque()
    attempts = 0
    by_depth = {}
    for name, v in base.items():
        attempts += 1
        if basis.add(v):
            witnesses.append(((), name))
            queue.append((v, (), name))
            by_depth[0] = by_depth.get(0, 0)+1
    while queue:
        v, word, probe = queue.popleft()
        for label, q in ops.items():
            candidate = apply(q, v)
            attempts += 1
            new_word = (label,)+word
            if basis.add(candidate):
                witnesses.append((new_word, probe))
                queue.append((candidate, new_word, probe))
                depth = len(new_word)
                by_depth[depth] = by_depth.get(depth, 0)+1
    counts = []
    for d in range(max(by_depth)+2):
        counts.append(sum(v for k, v in by_depth.items() if k<=d))
    return Closure(ops, base, basis, witnesses, attempts, tuple(counts))


def point(n, index):
    return tuple(F(i==index) for i in range(n))


def observation_masks(labels):
    """Readable-label tests; never introduce hidden state as a new observation."""
    return {'observe:'+str(label): tuple({i:F(1)} if x==label else {} for i,x in enumerate(labels))
            for label in dict.fromkeys(labels)}


def refine_lumping(operators, labels):
    """Coarsest stable partition refining declared labels; stronger than trace equality."""
    colors = tuple(labels)
    history = []
    while True:
        groups = {}
        for i, color in enumerate(colors):
            groups.setdefault(color, []).append(i)
        blocks = tuple(tuple(g) for g in groups.values())
        history.append(len(blocks))
        signature = []
        for i in range(len(colors)):
            signature.append((colors[i], tuple(
                tuple(sum((row.get(j,F(0)) for j in block), F(0)) for block in blocks)
                for q in operators.values() for row in (q[i],))))
        ids = {}
        new_colors = tuple(ids.setdefault(key, len(ids)) for key in signature)
        if len(ids)==len(blocks):
            return {'blocks':blocks,'history':tuple(history)}
        colors = new_colors


def quotient_matrix(q, blocks):
    """Produce a genuine substochastic quotient or reject unsafe state lumping."""
    quotient=[]
    for group in blocks:
        rows=[tuple(sum((q[i].get(j,F(0)) for j in target),F(0)) for target in blocks)
              for i in group]
        if any(row!=rows[0] for row in rows[1:]):
            raise ValueError('signature equality is not necessarily Markov lumpability')
        quotient.append({j:x for j,x in enumerate(rows[0]) if x})
    return matrix(quotient)


def plant_operators(p=None, micro=False, actions=None, masks=False):
    """Reuse v6 law unchanged. Invalid actions fail closed; runtime sees only k,b.

    h remains hidden. A state-signature vector is an evaluator construction.
    Never deploy the quotient state (k,h,b) as if h had become observable.
    """
    from .composition import Contract, COST, DEAD, macro_row, micro_row, quotient
    p = Contract() if p is None else p
    states = p.micros() if micro else p.states()
    ix = {s:i for i,s in enumerate(states)}
    ops={}
    for action in (tuple(COST) if actions is None else tuple(actions)):
        rows=[]
        for s in states:
            budget=s[3] if micro else s[2]
            if action not in p.actions(budget):
                rows.append({});continue
            law=micro_row(p,s,action) if micro else macro_row(p,s,action)
            rows.append({ix[t]:value for t,value in law.items() if t!=DEAD and value})
        ops[action]=matrix(rows)
    labels=tuple((quotient(s)[0],quotient(s)[2]) if micro else (s[0],s[2]) for s in states)
    if masks: ops.update(observation_masks(labels))
    return states,ops,labels


def delayed_fixture():
    # x,y have equal current and all one-command survival; prepare;check separates.
    ops={'prepare':matrix([{2:1},{3:1},{2:1},{3:1}]),
         'check':matrix([{0:1},{1:1},{2:1},{}])}
    return ('x','y','p','q'),ops,{'alive':vector([1]*4)}


def feedback_fixture():
    """Same action-sequence laws, unequal performance of a common readable feedback."""
    states=tuple(product((0,1),repeat=2)) # hidden W, genuinely readable Z
    ops={f'act{u}':matrix([{i:1} if w==u else {} for i,(w,z) in enumerate(states)])
         for u in (0,1)}
    informed=vector([F(1,2),0,0,F(1,2)])
    independent=vector([F(1,4)]*4)
    observable=dict(ops)
    observable.update(observation_masks(tuple(z for w,z in states)))
    return states,ops,observable,informed,independent


def rank_vs_states(n=7):
    if n<2: raise ValueError('at least two states')
    # Only one subsequent step matters; exactly rank 2, but n distinct p_i.
    return {'advance':matrix([{n-1:F(i,n-1)} for i in range(n)])},{'alive':vector([1]*n)}


def delayed_chain(n=9):
    if n<1: raise ValueError('positive chain length')
    return {'step':matrix([{i+1:1} if i<n-1 else {} for i in range(n)])},{'alive':vector([1]*n)}


def refinement_falsifier():
    """Trace signature classes need not form a stochastic Markov quotient.

    u,v are safe absorbers; r has survival 1/2; x goes to r and y goes
    half to u, half to v? v must die immediately so the mix matches r.
    r -> .5*u, v -> death; u -> u; x->r, y->.5*u+.5*v.
    x,y have (1,1,.5,.5,...) but transitions land in different trace classes.
    """
    # u=0, v=1, r=2, x=3, y=4
    q=matrix([{0:1},{},{0:F(1,2)},{2:1},{0:F(1,2),1:F(1,2)}])
    return {'step':q},{'alive':vector([1]*5)}


def lift_nuisance(core, multiplicity):
    """Explicit test instance of a constructive non-symmetric nuisance theorem.

    For each core transition i->j, nuisance maps r->(max(0,r-1)+i+2*j) mod m (noninjective for m>1).
    Arbitrary row-stochastic nuisance kernels also satisfy the same quotient.
    """
    if multiplicity<1: raise ValueError('positive multiplicity')
    out={}
    for label,q in core.items():
        rows=[]
        for i,row in enumerate(q):
            for r in range(multiplicity):
                rows.append({j*multiplicity+(max(0,r-1)+i+2*j)%multiplicity:v for j,v in row.items()})
        out[label]=matrix(rows)
    return out
