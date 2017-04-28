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
    adult_fee = Argument('adult_fee', type=float, nullable=False, required=True)
    child_fee = Argument('child_fee', type=float, nullable=False, required=True)
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)
