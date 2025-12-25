from collections.abc import Callable


def minimize_seq[T](
    f: Callable[[tuple[T, ...]], bool], seq: tuple[T, ...], /
) -> tuple[T, ...] | None:
    """Find the minimal subsequence of `seq` that satisfies `f`.

    Let x ≺ y mean x is a proper subsequence of y. Obviously, ≺ is a partial order.

    Assumptions:
    - x ≺ y -> f(x) -> f(y).
    - f(x) ∧ f(y) -> x ≺ y ∨ y ≺ x ∨ x = y.
    - `seq` does not have repeated elements.
    (x, y are any subsequences of `seq`.)

    Returns `None` if such subsequence does not exist.
    """
    # Check the most probable cases first
    if f(()):
        return ()
    if not f(seq):
        return None

    current = seq

    # Try to remove elements one by one, and see if f still holds.
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(current):
            candidate = current[:i] + current[i + 1 :]
            if f(candidate):
                current = candidate
                changed = True
            else:
                i += 1

    return current


if __name__ == "__main__":

    def _test_f[T](min_seq: tuple[T, ...]) -> Callable[[tuple[T, ...]], bool]:
        """Generate a test function for `minimize_seq`."""

        def f(sub_seq: tuple[T, ...]) -> bool:
            last_pos = -1
            for a in min_seq:
                if a not in sub_seq:
                    return False
                pos = sub_seq.index(a)
                if pos <= last_pos:
                    return False
                last_pos = pos
            return True

        return f

    assert minimize_seq(_test_f(()), (0, 1, 2, 3)) == ()
    assert minimize_seq(_test_f((0, 1, 2, 3)), (0, 1, 2, 3)) == (0, 1, 2, 3)

    assert minimize_seq(_test_f((1, 2, 3)), (0, 1, 2, 3, 4)) == (1, 2, 3)
    assert minimize_seq(_test_f((1, 2, 4)), (0, 1, 2, 3, 4)) == (1, 2, 4)
    assert minimize_seq(_test_f((0, 4)), (0, 1, 2, 3, 4)) == (0, 4)

    print("All tests passed.")
