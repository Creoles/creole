# coding: utf-8
import types
import warnings
import functools

from .util import import_string 
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
        return self

    @check_setting_initialized
    def load_from_object(self, obj):
        #  import pdb
        #  pdb.set_trace()
        if isinstance(obj, basestring):
            obj = import_string(obj)
        for key, value in obj.__dict__.iteritems():
            if key.isupper() and \
                    not key.startswith('__'):
                self._settings[key] = value
        return self

    def __getitem__(self, key):
        return self._settings.get(key)

    def __getattr__(self, key):
        val = self.__dict__.get(key, None)
        if not val:
            return self.__getitem__(key)
        return val


setting = CreoleSetting()
setting.load_from_object(settings)
"""Get the environ var like this:
    setting.var_name
or  setting['var_name']
"""
