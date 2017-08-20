# coding:utf-8
import abc

from quantbube.utils.serializers import BaseSerializer


class BaseConnection(abc.ABC):
    """
    base connection class
    """
    default_serializer_class = BaseSerializer
    timezone = "UTC"  # TODO FIX IMPORT SETTINGS

    def __init__(self, serializer_class=None):
        """
        :param serializer_class:
        """
        serializer_class = serializer_class or self.default_serializer_class
        self.serializer = serializer_class()

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

    def count(self, key, *args, **kwargs):
        """
        get the count of the data
        :return:
        """
        raise NotImplementedError()

    def delete(self, key, *args, **kwargs):
        """
        delete item from the data
        :param key:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def trim(self, key, length):
        """
        trim the length of the data
        :param key: the key location
        :param length: the length want to trim
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_slice(self, key, start=None, end=None, ordering=None, *args, **kwargs):
        """
        return sorted set from args
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def iter(self, key):
        """
        iter data
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def add_many(self, *args, **kwargs):
        """
        add many data
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
    def exists(self, key):
        """
        check data in database
        :return: bool
        """
        raise NotImplementedError()
