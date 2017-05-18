# coding: utf-8
from ...util import Resource, api_response
from .....service.attraction import AttractionService, AttractionFeeService
from ..req_param.attraction import (
    CreateAttractionApiParser,
    SearchAttractionApiParser,
    CreateAttractionFeeApiParser,
)
from creole.exc import ClientError


class AttractionApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateAttractionApiParser(),
        }
    }

    def get(self, id):
        attraction = AttractionService.get_by_id(id)
        return api_response(data=attraction)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            AttractionService.update_attraction_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            AttractionService.delete_attraction_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateAttractionApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateAttractionApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            AttractionService.create_attraction(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class SearchAttractionApi(Resource):
    meta = {
        'args_parser_dict': {
            'get': SearchAttractionApiParser(),
        }
    }

    def get(self):
        try:
            attraction_list, total = \
                AttractionService.search_attraction(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        if self.parsed_data['page'] == 1:
            data = {'attraction_data': attraction_list, 'total': total}
        else:
            data = {'attraction_data': attraction_list}
        return api_response(data=data)


class AttractionFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateAttractionFeeApiParser(),
        }
    }

    def get(self, id):
        fee = AttractionFeeService.get_by_id(id)
        return api_response(data=fee)

    def put(self, id):
        try:
            fee_id = AttractionFeeService.update_fee(id, **self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response(data={'fee_id': fee_id})

    def delete(self, id):
        try:
            AttractionFeeService.delete_fee(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class GetAttractionFeeApi(Resource):
    def get(self, attraction_id):
        fee = AttractionFeeService.get_by_attraction_id(id)
        return api_response(data=fee)


class CreateAttractionFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateAttractionFeeApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            AttractionFeeService.create_attraction_fee(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
