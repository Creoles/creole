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
