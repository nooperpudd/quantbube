# encoding:utf-8


class Bar(object):
    """
    bar data
    """
    def __int__(self, symbol, timestamp, open, close,
                high, low, adj_close, volume,
                resolution, period):
        """
        :return:
        """
        self.symbol = symbol

        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adj_close = adj_close
        self.period = period
        self.resolution = resolution
