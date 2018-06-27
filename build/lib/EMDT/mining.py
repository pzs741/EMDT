# -*- coding: utf-8 -*-
"""
mining主要完成了：
1.基于Web文档标签特征的问答对挖掘
2.基于Web文档密度特征的问答对挖掘
3.问答对生成
"""

__title__ = 'QAEM'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

from math import log1p

import jieba
from TEDT.text_rank import TextRank
from bs4 import BeautifulSoup

from EMDT.extraction import TEBR
from EMDT.util import *


class Mine(object):
    """ 挖掘类：提供两种算法所需的静态方法 """

    def __init__(self, content):
        """
       Keyword arguments:
       content                 -- 正文源代码，str类型-->BS类型
       """
        self.content = BeautifulSoup(content, "lxml")

    @staticmethod
    def bs_filter(bs_list):
        """ 网页DOM结点过滤器
        Input：bs_list        -- 所有结点（父、子），list类型
        1.含有 DIV 和 H. 的强特征标签
        2.H. 标签的 text 不能为无意义的停用词
        Outpt:new_bs_list      -- 满足要求的结点序列，list类型
        """
        new_bs_list = []
        word = None
        for i in bs_list:
            if i.h1:
                word = i.h1.text
            elif i.h2:
                word = i.h2.text
            elif i.h3:
                word = i.h3.text
            elif i.h4:
                word = i.h4.text
            elif i.h5:
                word = i.h5.text
            elif i.h6:
                word = i.h6.text
            if word and not in_stopwords(word):
                new_bs_list.append(i)
        return new_bs_list

    @staticmethod
    def mine_num(bs_object):
        """ DOM结点可挖掘子结点的数目
        Input：bs_object        -- 网页DOM结点，bs类型
        Outpt:mine_num          -- 可挖掘的子结点数目，int类型
        """
        return bs_object.find_all('div').__len__()

    @staticmethod
    def nearest_h(bs_object):
        """ 网页DOM结点最近的H.标签号
        Input：bs_object        -- 网页DOM结点，bs类型
        1.必须含有H.标签
        Outpt:H.标签的类型号      -- int类型
        """
        for child in bs_object.descendants:
            if child.name == 'h1':
                return 1
            elif child.name == 'h2':
                return 2
            elif child.name == 'h3':
                return 3
            elif child.name == 'h4':
                return 4
            elif child.name == 'h5':
                return 5
            elif child.name == 'h6':
                return 6

    @staticmethod
    def remove_h(*args):
        """ 去除网页DOM结点中的H.标签及内容
        Input：结点（str）和H.标签号（int） -- tuple类型
        Outpt:去除指定H.标签的DOM结点      -- str类型
        """
        a_list = []
        for i in args[0].contents:
            if not i.name == 'h' + str(args[1]):
                a_list.append(str(i))
        return ''.join(a_list).strip()

    @staticmethod
    def space_count(list):
        """ 空行统计，文本密度化
        Input：按\n划分的文本列表            -- list类型
        Outpt:空行数目表示的文本列表         -- list类型
        """
        tmp = []
        new_list = []
        for i in list:
            if i is not '':
                if len(tmp) is not 0:
                    new_list.append(tmp.count(''))
                new_list.append(i)
                tmp = []
            else:
                tmp.append(i)
        return new_list

    @staticmethod
    def split_with_number(content, number):
        """ 按指定数字切分密度化文本
        Input：文本列表（list），切分号（int）
        切分号对应密度文本中的空行号的数目
        Outpt:切分后的多文本序列[文本序列，切分号，文本序列...]       -- list of list类型
        """
        remain_list = []
        tmp_list = []
        for i in range(content.__len__()):
            if content[i] is not number:
                tmp_list.append(content[i])
            elif content[i] == number:
                remain_list.append(tmp_list)
                remain_list.append(content[i])
                tmp_list = []
            if i == content.__len__() - 1 and tmp_list is not []:
                remain_list.append(tmp_list)
        return remain_list

    @staticmethod
    def get_diff_number_from_list(list):
        """ 获得密度化文本中不同的行数统计号
        Input：密度化文本                     -- list类型
        Outpt:降序排列的行数统计号序列           -- list类型
        """
        number_list = []
        for i in list:
            if type(i) == int and i not in number_list:
                number_list.append(i)
        return sorted(number_list, reverse=True)

    @staticmethod
    def find_str_and_join(list):
        """ 连接密度化文本中的字符串序列
        Input：密度化文本[序列1,num,序列2,序列3,num]                     -- list类型
        Outpt:连接的密度化文本[序列1,num,序列2+序列3,num]                 -- str类型
        """
        tmp = []
        for i in list:
            question = [a for a in cut(str(i)) if a in q_good_words]
            if type(i) == str and not question:
                tmp.append(i)
            elif type(i) == str and  question:
                break

        return '\n'.join(tmp)

    @staticmethod
    def list_to_qa(list_int):
        """ 将单位密度化文本序列转化为[q,a]形式
        Input：一个密度化文本序列[序列1,序列2,序列3]  -- list类型
        Outpt:[序列1，其它文本序列]                 -- list类型
        """
        if type(list_int) == list:
            if list_int.__len__() == 1:
                return list_int[0]
            if list_int.__len__() >= 2:
                q = list_int[0]
                a = Mine.find_str_and_join(list_int[1:])
                return [q, a]
        return list_int

    @staticmethod
    def list_to_list_qa(remain_list):
        """ 将整个密度化文本序列转化为[q,a]形式
        Input：密度化文本序列集合[序列1,num,序列2...]          -- list类型
        Outpt:[[q1,a1],num,[q2,a2]...]                 -- list类型
        """
        qa_list = []
        for i in range(remain_list.__len__()):
            if type(remain_list[i]) == int:
                qa_list.append(remain_list[i])
            if type(remain_list[i]) == list:
                qa_list.append(Mine.list_to_qa(remain_list[i]))
        return qa_list

    @staticmethod
    def qa_filter(one_mine_list, qa_jaccard_threshold):
        """ 问答对过滤函数
        Input：问答对列表（tuple of list），过滤阈值（float）
        使用简化的jaccard函数--qa_jaccard过滤
        Outpt:过滤后的问答对列表                 -- list类型
        """
        filter_list = []
        for i in one_mine_list:
            if type(i) == list and i.__len__() == 2 and qa_jaccard(i[0], i[1]) >= qa_jaccard_threshold:
                filter_list.append((i[0], i[1]))
        return filter_list

    @staticmethod
    def get_good_and_bad_count(qa):
        """ 问题答案特征词统计
        Input：问答对                            -- tuple类型
        问题和答案特征互为好坏特征
        Outpt:积极特征数，消极特征数                -- int类型
        """
        g_count = 0
        b_count = 0

        for i in jieba.cut(qa[0]):
            if i in q_good_words:
                g_count += 1
            if i in q_bad_words:
                b_count += 1

        for i in jieba.cut(qa[1]):
            if i in a_good_words:
                g_count += 1
            if i in a_bad_words:
                b_count += 1

        return g_count, b_count

    @staticmethod
    def QADM(qa_list):
        """ 问答对挖掘模型
        Input：问答对列表                            -- list类型
        问答列表整体相关度得分*问答特征平均分
        Outpt:得分                              -- float类型
        """
        if not qa_list:
            return 0
        q_list = []
        a_list = []
        g_count = 0
        b_count = 0
        qa_score = 1
        for i in qa_list:
            q_list.append(i[0])
            a_list.append(i[1])
            g_count += Mine.get_good_and_bad_count(i)[0]
            b_count += Mine.get_good_and_bad_count(i)[1]
            qa_score *= ((g_count + 1) / (b_count + 1) + 1)
            g_count = 0
            b_count = 0
        q = [i for i in jieba.cut(''.join(q_list))]
        a = ''.join(a_list)
        t = TextRank()
        t.analyze(a)
        kv_list = t.wordvector()
        word_list = [i.word for i in kv_list]
        weight_list = [i.weight for i in kv_list]
        sim_score = 0
        for i in q:
            if i in word_list:
                sim_score += normalized(weight_list[word_list.index(i)], weight_list)
        return sim_score / len(qa_list) * log1p(qa_score)


