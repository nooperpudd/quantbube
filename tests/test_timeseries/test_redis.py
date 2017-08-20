# encoding:utf-8

import datetime
import unittest

from quantbube.timeseries.backends import RedisTimeSeries


class RedisStoreTest(unittest.TestCase):
    """
    """

    def setUp(self):
        self.time_series = RedisTimeSeries(redis_url="redis://127.0.0.1:6379?db=1")
        self.timestamp = datetime.datetime.now().timestamp()


    def tearDown(self):
        self.time_series.flush()

    def test_add(self):
        key = "APPL:SECOND:1"

        data = {
            "value": 21,
            "volume": 11344.34,
            "asks": [{"ask_1": 10, "price": 21}],
            "bid": [{"bid_1": 10, "price": 20}]
        }
        result = self.time_series.add(key, self.timestamp, data)
        self.assertTrue(result)

    def test_add_repeated_values(self):
        """
        ensure once insert repeated data
        """
        key = "APPL:SECOND:1"
        timestamp2 = self.timestamp + 1
        data = {"value": 1}
        result1 = self.time_series.add(key, self.timestamp, data)
        result2 = self.time_series.add(key, timestamp2, data)

        result_data1 = self.time_series.get(key, self.timestamp)
        result_data2 = self.time_series.get(key, timestamp2)

        self.assertTrue(result1)
        self.assertTrue(result2)

        self.assertDictEqual(data, result_data1)
        self.assertDictEqual(data, result_data2)

    def test_add_repeated_timestamp(self):
        """
        ensure each timestamp mapping to each value
        """
        key = "APPL:SECOND:1"
        data = {"value": 21}
        data2 = {"value": 33}
        result = self.time_series.add(key, self.timestamp, data)
        result2 = self.time_series.add(key, self.timestamp, data2)
        self.assertTrue(result)
        self.assertFalse(result2)

    def test_get(self):
        key = "APPL:SECOND:1"
        data = {"value": 10.3}
        self.time_series.add(key, self.timestamp, data)
        result = self.time_series.get(key, self.timestamp)
        self.assertDictEqual(data, result)


    def test_ttl(self):
        """
        :return:
        """

    def test_add_many(self):
        """
        :return:
        """
        pass

    def test_all(self):
        """
        :return:
        """
        pass
