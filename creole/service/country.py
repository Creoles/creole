# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.country import Country, City
from ..model import gen_commit_deco
from ..exc import (
    raise_error_json,
    DatabaseError,
)
from .base import BaseService


class CountryService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        country = Country.get(id)
        if not country:
            return {}
        country_data = cls._get_db_obj_data_dict(country)
        city_list = City.get_by_country_id(country.id)
        country_data['city_data'] = \
            [cls._get_db_obj_data_dict(city) for city in city_list]
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
            country_dict = cls._get_db_obj_data_dict(country)
            city_list = City.get_by_country_id(country.id)
            country_dict['city_data'] = \
                [cls._get_db_obj_data_dict(city) for city in city_list]
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
    def create_country(cls, name, name_en, nationality, language,
                       area_code, country_code, note=None):
        Country.create(
            name=name, name_en=name_en, nationality=nationality,
            language=language, area_code=area_code,
            country_code=country_code, note=note)


class CityService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        city = City.get(id)
        if not city:
            return {}
        city_data = cls._get_db_obj_data_dict(city)
        country = Country.get(city.country_id)
        city_data['country'] = cls._get_db_obj_data_dict(country)
        return city_data

    @classmethod
    def update_by_id(cls, id, **kwargs):
        City.update(id, **kwargs)

    @classmethod
    def delete_by_id(cls, id):
        City.delete(id)

    @classmethod
    def create_city(cls, name, name_en, country_id,
                    abbreviation, note=None):
        City.create(
            name=name, name_en=name_en, country_id=country_id,
            abbreviation=abbreviation, note=note)
