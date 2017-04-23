from .util import get_setting_manager
from .const import CREOLE_PROD

setting_manager = get_setting_manager()

CREOLE_ENV = setting_manager.get('CREOLE_ENV', CREOLE_PROD)
CREOLE_HOST = setting_manager.get('CREOLE_HOST', '127.0.0.1')
CREOLE_PORT = setting_manager.get_int('CREOLE_PORT', 8888)
CREOLE_DB_URL = setting_manager.get('CREOLE_DB_URL',
        "mysql+pymysql://root:123456@localhost:3306/creole?charset=utf8")
DB_SETTINGS = {
    'creole': {
        'url': CREOLE_DB_URL,
        'max_overflow': -1,
        'pool_size': 10,
        'pool_recycle': 1200
    }
}
