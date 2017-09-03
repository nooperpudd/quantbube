# encoding:utf-8
import abc


class BaseCompressor(abc.ABC):
    """
    """
    @abc.abstractmethod
    def compress(self, value, *args, **kwargs):
        """
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def decompress(self, value, *args, **kwargs):
        """
        :return:
        """
        raise NotImplementedError()

class DummpyCompressor(BaseCompressor):
    """
    dummpy class
    """
    def compress(self, value, *args, **kwargs):
        pass
    def decompress(self, value, *args, **kwargs):
        pass