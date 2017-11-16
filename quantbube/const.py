from enum import Enum

# set granularity expired time in redis

GRANULARITIES_TTL = {
    "second": 60 * 60,  # 1 hour
    "minute": 60 * 60 * 24,  # 1 day
    "hour": 60 * 60 * 24 * 7,  # 7 day
    "day": 60 * 60 * 24 * 30,  # 1 month
}


class DatetimeResolution(Enum):
    """
    time resolution
    """
    MILLISECOND = 1
    SECOND = 2
    MINUTE = 3
    HOUR = 4
    DAY = 5
    WEEK = 6
    MONTH = 6
    YEAR = 7


class TriggerStatus(Enum):
    """
    transaction trigger
    """
    SUCCESS = 1
    FAILED = 2
    HANGUP = 3  # hang-up
    CANCEL = 4


class TransactionStatus(Enum):
    """
    Transaction Status
    """
    FULL_ORDER = 1  # FULL ORDER
    PART_ORDER = 2  # 部分成交
    MARKET_ORDER = 3  # 市价成交
    LIMIT_ORDER = 4  # 限价成交
    WITHDRAW_ORDER = 5  # 撤单


class OrderStatus(Enum):
    """
    """
    BUY = 1
    SELL = 2


class TradeStatus(Enum):
    """
    """
    BUY = 1
    SELL = 2
