from enum import Enum, auto


class Resolution(Enum):
    """
    time resolution
    """
    MILLISECOND = auto()
    SECOND = auto()
    MINUTE = auto()
    HOUR = auto()
    DAY = auto()
    WEEK = auto()
    MONTH = auto()
    YEAR = auto()


class Trigger(Enum):
    """
    transaction trigger
    """
    SUCCESS = auto()
    FAILED = auto()
    HANGUP = auto()  # hang-up
    CANCEL = auto()


class TransactionStatus(Enum):
    """
    交易状态
    """

    ALL_ORDER = auto()  # 全部成交
    PART_ORDER = auto()  # 部分成交
    MARKET_ORDER = auto()  # 市价成交
    LIMIT_ORDER = auto()  # 限价成交
    WITHDRAW_ORDER = auto()  # 撤单

class Order(Enum):
    """
    """
    BUY = auto()
    SELL = auto()


class TradeStatus(Enum):
    """
    """
    BUY = auto()
    SELL = auto()