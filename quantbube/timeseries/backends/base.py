# coding:utf-8
import abc

from quantbube.utils.serializers import BaseSerializer

class BaseConnection(metaclass=abc.ABCMeta):
    """
    base connection class
    """
    default_serializer_class = BaseSerializer

    def __int__(self, structure, *args, **kwargs):
        """
        :param structure:
        :param args:
        :param kwargs:
        :return:
        """
        self.structure = structure

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
    def iter(self):
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
    def contains(self, *args, **kwargs):
        """
        check data in database
        :return: bool
        """
        raise NotImplementedError()
