# coding: utf-8
from sqlalchemy import (
    Column,
    DateTime,
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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from ..util import Enum
from . import Base, DBSession
from .base import BaseMixin
from .mixins import CompanyMixin, ContactMixin, AccountMixin
from .country import Country, City
from ..exc import (
    raise_error_json,
    CreoleErrCode,
    ClientError,
    InvalidateError,
)


class HotelCompany(Base, CompanyMixin):
    __tablename__ = 'hotel_company'

    intro = Column(String(200), doc=u'公司介绍')
    note = Column(String(200), doc=u'备注')

    @classmethod
    def create(cls, country_id, city_id, name, name_en,
               nickname_en, register_number, intro=None, note=None):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        company = cls(
            country_id=country_id, city_id=city_id,
            name=name, name_en=name_en, nickname_en=nickname_en,
            register_number=register_number,
            intro=intro, note=note
        )
        session.add(company)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_COMPANY_DUPLICATED))

    @classmethod
    def update(cls, id, **kwargs):
        session = DBSession()
        company = cls.get_by_id(id)
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_COMPANY_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(company, k, v)
        session.merge(company)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_COMPANY_DUPLICATED))

    @classmethod
    def delete(cls, id):
        session = DBSession()
        company = cls.get_by_id(id)
        if not company:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_COMPANY_NOT_EXIST))
        session.delete(company)
        session.flush()

    @classmethod
    def search(cls, country_id=None, city_id=None, page=1, number=20):
        session = DBSession()
        query = session.query(cls)
        total = None
        if city_id:
            query = query.filter(cls.city_id==city_id)
        elif country_id:
            query = query.filter(cls.country_id==country_id)
        if page == 1:
            total = query.count()
        company_list = query.offset((page - 1) * number).limit(number).all()
        return company_list, total


class HotelCompanyContact(Base, ContactMixin):
    __tablename__ = 'hotel_company_contact'

    company_id = Column(Integer, nullable=False, doc=u'公司ID')

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
        session = DBSession()
        company_list = cls.get_by_company_id(company_id)
        for company in company_list:
            session.delete(company)
        session.flush()


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
    telephone = Column(String(20), nullable=False, doc=u'预定电话')
    email = Column(String(30), nullable=False, doc=u'预定邮箱')

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
    def delete_by_company_id(cls, company_id):
        session = DBSession()
        hotel_list = cls.get_by_company_id(company_id)
        for hotel in hotel_list:
            session.delete(hotel)
        session.flush()

    @classmethod
    def get_by_company_id(cls, company_id):
        session = DBSession()
        return session.query(cls).filter(cls.company_id==company_id).all()

    @classmethod
    def search(cls, country_id=None, city_id=None, company_id=None,
               name=None, name_en=None, nickname_en=None,
               star_level=None, page=1, number=20):
        session = DBSession()
        query = session.query(cls)
        total = None
        if city_id:
            query = query.filter(cls.city_id==city_id)
        elif country_id:
            query = query.filter(cls.country_id==country_id)
        if name:
            query = query.filter(cls.name==name)
        elif name_en:
            query = query.filter(cls.name_en==name_en)
        elif nickname_en:
            query = query.filter(cls.nickname_en==nickname_en)
        if star_level:
            query = query.filter(cls.star_level==star_level)
        if page == 1:
            total = query.count()
        hotel_list = query.offset((page - 1) * number).limit(number).all()
        return hotel_list, total


