# coding: utf-8
from ...util import Resource, api_response
from .....service.vehicle import (
    VehicleService,
    VehicleCompanyService,
    VehicleAccountService,
    VehicleTypeService,
    VehicleFeeService,
    VehicleContactService,
)
from ..req_param.vehicle import (
    CreateVehicleApiParser,
    CreateVehicleCompanyApiParser,
    SearchVehicleCompanyApiParser,
    VehicleSearchApiParser,
    CreateVehicleAccountApiParser,
    CreateVehicleFeeApiParser,
    CreateVehicleTypeApiParser,
    CreateVehicleContactApiParser,
)
from creole.exc import ClientError, CreoleErrCode
from .....util import timestamp_to_datetime


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
            VehicleCompanyService.delete_vehicle_company_by_id(id)
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
            VehicleCompanyService.create_vehicle_company(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class SearchVehicleCompanyApi(Resource):
    meta = {
        'args_parser_dict': {
            'get': SearchVehicleCompanyApiParser,
        }
    }

    def get(self):
        vehicle_company = \
            VehicleCompanyService.search_company(**self.parsed_data)
        return api_response(data=vehicle_company)


class VehicleAccountApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateVehicleAccountApiParser,
        }
    }

    def get(self, id):
        data = VehicleAccountService.get_by_id(id)
        return api_response(data=data)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            VehicleAccountService.\
                update_account_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            VehicleAccountService.delete_account_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateVehicleAccountApi(Resource):
    """创建车辆账号信息"""
    meta = {
        'args_parser_dict': {
            'post': CreateVehicleAccountApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            VehicleAccountService.create_account(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class VehicleTypeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateVehicleTypeApiParser,
        }
    }

    def get(self, id):
        vehicle_type = VehicleTypeService.get_type_by_id(id)
        return api_response(data=vehicle_type)

    def put(self, id):
        try:
            VehicleTypeService.update_type_by_id(id, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            VehicleTypeService.delete_type_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateVehicleTypeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateVehicleTypeApiParser,
        }
    }

    def post(self):
        try:
            VehicleTypeService.create_type(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class VehicleFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateVehicleFeeApiParser,
        }
    }

    def get(self, id):
        fee = VehicleFeeService.get_by_id(id)
        return api_response(data=fee)

    def put(self, id):
        parsed_data = self.parsed_data
        start_time_stamp = int(parsed_data['start_time'])
        end_time_stamp = int(parsed_data['end_time'])
        parsed_data['start_time'] = timestamp_to_datetime(start_time_stamp)
        parsed_data['end_time'] = timestamp_to_datetime(end_time_stamp)
        try:
            VehicleTypeService.update_type_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            VehicleFeeService.delete_fee_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateVehicleFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateVehicleFeeApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        start_time_stamp = int(parsed_data['start_time'])
        end_time_stamp = int(parsed_data['end_time'])
        parsed_data['start_time'] = timestamp_to_datetime(start_time_stamp)
        parsed_data['end_time'] = timestamp_to_datetime(end_time_stamp)
        try:
            VehicleFeeService.create_fee(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class VehicleContactApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateVehicleContactApiParser,
        }
    }

    def get(self, id):
        contact = VehicleContactService.get_contact_by_id(id)
        return api_response(data=contact)

    def put(self, id):
        try:
            VehicleContactService.update_contact(id, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            VehicleContactService.delete_contact(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateVehicleContactApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateVehicleContactApiParser,
        }
    }

    def post(self):
        try:
            VehicleContactService.create_contact(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


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
            return api_response(code=CreoleErrCode.PARAMETER_ERROR)
        try:
            vehicle_list, total = VehicleService.search_vehicle(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        if self.parsed_data['page'] == 1:
            data = {'vehicle_data': vehicle_list, 'total': total}
        else:
            data = {'vehicle_data': vehicle_list}
        return api_response(data=data)
