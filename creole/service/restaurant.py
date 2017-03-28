# coding: utf-8
from .base import BaseService
from ..model import DBSession
from ..model.restaurant import (
    RestaurantCompany,
    Restaurant,
    Meal,
)
from ..exc import (
    raise_error_json,
    ClientError,
    CreoleErrCode,
)


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


class RestaurantService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        restaurant = Restaurant.get_by_id(id)
        return cls._get_db_obj_data_dict(restaurant)

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


class MealService(BaseService):
    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        _dict = {}
        restaurant_list = Meal.get_by_restaurant_id(restaurant_id)
        for item in restaurant_list:
            _dict[item.meal_type] = cls._get_db_obj_data_dict(item)
        return _dict

    @classmethod
    def create_meal(cls, restaurant_id, meal_type, adult_fee, adult_cost,
                    child_fee, child_cost):
        session = DBSession()
        meal = session.query(Meal).filter(
            Meal.restaurant_id==restaurant_id, Meal.meal_type==meal_type).first()
        if meal:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_MEAL_REACH_LIMIT))
        return Meal.create(
            restaurant_id=restaurant_id, meal_type=meal_type,
            adult_fee=adult_fee, adult_cost=adult_cost,
            child_fee=child_fee, child_cost=child_cost)

    @classmethod
    def update_meal_by_id(cls, id, adult_fee=None, adult_cost=None,
                     child_fee=None, child_cost=None):
        return Meal.updated(
            adult_fee=adult_fee, adult_cost=adult_cost,
            child_fee=child_fee, child_cost=child_cost)

    @classmethod
    def delete_meal_by_id(cls, id):
        return Meal.delete(id)
