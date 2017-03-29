# coding: utf-8
from ...util import Resource, api_response
from .....service.restaurant import (
    RestaurantCompanyService,
    RestaurantService,
    MealService,
)
from ..req_param.restaurant import (
    CreateRestaurantCompanyApiParser,
    SearchRestaurantCompanyApiParser,
    CreateRestaurantApiParser,
    SearchRestaurantApiParser,
    CreateMealApiParser,
    PutMealApiParser,
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
            RestaurantCompanyService.update_restaurant_company_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            RestaurantCompanyService.delete_restaurant_company_by_id(id)
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


class SearchRestaurantCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'get': SearchRestaurantCompanyApiParser,
        }
    }

    def get(self):
        restaurant_company = \
            RestaurantCompanyService.search_company(**self.parsed_data)
        return api_response(data=restaurant_company)


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


class SearchRestaurantApi(Resource):
    meta = {
        'args_parser_dict': {
            'get': SearchRestaurantApiParser,
        }
    }

    def get(self):
        restaurant_data, total = \
            RestaurantService.search_restaurant(**self.parsed_data)
        if self.parsed_data['page'] == 1:
            data = {'restaurant_data': restaurant_data, 'total': total}
        else:
            data = {'restaurant_data': restaurant_data}
        return api_response(data=data)


class CreateMealApi(Resource):
    """创建套餐Api"""
    meta = {
        'args_parser_dict': {
            'post': CreateMealApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            MealService.create_meal(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class MealApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': PutMealApiParser,
        }
    }

    def get(self, id):
        """根据restaurant_id获取餐厅下的套餐类型
        这里的id是restaurant_id"""
        restaurant_id = id
        meal_list = MealService.get_by_restaurant_id(restaurant_id)
        return api_response(data=meal_list)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            MealService.update_meal_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            MealService.delete_meal_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
