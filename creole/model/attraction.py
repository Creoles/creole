# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Index,
    Float,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .mixins import BaseMixin
from .country import Country, City
from ..exc import (
    raise_error_json,
    CreoleErrCode,
    ClientError,
    InvalidateError,
)


class AttractionFee(Base, BaseMixin):
    __tablename__ = 'attraction_fee'

    attraction_id = Column(Integer, unique=True, nullable=False, doc=u'景点id')
    public_price = Column(Float(3), nullable=False, doc=u'公开价')
    company_price = Column(Float(3), nullable=False, doc=u'公司价')
    tour_guide_price = Column(Float(3), nullable=False, doc=u'导游价')
    translator_price = Column(Float(3), nullable=False, doc=u'翻译价')
    free_policy = Column(Integer, nullable=False, doc=u'免票政策')
    child_discount = Column(Float(3), nullable=False, doc=u'儿童折扣')
    note = Column(String(100), nullable=True, doc=u'备注')

    @validates('attraction_id')
    def _validate_attraction_id(self, key, attraction_id):
        attraction = DBSession().query(Attraction).filter(
            Attraction.id==attraction_id).first()
        if not attraction:
            raise_error_json(InvalidateError(args=('attraction_id', attraction_id,)))
        return attraction_id

    @validates('child_discount')
    def _validate_child_discount(self, key, child_discount):
        if not (child_discount > 0 and child_discount <= 1):
            raise_error_json(InvalidateError(args=('child_discount', child_discount,)))
        return child_discount

    @classmethod
    def get_by_attraction_id(cls, attraction_id):
        session = DBSession()
        fee = session.query(cls).filter(
            cls.attraction_id==attraction_id).first()
        return fee

    @classmethod
    def create(cls, attraction_id, public_price, company_price, tour_guide_price,
               translator_price, free_policy, child_discount, note=None):
        session = DBSession()
        fee = cls(
            attraction_id=attraction_id, public_price=public_price,
            company_price=company_price, tour_guide_price=tour_guide_price,
            translator_price=translator_price, free_policy=free_policy,
            child_discount=child_discount, note=note
        )
        session.add(fee)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_FEE_DUPLICATED))
        return fee

    @classmethod
    def update(cls, id, **kwargs):
        fee = cls.get_by_id(id)
        if not fee:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(fee, k, v)
        session = DBSession()
        session.merge(fee)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_FEE_DUPLICATED))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        fee = session.query(cls).filter(cls.id==id).first()
        if not fee:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_FEE_NOT_EXIST))
        session.delete(fee)
        session.flush()

    @classmethod
    def delete_by_attraction_id(cls, attraction_id):
        session = DBSession()
        fee = cls.get_by_attraction_id(attraction_id)
        if fee:
            session.delete(fee)
            session.flush()


class Attraction(Base, BaseMixin):
    __tablename__ = 'attraction'

    country_id = Column(Integer, nullable=False, doc=u'国家id')
    city_id = Column(Integer, nullable=False, doc=u'城市id')
    address = Column(String(80), nullable=False, doc=u'景点地址')
    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')
    nickname_en = Column(String(30), unique=True, nullable=False, doc=u' 英文简称')
    intro_cn = Column(Unicode(128), nullable=True, doc=u'中文简介')
    intro_en = Column(String(128), nullable=True, doc=u'英文简介')
    note = Column(String(100), nullable=True, doc=u'备注')

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
               name_en, nickname_en, intro_cn, intro_en, note=None):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        attraction = cls(
            country_id=country_id, city_id=city_id,
            address=address, name=name, name_en=name_en,
            nickname_en=nickname_en, note=note,
            intro_cn=intro_cn, intro_en=intro_en)
        session.add(attraction)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_DUPLICATED))

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
        session.merge(attraction)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_DUPLICATED))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        attraction = session.query(cls).filter(cls.id==id).first()
        if not attraction:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ATTRACTION_NOT_EXIST))
        session.delete(attraction)
        session.flush()

    @classmethod
    def search(cls, country_id=None, city_id=None, name=None, page=1, number=20):
        """根据国家或者城市id查找"""
        query = DBSession().query(cls)
        total = None
        if name:
            attraction_list = query.filter(cls.name==name).all()
        else:
            if city_id:
                query = query.filter(cls.city_id==city_id)
            elif country_id:
                query = query.filter(cls.country_id==country_id)
            if page == 1:
                total = query.count()
            attraction_list = query.offset((page - 1) * number).limit(number).all()
        return attraction_list, total
