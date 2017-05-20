# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.attraction import Attraction, AttractionFee
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
)


class AttractionService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        attraction = Attraction.get_by_id(id)
        return cls._get_db_obj_data_dict(attraction)

    @classmethod
    def create_attraction(cls, country_id, city_id, address, name, name_en,
                          nickname_en, intro_cn, intro_en, note=None):
        Attraction.create(
            country_id=country_id, city_id=city_id,
            address=address, name=name, name_en=name_en,
            nickname_en=nickname_en, note=note,
            intro_cn=intro_cn, intro_en=intro_en)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_attraction_by_id(cls, id, **kwargs):
        Attraction.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_attraction_by_id(cls, id):
        Attraction.delete(id)
        AttractionFee.delete_by_attraction_id(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_attraction(cls, country_id=None, city_id=None,
                          name=None, page=1, number=20):
        raw_data = []
        attraction_list, total = Attraction.search(
            country_id=country_id, city_id=city_id,
            name=None, page=page, number=number)
        for attraction in attraction_list:
            raw_data.append(cls._get_db_obj_data_dict(attraction))
        return raw_data, total


class AttractionFeeService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        fee = AttractionFee.get_by_id(id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def create_attraction_fee(cls, attraction_id, public_price, company_price,
                              tour_guide_price, translator_price, free_policy,
                              child_discount, note=None):
        session = DBSession()
        AttractionFee.create(
            attraction_id=attraction_id, public_price=public_price,
            company_price=company_price, tour_guide_price=tour_guide_price,
            translator_price=translator_price, free_policy=free_policy,
            child_discount=child_discount, note=note
        )
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_fee(cls, id, **kwargs):
        session = DBSession()
        AttractionFee.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_fee(cls, id):
        session = DBSession()
        AttractionFee.delete(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def get_by_attraction_id(cls, attraction_id):
        fee = AttractionFee.get_by_attraction_id(attraction_id)
        return cls._get_db_obj_data_dict(fee)
