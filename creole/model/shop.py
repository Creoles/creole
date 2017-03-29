# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Float,
    Index,
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .country import Country, City
from .mixins import BaseMixin
from ..exc import (
    raise_error_json,
    InvalidateError,
    CreoleErrCode,
    DatabaseError,
    ClientError,
)
from ..util import Enum


class ShopCompany(Base, BaseMixin):
    """购物集团"""
    __tablename__ = 'shop_company'

    name = Column(Unicode(40), unique=True, nullable=False, doc=u'中文集团名')
    name_en = Column(String(60), unique=True, nullable=False, doc=u'英文集团名')

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
        company = DBSession().query(cls).filter(cls.id==id).first()
        return company

    @classmethod
    def delete(cls, id):
        session = DBSession()
        company = session.query(cls).filter(cls.id==id).first()
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_COMPANY_NOT_EXIST))
        session.delete(company)
        session.flush()

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
                ClientError(errcode=CreoleErrCode.SHOP_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        company = cls.get_by_id(id)
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_COMPANY_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(company, k, v)
        try:
            session.merge(company)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search(cls, name=None, name_en=None):
        session = DBSession()
        shop_company = None
        query = session.query(cls)
        if name:
            shop_company = query.filter(cls.name==name)
        elif name_en:
            shop_company = query.filter(cls.name_en==name_en)
        return shop_company


class Shop(Base, BaseMixin):
    """购物店"""
    __tablename__ = 'shop'

    SHOP_TYPE = Enum(
        ('JEWELRY', 1, u'珠宝'),
        ('TEA', 2, u'红茶'),
        ('OTHER', 3, u'其他'),
    )

    name = Column(Unicode(40), nullable=False, doc=u'中文店名')
    name_en = Column(String(60), nullable=False, doc=u'英文店名')
    address = Column(Unicode(100), nullable=False, doc=u'店铺地址')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')
    country_id = Column(Integer, nullable=False, doc=u'国家名')
    city_id = Column(Integer, nullable=False, doc=u'城市名')
    company_id = Column(Integer, nullable=True, doc=u'所属购物集团')
    shop_type = Column(TINYINT, nullable=False, doc=u'购物类型')

    contact = Column(Unicode(16), nullable=False, doc=u'联系人')
    fee_person = Column(Float(precision=3), nullable=False, doc=u'人头费')
    commission_ratio = Column(Float(precision=3), nullable=False, doc=u'佣金比例')

    average_score = Column(Float(precision=2), doc=u'平均评分')
    intro_cn = Column(Unicode(160), doc=u'中文介绍')
    intro_en = Column(String(160), doc=u'英文介绍')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en'),
            Index('idx_country_id_city_id_company_id_shop_type',
                  'country_id', 'city_id', 'company_id', 'shop_type'),
            Index('ix_average_score', 'average_score'),
            Index('ix_company_id', 'company_id'),
            Index('ix_country_id', 'country_id'),
            Index('ix_city_id', 'city_id'),
            Index('ix_shop_type', 'shop_type'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        shop_company = DBSession().query(ShopCompany).filter(
            ShopCompany.id==company_id).first()
        if not shop_company:
            raise_error_json(InvalidateError(args=('company_id' ,company_id,)))
        return company_id

    @validates('average_score')
    def _validate_average_score(self, key, average_score):
        if average_score > 5 or average_score < 0:
            raise_error_json(InvalidateError(msg='average score is invalid.'))
        return average_score

    @validates('shop_type')
    def _validate_shop_type(self, key, shop_type):
        if shop_type not in self.SHOP_TYPE.values():
            raise_error_json(InvalidateError(args=('shop_type', shop_type,)))
        return shop_type

    @validates('commission_ratio')
    def _validate_commission_ratio(self, key, commission_ratio):
        if commission_ratio > 100 or commission_ratio < 0:
            raise_error_json(
                InvalidateError(args=('commission_ratio', commission_ratio,)))
        return commission_ratio

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = DBSession().query(Country).filter(
            Country.id==country_id).first()
        if not country:
            raise_error_json(InvalidateError(args=('country_id', country_id,)))
        return country_id

    @classmethod
    def _validate_country_and_city(cls, country_id, city_id):
        city = DBSession().query(City).filter(
            City.id==city_id).first()
        if not city:
            raise_error_json(ClientError(errcode=CreoleErrCode.CITY_NOT_EXIST))
        elif city.country_id != country_id:
            raise_error_json(InvalidateError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        shop = session.query(cls).filter(cls.id==id).first()
        return shop

    @classmethod
    def get_by_company_id(cls, company_id):
        session = DBSession()
        shop_list = session.query(cls).filter(
            cls.company_id==company_id).all()
        return shop_list

    @classmethod
    def search(cls, country_id=None, city_id=None, company_id=None,
               shop_type=None, page=1, number=20):
        session = DBSession()
        query = session.query(cls)
        total = None
        if city_id:
            query = query.filter(cls.city_id==city_id)
        elif country_id:
            query = query.filter(cls.country_id==country_id)
        if company_id:
            query = query.filter(cls.company_id==company_id)
        if shop_type:
            query = query.filter(cls.shop_type==shop_type)
        if page == 1:
            total = query.count()
        shop_list = query.offset((page - 1) * number).limit(number).all()
        return shop_list, total

    @classmethod
    def create(cls, name, name_en, address, telephone, country_id,
               city_id, company_id, shop_type, contact, fee_person,
               commission_ratio, intro_cn='', intro_en=''):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        shop = cls(
            name=name, name_en=name_en, address=address,
            telephone=telephone, country_id=country_id,
            city_id=city_id, company_id=company_id, shop_type=shop_type,
            contact=contact, fee_person=fee_person, intro_cn=intro_cn,
            intro_en=intro_en, commission_ratio=commission_ratio)
        session.add(shop)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        shop = cls.get_by_id(id)
        if not shop:
            raise_error_json(ClientError(errcode=CreoleErrCode.SHOP_NOT_EXIST))
        if shop.country_id != kwargs['country_id'] \
                or shop.city_id != kwargs['city_id']:
            cls._validate_country_and_city(kwargs['country_id'], kwargs['city_id'])
        session = DBSession()
        for k, v in kwargs.iteritems():
            setattr(shop, k, v)
        try:
            session.merge(shop)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        shop = session.query(cls).filter(cls.id==id).first()
        if not shop:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_NOT_EXIST))
        session.delete(shop)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class ShopImage(Base, BaseMixin):
    """店铺对应的图片"""
    __tablename__ = 'shop_image'

    shop_id = Column(Integer, nullable=False, doc=u'店铺id')
    image_hash = Column(String(128), default=None)
