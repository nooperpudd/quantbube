# encoding:utf-8

import redis

from quantbube.utils import serializers
from .base import BaseConnection


class RedisException(Exception):
    """
    redis Exception
    """
    pass


class RedisTimeSeries(BaseConnection):
    """
    Redis to save time-series data
    sorted as the desc
    """
    default_serializer_class = serializers.MsgPackSerializer

    def __int__(self, redis_url=None, redis_db=None, data_schema=None,
                serializer_class=None,
                max_length: int = None, **kwargs):
        """
        :param url:
        :param db:
        :param data_schema:
        :param serializer_class:
        :param max_length:
        :param kwargs:
        """
        # todo add redis client, better refactor
        if redis_url:
            pool = redis.ConnectionPool.from_url(url=redis_url, db=redis_db, **kwargs)
            self.conn = redis.StrictRedis(connection_pool=pool)
        else:
            self.conn = redis.StrictRedis(**kwargs)

        serializer_class = serializer_class or self.default_serializer_class
        self.serializer = serializer_class(data_schema)
        # todo max length to auto trim the redis data
        self.max_length = max_length

    def add(self, name, timestamp, **data):
        """
        :param name: key name
        :param timestamp: timestamp
        :param data:
        :return:
        """
        results = self.serializer.dumps(data)
        return self.conn.zadd(name, timestamp, results)

    def get(self, name, timestamp):
        """
        :return:
        """
        results = self.conn.zrangebyscore(name, min=timestamp, max=timestamp, num=1, withscores=True)
        if results:
            return self.serializer.loads(results)

    def delete(self, key, start_timestamp=None, end_timestamp=None):
        """
        :param key:
        :param start_timestamp:
        :param end_timestamp:
        :return: bool
        """
        if start_timestamp and end_timestamp:
            self.conn.zremrangebyscore(key, start_timestamp, end_timestamp)
        elif start_timestamp and end_timestamp is None:
            self.conn.zremrangebyscore(key, start_timestamp, "+inf")
        elif start_timestamp is None and end_timestamp:
            self.conn.zremrangebyscore(key, "-inf", end_timestamp)
        else:
            self.conn.zrem(key)

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
        results = self.conn.zremrangebyrank(key, begin, end)
        return results

    def contains(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pipe = self.conn.pipeline()
        pipe.execute()

    def get_slice(self, key, start=None, end=None, ordering=None, *args, **kwargs):
        """
        :param key:
        :param start:
        :param end:
        :param ordering:
        :param args:
        :param kwargs:
        :return:
        """

        pipe = self.conn.pipeline()
        pipe.execute()

    def remove_many(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def add_many(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def all(self, key):
        pipe = self.conn.pipeline(transaction=True)
        pipe.zrange(key, 0, -1, withscores=True)
        result = pipe.execute()
        return result

    def iter(self):
        """
        :return:
        """

    def flush(self):
        """
        :return:
        """

    def execute(self):
        """
        :return:
        """
        pass
