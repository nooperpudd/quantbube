# encoding:utf-8

import configparser


class ConfigError(Exception):
    """
    """
    pass


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


class LazySettings(object):
    pass



