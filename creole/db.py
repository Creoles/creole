import logging
import functools

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.exc import SQLAlchemyError

from .config import setting

logger = logging.getLogger(__name__)


class DBManager(object):
    def __init__(self):
        self._session_map = {}

    def create_sessions(self):
        for db, db_config in setting.DB_SETTINGS.iteritems():
            self.add_session(db, db_config)
        return self

    def get_session(self, name):
        try:
            return self._session_map[name]
        except KeyError:
            raise KeyError('`%s` session not created.' % name)

    def add_session(self, db, db_config):
        if db in self._session_map:
            raise ValueError('Duplicate session name `{}`' % db)
        session = self._create_session(db, db_config)
        self._session_map[db] = session
        return session

    def _create_session(self, db, db_config):
        return self.create_engine(db, **db_config) 

    def create_engine(self, db, *args, **kwargs):
        url = kwargs.pop('url')
        engine = sqlalchemy_create_engine(url, **kwargs)
        logger.info('db: %s inited.', db)
        return engine

def gen_commit_deco(DBSession, raise_exc, error_type):
    def decorated(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            session = DBSession()
            try:
                session.flush()
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise_exc(error_type(msg=repr(e)))
            finally:
                session.close()
            return ret
        return wrapper
    return decorated

db_manager = DBManager().create_sessions()
