# coding: utf-8
from ...util import Resource, api_response
from .....service.vehicle import VehicleService, VehicleCompanyService
from ..req_param.vehicle import (
    CreateVehicleApiParser,
    CreateVehicleCompanyApiParser,
    VehicleSearchApiParser,
)
from creole.exc import ClientError, CreoleErrCode


class VehicleApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateVehicleApiParser,
        }
    }

    def get(self, id):
        vehicle = VehicleService.get_by_id(id)
        return api_response(data=vehicle)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            VehicleService.update_vehicle_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            VehicleService.delete_vehicle_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateVehicleApi(Resource):
    """创建车辆Api"""
    meta = {
        'args_parser_dict': {
            'post': CreateVehicleApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            VehicleService.create_vehicle(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class SearchVehicleApi(Resource):
    """搜索车辆Api"""
    meta = {
        'args_parser_dict': {
            'get': VehicleSearchApiParser,
        }
    }

    def get(self):
        operation = self.parsed_data.get('operation', None)
        seat = self.parsed_data.get('seat', None)
        if (seat and operation is None) or (seat is None and operation):
            api_response(code=CreoleErrCode.PARAMETER_ERROR)
        vehicle_list, total = VehicleService.search_vehicle(**self.parsed_data)
        if self.parsed_data['page'] == 1:
            data = {'vehicle_data': vehicle_list, 'total': total}
        else:
            data = {'vehicle_data': vehicle_list}
        return api_response(data=data)


class VehicleCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateVehicleCompanyApiParser,
        }
    }

    def get(self, id):
        company = VehicleCompanyService.get_by_id(id)
        return api_response(data=company)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            VehicleCompanyService.update_vehicle_company_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            VehicleCompanyService.delete_shop_company_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateVehicleCompanyApi(Resource):
    """创建车辆公司Api"""
    meta = {
        'args_parser_dict': {
            'post': CreateVehicleCompanyApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            VehicleCompanyService.create_shop_company(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
