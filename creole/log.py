# coding: utf-8
import sys
import logging

from flask import request

from .env import is_prod_env

CREOLE_SYSLOG_FORMAT = '%(name)s[%(process)d]: %(message)s'
CREOLE_CONSOLE_FORMAT = '%(asctime)s %(levelname)-7s ' + CREOLE_SYSLOG_FORMAT


class CreoleFormatter(logging.Formatter):
    """
    Log structure:

        datetime level name[pid] meta-log ## msg

    meta-log structure:

        [rid: request_id] [ip: ip] [os: os] [endpoint: endpoint] ## msg
        |---------------------- meta-log ----------------------|
    """
    MSG_SEPARTOR = '##'

    def _format(self, msg):
        # meta log
        rid = request.rid
        ip = request.ip_route_list
        os = request.platform
        endpoint = request.endpoint
        meta_log = \
            '[rid: {rid}] [ip: {ip}] [os: {os}] [endpoint: {endpoint}]'.format(
                rid=rid, ip=ip, os=os, endpoint=endpoint)
        return ' '.join(meta_log, msg)

    def format(self, record):
        if not isinstance(record.msg, basestring):
            record.msg = str(record.msg)
        record.msg = self.MSG_SEPARTOR + ' ' + record.msg
        record.msg = self._format(record.msg)
        return super(CreoleFormatter, self).format(record)


def _gen_console_log(app_name):
    _dict = {
        'version': 1,
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'loggers': {
            app_name: {
                'level': 'DEBUG',
                'propagate': False,
                'handlers': ['console'],
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'level': 'DEBUG',
            }
        },
        'formatters': {
            'console': {
                '()': CreoleFormatter,
                'format': CREOLE_CONSOLE_FORMAT,
            }
        },
    }
    return _dict


def _gen_syslog_log(app_name):
    _dict = {
        'version': 1,
        'root': {
            'handlers': ['syslog'],
            'level': 'INFO',
        },
        'loggers': {
            app_name: {
                'level': 'INFO',
                'handlers': ['syslog'],
                'propagate': False,
            }
        },
        'handlers': {
            'syslog': {
                'level': 'INFO',
                'address': '/dev/log',
                'facility': 'local6',
                'formatter': 'syslog',
                'class': 'logging.handlers.SysLogHandler',
            }
        },
        'formatters': {
            'syslog': {
                '()': CreoleFormatter,
                'format': CREOLE_SYSLOG_FORMAT,
                'prefix': app_name,
            }
        },
    }
    return _dict


def setup_logging(app_name):
    if sys.platform == 'darwin' or (not is_prod_env()):
        logging.config.dictConfig(_gen_console_log(app_name))
    else:
        logging.config.dictConfig(_gen_syslog_log(app_name))
