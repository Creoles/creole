from sqlalchemy.ext.declarative import declarative_base

from ..db import gen_commit_deco, db_manager
from ..exc import raise_error_json, DatabaseError

DBSession = db_manager.get_session('creole')
Base = declarative_base()
gen_commit_deco = gen_commit_deco(DBSession, raise_error_json, DatabaseError)
