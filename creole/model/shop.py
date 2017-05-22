# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Float,
    Index,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .country import Country, City
from .base import BaseMixin
from .mixins import CompanyMixin, ContactMixin
from ..exc import (
    raise_error_json,
    InvalidateError,
    CreoleErrCode,
    ClientError,
)
from ..util import Enum


class ShopCompany(Base, CompanyMixin):
    """购物集团"""
    __tablename__ = 'shop_company'

    intro = Column(String(500), nullable=False, doc=u'公司简介')

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
    def create(cls, country_id, city_id, name, name_en,
               nickname_en, register_number, intro=None):
        session = DBSession()
        company = cls(
            country_id=country_id, city_id=city_id, name=name,
            name_en=name_en, nickname_en=nickname_en,
            register_number=register_number, intro=intro)
        session.add(company)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_COMPANY_DUPLICATED))

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
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_COMPANY_DUPLICATED))

    @classmethod
    def search(cls, name=None, name_en=None, is_all=False):
        session = DBSession()
        shop_company = None
        query = session.query(cls)
        if is_all:
            shop_company = query.all()
        elif name:
            shop_company = query.filter(cls.name==name).first()
        elif name_en:
            shop_company = query.filter(cls.name_en==name_en).first()
        return shop_company


class ShopCompanyContact(Base, ContactMixin):
    __tablename__ = 'shop_company_contact'

    company_id = Column(Integer, nullable=False, doc=u'公司id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_company_id', 'company_id'),
        )
        return table_args + ContactMixin.__table_args__

    @classmethod
    def get_by_company_id(cls, company_id):
        session = DBSession()
        return session.query(cls).filter(cls.company_id==company_id).all()

    @classmethod
    def create(cls, contact, position, telephone, email, company_id):
        session = DBSession()
        person = cls(
            contact=contact, position=position,
            telephone=telephone, email=email,
            company_id=company_id
        )
        session.add(person)
        session.flush()
        return person

    @classmethod
    def delete_by_company_id(cls, company_id):
        contact_list = cls.get_by_company_id(company_id)
        session = DBSession()
        for item in contact_list:
            session.delete(item)
        session.flush()


class ShopFee(Base, BaseMixin):
    __tablename__ = 'shop_fee'
    ACCOUNT_PERIOD = Enum(
        ('NOW', 1, u'现结'),
        ('MONTH', 2, u'月结'),
    )
    ACCOUNT_WAY = Enum(
        ('CASH', 1, u'现金'),
        ('CHECK', 2, u'支票'),
        ('TRANSFER', 3, u'转账'),
    )

    shop_id = Column(Integer, unique=True, nullable=False, doc=u'商店ID')
    fee_person = Column(Float(precision=3), nullable=False, doc=u'人头费')
    company_ratio = Column(Float(precision=3), nullable=False, doc=u'公司返佣比例')
    tour_guide_ratio = Column(Float(precision=3), nullable=False, doc=u'导游返佣比例')
    account_period = Column(TINYINT, nullable=False, doc=u'结算周期')
    account_way = Column(TINYINT, nullable=False, doc=u'结算方式')
    note = Column(String(100), nullable=True, doc=u'备注')

    @validates('shop_id')
    def _validate_shop_id(self, key, shop_id):
        shop = DBSession().query(Shop).filter(Shop.id==shop_id).first()
        if not shop:
            raise_error_json(InvalidateError(args=('shop_id' ,shop_id,)))
        return shop_id

    @validates('account_way')
    def _validate_account_way(self, key, account_way):
        if account_way not in self.ACCOUNT_WAY.values():
            raise_error_json(InvalidateError(args=('account_way', account_way,)))
        return account_way

    @validates('account_period')
    def _validate_account_period(self, key, account_period):
        if account_period not in self.ACCOUNT_PERIOD.values():
            raise_error_json(InvalidateError(args=('account_period', account_period,)))
        return account_period

    @validates('company_ratio')
    def _validate_company_ratio(self, key, company_ratio):
        if company_ratio > 1 or company_ratio < 0:
            raise_error_json(
                InvalidateError(args=('company_ratio', company_ratio,)))
        return company_ratio

    @validates('tour_guide_ratio')
    def _validate_tour_guide_ratio(self, key, tour_guide_ratio):
        if tour_guide_ratio > 1 or tour_guide_ratio < 0:
            raise_error_json(
                InvalidateError(args=('tour_guide_ratio', tour_guide_ratio,)))
        return tour_guide_ratio

    @classmethod
    def get_by_shop_id(cls, shop_id):
        session = DBSession()
        fee_list = session.query(cls).filter(cls.shop_id==shop_id).all()
        return fee_list

    @classmethod
    def create(cls, shop_id, fee_person, company_ratio, tour_guide_ratio,
               account_period, account_way, note=None):
        session = DBSession()
        fee = cls(
            shop_id=shop_id, fee_person=fee_person, company_ratio=company_ratio,
            tour_guide_ratio=tour_guide_ratio, account_period=account_period,
            account_way=account_way, note=note
        )
        session.add(fee)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_FEE_DUPLICATED))
        return fee

    @classmethod
    def update(cls, id, **kwargs):
        fee = cls.get_by_id(id)
        if not fee:
            raise_error_json(ClientError(errcode=CreoleErrCode.SHOP_FEE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(fee, k, v)
        session = DBSession()
        session.add(fee)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_FEE_DUPLICATED))

    @classmethod
    def delete(cls, id):
        fee = cls.get_by_id(id)
        if not fee:
            raise_error_json(ClientError(errcode=CreoleErrCode.SHOP_FEE_NOT_EXIST))
        session = DBSession()
        session.delete(fee)
        session.flush()

    @classmethod
    def delete_by_shop_id(cls, shop_id):
        fee_list = cls.get_by_shop_id(shop_id)
        session = DBSession()
        for fee in fee_list:
            session.delete(fee)
        session.flush()


