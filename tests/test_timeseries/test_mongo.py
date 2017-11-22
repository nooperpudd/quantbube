import csv
import os
import unittest

from quantbube.timeseries.backends import MongoTickStore


class MongoTimeSeriesTest(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_collection(self):
        pass

    def test_get_collection(self):
        pass

    def test_add_one(self):
        pass

    def test_validator(self):
        pass

    def test_get_range(self):
        pass

    def test_add_many(self):
        pass

    def test_get_many(self):
        pass


class MongoTickStoreTest(unittest.TestCase):
    """
    """

    def setUp(self):
        self.mongo_tick = MongoTickStore(collection="ANSA")
        file = os.path.join(os.path.dirname(__file__), "tick.csv")
        with open(file, newline='', encoding='utf-8') as f:
            self.csv_reader = csv.reader(f)

        self.tick_data = [
            {
                "symbol": "GLP",
                "date": "03/03/2014,09:30:00.090",
                "bid_price": " 37.67",
                "bid_exchange": "K",
                "bid_size": "1",
                "ask_price": "39.22",
                "ask_exchange": " K",
                "ask_size": "7"
            },
            {
                "symbol": "GLP",
                "date": "03/03/2014,09:30:01.363",
                "bid_price": " 38.26",
                "bid_exchange": "N",
                "bid_size": "12",
                "ask_price": "39.18",
                "ask_exchange": " N",
                "ask_size": "1"
            }
        ]
        self.validator = {"validator": {
            "symbol": {"$type": "string", "$exists": "true"},
            "exchange": {"$type": "string", "$exists": "true"},
            "timestamp": {"$type": "date", "exists": "true"},
        }}

    def tearDown(self):
        """
        :return:
        """
        pass

    def test_add_one(self):
        """
        :return:
        """
        pass

    def test_add_repeat_data(self):
        """
        :return:
        """
        pass

    def test_add_many(self):
        """
        :return:
        """
        pass

    def test_get_many(self):
        """
        :return:
        """
        pass

    def test_query(self):
        """
        :return:
        """
        pass

    def test_ensure_index(self):
        """
        :return:
        """
        pass


class MongoBarDataTest(unittest.TestCase):
    """
    """

    def setUp(self):
        self.data = [
            {
                "symbol": "APPL",
                "Date": "2017-10-01 10:10:00",
                "high": 10.1,
                "low": 10.2,
                "open": 10.3,
                "close": 10.11,
                "volume": 1000
            },
            {
                "symbol": "APPL",
                "Date": "2017-10-01 10:11:00",
                "high": 10.2,
                "low": 10.0,
                "open": 10.16,
                "close": 9.0,
                "volume": 2000
            }
        ]

    def tearDown(self):
        pass
