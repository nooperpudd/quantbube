# encoding:utf-8
import functools
from typing import Union, TypeVar, Sequence, Iterable
import functools
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
    # todo support lock , when add large amount data
    # todo implement redis lock
    default_serializer_class = serializers.MsgPackSerializer
    incr_format = "{key}:ID"
    hash_format = "{key}:HASH"

    def __init__(self, redis_url, db=None,
                 serializer_class=None,
                 max_length: int = None, ordering="asc", **kwargs):
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
            pool = redis.ConnectionPool.from_url(url=redis_url, db=redis_db, **kwargs)
            self.conn = redis.StrictRedis(connection_pool=pool)
        else:
            self.conn = redis.StrictRedis(**kwargs)

        # todo max length to auto trim the redis data
        self.max_length = max_length
        self.ordering = ordering

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
        return self.client.get(incr_key)

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
        :return: bool
        """
        incr_key = self.incr_format.format(key=name)
        hash_key = self.hash_format.format(key=name)

        if not start_timestamp:
            start_timestamp = "-inf"
        if not end_timestamp:
            end_timestamp = "+inf"

        if start_timestamp or end_timestamp:

            result_data = self.client.zrangebyscore(name, min=start_timestamp, max=end_timestamp, withscores=True)
            # todo issues
            pipe = self.client.pipeline()
            pipe.decr(incr_key, len(result_data))
            pipe.zremrangebyscore(name, min=start_timestamp, max=end_timestamp)
            pipe.hdel(hash_key, result_data)
            pipe.exists()

        else:
            self.client.delete(incr_key, hash_key, name)

    def get_slice(self, key, start_timestamp=None, end_timestamp=None, ordering=None,
                  *args, **kwargs):
        """
        :param key:
        :param start_timestamp:
        :param end_timestamp:
        :param ordering:
        :return:
        """
        order = ordering if ordering else self.ordering

        if not start_timestamp:
            start_timestamp = "-inf"
        if not end_timestamp:
            end_timestamp = "+inf"

        if order == "asc":
            result_ids = self.client.zrangebyscore(key, min=start_timestamp, max=end_timestamp, withscores=True)
        else:
            result_ids = self.client.zrevrangebyscore(key, min=start_timestamp, max=end_timestamp, withscores=True)

        if result_ids:
            pipe = self.conn.pipeline()

            pipe.hmget(key, **result_ids)
            result_data = pipe.execute()
            # todo fix

    def trim(self, key, length):
        """
        trim the length in sorted key
        sorted set in asc or desc?
        :param key:
        :param length:
        :return:
        """

        # todo better refactor
        begin = length
        end = -1
        pipe = self.client.pipeline()

        results = self.conn.zremrangebyrank(key, begin, end)
        pipe.execute()
        return results

    def get_slice_by_length(self, key, start_timestamp, limit=None, ordering=None):
        """
        :param key:
        :param start_timestamp:
        :param limit:
        :param ordering:
        :return:
        """
        order = ordering if ordering else self.ordering

        pipe = self.conn.pipeline()
        # -1 means infinity
        if limit is None:
            limit = -1

        if order == "asc":
            pipe.zrangebyscore(key, start=start_timestamp, limit=limit, withscores=True)
        else:
            pipe.zrevrangebyscore(key, start=start_timestamp, limit=limit, withscores=True)

        pipe.execute()

    def remove_many(self, keys, *args, **kwargs):
        """
        remove many keys
        :param keys:
        :param args:
        :param kwargs:
        :return:
        """
        pipe = self.conn.pipeline()

        for key in keys:
            pipe.zrem(key)
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
                data.pop(index)
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

    def dumps(self):
        """
        dumps redis into db
        :return:
        """
        pass


class RedisLock(object):
    """
    """
    pass
