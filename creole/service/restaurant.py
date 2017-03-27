# coding: utf-8
from ..model.restaurant import RestaurantCompany, Restaurant


class RestaurantCompanyService(object):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = RestaurantCompany.get_by_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        return company_info

    @classmethod
    def delete_restaurant_company_by_id(cls, id):
        return RestaurantCompany.delete(id)

    @classmethod
    def update_restaurant_company_by_id(cls, id, **kwargs):
        return RestaurantCompany.update(id, **kwargs)

    @classmethod
    def create_restaurant_company(cls, name, name_en):
        return RestaurantCompany.create(name=name, name_en=name_en)


class RestaurantService(object):
    @classmethod
    def _get_restaurant_data_dict(cls, restaurant_obj):
        _dict = {}
        for k in restaurant_obj.__table__.columns._data:
            _dict[k] = getattr(restaurant_obj, k, None)
        return _dict

    @classmethod
    def get_by_id(cls, id):
        restaurant = Restaurant.get_by_id(id)
        return cls._get_restaurant_data_dict(restaurant)

    @classmethod
    def delete_restaurant_by_id(cls, id):
        return Restaurant.delete(id)

    @classmethod
    def update_restaurant_by_id(cls, id, **kwargs):
        return Restaurant.update(id, **kwargs)

    @classmethod
    def create_restaurant(cls, name, name_en, restaurant_type,
                          country_id, city_id, company_id, address,
                          contact, telephone, intro_cn=None, intro_en=None):
        return Restaurant.create(
            name=name, name_en=name_en, restaurant_type=restaurant_type,
            country_id=country_id, city_id=city_id, company_id=company_id,
            address=address, contact=contact, telephone=telephone,
            intro_cn=intro_cn, intro_en=intro_en
        )
