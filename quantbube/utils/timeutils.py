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
        return datetime.now()

