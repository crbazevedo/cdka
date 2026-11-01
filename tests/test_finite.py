"""Independent exhaustive tests of finite action sufficiency."""
from itertools import product
import unittest

from cdka.finite import (
    action_decoding, dowker_simplices, minimum_action_cover,
    minimum_memory_bits, t1_safe_actions, t1_expected_cover_size,
    equilibrium,
)


def independent_min_messages(safe):
    """Independent partition search, rather than enumerating action covers."""
    worlds = tuple(safe)
    if not worlds:
        return 0
    if any(not actions for actions in safe.values()):
        return None
    for num_messages in range(1, len(worlds) + 1):
        for encoding in product(range(num_messages), repeat=len(worlds)):
            if any(
                not set.intersection(*(set(safe[w]) for w, m in zip(worlds, encoding) if m == code))
                for code in set(encoding)
            ):
                continue
            return len(set(encoding))
    return None


class FiniteTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(minimum_action_cover({}), ())
        self.assertEqual(minimum_memory_bits(()), 0)

    def test_infeasible(self):
        self.assertIsNone(minimum_action_cover({"a": {1}, "b": set()}))
        self.assertIsNone(minimum_memory_bits(None))

    def test_noncomparable_actions(self):
        self.assertEqual(len(minimum_action_cover({"w1": {1, "a"}, "w2": {"a"}})), 1)

    def test_pairwise_does_not_imply_triple(self):
        relation = {"A": {1, 2}, "B": {2, 3}, "C": {1, 3}}
        complex_ = dowker_simplices(relation)
        self.assertEqual(len(complex_), 6)
        self.assertNotIn(frozenset(relation), complex_)
        self.assertEqual(len(minimum_action_cover(relation)), 2)

    def test_all_relations_three_worlds_three_actions(self):
        """Exhaustively cross-check 512 binary relations using partitions."""
        worlds = range(3)
        actions = range(3)
        for mask in range(1 << 9):
            relation = {w: {a for a in actions if mask & (1 << (3*w + a))}
                        for w in worlds}
            cover = minimum_action_cover(relation)
            expected = independent_min_messages(relation)
            self.assertEqual(None if cover is None else len(cover), expected, mask)
            decoding = action_decoding(relation)
            if decoding is not None:
                self.assertTrue(all(decoding[w] in relation[w] for w in worlds))

    def test_t1_boundaries(self):
        for lam, expected in [(0, 1), (0.5, 1), (0.500001, 2),
                              (1.0, 2), (2.5, 2), (2.500001, None)]:
            cover = minimum_action_cover(t1_safe_actions(lam))
            self.assertEqual(None if cover is None else len(cover), expected)
            self.assertEqual(t1_expected_cover_size(lam), expected)

    def test_t1_stable_equilibria(self):
        # d/dx[-x+lam*w+u] = -1; global exponential convergence for every lambda.
        self.assertAlmostEqual(equilibrium(2.0, 1, -1), 1.0)
        self.assertAlmostEqual(equilibrium(2.0, -1, 1), -1.0)

    def test_finite_horizon_shifts_thresholds(self):
        from math import log
        # horizon ln(2) gives gain=1/2 and effective safe bound=3.
        h = log(2)
        for lam, expected in [(2.0, 1), (2.01, 2), (4.0, 2), (4.01, None)]:
            cover = minimum_action_cover(t1_safe_actions(lam, horizon=h))
            self.assertEqual(None if cover is None else len(cover), expected)

    def test_more_actions_can_reduce_required_memory(self):
        old = minimum_action_cover(t1_safe_actions(1.0))
        expanded = minimum_action_cover(t1_safe_actions(1.0, actions=(-1, 0, 1)))
        self.assertEqual(minimum_memory_bits(old), 1)
        self.assertEqual(minimum_memory_bits(expanded), 0)

    def test_invalid_horizon_and_actions(self):
        for invalid in (float('nan'), 0.0, -1.0, float('-inf')):
            with self.assertRaises(ValueError):
                t1_safe_actions(1.0, horizon=invalid)
        with self.assertRaises(ValueError):
            t1_safe_actions(1.0, actions=(float('nan'),))

    def test_t1_invalid_parameters(self):
        for invalid in (float('nan'), float('inf'), -0.1):
            with self.assertRaises(ValueError):
                t1_safe_actions(invalid)
        with self.assertRaises(ValueError):
            t1_safe_actions(1.0, boundary=0.0)


if __name__ == '__main__':
    unittest.main()
