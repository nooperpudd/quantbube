# encoding:utf-8

import pymongo

from quantbube.conf import settings


class MongoDBConnectionError(Exception):
    """
    """
    pass


class CallableMixin(object):
    """
    """

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass


class MongoConnection(object):
    """
    """
    config = settings.MONGO_ENGINE
    dbs = {}  # mongo db
    connections = {}  # mongo connection strings

    @classmethod
    def get_client(cls, alias="default"):
        """
        :param alias:
        :return:
        """
        if cls.connections.get(alias):
            mongo_client = cls.connections[alias]
        else:
            mongo_config = cls.config.get(alias)
            url = mongo_config.get("url")
            options = mongo_config.get("options", {})
            client = pymongo.MongoClient(url, **options)

            cls.connections[alias] = client
            mongo_client = client
        return mongo_client

    @classmethod
    def disconnect(cls, alias="default"):
        """
        :return:
        """
        if alias in cls.connections:
            cls.connections[alias].close()
            cls.connections.pop(alias)
