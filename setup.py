# !/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
)

setup(
    name='creole',
    version='1.0.0',
    description='OTA Backend System',
    author='Eric Zhang',
    author_email='eric.pucker@gmail.com',
    packages=[
        'creole',
        'creole.cli',
    ],
    include_package_data=True,
    url='https://github.com/creoles/creole',
    entry_points={
        'console_scripts': [
            'creole = creole.cli:main',
        ],
    },
    install_requires=open('requirements.txt').readlines(),
)
