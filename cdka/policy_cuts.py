"""CDKA T3.D/T4.C: policy-aware physical information cuts.

Known mathematical instruments (Dobrushin, finite-state controllers,
occupancy planning, positive-kernel invariance), independently derived.
No claim of general agency or mathematical novelty.

Finite-horizon laws may depend on a DECLARED clock and observable physical
state. No policy receives W, an unrecorded history, or the design occupancy
at run time. Missing transition mass means failure and is NEVER normalized.
All reference calculations use exact fractions.Fraction arithmetic.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from typing import Hashable, Mapping, Sequence

State = Hashable
Action = Hashable
Row = Mapping[State, F]


def total_variation(p: Row, q: Row) -> F:
    """TV for two normalized finite laws (not subprobability survivors)."""
    if sum(p.values(), F(0)) != 1 or sum(q.values(), F(0)) != 1:
        raise ValueError('TV inputs must be probability laws')
    if any(x < 0 for x in (*p.values(), *q.values())):
        raise ValueError('negative probability')
    return sum((abs(p.get(k, F(0)) - q.get(k, F(0)))
                for k in p.keys() | q.keys()), F(0)) / 2


def dobrushin(rows: Mapping[State, Row]) -> F:
    """Exact contraction coefficient max TV of distinct input rows."""
    labels = tuple(rows)
    return max((total_variation(rows[c], rows[d]) for c in labels
                for d in labels if c != d), default=F(0))


def feedback_envelope(channels: Mapping[State, Mapping[Action, Row]]) -> F:
    """sup_pi delta(K_pi), with independently feasible row-wise actions.

    Distinct input rows must be used: mixing different actions at the SAME
    sole input does not by itself make a channel carry an input distinction.
    Global constraints coupling actions across different observations may
    make this expression only an upper bound; they are not assumed here.
    """
    labels = tuple(channels)
    if any(not channels[c] for c in labels):
        raise ValueError('each input requires an admissible action')
    return max((total_variation(ra, rb)
                for c in labels for d in labels if c != d
                for ra in channels[c].values()
                for rb in channels[d].values()), default=F(0))


def deterministic_feedback_values(channels) -> tuple[F, ...]:
    """Independent exhaustive oracle for the feedback envelope."""
    labels = tuple(channels)
    return tuple(dobrushin({c: channels[c][a] for c, a in zip(labels, plan)})
                 for plan in product(*(tuple(channels[c]) for c in labels)))


def live_binary_value(joint: Mapping[tuple[int, Hashable], F]) -> tuple[F, F, F]:
    """Mass, unnormalized distinguishability, and best safe terminal action.

    mu(w,c) = P(W=w, C=c, alive). Both terminal actions are assumed feasible
    for every live c and the correct action is w. The returned value equals
    (mass + sum_c |mu(0,c)-mu(1,c)|)/2, not a normalized conditional accuracy.
    """
    if any(w not in (0, 1) or p < 0 for (w, _), p in joint.items()):
        raise ValueError('binary W and nonnegative live masses required')
    mass = sum(joint.values(), F(0))
    if mass > 1:
        raise ValueError('live mass exceeds one')
    labels = {c for _, c in joint}
    separation = sum((abs(joint.get((0,c), F(0)) - joint.get((1,c), F(0)))
                      for c in labels), F(0))
    direct = sum((max(joint.get((0,c), F(0)), joint.get((1,c), F(0)))
                  for c in labels), F(0))
    if direct != (mass + separation)/2:
        raise AssertionError('algebraic identity failed')
    return mass, separation, direct


@dataclass
class PhysicalModel:
    """Finite live-state model. The missing row mass is absorbing failure.

    Observation C is the complete physical input available to the controller.
    The model stores underlying (W,C), not W as an allowed policy argument.
    Resource/health limitations must be in C, actions, or transition rows.
    """
    states: tuple[State, ...]
    observations: Mapping[State, Hashable]
    actions: Mapping[Hashable, tuple[Action, ...]]
    kernel: Mapping[tuple[State, Action], Row]

    def __post_init__(self):
        if len(set(self.states)) != len(self.states):
            raise ValueError('duplicate states')
        universe = set(self.states)
        for s in self.states:
            c = self.observations[s]
            if not self.actions.get(c):
                raise ValueError('no action for observable state')
            for a in self.actions[c]:
                row = self.kernel[s, a]
                if any(t not in universe or p < 0 for t,p in row.items()):
                    raise ValueError('invalid transition row')
                if sum(row.values(), F(0)) > 1:
                    raise ValueError('kernel row exceeds one')

    def prescriptions(self, live: Sequence[F] | None = None):
        """Generate maps C->A, shared by all hidden states with identical C."""
        cells = tuple(dict.fromkeys(self.observations[s] for s in self.states))
        relevant = set(cells) if live is None else {
            self.observations[s] for s,p in zip(self.states, live) if p > 0}
        options = [self.actions[c] if c in relevant else self.actions[c][:1]
                   for c in cells]
        for values in product(*options):
            yield dict(zip(cells, values))

    def advance(self, mu: Sequence[F], prescription: Mapping) -> tuple[F, ...]:
        index = {s:i for i,s in enumerate(self.states)}
        new = [F(0)] * len(self.states)
        for s,p in zip(self.states, mu):
            if not p:
                continue
            c = self.observations[s]
            a = prescription[c]
            if a not in self.actions[c]:
                raise ValueError('physically unavailable action')
            for t,q in self.kernel[s, a].items():
                new[index[t]] += p*q
        if sum(new, F(0)) > sum(mu, F(0)):
            raise AssertionError('failure mass was incorrectly renormalized')
        return tuple(new)

    def survival_optimum(self, initial: Mapping[State, F], steps: int):
        """Exact finite-horizon design DP; outputs a physical prescription plan.

        The occupancy is an OFFLINE design statistic, not an additional
        observation or memory at execution. Nonstationary policies assume
        the stage index/clock is available. Fresh behavioral randomization
        cannot improve this unconstrained expected finite-horizon objective.
        """
        if type(steps) is not int or steps < 0:
            raise ValueError('nonnegative integer horizon required')
        mu = tuple(initial.get(s, F(0)) for s in self.states)
        if any(p < 0 for p in mu) or sum(mu, F(0)) > 1:
            raise ValueError('invalid initial live distribution')

        @lru_cache(None)
        def value(t, mass):
            if t == 0:
                return sum(mass, F(0)), ()
            best = F(-1)
            best_plan = ()
            for phi in self.prescriptions(mass):
                future, plan = value(t-1, self.advance(mass, phi))
                if future > best:
                    best, best_plan = future, (phi,) + plan
            return best, best_plan
        result, plan = value(steps, mu)
        return {'value': result, 'plan': plan, 'design_states': value.cache_info().currsize}

    def full_state_oracle(self, initial: Mapping[State, F], steps: int) -> F:
        """Relaxation allowed to see hidden W: diagnostic upper bound ONLY."""
        v = {s: F(1) for s in self.states}
        for _ in range(steps):
            v = {s: max(sum((p*v[t] for t,p in self.kernel[s,a].items()), F(0))
                        for a in self.actions[self.observations[s]]) for s in self.states}
        return sum((p*v[s] for s,p in initial.items()), F(0))

    def invariant_under(self, prescription: Mapping) -> frozenset[State]:
        """Greatest live support closed with probability 1 under this policy."""
        good = set(self.states)
        while True:
            keep = {s for s in good
                    if sum(self.kernel[s,prescription[self.observations[s]]].values(), F(0)) == 1
                    and all(t in good for t,p in
                            self.kernel[s,prescription[self.observations[s]]].items() if p > 0)}
            if keep == good:
                return frozenset(good)
            good = keep

    def stationary_safe_witnesses(self, required: Sequence[State]):
        needed = set(required)
        for phi in self.prescriptions():
            good = self.invariant_under(phi)
            if needed <= good:
                yield phi, good


def renewal_model(error: F = F(1, 10), selectable_repair: bool = True):
    """A regenerative physical controller with a hidden static binary W.

    C = (phase, memory, actuator_health, resource_token).
    Repair phase: (0,m,0,1) --write a, cost 1--> (1,a xor noise,1,0).
    Act phase: choose u. If u=W, actuator command latches memory=u,
    restores one resource from the environment, and wear forces next repair:
                    (1,m,1,0) --> (0,u,0,1).
    If u!=W, the trajectory fails irreversibly. No observation of W later.
    All dependence on past commands is represented in the physical latch.
    """
    error = F(error)
    if not F(0) <= error <= F(1,2):
        raise ValueError('repair flip probability must be in [0,1/2]')
    cells = tuple((phase, m, phase, 1-phase) for phase in (0,1) for m in (0,1))
    states = tuple((w,c) for w in (0,1) for c in cells)
    obs = {s:s[1] for s in states}
    actions = {c: (('write',0), ('write',1)) if c[0] == 0 and selectable_repair
               else ((('write',0),) if c[0] == 0 else (('act',0),('act',1)))
               for c in cells}
    kernel = {}
    for w,c in states:
        for a in actions[c]:
            if c[0] == 0:
                bit = a[1]
                row = {}
                for m,p in ((bit,1-error),(1-bit,error)):
                    if p:
                        row[(w,(1,m,1,0))] = p
            else:
                row = {(w,(0,a[1],0,1)):F(1)} if a[1] == w else {}
            kernel[(w,c),a] = row
    initial = {(w,(0,w,0,1)):F(1,2) for w in (0,1)}
    return PhysicalModel(states,obs,actions,kernel), initial


def cycle_profiles(error: F = F(1,10), selectable_repair: bool = True):
    """Independent exact local oracle: enumerate two-bit repair/act maps."""
    error = F(error)
    if not 0 <= error <= F(1,2):
        raise ValueError('error outside [0,1/2]')
    repair_maps = tuple(product((0,1), repeat=2)) if selectable_repair else ((0,0),)
    result = []
    for f in repair_maps:
        for g in product((0,1), repeat=2):
            profile = []
            for w in (0,1):
                value = sum((p for y,p in ((f[w],1-error),(1-f[w],error))
                             if g[y] == w), F(0))
                profile.append(value)
            result.append((f,g,tuple(profile)))
    return tuple(result)


def profile_products(error: F, cycles: int):
    """All distinct reliability vectors of deterministic cycle schedules."""
    if type(cycles) is not int or cycles < 1:
        raise ValueError('cycles must be a positive integer')
    stage = {p for _,_,p in cycle_profiles(error)}
    values = {(F(1),F(1))}
    for _ in range(cycles):
        values = {(a*c,b*d) for a,b in values for c,d in stage}
    return frozenset(values)


def pareto_front(profiles):
    points = tuple(set(profiles))
    return frozenset(p for p in points
                     if not any(q != p and q[0] >= p[0] and q[1] >= p[1]
                                for q in points))


def renewal_closed_form(error: F, cycles: int):
    """Exact mean and robust survival of this model, not a general law.

    Robust optimum uses fresh behavioral randomization only (or deterministic
    laws). A persistent external policy seed would add memory and changes
    the robust problem; it is intentionally NOT freely provided here.
    """
    error = F(error)
    if not 0 <= error <= F(1,2) or type(cycles) is not int or cycles < 1:
        raise ValueError('invalid renewal parameters')
    balanced = (1-error)**cycles
    return {'balanced': balanced, 'robust': balanced,
            'mean': max(F(1,2), balanced),
            'persistent_seed_robust': max(F(1,2), balanced)}


def randomized_cycle_profile(error: F, f: tuple[F,F], g: tuple[F,F]):
    """f[m]=P(write1|m), g[y]=P(act1|y), fresh independent coins."""
    error = F(error)
    if not 0 <= error <= F(1,2) or any(not 0 <= z <= 1 for z in (*f,*g)):
        raise ValueError('invalid behavioral probabilities')
    prob_one = [error + (1-2*error)*f[w] for w in (0,1)]
    action_one = [(1-y)*g[0]+y*g[1] for y in prob_one]
    return 1-action_one[0], action_one[1]