class HotelAccount(Base, AccountMixin):
    __tablename__ = 'hotel_account'

    hotel_id = Column(Integer, nullable=False, doc=u'所属酒店id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_hotel_id', 'hotel_id'),
        )
        return table_args + AccountMixin.__table_args__

    @classmethod
    def create(cls, hotel_id, currency, bank_name,
               deposit_bank, payee, account,
               swift_code=None, note=None):
        session = DBSession()
        account = cls(
            hotel_id=hotel_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, swift_code=swift_code,
            note=note)
        session.add(account)
        try:
            session.flush()
            return account
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_ACCOUNT_DUPLICATED))

    @classmethod
    def get_by_hotel_id(cls, hotel_id):
        return DBSession().query(cls).\
            filter(cls.hotel_id==hotel_id).all()

    @classmethod
    def delete(cls, id):
        session = DBSession()
        account = session.query(cls).filter(cls.id==id).first()
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_ACCOUNT_NOT_EXIST))
        session.delete(account)
        session.flush()

    @classmethod
    def delete_by_hotel_id(cls, hotel_id):
        session = DBSession()
        account_list = cls.get_by_hotel_id(hotel_id)
        for account in account_list:
            session.delete(account)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        account = cls.get_by_id(id)
        if not account:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_ACCOUNT_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(account, k, v)
        session = DBSession()
        session.merge(account)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_ACCOUNT_DUPLICATED))


class HotelContact(Base, ContactMixin):
    __tablename__ = 'hotel_contact'

    hotel_id= Column(Integer, nullable=False, doc=u'酒店ID')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_hotel_id', 'hotel_id'),
        )
        return table_args + ContactMixin.__table_args__

    @classmethod
    def get_by_hotel_id(cls, hotel_id):
        session = DBSession()
        return session.query(cls).filter(cls.hotel_id==hotel_id).all()

    @classmethod
    def create(cls, contact, position, telephone, email, hotel_id):
        session = DBSession()
        person = cls(
            contact=contact, position=position,
            telephone=telephone, email=email,
            hotel_id=hotel_id
        )
        session.add(person)
        session.flush()
        return person

    @classmethod
    def delete_by_hotel_id(cls, hotel_id):
        session = DBSession()
        hotel_list = cls.get_by_hotel_id(hotel_id)
        for hotel in hotel_list:
            session.delete(hotel)
        session.flush()


class HotelFee(Base, BaseMixin):
    __tablename__ = 'hotel_fee'

    FREE_TYPE = Enum(
        ('PEOPLE', 1, u'按客户数'),
        ('ROOM', 2, u'按房间数'),
    )

    hotel_id = Column(Integer, nullable=False, doc=u'酒店ID')
    free_policy = Column(TINYINT, nullable=True, doc=u'免房费政策')
    free = Column(Integer, nullable=True, doc=u'多少免一')
    note = Column(String(100), nullable=True)
    confirm_person = Column(String(30), nullable=False, doc=u'确认人')
    attachment_hash = Column(String(128), nullable=True, doc=u'附件哈希值')

    @validates('free_policy')
    def _validate_free_policy(self, key, free_policy):
        if free_policy not in self.FREE_TYPE.values():
            raise_error_json(InvalidateError(args=('free_policy', free_policy,)))
        return free_policy

    @classmethod
    def get_by_hotel_id(cls, hotel_id):
        session = DBSession()
        fee = session.query(cls).filter(cls.hotel_id==hotel_id).first()
        return fee

    @classmethod
    def create(cls, hotel_id, confirm_person, free_policy=None,
               free=None, note=None, attachment_hash=None):
        session = DBSession()
        price = cls(
            hotel_id=hotel_id, confirm_person=confirm_person,
            free_policy=free_policy, free=free, note=note,
            attachment_hash=attachment_hash
        )
        session.add(price)
        session.flush()
        return price.id

    @classmethod
    def update(cls, id, **kwargs):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_FEE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(price, k, v)
        session = DBSession()
        session.merge(price)
        session.flush()

    @classmethod
    def delete(cls, id):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.HOTEL_FEE_NOT_EXIST))
        session = DBSession()
        session.delete(price)
        session.flush()

    @classmethod
    def delete_by_hotel_id(cls, hotel_id):
        session = DBSession()
        price = cls.get_by_hotel_id(hotel_id)
        if price:
            session.delete(price)
        session.flush()


