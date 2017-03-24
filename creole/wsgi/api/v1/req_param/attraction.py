# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class SearchAttractionApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    name = Argument('name', required=False)


class CreateAttractionApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=True)
    city_id = Argument('city_id', type=int, required=True)
    address = Argument('address', required=True)
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)
    adult_fee = Argument('adult_fee', type=float, required=True)
    child_fee = Argument('child_fee', type=float, required=True)
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)
