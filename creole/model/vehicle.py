# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
    Float,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy.orm import validates

from . import Base, DBSession
from .mixins import BaseMixin
from .country import Country, City
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

    name = Column(Unicode(40), nullable=False, doc=u'中文集团名')
    name_en = Column(String(60), nullable=False, doc=u'英文集团名')

    @validates('name')
    def _validate_name(self, key, name):
        company = DBSession().query(VehicleCompany).filter(
            VehicleCompany.name==name,
            VehicleCompany.is_delete==VehicleCompany.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))
        return name

    @validates('name_en')
    def _validate_name_en(self, key, name_en):
        company = DBSession().query(VehicleCompany).filter(
            VehicleCompany.name_en==name_en,
            VehicleCompany.is_delete==VehicleCompany.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))
        return name_en

    @classmethod
    def delete(cls, id):
        DBSession().query(cls).filter(
            cls.id==id
        ).update(
            {'is_delete': cls.FIELD_STATUS.FIELD_STATUS_DELETED},
            synchronize_session=False)

    @classmethod
    def create(cls, name, name_en):
        session = DBSession()
        company = cls(name=name, name_en=name_en)
        session.add(company)
        try:
            session.commit()
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
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class Vehicle(Base, BaseMixin):
    """车辆"""
    __tablename__ = 'vehicle'

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

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        company = DBSession().query(VehicleCompany).filter(
            VehicleCompany.id==country_id,
            VehicleCompany.is_delete==VehicleCompany.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if not company:
            raise_error_json(InvalidateError(args=(country_id,)))
        return country_id

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = DBSession().query(Country).filter(
            Country.id==country_id,
            Country.is_delete==Country.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if not country:
            raise_error_json(InvalidateError(args=(country_id,)))
        return country_id

    @classmethod
    def _validate_country_and_city(cls, country_id, city_id):
        city = DBSession().query(City).filter(
            City.id==city_id,
            City.is_delete==City.FIELD_STATUS.FIELD_STATUS_NO_DELETE 
        ).first()
        if not city:
            raise_error_json(ClientError(errcode=CreoleErrCode.CITY_NOT_EXIST))
        elif city.country_id != country_id:
            raise_error_json(InvalidateError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        vehicle = session.query(cls).filter(
            cls.id==id,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return vehicle

    @classmethod
    def search(cls):
        pass

    @classmethod
    def create(cls, company_id, country_id, city_id, vehicle_type,
               seat, start_use, license, register_number, contact,
               telephone, unit_price):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        vehicle = cls(
            company_id=company_id, country_id=country_id, city_id=city_id,
            vehicle_type=vehicle_type, seat=seat, start_use=start_use,
            license=license, register_number=register_number, contact=contact,
            telephone=telephone, unit_price=unit_price
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
            raise_error_json(ClientError(errcode=CreoleErrCode.VEHICLE_NOT_EXIST))
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
        DBSession().query(cls).filter(
            cls.id==id
        ).update(
            {'is_delete': cls.FIELD_STATUS.FIELD_STATUS_DELETED},
            synchronize_session=False)


class VehicleImage(Base, BaseMixin):
    """车辆对应的图片"""
    __tablename__ = 'vehicle_image'

    vehicle_id = Column(Integer, nullable=False, doc=u'车辆id')
    image_hash = Column(String(128), default=None)
