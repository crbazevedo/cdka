"""Exact finite causal-cut laboratory for CDKA T3/T4.

This is a model-specific application of binary hypothesis testing, data
processing, and finite-state controller synthesis, NOT a new theorem.

World W is a fair binary variable. A physically limited sensor records Y;
each mandatory repair restores actuator availability but can erase volatile
memory and can change W. Final action must equal the CURRENT world. Policies
may use only physical readouts available after repair, never a free record
of previous observations or previous actions.

The repair protection schedule is precommitted, independent of W, and
NOT readable as a side channel at the final decision. An alternative
actuator-state side channel is deliberately tested as a counterexample.
All exact probabilities use fractions.Fraction.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import log2
from typing import Hashable, Iterable, Mapping

ERASED = 2
MEMORY = (0, 1, ERASED)
WORLDS = (0, 1)


def _prob(p: F, maximum: F = F(1)) -> F:
    p = F(p)
    if not (0 <= p <= maximum):
        raise ValueError(f"probability must be between 0 and {maximum}")
    return p


def _accumulate(d: dict, key, value: F) -> None:
    if value:
        d[key] = d.get(key, F(0)) + value


def bayes_best(joint: Mapping[tuple[int, Hashable], F],
               symbols: Iterable[Hashable] = MEMORY) -> tuple[F, dict]:
    """Independent exhaustive deterministic terminal-policy oracle."""
    symbols = tuple(symbols)
    if not joint:
        return F(0), {}
    best = F(-1)
    best_decoder = None
    for actions in product(WORLDS, repeat=len(symbols)):
        decoder = dict(zip(symbols, actions))
        prob = sum((p for (w, symbol), p in joint.items()
                    if decoder[symbol] == w), F(0))
        if prob > best:
            best = prob
            best_decoder = decoder
    return best, best_decoder


def total_variation_binary(joint: Mapping[tuple[int, Hashable], F],
                           symbols: Iterable[Hashable] = MEMORY) -> F:
    """TV between terminal observation laws conditioned on W_final=0/1.

    This implementation expects balanced terminal priors, ensured by the
    symmetric binary model. The global observation must include every
    physically available channel, not merely an explicit memory register.
    """
    symbols = tuple(symbols)
    p0 = sum((joint.get((0, m), F(0)) for m in symbols), F(0))
    p1 = sum((joint.get((1, m), F(0)) for m in symbols), F(0))
    if p0 != F(1, 2) or p1 != F(1, 2):
        raise ValueError("balanced terminal prior required")
    return sum((abs(2*joint.get((0,m),F(0))-
                    2*joint.get((1,m),F(0))) for m in symbols),F(0))/2


def zero_error_support_obstructions(
    joint: Mapping[tuple[int, Hashable], F],
    safe_actions: Mapping[int, frozenset[int]],
    symbols: Iterable[Hashable],
) -> dict[Hashable, frozenset[int]]:
    """Signals where the joint support contains incompatible safe actions.

    A zero-error decoder exists iff this dictionary is empty, provided
    every signal has at least one possible world and terminal action
    availability is the same for all worlds.
    """
    failures = {}
    for m in symbols:
        possible = frozenset(w for w in safe_actions
                             if joint.get((w,m),F(0))>0)
        if not possible:
            continue
        common = set.intersection(*(set(safe_actions[w]) for w in possible))
        if not common:
            failures[m] = possible
    return failures


@dataclass(frozen=True)
class CausalCutSystem:
    """Sensing/repaired-actuator controller with physically volatile memory.

    eta = BSC error of sensing W_initial (0..1/2).
    rho = erasure probability on EACH unprotected repair (0..1).
    nu  = chance W flips on EACH repair (0..1/2).
    cycles = number of compulsory repairs before the deadline.
    budget = integer resource tokens: one per repair, one extra token to
             protect memory for any given repair.

    The protection schedule is precommitted independently of W and its
    choice is NOT a visible bit at the terminal controller.
    """
    eta: F = F(0)
    rho: F = F(1)
    nu: F = F(0)
    cycles: int = 1
    budget: int = 1

    def __post_init__(self):
        object.__setattr__(self, "eta", _prob(self.eta,F(1,2)))
        object.__setattr__(self, "rho", _prob(self.rho))
        object.__setattr__(self, "nu", _prob(self.nu,F(1,2)))
        if (type(self.cycles) is not int or self.cycles < 1 or
            type(self.budget) is not int or self.budget < 0):
            raise ValueError("cycles >=1, budget >=0 must be integers")

    @property
    def actuator_ready(self) -> bool:
        return self.budget >= self.cycles

    def max_protections(self) -> int:
        return min(self.cycles, max(0,self.budget-self.cycles))

    def canonical_schedule(self) -> tuple[bool, ...]:
        """Any nonadaptive schedule with this number of protected repairs
        has equal terminal value in the homogeneous model."""
        k = self.max_protections()
        return (True,)*k + (False,)*(self.cycles-k)

    def terminal_joint(self, schedule: tuple[bool, ...] | None = None
                       ) -> dict[tuple[int,int], F]:
        """Exact joint law P(W_final, M_final) via forward propagation."""
        if not self.actuator_ready:
            return {}
        if schedule is None:
            schedule = self.canonical_schedule()
        if (len(schedule)!=self.cycles or
            sum(schedule)+self.cycles>self.budget):
            raise ValueError("repair protection schedule exceeds available budget")
        # After a possibly noisy observation, memory contains the reading.
        distribution: dict[tuple[int,int],F] = {}
        for w in WORLDS:
            for y in WORLDS:
                p=F(1,2)*(1-self.eta if y==w else self.eta)
                _accumulate(distribution,(w,y),p)

        # Each mandatory repair can alter both the physical context and
        # the volatile memory; no new observation is physically available.
        for protected in schedule:
            upcoming: dict[tuple[int,int],F] = {}
            for (w,m),p in distribution.items():
                for w_next, pw in ((w,1-self.nu),(1-w,self.nu)):
                    if protected or m==ERASED:
                        memory_outcomes=((m,F(1)),)
                    else:
                        memory_outcomes=((m,1-self.rho),(ERASED,self.rho))
                    for m_next,pm in memory_outcomes:
                        _accumulate(upcoming,(w_next,m_next),p*pw*pm)
            distribution=upcoming
        if sum(distribution.values(),F(0))!=1:
            raise AssertionError("probability mass not preserved")
        return distribution

    def best_success(self) -> F:
        if not self.actuator_ready:
            return F(0)
        return bayes_best(self.terminal_joint())[0]

    def exact_formula(self) -> F:
        """Closed form for best final survival of this restricted model."""
        if not self.actuator_ready:
            return F(0)
        n=self.cycles
        k=self.max_protections()
        coefficient=(1-2*self.eta)*(1-2*self.nu)**n*(1-self.rho)**(n-k)
        return (1+coefficient)/2

    def memory_tv(self) -> F:
        if not self.actuator_ready:
            raise ValueError("terminal actuator unavailable")
        return total_variation_binary(self.terminal_joint())

    def zero_error_obstructions(self) -> dict:
        return zero_error_support_obstructions(
            self.terminal_joint(),{0:frozenset((0,)),1:frozenset((1,))},
            MEMORY,
        )

    def initial_sensor_information_bits(self) -> float:
        """I(W_initial;Y_initial), not terminal usable information."""
        return 1-_h2(float(self.eta))

    def terminal_information_bits(self) -> float:
        """I(W_final;M_final) for uniform final W, computed from joint."""
        joint=self.terminal_joint()
        if not joint:
            return 0.0
        p_m={m:sum((joint.get((w,m),F(0)) for w in WORLDS),F(0))
             for m in MEMORY}
        value=0.0
        for (w,m),p in joint.items():
            if p:
                value+=float(p)*log2(float(p/(F(1,2)*p_m[m])))
        return value


def _h2(p: float) -> float:
    if p<=0 or p>=1:
        return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)


def deterministic_minimal_obstructions() -> list[tuple]:
    """Exhaust all two-state deterministic sensor and repair maps.

    Injective sensor + noninjective repair + binary incompatible terminal
    actions is the smallest deterministic information-cut obstruction.
    """
    funcs=list(product(WORLDS,repeat=2))
    failures=[]
    for sensor in funcs:
        if sensor[0]==sensor[1]:
            continue  # sensory marginal itself is insufficient
        for reset in funcs:
            joint={}
            for w in WORLDS:
                m=reset[sensor[w]]
                _accumulate(joint,(w,m),F(1,2))
            maximum=bayes_best(joint,symbols=WORLDS)[0]
            if maximum<F(1):
                failures.append((sensor,reset,maximum))
    return failures


def physical_configuration_bypass() -> tuple[F,F]:
    """Counterexample to a cut that examines M but ignores organization Z.

    After perfect sensing W, repair resets volatile memory M to 0. A
    pre-repair physical configuration action persists in actuator mode Z=W
    and is readable at the final decision: optimal action is U=Z.
    """
    memory_only={(w,0):F(1,2) for w in WORLDS}
    with_organization={(w,(0,w)):F(1,2) for w in WORLDS}
    no_memory=bayes_best(memory_only,symbols=(0,))[0]
    whole_cut=bayes_best(with_organization,symbols=((0,0),(0,1)))[0]
    return no_memory,whole_cut


def enumerate_repair_schedules(system: CausalCutSystem) -> dict:
    """Exact oracle independently scores EVERY resource-feasible schedule."""
    if not system.actuator_ready:
        return {}
    scores={}
    for flags in product((False,True),repeat=system.cycles):
        if sum(flags)+system.cycles>system.budget:
            continue
        scores[flags]=bayes_best(system.terminal_joint(flags))[0]
    return scores


def general_safe_decision_value(
    joint: Mapping[tuple[int, Hashable], F],
    safe_actions: Mapping[int, frozenset[int]],
    symbols: Iterable[Hashable],
) -> tuple[F, dict]:
    """Exact finite safe-decision oracle allowing multiple safe actions.

    Unlike binary classification, a correct intervention need only be in
    A_w; it need not identify w uniquely.
    """
    symbols=tuple(symbols)
    actions=tuple(sorted(set().union(*safe_actions.values())))
    if not actions:
        return F(0), {}
    maximum=F(-1)
    argmax={}
    for plan in product(actions, repeat=len(symbols)):
        decoder=dict(zip(symbols,plan))
        score=sum((p for (w,m),p in joint.items()
                   if decoder[m] in safe_actions[w]),F(0))
        if score>maximum:
            maximum=score
            argmax=decoder
    return maximum,argmax


def higher_order_compatibility_obstruction() -> tuple[F, bool, dict]:
    """Three worlds: every pair admits a common action, but not the triple.

    A compulsory repair collapses all three worlds into the same terminal
    physical signal. No zero-error decision is possible; best success
    with uniform prior is exactly 2/3. This is the Dowker phenomenon in
    an actual (albeit simple) memory-transition architecture.
    """
    safe={
        0:frozenset((0,1)),
        1:frozenset((1,2)),
        2:frozenset((0,2)),
    }
    joint={(w,ERASED):F(1,3) for w in safe}
    pairwise=all(bool(safe[w]&safe[v]) for w in safe for v in safe if w!=v)
    failures=zero_error_support_obstructions(joint,safe,(ERASED,))
    best,_=general_safe_decision_value(joint,safe,(ERASED,))
    return best,pairwise,failures


def action_conditioned_reset_signaling() -> dict[tuple[int,int], F]:
    """Per-action reset erases memory, but adaptive reset choice transmits it.

    For each fixed repair mode a∈{0,1}:
       K^a(m'|m)=1{m'=a}, independent of m,
    so the channel has Dobrushin/TV coefficient 0.

    If repair policy selects a=pi(m), the closed-loop kernel is instead
       K_pi(m'|m)=1{m'=pi(m)}.
    Identity or negation policies carry one bit through the reset,
    whereas constant policies carry none. This is a known example of
    information/signaling through physical actions, NOT a new theorem.
    """
    values={}
    for policy in product(WORLDS, repeat=2):
        joint={}
        for w in WORLDS:
            sensed=w  # initial sensor perfect
            repair_mode=policy[sensed]
            # Each fixed-mode repair destroys m but writes its chosen mode.
            _accumulate(joint,(w,repair_mode),F(1,2))
        values[policy]=total_variation_binary(joint,symbols=WORLDS)
    return values
