# coding: utf-8
import os
import sys
import time
import datetime


_func = lambda x: x is not None and len(x) != 0


def timestamp_to_date(timestamp):
    t = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d", t)


def datetime_to_timestamp(dt):
    if isinstance(dt, datetime.datetime):
        return time.mktime(dt.timetuple())
    return 0


class CachedProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        value = self.func(instance)
        setattr(instance, self.func.__name__, value)
        return value


cached_property = CachedProperty


class EnumItem(object):
    def __init__(self, key, value, help=''):
        self.key = key
        self.value = value
        self.help = help


class Enum(object):
    def __init__(self, *args):
        self._items = dict()
        self._values = []
        for item in args:
            if len(item) not in (2, 3):
                raise ValueError(item)
            elif item[1] in self._values:
                raise ValueError('Duplicate value: %r', item[1])
            self._items[item[0]] = EnumItem(*item)
            self._values.append(item[1])

    def __getattr__(self, key):
        try:
            return self._items[key].value
        except KeyError:
            raise AttributeError(key)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def values(self):
        return self._values

    def keys(self):
        return self._items.keys()

    def items(self):
        return self._items.iteritems()


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

    def get_int(self, key, default=None):
        value = self.__getitem__(key)
        if value is not None:
            return int(value)
        return default


def get_setting_manager():
    return EnvReader()


def import_string(imp_name):
    imp_name = str(imp_name).replace(':', '.')
    try:
        __import__(imp_name)
    except ImportError:
        if '.' not in imp_name:
            raise
    else:
        return sys.modules[imp_name]
    mod_name, obj_name = imp_name.rsplit('.', 1)
    try:
        mod = __import__(mod_name, None, None, [obj_name])
    except ImportError:
        mod = import_string(mod_name)
    try:
        return getattr(mod, obj_name)
    except AttributeError as e:
        raise ImportError(e)
