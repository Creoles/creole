from flask import current_app
from sqlalchemy.ext.declarative import declarative_base

from ..db import gen_commit_deco
from ..exc import raise_error_json, DatabaseError

Base = declarative_base()
DBSession = current_app.db_manager.get_session('creole')
gen_commit_deco = gen_commit_deco(DBSession, raise_error_json, DatabaseError)
