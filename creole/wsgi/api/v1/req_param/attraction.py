# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class SearchAttractionApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    name = Argument('name', required=False)
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


class CreateAttractionApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    address = Argument('address', nullable=False, required=True)
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    nickname_en = Argument('nickname_en', nullable=False, required=True)
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)
    note = Argument('note', required=False)


class CreateAttractionFeeApiParser(BaseRequestParser):
    attraction_id = Argument('attraction_id', type=int, nullable=False, required=True)
    public_price = Argument('public_price', type=float, nullable=False, required=True)
    company_price = Argument('company_price', type=float, nullable=False, required=True)
    tour_guide_price = Argument('tour_guide_price', type=float, nullable=False, required=True)
    translator_price = Argument('translator_price', type=float, nullable=False, required=True)
    free_policy = Argument('free_policy', type=int, nullable=False, required=True)
    child_discount = Argument('child_discount', type=float, nullable=False, required=True)
    note = Argument('note', required=False)
