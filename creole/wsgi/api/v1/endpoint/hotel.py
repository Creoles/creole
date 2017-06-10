# coding: utf-8
from ...util import Resource, api_response
from .....service.hotel import (
    HotelService,
    HotelFeeService,
    RoomPriceService,
    MealPriceService,
    RoomAdditionalChargeService,
    FestivalAdditionalChargeService,
)
from ..req_param.restaurant import (
    CreateHotelApiParser,
    CreateHotelFeeApiParser,
    EditRoomPriceApiParser,
    EditMealPriceApiParser,
    EditRoomAdditionalChargeApiParser,
    EditFestivalAdditionalChargeApiParser,
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


class CreateHotelFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateHotelFeeApiParser(),
        }
    }

    def post(self):
        try:
            fee_id = HotelFeeService.create_hotel_fee(**self.parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response(data={'fee_id': fee_id})


class HotelFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateHotelFeeApiParser(),
        }
    }

    def get(self, id):
        fee = HotelFeeService.get_by_id(id)
        return api_response(data=fee)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            HotelFeeService.update_fee(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            HotelFeeService.delete_fee(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class GetHotelFeeApi(Resource):
    def get(cls, hotel_id):
        fee = HotelFeeService.get_by_hotel_id(hotel_id)
        return api_response(data=fee)


class EditRoomPriceApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': EditRoomPriceApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        delete_id_list = parsed_data.get('delete_id_list', None)
        update_list = parsed_data.get('update_list', None)
        create_list = parsed_data.get('create_list', None)
        try:
            RoomPriceService.edit_room_service(
                create_list=create_list,
                update_list=update_list,
                delete_id_list=delete_id_list
            )
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class EditMealPriceApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': EditMealPriceApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        delete_id_list = parsed_data.get('delete_id_list', None)
        update_list = parsed_data.get('update_list', None)
        create_list = parsed_data.get('create_list', None)
        try:
            MealPriceService.edit_meal_service(
                create_list=create_list,
                update_list=update_list,
                delete_id_list=delete_id_list
            )
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class EditRoomAdditionalChargeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': EditRoomAdditionalChargeApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        delete_id_list = parsed_data.get('delete_id_list', None)
        update_list = parsed_data.get('update_list', None)
        create_list = parsed_data.get('create_list', None)
        try:
            RoomAdditionalChargeService.edit_additional_charge_service(
                create_list=create_list,
                update_list=update_list,
                delete_id_list=delete_id_list
            )
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class EditFestivalAdditionalChargeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': EditFestivalAdditionalChargeApiParser(),
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        delete_id_list = parsed_data.get('delete_id_list', None)
        update_list = parsed_data.get('update_list', None)
        create_list = parsed_data.get('create_list', None)
        try:
            FestivalAdditionalChargeService.edit_additional_charge_service(
                create_list=create_list,
                update_list=update_list,
                delete_id_list=delete_id_list
            )
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
