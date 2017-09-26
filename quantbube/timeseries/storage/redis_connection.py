# encoding:utf-8
import redis

from quantbube.conf import settings


class RedisConnectionFactory(object):
    """
    store connection pool
    redis connection factory

    REDIS_ENGINE = {
        "default": {
            "url": "redis://127.0.0.1:6379?db=1",
            "options": {
                "pool_options":{},
                "redis_options":{},
            },
        }
    }
    """
    pools = {}
    config = settings.REDIS_ENGINE

    @classmethod
    def get_client(cls, server="default"):
        """
        :param server: server config name
        :return:
        """
        redis_settings = cls.config.get(server)
        url = redis_settings.get("url")
        options = redis_settings.get("options")
        pool_options = None
        redis_options = None
        if options:
            pool_options = options.get("pool_options")
            redis_options = options.get("redis_options")

        pool = cls.create_pool(url, **pool_options)

        return redis.StrictRedis(connection_pool=pool, **redis_options)

    @classmethod
    def create_pool(cls, server, url, **kwargs):
        """
        :return:
        """
        if server not in cls.pools:
            pool = redis.ConnectionPool.from_url(url, **kwargs)
            cls.pools[server] = pool
        return cls.pools[server]

    @classmethod
    def close(cls):
        for server in cls.pools:
            pool = cls.pools[server]
            pool.disconnect()
        cls.pools = None
