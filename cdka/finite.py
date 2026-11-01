"""Exact finite action-sufficiency baselines.

A world is a possible condition and each world has a nonempty set of safe
actions. Under perfect observation, one-shot deterministic memory, and
zero error, the minimum number of internal messages is the minimum number
of actions whose success sets cover all worlds. This is a known result,
not a new CDKA theorem.
"""
from __future__ import annotations

from itertools import combinations
from math import expm1, inf, isfinite
from typing import Hashable, Iterable, Mapping


def minimum_action_cover(
    safe_actions: Mapping[Hashable, Iterable[Hashable]],
) -> tuple[Hashable, ...] | None:
    """Return a minimum set of actions covering every world, or None.

    The empty world set has the empty cover. Worlds with no safe action
    make the instance infeasible. This exhaustive reference solver is
    exponential by design; it is not intended for large instances.
    """
    worlds = tuple(safe_actions)
    if not worlds:
        return ()
    materialized = {w: tuple(safe_actions[w]) for w in worlds}
    allowed = {w: frozenset(materialized[w]) for w in worlds}
    if any(not acts for acts in allowed.values()):
        return None
    # Preserve insertion order without assuming actions are sortable.
    actions = tuple(dict.fromkeys(a for w in worlds for a in materialized[w]))
    for k in range(1, len(actions) + 1):
        for selected in combinations(actions, k):
            if all(not allowed[w].isdisjoint(selected) for w in worlds):
                return selected
    return None


def minimum_memory_bits(cover: tuple[Hashable, ...] | None) -> int | None:
    """Worst-case fixed-width binary storage; NOT Shannon mutual information."""
    return None if cover is None else (0 if len(cover) <= 1 else (len(cover) - 1).bit_length())


def action_decoding(
    safe_actions: Mapping[Hashable, Iterable[Hashable]],
) -> dict[Hashable, Hashable] | None:
    """Construct a deterministic viable state-to-action assignment."""
    selected = minimum_action_cover(safe_actions)
    if selected is None:
        return None
    allowed = {w: frozenset(acts) for w, acts in safe_actions.items()}
    return {w: next(a for a in selected if a in allowed[w]) for w in allowed}


def dowker_simplices(
    safe_actions: Mapping[Hashable, Iterable[Hashable]],
) -> frozenset[frozenset[Hashable]]:
    """Nonempty simplices of worlds sharing at least one safe action."""
    worlds = tuple(safe_actions)
    allowed = {w: frozenset(safe_actions[w]) for w in worlds}
    return frozenset(
        frozenset(group)
        for k in range(1, len(worlds) + 1)
        for group in combinations(worlds, k)
        if set.intersection(*(set(allowed[w]) for w in group))
    )


def equilibrium(lam: float, w: int, u: int) -> float:
    """Equilibrium of dx/dt=-x+lam*w+u, for constant w,u."""
    if not isfinite(lam) or lam < 0 or w not in (-1, 1) or not isfinite(u):
        raise ValueError("lam must be finite and >=0, w in {-1,+1}, u finite")
    return lam * w + u


def t1_safe_actions(
    lam: float,
    boundary: float = 1.5,
    *,
    actions: tuple[float, ...] = (-1, 1),
    horizon: float = inf,
) -> dict[int, set[float]]:
    """Actions preserving |x(t)|<=boundary over t in [0,horizon].

    Dynamics: dx/dt=-x+lam*w+u, x(0)=0, w in {-1,1}, u held
    constant. The peak magnitude is |lam*w+u|*(1-exp(-horizon)).
    An infinite horizon means the full limiting equilibrium magnitude.
    """
    if not isfinite(boundary) or boundary <= 0:
        raise ValueError("boundary must be positive and finite")
    if not (horizon > 0 and (isfinite(horizon) or horizon == inf)):
        raise ValueError("horizon must be positive or infinity")
    acts = tuple(actions)
    if not all(isfinite(a) for a in acts):
        raise ValueError("actions must be finite")
    gain = 1.0 if horizon == inf else -expm1(-horizon)
    admissible_equilibrium = boundary / gain
    return {w: {u for u in acts
                if abs(equilibrium(lam, w, u)) <= admissible_equilibrium}
            for w in (-1, 1)}


def t1_expected_cover_size(lam: float) -> int | None:
    """Analytic closed form for boundary=1.5 (inclusive)."""
    if not isfinite(lam) or lam < 0:
        raise ValueError("lam must be finite and >=0")
    if lam <= 0.5:
        return 1
    if lam <= 2.5:
        return 2
    return None
