from sqlalchemy.exc import SQLAlchemyError

from ..model.user import AdminUser, CustomerUser
from ..model import DBSession
from ..exc import raise_error_json, DatabaseError


class AdminUserService(object):
    @classmethod
    def create_user(cls, user_name, password):
        """创建新用户"""
        session = DBSession()
        user = AdminUser(user_name=user_name, password=password, role=999)
        session.add(user)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class CustomerUserService(object):
    @classmethod
    def create_user(cls, user_name, password,
                    customer_name, address, telephone):
        """创建新用户"""
        session = DBSession()
        user = CustomerUser(
            user_name=user_name, password=password, role=999,
            customer_name=customer_name, address=address,
            telephone=telephone)
        session.add(user)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