class RoomPrice(Base, BaseMixin):
    __tablename__ = 'room_price'

    ROOM_TYPE = Enum(
        ('SINGLE', 1, u'单人间'),
        ('DOUBLE', 2, u'双人间'),
        ('TRIPLE', 3, u'三人间'),
        ('SUITE', 4, u'套间'),
        ('TOUR_GUIDE', 5, u'导游房'),
    )

    hotel_fee_id = Column(Integer, nullable=False, doc=u'费用ID')
    room_type = Column(TINYINT, nullable=False, doc=u'房型')
    start_time = Column(DateTime, nullable=False, doc=u'开始时间')
    end_time = Column(DateTime, nullable=False, doc=u'结束时间')
    price = Column(Float(3), nullable=False, doc=u'房价')
    note = Column(String(100), nullable=True)

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_hotel_fee_id', 'hotel_fee_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('room_type')
    def _validate_room_type(self, key, room_type):
        if room_type not in self.ROOM_TYPE.values():
            raise_error_json(InvalidateError(args=('room_type', room_type,)))
        return room_type

    @classmethod
    def get_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        _list = session.query(cls).filter(cls.hotel_fee_id==hotel_fee_id).all()
        return _list

    @classmethod
    def create(cls, hotel_fee_id, room_type,
               start_time, end_time, price, note=None):
        session = DBSession()
        price = cls(
            hotel_fee_id=hotel_fee_id, room_type=room_type,
            start_time=start_time, end_time=end_time,
            price=price, note=note
        )
        session.add(price)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ROOM_PRICE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(price, k, v)
        session = DBSession()
        session.merge(price)
        session.flush()

    @classmethod
    def delete(cls, id):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ROOM_PRICE_NOT_EXIST))
        session = DBSession()
        session.delete(price)
        session.flush()

    @classmethod
    def delete_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        price_list = cls.get_by_hotel_fee_id(hotel_fee_id)
        for price in price_list:
            session.delete(price)
        session.flush()


class MealPrice(Base, BaseMixin):
    __tablename__ = 'meal_price'

    MEAL_TYPE = Enum(
        ('BREAKFAST', 1, u'早餐'),
        ('LUNCH', 2, u'午餐'),
        ('DINNER', 3, u'晚餐'),
    )

    hotel_fee_id = Column(Integer, nullable=False, doc=u'费用ID')
    meal_type = Column(TINYINT, nullable=False, doc=u'餐饮类型')
    start_time = Column(DateTime, nullable=False, doc=u'开始时间')
    end_time = Column(DateTime, nullable=False, doc=u'结束时间')
    price = Column(Float(3), nullable=False, doc=u'餐饮价格')
    note = Column(String(100), nullable=True)

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_hotel_fee_id', 'hotel_fee_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('meal_type')
    def _validate_meal_type(self, key, meal_type):
        if meal_type not in self.MEAL_TYPE.values():
            raise_error_json(InvalidateError(args=('meal_type', meal_type,)))
        return meal_type

    @classmethod
    def get_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        _list = session.query(cls).filter(cls.hotel_fee_id==hotel_fee_id).all()
        return _list

    @classmethod
    def create(cls, hotel_fee_id, meal_type,
               start_time, end_time, price, note=None):
        session = DBSession()
        price = cls(
            hotel_fee_id=hotel_fee_id, meal_type=meal_type,
            start_time=start_time, end_time=end_time,
            price=price, note=note
        )
        session.add(price)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.MEAL_PRICE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(price, k, v)
        session = DBSession()
        session.merge(price)
        session.flush()

    @classmethod
    def delete(cls, id):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.MEAL_PRICE_NOT_EXIST))
        session = DBSession()
        session.delete(price)
        session.flush()

    @classmethod
    def delete_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        price_list = cls.get_by_hotel_fee_id(hotel_fee_id)
        for price in price_list:
            session.delete(price)
        session.flush()


