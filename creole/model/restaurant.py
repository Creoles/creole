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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

from . import Base, DBSession
from .mixins import AccountMixin, BaseMixin
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
        session.flush()

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
        meal = cls.get_by_id(id)
        if not meal:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_MEAL_TYPE_NOT_EXIST))
        session = DBSession()
        if adult_fee:
            meal.adult_fee = adult_fee
        if adult_cost:
            meal.adult_cost = adult_cost
        if child_fee:
            meal.child_fee = child_fee
        if child_cost:
            meal.child_cost = child_cost
        session.merge(meal)
        session.flush()


class Restaurant(Base, BaseMixin):
    __tablename__ = 'restaurant'

    TYPE = Enum(
        ('CHINESE', 1, u'中餐'),
        ('SRILANKA', 2, u'斯里兰卡'),
        ('WESTERN', 3, u'西餐'),
        ('SPECIAL', 4, u'综合'),
        ('GENERAL', 5, u'其他'),
    )
    ENVIRON_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )
    TASTE_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )
    SERVICE_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )
    COST_LEVEL = Enum(
        ('LUXURY', 1, u'昂贵'),
        ('NORMAL', 2, u'一般'),
        ('BUDGET', 3, u'便宜'),
    )
    COOPERATION_LEVEL = Enum(
        ('KEY', 1, u'核心'),
        ('NORMAL', 2, u'一般'),
    )
    RECOMMEND_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )

    name = Column(Unicode(30), unique=True, nullable=False, doc=u'中文名称')
    name_en = Column(String(30), unique=True, nullable=False, doc=u'英文名称')
    nickname_en = Column(String(20), unique=True, nullable=False, doc=u'英文名简称')
    restaurant_type = Column(TINYINT, nullable=False, doc=u'餐厅类型')
    country_id = Column(Integer, nullable=False, doc=u'国家id')
    city_id = Column(Integer, nullable=False, doc=u'城市id')
    address = Column(String(100), nullable=False, doc=u'餐厅地址')
    intro_cn = Column(Unicode(128), nullable=True, doc=u'中文介绍')
    intro_en = Column(String(128), nullable=True, doc=u'英文介绍')
    environ_level = Column(TINYINT, nullable=False, doc=u'环境等级')
    taste_level = Column(TINYINT, nullable=False, doc=u'口味等级')
    service_level = Column(TINYINT, nullable=False, doc=u'服务等级')
    cost_level = Column(TINYINT, nullable=False, doc=u'消费等级')
    cooperation_level = Column(TINYINT, nullable=False, doc=u'合作程度')
    recommend_level = Column(TINYINT, nullable=False, doc=u'推荐程度')

    # 联系人信息
    contact_one = Column(String(20), nullable=False, doc=u'联系人')
    position_one = Column(String(20), nullable=False, doc=u'职位')
    telephone_one = Column(String(20), nullable=False, doc=u'联系电话')
    email_one = Column(String(30), nullable=False, doc=u'邮箱')
    contact_two = Column(String(20), nullable=False, doc=u'联系人')
    position_two = Column(String(20), nullable=False, doc=u'职位')
    telephone_two = Column(String(20), nullable=False, doc=u'联系电话')
    email_two = Column(String(30), nullable=False, doc=u'邮箱')
    contact_three = Column(String(20), nullable=True, doc=u'联系人')
    position_three = Column(String(20), nullable=True, doc=u'职位')
    telephone_three = Column(String(20), nullable=True, doc=u'联系电话')
    email_three = Column(String(30), nullable=True, doc=u'邮箱')

    # 餐厅套餐介绍
    standard_meal_intro_cn = Column(Unicode(500), nullable=True, doc=u'标准餐中文介绍')
    standard_meal_intro_en = Column(String(800), nullable=True, doc=u'标准餐英文介绍')
    upgrade_meal_intro_cn = Column(Unicode(500), nullable=True, doc=u'升级餐中文介绍')
    upgrade_meal_intro_en = Column(String(800), nullable=True, doc=u'升级餐英文介绍')
    luxury_meal_intro_cn = Column(Unicode(500), nullable=True, doc=u'豪华餐中文介绍')
    luxury_meal_intro_en = Column(String(800), nullable=True, doc=u'豪华餐英文介绍')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_name', 'name'),
            Index('ix_name_en', 'name_en'),
            Index('ix_country_id', 'country_id'),
            Index('ix_city_id', 'city_id'),
            Index('ix_restaurant_type', 'restaurant_type'),
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

    @validates('environ_level')
    def _validate_environ_level(self, key, environ_level):
        if environ_level not in self.ENVIRON_LEVEL.values():
            raise_error_json(InvalidateError(args=('environ_level', environ_level)))
        return environ_level

    @validates('taste_level')
    def _validate_taste_level(self, key, taste_level):
        if taste_level not in self.TASTE_LEVEL.values():
            raise_error_json(InvalidateError(args=('taste_level', taste_level)))
        return taste_level

    @validates('service_level')
    def _validate_service_level(self, key, service_level):
        if service_level not in self.SERVICE_LEVEL.values():
            raise_error_json(InvalidateError(args=('service_level', service_level)))
        return service_level

    @validates('cost_level')
    def _validate_cost_level(self, key, cost_level):
        if cost_level not in self.COST_LEVEL.values():
            raise_error_json(InvalidateError(args=('cost_level', cost_level)))
        return cost_level

    @validates('cooperation_level')
    def _validate_cooperation_level(self, key, cooperation_level):
        if cooperation_level not in self.COOPERATION_LEVEL.values():
            raise_error_json(InvalidateError(args=('cooperation_level', cooperation_level)))
        return cooperation_level

    @validates('recommend_level')
    def _validate_recommend_level(self, key, recommend_level):
        if recommend_level not in self.RECOMMEND_LEVEL.values():
            raise_error_json(InvalidateError(args=('recommend_level', recommend_level)))
        return recommend_level

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
    def delete(cls, id):
        session = DBSession()
        restaurant = session.query(cls).filter(cls.id==id).first()
        if not restaurant:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.RESTAURANT_NOT_EXIST))
        session.delete(restaurant)
        session.flush()

    @classmethod
    def create(cls, name, name_en, nickname_en, restaurant_type,
               country_id, city_id, address, environ_level,
               taste_level, service_level, cost_level,
               cooperation_level, recommend_level, contact_one,
               position_one, telephone_one, email_one, contact_two,
               position_two, email_two, telephone_two, contact_three=None,
               position_three=None, email_three=None, telephone_three=None,
               standard_meal_intro_cn=None, standard_meal_intro_en=None,
               upgrade_meal_intro_cn=None, upgrade_meal_intro_en=None,
               luxury_meal_intro_cn=None, luxury_meal_intro_en=None,
               intro_cn=None, intro_en=None):
        cls._validate_country_and_city(country_id, city_id)
        session = DBSession()
        restaurant = cls(
            name=name, name_en=name_en, nickname_en=nickname_en,
            restaurant_type=restaurant_type, country_id=country_id,
            city_id=city_id, address=address, environ_level=environ_level,
            taste_level=taste_level, service_level=service_level,
            cost_level=cost_level, cooperation_level=cooperation_level,
            recommend_level=recommend_level, contact_one=contact_one,
            position_one=position_one, telephone_one=telephone_one,
            email_one=email_one, contact_two=contact_two,
            position_two=position_two, email_two=email_two,
            telephone_two=telephone_two, contact_three=contact_three,
            position_three=position_three, email_three=email_three,
            telephone_three=telephone_three,
            standard_meal_intro_cn=standard_meal_intro_cn,
            standard_meal_intro_en=standard_meal_intro_en,
            upgrade_meal_intro_cn=upgrade_meal_intro_cn,
            upgrade_meal_intro_en=upgrade_meal_intro_en,
            luxury_meal_intro_cn=luxury_meal_intro_cn,
            luxury_meal_intro_en=luxury_meal_intro_en,
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
               restaurant_type=None,
               page=1, number=20):
        session = DBSession()
        query = session.query(cls)
        total = None
        if city_id:
            query = query.filter(cls.city_id==city_id)
        elif country_id:
            query = query.filter(cls.country_id==country_id)
        if restaurant_type:
            query = query.filter(cls.restaurant_type==restaurant_type)
        if page == 1:
            total = query.count()
        shop_list = query.offset((page - 1) * number).limit(number).all()
        return shop_list, total


