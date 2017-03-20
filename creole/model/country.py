# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Index,
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

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

    name = Column(Unicode(20), unique=True, nullable=False, doc=u'国家名')
    name_en = Column(String(40), unique=True, nullable=False, doc=u'国家名, 英文')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en', unique=True),
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
        )
        return table_args + BaseMixin.__table_args__

    @classmethod
    def get(cls, id):
        country = DBSession().query(cls).filter(cls.id==id).first()
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
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.COUNTRY_NAME_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        country = session.query(cls).filter(cls.id==id).first()
        if not country:
            raise_error_json(ClientError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))
        session.delete(country)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create(cls, name, name_en):
        session = DBSession()
        country = cls(name=name, name_en=name_en)
        session.add(country)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.COUNTRY_NAME_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class City(Base, BaseMixin):
    __tablename__ = 'city'

    name = Column(Unicode(20), unique=True, nullable=False, doc=u'城市名')
    name_en = Column(String(40), unique=True, nullable=False, doc=u'城市名, 英文')
    country_id = Column(Integer, nullable=False, doc=u'国家ID')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en', unique=True),
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
            Index('ix_country_id', 'country_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = Country.get(country_id)
        if not country:
            raise_error_json(ClientError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))
        return country_id

    @classmethod
    def get(cls, id):
        city = DBSession().query(cls).filter(cls.id==id).first()
        return city

    @classmethod
    def get_by_country_id(cls, country_id):
        city_list = DBSession().query(cls).filter(
            cls.country_id==country_id).all()
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
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.CITY_NAME_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete(cls, id, **kwargs):
        session = DBSession()
        country = session.query(cls).filter(cls.id==id).first()
        if not country:
            raise_error_json(ClientError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))
        session.delete(country)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create(cls, name, name_en, country_id):
        session = DBSession()
        city = cls(
            name=name, name_en=name_en, country_id=country_id)
        session.add(city)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.CITY_NAME_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
