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

from ..util import Enum
from . import Base, DBSession
from .mixins import BaseMixin
from .country import Country, City
from .user import User
from ..exc import (
    raise_error_json,
    InvalidateError,
    CreoleErrCode,
    DatabaseError,
    ClientError,
)


class VehicleCompany(Base, BaseMixin):
    """车辆公司"""
    __tablename__ = 'vehicle_company'

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
        session = DBSession()
        company = session.query(cls).filter(cls.id==id).first()
        return company

    @classmethod
    def delete(cls, id):
        session = DBSession()
        company = session.query(cls).filter(cls.id==id).first()
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_NOT_EXIST))
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
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        company = cls.get_by_id(id)
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(company, k, v)
        try:
            session.merge(company)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


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
    note = Column(String(40), nullable=False, doc=u'备注')


class VehicleCompanyAccount(Base, AccountMixin):
    """车辆公司账单结算账号"""
    __tablename__ = 'vehicle_company_account'

    company_id = Column(Integer, nullable=False, doc=u'公司id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_company_id_account', 'company_id', 'account'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        company = VehicleCompany.get_by_id(company_id)
        if not company:
            raise_error_json(InvalidateError(args=('company_id', company_id)))
        return company_id

    @classmethod
    def create(cls, company_id, currency, bank_name,
               deposit_bank, payee, account, note=None):
        session = DBSession()
        account = cls(
            company_id=company_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, note=note)
        try:
            session.add(account)
            session.commit()
            return account.id
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def get_by_company_id(cls, company_id):
        return DBSession().query(cls).filter(cls.company_id==company_id).all()

    @classmethod
    def get_by_id(cls, id):
        return DBSession().query(cls).filter(cls.id==id).first()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        account = session.query(cls).filter(cls.id==id).first()
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST))
        session.delete(account)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        account = cls.get_by_id(id)
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(account, k, v)
        session = DBSession()
        try:
            session.merge(account)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class VehicleUserAccount(Base, AccountMixin):
    """车辆所有者账单结算账号, 仅在非公司车辆使用"""
    __tablename__ = 'vehicle_user_account'

    user_id = Column(Integer, nullable=False, doc=u'用户id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_user_id_account', 'user_id', 'account'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('user_id')
    def _validate_user_id(self, key, user_id):
        company = User.get_by_id(user_id)
        if not company:
            raise_error_json(InvalidateError(args=('user_id', user_id)))
        return user_id

    @classmethod
    def create(cls, user_id, currency, bank_name,
               deposit_bank, payee, account, note=None):
        session = DBSession()
        account = cls(
            user_id=user_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, note=note)
        try:
            session.add(account)
            session.commit()
            return account.id
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def get_by_user_id(cls, user_id):
        return DBSession().query(cls).filter(cls.user_id==user_id).all()

    @classmethod
    def get_by_id(cls, id):
        return DBSession().query(cls).filter(cls.id==id).first()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        account = session.query(cls).filter(cls.id==id).first()
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST))
        session.delete(account)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        account = cls.get_by_id(id)
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(account, k, v)
        session = DBSession()
        try:
            session.merge(account)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class Vehicle(Base, BaseMixin):
    """车辆"""
    __tablename__ = 'vehicle'

    # 由于循环引用, 从VehicleSearchApiParser中copy一份
    OPERATIONS = Enum(
        ('GREATER', 1, u'大于'),
        ('EQUAL', 2, u'等于'),
        ('LESS', 3, u'小于'),
    )

    TYPE = Enum(
        ('COMPANY', 1, u'公司账号'),
        ('PERSSON', 2, u'个人账号'),
    )

    account_id = Column(Integer, nullable=False, doc=u'结算账号Id')
    account_type = Column(TINYINT, nullable=False, default=TYPE.COMPANY, doc=u'账号类型')
    company_id = Column(Integer, nullable=True, doc=u'所属车辆公司')
    country_id = Column(Integer, nullable=False, doc=u'国家名')
    city_id = Column(Integer, nullable=False, doc=u'城市名')
    vehicle_type = Column(String(16), nullable=False, doc=u'车辆型号')
    seat = Column(TINYINT, nullable=False, doc=u'座位数')
    start_use = Column(String(4), nullable=False, doc=u'使用年限')
    license = Column(String(10), nullable=False, doc=u'车牌号')
    register_number = Column(String(20), nullable=False, doc=u'旅游局注册号')
    contact = Column(Unicode(16), nullable=False, doc=u'联系人')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')
    unit_price = Column(Float(precision=3), nullable=False, doc=u'每公里单价')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_country_id_city_id_company_id_vehicle_type_seat',
                  'country_id', 'city_id', 'company_id', 'vehicle_type', 'seat'),
            Index('ix_company_id', 'company_id'),
            Index('ix_country_id', 'country_id'),
            Index('ix_city_id', 'city_id'),
            Index('ix_vehicle_type', 'vehicle_type'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('account_type')
    def _validate_account_type(self, key, account_type):
        if account_type not in self.TYPE.values():
            raise_error_json(InvalidateError(args=('account_type', account_type)))
        return account_type

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        company = DBSession().query(VehicleCompany).filter(
            VehicleCompany.id==company_id).first()
        if not company:
            raise_error_json(InvalidateError(args=('company_id', company_id)))
        return company_id

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
    def get_by_id(cls, id):
        session = DBSession()
        vehicle = session.query(cls).filter(cls.id==id).first()
        return vehicle

    @classmethod
    def create(cls, account_id, account_type, company_id, country_id, city_id,
               vehicle_type, seat, start_use, license, register_number,
               contact, telephone, unit_price):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        vehicle = cls(
            company_id=company_id, country_id=country_id, city_id=city_id,
            vehicle_type=vehicle_type, seat=seat, start_use=start_use,
            license=license, register_number=register_number, contact=contact,
            telephone=telephone, unit_price=unit_price, account_type=account_type,
            account_id=account_id
        )
        session.add(vehicle)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update(cls, id, **kwargs):
        vehicle = cls.get_by_id(id)
        if not vehicle:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(vehicle, k, v)
        session = DBSession()
        try:
            session.merge(vehicle)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        vehicle = session.query(cls).filter(cls.id==id).first()
        if not vehicle:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_NOT_EXIST))
        session.delete(vehicle)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search(cls, country_id=None, city_id=None, company_id=None,
               vehicle_type=None, operation=None, seat=None, page=1, number=20):
        query = DBSession().query(cls)
        total = None
        if country_id:
            query = query.filter(cls.country_id==country_id)
        if city_id:
            query = query.filter(cls.city_id==city_id)
        if company_id:
            query = query.filter(cls.company_id==company_id)
        if vehicle_type:
            query = query.filter(cls.vehicle_type==vehicle_type)
        if operation and seat:
            if operation == cls.OPERATIONS.GREATER:
                query = query.filter(cls.seat>seat)
            elif operation == cls.OPERATIONS.EQUAL:
                query = query.filter(cls.seat==seat)
            elif operation == cls.OPERATIONS.LESS:
                query = query.filter(cls.seat<seat)
        if page == 1:
            total = query.count()
        vehicle_list = query.offset((page - 1) * number).limit(number).all()
        return vehicle_list, total


class VehicleImage(Base, BaseMixin):
    """车辆对应的图片"""
    __tablename__ = 'vehicle_image'

    vehicle_id = Column(Integer, nullable=False, doc=u'车辆id')
    image_hash = Column(String(128), default=None)
