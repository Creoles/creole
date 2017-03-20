# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


class CreateVehicleApiParser(BaseRequestParser):
    company_id = Argument('company_id', type=int, required=True)
    country_id = Argument('country_id', type=int, required=True)
    city_id = Argument('city_id', type=int, required=True)
    vehicle_type = Argument('vehicle_type', required=True)
    seat = Argument('seat', type=int, required=True)
    start_use = Argument('start_use', required=True)
    license = Argument('license', required=True)
    register_number = Argument('register_number', required=True)
    contact = Argument('contact', required=True)
    telephone = Argument('telephone', required=True)
    unit_price = Argument('unit_price', type=float, required=True)


class CreateVehicleCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)


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
    company_id = Argument('company_id', type=int, required=False)
    user_id = Argument('user_id', type=int, required=False)
    currency = Argument(
        'currency', choices=CURRENCY.values(), type=int, required=True)
    bank_name = Argument('bank_name', required=True)
    deposit_bank = Argument('deposit_bank', required=True)
    payee = Argument('payee', required=True)
    account = Argument('account', required=True)
    note = Argument('note', required=False)


class DeleteVehicleAccountApiParser(BaseRequestParser):
    is_company = Argument('is_company', type=bool, required=True)


class GetVehicleAccountApiParser(BaseRequestParser):
    company_id = Argument('company_id', type=int, required=False)
    user_id = Argument('user_id', type=int, required=False)
