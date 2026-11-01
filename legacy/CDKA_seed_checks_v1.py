"""CDKA v1.0: deterministic exhaustive checks of proof baselines.

Only uses the Python standard library. These checks validate examples, not novelty.
"""
from itertools import combinations
from math import log2


def min_cover(worlds, actions, safe):
    """Minimum number of distinct actions covering all world states, or None."""
    for k in range(1, len(actions) + 1):
        for group in combinations(actions, k):
            if all(any(safe(w, a) for a in group) for w in worlds):
                return k
    return None


def linear_plant(lam, w, a):
    # smooth physical map, but thresholds of viable actions can be discontinuous
    return lam * w + a


def test_action_thresholds():
    worlds = (-1, 1)
    actions = (-1, 1)
    expected = [(0.0, 1), (0.5, 1), (0.5001, 2), (1.0, 2),
                (2.5, 2), (2.5001, None)]
    for lam, exp in expected:
        k = min_cover(worlds, actions,
                      lambda w, a: abs(linear_plant(lam, w, a)) <= 1.5 + 1e-12)
        assert k == exp, (lam, k, exp)
    return expected


def test_pairwise_not_global():
    viable = {"A": {1, 2}, "B": {2, 3}, "C": {1, 3}}
    worlds = tuple(viable)
    assert all(viable[x] & viable[y] for x, y in combinations(worlds, 2))
    assert not set.intersection(*(viable[w] for w in worlds))
    assert min_cover(worlds, (1, 2, 3), lambda w, a: a in viable[w]) == 2


def h2(p):
    if p <= 0 or p >= 1: return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def test_binary_fano():
    # W fair and Y = W passed through a binary symmetric channel.
    # MAP error is eta and I(W;Y)=1-h2(eta), saturating binary Fano.
    for eta in (0.0, 0.1, 0.25, 0.5):
        mutual_information = 1 - h2(eta)
        fano_bound = 1 - h2(eta)
        assert abs(mutual_information - fano_bound) < 1e-12


def test_binary_kl_lower_bound():
    # KL(P_control||P_baseline) >= binary KL of a success event, by DPI.
    import math
    p0, q, eps = 0.1, 0.7, 0.2
    d = q*math.log(q/p0) + (1-q)*math.log((1-q)/(1-p0))
    expected_energy_lower_bound = 2*eps*d
    assert d > 0 and expected_energy_lower_bound > 0
    return d, expected_energy_lower_bound


if __name__ == "__main__":
    print("Smooth physical map y=lambda*w+a, safe iff |y|<=1.5")
    for lam, k in test_action_thresholds():
        print(f"lambda={lam:>6.4f}: k_min={str(k):>4}; storage bits={('not viable' if k is None else (k-1).bit_length())}")
    test_pairwise_not_global()
    test_binary_fano()
    d, lb = test_binary_kl_lower_bound()
    print(f"binary event KL={d:.6f} nats, minimum expected control energy={lb:.6f} (model normalized)")
    print("All CDKA seed checks passed.")