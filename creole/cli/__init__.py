#!/usr/bin/env python
# coding: utf-8
"""
Usage:
    creole <command> [<args> ...]
    creole --help

Commands:
    deploy      Deploy service to remote host
    serve       Start server
"""
import sys

from docopt import docopt

from . import deploy, serve


def main():
    args = docopt(__doc__, options_first=True)
    argv = [args['<command>']] + args['<args>']
    rv = 0
    if args['<command>'] == 'deploy':
        rv = deploy.main(argv=argv)
    elif args['<command>'] == 'serve':
        rv = serve.main(argv=argv)
    sys.exit(rv)


if __name__ == "__main__":
    main()
