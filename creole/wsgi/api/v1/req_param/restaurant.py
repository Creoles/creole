# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


# 餐厅类型
RESTAURANT_TYPE = Enum(
    ('CHINESE', 1, u'中餐'),
    ('WESTERN', 2, u'西餐'),
    ('SPECIAL', 3, u'特色'),
    ('GENERAL', 4, u'综合'),
)


class CreateRestaurantCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)

class SearchRestaurantCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)


class CreateRestaurantApiParser(BaseRequestParser):
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )

    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)
    restaurant_type = Argument(
        'restaurant_type', required=True, type=int,
        choices=RESTAURANT_TYPE.values())
    country_id = Argument('country_id', type=int, required=True)
    city_id = Argument('city_id', type=int, required=True)
    company_id = Argument('company_id', type=int, required=True)
    address = Argument('address', required=True)
    contact = Argument('contact', required=True)
    telephone = Argument('telephone', required=True)
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)

    # 支付
    currency = Argument(
        'currency', choices=CURRENCY.values(), type=int,
        required=True, location=('json', 'form'))
    bank_name = Argument('bank_name', required=True, location=('json', 'form'))
    deposit_bank = Argument('deposit_bank', required=True, location=('json', 'form'))
    payee = Argument('payee', required=True, location=('json', 'form'))
    account = Argument('account', required=True, location=('json', 'form'))
    note = Argument('note', required=False, location=('json', 'form'))


class SearchRestaurantApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    restaurant_type = Argument(
        'restaurant_type', required=False, type=int,
        choices=RESTAURANT_TYPE.values())
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


def meal_list_parser(meal_dict):
    for k, v in meal_dict.iteritems():
        _type = CreateMealApiParser._RESERVED_DICT.get(k, None)
        if not _type:
            raise ValueError('Invalid key: {!r}'.format(k))
        try:
            meal_dict[k] = _type(v)
        except Exception:
            raise ValueError('Invalid value: {!r}'.format(v))
    return meal_dict


class CreateMealApiParser(BaseRequestParser):
    TYPE = Enum(
        ('STANDARD', 1, u'标准餐'),
        ('UPGRADE', 2, u'升级餐'),
        ('LUXURY', 3, u'豪华餐'),
    )
    _RESERVED_DICT = {
        'restaurant_id': int,
        'meal_type': int,
        'adult_fee': float,
        'adult_cost': float,
        'child_fee': float,
        'child_cost': float,
    }


    meal_list = Argument('meal_list', type=meal_list_parser, required=True, action='append')
    #  restaurant_id = Argument('restaurant_id', type=int, required=True)
    #  meal_type = Argument('meal_type', type=int, required=True, choices=TYPE.values())
    #  adult_fee = Argument('adult_fee', type=float, required=True)
    #  adult_cost = Argument('adult_cost', type=float, required=True)
    #  child_fee = Argument('child_fee', type=float, required=True)
    #  child_cost = Argument('child_cost', type=float, required=True)


class PutMealApiParser(BaseRequestParser):
    adult_fee = Argument('adult_fee', type=float, required=False)
    adult_cost = Argument('adult_cost', type=float, required=False)
    child_fee = Argument('child_fee', type=float, required=False)
    child_cost = Argument('child_cost', type=float, required=False)
