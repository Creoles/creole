# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class CreateShopApiParser(BaseRequestParser):
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    address = Argument('address', nullable=False, required=True)
    telephone = Argument('telephone', nullable=False, required=True)
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    company_id = Argument('company_id')
    shop_type = Argument('shop_type', type=int, nullable=False, required=True)
    contact = Argument('contact', nullable=False, required=True)
    fee_person = Argument('fee_person', nullable=False, required=True, type=float)
    commission_ratio = Argument('commission_ratio', nullable=False, required=True, type=float)
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
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)


class SearchShopCompanyApiParser(BaseRequestParser):
    is_all = Argument('is_all', type=bool, default=False, required=True)
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)
