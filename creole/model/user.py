# coding: utf-8
import uuid
import datetime
import random
import hashlib
import binascii

from sqlalchemy import (
    Column,
    Unicode,
    String,
    DateTime,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy.orm import validates

from . import Base, DBSession
from .mixins import BaseMixin
from ..exc import (
    raise_error_json,
    ClientError,
    DatabaseError,
    CreoleErrCode,
    ParameterError,
)
# from ..util import Enum

PASSWD_PREFIX = '5ad86243ed508405e'
PASSWD_POSTFIX = 'a313c5b993b84'


# class Role(Base, BaseMixin):
#     ROLES = Enum(
#         ('SUPER_ADMIN', 999, u'超级管理员'),
#         ('ADMIN', 99, u'管理员'),
#         (),
#     )


class User(Base, BaseMixin):
    __tablename__ = 'user'
    # 基本用户信息
    user_name = Column(Unicode(40), nullable=False, unique=True, doc=u'用户名')
    password_hash = \
        Column(String(70), nullable=False, doc=u'用户密码哈希值')
    uuid = Column(String(40), nullable=False, unique=True, doc=u'uuid')
    session_id = Column(String(128), doc=u'用户session id')
    session_create_time = Column(DateTime, doc=u'session创建时间')
    role = Column(TINYINT, nullable=False, doc=u'用户权限')
    customer_name = Column(Unicode(40), nullable=True, doc=u'客户名称')
    address = Column(Unicode(256), nullable=False, doc=u'地址')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')

    @validates('user_name')
    def validate_user_name(self, key, user_name):
        """检验用户名"""
        session = DBSession()
        user = session.query(User).filter(
            User.user_name == user_name,
            User.is_delete == User.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if user is not None:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.USER_NAME_DUPLICATED))
        return user_name

    def new_session(self):
        # TODO: 建立缓存之后，注意新增new cache和删掉old cache
        td = datetime.datetime.now() - datetime.datetime(1980, 1, 1)
        ss = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6  # noqa

        rs = random.randint(10 ** 8, 10 ** 8 * 9)
        user_session = '%d%d' % (ss, rs)
        return user_session

    @classmethod
    def passwd_hash(cls, password):
        """compute the hash value of the password"""
        md = hashlib.md5()
        md.update(PASSWD_PREFIX + password + PASSWD_POSTFIX)
        return binascii.hexlify(md.digest())

    @classmethod
    def add_new_user(cls, **kwargs):
        _uuid = str(uuid.uuid4())
        session = DBSession()
        _user = session.query(cls).filter(
            cls.uuid==_uuid,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if _user:
            raise_error_json(
                DatabaseError(msg='uuid has existed.'))
        passwd = kwargs.pop('password')
        password_hash = cls.passwd_hash(passwd)
        user = User(password_hash=password_hash, uuid=_uuid, **kwargs)
        session.add(user)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def get_by_uuid(cls, uuid):
        session = DBSession()
        user = session.query(cls).filter(
            cls.uuid==uuid,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return user

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        user = session.query(cls).filter(
            cls.id==id,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return user

    @classmethod
    def get_by_name(cls, user_name):
        session = DBSession()
        user = session.query(cls).filter(
            cls.user_name==user_name,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return user

    @classmethod
    def get_by_customer_name(cls, customer_name):
        session = DBSession()
        user = session.query(cls).filter(
            cls.customer_name==customer_name,
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        return user

    @classmethod
    def delete(cls, id):
        DBSession().query(cls).filter(
            cls.id==id
        ).update(
            {'is_delete': cls.FIELD_STATUS.FIELD_STATUS_DELETED},
            synchronize_session=False)

    @classmethod
    def update(cls, id, **kwargs):
        """更新字段"""
        session = DBSession()
        user = session.query(cls).filter(
            cls.id==id, 
            cls.is_delete==cls.FIELD_STATUS.FIELD_STATUS_NO_DELETE
        ).first()
        if user is None:
            raise_error_json(ParameterError(args=(id,)))
        for k, v in kwargs.iteritems():
            if v is not None:
                if k == 'password':
                    v = cls.passwd_hash(v)
                    k = 'password_hash'
                setattr(user, k, v)
        try:
            session.merge(user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
