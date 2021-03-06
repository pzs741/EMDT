# 基于Web文档密度和标签的问答对抽取及挖掘算法 
---
EMDT（ Extraction and Mining Algorithm for Question Answering Pair Based on Web Document Density and Tags）
---
## 算法功能简介
基于**Web**文档密度和标签的问答对抽取及挖掘算法完成了：从指定**ur**l或者**HTML**文档中抽取出网页源代码，使用**TEBR**（基于**行块分布函数**的通用网页正文抽取算法）去除**网页噪声**，同时可以**辅以规则**提高**正文**和**主题**抽取的准确率（可选），将正文web源代码解析成**DOM树**，通过两个**强特征**标签**< div >**和**< h. >**结合和**最大最小权**循环**深度遍历**DOM树所有子孙结点挖掘问答对，同时提出了一种**不依赖**与任何Web标签的基于**网页文本密度**的**迭代切割算**法找出所有可能存在的问答对序列，再通过**问答对挖掘**模型**QADM**排序打分，最后选举**得分最高**的问答对序列，该算法让**EMDT**的挖掘率上升了**20%**（同时QADM可有效保证问答对的**质量**），两种挖掘**算法融合**使用的情况下，在华为官方提供的测试集上（共**3501**个WEB文档）挖掘出**11914条**问答对，**挖掘率**高达到了3.4，平均每个文档挖掘出**3.4条问答序列**。

## 算法库组成
+ extraction --- TEBR网页正文抽取模块
+ mining --- 挖掘模型和融合算法组成的问答对挖掘模块
+ EMDT --- 网页抽取、去噪、融合挖掘、问答序列生成、质量判定模块。

## 算法库安装
* 全自动安装：pip install EMDT
* 半自动安装：git clone https://github.com/pzs741/EMDT.git 
cd EMDT-mater
python setup.py install
* 手动安装：将 EMDT 目录放置于当前目录或者 site-packages 目录
* 通过 `import EMDT` 来引用

## 基础配置
**特别提醒：**实例化EMDT只需要URL或者WEB源代码，一下为默认的全局配置，实例化时可直接覆盖！
+ LOG_ENABLE = True&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 是否开启日志
+ LOG_LEVEL  = 'INFO'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#默认日志等级
+ LOG_FILE = get_current_path('log.txt')&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#日志默认存储路径（项目根目录）
+ FORMAT = '%(asctime)s - %(levelname)s - %(message)s'&nbsp;&nbsp;&nbsp;#日志输出格式
+ BLOCKSIZE = 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#网页正文抽取行块的窗口长度
+ CAPACITY = 5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#网页正文抽取行块的窗口容量
+ TIMEOUT = 5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#输入为URL是响应超时时间
+ SAVEIMAGE = False&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#网页源代码中是否保留图片地址
+ CONTENT_RULE = ['.help-details.webhelp','.help-center-title']&nbsp;&nbsp;#正文辅助抽取规则
+ TOPIC_RULE = ['.crumbs','.parentlink']&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#主题辅助抽取规则
+ QA_JACCARD_THRESHOLD = 0.25&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#基于密度的挖掘算法问答过滤阈值
+ REMOVE_HTML = False  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#去除答案HTML

## 输入示例
1. 输入为url

```
from EMDT import EMDT
url = 'https://support.huaweicloud.com/ecs_gls/index.html#'
e = EMDT(url, LOG_ENABLE=False)
e.analyse()
e.format()
for i in e.summery:
    print(i, '\n-------------------------------------------')
```

2. 输入为WEB文档（网页源代码）

```
from EMDT import EMDT
with open('path_of_file', encoding='utf-8', mode='r') as f:
    e = EMDT(f.read())
    e.analyse()
    e.format()
    for i in e.summery:
        log('info', 'summery:{};文件名：{};Tag:{}'.format(i[0]+","+i[1], x, e.tag))
```
## 实例测试

```
# -*- coding: utf-8 -*-
"""
A simple example, have fun!
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

from EMDT import EMDT
import os

if __name__ == "__main__":
    dir = 'support.huaweicloud.com/'
    for x in os.listdir(dir):
        with open(dir + x, encoding='utf-8', mode='r') as f:
            e = EMDT(f.read())
            e.analyse()
            e.format()
            for i in e.summery:
                print(i)

    # url = 'https://support.huaweicloud.com/ecs_gls/index.html#'
    # e = EMDT(url, LOG_ENABLE=False)
    # e.analyse()
    # e.format()
    # for i in e.summery:
    #     print(i, '\n-------------------------------------------')
```


