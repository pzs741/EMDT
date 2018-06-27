# -*- coding: utf-8 -*-
"""
基于行块分布函数的通用网页正文抽取(General web page text extraction based on row block distribution function)）

extraction主要完成了：
1.获取URL、文件源代码
2.网页正文抽取
3.网页主题抽取
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

import requests
from bs4 import BeautifulSoup

from EMDT.util import *


class TEBR(object):
    """ 基于行块分布函数的通用网页正文抽取 """

    def __init__(self, url, blockSize=10, capacity=5, timeout=5, image=False, content_rule=['.help-details.webhelp'],
                 topic_rule=['.crumbs', '.parentlink']):
        """
        Keyword arguments:
        url                        -- 网址或者字符串（网页源代码），str类型
        blockSize                  -- 窗口大小，int类型
        capacity                   -- 窗口容量，int类型
        timeout                  -- 超时时间，int类型
        image                  -- 加载图像源码，bool类型
        content_rule                   -- 正文抽取规则，list类型
        topic_rule                   -- 主题抽取规则，list类型
        """
        self.url = url
        self.blockSize = blockSize
        self.capacity = capacity
        self.timeout = timeout
        self.saveImage = image
        self.content_rule = content_rule
        self.topic_rule = topic_rule
        self.rawPage = ""
        self.ctexts = []
        self.cblocks = []
        self.content = ""
        self.topic = ''
        self.textline_list = []
        self.bad = False

    def getRawPage(self):
        """ 获取网页源代码

         Return:
         网页源代码               -- 文件或者网页源代码,str类型
         """
        if type(self.url) is not str:
            raise Exception('请输入字符串序列，文本或者url！')
        elif self.url.startswith('http'):
            resp = requests.get(self.url, timeout=self.timeout)
            resp.encoding = "UTF-8"
            return resp.text
        else:
            return self.url

    @classmethod
    def processTags(cls, body):
        """ 去除所有tag，包括样式、Js脚本内容等，但保留原有的换行符\n

         Return:
         文本行，预处理后的网页源代码               -- str类型，list类型
         """
        body = re.sub(reCOMM, "", body)
        body = re.sub(reTRIM.format("script"), "", re.sub(reTRIM.format("style"), "", body))
        body = re.sub(reTEXTAREA, "", body)
        textline_list = body.split('\n')
        body = re.sub(reTAG, "", body)
        return body, textline_list

    def processBlocks(self):
        """ 将网页内容按行分割，定义行块 blocki 为第 [i,i+blockSize] 行文本之和并给出行块长度基于行号的分布函数

        1.构造行块分布函数
        2.选定起始和终止位置
         """
        self.ctexts = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]
        self.cblocks = [0] * (len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x, y: x + y, self.textLens[i: lines - 1 - self.blockSize + i], self.cblocks))
        if self.cblocks:
            maxTextLen = max(self.cblocks)
        else:
            self.bad = True
            return ''
        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > self.capacity:
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > self.capacity:
            self.end += 1
        # 正文出现在最长的行块，截取两边至行块长度为 0 的范围：
        # self.content = "\n".join(self.ctexts[self.start:self.end]).strip()

    def processImages(self):
        """ 如果需要提取正文区域出现的图片，只需要在第一步去除tag时保留<img>标签的内容 """
        self.body = reIMG.sub(r'{{\1}}', self.body)

    def getContext(self):
        """ 去除网页噪音

        Return:
         正文网页源代码               -- str类型
         """
        for i in self.content_rule:
            try:
                return str(self.soup.select(i)[0])
            except:
                continue
        self.body = re.findall(reBODY, self.rawPage)[0]
        if self.saveImage:
            self.processImages()
        self.body, self.textline_list = self.processTags(self.body)
        self.processBlocks()
        if not self.bad:
            html_code = []
            for index, textline in enumerate(self.textline_list):
                if index >= self.start and index <= self.end:
                    html_code.append(textline)
            return '\n'.join(html_code)
        else:
            return ''

    def get_topic(self):
        """ 获取网页主题字段
        1.存在预配置主题抽取规则则优先规则抽取
        2.不存在预配置主题规则则根据强标签<title>抽取
         """
        for i in self.topic_rule:
            try:
                return self.soup.select(i)[0].text.replace(' ', '').replace('\n', '').split('>')[1]
            except:
                try:
                    return self.soup.select(i)[0].text.strip().split('\n')[1]
                except:
                    continue
        try:
            return re.split('[_\-|]', self.soup.find('title').text)[1]
        except:
            return ''

    def extrat(self):
        """ 抽取网页正文和主题
        1.更新所有实例参数
        2.通过topic和content获取主题和正文源代码
         """
        self.rawPage = re.sub(reTRIM.format("script"), "", re.sub(reTRIM.format("style"), "", self.getRawPage()))
        self.soup = BeautifulSoup(self.rawPage, 'lxml')
        self.content = self.getContext()
        self.topic = self.get_topic()


if __name__ == '__main__':
    pass
