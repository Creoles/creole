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
    ParameterError,
)


class RestaurantCompanyService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = RestaurantCompany.get_by_id(id)
        restaurant_list = Restaurant.get_by_company_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        company_info['restaurant_list'] = \
            [cls._get_db_obj_data_dict(item) for item in restaurant_list]
        return company_info

    @classmethod
    def delete_restaurant_company_by_id(cls, id):
        """删除餐饮公司, 有三个步骤:
        1. 删除公司
        2. 删除公司名下的所有餐厅
        3. 删除所有餐厅对应的套餐
        """
        session = DBSession()
        # 删除公司
        RestaurantCompany.delete(id)
        restaurant_list = Restaurant.get_by_company_id(id)
        for restaurant in restaurant_list:
            # 删除餐厅对应的套餐
            meal_list = Meal.get_by_restaurant_id(restaurant.id)
            for meal in meal_list:
                session.delete(meal)
            # 删除公司下的餐厅
            session.delete(restaurant)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_restaurant_company_by_id(cls, id, **kwargs):
        return RestaurantCompany.update(id, **kwargs)

    @classmethod
    def create_restaurant_company(cls, name, name_en):
        return RestaurantCompany.create(name=name, name_en=name_en)

    @classmethod
    def search_company(cls, name=None, name_en=None, is_all=False):
        restaurant_company = \
            RestaurantCompany.search(name=name, name_en=name_en, is_all=is_all)
        return [cls._get_db_obj_data_dict(item) for item in restaurant_company]


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
        session = DBSession()
        Restaurant.delete(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

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
                          company_id=None, restaurant_type=None,
                          page=1, number=20):
        raw_data = []
        restaurant_list, total = Restaurant.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, restaurant_type=restaurant_type,
            page=page, number=number)
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
    def edit_meal(cls, create_list=None,
                  update_list=None, delete_id_list=None):
        """编辑套餐类型:
        
        :param create_list: 需要创建的套餐列表, 元素为dict
        :param update_list: 需要更新的套餐列表, 元素为dict
        :param delete_id_list: 需要删除的套餐Id列表
        """
        session = DBSession()
        if create_list:
            if len(create_list) > 3:
                raise_error_json(ParameterError())
            cls.create_meal(create_list, delete_id_list)
        if update_list:
            if len(update_list) > 3:
                raise_error_json(ParameterError())
            cls.update_meal_list(update_list)
        if delete_id_list:
            if len(delete_id_list) > 3:
                raise_error_json(ParameterError())
            cls.multi_delete_meal(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_meal(cls, meal_list, delete_id_list):
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
            if meal and meal.id not in delete_id_list:
                raise_error_json(
                    ClientError(errcode=CreoleErrCode.RESTAURANT_MEAL_REACH_LIMIT))
            Meal.create(
                restaurant_id=restaurant_id, meal_type=meal_type,
                adult_fee=adult_fee, adult_cost=adult_cost,
                child_fee=child_fee, child_cost=child_cost)

    @classmethod
    def update_meal_list(cls, update_list):
        for meal_dict in update_list:
            Meal.update(
                id=meal_dict['id'], adult_fee=meal_dict['adult_fee'],
                adult_cost=meal_dict['adult_cost'],
                child_fee=meal_dict['child_fee'],
                child_cost=meal_dict['child_cost'])

    @classmethod
    def multi_delete_meal(cls, delete_id_list):
        for id in delete_id_list:
            Meal.delete(id)
