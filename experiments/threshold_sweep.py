"""Reproduce T1 informational thresholds (no third-party dependencies)."""
from cdka.finite import minimum_action_cover, minimum_memory_bits, t1_safe_actions


def main():
    print("lambda,cover_size,fixed_memory_bits,safe_actions_for_minus_one,safe_actions_for_plus_one")
    for lam in (0.0, 0.49, 0.5, 0.51, 1.0, 2.49, 2.5, 2.51, 3.0):
        relation = t1_safe_actions(lam)
        cover = minimum_action_cover(relation)
        k = None if cover is None else len(cover)
        bits = minimum_memory_bits(cover)
        print(f"{lam:g},{k},{bits},{sorted(relation[-1])},{sorted(relation[1])}")


if __name__ == '__main__':
    main()
