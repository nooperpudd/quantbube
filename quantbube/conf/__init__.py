# encoding:utf-8
"""
django module settings import
"""
import importlib
import os

from quantbube.conf import global_settings
from quantbube.utils.functional import LazyObject, empty

ENVIRONMENT_VARIABLE = "QUANTBUBE_SETTINGS"


class Settings(object):
    """
    set default global settings
    """
    def __init__(self, settings_module=None):
        """
        :param settings_module: user set settings
        """
        # global settings
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        self._explicit_settings = set()  # user settings

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        # user settings
        if settings_module:
            mod = importlib.import_module(self.SETTINGS_MODULE)

            for setting in dir(mod):
                if setting.isupper():
                    setting_value = getattr(mod, setting)

                    setattr(self, setting, setting_value)
                    self._explicit_settings.add(setting)

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        settings_module = self.SETTINGS_MODULE if self.SETTINGS_MODULE else global_settings
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': settings_module,
        }


class LazySettings(LazyObject):
    """
    A lazy proxy for either global Django settings or a custom settings object.
    The user can manually configure settings prior to using them. Otherwise,
    Django uses the settings module pointed to by DJANGO_SETTINGS_MODULE.
    """
    def _setup(self):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)

        if settings_module:
            self._wrapped = Settings(settings_module)
        else:
            self._wrapped = Settings()

    def __getattr__(self, name):
        """
        Return the value of a setting and cache it in self.__dict__.
        """
        if self._wrapped is empty:
            self._setup()
        val = getattr(self._wrapped, name)
        self.__dict__[name] = val
        return val

    def __setattr__(self, name, value):
        """
        Set the value of setting. Clear all cached values if _wrapped changes
        (@override_settings does this) or clear single values when set.
        """
        if name == '_wrapped':
            self.__dict__.clear()
        else:
            self.__dict__.pop(name, None)
        super(LazySettings, self).__setattr__(name, value)

    def __delattr__(self, name):
        """
        Delete a setting and clear it from cache if needed.
        """
        super(LazySettings, self).__delattr__(name)
        self.__dict__.pop(name, None)

    @property
    def configured(self):
        """
        Returns True if the settings have already been configured.
        """
        return self._wrapped is not empty

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is empty:
            return '<LazySettings [Unevaluated]>'
        return '<LazySettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }


settings = LazySettings()
