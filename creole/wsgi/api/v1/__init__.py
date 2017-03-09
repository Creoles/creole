# coding: utf-8
from flask import Blueprint
from flask_restful import Api

from .endpoint.user import UserInfoApi, CreateUserApi
from .endpoint.country import (
    CountryApi,
    AllCountryApi,
    CreateCountryApi,
    CityApi,
    CreateCityApi,
)


blue_print = Blueprint('api_v1', __name__)
app = Api(blue_print)

# 用户
app.add_resource(UserInfoApi, '/user/<info>', endpoint='user-info')
app.add_resource(CreateUserApi, '/user/create_user', endpoint='user-create')

# 国家和城市
app.add_resource(CountryApi, '/country/<int:id>', endpoint='get-country')
app.add_resource(AllCountryApi, '/country/all', endpoint='get-all-country')
app.add_resource(CreateCountryApi, '/country/create', endpoint='create-country')
app.add_resource(CityApi, '/city/<int:id>', endpoint='get-city')
app.add_resource(CreateCityApi, '/city/create', endpoint='create-city')
