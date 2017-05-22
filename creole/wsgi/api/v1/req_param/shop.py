 # coding: utf-8
from flask_restful.reqparse import Argument

from creole.util import Enum
from ...util import BaseRequestParser
from .mixins import CompanyParserMixin, ContactParserMixin


class CreateShopApiParser(BaseRequestParser):
    SHOP_TYPE = Enum(
        ('JEWELRY', 1, u'珠宝'),
        ('TEA', 2, u'红茶'),
        ('OTHER', 3, u'其他'),
    )
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    nickname_en = Argument('nickname_en', nullable=False, required=True)
    address = Argument('address', nullable=False, required=True)
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    company_id = Argument('company_id', type=int, nullable=False, required=True)
    shop_type = Argument(
        'shop_type', type=int, choices=SHOP_TYPE, nullable=False, required=True)
    intro_cn = Argument('intro_cn')
    intro_en = Argument('intro_en')


class ShopSearchApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    shop_type = Argument('shop_type', type=int, required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)

class CreateShopCompanyApiParser(CompanyParserMixin, BaseRequestParser):
    intro = Argument('intro')


class SearchShopCompanyApiParser(BaseRequestParser):
    is_all = Argument('is_all', type=bool, default=False, required=True)
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)


class CreateShopCompanyContactApiParser(ContactParserMixin, BaseRequestParser):
    company_id = Argument(
        'company_id', required=True, nullable=False,
        type=int, location=('json', 'form'))
