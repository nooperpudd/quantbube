# encoding:utf-8
import functools

import pytz
from bson.codec_options import CodecOptions
from pymongo import WriteConcern
import datetime
from quantbube.conf import settings
from quantbube.timeseries.storage import MongoConnection
from .base import TimeSeriesBase


class MongoTimeSeries(TimeSeriesBase):
    """
    """

    def __init__(self, collection, db="quantbube", server="default", validator=None):
        """
        :param db:
        :param server:
        :param validator:
        """
        super(MongoTimeSeries, self).__init__()
        self.server = server

        self._db = db
        self._collection = collection
        self.client = MongoConnection.get_client(server)

    @property
    @functools.lru_cache()
    def db(self):
        return self.client[self._db]

    @property
    @functools.lru_cache()
    def collection(self):
        options = CodecOptions(tz_aware=True, tzinfo=pytz.timezone(settings.TIMEZONE))

        return self.db.get_collection(self._collection,
                                      codec_options=options,
                                      write_concern=WriteConcern())

    def create_collection(self, collection, validator=None):
        """
        :param collection:
        :param validator:
        :return:
        """
        # https://docs.mongodb.com/manual/reference/command/create/

        options = CodecOptions(tz_aware=True, tzinfo=pytz.timezone(settings.TIMEZONE))

        self.db.create_collection(name=collection,
                                  options=options,
                                  validator=validator,
                                  validationAction="error")

    def get_collection(self, collection):
        """
        get collection
        :param collection:
        :return:
        """
        # todo write concern

        options = CodecOptions(tz_aware=True, tzinfo=pytz.timezone(settings.TIMEZONE))

        return self.db.create_collection(collection, codec_options=options,
                                         write_concern=WriteConcern())

    def create_validate(self, schema):
        """
        :param schema:
        :return:
        """
        collection = self.get_collection(self.collection)

    def ensure_unique(self):
        """
        :return:
        """
        pass

    def ensure_index(self):
        """
        create index core
        :return:
        """
        # todo create index

        pass

    def _bulk_write(self):
        """
        :return:
        """
        #  http://api.mongodb.com/python/current/examples/bulk.html
        # todo support mongo bulk write

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



    def _set_index(self):
        """
        set mongodb index
        :return:
        """
        pass


class MongoTickStore(MongoTimeSeries):
    # https://jira.mongodb.org/browse/PYTHON-1064
    """

    """
    def add(self, symbol, timestamp, data):
        """
        :param symbol:
        :param timestamp:
        :param data:
        :return:
        """
        collection = self.db[self.collection]

        collection.insert_one(document=document)


class MongoBarStore(MongoTimeSeries):
    def __init__(self, resolution):
        self.resolution = resolution
