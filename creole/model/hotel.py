# coding: utf-8
from sqlalchemy import (
    Column,
    Unicode,
    String,
    Integer,
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
from .country import Country, City
from ..exc import (
    raise_error_json,
    CreoleErrCode,
    ClientError,
    InvalidateError,
)


class HotelCompany(Base, BaseMixin):
    __tablename__ = 'hotel_company'


class Hotel(Base, BaseMixin):
    __tablename__ = 'hotel'

    LEVEL = Enum(
        ('ONE', 1, u'一星'),
        ('TWO', 2, u'二星'),
        ('THREE', 3, u'三星'),
        ('FOUR', 4, u'四星'),
        ('FIVE', 5, u'五星'),
    )

    country_id = Column(Integer, nullable=False, doc=u'国家id')
    city_id = Column(Integer, nullable=False, doc=u'城市id')
    company_id = Column(Integer, nullable=False, doc=u'公司ID')
    address = Column(String(100), nullable=False, doc=u'餐厅地址')
    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')
    nickname_en = Column(String(20), unique=True, nullable=False, doc=u'英文名简称')
    star_level = Column(TINYINT, nullable=False, doc=u'酒店星级')
    comment_level = Column(TINYINT, nullable=False, doc=u'酒店网上评比星级')
    standard_room_number = Column(SMALLINT, nullable=False, doc=u'标间大床房数')
    standard_double_room_number = Column(SMALLINT, nullable=False, doc=u'标间双床房数')
    triple_room_number = Column(SMALLINT, nullable=False, doc=u'三人间数')
    suite_room_number = Column(SMALLINT, nullable=False, doc=u'套间数')
    tour_guide_room_number = Column(SMALLINT, nullable=False, doc=u'导游房数')
    start_year = Column(SMALLINT, nullable=False, doc=u'开业年份')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')
    email = Column(String(30), nullable=False, doc=u'邮箱')

    intro_cn = Column(Unicode(500), nullable=True, doc=u'中文介绍')
    intro_en = Column(String(800), nullable=True, doc=u'英文介绍')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_company_id', 'company_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('star_level')
    def _validate_star_level(self, key, star_level):
        if star_level not in self.LEVEL.values():
            raise_error_json(InvalidateError(args=('star_level', star_level,)))
        return star_level

    @validates('comment_level')
    def _validate_comment_level(self, key, comment_level):
        if comment_level not in self.LEVEL.values():
            raise_error_json(InvalidateError(args=('comment_level', comment_level,)))
        return comment_level

    @validates('country_id')
    def _validate_country_id(self, key, country_id):
        country = DBSession().query(Country).filter(
            Country.id==country_id).first()
        if not country:
            raise_error_json(InvalidateError(args=('country_id', country_id,)))
        return country_id

    @validates('company_id')
    def _validate_company_id(self, key, company_id):
        company = DBSession().query(HotelCompany).filter(
            HotelCompany.id==company_id).first()
        if not company:
            raise_error_json(InvalidateError(args=('company_id', company_id,)))
        return company_id

    @classmethod
    def _validate_country_and_city(cls, country_id, city_id):
        city = DBSession().query(City).filter(City.id==city_id).first()
        if not city:
            raise_error_json(ClientError(errcode=CreoleErrCode.CITY_NOT_EXIST))
        elif city.country_id != country_id:
            raise_error_json(InvalidateError(errcode=CreoleErrCode.COUNTRY_NOT_EXIST))

    @classmethod
    def create(cls, country_id, city_id, company_id, address, name,
               name_en, nickname_en, star_level, comment_level,
               standard_room_number, standard_double_room_number,
               triple_room_number, suite_room_number, tour_guide_room_number,
               start_year, telephone, email, intro_cn=None, intro_en=None):
        session = DBSession()
        hotel = cls(
            country_id=country_id, city_id=city_id, company_id=company_id,
            address=address, name=name, name_en=name_en, nickname_en=nickname_en,
            star_level=star_level, comment_level=comment_level,
            standard_room_number=standard_room_number,
            standard_double_room_number=standard_double_room_number,
            triple_room_number=triple_room_number,
            suite_room_number=suite_room_number,
            tour_guide_room_number=tour_guide_room_number,
            start_year=start_year, telephone=telephone, email=email,
            intro_cn=intro_cn, intro_en=intro_en
        )
        session.add(hotel)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_DUPLICATED))

    @classmethod
    def update(cls, id, **kwargs):
        hotel = cls.get_by_id(id)
        if not hotel:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_NOT_EXIST))
        if hotel.country_id != kwargs['country_id'] \
                or hotel.city_id != kwargs['city_id']:
            cls._validate_country_and_city(kwargs['country_id'], kwargs['city_id'])
        for k, v in kwargs.iteritems():
            setattr(hotel, k, v)
        session = DBSession()
        session.merge(hotel)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_DUPLICATED))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        hotel = session.query(cls).filter(cls.id==id).first()
        if not hotel:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_NOT_EXIST))
        session.delete(hotel)
        session.flush()

    @classmethod
    def get_by_company_id(cls, company_id):
        session = DBSession()
        return session.query(cls).filter(cls.company_id==company_id).all()
