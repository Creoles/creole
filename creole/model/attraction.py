# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Index,
    Float,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .mixins import BaseMixin
from .country import Country, City
from ..exc import (
    raise_error_json,
    CreoleErrCode,
    ClientError,
    DatabaseError,
    InvalidateError,
)


class Attraction(Base, BaseMixin):
    __tablename__ = 'attraction'

    country_id = Column(Integer, nullable=False, doc=u'国家id')
    city_id = Column(Integer, nullable=False, doc=u'城市id')
    address = Column(String(80), nullable=False, doc=u'景点地址')
    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')
    adult_fee = Column(Float(precision=3), nullable=False, doc=u'成人门票')
    child_fee = Column(Float(precision=3), nullable=False, doc=u'儿童门票')
    intro_cn = Column(Unicode(128), nullable=True, doc=u'中文简介')
    intro_en = Column(String(128), nullable=True, doc=u'英文简介')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_country_id', 'country_id'),
            Index('ix_city_id', 'city_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = DBSession().query(Country).filter(
            Country.id==country_id).first()
        if not country:
            raise_error_json(InvalidateError(args=('country_id', country_id,)))
        return country_id

    @classmethod
    def _validate_country_and_city(cls, country_id, city_id):
        city = DBSession().query(City).filter(City.id==city_id).first()
        if not city:
            raise_error_json(ClientError(errcode=CreoleErrCode.CITY_NOT_EXIST))
        elif city.country_id != country_id:
            raise_error_json(InvalidateError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))

    @classmethod
    def create(cls, country_id, city_id, address, name,
               name_en, adult_fee, child_fee, intro_cn, intro_en):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        attraction = cls(
            country_id=country_id, city_id=city_id,
            address=address, name=name, name_en=name_en,
            adult_fee=adult_fee, child_fee=child_fee,
            intro_cn=intro_cn, intro_en=intro_en)
        try:
            session.add(attraction)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


    @classmethod
    def update(cls, id, **kwargs):
        attraction = cls.get_by_id(id)
        if not attraction:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_NOT_EXIST))
        if attraction.country_id != kwargs['country_id'] \
                or attraction.city_id != kwargs['city_id']:
            cls._validate_country_and_city(kwargs['country_id'], kwargs['city_id'])
        for k, v in kwargs.iteritems():
            setattr(attraction, k, v)
        session = DBSession()
        try:
            session.merge(attraction)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        attraction = session.query(cls).filter(cls.id==id).first()
        return attraction

    @classmethod
    def delete(cls, id):
        session = DBSession()
        attraction = session.query(cls).filter(cls.id==id).first()
        if not attraction:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_NOT_EXIST))
        session.delete(attraction)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search(cls, country_id=None, city_id=None, name=None, page=1, number=20):
        """根据国家或者城市id查找"""
        query = DBSession().query(cls)
        total = None
        if city_id:
            query = query.filter(cls.city_id==city_id)
        elif country_id:
            query = query.filter(cls.country_id==country_id)
        if name:
            query = query.filter(cls.name==name)
        if page == 1:
            total = query.count()
        attraction_list = query.offset((page - 1) * number).limit(number).all()
        return attraction_list, total

