#!/usr/bin/env python 
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'

import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import re

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    ul_info_list = soup.find_all('ul', attrs={'class': 'boreList'}, limit=1)
    li_info_list = ul_info_list[0].find_all('li')
    for item in li_info_list:
        analyzeInfo(item)

def analyzeInfo(item):
    result = {}
    a_title = item.find_all('a')
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0004'     #新闻类别:海啸
    result['link'] = 'http://www.oceanguide.org.cn' + a_title[0]['href']        #新闻链接
    result['originalText'] = get_original(result['link'])       #新闻原文
    result['source'] = get_source(result['link'])       #新闻来源
    result['title'] = a_title[0].get_text().strip()     #新闻标题
    time = re.sub("\D", "", item.find('p').get_text().strip())
    timeList = list(time)
    if timeList[4] != '1':
        timeList.insert(4, '0')
    releaseTime = ''.join(timeList)
    result['releaseTime'] = releaseTime       #发布时间
    address = (re.findall(r"发布(.+?)海域地震海啸信息",result['title']))
    result['place'] = address[0]        #发生地点
    rule = re.compile(r'[（](.*?)[）]', re.S)
    landl = re.findall(rule, result['originalText'])
    landlList = landl[1].split(',')
    result['longitude'] = landlList[1][:-1].replace(' ','')     #地点经度
    result['latitude'] = landlList[0][:-1].replace(' ','')      #地点纬度
    result['strength'] = ''     #灾害强度
    result['occurTime'] = releaseTime     #发生时间
    result['injured'] = '0'         #受伤人数
    result['death'] = '0'         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = ''       #多个路径之间用分号隔开
    result['more'] = ''       #特殊字段
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'tsunami'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句

def get_original(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'forecastSpecific'}, limit=1)
    p_info_list = div_info_list[0].find_all('p', attrs={'class': 'forCon'}, limit=1)
    return (p_info_list[0].get_text())

def get_source(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'forecastSpecific'}, limit=1)
    divs_info_list = div_info_list[0].find_all('div', attrs={'style': 'position:relative;'}, limit=1)
    p_info_list = divs_info_list[0].find_all('p')
    ps_info_list = p_info_list[1].find_all('span')
    return (ps_info_list[0].get_text())

# ---------------------------------------------------------------

mysqlCommand = MySQLCommand()

class tsunami(object):

   def rund(self):
       mysqlCommand.connectMysql()

       url = 'http://www.oceanguide.org.cn/hyyj/map/boreList.htm?type=bore'
       infos_paser(url)

       mysqlCommand.closeMysql()

       a = tsunami()
       t = Timer(2*60*60,a.rund)#60秒爬取一次
       t.start()

# --------测试代码-----------
#a = tsunami()
#a.rund()


