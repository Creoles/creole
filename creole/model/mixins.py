from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    text,
    Index,
)
from sqlalchemy.dialects.mysql import (
    TINYINT,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates

from ..exc import InvalidateError


class BaseMixin(object):
    FIELD_STATUS_DELETED = 1
    FIELD_STATUS_NO_DELETE = 0
    FIELD_STATUSES = (
        FIELD_STATUS_DELETED,
        FIELD_STATUS_NO_DELETE,
    )

    @declared_attr
    def __table_args__(self):
        return (
            Index('ix_created_at', 'created_at'),
            Index('ix_updated_at', 'updated_at'),
        )

    id = Column(Integer, primary_key=True)
    is_delete = Column(TINYINT, nullable=False, server_default='0',
                       doc='0: exist, 1: deleted')
    created_at = Column(DateTime, nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False,
                        server_default=text(
                            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
                        ))

    @validates('is_delete')
    def validate_is_delete(self, key, is_delete):
        if is_delete not in self.FIELD_STATUSES:
            raise InvalidateError(args=(key, is_delete))
        return is_delete
