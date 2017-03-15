# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import validates

from . import Base, DBSession
from .mixins import BaseMixin
from ..exc import (
    raise_error_json,
    ParameterError,
    DatabaseError,
    ClientError,
    CreoleErrCode,
)


class Country(Base, BaseMixin):
    __tablename__ = 'country'

    name = Column(Unicode(20), nullable=False, doc=u'国家名')
    name_en = Column(String(40), nullable=False, doc=u'国家名, 英文')

    @validates('name')
    def _validate_name(self, key, name):
        country = DBSession().query(Country).filter(
            Country.name==name,
            Country.is_delete==Country.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if country:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.COUNTRY_NAME_DUPLICATED))
        return name

    @validates('name_en')
    def _validate_name_en(self, key, name_en):
        country = DBSession().query(Country).filter(
            Country.name_en==name_en,
            Country.is_delete==Country.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if country:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.COUNTRY_NAME_DUPLICATED))
        return name_en

    @classmethod
    def get(cls, id):
        country = DBSession().query(cls).filter(
            cls.id==id,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return country

    @classmethod
    def get_all(cls):
        country_list = DBSession().query(cls).all()
        return country_list

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        country = cls.get(id)
        if country is None:
            raise_error_json(ParameterError(args=(id,)))
        for k, v in kwargs.iteritems():
            setattr(country, k, v)
        try:
            session.merge(country)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete(cls, id):
        DBSession().query(cls).filter(
            cls.id==id
        ).update(
            {'is_delete': cls.FIELD_STATUS.FIELD_STATUS_DELETED},
            synchronize_session=False)

    @classmethod
    def create(cls, name, name_en):
        session = DBSession()
        country = cls(name=name, name_en=name_en)
        session.add(country)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class City(Base, BaseMixin):
    __tablename__ = 'city'

    name = Column(Unicode(20), nullable=False, doc=u'城市名')
    name_en = Column(String(40), nullable=False, doc=u'城市名, 英文')
    country_id = Column(Integer, nullable=False, doc=u'国家ID')

    @validates('name')
    def _validate_name(self, key, name):
        city = DBSession().query(City).filter(
            City.name==name,
            City.is_delete==City.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if city:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.CITY_NAME_DUPLICATED))
        return name

    @validates('name_en')
    def _validate_name_en(self, key, name_en):
        city = DBSession().query(City).filter(
            City.name_en==name_en,
            City.is_delete==City.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if city:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.CITY_NAME_DUPLICATED))
        return name_en

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = Country.get(country_id)
        if not country:
            raise_error_json(ClientError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))
        return country

    @classmethod
    def get(cls, id):
        city = DBSession().query(cls).filter(
            cls.id==id,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return city

    @classmethod
    def get_by_country_id(cls, country_id):
        city_list = DBSession().query(cls).filter(
            cls.country_id==country_id,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).all()
        return city_list

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        city = cls.get(id)
        if city is None:
            raise_error_json(ParameterError(args=(id,)))
        for k, v in kwargs.iteritems():
            setattr(city, k, v)
        try:
            session.merge(city)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete(cls, id, **kwargs):
        DBSession().query(cls).filter(
            cls.id==id
        ).update(
            {'is_delete': cls.FIELD_STATUS.FIELD_STATUS_DELETED},
            synchronize_session=False)

    @classmethod
    def create(cls, name, name_en, country_id):
        session = DBSession()
        city = cls(
            name=name, name_en=name_en, country_id=country_id)
        session.add(city)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
