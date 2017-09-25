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

    def get_client(self, **kwargs):
        pool = self.create_pool(**kwargs)
        return redis.StrictRedis(connection_pool=pool, **kwargs)

    def create_pool(self, **kwargs):
        """
        :return:
        """
        key = self.options["url"]
        if key not in self.pools:
            pool = redis.ConnectionPool.from_url(**kwargs)
            self.pools[key] = pool
        return self.pools[key]

    def close(self):
        for key in self.pools:
            pool = self.pools[key]
            pool.disconnect()
