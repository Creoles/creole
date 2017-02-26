from flask import current_app
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DBSession = current_app.db_manager.get_session('creole')
