# encoding:utf-8
import functools
import itertools
from typing import Union, TypeVar, Sequence, Iterable

import redis

from quantbube.utils import helper
from quantbube.utils import serializers
from .base import BaseConnection

T = TypeVar('T')


class RedisException(Exception):
    """
    redis Exception
    """
    pass


def transaction():
    """
    wrapper class
    :return:
    """

    def wrapper(func):
        """
        :return:
        """

        @functools.wraps(func)
        def inner(*args, **kwargs):
            """
            :param args:
            :param kwargs:
            :return:
            """

        return inner

    return wrapper


class RedisTimeSeries(BaseConnection):
    """
    Redis to save time-series data
    use redis sorted set as the time-series
    sorted as the desc
    """
    # todo support redis transaction
    # todo support ttl
    # todo support timezone info
    # todo only support max length 2**63-1
    # todo support parllizem and mulit threading
    # todo support lock, when add large amount data
    # todo implement redis lock
    default_serializer_class = serializers.MsgPackSerializer
    incr_format = "{key}:ID"
    hash_format = "{key}:HASH"

    def __init__(self, redis_url, db=None,
                 serializer_class=None,
                 max_length=10000, **kwargs):
        """
        :param url:
        :param db:
        :param serializer_class:
        :param max_length:
        :param ordering: set time-series order as asc or desc
        :param kwargs:
        """
        super().__init__(serializer_class)

        # todo add redis client, better refactor
        if redis_url:
            pool = redis.ConnectionPool.from_url(url=redis_url, db=db, **kwargs)
            self.conn = redis.StrictRedis(connection_pool=pool)
        else:
            self.conn = redis.StrictRedis(**kwargs)

        # todo max length to auto trim the redis data
        self.max_length = max_length

    def validate_timestamp(self):
        """
        :return:
        """
        pass

    def rapper_data(self):

        pass

    @property
    @functools.lru_cache()
    def client(self):
        """
        :return:
        """
        # todo redis client
        return self.conn

    def count(self, name):
        """
        :param name:
        :return: int
        """
        incr_key = self.incr_format.format(key=name)
        return int(self.client.get(incr_key))

    def add(self, name, timestamp, data):
        """
        incr -> result
        hmset key field value
        zadd (sorted set) key score(timestamp) value

        ensure only one timestamp corresponding one value
        :param name: key name
        :param timestamp: timestamp
        :param data:
        :return: bool
        """
        dumps_data = self.serializer.dumps(data)
        incr_key = self.incr_format.format(key=name)
        hash_key = self.hash_format.format(key=name)

        if not self.exists(name, timestamp):
            key_id = self.client.incr(incr_key)
            dumps_dict = {key_id: dumps_data}
            pipe = self.client.pipeline()
            pipe.zadd(name, timestamp, key_id)
            pipe.hmset(hash_key, dumps_dict)
            results = pipe.execute()
            return True if all(results) else False
        else:
            return False

    def exists(self, name, timestamp=None) -> bool:
        """
        :param name:
        :param timestamp:
        :return: bool
        """
        if timestamp:
            # Time complexity: O(log(N))
            result = self.client.zcount(name, min=timestamp, max=timestamp)
            return bool(result)
        else:
            return self.client.exists(name)

    def get(self, name, timestamp):
        """
        :param name:
        :param timestamp:
        :return:
        """
        hash_key = self.hash_format.format(key=name)

        result_id = self.client.zrangebyscore(name, min=timestamp, max=timestamp)
        if result_id:
            data = self.client.hmget(hash_key, result_id)
            # only one item
            return self.serializer.loads(data[0])

    def delete(self, name, start_timestamp=None, end_timestamp=None):
        """
        delete one key item or delete by timestamp order
        :param name:
        :param start_timestamp:
        :param end_timestamp:
        :return: bool or delete num
        """
        # todo large data
        incr_key = self.incr_format.format(key=name)
        hash_key = self.hash_format.format(key=name)

        if start_timestamp or end_timestamp:
            if not start_timestamp:
                start_timestamp = "-inf"
            if not end_timestamp:
                end_timestamp = "+inf"
            result_data = self.client.zrangebyscore(name,
                                                    min=start_timestamp,
                                                    max=end_timestamp,
                                                    withscores=False)
            pipe = self.client.pipeline()
            pipe.decr(incr_key, len(result_data))
            pipe.zremrangebyscore(name, min=start_timestamp, max=end_timestamp)
            pipe.hdel(hash_key, *result_data)
            pipe.execute()
        else:
            return self.client.delete(name, incr_key, hash_key)

    def trim(self, name, length=None):
        """
        trim redis sorted set key as the number of length,
        trim the data as the asc timestamp
        :param name:
        :param length:
        :return:
        """
        if length is None:
            length = self.max_length

        if length >= self.count(name):
            length = self.count(name)

        incr_key = self.incr_format.format(key=name)
        hash_key = self.hash_format.format(key=name)

        begin = 0
        end = length - 1

        result_data = self.client.zrange(name=name, start=begin, end=end, desc=False)

        if result_data:
            pipe = self.client.pipeline()
            pipe.decr(incr_key, length)
            pipe.zremrangebyrank(name, min=begin, max=end)
            pipe.hdel(hash_key, *result_data)
            pipe.execute()

    def get_slice(self, name, start=None, end=None,
                  start_index=None, limit=None, asc=True):
        """
        :param name:
        :param start:
        :param end:
        :param start_index:
        :param limit:
        :param asc:
        :return:
        """
        if asc:
            func = self.client.zrangebyscore
        else:
            func = self.client.zrevrangebyscore
        if start is None:
            start = "-inf"
        if end is None:
            end = "+inf"
        if start_index is None:
            start_index = 0

        if limit is None:
            limit = -1

        results_ids = func(name, min=start, max=end, withscores=True, start=start_index, num=limit)
        if results_ids:
            data = self.client.hmget(name, **results_ids)
            # todo dumps data
            return data

    def remove_many(self, keys, *args, **kwargs):
        """
        remove many keys
        :param keys:
        :param args:
        :param kwargs:
        :return:
        """
        chunks_data = helper.chunks(keys, 10000)

        for chunk_keys in chunks_data:
            incr_chunks = [itertools.starmap(lambda x: self.incr_format.format(key=x), chunks_data)]
            hash_chunks = [itertools.starmap(lambda x: self.hash_format.format(key=x), chunks_data)]
            pipe = self.client.pipeline()
            pipe.delete(*chunk_keys)
            pipe.delete(*incr_chunks)
            pipe.delete(*hash_chunks)
            pipe.execute()

    def add_many(self, name, data: list, *args, **kwargs):
        """
        :param name:
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        # todo refactor the data
        # todo test many item data execute how much could support 10000? 100000? 10000000?
        # remove exist data
        for index, (timestamp, item) in enumerate(data):
            if self.exists(timestamp):
                data.pop(index)  # todo bugs # index will remove when iter data
            else:
                item = self.serializer.dumps(item)

        length = len(data)

        incr_key = self.incr_format.format(key=name)
        hash_key = self.hash_format.format(key=name)

        current_incr = self.client.get(incr_key)
        result_incr = self.client.incrby(incr_key, length)

        chunks_data = helper.chunks(data, 200)

        for chunks in chunks_data:
            chunks_items = []
            pipe = self.client.pipeline()
            pipe.zadd(name, *chunks)
            pipe.hmset(hash_key, *chunks_items)
            pipe.execute()

        pipe = self.conn.pipeline()

        for timestamp, item in enumerate(data):
            dumps_data = self.serializer.dumps(item)
            pipe.zadd()

        # many data maybe have the dumplicated data

        pipe = self.conn.pipeline()
        # fist trim exist data timestamp then insert large

        # get the slice data from start to end
        # find exist ,and remove
        # then insert larage
        for item in data:
            if not self.exists(name, item["timestamp"]):
                id_ = self.client.incr("data")

        pipe.execute()

    def add_many_values(self, key, data: Union[Sequence[T], Iterable[T]], *args, **kwargs):
        """
        [{"timestamp":"","values":""}]
        :param key:
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        pipe = self.conn.pipeline()

        for item in data:
            pass

        pipe.execute()

    def iter_all(self, name):
        """
        :param name:
        :return:
        """
        hash_name = self.hash_format.format(key=name)
        result_ids = self.client.zrange(name, 0, -1, withscores=True)
        result_data = self.client.hgetall(hash_name)
        pipe = self.conn.pipeline()
        pipe.zrange(name, 0, -1, withscores=True)
        results = pipe.execute()
        return results

    def iter(self, key):
        """
        :return:
        """

    def flush(self):
        """
        flush database
        :return:
        """
        self.client.flushdb()


class RedisLock(object):
    """
    """
    pass
