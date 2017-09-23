# encoding:utf-8

import redis


class RedisConnectionFactory(object):
    """
    store connection pool
    redis connection factory
    """
    pools = {}

    def __init__(self, **kwargs):
        """
        """
        self.options = kwargs

    def get_connection(self, **kwargs):
        pool = self.get_or_create_connection_pool(**kwargs)
        client = redis.StrictRedis(connection_pool=pool, **kwargs)
        return client

    def get_or_create_connection_pool(self, **kwargs):
        """
        :return:
        """
        key = self.options["url"]
        if key not in self.pools:
            pool = redis.ConnectionPool.from_url(**kwargs)
            self.pools[key] = pool
        return self.pools[key]

    def close(self):
        pass