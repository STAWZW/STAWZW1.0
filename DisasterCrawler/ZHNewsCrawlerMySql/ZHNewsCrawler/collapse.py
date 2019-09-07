#!/usr/bin/env python 
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'

import urllib.request
import ssl
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import re
import toYc
import fool

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
    result = {}
    address =''
    a_list = item.find_all('a', limit=1)
    h3_list = item.find_all('h3',attrs={'class': 'tit'},limit=1)
    span_link_list = h3_list[0].find_all('span', limit=1)
    div_list = item.find_all('div', attrs={'class': 'src-tim'}, limit=1)
    span2_list = div_list[0].find_all('span', attrs={'class': 'tim'}, limit=1)
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0010'     #新闻类别:崩塌
    result['link'] = span_link_list[0]['lanmu1']
    result['title'] = a_list[0].get_text().strip()
    result['releaseTime'] = re.sub('\D', '', span2_list[0].get_text().strip())
    result['source'] = get_source(result['link'])
    result['originalText'] = get_originalText(result['link'])
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
        title = 'collapse'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句

def get_source(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'cnt_bd'}, limit=1)
    span_info_list = div_info_list[0].find_all('span', attrs={'class': 'info'}, limit=1)
    i_info_list = span_info_list[0].find_all('i')
    return i_info_list[0].get_text().strip()[3:7]

def get_originalText(url):
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
    return (textStr)[4:]



# ---------------------------------------------------------------

mysqlCommand = MySQLCommand()

class collapse(object):

   def rund(self):
       mysqlCommand.connectMysql()
       
       try:
           url = 'https://search.cctv.com/search.php?qtext=%E5%B1%B1%E4%BD%93%E5%B4%A9%E5%A1%8C&type=web#'
           infos_paser(url)
       except Exception as e:
           print("访问网站失败", str(e))#输出插入失败的报错语句

       mysqlCommand.closeMysql()

       a = collapse()
       t = Timer(2*60*60,a.rund)#60秒爬取一次
       t.start()


# --------测试代码-----------
#a = collapse()
#a.rund()


