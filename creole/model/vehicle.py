# coding: utf-8
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    Float,
    Index,
)
from sqlalchemy.dialects.mysql import (
    TINYINT,
    SMALLINT,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from ..util import Enum
from . import Base, DBSession
from .base import BaseMixin
from .mixins import AccountMixin, ContactMixin, CompanyMixin
from .country import Country, City
from ..exc import (
    raise_error_json,
    InvalidateError,
    CreoleErrCode,
    ClientError,
)


class VehicleCompany(Base, CompanyMixin):
    """车辆公司"""
    __tablename__ = 'vehicle_company'
    COMPANY_TYPE = Enum(
        ('COMPANY', 1, u'公司'),
        ('PERSON', 2, u'个人'),
    )

    company_type = Column(TINYINT, nullable=False, doc=u'公司类型')
    vehicle_number = Column(SMALLINT, nullable=False, doc=u'车辆数量')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_company_type', 'company_type'),
            Index('idx_country_id_city_id_company_type',
                  'country_id', 'city_id', 'company_type')
        )
        return table_args + CompanyMixin.__table_args__

    @validates('company_type')
    def _validate_company_type(self, key, company_type):
        if company_type not in self.COMPANY_TYPE.values():
            raise_error_json(InvalidateError(args=('company_type', company_type,)))
        return company_type

    @classmethod
    def delete(cls, id):
        session = DBSession()
        company = session.query(cls).filter(cls.id==id).first()
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_NOT_EXIST))
        session.delete(company)
        session.flush()

    @classmethod
    def create(cls, company_type, country_id, city_id, name, name_en,
               nickname_en, vehicle_number, register_number):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        company = cls(
            company_type=company_type, country_id=country_id,
            city_id=city_id, name=name, name_en=name_en,
            nickname_en=nickname_en, vehicle_number=vehicle_number,
            register_number=register_number
        )
        session.add(company)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        company = cls.get_by_id(id)
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(company, k, v)
        session.merge(company)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))

    @classmethod
    def search(cls, name=None, name_en=None, country_id=None,
               city_id=None, company_type=None, number=20, page=1):
        session = DBSession()
        query = session.query(cls)
        total = None
        if name:
            company_list = query.filter(cls.name==name).all()
        elif name_en:
            company_list = query.filter(cls.name_en==name_en).all()
        else:
            if city_id:
                query = query.filter(cls.city_id==city_id)
            elif country_id:
                query = query.filter(cls.country_id==country_id)
            if company_type:
                query = query.filter(cls.company_type==company_type)
            if page == 1:
                total = query.count()
            company_list = query.offset((page - 1) * number).limit(number).all()
        return company_list, total


class VehicleContact(Base, ContactMixin):
    __tablename__ = 'vehicle_contact'

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


class VehicleAccount(Base, AccountMixin):
    """车辆公司账单结算账号"""
    __tablename__ = 'vehicle_company_account'

    company_id = Column(Integer, nullable=False, doc=u'所属公司id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_company_id', 'company_id'),
        )
        return table_args + AccountMixin.__table_args__

    @classmethod
    def create(cls, company_id, currency, bank_name,
               deposit_bank, payee, account,
               swift_code=None, note=None):
        session = DBSession()
        account = cls(
            company_id=company_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, swift_code=swift_code,
            note=note)
        session.add(account)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_DUPLICATED))
        return account

    @classmethod
    def get_by_company_id(cls, company_id):
        return DBSession().query(cls).\
            filter(cls.company_id==company_id).all()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        account = session.query(cls).filter(cls.id==id).first()
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST))
        session.delete(account)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        account = cls.get_by_id(id)
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(account, k, v)
        session = DBSession()
        session.merge(account)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_ACCOUNT_DUPLICATED))


