# coding: utf-8
import datetime

from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Index,
    Float,
    DateTime,
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.dialects.mysql import (
    TINYINT,
    SMALLINT,
)
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .country import Country
from .mixins import BaseMixin
from ..exc import (
    raise_error_json,
    InvalidateError,
    CreoleErrCode,
    DatabaseError,
    ClientError,
)
from ..util import Enum


class TourGuide(Base, BaseMixin):
    """导游"""
    __tablename__ = 'tour_guide'

    GUIDE_TYPE = Enum(
        ('INTERNATIONAL', 0, u'国际导游'),
        ('DRIVER', 1, u'司机导游'),
        ('ATTRACTION', 2, u'景点导游'),
        ('TRANSLATOR', 3, u'翻译'),
    )
    GENDER = Enum(
        ('MALE', 1, u'男性'),
        ('FEMALE', 2, u'女性'),
    )
    CERTIFICATE_TYPE = Enum(
        ('ID', 1, u'身份证'),
        ('PASSPORT', 2, u'护照'),
    )

    guide_type = Column(TINYINT, nullable=False, doc=u'导游类型')
    country_id = Column(Integer, nullable=False, doc=u'国家ID')
    name = Column(Unicode(10), nullable=True, doc=u'中文名称')
    name_en = Column(String(20), nullable=True, doc=u'英文名称')
    gender = Column(TINYINT, nullable=False, doc=u'性别')
    birthday = Column(DateTime, nullable=False, doc=u'生日')
    start_work = Column(SMALLINT, nullable=False, doc=u'开始工作的年份')
    language = Column(String(20), nullable=False, doc=u'语言')
    certificate_type = Column(TINYINT, nullable=False, doc=u'证件类型')
    certificate_number = Column(String(20), nullable=False, doc=u'证件编号')
    tour_guide_numer = Column(String(20), nullable=False, doc=u'导游证编号')
    passport_country = Column(String(30), nullable=True, doc=u'签证国别')
    telephone = Column(String(20), nullable=False, doc=u'电话')
    intro = Column(String(256), nullable=False, doc=u'自我介绍')
    image_hash = Column(String(128), nullable=False, doc=u'护照/身份证照片')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en'),
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = DBSession().query(Country).filter(
            Country.id==country_id).first()
        if not country:
            raise_error_json(InvalidateError(args=('country_id', country_id,)))
        return country_id

    @validates('guide_type')
    def _validate_guide_type(self, key, guide_type):
        if guide_type not in self.GUIDE_TYPE.values():
            raise_error_json(
                InvalidateError(args=('guide_type', guide_type)))
        return guide_type

    @validates('gender')
    def _validate_gender(self, key, gender):
        if gender not in self.GENDER.values():
            raise_error_json(
                InvalidateError(args=('gender', gender)))
        return gender

    @validates('certificate_type')
    def _validate_certificate_type(self, key, certificate_type):
        if certificate_type not in self.CERTIFICATE_TYPE.values():
            raise_error_json(
                InvalidateError(args=('certificate_type', certificate_type)))
        return certificate_type

    @validates('start_work')
    def _validate_start_work(self, key, start_work):
        if start_work < 1900 or start_work > datetime.datetime.now().year:
            raise_error_json(
                InvalidateError(args=('start_work', start_work)))
        return start_work

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        tour_guide = session.query(cls).filter(cls.id==id).first()
        return tour_guide

    @classmethod
    def create(cls, guide_type, country_id, name, name_en, gender, birthday,
               start_work, language, certificate_type, certificate_number,
               tour_guide_numer, passport_country, telephone, intro, image_hash):
        session = DBSession()
        tour_guide = cls(
            guide_type=guide_type, country_id=country_id, name=name,
            name_en=name_en, gender=gender, birthday=birthday,
            start_work=start_work, language=language,
            certificate_type=certificate_type, certificate_number=certificate_number,
            tour_guide_numer=tour_guide_numer, passport_country=passport_country,
            telephone=telephone, intro=intro, image_hash=image_hash)
        session.add(tour_guide)
        session.flush()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        tour_guide = session.query(cls).filter(cls.id==id).first()
        if not tour_guide:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_NOT_EXIST))
        session.delete(tour_guide)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        tour_guide = cls.get_by_id(id)
        if not tour_guide:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(tour_guide, k, v)
        session.merge(tour_guide)
        session.flush()



