# encoding:utf-8

import redis
import contextlib


class RedisConnectionFactory(object):
    """
    store connection pool
    redis connection factory
    """
    pools = {}

    def __init__(self):
        """
        :param kwargs:
        """
        pass

    def get_or_create_connection_pool(self):
        """
        :return:
        """
        if self.redis_url:
            pool = redis.ConnectionPool.from_url(url=self.redis_url, db=self.db, **self.options)
            self.conn = redis.StrictRedis(connection_pool=pool)
        else:
            self.conn = redis.StrictRedis(**kwargs)

        pass

    def get_connection(self):
        """
        :return:
        """

    def rest(self):
        """
        :return:
        """
        pass


