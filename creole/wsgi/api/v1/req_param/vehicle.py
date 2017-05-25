# coding: utf-8
from flask_restful.reqparse import Argument

from .mixins import (
    AccountParserMixin,
    ContactParserMixin,
    CompanyParserMixin,
)
from ...util import BaseRequestParser
from creole.util import Enum


class CreateVehicleApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    company_id = Argument('company_id', type=int, nullable=False, required=True)
    license = Argument('license', nullable=False, required=True)
    insurance_number = Argument('insurance_number', nullable=False, required=True)
    start_use = Argument('start_use', nullable=False, required=True)
    register_number = Argument('register_number', nullable=False, required=True)
    vehicle_type_id = Argument('vehicle_type_id', type=int, nullable=False, required=True)


class CreateVehicleCompanyApiParser(CompanyParserMixin, BaseRequestParser):
    COMPANY_TYPE = Enum(
        ('COMPANY', 1, u'公司'),
        ('PERSON', 2, u'个人'),
    )
    company_type = Argument(
        'company_type', choices=COMPANY_TYPE.values(), type=int,
        nullable=False, required=True)
    vehicle_number = Argument('vehicle_number', type=int, nullable=False, required=True)


class SearchVehicleCompanyApiParser(BaseRequestParser):
    COMPANY_TYPE = Enum(
        ('COMPANY', 1, u'公司'),
        ('PERSON', 2, u'个人'),
    )

    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_type = Argument(
        'company_type', type=int, choices=COMPANY_TYPE.values(), required=False)
    number = Argument('number', type=int, default=20, required=False)
    page = Argument('page', type=int, default=1, required=False)


class SearchVehicleApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    vehicle_type_id = Argument('vehicle_type_id', type=int, required=False)
    license = Argument('license', required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateVehicleAccountApiParser(AccountParserMixin, BaseRequestParser):
    company_id = Argument(
        'company_id', type=int, required=True, location=('json', 'form'))


class CreateVehicleFeeApiParser(BaseRequestParser):
    vehicle_type_id = Argument(
        'vehicle_type_id', required=True, nullable=False,
        type=int, location=('json', 'form'))
    company_id = Argument(
        'company_id', required=True, nullable=False,
        type=int, location=('json', 'form'))
    unit_price = Argument(
        'unit_price', required=True, nullable=False,
        type=float, location=('json', 'form'))
    start_time = Argument(
        'start_time', required=True, nullable=False, location=('json', 'form'))
    end_time = Argument(
        'end_time', required=True, nullable=False, location=('json', 'form'))
    confirm_person = Argument(  
        'confirm_person', required=True, nullable=False,
        type=int, location=('json', 'form'))
    attachment_hash = Argument(
        'attachment_hash', required=True,
        nullable=False, location=('json', 'form'))


class SearchVehicleFeeApiParser(BaseRequestParser):
    vehicle_type_id = Argument('vehicle_type_id', required=False, type=int)
    company_id = Argument('company_id', required=False, type=int)
    unit_price = Argument('unit_price', required=False, type=float)
    start_time = Argument('start_time', required=False)
    end_time = Argument('end_time', required=False)
    confirm_person = Argument('confirm_person', required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateVehicleTypeApiParser(BaseRequestParser):
    VEHICLE_TYPE = Enum(
        ('CAR', 1, u'轿车'),
        ('VAN', 2, u'货车'),
        ('BIG_VAN', 3, u'大货车'),
        ('MINI_COATCH', 4, u'迷你大巴'),
        ('COATCH', 5, u'大巴'),
        ('LONG_COATCH', 6, u'加长大巴'),
        ('OTHER', 7, u'其他'),
    )

    vehicle_type = Argument(
        'vehicle_type', type=int, choices=VEHICLE_TYPE.values(),
        required=True, nullable=False)
    brand = Argument('brand', required=True, nullable=False)
    seat = Argument('seat', type=int, required=True, nullable=False)
    available_seat = Argument(
        'available_seat', type=int, required=True, nullable=False)
    passenger_count = Argument(
        'passenger_count', type=int, required=True, nullable=False)
    note = Argument('note')


class SearchVehicleTypeApiParser(BaseRequestParser):
    VEHICLE_TYPE = Enum(
        ('CAR', 1, u'轿车'),
        ('VAN', 2, u'货车'),
        ('BIG_VAN', 3, u'大货车'),
        ('MINI_COATCH', 4, u'迷你大巴'),
        ('COATCH', 5, u'大巴'),
        ('LONG_COATCH', 6, u'加长大巴'),
        ('OTHER', 7, u'其他'),
    )

    vehicle_type = Argument(
        'vehicle_type', type=int, choices=VEHICLE_TYPE.values(), required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateVehicleContactApiParser(ContactParserMixin, BaseRequestParser):
    company_id = Argument(
        'company_id', required=True, nullable=False,
        type=int, location=('json', 'form'))
