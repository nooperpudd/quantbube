import csv
import os
import unittest


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
        file = os.path.join(os.path.dirname(__file__), "tick.csv")
        with open(file, newline='', encoding='utf-8') as f:
            self.csv_reader = csv.reader(f)
        self.data = {"Date": "2017-10-01",
                     "high": 10.1,
                     "low": 10.2,
                     "open": 10.3,
                     "close": 10.11,
                     "volume": 1000}
        self.validator = {
            "validator": {
                "symbol":"",
            }
        }

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
        pass

    def tearDown(self):
        pass
