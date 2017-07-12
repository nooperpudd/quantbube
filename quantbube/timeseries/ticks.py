# encoding:utf-8


class Tick(object):
    """
    """
    # __slots__ =  ("","")
    def __int__(self,timestamp,symbol,bid,ask,bid_amount,ask_amount):
        """
        :return:
        """
        self.timestamp = timestamp
        self.symbol = symbol
        self.bid = bid
        self.ask = ask
        self.bid_amount = bid_amount
        self.ask_amount = ask_amount