class VehicleType(Base, BaseMixin):
    """车型信息"""
    __tablename__ = 'vehicle_type'

    VEHICLE_TYPE = Enum(
        ('CAR', 1, u'轿车'),
        ('VAN', 2, u'货车'),
        ('BIG_VAN', 3, u'大货车'),
        ('MINI_COATCH', 4, u'迷你大巴'),
        ('COATCH', 5, u'大巴'),
        ('LONG_COATCH', 6, u'加长大巴'),
        ('OTHER', 7, u'其他'),
    )

    vehicle_type = Column(TINYINT, nullable=False, doc=u'车辆型号')
    brand = Column(String(20), nullable=False, doc=u'车辆品牌')
    seat = Column(TINYINT, nullable=False, doc=u'理论座位数')
    available_seat = Column(TINYINT, nullable=False, doc=u'实际可用座位数')
    passenger_count = Column(TINYINT, nullable=False, doc=u'建议乘客人数')
    note = Column(String(100), nullable=True, doc=u'备注')

    @validates('vehicle_type')
    def _validate_vehicle_type(self, key, vehicle_type):
        if vehicle_type not in self.VEHICLE_TYPE.values():
            raise_error_json(InvalidateError(args=('vehicle_type', vehicle_type)))
        return vehicle_type

    @classmethod
    def delete(cls, id):
        session = DBSession()
        vehicle_type = session.query(cls).filter(cls.id==id).first()
        if not vehicle_type:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_TYPE_NOT_EXIST))
        session.delete(vehicle_type)
        session.flush()

    @classmethod
    def create(cls, vehicle_type, brand, seat, available_seat,
               passenger_count, note=None):
        session = DBSession()
        type = cls(
            vehicle_type=vehicle_type, brand=brand,
            seat=seat, available_seat=available_seat,
            passenger_count=passenger_count, note=note
        )
        session.add(type)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        type = cls.get_by_id(id)
        if not type:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_TYPE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(type, k, v)
        session = DBSession()
        session.merge(type)
        session.flush()

    @classmethod
    def search(cls, vehicle_type=None, number=20, page=1):
        total = None
        session = DBSession()
        query = session.query(cls)
        if vehicle_type:
            query = query.filter(cls.vehicle_type==vehicle_type)
        if page == 1:
            total = query.count()
        type_list = query.offset((page - 1) * number).limit(number).all()
        return type_list, total


class Vehicle(Base, BaseMixin):
    """车辆"""
    __tablename__ = 'vehicle'

    country_id = Column(Integer, nullable=False, doc=u'国家名')
    city_id = Column(Integer, nullable=False, doc=u'城市名')
    company_id = Column(Integer, nullable=False, doc=u'所属车辆公司')
    license = Column(String(10), unique=True, nullable=False, doc=u'车牌号')
    insurance_number = Column(String(30), nullable=False, doc=u'车辆保险号')
    start_use = Column(String(4), nullable=False, doc=u'使用年限')
    register_number = Column(String(20), nullable=False, doc=u'旅游局注册号')

    # 车型信息
    vehicle_type_id = Column(Integer, nullable=False, doc=u'车型id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('idx_country_id_city_id_company_id_vehicle_type_id',
                  'country_id', 'city_id', 'company_id', 'vehicle_type_id'),
            Index('ix_company_id', 'company_id'),
            Index('ix_country_id', 'country_id'),
            Index('ix_city_id', 'city_id'),
            Index('ix_vehicle_type_id', 'vehicle_type_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        company = DBSession().query(VehicleCompany).filter(
            VehicleCompany.id==company_id).first()
        if not company:
            raise_error_json(InvalidateError(args=('company_id', company_id)))
        return company_id

    @validates('vehicle_type_id')
    def _validate_vehicle_type_id(self, key, vehicle_type_id):
        company = DBSession().query(VehicleType).filter(
            VehicleType.id==vehicle_type_id).first()
        if not company:
            raise_error_json(InvalidateError(args=('vehicle_type_id', vehicle_type_id)))
        return vehicle_type_id

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
    def get_by_company_id(cls, company_id):
        session = DBSession()
        vehicle_list = session.query(cls).filter(
            cls.company_id==company_id).all()
        return vehicle_list

    @classmethod
    def create(cls, company_id, country_id, city_id, vehicle_type_id,
               start_use, license, register_number, insurance_number):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        vehicle = cls(
            company_id=company_id, country_id=country_id, city_id=city_id,
            vehicle_type_id=vehicle_type_id, start_use=start_use,
            license=license, register_number=register_number,
            insurance_number=insurance_number,
        )
        session.add(vehicle)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_LICENSE_DUPLICATED))

    @classmethod
    def update(cls, id, **kwargs):
        vehicle = cls.get_by_id(id)
        if not vehicle:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_NOT_EXIST))
        if vehicle.country_id != kwargs['country_id'] \
                or vehicle.city_id != kwargs['city_id']:
            cls._validate_country_and_city(kwargs['country_id'], kwargs['city_id'])
        for k, v in kwargs.iteritems():
            setattr(vehicle, k, v)
        session = DBSession()
        session.merge(vehicle)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_LICENSE_DUPLICATED))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        vehicle = session.query(cls).filter(cls.id==id).first()
        if not vehicle:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.SHOP_NOT_EXIST))
        session.delete(vehicle)
        session.flush()

    @classmethod
    def search(cls, country_id=None, city_id=None, company_id=None,
               vehicle_type_id=None, license=None, page=1, number=20):
        query = DBSession().query(cls)
        total = None
        if license:
            vehicle_list = query.filter(cls.license==license).all()
        else:
            if city_id:
                query = query.filter(cls.city_id==city_id)
            elif country_id:
                query = query.filter(cls.country_id==country_id)
            if company_id:
                query = query.filter(cls.company_id==company_id)
            if vehicle_type_id:
                query = query.filter(cls.vehicle_type_id==vehicle_type_id)
            if page == 1:
                total = query.count()
            vehicle_list = query.offset((page - 1) * number).limit(number).all()
        return vehicle_list, total


