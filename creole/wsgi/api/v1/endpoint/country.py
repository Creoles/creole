# coding: utf-8
from ...util import Resource, api_response
from .....service.country import CountryService, CityService
from ..req_param.country import CountryApiParser, CityApiParser
from creole.exc import ClientError


class CountryApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CountryApiParser(),
        }
    }

    def get(self, id):
        """根据Id查询国家"""
        country = CountryService.get_by_id(id)
        return api_response(data=country)

    def put(self, id):
        """修改国家资料"""
        parsed_data = self.parsed_data
        try:
            CountryService.update_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        """删除国家"""
        try:
            CountryService.delete_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class AllCountryApi(Resource):
    def get(self):
        """获取全部国家信息"""
        country_list = CountryService.get_all_country()
        return api_response(data=country_list) 


class CreateCountryApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CountryApiParser(),
        }
    }

    def post(self):
        """添加国家"""
        try:
            CountryService.create_country(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CityApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CityApiParser(),
        }
    }

    def get(self, id):
        """根据Id查询城市"""
        country = CityService.get_by_id(id)
        return api_response(data=country)

    def put(self, id):
        """修改城市资料"""
        parsed_data = self.parsed_data
        try:
            CityService.update_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        """删除城市"""
        try:
            CityService.delete_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateCityApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CityApiParser(),
        }
    }

    def post(self):
        """添加国家"""
        try:
            CityService.create_city(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
