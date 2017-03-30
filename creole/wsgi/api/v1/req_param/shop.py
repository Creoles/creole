# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class CreateShopApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)
    address = Argument('address', required=True)
    telephone = Argument('telephone', required=True)
    country_id = Argument('country_id', type=int, required=True)
    city_id = Argument('city_id', type=int, required=True)
    company_id = Argument('company_id')
    shop_type = Argument('shop_type', type=int, required=True)
    contact = Argument('contact', required=True)
    fee_person = Argument('fee_person', required=True, type=float)
    commission_ratio = Argument('commission_ratio', required=True, type=float)
    intro_cn = Argument('intro_cn')
    intro_en = Argument('intro_en')


class ShopSearchApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    shop_type = Argument('shop_type', type=int, required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)

class CreateShopCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)


class SearchShopCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)
