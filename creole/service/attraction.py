# coding: utf-8
from ..model.attraction import Attraction


class AttractionService(object):
    @classmethod
    def _get_attraction_data_dict(cls, attraction_obj):
        _dict = {}
        for k in attraction_obj.__table__.columns._data:
            _dict[k] = getattr(attraction_obj, k, None)
        return _dict

    @classmethod
    def create_attraction(cls, country_id, city_id, address, name,
                          name_en, adult_fee, child_fee, intro_cn, intro_en):
        return Attraction.create(
            country_id=country_id, city_id=city_id,
            address=address, name=name, name_en=name_en,
            adult_fee=adult_fee, child_fee=child_fee,
            intro_cn=intro_cn, intro_en=intro_en)

    @classmethod
    def update_attraction_by_id(cls, id, **kwargs):
        return Attraction.update(id, **kwargs)

    @classmethod
    def delete_attraction_by_id(cls, id):
        return Attraction.delete(id)

    @classmethod
    def search_attraction(cls, country_id=None, city_id=None, name=None):
        raw_data = []
        attraction_list, total = Attraction.search(
            country_id=country_id, city_id=city_id, name=None)
        for attraction in attraction_list:
            raw_data.append(cls._get_attraction_data_dict(attraction))
        return raw_data, total

    @classmethod
    def get_by_id(cls, id):
        attraction = Attraction.get_by_id(id)
        return cls._get_attraction_data_dict(attraction)
