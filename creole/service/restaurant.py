# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

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
    DatabaseError,
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
    def _get_db_obj_data_dict(cls, restaurant_obj):
        _dict = super(RestaurantService, cls).\
            _get_db_obj_data_dict(restaurant_obj)
        if restaurant_obj:
            # 拉取餐厅对应的套餐类型
            meal_list = MealService.get_by_restaurant_id(restaurant_obj.id)
            _dict['meal_type'] = meal_list
        return _dict

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
                          contact, telephone, currency, bank_name,
                          deposit_bank, payee, account, note=None,
                          intro_cn=None, intro_en=None):
        return Restaurant.create(
            name=name, name_en=name_en, restaurant_type=restaurant_type,
            country_id=country_id, city_id=city_id, company_id=company_id,
            address=address, contact=contact, telephone=telephone,
            currency=currency, bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, note=note,
            intro_cn=intro_cn, intro_en=intro_en
        )

    @classmethod
    def search_restaurant(cls, country_id=None, city_id=None,
                          company_id=None, page=1, number=20):
        raw_data = []
        restaurant_list, total = Restaurant.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, page=page, number=number)
        for restaurant in restaurant_list:
            raw_data.append(cls._get_db_obj_data_dict(restaurant))
        return raw_data, total


class MealService(BaseService):
    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        _list = []
        restaurant_list = Meal.get_by_restaurant_id(restaurant_id)
        for item in restaurant_list:
            _list.append(cls._get_db_obj_data_dict(item))
        return _list

    @classmethod
    def create_meal(cls, meal_list):
        session = DBSession()
        for meal_dict in meal_list:
            restaurant_id=meal_dict['restaurant_id']
            meal_type=meal_dict['meal_type']
            adult_fee=meal_dict['adult_fee']
            adult_cost=meal_dict['adult_cost']
            child_fee=meal_dict['child_fee']
            child_cost=meal_dict['child_cost']
            # 检查是否已经添加过
            meal = session.query(Meal).filter(
                Meal.restaurant_id==restaurant_id, Meal.meal_type==meal_type).first()
            if meal:
                raise_error_json(
                    ClientError(errcode=CreoleErrCode.RESTAURANT_MEAL_REACH_LIMIT))
            Meal.create(
                restaurant_id=restaurant_id, meal_type=meal_type,
                adult_fee=adult_fee, adult_cost=adult_cost,
                child_fee=child_fee, child_cost=child_cost)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_meal_by_id(cls, id, adult_fee=None, adult_cost=None,
                     child_fee=None, child_cost=None):
        return Meal.update(
            id=id, adult_fee=adult_fee, adult_cost=adult_cost,
            child_fee=child_fee, child_cost=child_cost)

    @classmethod
    def delete_meal_by_id(cls, id):
        return Meal.delete(id)
