# coding: utf-8
from flask_restful.reqparse import Argument

from creole.util import Enum
from ...util import BaseRequestParser


class UserInfoParser(BaseRequestParser):
    TYPE = Enum(
        ('uuid', 0, u'根据uuid查询'),
        ('id', 1, u'根据id查询'),
        ('name', 2, u'根据用户名查询'),
        ('customer_name', 3, u'根据客户名查询'),
    )
    type_ = Argument('type', type=int, default=TYPE.id)


class UserInfoPutParser(BaseRequestParser):
    TYPE = Enum(
        ('uuid', 0, u'根据uuid查询'),
        ('id', 1, u'根据id查询'),
        ('name', 2, u'根据用户名查询'),
        ('customer_name', 3, u'根据客户名查询'),
    )
    user_name = Argument('user_name', required=False)
    password = Argument('password', required=False)
    role = Argument('role', type=int, required=False)
    customer_name = Argument('customer_name', required=False)
    address = Argument('address', required=False)
    telephone = Argument('telephone', required=False)


class UserInfoPostParser(BaseRequestParser):
    user_name = Argument('user_name', required=True)
    password = Argument('password', required=True)
    role = Argument('role', type=int, required=False, default=99)
    customer_name = Argument('customer_name', required=False)
    address = Argument('address', required=False)
    telephone = Argument('telephone', required=False)
    is_admin = Argument('is_admin', type=bool, required=True, default=False)
