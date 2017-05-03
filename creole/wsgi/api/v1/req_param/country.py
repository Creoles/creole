# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class CountryApiParser(BaseRequestParser):
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    nationality = Argument('nationality', nullable=False, required=True)
    language = Argument('language', nullable=False, required=True)
    area_code = Argument('area_code', nullable=False, required=True)
    country_code = Argument('country_code', nullable=False, required=True)
    note = Argument('note')


class CityApiParser(BaseRequestParser):
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    country_id = Argument('country_id', nullable=False, required=True)
    abbreviation = Argument('abbreviation', nullable=False, required=True)
    note = Argument('note')
