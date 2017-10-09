# encoding:utf-8
import functools

from quantbube.timeseries.storage import MongoConnection
from .base import TimeSeriesBase

"""
second resolution

schema
{ 
    name: "",
    data: {
    
    }
    timestamp: ""
}
"""


class MongoTimeSeries(TimeSeriesBase):
    """
    """

    def __init__(self, db, resolution, server="default"):
        """
        """
        super(MongoTimeSeries, self).__init__()
        self.server = server
        self.resolution = resolution
        self._db = db

    @property
    @functools.lru_cache()
    def client(self):
        if not getattr(self, "mongo_client"):
            self.mongo_client = MongoConnection.get_client(self.server)
        return self.mongo_client

    @property
    @functools.lru_cache()
    def db(self):
        return self.client[self._db]

    def get_collection(self, ):
        pass

    def add_many(self, key, data, *args, **kwargs):
        """
        :param key:
        :param data:
        :param args:
        :param kwargs:
        :return:
        """

    def get(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def add(self, name, *args, **kwargs):
        """
        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @property
    def query(self):
        """
        :return:
        """
        pass

    def _set_index(self):
        """
        set mongodb index
        :return:
        """
        pass


class MongoTickStore(TimeSeriesBase):
    pass
