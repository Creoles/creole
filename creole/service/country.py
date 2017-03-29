# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.country import Country, City
from ..model import gen_commit_deco
from ..exc import (
    raise_error_json,
    DatabaseError,
)


class CountryService(object):
    @classmethod
    def get_by_id(cls, id):
        country_data = {'city_data': []}
        country = Country.get(id)
        if not country:
            return country_data
        country_data['name'] = getattr(country, 'name', '')
        country_data['name_en'] = getattr(country, 'name_en', '')
        country_data['id'] = country.id
        city_list = City.get_by_country_id(country.id)
        for city in city_list:
            city_dict = {}
            city_dict['name'] = getattr(city, 'name', '')
            city_dict['name_en'] = getattr(city, 'name_en', '')
            city_dict['id'] = city.id
            country_data['city_data'].append(city_dict)
        return country_data

    @classmethod
    def get_all_country(cls):
        """获取全部国家信息
        
        :return a list object:

            [
                {
                    'id': 1,
                    'name': u'中国',
                    'name_en': 'China',
                    'city_data': [
                        {
                            'id': 1,
                            'name': u'北京',
                            'name_en': 'Beijing'
                        }, {
                            'id': 2,
                            'name': u'上海',
                            'name_en': 'Shanghai'
                        }
                    ]
                }, {
                    'id': 1,
                    'name': u'美国',
                    'name_en': 'America',
                    'city_data': [
                        {
                            'id': 1,
                            'name': u'纽约',
                            'name_en': 'New York'
                        }, {
                            'id': 2,
                            'name': u'旧金山',
                            'name_en': 'San Francisco'
                        }
                    ]
                },
            ]
        """
        resp_data = []
        country_list = Country.get_all()
        for country in country_list:
            country_dict = {'city_data': []}
            country_dict['name'] = country.name
            country_dict['name_en'] = country.name_en
            country_dict['id'] = country.id
            city_list = City.get_by_country_id(country.id)
            for city in city_list:
                country_dict['city_data'].append({
                    'name': city.name,
                    'name_en': city.name_en,
                    'id': city.id
                })
            resp_data.append(country_dict)
        return resp_data

    @classmethod
    def update_by_id(cls, id, **kwargs):
        return Country.update(id, **kwargs)

    @classmethod
    @gen_commit_deco
    def delete_by_id(cls, id):
        session = DBSession()
        Country.delete(id)
        city_list = City.get_by_country_id(id)
        for city in city_list:
            session.delete(city)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

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
        city_data['id'] = city.id
        country = Country.get(city.country_id)
        city_data['country'] = {
            'name': country.name,
            'name_en': country.name_en,
            'id': country.id
        }
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
