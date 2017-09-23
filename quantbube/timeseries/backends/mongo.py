# encoding:utf-8
import functools
from .base import TimeSeriesBase
import pymongo

from quantbube.const import  TimeResolution

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
    def __init__(self, resolution, db, url="mongodb://localhost:27017/",**kwargs):
        """
        """
        super(MongoTimeSeries, self).__init__()
        self.client = pymongo.MongoClient(url,tz_aware=True,**kwargs)
        self.database = db
        self.resolution = resolution

    @property
    @functools.lru_cache()
    def db(self):
        return self.client[self.database]



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
