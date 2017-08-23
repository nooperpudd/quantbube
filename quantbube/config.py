# encoding:utf-8

import configparser


class ConfigError(Exception):
    """
    """
    pass


class GlobalConfig(object):
    """
    """

    TIMEZONE = "UTC"  # default timezone
    DEBUG = True

    REDIS_ENGINE = "redis://127.0.0.1:6379?db=1"
    MONGO_ENGINE = ""

    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "verbose": {
                "class": "logging.Formatter",
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
            "simple": {
                "class": "logging.Formatter",
                "format": "%(levelname)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO"
            }
        },
        "root": {
            "level": "DEBUG",
            "handle": ["console"]
        }
    }


class ConfigSettings(object):
    """
    """

    def __init__(self, ini_file):
        """
        """
        self.ini_file = ""

        self.configure = configparser.ConfigParser()

    def load_init(self):
        """
        :return:
        """


class CmdParser(object):
    """
    """

    def __init__(self):
        """
        """
        pass
