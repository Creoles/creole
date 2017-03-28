# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


class CreateRestaurantCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)


class CreateRestaurantApiParser(BaseRequestParser):
    TYPE = Enum(
        ('CHINESE', 1, u'中餐'),
        ('WESTERN', 2, u'西餐'),
        ('SPECIAL', 3, u'特色'),
        ('GENERAL', 4, u'综合'),
    )

    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)
    restaurant_type = Argument(
        'restaurant_type', required=True, type=int, choices=TYPE.values())
    country_id = Argument('country_id', type=int, required=True)
    city_id = Argument('city_id', type=int, required=True)
    company_id = Argument('company_id', type=int, required=True)
    address = Argument('address', required=True)
    contact = Argument('contact', required=True)
    telephone = Argument('telephone', required=True)
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)


class SearchRestaurantApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)


class CreateMealApiParser(BaseRequestParser):
    TYPE = Enum(
        ('STANDARD', 1, u'标准餐'),
        ('UPGRADE', 2, u'升级餐'),
        ('LUXURY', 3, u'豪华餐'),
    )

    restaurant_id = Argument('restaurant_id', type=int, required=True)
    meal_type = Argument('meal_type', type=int, required=True, choices=TYPE.values())
    adult_fee = Argument('adult_fee', type=float, required=True)
    adult_cost = Argument('adult_cost', type=float, required=True)
    child_fee = Argument('child_fee', type=float, required=True)
    child_cost = Argument('child_cost', type=float, required=True)


class PutMealApiParser(BaseRequestParser):
    adult_fee = Argument('adult_fee', type=float, required=False)
    adult_cost = Argument('adult_cost', type=float, required=False)
    child_fee = Argument('child_fee', type=float, required=False)
    child_cost = Argument('child_cost', type=float, required=False)
