# coding: utf-8
from ...util import Resource, api_response
from .....service.shop import (
    ShopService,
    ShopCompanyService,
    ShopCompanyContactService,
    ShopFeeService,
)
from ..req_param.shop import (
    CreateShopApiParser,
    CreateShopCompanyApiParser,
    SearchShopCompanyApiParser,
    ShopSearchApiParser,
    CreateShopCompanyContactApiParser,
    CreateShopFeeApiParser,
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
        """根据ID查询公司"""
        company = ShopCompanyService.get_by_id(id)
        contact_list = ShopCompanyContactService.get_by_company_id(id)
        company['contact_list'] = contact_list
        return api_response(data=company)

    def put(self, id):
        """根据ID修改公司信息"""
        parsed_data = self.parsed_data
        try:
            ShopCompanyService.update_shop_company_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        """根据ID删除公司"""
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


class CreateShopCompanyContactApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateShopCompanyContactApiParser(),
        }
    }

    def post(self):
        try:
            contact_id = \
                ShopCompanyContactService.create_contact(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response(data={'contact_id': contact_id})


class ShopCompanyContactApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateShopCompanyContactApiParser(),
        }
    }

    def get(self, id):
        contact = ShopCompanyContactService.get_by_id(id)
        return api_response(data=contact)

    def put(self, id):
        try:
            ShopCompanyContactService.update_contact(id, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            ShopCompanyContactService.delete_contact(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class GetShopCompanyContactApi(Resource):
    def get(self, company_id):
        contact_list = \
            ShopCompanyContactService.get_by_company_id(company_id)
        return api_response(data=contact_list)


class CreateShopFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateShopFeeApiParser(),
        }
    }

    def post(self):
        try:
            fee_id = ShopFeeService.create_fee(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response(data={'fee_id': fee_id})


class ShopFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateShopFeeApiParser(),
        }
    }

    def get(self, id):
        fee = ShopFeeService.get_fee_by_id(id)
        return api_response(data=fee)

    def put(self, id):
        try:
            ShopFeeService.update_fee_by_id(id, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            ShopFeeService.delete_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class GetShopFeeApi(Resource):
    def get(self, shop_id):
        fee_list = ShopFeeService.get_fee_by_shop_id(shop_id)
        return api_response(data=fee_list)