class Shop(Base, BaseMixin):
    """购物店"""
    __tablename__ = 'shop'
    SHOP_TYPE = Enum(
        ('JEWELRY', 1, u'珠宝'),
        ('TEA', 2, u'红茶'),
        ('OTHER', 3, u'其他'),
    )

    country_id = Column(Integer, nullable=False, doc=u'国家名')
    city_id = Column(Integer, nullable=False, doc=u'城市名')
    address = Column(Unicode(100), nullable=False, doc=u'店铺地址')
    shop_type = Column(TINYINT, nullable=False, doc=u'购物类型')
    company_id = Column(Integer, nullable=True, doc=u'所属购物集团')
    name = Column(Unicode(40), unique=True, nullable=False, doc=u'中文店名')
    name_en = Column(String(60), unique=True, nullable=False, doc=u'英文店名')
    nickname_en = Column(String(20), nullable=False, doc=u'英文简称')

    intro_cn = Column(Unicode(500), doc=u'中文介绍')
    intro_en = Column(String(500), doc=u'英文介绍')
    note = Column(String(100), nullable=True, doc=u'备注')

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

    @validates('shop_type')
    def _validate_shop_type(self, key, shop_type):
        if shop_type not in self.SHOP_TYPE.values():
            raise_error_json(InvalidateError(args=('shop_type', shop_type,)))
        return shop_type

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
    def create(cls, name, name_en, nickname_en, address, country_id,
               city_id, company_id, shop_type, intro_cn='', intro_en='',
               note=None):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        shop = cls(
            name=name, name_en=name_en, address=address,
            nickname_en=nickname_en, country_id=country_id,
            city_id=city_id, company_id=company_id, shop_type=shop_type,
            intro_cn=intro_cn, intro_en=intro_en, note=note)
        session.add(shop)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_DUPLICATED))

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
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_DUPLICATED))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        shop = session.query(cls).filter(cls.id==id).first()
        if not shop:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_NOT_EXIST))
        session.delete(shop)
        session.flush()

    @classmethod
    def delete_by_company_id(cls, company_id):
        shop_list = cls.get_by_company_id(company_id)
        session = DBSession()
        for item in shop_list:
            session.delete(item)
        session.flush()


class ShopImage(Base, BaseMixin):
    """店铺对应的图片"""
    __tablename__ = 'shop_image'

    shop_id = Column(Integer, nullable=False, doc=u'店铺id')
    image_hash = Column(String(128), default=None)
