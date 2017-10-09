# encoding:utf-8
"""
global configuration settings
"""
TIMEZONE = "UTC"  # default timezone

DEBUG = True

LOG_LEVEL = "INFO"  # default log level

ANNUAL_FACTOR = 252 #

REDIS_ENGINE = {
    "default": {
        "url": "redis://127.0.0.1:6379?db=1",
        "options": {
            "pool_options": {},
            "redis_options": {}
        },
    }
}
MONGO_ENGINE = {
    "default": {

    }
}

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
