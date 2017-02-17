# coding: utf-8
from flask_restful import Resource


class UserApi(Resource):
    TYPE = (
        ('uuid', 0, u'根据uuid查询'),
        ('id', 1, u'根据id查询'),
        ('name', 2, u'根据用户名查询'),
        ('customer_name', 3, u'根据客户名查询'),
    )

    def get(self, key, type):
        """查询用户信息"""
        pass

    def post(self):
        """添加新用户"""
        pass

    def put(self, key):
        """更新用户资料"""
        pass
