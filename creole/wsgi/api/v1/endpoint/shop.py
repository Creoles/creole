# coding: utf-8
from ...util import Resource, api_response
from .....service.shop import ShopService, ShopCompanyService
from ..req_param.shop import (
    CreateShopApiParser,
    CreateShopCompanyApiParser,
    SearchShopCompanyApiParser,
    ShopSearchApiParser,
)
from creole.exc import ClientError, CreoleErrCode
from creole.model.shop import Shop


class ShopApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateShopApiParser(),
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
            'post': CreateShopApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            ShopService.create_shop(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class ShopSearchApi(Resource):
    meta = {
        'args_parser_dict': {
            'get': ShopSearchApiParser(),
        }
    }
    def get(self):
        shop_type = self.parsed_data.get('shop_type', None)
        if shop_type and shop_type not in Shop.SHOP_TYPE.values():
            return api_response(code=CreoleErrCode.PARAMETER_ERROR)
        shop_data, total = ShopService.search_shop(**self.parsed_data)
        if self.parsed_data['page'] == 1:
            data = {'shop_data': shop_data, 'total': total}
        else:
            data = {'shop_data': shop_data}
        return api_response(data=data)

class ShopCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateShopCompanyApiParser(),
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
            'post': CreateShopCompanyApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            ShopCompanyService.create_shop_company(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class SearchShopCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'get': SearchShopCompanyApiParser(),
        }
    }

    def get(self):
        shop_company = \
            ShopCompanyService.search_company(**self.parsed_data)
        return api_response(data=shop_company)
