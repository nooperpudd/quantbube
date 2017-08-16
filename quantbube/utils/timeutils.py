# encoding:utf-8

import time
from datetime import datetime

import pytz
from dateutil import parser


def tz_now(timezone=None):
    """
    return current timezone time if timezone is None return utc time
    :param timezone:
    :return: current datetime now
    """
    if timezone:
        return datetime.now(tz=pytz.timezone(timezone))
    else:
        return datetime.now(tz=pytz.utc)


def timestamp_to_datetime(timestamp, timezone=None):
    """
    convert timestamp to datetime
    :param timestamp:
    :param timezone:
    :return:
    """
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp, timezone)


def datetime_to_timestamp(dt):
    """
    convert datetime to timestamp
    :param dt: datetime or datetime string format
    :return: int timestamp
    """
    if isinstance(dt, datetime):
        return time.mktime(dt.timetuple())
    elif isinstance(dt, str):
        dt = parser.parse(dt)
        return time.mktime(dt.timetuple())
