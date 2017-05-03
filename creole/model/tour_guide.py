# coding: utf-8
import datetime

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
    SMALLINT,
)
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.exc import IntegrityError

from . import Base, DBSession
from .country import Country
from .mixins import BaseMixin, AccountMixin
from ..exc import (
    raise_error_json,
    InvalidateError,
    CreoleErrCode,
    ClientError,
)
from ..util import Enum


class TourGuide(Base, BaseMixin):
    """导游"""
    __tablename__ = 'tour_guide'

    GUIDE_TYPE = Enum(
        ('INTERNATIONAL', 1, u'国际导游'),
        ('DRIVER', 2, u'司机导游'),
        ('ATTRACTION', 3, u'景点导游'),
        ('TRANSLATOR', 4, u'翻译'),
        ('LEADER', 5, u'领队'),
    )
    GENDER = Enum(
        ('MALE', 1, u'男性'),
        ('FEMALE', 2, u'女性'),
    )
    LANGUAGE_LEVEL = Enum(
        ('EXCELLENT', 1, u'熟练'),
        ('VERY_GOOD', 2, u'优秀'),
        ('GOOD', 3, u'良好'),
        ('FAIR', 4, u'及格'),
        ('POOR', 5, u'差'),
    )
    PASSPORT_TYPE = Enum(
        ('TRAVEL', 1, u'旅游签证'),
        ('BUSINESS', 2, u'商务签证'),
        ('WORK', 3, u'工作签证'),
    )
    CERTIFICATE_TYPE = Enum(
        ('ID', 1, u'身份证'),
        ('PASSPORT', 2, u'护照'),
    )

    guide_type = Column(TINYINT, nullable=False, doc=u'导游类型')
    country_id = Column(Integer, nullable=False, doc=u'国家ID')
    name = Column(Unicode(10), nullable=True, doc=u'中文名称')
    name_en = Column(String(20), nullable=False, doc=u'英文名称')
    nickname_en = Column(String(10), nullable=True, doc=u'英文名简称')
    gender = Column(TINYINT, nullable=False, doc=u'性别')
    birthday = Column(SMALLINT, nullable=False, doc=u'出生年份')
    start_work = Column(SMALLINT, nullable=False, doc=u'开始工作的年份')
    first_language = Column(String(20), nullable=False, doc=u'第一语言')
    first_language_level = Column(TINYINT, nullable=False, doc=u'第一语言等级')
    second_language = Column(String(20), nullable=False, doc=u'第二语言')
    second_language_level = Column(TINYINT, nullable=False, doc=u'第二语言等级')
    third_language = Column(String(20), nullable=True, doc=u'第三语言')
    third_language_level = Column(TINYINT, nullable=True, doc=u'第三语言等级')
    certificate_type = Column(TINYINT, nullable=False, doc=u'证件类型')
    certificate_number = Column(String(20), nullable=False, doc=u'证件编号')
    tour_guide_number = Column(String(20), nullable=False, doc=u'导游证编号')
    passport_country = Column(String(30), nullable=False, doc=u'签证国别')
    passport_type = Column(TINYINT, nullable=False, doc=u'签证类型')
    passport_note = Column(String(128), nullable=True, doc=u'签证备注')
    telephone_one = Column(String(20), nullable=False, doc=u'电话')
    telephone_two = Column(String(20), nullable=True, doc=u'电话')
    email = Column(String(30), nullable=True, doc=u'邮箱')
    company_id = Column(Integer, nullable=False, doc=u'所属公司')
    intro = Column(String(256), nullable=True, doc=u'自我介绍')
    image_hash = Column(String(128), nullable=False, doc=u'护照/身份证照片')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_name_name_en', 'name', 'name_en'),
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
            Index('ix_country_id', 'country_id'),
            Index('ix_gender', 'gender'),
            Index('idx_country_id_gender', 'country_id', 'gender'),
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

    @validates('first_language_level')
    def _validate_first_language_level(self, key, first_language_level):
        if first_language_level not in self.LANGUAGE_LEVEL.values():
            raise_error_json(
                InvalidateError(args=('first_language_level', first_language_level)))
        return first_language_level

    @validates('second_language_level')
    def _validate_second_language_level(self, key, second_language_level):
        if second_language_level not in self.LANGUAGE_LEVEL.values():
            raise_error_json(
                InvalidateError(args=('second_language_level', second_language_level)))
        return second_language_level

    @validates('passport_type')
    def _validate_passport_type(self, key, passport_type):
        if passport_type not in self.PASSPORT_TYPE.values():
            raise_error_json(
                InvalidateError(args=('passport_type', passport_type)))
        return passport_type

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        tour_guide = session.query(cls).filter(cls.id==id).first()
        return tour_guide

    @classmethod
    def create(cls, guide_type, country_id, name, name_en, nickname_en,
               gender, birthday, start_work, first_language, first_language_level,
               second_language, second_language_level, certificate_type,
               certificate_number, tour_guide_number, passport_country,
               passport_type, passport_note, telephone_one, image_hash,
               company_id, third_language=None, third_language_level=None,
               email=None, intro=None, telephone_two=None):
        session = DBSession()
        tour_guide = cls(
            guide_type=guide_type, country_id=country_id, name=name,
            name_en=name_en, nickname_en=nickname_en, gender=gender,
            birthday=birthday, start_work=start_work, first_language=first_language,
            first_language_level=first_language_level, second_language=second_language,
            second_language_level=second_language_level, third_language=third_language,
            third_language_level=third_language_level, certificate_type=certificate_type,
            certificate_number=certificate_number, tour_guide_number=tour_guide_number,
            passport_country=passport_country, passport_type=passport_type,
            passport_note=passport_note, telephone_one=telephone_one,
            company_id=company_id, email=email, telephone_two=telephone_two,
            image_hash=image_hash, intro=intro)
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

    @classmethod
    def search(cls, country_id=None, gender=None,
               guide_type=None, page=1, number=20):
        session = DBSession()
        query = session.query(cls)
        total = None
        if country_id:
            query = query.filter(cls.country_id==country_id)
        if gender:
            query = query.filter(cls.gender==gender)
        if guide_type:
            query = query.filter(cls.guide_type==guide_type)
        if page == 1:
            total = query.count()
        tour_guide_list = \
            query.offset((page - 1) * number).limit(number).all()
        return tour_guide_list, total


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
    currency = Column(TINYINT, nullable=False, doc=u'货币类型')
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
    def delete(cls, id=None, tour_guide_id=None):
        if not (id or tour_guide_id):
            raise_error_json(InvalidateError())
        session = DBSession()
        if tour_guide_id:
            fee = session.query(cls).filter(cls.tour_guide_id==tour_guide_id).first()
        else:
            fee = session.query(cls).filter(cls.id==id).first()
        if not fee:
            return
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


class TourGuideAccount(Base, AccountMixin):
    __tablename__ = 'tour_guide_account'

    tour_guide_id = Column(Integer, nullable=False, doc=u'导游ID')

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

    @classmethod
    def get_by_tour_guide_id(cls, tour_guide_id):
        account = DBSession().query(cls).filter(
            cls.tour_guide_id==tour_guide_id).all()
        return account

    @classmethod
    def create(cls, tour_guide_id, currency, bank_name,
               deposit_bank, payee, account, swift_code=None, note=None):
        session = DBSession()
        account = cls(
            tour_guide_id=tour_guide_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, swift_code=swift_code, note=note)
        session.add(account)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_ACCOUNT_DUPLICATED))

    @classmethod
    def delete(cls, id=None, tour_guide_id=None):
        if not (id or tour_guide_id):
            raise_error_json(InvalidateError())
        session = DBSession()
        if tour_guide_id:
            account = session.query(cls).filter(cls.tour_guide_id==tour_guide_id).first()
        else:
            account = session.query(cls).filter(cls.id==id).first()
        if not account:
            return
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
