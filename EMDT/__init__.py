# -*- coding: utf-8 -*-
"""
努力不需要理由，如果需要，就是为了不需要的理由。
"""
__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

from EMDT.emdt import EMDT
from EMDT.extraction import TEBR
from EMDT.mining import (
    Mine,
    MineByTag,
    MineByDensity
)

__all__ = [EMDT, TEBR, Mine, MineByTag, MineByDensity]

version_info = (0, 1, 2)

__version__ = ".".join(map(str, version_info))

print('__title__:',__title__)
print('__author__:',__author__)
print('__license__:',__license__)
print('__copyright__:',__copyright__)
print('__version__:',__version__)
