# -*- coding:utf-8 -*-
import argparse
from sqlalchemy import create_engine

from creole.model.user import Base
from creole.config import setting

engine = create_engine(setting.CREOLE_DB_URL, echo=True)


def create_all():
    Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cmd', help='db command',
                        choices=['create', 'drop', 'refresh', 'import'])
    args = parser.parse_args()

    if args.cmd and args.cmd == 'create':
        create_all()
    elif args.cmd and args.cmd == 'drop':
        drop_all()
    elif args.cmd and args.cmd == 'refresh':
        drop_all()
        create_all()

if __name__ == '__main__':
    main()
