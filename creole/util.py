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
    def __init__(self, **kwargs):
        self._items = dict()
        self._values = []
        for item in kwargs:
            if len(item) not in (2, 3):
                raise ValueError(item)
            elif item[1] in self._values:
                raise ValueError('Duplicate value: %r', item[1])
            self._items[item[0]] = EnumItem(**item)
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
