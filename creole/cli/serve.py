# !/usr/bin/env python
# coding: utf-8
"""
usage:
    creole serve
    creole serve [--dev] [--] [<gunicorn_args> ...]
    creole serve --help

options:
    --dev   Run server in dev mode
"""
import os
import sys

from docopt import docopt

from creole.const import CREOLE_DEV
from .util import cd_root


def serve(dev=False, gunicorn_args=None):
    if dev:
        os.environ['CREOLE_ENV'] = CREOLE_DEV 
    if not gunicorn_args:
        sys.argv[1:] = []
        sys.argv.append('creole.wsgi.app:wsgi_app')
    else:
        sys.argv[1:] = gunicorn_args

    from creole.gunicorn import CreooleApplication
    return CreooleApplication(__doc__[7:]).run()


def main(argv=None):
    args = docopt(__doc__, argv=argv)
    with cd_root():
        return serve(args['--dev'], args['<gunicorn_args>'])
