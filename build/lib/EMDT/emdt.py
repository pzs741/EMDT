# -*- coding: utf-8 -*-

"""
EMDT（ Extraction and Mining Algorithm for Question Answering Pair Based on Web Document Density and Tags）要完成了：

1.通过TEBR+规则（可选）去除网页文档噪声
2.通过<title>强特征+规则（可选）抽取Web文档主题
3.对于拥有<div>和<h.>强特征的Web文档，循环遍历网页DOM树结合最大最小权重挖掘问答对
4.对于没有<div>和<h.>强特征的Web文档，基于网页正文密度使用判定模型QADM+最大迭代切割算法挖掘问答对
5.集成Web文档的主题、父问题、子问题、答案，其中问题以查询序列的格式输出，答案以网页源代码和纯文本两种格式输出
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'


from EMDT.extraction import TEBR
from EMDT.mining import MineByDensity, MineByTag
from EMDT.util import *


class EMDT(object):
    """ 基于Web文档密度和标签的问答对抽取及挖掘算法 """

    def __init__(self, url, config=None, **kwargs):
        """
        Keyword arguments:
        url                        -- 网址或者字符串（网页源代码），str类型
        config                  -- 默认配置，可拓展，dict类型
        """
        self._config = config or Configuration()
        self._config = extend_config(self._config, kwargs)
        if self._config.LOG_ENABLE:
            logging.basicConfig(level=self._config.LOG_LEVEL,
                                format=self._config.FORMAT,
                                filemode='w')

        self.blockSize = self._config.BLOCKSIZE
        self.capacity = self._config.CAPACITY
        self.timeout = self._config.TIMEOUT
        self.saveImage = self._config.SAVEIMAGE
        self.content_rule = self._config.CONTENT_RULE
        self.topic_rule = self._config.TOPIC_RULE
        self.qa_jaccard_threshold = self._config.QA_JACCARD_THRESHOLD
        self.url = url
        t = TEBR(self.url, self.blockSize, self.capacity, self.timeout, self.saveImage, self.content_rule,
                 self.topic_rule)
        t.extrat()
        self.content = t.content
        self.topic = t.topic
        self.mine_question = []
        self.answers = []
        self.querys_list = []
        self.tag = 0
        self.summery = []

    def analyse(self):
        """ 网页分析
        tag == 0        ---分析失败
        tag == 1        ---网页有强特征，且挖掘数量大于等于2
        tag == 2        ---网页有强特征，但挖掘数量等于1,基于Web文本密度挖掘无效
        tag == 3        ---网页有强特征，但挖掘数量等于1,基于Web文本密度挖掘有效
        tag == 4        ---网页无强特征，基于Web文本密度挖掘无效
        tag == 5        ---网页无强特征，基于Web文本密度挖掘有效
         Return:
         实例变量更新
         """
        m1 = MineByTag(self.content)
        m1.qa_mine()
        m1.get_qa()
        if m1.qa.__len__() >= 2:
            self.tag = 1
            for i in m1.qa:
                self.mine_question.append(question_format(i[0]))
                self.answers.append(i[1])
        elif m1.qa.__len__() == 1:
            self.tag = 2
            self.mine_question.append(question_format(m1.qa[0][0]))
            self.answers.append(m1.qa[0][1])
            m2 = MineByDensity(self.content, self.qa_jaccard_threshold)
            m2.qa_mine()
            m2.get_qa()
            if m2.qa:
                self.tag = 3
                for i in m2.qa:
                    self.mine_question.append(question_format(i[0]))
                    self.answers.append(i[1])
        else:
            self.tag = 4
            m2 = MineByDensity(self.content, self.qa_jaccard_threshold)
            m2.qa_mine()
            m2.get_qa()
            if m2.qa:
                self.tag = 5
                for i in m2.qa:
                    self.mine_question.append(question_format(i[0]))
                    self.answers.append(i[1])
        if self.mine_question.__len__() is not self.answers.__len__():
            raise Exception('发生错误，analyse执行失败！')

    def format(self):
        """ 格式化输出

         Return:
         summery：[[查询序列,主题,答案],...,[...]]               -- list of list 类型
         """
        if not self.tag:
            raise Exception('请先执行analyse方法！')
        elif self.tag == 1:
            for index, i in enumerate(self.mine_question):
                if index == 0:
                    if is_rubbish_phrase(self.mine_question[0]):
                        pass
                    else:
                        self.summery.append([self.topic + ' ' + i, self.topic, self.answers[index]])
                elif index >= 1:
                    if is_rubbish_phrase(self.mine_question[0]):
                        self.summery.append(
                            [self.topic + ' ' + i, self.topic, self.answers[index]])
                    else:
                        self.summery.append(
                            [self.topic + ' ' + self.mine_question[0] + ' ' + i, self.topic, self.answers[index]])
        elif self.tag == 2:
            self.summery.append([self.topic + ' ' + self.mine_question[0], self.topic, self.answers[0]])
        elif self.tag == 3:
            for index, i in enumerate(self.mine_question):
                if index == 0:
                    self.summery.append([self.topic + ' ' + i, self.topic, self.answers[index]])
                elif index >= 1:
                    if i == self.mine_question[0]:
                        pass
                    else:
                        if is_rubbish_phrase(self.mine_question[0]):
                            self.summery.append(
                                [self.topic + ' ' + i, self.topic, self.answers[index]])
                        else:
                            self.summery.append(
                                [self.topic + ' ' + self.mine_question[0] + ' ' + i, self.topic, self.answers[index]])

        elif self.tag == 4:
            pass
        elif self.tag == 5:
            for index, i in enumerate(self.mine_question):
                self.summery.append([self.topic + ' ' + i, self.topic, self.answers[index]])

        for i in self.summery:
            log('info', '\n问答序列：{}，\n主题：{}，\n答案：{}'.format(i[0], i[1], i[2][:50] + '...'))


if __name__ == "__main__":
    pass

