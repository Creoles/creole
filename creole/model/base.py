# coding: utf-8
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    text,
    Index,
)
from sqlalchemy.ext.declarative import declared_attr

from . import DBSession


class BaseMixin(object):
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

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        obj = session.query(cls).filter(cls.id==id).first()
        return obj
