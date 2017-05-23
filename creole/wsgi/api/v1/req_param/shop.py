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
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateShopCompanyContactApiParser(ContactParserMixin, BaseRequestParser):
    company_id = Argument(
        'company_id', required=True, nullable=False,
        type=int, location=('json', 'form'))


class CreateShopContactApiParser(ContactParserMixin, BaseRequestParser):
    shop_id = Argument(
        'shop_id', required=True, nullable=False,
        type=int, location=('json', 'form'))


class CreateShopFeeApiParser(BaseRequestParser):
    ACCOUNT_PERIOD = Enum(
        ('NOW', 1, u'现结'),
        ('MONTH', 2, u'月结'),
    )
    ACCOUNT_WAY = Enum(
        ('CASH', 1, u'现金'),
        ('CHECK', 2, u'支票'),
        ('TRANSFER', 3, u'转账'),
    )
    shop_id = Argument('shop_id', type=int, required=True, nullable=False)
    fee_person = Argument('fee_person', type=float, required=True, nullable=False)
    company_ratio = Argument('company_ratio', type=float, required=True, nullable=False)
    tour_guide_ratio = Argument(
        'tour_guide_ratio', type=float, required=True, nullable=False)
    account_period = Argument(
        'account_period', type=int, choices=ACCOUNT_PERIOD.values(),
        required=True, nullable=False)
    account_way = Argument(
        'account_way', type=int, choices=ACCOUNT_WAY.values(),
        required=True, nullable=False)
    note = Argument('note')
