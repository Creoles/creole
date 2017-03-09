# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class CountryApiParser(BaseRequestParser):
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)