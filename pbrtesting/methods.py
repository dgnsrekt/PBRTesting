def ints_are_commutative(x, y):
    return x + y == y + x


def ints_cancel(x, y):
    return (x + y) - y == x


def reversing_twice_gives_same_list(xs):
    # This will generate lists of arbitrary length (usually between 0 and
    # 100 elements) whose elements are integers.
    ys = list(xs)
    ys.reverse()
    ys.reverse()
    return xs == ys


def generated_tuples_work(t):
    # A tuple is generated as the one you provided, with the corresponding
    # types in those positions.
    return all([len(t) == 2, isinstance(t[0], bool), isinstance(t[1], str)])
