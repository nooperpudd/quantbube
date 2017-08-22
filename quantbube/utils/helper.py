# encoding:utf-8

import itertools


def chunks(iterable, n=10000):
    """
    :param iterable:
    :param n:
    :return:
    """
    # todo doc
    # todo examples

    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
