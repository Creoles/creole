# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from .base import BaseService
from ..model import DBSession
from ..model.restaurant import (
    Restaurant,
    RestaurantAccount,
    Meal,
)
from ..exc import (
    raise_error_json,
    ClientError,
    DatabaseError,
    CreoleErrCode,
    ParameterError,
)


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
    def create_restaurant(cls, name, name_en, nickname_en, restaurant_type,
               country_id, city_id, address, environ_level,
               taste_level, service_level, cost_level,
               cooperation_level, recommend_level, contact_one,
               position_one, telephone_one, email_one, contact_two,
               position_two, email_two, telephone_two, contact_three=None,
               position_three=None, email_three=None, telephone_three=None,
               standard_meal_intro_cn=None, standard_meal_intro_en=None,
               upgrade_meal_intro_cn=None, upgrade_meal_intro_en=None,
               luxury_meal_intro_cn=None, luxury_meal_intro_en=None,
               intro_cn=None, intro_en=None):
        return Restaurant.create(
            name=name, name_en=name_en, nickname_en=nickname_en,
            restaurant_type=restaurant_type, country_id=country_id,
            city_id=city_id, address=address, environ_level=environ_level,
            taste_level=taste_level, service_level=service_level,
            cost_level=cost_level, cooperation_level=cooperation_level,
            recommend_level=recommend_level, contact_one=contact_one,
            position_one=position_one, telephone_one=telephone_one,
            email_one=email_one, contact_two=contact_two,
            position_two=position_two, email_two=email_two,
            telephone_two=telephone_two, contact_three=contact_three,
            position_three=position_three, email_three=email_three,
            telephone_three=telephone_three,
            standard_meal_intro_cn=standard_meal_intro_cn,
            standard_meal_intro_en=standard_meal_intro_en,
            upgrade_meal_intro_cn=upgrade_meal_intro_cn,
            upgrade_meal_intro_en=upgrade_meal_intro_en,
            luxury_meal_intro_cn=luxury_meal_intro_cn,
            luxury_meal_intro_en=luxury_meal_intro_en,
            intro_cn=intro_cn, intro_en=intro_en
        )

    @classmethod
    def search_restaurant(cls, country_id=None, city_id=None,
                          restaurant_type=None, page=1, number=20):
        raw_data = []
        restaurant_list, total = Restaurant.search(
            country_id=country_id, city_id=city_id,
            restaurant_type=restaurant_type,
            page=page, number=number)
        for restaurant in restaurant_list:
            raw_data.append(cls._get_db_obj_data_dict(restaurant))
        return raw_data, total


class RestaurantAccountService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        account = RestaurantAccount.get_by_id(id)
        return cls._get_db_obj_data_dict(account)

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        account_list = RestaurantAccount.get_by_restaurant_id(restaurant_id)
        return [cls._get_db_obj_data_dict(account) for account in account_list]

    @classmethod
    def edit_restaurant_account(cls, create_list=None,
                                update_list=None, delete_id_list=None):
        """编辑餐厅银行资料:
        
        :param create_list: 需要创建的银行资料列表, 元素为dict
        :param update_list: 需要更新的银行资料列表, 元素为dict
        :param delete_id_list: 需要删除的银行资料Id列表
        """
        session = DBSession()
        if create_list:
            cls.create_account(create_list)
        if update_list:
            cls.update_account(update_list)
        if delete_id_list:
            cls.delete_account(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_account(cls, account_list):
        for account_dict in account_list:
            restaurant_id = account_dict['restaurant_id']
            currency = account_dict['currency']
            bank_name = account_dict['bank_name']
            deposit_bank = account_dict['deposit_bank']
            payee = account_dict['payee']
            account = account_dict['account']
            swift_code = account_dict.get('swift_code', None)
            note = account_dict.get('note', None)
        RestaurantAccount.create(
            restaurant_id=restaurant_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, note=note,
            swift_code=swift_code)

    @classmethod
    def delete_account(cls, delete_id_list):
        for id in delete_id_list:
            RestaurantAccount.delete(id)

    @classmethod
    def update_account(cls, update_list):
        for account_dict in update_list:
            RestaurantAccount.update(**account_dict)


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
