# encoding:utf-8
import abc


class BaseSerializer(abc.ABC):
    """
    The base serializer class,
    only defines the signature for loads and dumps
    """

    @abc.abstractmethod
    def loads(self, data, *args, **kwargs):
        """
        Deserialize the data
        :param data: the structure data need to be
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def dumps(self, data, *args, **kwargs):
        """
        Serialize ``data`` to kinds of type
        :param data:
        :return:
        """
        raise NotImplementedError()