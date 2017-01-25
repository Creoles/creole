import sys

from .conf import setting
from . import const


def is_prod_env():
    if sys.platform == 'darwin' or \
            setting.CREOLE_ENV == const.CREOLE_TEST:
        return False
    return True
