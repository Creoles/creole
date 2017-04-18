from .config import setting
from . import const


def is_prod_env():
    return setting.CREOLE_ENV == const.CREOLE_PROD
