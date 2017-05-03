# coding: utf-8
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    text,
    Index,
    String,
)
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.mysql import (
    TINYINT,
)

from . import DBSession
from ..util import Enum
from ..exc import (
    raise_error_json,
    InvalidateError,
)


class BaseMixin(object):
    FIELD_STATUS = Enum(
        ('FIELD_STATUS_DELETED', 1, u'已删除'),
        ('FIELD_STATUS_NO_DELETE', 0, u'未删除'),
    )

    @declared_attr
    def __table_args__(self):
        return (
            Index('ix_created_at', 'created_at'),
            Index('ix_updated_at', 'updated_at'),
        )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False,
                        server_default=text(
                            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
                        ))


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
    swift_code = Column(String(20), nullable=True, doc=u'国际电汇码')
    note = Column(String(40), nullable=False, doc=u'备注')

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
