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


class Meal(Base, BaseMixin):
    """套餐等级"""
    __tablename__ = 'meal'

    TYPE = Enum(
        ('STANDARD', 1, u'标准餐'),
        ('UPGRADE', 2, u'升级餐'),
        ('LUXURY', 3, u'豪华餐'),
    )

    restaurant_id = Column(Integer, nullable=False, doc=u'餐厅id')
    meal_type = Column(TINYINT, nullable=False, doc=u'套餐类型')
    adult_fee = Column(Float, nullable=False, doc=u'成人报价')
    adult_cost = Column(Float, nullable=False, doc=u'成人成本')
    child_fee = Column(Float, nullable=False, doc=u'儿童报价')
    child_cost = Column(Float, nullable=False, doc=u'儿童成本')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_restaurant_id', 'restaurant_id'),
            Index('idx_restaurant_id_meal_type', 'restaurant_id', 'meal_type'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('meal_type')
    def _validate_restaurant_type(self, key, meal_type):
        if meal_type not in self.TYPE.values():
            raise_error_json(InvalidateError(args=('meal_type', meal_type)))
        return meal_type

    @validates('restaurant_id')
    def _validate_restaurant_id(self, key, restaurant_id):
        restaurant = Restaurant.get_by_id(restaurant_id)
        if not restaurant:
            raise_error_json(InvalidateError(args=('restaurant_id', restaurant_id)))
        return restaurant_id

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        restaurant = session.query(cls).filter(cls.id==id).first()
        return restaurant

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        return DBSession().query(cls).filter(cls.restaurant_id==restaurant_id).all()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        meal = session.query(cls).filter(cls.id==id).first()
        if not meal:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_MEAL_TYPE_NOT_EXIST))
        session.delete(meal)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create(cls, restaurant_id, meal_type, adult_fee, adult_cost,
               child_fee, child_cost):
        session = DBSession()
        meal = cls(
            restaurant_id=restaurant_id, meal_type=meal_type,
            adult_fee=adult_fee, adult_cost=adult_cost,
            child_fee=child_fee, child_cost=child_cost)
        session.add(meal)
        session.flush()

    @classmethod
    def update(cls, id, adult_fee=None, adult_cost=None,
               child_fee=None, child_cost=None):
        _dict = dict()
        if adult_fee:
            _dict['adult_fee'] = adult_fee
        if adult_cost:
            _dict['adult_cost'] = adult_cost
        if child_fee:
            _dict['child_fee'] = child_fee
        if child_cost:
            _dict['child_cost'] = child_cost
        DBSession().query(cls).filter(
            cls.id == id
        ).update(_dict, synchronize_session=False)


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

    @classmethod
    def search(cls, name=None, name_en=None):
        session = DBSession()
        restaurant_company = None
        query = session.query(cls)
        if name:
            restaurant_company = query.filter(cls.name==name).first()
        elif name_en:
            restaurant_company = query.filter(cls.name_en==name_en).first()
        return restaurant_company