class MineByTag(Mine):
    """ 基于Web标签的问答对挖掘算法 """

    def __init__(self, content):
        """
        Keyword arguments:
        content                 -- 继承类Mine
        """
        super(MineByTag, self).__init__(content)
        self.qa_list = self.content.find_all('div')
        self.rank_list = []
        self.qa = []

    def qa_mine(self):
        """ qa对挖掘
        1.H.标签号越小的权值越大，优先保留
        2.挖掘数目越大的权值越小，优先舍弃
        """
        self.qa_list = Mine.bs_filter(self.qa_list)
        for i in self.qa_list:
            self.rank_list.append((i, Mine.mine_num(i)))
        self.rank_list.sort(key=lambda x: x[1], reverse=True)
        self.rank_list = [(i[0], Mine.nearest_h(i[0])) for i in self.rank_list]

    def get_qa(self):
        """ 获取问答对
        1.抽取DOM结点中H.标签中的正文作为问题
        2.删除DOM结点中H标签，作为问题的答案
        """
        for i in self.rank_list:
            q = i[0].find('h' + str(i[1]))
            if q and q.text not in [i[0] for i in self.qa]:
                a = Mine.remove_h(i[0], i[1])
                self.qa.append((q.text, a))


class MineByDensity(Mine):
    """ 基于Web文本密度的问答对挖掘算法 """

    def __init__(self, content, qa_jaccard_threshold=0.25):
        """
        Keyword arguments:
        注意：content去除标签后（密度化）初始化为类属性
        content                 -- 网页源代码，str-->str
        qa_jaccard_threshold    -- 问答对阈值，float类型
        """
        self.qa_jaccard_threshold = qa_jaccard_threshold
        self.content = TEBR.processTags(content)[0].strip().split('\n')
        self.remain_list = Mine.space_count(self.content)
        self.number_list = Mine.get_diff_number_from_list(self.remain_list)
        self.mine_list = []
        self.qa = []

    def qa_mine(self):
        """ qa对挖掘
        按照行号统计数进行迭代切割
        """
        for i in self.number_list:
            self.mine_list.append(Mine.qa_filter(Mine.list_to_list_qa(Mine.split_with_number(self.remain_list, i)),
                                                 self.qa_jaccard_threshold))

    def get_qa(self):
        """ 获取问答对
        保留挖掘模型得分最大的问答对序列
        """
        if self.mine_list:
            self.score_list = [i for i in map(Mine.QADM, self.mine_list)]
            index = self.score_list.index(max(self.score_list))
            self.qa = [i for i in self.mine_list[index]]
        else:
            pass


if __name__ == "__main__":
    pass
