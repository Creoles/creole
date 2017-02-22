import logging

from sqlalchemy import create_engine as sqlalchemy_create_engine

from .config import setting

logger = logging.getLogger(__name__)


class DBManager(object):
    def __init__(self):
        self._session_map = {}

    def create_sessions(self):
        for db, db_config in setting.DB_SETTINGS.iteritems():
            self.add_session(db, db_config)

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
        engine = sqlalchemy_create_engine(*args, **kwargs)
        logger.info('db: %s inited.', db)
        return engine
