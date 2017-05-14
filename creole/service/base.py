# coding: utf-8
import datetime

from ..util import datetime_to_timestamp


class BaseService(object):
    @classmethod
    def _get_db_obj_data_dict(cls, obj):
        _dict = {}
        if obj is None:
            return _dict
        for k in obj.__table__.columns._data:
            value = getattr(obj, k, None)
            if isinstance(value, datetime.datetime):
                value = datetime_to_timestamp(value)
            _dict[k] = value
        return _dict

