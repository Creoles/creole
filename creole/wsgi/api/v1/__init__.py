# coding: utf-8
from flask import Blueprint
from flask_restful import Api

from .endpoint.user import UserInfoApi, CreateUserApi


blue_print = Blueprint('api_v1', __name__)
app = Api(blue_print)

# 用户
app.add_resource(UserInfoApi, '/user/<key>', endpoint='user-info')
app.add_resource(CreateUserApi, '/create_user', endpoint='user-create')
