# coding: utf-8
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
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy import validates

from . import Base, DBSession
from .mixins import BaseMixin
from ..exc import raise_error_json, ClientError, CreoleErrCode
# from ..util import Enum

PASSWD_PREFIX = '5ad86243ed508405e'
PASSWD_POSTFIX = 'a313c5b993b84'


# class Role(Base, BaseMixin):
#     ROLES = Enum(
#         ('SUPER_ADMIN', 999, u'超级管理员'),
#         ('ADMIN', 99, u'管理员'),
#         (),
#     )


class UserMixin(BaseMixin):
    # 基本用户信息
    user_name = Column(Unicode(40), nullable=False, unique=True, doc=u'用户名')
    password_hash = \
        Column(String(70), nullable=False, doc=u'用户密码哈希值')
    uuid = Column(String(40), nullable=False, unique=True, doc=u'uuid')
    session_id = Column(String(128), doc=u'用户session id')
    session_create_time = Column(DateTime, doc=u'session创建时间')
    role = Column(TINYINT, nullable=False, doc=u'用户权限')

    def new_session(self):
        # TODO: 建立缓存之后，注意新增new cache和删掉old cache
        td = datetime.datetime.now() - datetime.datetime(1980, 1, 1)
        ss = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6  # noqa

        rs = random.randint(10 ** 8, 10 ** 8 * 9)
        user_session = '%d%d' % (ss, rs)
        return user_session

    def passwd_hash(self, password):
        """compute the hash value of the password"""
        md = hashlib.md5()
        md.update(PASSWD_PREFIX + password + PASSWD_POSTFIX)
        return binascii.hexlify(md.digest())

    @validates('password_hash')
    def validate_password_hash(self, key, password):
        return self.passwd_hash(password)


class CustomerUser(Base, UserMixin):
    """客户"""
    __tablename__ = 'customer_user'

    customer_name = Column(Unicode(40), nullable=False, doc=u'客户名称')
    address = Column(Unicode(256), nullable=False, doc=u'地址')
    telephone = Column(String(20), nullable=False, doc=u'联系电话')

    @validates('user_name')
    def validate_user_name(self, key, user_name):
        """检验用户名"""
        session = DBSession()
        user = session.query(CustomerUser).filter(user_name == user_name).first()
        if user is not None:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.USER_NAME_DUPLICATED))

class AdminUser(Base, UserMixin):
    """管理员"""
    __tablename__ = 'admin_user'

    @validates('user_name')
    def validate_user_name(self, key, user_name):
        """检验用户名"""
        session = DBSession()
        user = session.query(AdminUser).filter(user_name == user_name).first()
        if user is not None:
            raise_error_json(
                ClientError(errcode=CreoleErrCode.USER_NAME_DUPLICATED))
