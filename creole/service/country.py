# coding: utf-8
from ..model.country import Country, City
from ..model import gen_commit_deco


class CountryService(object):
    @classmethod
    def get_by_id(cls, id):
        country_data = {'city_data': []}
        country = Country.get(id)
        if not country:
            return country_data
        country_data['name'] = getattr(country, 'name', '')
        country_data['name_en'] = getattr(country, 'name_en', '')
        city_list = City.get_by_country_id(country.id)
        for city in city_list:
            city_dict = {}
            city_dict['name'] = getattr(city, 'name', '')
            city_dict['name_en'] = getattr(city, 'name_en', '')
            country_data['city_data'].append(city_dict)
        return country_data

    @classmethod
    def update_by_id(cls, id, **kwargs):
        return Country.update(id, **kwargs)

    @classmethod
    @gen_commit_deco
    def delete_by_id(cls, id):
        Country.delete(id)

    @classmethod
    def create_country(cls, name, name_en):
        Country.create(name, name_en)


class CityService(object):
    @classmethod
    def get_by_id(cls, id):
        city_data = {}
        city = City.get(id)
        if not city:
            return city_data
        city_data['name'] = city.name
        city_data['name_en'] = city.name_en
        country = Country.get(city.country_id)
        city_data['country'] = {'name': country.name, 'name_en': country.name_en}
        return city_data

    @classmethod
    def update_by_id(cls, id, **kwargs):
        City.update(id, **kwargs)

    @classmethod
    def delete_by_id(cls, id):
        City.delete(id)

    @classmethod
    def create_city(cls, name, name_en, country_id):
        City.create(name, name_en, country_id)