class RoomAdditionalCharge(Base, BaseMixin):
    __tablename__ = 'room_additional_charge'

    ROOM_LEVEL = Enum(
        ('STANDARD', 1, '标准间'),
        ('DELUXE', 2, u'豪华间'),
        ('SUITE', 3, u'套间'),
    )

    hotel_fee_id = Column(Integer, nullable=False, doc=u'费用ID')
    room_level = Column(TINYINT, nullable=False, doc=u'房间级别')
    start_time = Column(DateTime, nullable=False, doc=u'开始时间')
    end_time = Column(DateTime, nullable=False, doc=u'结束时间')
    price = Column(Float(3), nullable=False, doc=u'餐饮价格')
    note = Column(String(100), nullable=True)

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_hotel_fee_id', 'hotel_fee_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('room_level')
    def _validate_room_level(self, key, room_level):
        if room_level not in self.ROOM_LEVEL.values():
            raise_error_json(InvalidateError(args=('room_level', room_level,)))
        return room_level

    @classmethod
    def get_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        _list = session.query(cls).filter(cls.hotel_fee_id==hotel_fee_id).all()
        return _list

    @classmethod
    def create(cls, hotel_fee_id, room_level,
               start_time, end_time, price, note=None):
        session = DBSession()
        price = cls(
            hotel_fee_id=hotel_fee_id, room_level=room_level,
            start_time=start_time, end_time=end_time,
            price=price, note=note
        )
        session.add(price)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ROOM_ADDITIONAL_PRICE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(price, k, v)
        session = DBSession()
        session.merge(price)
        session.flush()

    @classmethod
    def delete(cls, id):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.ROOM_ADDITIONAL_PRICE_NOT_EXIST))
        session = DBSession()
        session.delete(price)
        session.flush()

    @classmethod
    def delete_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        price_list = cls.get_by_hotel_fee_id(hotel_fee_id)
        for price in price_list:
            session.delete(price)
        session.flush()


class FestivalAdditionalCharge(Base, BaseMixin):
    __tablename__ = 'festival_additional_charge'

    FESTIVAL_TYPE = Enum(
        ('CHRISTMAS_EVE', 1, u'平安夜'),
        ('CHRISTMAS', 2, u'圣诞节'),
        ('NEW_YEAR', 3, u'新年'),
        ('CHINEASE_NEW_YEAR', 4, u'中国新年'),
    )

    hotel_fee_id = Column(Integer, nullable=False, doc=u'费用ID')
    festival_type = Column(TINYINT, nullable=False, doc=u'节日类型')
    start_time = Column(DateTime, nullable=False, doc=u'开始时间')
    end_time = Column(DateTime, nullable=False, doc=u'结束时间')
    price = Column(Float(3), nullable=False, doc=u'节日附加价格')
    note = Column(String(100), nullable=True)

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_hotel_fee_id', 'hotel_fee_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('festival_type')
    def _validate_festival_type(self, key, festival_type):
        if festival_type not in self.FESTIVAL_TYPE.values():
            raise_error_json(InvalidateError(args=('festival_type', festival_type,)))
        return festival_type

    @classmethod
    def get_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        _list = session.query(cls).filter(cls.hotel_fee_id==hotel_fee_id).all()
        return _list

    @classmethod
    def create(cls, hotel_fee_id, festival_type,
               start_time, end_time, price, note=None):
        session = DBSession()
        price = cls(
            hotel_fee_id=hotel_fee_id, festival_type=festival_type,
            start_time=start_time, end_time=end_time,
            price=price, note=note
        )
        session.add(price)
        session.flush()

    @classmethod
    def update(cls, id, **kwargs):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.FESTIVAL_PRICE_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(price, k, v)
        session = DBSession()
        session.merge(price)
        session.flush()

    @classmethod
    def delete(cls, id):
        price = cls.get_by_id(id)
        if not price:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.FESTIVAL_PRICE_NOT_EXIST))
        session = DBSession()
        session.delete(price)
        session.flush()

    @classmethod
    def delete_by_hotel_fee_id(cls, hotel_fee_id):
        session = DBSession()
        price_list = cls.get_by_hotel_fee_id(hotel_fee_id)
        for price in price_list:
            session.delete(price)
        session.flush()
