# -*- coding: utf-8 -*-
"""
util主要完成了以下工作：
1.规则字符、特征字符
2.查询词格式化函数、归一化函数、日志函数、拓展配置函数
3.全局配置
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

import logging
import os
import re

from TEDT.segmentation import WordSegmentation, get_default_stop_words_file
from jieba import cut

DEBUG = True

reBODY = r'<body.*?>([\s\S]*?)<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG = r'<[\s\S]*?>|[ \t\r\f\v]'
reTEXTAREA = r'<textarea.*?>([\s\S]*?)<\/textarea>'
reIMG = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')

a_bad_words = q_good_words = ['请问', '问', 'Q', '什么', '吗', '？', '哪些', '是否', '如何', '能否', '原因']
q_bad_words = a_good_words = ['回答', '答', '答案', 'A']


# 产生一个停词列表
def stop_words_list():
    stop_words_list = []
    with open(get_default_stop_words_file(), encoding='utf-8', mode='r') as f:
        line = f.readline()
        while line:
            stop_words_list.append(line.replace(" ", '').strip().lower())
            line = f.readline()
    return stop_words_list


# 判断一个单词是否为停词
def in_stopwords(word):
    if type(word) == str:
        word = word.replace(" ", '').strip().lower()
    else:
        raise Exception('错误格式类型{},无法判断是否为停词！'.format(type(word)))
    if word in stop_words_list():
        return True
    else:
        return False


# 判断一个短语是否全由停词组成
def is_rubbish_phrase(phrase):
    phrase_list = [i for i in cut(phrase)]
    count = 0
    for i in phrase_list:
        if in_stopwords(i):
            count += 1
    if count == phrase_list.__len__():
        return True
    else:
        return False


# 将问题格式化
def question_format(question):
    return question.replace(" ", '').strip()


# 将list中的一个数据归一化
def normalized(data, data_list):
    return (data - min(data_list) + 1) / (max(data_list) - min(data_list) + 1)


# 日志函数
def log(level, msg):
    global DEBUG
    if DEBUG:
        if level == 'info':
            logging.info(msg)
        elif level == 'warning':
            logging.warning(msg)
        elif level == 'debug':
            logging.debug(msg)
        elif level == 'error':
            logging.error(msg)
    else:
        pass


def get_current_path(path):
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, path)


# jaccard相关度
def jaccard(x1, x2):
    intersection = [i for i in x1 if i in x2]
    union = [i for i in x1 if i not in x2]
    union[0:0] = x2
    return float(len(intersection)) / len(union)


# 计算简化的qa相关系数
def qa_jaccard(q, a):
    w = WordSegmentation()
    q = w.segment(q)
    a = w.segment(a)
    intersection = [i for i in q if i in a]
    if intersection:
        return float(intersection.__len__() / q.__len__())
    else:
        return 0

# 拓展配置，自动将字典转换为参数配置
def extend_config(config, config_items):
    """
    We are handling config value setting like this for a cleaner api.
    Users just need to pass in a named param to this source and we can
    dynamically generate a config object for it.
    """
    for key, val in list(config_items.items()):
        if hasattr(config, key):
            setattr(config, key, val)

    return config


# 全局配置
class Configuration(object):
    def __init__(self):
        """
        Modify any of these QGDT properties
        TODO: Have a separate Config extend this!
        """

        self.LOG_ENABLE = True  # 是否开启日志
        self.LOG_LEVEL = 'INFO'  # 默认日志等级
        self.LOG_FILE = get_current_path('log.txt')  # 日志默认存储路径（项目根目录）
        self.FORMAT = '%(asctime)s - %(levelname)s - %(message)s'  # 日志输出格式
        self.BLOCKSIZE = 10  # 网页正文抽取行块的窗口长度
        self.CAPACITY = 5  # 网页正文抽取行块的窗口容量
        self.TIMEOUT = 5  # 输入为URL是响应超时时间
        self.SAVEIMAGE = False  # 网页源代码中是否保留图片地址
        self.CONTENT_RULE = ['.help-details.webhelp', '.help-center-title']  # 正文辅助抽取规则
        self.TOPIC_RULE = ['.crumbs', '.parentlink']  # 主题辅助抽取规则
        self.QA_JACCARD_THRESHOLD = 0.25  # 基于密度的挖掘算法问答过滤阈值
        self.REMOVE_HTML = False#去除答案HTML

if __name__ == '__main__':
    phrase = 'DNS'
    print(is_rubbish_phrase(phrase))
