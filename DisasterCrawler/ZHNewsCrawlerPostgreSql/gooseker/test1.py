# -*- coding: utf-8 -*-
# 使用GsExtractor类的示例程序
# 以webdriver驱动Firefox采集亚马逊商品列表
# xslt保存在xslt_bbs.xml中
# 采集结果保存在third文件夹中
import os
import time
from lxml import etree
from selenium import webdriver
from gooseeker import GsExtractor

# 引用提取器
bbsExtra = GsExtractor()   
bbsExtra.setXsltFromAPI("a0056d16ff3003ae9d5b48bcfa54f4af", "newsCrawler") # 设置xslt抓取规则

# 创建存储结果的目录
current_path = os.getcwd()
res_path = current_path + "/third-result"
if os.path.exists(res_path):
    pass
else:
    os.mkdir(res_path)

# 驱动火狐
driver = webdriver.Firefox()
url = "https://www.amazon.cn/s/ref=sr_pg_1?rh=n%3A658390051%2Cn%3A!658391051%2Cn%3A658414051%2Cn%3A658810051&page=1&ie=UTF8&qid=1476258544"
driver.get(url)
time.sleep(2)

# 获取网页内容
content = driver.execute_script("return document.documentElement.outerHTML")#page_source.encode('utf-8')

# 获取docment
doc = etree.HTML(content)
# 调用extract方法提取所需内容
result = bbsExtra.extract(doc)

# 保存结果
file_path = res_path + "/page-" + str(page) + ".xml"
open(file_path,"wb").write(result)
print('第' + str(page) + '页采集完毕，文件:' + file_path)
driver.quit()