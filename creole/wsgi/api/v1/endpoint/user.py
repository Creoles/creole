# coding: utf-8
from flask_restful import Resource
from flask import jsonify

from .....util import Enum
from ..req_param.user import UserInfoParser, UserInfoPostParser, UserInfoPutParser
from ...util import ApiMixin
from creole.handler.user import create_user


class UserInfoApi(ApiMixin, Resource):
    meta = {
        'args_parser_dict': {
            '*': UserInfoParser,
            'put': UserInfoPutParser,
        }
    }

    def get(self, key):
        """查询用户信息"""
        pass

    def put(self, key):
        """更新用户资料"""
        pass

    def delete(self, key):
        pass


class CreateUserApi(ApiMixin, Resource):
    meta = {
        'args_parser_dict': {
            'post': UserInfoPostParser,
        }
    }
    def post(self):
        """添加新用户"""
        params = self.parsed_data
        create_user(**params)
        return jsonify({
            'result': 200,
            'message': 'ok'
        })
