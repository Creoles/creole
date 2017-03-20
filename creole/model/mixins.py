# coding: utf-8
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    text,
    Index,
)
from sqlalchemy.ext.declarative import declared_attr

from ..util import Enum


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
