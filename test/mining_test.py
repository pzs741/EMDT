# -*- coding: utf-8 -*-
"""
extraction_test.py unit test.
"""

__title__ = 'EMDT'
__author__ = 'Ex_treme'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018, Ex_treme'

from EMDT.mining import MineByTag

if __name__ == "__main__":
    content = """                    
                    </div>
                    <div class="help-main">
                        <div class="crumbs"></div>

                        <div class="helpContent">
                            <div class="help-details webhelp" style=""><a name="ZH-CN_TOPIC_0025000762"></a> <a name="ZH-CN_TOPIC_0025000762"></a> 
    <h1 class="topictitle1">
    	上云迁移解决方案 FAQ
    </h1>
    <div id="body52579650">
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p8622890">
    		Q：什么是P2V和V2V？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p10497152">
    		A：P2V即Physical to Virtual的缩写，指迁移物理服务器上的操作系统及其上的应用软件和数据到华为云平台虚拟服务器中。V2V即Virtual to Virtual的缩写，是在虚拟机之间移动操作系统和数据。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p27365507">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p44962972">
    		Q：什么是上云迁移服务？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p2013564">
    		A：华为上云迁移服务提供的是将客户物理服务器上或其他虚拟化平台上的业务系统迁移至华为虚拟化平台上的服务，是一种能将客户应用级业务、文件级业务以及系统级业务迁移到华为虚拟化平台上并正常运行的完整的交付方案。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p18122076">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p28880957">
    		Q：影响迁移效率的主要因素有什么？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p58602024">
    		A：专线网络带宽及网络质量、迁移源主机和目的虚拟机的磁盘IO、迁移数据总量大小、源主机和目的主机性能（如：CPU、内存等）。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p57656175">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p49143529">
    		Q：如何计算业务中断时间？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p39638585">
    		A：停机时间 = 最后一次数据增量同步时间 + 业务切换时间
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p21202951">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p56608836">
    		Q：什么时候适宜块级迁移，什么时候适宜文件级迁移？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p39717481">
    		A：
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p39717481">
    		块级迁移适用场景：
    	</p>
    	<ol id="ZH-CN_TOPIC_0025000762__ol62999416">
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			包含大量小文件的主机；
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			磁盘使用率高的主机；
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			Windows在线迁移，注重成功率用块级；
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			需要保持分区结构与源端完全一致。
    		</li>
    	</ol>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p39717481">
    		文件级迁移适用场景：
    	</p>
    	<ol id="ZH-CN_TOPIC_0025000762__ol62999416">
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			规划的目的VM磁盘空间大小相对于源端进行扩容或者减容；
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			只迁移部分数据文件，排除部分不迁移的文件；
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			Windows在线迁移，注重效率使用文件级。
    		</li>
    	</ol>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p30123835">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p2679067">
    		Q：设定迁移批次的最佳原则是什么？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p24111608">
    		A：首先对业务迁移的关联性进行考虑，其次对业务迁移的迁移风险进行考虑，最后考虑迁移目标值，据此得出业务迁移顺序。一般情况下，由于客户的应用系统及设备数量众多，且各应用系统的重要程度、服务时段、依赖的设备情况等各不相同，因而建议采用分批次逐步迁移的方案，依据如下原则对设备进行分批次迁移：
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p24111608">
    		1）先易后难。对于相对独立，关联系统少的应用，迁移到新的数据中心机房后，容易恢复正常运行。这类应用的迁移较为容易，可优先进行。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p24111608">
    		2）先普通业务系统，后核心业务系统。普通业务系统在迁移过程中出现问题，对公司日常经营活动造成的影响较小，可优先进行，为核心业务系统的迁移积累经验并验证迁移计划。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p24111608">
    		3）选择周末或节假日进行迁移。迁移前后需进行大量准备工作，迁移后需要进行大量测试工作，因而选择周末或节假日能使得迁移作具备充裕的时间，同时避免对日常业务工作造成影响。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p15677883">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p6883221">
    		Q：业务会长时间中断吗？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p61948991">
    		A：对业务连续性要求高的迁移，可以采用在线迁移的方式 ，并且选择选在业务量最低时进行业务切换，最大幅度降低业务切换对客户感受的影响。
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p20670010">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p51812368">
    		Q：哪些情景需要FusionSphere业务迁移？
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p63658128">
    		A：通常，有以下几种情景需要提供业务迁移服务：
    	</p>
    	<ol id="ZH-CN_TOPIC_0025000762__ol62999416">
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			原业务平台即将过保/已过保，拟采购华为虚拟化平台的情景
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			原业务平台空间已无法再次扩容，通过购买华为虚拟化平台提供更大容量空间的情景
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			原业务平台性能已不能满足业务需要，购买华为虚拟化平台来提升性能的场景
    		</li>
    		<li id="ZH-CN_TOPIC_0025000762__li3454809">
    			数据中心虚拟化资源池建设，需要对整体架构重新设计时
    		</li>
    	</ol>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p56034750">
    		<br />
    	</p>
    	<p class="msonormal" id="ZH-CN_TOPIC_0025000762__p34550710">
    		Q：华为云迁移都支持什么场景？
    """
    m = MineByTag(content)
    # m = MineByDensity(content)
    m.qa_mine()
    m.get_qa()
    for i in m.qa:
        print(i)
