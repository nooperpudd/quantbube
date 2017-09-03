# coding:utf-8
import abc

from quantbube.utils.compression import DummpyCompressor
from quantbube.utils.serializers import DummySerializer


class BaseConnection(abc.ABC):
    """
    base connection class
    """
    default_serializer_class = DummySerializer
    default_compressor_class = DummpyCompressor

    def __init__(self, serializer_class=None, compressor_class=None):
        """
        :param serializer_class:
        :param compressor_class:
        """
        serializer_class = serializer_class or self.default_serializer_class
        self.serializer = serializer_class()
        compressor_class = compressor_class or self.default_compressor_class
        self.compressor = compressor_class()

    @abc.abstractmethod
    def add(self, *args, **kwargs):
        """
        add item to storage
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        """
        get one item from storage
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def count(self, name):
        """
        get the count of the data
        :return:
        """
        raise NotImplementedError()

    def delete(self, name, *args, **kwargs):
        """
        delete item from the data
        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def trim(self, name, length):
        """
        trim the length of the data
        :param name: the key location
        :param length: the length want to trim
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_slice(self, name, start=None, end=None, asc=True):
        """
        return sorted set from args
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def add_many(self, key, data, *args, **kwargs):
        """
        add many data
        :param key:
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_many(self, *args, **kwargs):
        """
        remove many data
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, name, timestamp=None):
        """
        check data in database
        :return: bool
        """
        raise NotImplementedError()