class VehicleFee(Base, BaseMixin):
    __tablename__ = 'vehicle_fee'

    vehicle_type_id = Column(Integer, nullable=False, doc=u'车型ID')
    company_id = Column(Integer, nullable=False, doc=u'公司ID')
    unit_price = Column(Float(3), nullable=False, doc=u'每公里价格')
    start_time = Column(DateTime, nullable=False, doc=u'开始时间')
    end_time = Column(DateTime, nullable=False, doc=u'结束时间')
    confirm_person = Column(String(30), nullable=True, doc=u'确认人')
    attachment_hash = Column(String(128), nullable=False, doc=u'合同附件')

    @classmethod
    def get_by_company_id(cls, company_id):
        session = DBSession()
        return session.query(cls).filter(cls.company_id==company_id).all()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        fee = session.query(cls).filter(cls.id==id).first()
        if not fee:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_FEE_NOT_EXIST))
        session.delete(fee)
        session.flush()

    @classmethod
    def create(cls, vehicle_type_id, company_id, unit_price, start_time,
               end_time, confirm_person, attachment_hash):
        session = DBSession()
        fee = cls(
            vehicle_type_id=vehicle_type_id, company_id=company_id,
            unit_price=unit_price, start_time=start_time,
            end_time=end_time, confirm_person=confirm_person,
            attachment_hash=attachment_hash
        )
        session.add(fee)
        session.flush()
        return fee

    @classmethod
    def update(cls, id, **kwargs):
        type = cls.get_by_id(id)
        if not type:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_FEE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(type, k, v)
        session = DBSession()
        session.merge(type)
        session.flush()

    @classmethod
    def search(cls, vehicle_type_id=None, company_id=None, unit_price=None,
               start_time=None, end_time=None, confirm_person=None,
               number=20, page=1):
        session = DBSession()
        total = None
        query = session.query(cls)
        if vehicle_type_id:
            query = query.filter(cls.vehicle_type_id==vehicle_type_id)
        if company_id:
            query = query.filter(cls.company_id==company_id)
        if unit_price:
            query = query.filter(cls.unit_price==unit_price)
        if start_time:
            query = query.filter(cls.start_time>=start_time)
        if end_time:
            query = query.filter(cls.end_time<=end_time)
        if confirm_person:
            query = query.filter(cls.confirm_person==confirm_person)
        if page == 1:
            total = query.count()
        fee_list = query.offset((page - 1) * number).limit(number).all()
        return fee_list, total


class VehicleImage(Base, BaseMixin):
    """车辆对应的图片"""
    __tablename__ = 'vehicle_image'

    vehicle_id = Column(Integer, nullable=False, doc=u'车辆id')
    image_hash = Column(String(128), default=None)
