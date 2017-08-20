# encoding:utf-8

class RedisConnectionFactory(object):
    """
    redis connection factory
    """
    pools = {}

    def __init__(self,url,db,*args,**kwargs):
        """
        """
        self.options = kwargs
        self.url = url

    def connection_pool(self):
        """
        :return:
        """
        pass

