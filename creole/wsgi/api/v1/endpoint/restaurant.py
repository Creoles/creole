# coding: utf-8
from ...util import Resource, api_response
from .....service.restaurant import (
    RestaurantService,
    RestaurantAccountService,
    MealService,
)
from ..req_param.restaurant import (
    EditMealApiParser,
    CreateRestaurantApiParser,
    SearchRestaurantApiParser,
)
from creole.exc import ClientError


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


class RestaurantAccountApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateRestaurantApiParser,
        }
    }

    def get(self, id):
        account = RestaurantAccountService.get_by_restaurant_id(id)
        return api_response(data=account)

    def delete(self, id):
        try:
            RestaurantAccountService.delete_account_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def put(self, id):
        try:
            RestaurantAccountService.update_account_by_id(id, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateRestaurantAccountApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateRestaurantApiParser,
        }
    }

    def post(self):
        try:
            RestaurantAccountService.create_account(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class MealApi(Resource):
    def get(self, restaurant_id):
        """根据restaurant_id获取餐厅下的套餐类型"""
        meal_list = MealService.get_by_restaurant_id(restaurant_id)
        return api_response(data=meal_list)


class EditMealApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': EditMealApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        delete_id_list = parsed_data.get('delete_id_list', None)
        update_list = parsed_data.get('update_meal_list', None)
        create_list = parsed_data.get('create_meal_list', None)
        try:
            MealService.edit_meal(
                create_list=create_list,
                update_list=update_list,
                delete_id_list=delete_id_list)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
