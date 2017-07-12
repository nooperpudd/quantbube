# encoding:utf-8

import abc


class StrategyHandler(metaclass=abc.ABCMeta):
    """
    strategy handler base
    """
    def setup(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def on_tick(self,*args,**kwargs):
        """
        handler tick data
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def on_bar(self, *args, **kwargs):
        """
        handler bar data
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def scheduler(self, *args, **kwargs):
        """
        define schedule engine
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def handler_data(self, *args, **kwargs):
        """
        handler the data
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def on_order(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def run_simulation(self):
        """
        :return:
        """
        pass

    def run_backtest(self):
        """
        :return:
        """
        pass

    def run_live(self):
        """
        :return:
        """
        pass
