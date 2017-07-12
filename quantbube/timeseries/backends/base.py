# encoding:utf-8

import abc


class BaseSerializer(metaclass=abc.ABCMeta):
    """
     The base serializer class,
    only defines the signature for loads and dumps
    """

    @abc.abstractmethod
    def loads(self, serialized_data):
        """

        :param serialized_data: the structure data need to be
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def dumps(self, data):
        """
        :param data:
        :return:
        """
        raise NotImplementedError()


class BaseConnection(metaclass=abc.ABCMeta):
    """
    base connect class
    """

    def __int__(self, structure, *args, **kwargs):
        """
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

    @abc.abstractmethod
    def count(self, key, *args, **kwargs):
        """
        get the count of the data
        :return:
        """
        raise NotImplementedError()

    def delete(self, key, *args, **kwargs):
        """
        delete item from the data
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
    def to_pandas(self):
        """
        convert data to pandas DataFrame
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
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def contains(self, *args, **kwargs):
        """
        :return:
        """
        raise NotImplementedError()
