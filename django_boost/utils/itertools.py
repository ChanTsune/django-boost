from functools import partial
from itertools import islice


def take(n, iterable):
    """Return first *n* items of the iterable as a list.

    example ::

    >>> take(3, range(10))
    [0, 1, 2]
    >>> take(5, range(3))
    [0, 1, 2]

    Effectively a short replacement for ``next`` based iterator consumption
    when you want more than one item, but less than the whole iterator.
    """
    return list(islice(iterable, n))


def chunked(iterable, n):
    """Break *iterable* into lists of length *n*:

    example ::

    >>> list(chunked([1, 2, 3, 4, 5, 6], 3))
    [[1, 2, 3], [4, 5, 6]]

    If the length of *iterable* is not evenly divisible by *n*, the last
    returned list will be shorter:

    example ::

    >>> list(chunked([1, 2, 3, 4, 5, 6, 7, 8], 3))
    [[1, 2, 3], [4, 5, 6], [7, 8]]


    To use a fill-in value instead, see the :func:`grouper` recipe.
    :func:`chunked` is useful for splitting up a computation on a large number
    of keys into batches, to be pickled and sent off to worker processes. One
    example is operations on rows in MySQL, which does not implement
    server-side cursors properly and would otherwise load the entire dataset
    into RAM on the client.
    """
    return iter(partial(take, n, iter(iterable)), [])
