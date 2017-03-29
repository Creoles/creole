class BaseService(object):
    @classmethod
    def _get_db_obj_data_dict(cls, obj):
        _dict = {}
        if obj is None:
            return _dict
        for k in obj.__table__.columns._data:
            _dict[k] = getattr(obj, k, None)
        return _dict

