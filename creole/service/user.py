# coding: utf-8
from ..model.user import User
from ..wsgi.api.v1.req_param.user import UserInfoParser
from ..model import gen_commit_deco
from ..exc import (
    raise_error_json,
    ClientError,
    CreoleErrCode,
)


class UserService(object):
    @classmethod
    def create_user(cls, user_name, password, role=99, 
                    customer_name=None, address=None,
                    telephone=None, is_admin=False):
        """创建新用户"""
        # TODO 权限问题
        if not is_admin:
            role = 1
        User.add_new_user(
            user_name=user_name,
            password=password,
            customer_name=customer_name,
            address=address,
            telephone=telephone,
            role=role)

    @classmethod
    def get_user(cls, key, type_):
        """查找用户"""
        user = None
        if type_ == UserInfoParser.TYPE.uuid:
            user = User.get_by_uuid(key)
        elif type_ == UserInfoParser.TYPE.id:
            user = User.get_by_id(int(key))
        elif type_ == UserInfoParser.TYPE.name:
            user = User.get_by_name(key)
        elif type_ == UserInfoParser.TYPE.customer_name:
            user = User.get_by_customer_name(key)
        if user is None:
            return {}
        user_dict = {}
        for k, v in user.__dict__.iteritems():
            if not k.startswith('_'):
                user_dict[k] = v
        return user_dict

    @classmethod
    def _get_user(cls, key):
        user = User.get_by_id(key)
        if not user:
            raise_error_json(ClientError(
                errcode=CreoleErrCode.USER_NOT_EXIST))
    
    @classmethod
    @gen_commit_deco
    def delete_user(cls, key):
        """删除用户"""
        cls._get_user(key)
        User.delete(key)

    @classmethod
    @gen_commit_deco
    def update_user(cls, key, **kwargs):
        cls._get_user(key)
        User.update(key, **kwargs)
