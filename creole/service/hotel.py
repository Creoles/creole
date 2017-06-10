# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.hotel import (
    Hotel,
    HotelFee,
    RoomPrice,
    MealPrice,
    RoomAdditionalCharge,
    FestivalAdditionalCharge,
)
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
)


class HotelService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        hotel = Hotel.get_by_id(id)
        return cls._get_db_obj_data_dict(hotel)

    @classmethod
    def get_by_company_id(cls, company_id):
        hotel = Hotel.get_by_company_id(company_id)
        return cls._get_db_obj_data_dict(hotel)

    @classmethod
    def create_hotel(cls, country_id, city_id, company_id, address, name,
                     name_en, nickname_en, star_level, comment_level,
                     standard_room_number, standard_double_room_number,
                     triple_room_number, suite_room_number, tour_guide_room_number,
                     start_year, telephone, email, intro_cn=None, intro_en=None):
        Hotel.create(
            country_id=country_id, city_id=city_id, company_id=company_id,
            address=address, name=name, name_en=name_en, nickname_en=nickname_en,
            star_level=star_level, comment_level=comment_level,
            standard_room_number=standard_room_number,
            standard_double_room_number=standard_double_room_number,
            triple_room_number=triple_room_number,
            suite_room_number=suite_room_number,
            tour_guide_room_number=tour_guide_room_number,
            start_year=start_year, telephone=telephone, email=email,
            intro_cn=intro_cn, intro_en=intro_en
        )
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_hotel(cls, id, **kwargs):
        Hotel.updated(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_hotel(cls, id):
        Hotel.delete(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class HotelFeeService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        fee = HotelFee.get_by_id(id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def get_by_hotel_id(cls, hotel_id):
        fee = HotelFee.get_by_hotel_id(hotel_id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def create_hotel_fee(cls, hotel_id, confirm_person, free_policy=None,
                         free=None, note=None, attachment_hash=None):
        fee_id = HotelFee.create(
            hotel_id=hotel_id, confirm_person=confirm_person,
            free_policy=free_policy, free=free, note=note,
            attachment_hash=attachment_hash
        )
        session = DBSession()
        try:
            session.commit()
            return fee_id
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_fee(cls, id, **kwargs):
        HotelFee.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_fee(cls, id):
        HotelFee.delete(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class RoomPriceService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = RoomPrice.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_room_service(cls, create_list=None, update_list=None,
                          delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_room_price(create_list)
        if update_list:
            cls.update_room_price(update_list)
        if delete_id_list:
            cls.delete_room_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_room_price(cls, price_list):
        for price_dict in price_list:
            RoomPrice.create(**price_dict)

    @classmethod
    def update_room_price(cls, price_list):
        for price_dict in price_list:
            RoomPrice.update(**price_dict)

    @classmethod
    def delete_room_price(cls, delete_id_list):
        for id in delete_id_list:
            RoomPrice.delete(id)


class MealPriceService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = MealPrice.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_meal_service(cls, create_list=None, update_list=None,
                          delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_meal_price(create_list)
        if update_list:
            cls.update_meal_price(update_list)
        if delete_id_list:
            cls.delete_meal_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_meal_price(cls, price_list):
        for price_dict in price_list:
            MealPrice.create(**price_dict)

    @classmethod
    def update_meal_price(cls, price_list):
        for price_dict in price_list:
            MealPrice.update(**price_dict)

    @classmethod
    def delete_meal_price(cls, delete_id_list):
        for id in delete_id_list:
            MealPrice.delete(id)


class RoomAdditionalChargeService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = RoomAdditionalCharge.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_additional_charge_service(
            cls, create_list=None, update_list=None,
            delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_additional_charge_price(create_list)
        if update_list:
            cls.update_additional_charge_price(update_list)
        if delete_id_list:
            cls.delete_additional_charge_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            RoomAdditionalCharge.create(**price_dict)

    @classmethod
    def update_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            RoomAdditionalCharge.update(**price_dict)

    @classmethod
    def delete_additional_charge_price(cls, delete_id_list):
        for id in delete_id_list:
            RoomAdditionalCharge.delete(id)


class FestivalAdditionalChargeService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = FestivalAdditionalCharge.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_additional_charge_service(
            cls, create_list=None, update_list=None,
            delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_additional_charge_price(create_list)
        if update_list:
            cls.update_additional_charge_price(update_list)
        if delete_id_list:
            cls.delete_additional_charge_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            FestivalAdditionalCharge.create(**price_dict)

    @classmethod
    def update_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            FestivalAdditionalCharge.update(**price_dict)

    @classmethod
    def delete_additional_charge_price(cls, delete_id_list):
        for id in delete_id_list:
            FestivalAdditionalCharge.delete(id)
