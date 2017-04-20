# coding: utf-8
from __future__ import absolute_import

import sys
import multiprocessing
from gunicorn.app.wsgiapp import WSGIApplication

from .config import setting
from .env import is_prod_env


class CreoleApplication(WSGIApplication):
    def init(self, parser, opts, args):
        super_cfg = super(CreoleApplication, self).init(
            parser, opts, args)
        cfg = self._get_default_setting()
        if super_cfg:
            cfg.update(super_cfg)
        return cfg

    def _get_default_setting(self):
        cfg = dict(
            proc_name='ota.creole',
            loglevel='debug',
            worker_class='gevent',
            graceful_timeout=10,
            timeout=10,
            bind='{}:{}'.format(
                setting.CREOLE_HOST, setting.CREOLE_PORT),
        )

        if is_prod_env():
            cfg.update(dict(
                workers=multiprocessing.cpu_count() * 2 + 1,
                loglevel='info'))
        if sys.platform != 'darwin':
            cfg.update(dict(
                syslog=True,
                syslog_addr='unix:///dev/log#dgram',
                syslog_prefix='creole',
                syslog_facility='local6'))
        return cfg
