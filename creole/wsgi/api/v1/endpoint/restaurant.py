# coding: utf-8
from ...util import Resource, api_response
from .....service.restaurant import (
    RestaurantCompanyService,
    RestaurantService,
)
from ..req_param.restaurant import (
    CreateRestaurantCompanyApiParser,
    CreateRestaurantApiParser,
)
from creole.exc import ClientError


class RestaurantCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateRestaurantCompanyApiParser,
        }
    }

    def get(self, id):
        company = RestaurantCompanyService.get_by_id(id)
        return api_response(data=company)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            RestaurantCompanyService.update_restaurant_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            RestaurantCompanyService.delete_restaurant_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateRestaurantCompanyApi(Resource):
    """创建餐饮公司Api"""
    meta = {
        'args_parser_dict': {
            'post': CreateRestaurantCompanyApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            RestaurantCompanyService.create_restaurant_company(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class RestaurantApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateRestaurantApiParser,
        }
    }

    def get(self, id):
        restaurant = RestaurantService.get_by_id(id)
        return api_response(data=restaurant)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            RestaurantService.update_restaurant_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            RestaurantService.delete_restaurant_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateRestaurantApi(Resource):
    """创建餐饮公司Api"""
    meta = {
        'args_parser_dict': {
            'post': CreateRestaurantApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            RestaurantService.create_restaurant(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
