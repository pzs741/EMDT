# -*- coding: utf-8 -*-
"""
extraction_test.py unit test.
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

from EMDT import TEBR

if __name__ == "__main__":
    # with open('test.html', encoding='utf-8', mode='r') as f:
    #     t = TEBR(f.read(),content_rule=[''],topic_rule=[''])
    #     t.extrat()

    t = TEBR('https://support.huaweicloud.com/sol_migrationcloud_faq/sol_migrationcloud_faq_0001.html#',
             content_rule=[''], topic_rule=[''])
    t.extrat()
    print(t.content, '\n', t.topic)
    # print(t.start,t.end)
