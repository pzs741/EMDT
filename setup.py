#!/bin/python3.6
# -*- coding: utf-8 -*-
"""
Ex_treme 2018 -- https://github.com/pzs741
"""

import sys
import os
import codecs


__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

version_info = (0, 2, 0)

__version__ = ".".join(map(str, version_info))


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload -r pypi')
    sys.exit()


# This *must* run early. Please see this API limitation on our users:
if sys.version_info[0] == 2 and sys.argv[-1] not in ['publish', 'upload']:
    sys.exit('WARNING! You are attempting to install EMDT\'s '
             'python3 repository on python2. PLEASE RUN '
             '`$ pip3 install EMDT` for python3 or '
             '`$ pip install EMDT` for python2')



with codecs.open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name=__title__,
    version=__version__,
    license=__license__,
    long_description=readme,
    author=__author__,
    description='EMDT,Extraction and Mining Algorithm for Question Answering Pair Based on Web Document Density and Tags',
    author_email='pzsyjsgldd@163.com',
    url='https://github.com/pzs741/EMDT',
    install_requires=['jieba>=0.39','requests>=2.18.4','TEDT>=0.5','beautifulsoup4==4.5.3'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
    packages=['EMDT'],
    package_dir={'EMDT':'EMDT'},
    package_data={'EMDT':['*.*',]}
)
