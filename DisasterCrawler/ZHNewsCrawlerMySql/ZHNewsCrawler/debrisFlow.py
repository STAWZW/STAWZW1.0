#!/usr/bin/env python 
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'

import urllib.request
import ssl
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import fool
import re
import toYc

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('utf-8')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'outer'}, limit=1)
    ul_info_list = div_info_list[0].find_all('ul')
    li_info_list = ul_info_list[0].find_all('li')
    for item in li_info_list:
        analyzeInfo(item)

def analyzeInfo(item):
    address = ''
    result = {}
    a_list = item.find_all('a', limit=1)
    h3_list = item.find_all('h3',attrs={'class': 'tit'},limit=1)
    span_link_list = h3_list[0].find_all('span', limit=1)
    div_list = item.find_all('div', attrs={'class': 'src-tim'}, limit=1)
    span1_list = div_list[0].find_all('span', attrs={'class': 'src'}, limit=1)
    span2_list = div_list[0].find_all('span', attrs={'class': 'tim'}, limit=1)
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0008'     #类别:泥石流
    result['link'] = span_link_list[0]['lanmu1']
    result['title'] = a_list[0].get_text().strip()      #新闻标题
    result['releaseTime'] = re.sub("\D", "", span2_list[0].get_text().strip())        #发布时间
    result['source'] = span1_list[0].get_text().strip().replace('来源：', '')     #新闻来源
    result['originalText'] = get_original(result['link'])       #新闻原文
    title_str = [result['originalText']]
    words, ners = fool.analysis(title_str)
    for itemSun in ners[0]:
        if itemSun[2] == 'location':
            if itemSun[3] in address:
                break
            else:
                address = address + itemSun[3] + ','
    result['place'] = address       #发生地点
    result['longitude'] = '0'     #地点经度
    result['latitude'] = '0'      #地点纬度
    result['strength'] = ''     #灾害强度
    result['occurTime'] = ''     #发生时间
    originalText = result['originalText'] + '，' + result['title']
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    result['injured'] = str(injured)         #受伤人数
    result['death'] = str(death)         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = ''       #多个路径之间用分号隔开
    result['more'] = ''       #特殊字段
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'debrisFlow'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句

def get_original(url):
    textStr = ''
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'cnt_bd'}, limit=1)
    p_info_list = div_info_list[0].find_all('p')
    for item in p_info_list:
        if item.find('script') != None:
            continue
        else:
            textStr = textStr + item.get_text().strip()
    return (textStr)



# ---------------------------------------------------------------

mysqlCommand = MySQLCommand()

class debrisFlow(object):

   def rund(self):
       mysqlCommand.connectMysql()

       url = 'https://search.cctv.com/search.php?qtext=%E6%B3%A5%E7%9F%B3%E6%B5%81&type=web'
       infos_paser(url)

       mysqlCommand.closeMysql()

       a = debrisFlow()
       t = Timer(2*60*60,a.rund)#60秒爬取一次
       t.start()


# --------测试代码-----------
#a = debrisFlow()
#a.rund()



