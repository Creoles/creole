# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser


class CreateRestaurantCompanyApiParser(BaseRequestParser):
    name = Argument('name', required=True)
    name_en = Argument('name_en', required=True)
