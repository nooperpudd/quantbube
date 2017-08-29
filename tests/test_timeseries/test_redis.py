# encoding:utf-8
import datetime
import unittest

from quantbube.timeseries.backends import RedisTimeSeries


class RedisStoreTest(unittest.TestCase):
    def setUp(self):
        self.time_series = RedisTimeSeries(redis_url="redis://127.0.0.1:6379?db=1")
        self.timestamp = datetime.datetime.now().timestamp()

    def tearDown(self):
        self.time_series.flush()

    def generate_data(self, key, length):
        """
        :return:
        """
        data_list = []
        for i in range(length):
            timestamp = self.timestamp + i
            data = {"value": i}
            data_list.append((timestamp, data))
            self.time_series.add(key, timestamp, data)
        return data_list

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
        key = "APPL:SECOND:2"
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
        key = "APPL:SECOND:3"
        data = {"value": 21}
        data2 = {"value": 33}
        result = self.time_series.add(key, self.timestamp, data)
        result2 = self.time_series.add(key, self.timestamp, data2)
        self.assertTrue(result)
        self.assertFalse(result2)

    def test_get(self):
        key = "APPL:SECOND:4"
        data = {"value": 10.3}
        self.time_series.add(key, self.timestamp, data)
        result = self.time_series.get(key, self.timestamp)
        self.assertDictEqual(data, result)

    def test_delete_key(self):
        key = "APPL:SECOND:5"
        incr_key = key + ":ID"
        hash_key = key + ":HASH"
        data = {"value": 10.4}
        self.time_series.add(key, self.timestamp, data)

        self.assertEqual(self.time_series.delete(key), 3)
        self.assertFalse(self.time_series.exists(key))
        self.assertFalse(self.time_series.exists(hash_key))
        self.assertFalse(self.time_series.exists(incr_key))

    def test_delete_one_timestamp(self):

        key = "APPL:SECOND:6"
        data = {"value": 10.3}
        hash_key = key + ":HASH"
        self.time_series.add(key, self.timestamp, data)
        self.time_series.delete(key, start_timestamp=self.timestamp,
                                end_timestamp=self.timestamp)
        self.assertEqual(self.time_series.count(key), 0)

        client = self.time_series.client
        self.assertEqual(client.hgetall(hash_key), {})
        self.assertEqual(client.zrange(key, 0, -1), [])

    def test_delete_with_start_timestamp(self):
        key = "APPL:SECOND"
        data_list = self.generate_data(key, 10)

        start_timestamp = self.timestamp + 3

        self.time_series.delete(key, start_timestamp=start_timestamp)
        self.assertEqual(self.time_series.count(key), 3)

        for item in data_list[:]:
            if item[0] >= start_timestamp:
                data_list.remove(item)

        for timestamp, data in data_list:
            result = self.time_series.get(key, timestamp)
            self.assertEqual(result, data)

    def test_delete_with_end_timestamp(self):
        key = "APPL:SECOND"
        data_list = self.generate_data(key, 10)

        end_timestamp = self.timestamp + 5

        self.time_series.delete(key, end_timestamp=end_timestamp)
        self.assertEqual(self.time_series.count(key), 4)

        for item in data_list[:]:
            if item[0] <= end_timestamp:
                data_list.remove(item)

        for timestamp, data in data_list:
            result = self.time_series.get(key, timestamp)
            self.assertEqual(result, data)

    def test_delete_with_start_and_end(self):
        key = "APPL:SECOND"
        data_list = self.generate_data(key, 10)

        start_timestamp = self.timestamp + 3
        end_timestamp = self.timestamp + 6

        self.time_series.delete(key, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        self.assertEqual(self.time_series.count(key), 6)

        for item in data_list[:]:
            if start_timestamp <= item[0] <= end_timestamp:
                data_list.remove(item)

        for timestamp, data in data_list:
            result = self.time_series.get(key, timestamp)
            self.assertEqual(result, data)

    def test_trim(self):
        key = "APPL:MINS:10"
        data_list = self.generate_data(key, 20)
        self.time_series.trim(key, 5)
        self.assertEqual(self.time_series.count(key), 15)

        data_list = sorted(data_list, key=lambda k: k[0])

        result_data_list = data_list[5 - len(data_list):]
        trim_data_list = data_list[:5]

        for timestamp, data in result_data_list:
            result = self.time_series.get(key, timestamp)
            self.assertEqual(result, data)
        for timestamp, _ in trim_data_list:
            result = self.time_series.get(key, timestamp)
            self.assertIsNone(result)

    def test_trim_length_none(self):
        key = "APPL:MINS:15"
        data_list = self.generate_data(key, 30)
        self.time_series.trim(key)
        self.assertEqual(self.time_series.count(key), 0)
        length = self.time_series.max_length
        trim_data_list = data_list[:length]

        for timestamp, _ in trim_data_list:
            result = self.time_series.get(key, timestamp)
            self.assertIsNone(result)




        # todo get all
        # self.assertListEqual()

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
