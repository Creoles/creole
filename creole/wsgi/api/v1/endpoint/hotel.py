# coding: utf-8
from ...util import Resource, api_response
from .....service.hotel import (
    HotelService,
)
from ..req_param.restaurant import (
    CreateHotelApiParser,
)
from creole.exc import ClientError


class HotelApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateHotelApiParser(),
        }
    }

    def get(self, id):
        hotel = HotelService.get_by_id(id)
        return api_response(data=hotel)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            HotelService.update_hotel(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            HotelService.delete_hotel(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class GetHotelApi(Resource):
    def get(self, company_id):
        hotel_list = HotelService.get_by_company_id(id)
        return api_response(data=hotel_list)


class CreateHotelApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateHotelApiParser(),
        }
    }

    def post(self):
        try:
            HotelService.create_hotel(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
