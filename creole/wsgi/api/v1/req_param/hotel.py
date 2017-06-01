# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


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
