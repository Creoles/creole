# coding: utf-8
from flask_restful import Resource
from flask import jsonify

from ..req_param.user import UserInfoParser, UserInfoPostParser, UserInfoPutParser
from ...util import ApiMixin
from creole.service.user import UserService


class UserInfoApi(ApiMixin, Resource):
    meta = {
        'args_parser_dict': {
            '*': UserInfoParser,
            'put': UserInfoPutParser,
        }
    }

    def get(self, key):
        """查询用户信息"""
        return jsonify(
            UserService.get_user(key, self.parsed_data['type_'])
        )

    def put(self, key):
        """更新用户资料"""
        UserService.update_user(key, **self.parsed_data)
        return jsonify({
            'result': 200,
            'message': 'ok'
        })

    def delete(self, key):
        UserService.delete_user(key)
        return jsonify({
            'result': 200,
            'message': 'ok'
        })


class CreateUserApi(ApiMixin, Resource):
    meta = {
        'args_parser_dict': {
            'post': UserInfoPostParser,
        }
    }
    def post(self):
        """添加新用户"""
        params = self.parsed_data
        UserService.create_user(**params)
        return jsonify({
            'result': 200,
            'message': 'ok'
        })
