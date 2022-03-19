#!/usr/bin/env python3
#
# amaconsole setup

from setuptools import setup, find_packages

setup(
    name='amaconsole',
    version='1.0',
    description='Ama console',
    long_description_content_type='text/markdown',
    keywords=['Password Cracking', ],
    author='glozanoa',
    author_email='glozanoa@uni.pe',
    url='https://github.com/fpolit/amaconsole',
    license='GPLv3',
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'amaconsole = amaconsole.main:run',
        ],
    }
)
