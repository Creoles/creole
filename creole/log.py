# coding: utf-8
import sys
import logging
import logging.config

from flask import request

from .env import is_prod_env

CREOLE_SYSLOG_FORMAT = '%(name)s[%(process)d]: %(message)s'
CREOLE_CONSOLE_FORMAT = '%(asctime)s %(levelname)-7s ' + CREOLE_SYSLOG_FORMAT


class CreoleFormatter(logging.Formatter):
    """
    Log structure:

        datetime level name[pid] meta-log ## msg

    meta-log structure:

        (rid: request_id ip: ip os: os endpoint: endpoint) ## msg
        |---------------------- meta-log ----------------------|
    """
    MSG_SEPARTOR = '##'

    def __init__(self, prefix, *args, **kwargs):
        self.prefix = prefix
        super(CreoleFormatter, self).__init__(*args, **kwargs)

    def _format(self, msg):
        meta_log = ''
        if request:
            # meta log
            rid = request.rid
            ip = request.ip_route_list
            os = request.platform
            endpoint = request.endpoint
            meta_log = \
                '(rid: {rid} ip: {ip} os: {os} ' \
                'endpoint: {endpoint})'.format(
                    rid=rid, ip=ip, os=os, endpoint=endpoint)
        if meta_log:
            return ' '.join([meta_log, msg])
        return msg

    def format(self, record):
        record.name = self.prefix + '.' + record.name
        if not isinstance(record.msg, basestring):
            record.msg = str(record.msg)
        record.msg = self.MSG_SEPARTOR + ' ' + record.msg
        record.msg = self._format(record.msg)
        return super(CreoleFormatter, self).format(record)


def _gen_console_log(app_name, log_level):
    _dict = {
        'version': 1,
        'root': {
            'handlers': ['console'],
            'level': log_level,
        },
        'loggers': {
            app_name: {
                'level': log_level,
                'propagate': False,
                'handlers': ['console'],
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'formatter': 'console',
                'class': 'logging.StreamHandler',
            }
        },
        'formatters': {
            'console': {
                '()': CreoleFormatter,
                'format': CREOLE_CONSOLE_FORMAT,
                'prefix': app_name,
            }
        },
    }
    return _dict


def _gen_syslog_log(app_name, log_level):
    _dict = {
        'version': 1,
        'root': {
            'handlers': ['syslog'],
            'level': log_level,
        },
        'loggers': {
            app_name: {
                'level': log_level,
                'handlers': ['syslog'],
                'propagate': False,
            }
        },
        'handlers': {
            'syslog': {
                'level': log_level,
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


def setup_logging(app_name, log_level=None):
    if sys.platform == 'darwin':
        log_level = log_level or logging.DEBUG
        log_dict = _gen_console_log(app_name, log_level)
    elif is_prod_env():
        log_level = log_level or logging.INFO
        log_dict = _gen_syslog_log(app_name, log_level)
    else:
        log_level = log_level or logging.DEBUG
        log_dict = _gen_console_log(app_name, log_level)
    logging.config.dictConfig(log_dict)
