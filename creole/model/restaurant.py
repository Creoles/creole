# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Index,
    Float,
)
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .mixins import BaseMixin
from ..util import Enum
from .country import Country, City
from ..exc import (
    raise_error_json,
    CreoleErrCode,
    ClientError,
    DatabaseError,
    InvalidateError,
)


class RestaurantCompany(Base, BaseMixin):
    __tablename__ = 'restaurant_company'
    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en', unique=True),
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
        )
        return table_args + BaseMixin.__table_args__

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        company = session.query(cls).filter(cls.id==id).first()
        return company

    @classmethod
    def delete(cls, id):
        session = DBSession()
        company = session.query(cls).filter(cls.id==id).first()
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_COMPANY_NOT_EXIST))
        session.delete(company)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create(cls, name, name_en):
        session = DBSession()
        company = cls(name=name, name_en=name_en)
        session.add(company)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        company = cls.get_by_id(id)
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_COMPANY_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(company, k, v)
        try:
            session.merge(company)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class Restaurant(Base, BaseMixin):
    __tablename__ = 'restaurant'

    TYPE = Enum(
        ('CHINESE', 1, u'中餐'),
        ('WESTERN', 2, u'西餐'),
        ('SPECIAL', 3, u'特色'),
        ('GENERAL', 4, u'综合'),
    )

    country_id = Column(Integer, nullable=False, doc=u'国家id')
    city_id = Column(Integer, nullable=False, doc=u'城市id')
    company_id = Column(Integer, nullable=False, doc=u'公司id')
    address = Column(String(80), nullable=False, doc=u'景点地址')
    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')
    restaurant_type = Column(TINYINT, nullable=False, doc=u'餐厅类型')
    contact = Column(Unicode(16), nullable=False, doc=u'联系人')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')
    intro_cn = Column(Unicode(128), nullable=True, doc=u'中文介绍')
    intro_en = Column(String(128), nullable=True, doc=u'英文介绍')
    meal_type = Column(Integer, nullable=False, doc=u'菜品ID')
