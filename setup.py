# -*- coding: utf-8 -*-

import os
import os.path

from setuptools import find_packages
from setuptools import setup

name = 'linkedin_parser'
version = '0.0.1'


def find_requires():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open('{0}/requirements.txt'.format(dir_path), 'r') as reqs:
        requirements = reqs.readlines()
    return requirements


if __name__ == "__main__":
    setup(
        name=name,
        version=version,
        description='linkedin parser tool using selenium',
        packages=find_packages(),
        install_requires=find_requires(),
        data_files=[(
            'linkedin_parser',
            ['linkedin_parser/config.yaml']
        )],
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'lnkd = linkedin_parser.cli:main',
            ],
        },
    )