## 输出日志示例
```
2018-06-13 13:31:03,871 - DEBUG - Building prefix dict from the default dictionary ...
2018-06-13 13:31:03,871 - DEBUG - Loading model from cache /tmp/jieba.cache
2018-06-13 13:31:04,405 - DEBUG - Loading model cost 0.534 seconds.
2018-06-13 13:31:04,405 - DEBUG - Prefix dict has been built succesfully.
2018-06-13 13:31:04,509 - INFO - summery:多维交互分析服务 获取日志列表,多维交互分析服务;文件名：support.huaweicloud.com_api-molap_zh-cn_topic_0034789650.html;Tag:1
2018-06-13 13:31:04,509 - INFO - summery:多维交互分析服务 获取日志列表 功能介绍,多维交互分析服务;文件名：support.huaweicloud.com_api-molap_zh-cn_topic_0034789650.html;Tag:1
2018-06-13 13:31:04,509 - INFO - summery:多维交互分析服务 获取日志列表 URL,多维交互分析服务;文件名：support.huaweicloud.com_api-molap_zh-cn_topic_0034789650.html;Tag:1
2018-06-13 13:31:04,509 - INFO - summery:多维交互分析服务 获取日志列表 响应,多维交互分析服务;文件名：support.huaweicloud.com_api-molap_zh-cn_topic_0034789650.html;Tag:1
2018-06-13 13:31:04,509 - INFO - summery:多维交互分析服务 获取日志列表 请求,多维交互分析服务;文件名：support.huaweicloud.com_api-molap_zh-cn_topic_0034789650.html;Tag:1
2018-06-13 13:31:04,509 - INFO - summery:多维交互分析服务 获取日志列表 响应码,多维交互分析服务;文件名：support.huaweicloud.com_api-molap_zh-cn_topic_0034789650.html;Tag:1
2018-06-13 13:31:04,890 - INFO - summery:会议 调试运行,会议;文件名：support.huaweicloud.com_devg-cloudvc_zh-cn_topic_0069399688.html;Tag:3
2018-06-13 13:31:04,890 - INFO - summery:会议 调试运行 鉴权信息,会议;文件名：support.huaweicloud.com_devg-cloudvc_zh-cn_topic_0069399688.html;Tag:3
2018-06-13 13:31:05,045 - INFO - summery:联络中心 外呼相关,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277113.html;Tag:3
2018-06-13 13:31:05,045 - INFO - summery:联络中心 外呼相关 预览释放,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277113.html;Tag:3
2018-06-13 13:31:05,111 - INFO - summery:云监控服务 如何自定义添加监控项?,云监控服务;文件名：support.huaweicloud.com_ces_faq_ces_faq_0007.html;Tag:2
2018-06-13 13:31:05,237 - INFO - summery:云容器引擎 获取集群结点的metrics监控数据,云容器引擎;文件名：support.huaweicloud.com_api-cce_zh-cn_topic_0036216941.html;Tag:3
2018-06-13 13:31:05,237 - INFO - summery:云容器引擎 获取集群结点的metrics监控数据 获取集群结点支持的metrics列表,云容器引擎;文件名：support.huaweicloud.com_api-cce_zh-cn_topic_0036216941.html;Tag:3
2018-06-13 13:31:05,501 - INFO - summery:云审计服务 创建追踪器,云审计服务;文件名：support.huaweicloud.com_api-cts_zh-cn_topic_0044325124.html;Tag:1
2018-06-13 13:31:05,501 - INFO - summery:云审计服务 创建追踪器 功能介绍,云审计服务;文件名：support.huaweicloud.com_api-cts_zh-cn_topic_0044325124.html;Tag:1
2018-06-13 13:31:05,501 - INFO - summery:云审计服务 创建追踪器 返回值,云审计服务;文件名：support.huaweicloud.com_api-cts_zh-cn_topic_0044325124.html;Tag:1
2018-06-13 13:31:05,501 - INFO - summery:云审计服务 创建追踪器 URI,云审计服务;文件名：support.huaweicloud.com_api-cts_zh-cn_topic_0044325124.html;Tag:1
2018-06-13 13:31:05,501 - INFO - summery:云审计服务 创建追踪器 请求,云审计服务;文件名：support.huaweicloud.com_api-cts_zh-cn_topic_0044325124.html;Tag:1
2018-06-13 13:31:05,501 - INFO - summery:云审计服务 创建追踪器 响应,云审计服务;文件名：support.huaweicloud.com_api-cts_zh-cn_topic_0044325124.html;Tag:1
2018-06-13 13:31:05,767 - INFO - summery:虚拟私有云 公共响应消息头,虚拟私有云;文件名：support.huaweicloud.com_api-vpc_zh-cn_topic_0022488528.html;Tag:3
2018-06-13 13:31:05,816 - INFO - summery:多维交互分析服务 M-OLAP与Spark什么关系？,多维交互分析服务;文件名：support.huaweicloud.com_molap_faq_zh-cn_topic_0034878451.html;Tag:2
2018-06-13 13:31:06,105 - INFO - summery:联络中心 文字交谈应答,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 前置条件,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 响应消息,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 示例,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 注意事项,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 接口说明,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 触发事件,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,106 - INFO - summery:联络中心 文字交谈应答 错误结果码,联络中心;文件名：support.huaweicloud.com_api-cloudipcc_zh-cn_topic_0064277329.html;Tag:1
2018-06-13 13:31:06,417 - INFO - summery:弹性伸缩服务 查询伸缩实例挂起信息,弹性伸缩服务;文件名：support.huaweicloud.com_api-as_zh-cn_topic_0043063081.html;Tag:1

```

---
## 作者
Z.S. Peng/[**Ex_treme**](https://pzs741.github.io/)