class TourGuideFee(Base,BaseMixin):
    __tablename__ = 'tour_guide_fee'

    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )
    SERVICE_TYPE = Enum(
        ('FIXED', 1, u'固定服务费'),
        ('COUNT', 2, u'人头费'),
    )

    tour_guide_id = Column(Integer, unique=True, nullable=False, doc=u'导游ID')
    currency = Column(TINYINT, nullable=False, doc=u'结算币种')
    base_fee = Column(Float(precision=3), nullable=False, doc=u'基本工资')
    service_type = Column(TINYINT, nullable=False, doc=u'服务类型')
    service_fee = Column(Float(precision=3), nullable=False, doc=u'服务费')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_tour_guide_id', 'tour_guide_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('currency')
    def _validate_currency(self, key, currency):
        if currency not in self.CURRENCY.values():
            raise_error_json(
                InvalidateError(args=('currency', currency,)))
        return currency

    @validates('service_type')
    def _validate_service_type(self, key, service_type):
        if service_type not in self.SERVICE_TYPE.values():
            raise_error_json(
                InvalidateError(args=('service_type', service_type,)))
        return service_type

    @validates('tour_guide_id')
    def _validate_tour_guide_id(self, key, tour_guide_id):
        tour_guide = DBSession().query(TourGuide).filter(
            TourGuide.id==tour_guide_id).first()
        if not tour_guide:
            raise_error_json(InvalidateError(args=('tour_guide_id', tour_guide_id,)))
        return tour_guide_id

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        fee = session.query(cls).filter(cls.id==id).first()
        return fee

    @classmethod
    def get_by_tour_guide_id(cls, tour_guide_id):
        fee = DBSession().query(cls).filter(
            cls.tour_guide_id==tour_guide_id).first()
        return fee

    @classmethod
    def create(cls, tour_guide_id, currency, base_fee,
               service_type, service_fee):
        session = DBSession()
        fee = cls(
            tour_guide_id=tour_guide_id, currency=currency,
            base_fee=base_fee, service_type=service_type,
            service_fee=service_fee)
        session.add(fee)
        session.flush()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        fee = session.query(cls).filter(cls.id==id).first()
        if not fee:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_FEE_NOT_EXIST))
        session.delete(fee)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        fee = cls.get_by_id(id)
        if not fee:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_FEE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(fee, k, v)
        session.merge(fee)
        session.flush()


class TourGuideAccount(Base, BaseMixin):
    __tablename__ = 'tour_guide_account'
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )

    tour_guide_id = Column(Integer, nullable=False, doc=u'导游ID')
    currency = Column(TINYINT, nullable=False, doc=u'结算币种')
    bank_name = Column(String(30), nullable=False, doc=u'银行名称')
    deposit_bank = Column(String(30), nullable=False, doc=u'开户行')
    payee = Column(String(20), nullable=False, doc=u'收款人')
    account = Column(String(20), unique=True, nullable=False, doc=u'账号')
    note = Column(String(40), nullable=False, doc=u'备注')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_tour_guide_id', 'tour_guide_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('tour_guide_id')
    def _validate_tour_guide_id(self, key, tour_guide_id):
        tour_guide = DBSession().query(TourGuide).filter(
            TourGuide.id==tour_guide_id).first()
        if not tour_guide:
            raise_error_json(InvalidateError(args=('tour_guide_id', tour_guide_id,)))
        return tour_guide_id

    @validates('currency')
    def _validate_currency(self, key, currency):
        if currency not in self.CURRENCY.values():
            raise_error_json(
                InvalidateError(args=('currency', currency,)))
        return currency

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        account = session.query(cls).filter(cls.id==id).first()
        return account

    @classmethod
    def get_by_tour_guide_id(cls, tour_guide_id):
        account = DBSession().query(cls).filter(
            cls.tour_guide_id==tour_guide_id).first()
        return account

    @classmethod
    def create(cls, tour_guide_id, currency, bank_name,
               deposit_bank, payee, account, note):
        session = DBSession()
        account = cls(
            tour_guide_id=tour_guide_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, note=note)
        session.add(account)
        session.flush()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        account = session.query(cls).filter(cls.id==id).first()
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_ACCOUNT_NOT_EXIST))
        session.delete(account)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        account = cls.get_by_id(id)
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_ACCOUNT_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(account, k, v)
        session.merge(account)
        session.flush()
