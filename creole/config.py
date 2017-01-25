import os
import types
import warnings
import functools

from .util import load_module_from_string
from . import settings


setting_initialized = False


def check_setting_initialized(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global setting_initialized
        if setting_initialized:
            warnings.warn('Have already load the settings!')
            return
        func(*args, **kwargs)
        setting_initialized = True
    return wrapper


class CreoleSetting(object):
    def __init__(self):
        self._settings = {}

    @check_setting_initialized
    def load_from_pyfile(self, file_name):
        d = types.ModuleType('setting')
        d.__file__ = file_name.__name__
        try:
            with open(file_name) as f:
                exec(
                    compile(f.read(), file_name, 'exec'),
                    d.__dict__
                )
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.load_from_object(d)

    @check_setting_initialized
    def load_from_object(self, obj):
        if isinstance(obj, basestring):
            obj = load_module_from_string(obj)
        for key, value in obj.__dict__.iteritems():
            if not key.startswith('__'):
                self._settings[key] = value

    def __getitem__(self, key):
        return self._settings.get(key)

    def __getattr__(self, key):
        val = self.__dict__.get(key, None)
        if not val:
            return self.__getitem__(key)
        return val


class EnvReader(object):
    """Get the settings from the Environ.

    Usage: r = EnvReader()
           r.get('SETTING_VAR_NAME')
    """
    def __init__(self):
        self._setting_dict = {}

    def _normalize(self, key):
        return key.strip()

    def __getitem__(self, key):
        value = self._setting_dict.get(key, None)
        if not value:
            value = os.getenv(key, None)
            self._setting_dict.__setitem__(key, value)
        return value

    def get(self, key, default=None):
        value = self.__getitem__(key)
        if value is None:
            value = default
        return value


def get_setting_manager():
    return EnvReader()


setting = CreoleSetting().load_from_object(settings)
"""Get the environ var like this:
    setting.var_name
or  setting['var_name']
"""