class RestaurantAccount(Base, AccountMixin):
    __tablename__ = 'restaurant_account'

    restaurant_id = Column(Integer, nullable=False, doc=u'餐厅id')

    @declared_attr
    def __table_args__(self):
        table_args = (
            Index('ix_restaurant_id', 'restaurant_id'),
        )
        return table_args + BaseMixin.__table_args__

    @validates('restaurant_id')
    def _validate_restaurant_id(self, key, restaurant_id):
        tour_guide = DBSession().query(Restaurant).filter(
            Restaurant.id==restaurant_id).first()
        if not tour_guide:
            raise_error_json(InvalidateError(args=('restaurant_id', restaurant_id,)))
        return restaurant_id

    @classmethod
    def get_by_restaurant_id(cls, restaurant_id):
        account = DBSession().query(cls).filter(
            cls.restaurant_id==restaurant_id).all()
        return account

    @classmethod
    def create(cls, restaurant_id, currency, bank_name,
               deposit_bank, payee, account, swift_code=None,
               note=None):
        session = DBSession()
        account = cls(
            restaurant_id=restaurant_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, swift_code=swift_code,
            note=note)
        session.add(account)
        session.flush()

    @classmethod
    def delete(cls, id=None, restaurant_id=None):
        if not (id or restaurant_id):
            raise_error_json(InvalidateError())
        session = DBSession()
        if restaurant_id:
            account = session.query(cls).filter(cls.restaurant_id==restaurant_id).first()
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
                ClientError(errcode=CreoleErrCode.RESTAURANT_ACCOUNT_NOT_EXIST))
        for k, v in kwargs.iteritems():
            setattr(account, k, v)
        session.merge(account)
        session.flush()
