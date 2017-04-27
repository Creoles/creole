# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


class GetVehicleAccountApiParser(BaseRequestParser):
    ACCOUNT_TYPE = Enum(
        ('COMPANY', 1, u'公司账号'),
        ('PERSSON', 2, u'个人账号'),
    )
    account_type = Argument(
        'account_type', type=int, choices=ACCOUNT_TYPE.values(), required=True)

class CreateVehicleApiParser(BaseRequestParser):
    account_id = Argument('account_id', type=int, required=True)
    company_id = Argument('company_id', type=int, required=True)
    country_id = Argument('country_id', type=int, required=True)
    city_id = Argument('city_id', type=int, required=True)
    vehicle_type = Argument('vehicle_type', required=True)
    seat = Argument('seat', type=int, required=True)
    start_use = Argument('start_use', required=True)
    license = Argument('license', required=True)
    register_number = Argument('register_number', required=True)
    insurance_number = Argument('insurance_number', required=True)
    contact = Argument('contact', required=True)
    telephone = Argument('telephone', required=True)
    unit_price = Argument('unit_price', type=float, required=True)


class CreateVehicleCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)


class SearchVehicleCompanyApiParser(BaseRequestParser):
    is_all = Argument('is_all', type=bool, default=False, required=True)
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)


class VehicleSearchApiParser(BaseRequestParser):
    OPERATIONS = Enum(
        ('GREATER', 1, u'大于'),
        ('EQUAL', 2, u'等于'),
        ('LESS', 3, u'小于'),
    )
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    vehicle_type = Argument('vehicle_type', type=int, required=False)
    operation = Argument(
        'operation', type=int, choices=OPERATIONS.values(), required=False)
    seat = Argument('seat', type=int, required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateVehicleAccountApiParser(BaseRequestParser):
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )
    TYPE = Enum(
        ('COMPANY', 1, u'公司账号'),
        ('PERSSON', 2, u'个人账号'),
    )
    owner_id = Argument('owner_id', type=int, required=False, location=('json', 'form'))
    account_type = Argument(
        'account_type', type=int, choices=TYPE.values(), required=True)
    currency = Argument(
        'currency', choices=CURRENCY.values(), type=int,
        required=True, location=('json', 'form'))
    bank_name = Argument('bank_name', required=True, location=('json', 'form'))
    deposit_bank = Argument('deposit_bank', required=True, location=('json', 'form'))
    payee = Argument('payee', required=True, location=('json', 'form'))
    account = Argument('account', required=True, location=('json', 'form'))
    note = Argument('note', required=False, location=('json', 'form'))
