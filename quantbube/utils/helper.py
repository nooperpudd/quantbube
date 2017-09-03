# encoding:utf-8
import itertools


def chunks(iterable, n=1000):
    """
    >>> chunks(range(6),n=2)
    ... [(0,1),(2,3),(4,5)]
    :param iterable: list, iter
    :param n: chunk split size
    :return: yield, iter
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