class Restaurant(Base, BaseMixin):
    __tablename__ = 'restaurant'

    TYPE = Enum(
        ('CHINESE', 1, u'中餐'),
        ('WESTERN', 2, u'西餐'),
        ('SPECIAL', 3, u'特色'),
        ('GENERAL', 4, u'综合'),
    )

    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )

    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')
    restaurant_type = Column(TINYINT, nullable=False, doc=u'餐厅类型')
    country_id = Column(Integer, nullable=False, doc=u'国家id')
    city_id = Column(Integer, nullable=False, doc=u'城市id')
    company_id = Column(Integer, nullable=False, doc=u'公司id')
    address = Column(String(80), nullable=False, doc=u'餐厅地址')
    contact = Column(Unicode(16), nullable=False, doc=u'联系人')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')
    intro_cn = Column(Unicode(128), nullable=True, doc=u'中文介绍')
    intro_en = Column(String(128), nullable=True, doc=u'英文介绍')

    # 收款
    currency = Column(TINYINT, nullable=False, doc=u'结算币种')
    bank_name = Column(String(30), nullable=False, doc=u'银行名称')
    deposit_bank = Column(String(30), nullable=False, doc=u'开户行')
    payee = Column(String(20), nullable=False, doc=u'收款人')
    account = Column(String(20), unique=True, nullable=False, doc=u'账号')
    note = Column(String(40), nullable=False, doc=u'备注')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
            Index('ix_company_id', 'company_id'),
            Index('ix_country_id', 'country_id'),
            Index('ix_city_id', 'city_id'),
            Index('idx_city_id_company_id', 'city_id', 'company_id'),
            Index('idx_country_id_company_id', 'country_id', 'company_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = DBSession().query(Country).filter(
            Country.id==country_id).first()
        if not country:
            raise_error_json(InvalidateError(args=('country_id', country_id,)))
        return country_id

    @validates('restaurant_type')
    def _validate_restaurant_type(self, key, restaurant_type):
        if restaurant_type not in self.TYPE.values():
            raise_error_json(InvalidateError(args=('restaurant_type', restaurant_type)))
        return restaurant_type

    @validates('currency')
    def _validate_currency(self, key, currency):
        if currency not in self.CURRENCY.values():
            raise_error_json(InvalidateError(args=('currency', currency)))
        return currency

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        company = RestaurantCompany.get_by_id(company_id)
        if not company:
            raise_error_json(InvalidateError(args=('company_id', company_id)))
        return company_id

    @classmethod
    def _validate_country_and_city(cls, country_id, city_id):
        city = DBSession().query(City).filter(City.id==city_id).first()
        if not city:
            raise_error_json(ClientError(errcode=CreoleErrCode.CITY_NOT_EXIST))
        elif city.country_id != country_id:
            raise_error_json(InvalidateError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        restaurant = session.query(cls).filter(cls.id==id).first()
        return restaurant

    @classmethod
    def get_by_company_id(cls, company_id):
        session = DBSession()
        restaurant_list = session.query(cls).filter(
            cls.company_id==company_id).all()
        return restaurant_list

    @classmethod
    def delete(cls, id):
        session = DBSession()
        restaurant = session.query(cls).filter(cls.id==id).first()
        if not restaurant:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_NOT_EXIST))
        session.delete(restaurant)
        session.flush()

    @classmethod
    def create(cls, name, name_en, restaurant_type,
               country_id, city_id, company_id, address,
               contact, telephone, currency, bank_name,
               deposit_bank, payee, account, note=None,
               intro_cn=None, intro_en=None):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        restaurant = cls(
            name=name, name_en=name_en, restaurant_type=restaurant_type,
            country_id=country_id, city_id=city_id, company_id=company_id,
            address=address, contact=contact, telephone=telephone,
            currency=currency, bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, note=note,
            intro_cn=intro_cn, intro_en=intro_en
        )
        try:
            session.add(restaurant)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        restaurant = cls.get_by_id(id)
        if not restaurant:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_NOT_EXIST))
        if restaurant.country_id != kwargs['country_id'] \
                or restaurant.city_id != kwargs['city_id']:
            cls._validate_country_and_city(kwargs['country_id'], kwargs['city_id'])
        for k, v in kwargs.iteritems():
            setattr(restaurant, k, v)
        session = DBSession()
        try:
            session.merge(restaurant)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search(cls, country_id=None, city_id=None,
               company_id=None, page=1, number=20):
        session = DBSession()
        query = session.query(cls)
        total = None
        if city_id:
            query = query.filter(cls.city_id==city_id)
        elif country_id:
            query = query.filter(cls.country_id==country_id)
        if company_id:
            query = query.filter(cls.company_id==company_id)
        if page == 1:
            total = query.count()
        shop_list = query.offset((page - 1) * number).limit(number).all()
        return shop_list, total
