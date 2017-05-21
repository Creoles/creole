# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Index,
    String,
)
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.mysql import (
    TINYINT,
)

from . import DBSession
from .base import BaseMixin
from .country import Country, City
from ..util import Enum
from ..exc import (
    raise_error_json,
    CreoleErrCode,
    ClientError,
    InvalidateError,
)


class AccountMixin(BaseMixin):
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )

    currency = Column(TINYINT, nullable=False, doc=u'结算币种')
    bank_name = Column(String(30), nullable=False, doc=u'银行名称')
    deposit_bank = Column(String(30), nullable=False, doc=u'开户行')
    payee = Column(String(20), nullable=False, doc=u'收款人')
    account = Column(String(20), unique=True, nullable=False, doc=u'账号')
    swift_code = Column(String(20), nullable=True, doc=u'国际电汇码')
    note = Column(String(40), nullable=False, doc=u'备注')

    @validates('currency')
    def _validate_currency(self, key, currency):
        if currency not in self.CURRENCY.values():
            raise_error_json(
                InvalidateError(args=('currency', currency,)))
        return currency


class ContactMixin(BaseMixin):
    contact = Column(Unicode(16), nullable=False, doc=u'联系人')
    position = Column(String(30), nullable=False, doc=u'职位')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')
    email = Column(String(30), nullable=False, doc=u'邮箱')

    @classmethod
    def update(cls, id, **kwargs):
        person = cls.get_by_id(id)
        if not person:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.CONTACT_PERSON_NOT_EXIST))
        session = DBSession()
        for k, v in kwargs.iteritems():
            setattr(person, k, v)
        session.merge(person)
        session.flush()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        person = session.query(cls).filter(cls.id==id).first()
        if not person:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.CONTACT_PERSON_NOT_EXIST))
        session.delete(person)
        session.flush()


class CompanyMixin(BaseMixin):
    country_id = Column(Integer, nullable=False, doc=u'国家名')
    city_id = Column(Integer, nullable=False, doc=u'城市名')
    name = Column(Unicode(40), unique=True, nullable=False, doc=u'中文集团名')
    name_en = Column(String(60), unique=True, nullable=False, doc=u'英文集团名')
    nickname_en = Column(String(30), unique=True, nullable=False, doc=u'英文简称')
    register_number = Column(String(30), nullable=False, doc=u'公司注册编号')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en', unique=True),
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
            Index('idx_country_id_city_id', 'country_id', 'city_id'),
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
