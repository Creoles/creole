# coding: utf-8
from ...util import Resource, api_response
from .....service.shop import ShopService, ShopCompanyService
from ..req_param.shop import (
    CreateShopApiParser,
    CreateShopCompanyApiParser,
)
from creole.exc import ClientError


class ShopApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateShopApiParser,
        }
    }

    def get(self, id):
        """根据ID查询店铺"""
        shop = ShopService.get_by_id(id)
        return api_response(data=shop)

    def put(self, id):
        """根据ID修改店铺信息"""
        parsed_data = self.parsed_data
        try:
            ShopService.update_shop_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        """根据ID删除店铺"""
        try:
            ShopService.delete_shop_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateShopApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateShopApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            ShopService.create_shop(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class ShopCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateShopCompanyApiParser,
        }
    }

    def get(self, id):
        """根据ID查询店铺"""
        shop = ShopCompanyService.get_by_id(id)
        return api_response(data=shop)

    def put(self, id):
        """根据ID修改店铺信息"""
        parsed_data = self.parsed_data
        try:
            ShopCompanyService.update_shop_company_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        """根据ID删除店铺"""
        try:
            ShopCompanyService.delete_shop_company_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateShopCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateShopCompanyApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            ShopCompanyService.create_shop_company(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
