# coding: utf-8
import copy

from flask_restful.reqparse import Argument

from .mixins import (
    dict_parser_func, 
    ContactParserMixin,
    CompanyParserMixin,
    AccountParserMixin,
)
from ...util import BaseRequestParser
from creole.util import Enum


class CreateHotelCompanyContactApiParser(ContactParserMixin, BaseRequestParser):
    company_id = Argument(
        'company_id', required=True, nullable=False,
        type=int, location=('json', 'form'))


class CreateHotelCompanyApiParser(CompanyParserMixin, BaseRequestParser):
    intro = Argument('intro')
    note = Argument('intro')


class CreateHotelApiParser(BaseRequestParser):
    LEVEL = Enum(
        ('ONE', 1, u'一星'),
        ('TWO', 2, u'二星'),
        ('THREE', 3, u'三星'),
        ('FOUR', 4, u'四星'),
        ('FIVE', 5, u'五星'),
    )

    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    company_id = Argument('company_id', type=int, nullable=False, required=True)
    address = Argument('address', nullable=False, required=True)
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    nickname_en = Argument('nickname_en', nullable=False, required=True) 
    star_level = Argument('star_level', type=int, nullable=False, required=True)
    comment_level = Argument('comment_level', type=int, nullable=False, required=True)
    standard_room_number = Argument(
        'standard_room_number', type=int, nullable=False, required=True)
    standard_double_room_number = Argument(
        'standard_double_room_number', type=int, nullable=False, required=True)
    triple_room_number = Argument(
        'triple_room_number', type=int, nullable=False, required=True)
    suite_room_number = Argument(
        'suite_room_number', type=int, nullable=False, required=True)
    tour_guide_room_number = Argument(
        'tour_guide_room_number', type=int, nullable=False, required=True)
    start_year = Argument('start_year', type=int, nullable=False, required=True)
    telephone = Argument('telephone', nullable=False, required=True)
    email = Argument('email', nullable=False, required=True)
    intro_cn = Argument('intro_cn')
    intro_en = Argument('intro_en')


class SearchHotelApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)
    nickname_en = Argument('nickname_en', required=False)
    star_level = Argument('star_level', type=int, required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateHotelAccountApiParser(AccountParserMixin, BaseRequestParser):
    hotel_id = Argument(
        'hotel_id', required=True, nullable=False,
        type=int, location=('json', 'form'))


class CreateHotelContactApiParser(ContactParserMixin, BaseRequestParser):
    hotel_id = Argument(
        'hotel_id', required=True, nullable=False,
        type=int, location=('json', 'form'))


class CreateHotelFeeApiParser(BaseRequestParser):
    FREE_TYPE = Enum(
        ('PEOPLE', 1, u'按客户数'),
        ('ROOM', 2, u'按房间数'),
    )

    hotel_id = Argument('hotel_id', type=int, nullable=False, required=True)
    confirm_person = Argument('confirm_person', nullable=False, required=True)
    free_policy = Argument(
        'free_policy', type=int, choices=FREE_TYPE.values(),
        nullable=False, required=True)
    free = Argument('free', type=int)
    note = Argument('note')
    attachment_hash = Argument('attachment_hash')


class EditRoomPriceApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'hotel_fee_id': (int, True),
        'room_type': (int, True),
        'start_time': (str, True),
        'end_time': (str, True),
        'price': (float, True),
        'note': (str, False),
    }
    _UPDATE_PARAM_MAPPING = copy.deepcopy(_CREATE_PARAM_MAPPING)
    _UPDATE_PARAM_MAPPING.update({'id': (int, True)})

    create_list = Argument(
        'create_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_CREATE_PARAM_MAPPING))
    update_list = Argument(
        'update_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_UPDATE_PARAM_MAPPING))
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')


class EditMealPriceApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'hotel_fee_id': (int, True),
        'meal_type': (int, True),
        'start_time': (str, True),
        'end_time': (str, True),
        'price': (float, True),
        'note': (str, False),
    }
    _UPDATE_PARAM_MAPPING = copy.deepcopy(_CREATE_PARAM_MAPPING)
    _UPDATE_PARAM_MAPPING.update({'id': (int, True)})

    create_list = Argument(
        'create_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_CREATE_PARAM_MAPPING))
    update_list = Argument(
        'update_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_UPDATE_PARAM_MAPPING))
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')


class EditRoomAdditionalChargeApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'hotel_fee_id': (int, True),
        'room_level': (int, True),
        'start_time': (str, True),
        'end_time': (str, True),
        'price': (float, True),
        'note': (str, False),
    }
    _UPDATE_PARAM_MAPPING = copy.deepcopy(_CREATE_PARAM_MAPPING)
    _UPDATE_PARAM_MAPPING.update({'id': (int, True)})

    create_list = Argument(
        'create_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_CREATE_PARAM_MAPPING))
    update_list = Argument(
        'update_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_UPDATE_PARAM_MAPPING))
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')


class EditFestivalAdditionalChargeApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'hotel_fee_id': (int, True),
        'festival_type': (int, True),
        'start_time': (str, True),
        'end_time': (str, True),
        'price': (float, True),
        'note': (str, False),
    }
    _UPDATE_PARAM_MAPPING = copy.deepcopy(_CREATE_PARAM_MAPPING)
    _UPDATE_PARAM_MAPPING.update({'id': (int, True)})

    create_list = Argument(
        'create_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_CREATE_PARAM_MAPPING))
    update_list = Argument(
        'update_list', required=False, action='append',
        type=dict_parser_func(param_mapping=_UPDATE_PARAM_MAPPING))
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')
