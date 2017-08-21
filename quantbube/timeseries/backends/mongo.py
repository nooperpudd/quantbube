# encoding:utf-8

from .base import BaseConnection
import pymongo


class MongoTimeSeries(BaseConnection):
    """
    """
    def __init__(self):
        """
        """
        self.client = pymongo.MongoReplicaSetClient

    def get(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        pass
    def add(self, *args, **kwargs):
        """
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
