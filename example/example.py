# -*- coding: utf-8 -*-
"""
A simple example, have fun!
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

from EMDT import EMDT

if __name__ == "__main__":
    # dir = 'support.huaweicloud.com/'
    # for x in os.listdir(dir):
    #     with open(dir + x, encoding='utf-8', mode='r') as f:
    #         e = EMDT(f.read())
    #         e.analyse()
    #         e.format()
    #         for i in e.summery:
    #             print(i)
    #
    url = 'https://support.huaweicloud.com/ecs_gls/index.html#'
    e = EMDT(url)
    e.analyse()
    e.format()
    for i in e.summery:
        print(i, '\n-------------------------------------------')
