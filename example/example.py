# -*- coding: utf-8 -*-
"""
A simple example, have fun!
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

from EMDT import EMDT

if __name__ == "__main__":
    # dir = '../support.huaweicloud.com/'
    # for x in os.listdir(dir):
    # x = 'support.huaweicloud.com_pg-evs_zh-cn_topic_0017934420.html'
    # x = 'support.huaweicloud.com_sol_disaster_faq_sol_disaster_faq_0001.html'
    # x = 'support.huaweicloud.com_pg-ecs_zh-cn_topic_0017158243.html'
    # with open(dir + x, encoding='utf-8', mode='r') as f:
    #     e = EMDT(f.read())
    #     e.analyse()
    #     e.format()
    #     for i in e.summery:
    #         print(i)
    #
    url = 'https://support.huaweicloud.com/sol_migrationcloud_faq/sol_migrationcloud_faq_0001.html#'
    url = 'https://support.huaweicloud.com/ecs_gls/index.html#'
    e = EMDT(url,
             LOG_ENABLE=True,
             LOG_LEVEL='INFO',
             FORMAT='%(asctime)s - %(levelname)s - %(message)s',
             BLOCKSIZE=10,
             CAPACITY=5,
             TIMEOUT=5,
             SAVEIMAGE=True,
             CONTENT_RULE=['.help-details.webhelp', '.help-center-title'],
             TOPIC_RULE=['.crumbs', '.parentlink'],
             QA_JACCARD_THRESHOLD=0.25,
             REMOVE_HTML=False)
    e.analyse()
    e.format()
    for i in e.summery:
        print(i, '\n-------------------------------------------')
