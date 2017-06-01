# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.hotel import Hotel
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
