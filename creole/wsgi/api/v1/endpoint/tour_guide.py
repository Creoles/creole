# coding: utf-8
from ...util import Resource, api_response
from .....service.tour_guide import (
    TourGuideService,
    TourGuideFeeService,
    TourGuideAccountService,
)
from ..req_param.tour_guide import (
    CreateTourGuideApiParser,
    CreateTourGuideFeeApiParser,
    EditTourGuideAccountApiParser,
)
from creole.exc import ClientError


class TourGuideApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateTourGuideApiParser,
        }
    }

    def get(self, id):
        tour_guide = TourGuideService.get_by_id(id)
        return api_response(data=tour_guide)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            TourGuideService.update_tour_guide_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            TourGuideService.delete_tour_guide_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateTourGuideApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateTourGuideApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            TourGuideService.create_tour_guide(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class TourGuideFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'put': CreateTourGuideFeeApiParser,
        }
    }

    def get(self, id):
        tour_guide_id = id
        fee = TourGuideFeeService.get_by_tour_guide_id(tour_guide_id)
        return api_response(data=fee)

    def put(self, id):
        parsed_data = self.parsed_data
        try:
            TourGuideFeeService.update_tour_guide_fee_by_id(id, **parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()

    def delete(self, id):
        try:
            TourGuideFeeService.delete_tour_guide_fee_by_id(id)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class CreateTourGuideFeeApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': CreateTourGuideFeeApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        try:
            TourGuideFeeService.create_tour_guide_fee(**parsed_data)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()


class TourGuideAccountApi(Resource):
    def get(self, tour_guide_id):
        account_list= \
            TourGuideAccountService.get_by_tour_guide_id(tour_guide_id)
        return api_response(data=account_list)


class EditTourGuideAccountApi(Resource):
    meta = {
        'args_parser_dict': {
            'post': EditTourGuideAccountApiParser,
        }
    }

    def post(self):
        parsed_data = self.parsed_data
        delete_id_list = parsed_data.get('delete_id_list', None)
        update_list = parsed_data.get('update_account_list', None)
        create_list = parsed_data.get('create_account_list', None)
        try:
            TourGuideAccountService.edit_tour_guide_account(
                create_list=create_list,
                update_list=update_list,
                delete_id_list=delete_id_list)
        except ClientError as e:
            return api_response(code=e.errcode, message=e.msg)
        return api_response()
