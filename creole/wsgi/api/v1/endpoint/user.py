# coding: utf-8
from ..req_param.user import (
    UserInfoParser,
    UserInfoPostParser,
    UserInfoPutParser,
)
from ...util import Resource, api_response
from creole.exc import ClientError
from creole.service.user import UserService


class UserInfoApi(Resource):
    meta = {
        'args_parser_dict': {
            '*': UserInfoParser,
            'put': UserInfoPutParser,
        }
    }

    def get(self, info):
        """查询用户信息"""
        if self.parsed_data['type'] == UserInfoParser.TYPE.id:
            info = int(info)
        try:
            user = UserService.get_user(info, self.parsed_data['type'])
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response(data=user)

    def put(self, key):
        """更新用户资料"""
        try:
            UserService.update_user(key, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, key):
        try:
            UserService.delete_user(key)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateUserApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': UserInfoPostParser,
        }
    }

    def post(self):
        """添加新用户"""
        params = self.parsed_data
        try:
            UserService.create_user(**params)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
