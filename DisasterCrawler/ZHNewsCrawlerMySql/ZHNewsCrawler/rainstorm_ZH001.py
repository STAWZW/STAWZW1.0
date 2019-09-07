#!/usr/bin/env python 
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'


#暴雨爬取
import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import re
import cpca
import requests
import toYc

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'newtest'}, limit=1)

    p_info_list = div_info_list[0].find_all('p', attrs={'class': 'p8'})
    for item in p_info_list:
        analyzeInfo_one(item)

def analyzeInfo_one(item):
    result = {}
    a_title = item.find_all('a')
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0006'     #类别:暴雨
    result['link'] = 'http://www.cibeicn.com' + a_title[0]['href']      # 新闻链接
    source = get_source(result['link'])
    result['source'] = re.findall(r'来源：(.+)',source)[0]      #新闻来源
    result['originalText'] = get_original(result['link'])       # 新闻原文
    release = get_releaseTime(result['link'])
    releaseTime = re.sub("\D", "", release)
    result['releaseTime'] = releaseTime          # 发布时间
    strong_info_list = item.find('strong')
    if strong_info_list == None:
        a_info_list = a_title[0].get_text().strip()
        result['title'] = a_info_list                   # 标题
    else:
        result['title'] = strong_info_list.get_text().strip()
    title_str = [result['originalText']]
    df = cpca.transform(title_str)
    place = df.values
    result['place'] = place[0][0] + place[0][1] + place[0][2]       #发生地点
    if result['place'] != '':
        llat = geocode(result['place'])
        result['longitude'] = llat[0]     #地点经度
        result['latitude'] = llat[1]      #地点纬度
    else:
        result['longitude'] = '0'
        result['latitude'] = '0'
    result['strength'] = '暴雨'    #灾害强度
    result['occurTime'] = ''     #发生时间
    originalText = result['originalText'] + result['title']
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    result['injured'] = str(injured)         #受伤人数
    result['death'] = str(death)         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = ''       #多个路径之间用分号隔开
    result['more'] = ''       #特殊字段
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'rainstorm_ZH001'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句
    

def get_original(url):
    textStr = ''
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    result_info_list = soup.find_all('div', attrs={'id': 'result'}, limit=1)
    divs_info_list = result_info_list[0].find_all('div')       #文本结构不同采用两种标签
    for item in divs_info_list:
        textStr = textStr + item.get_text().strip()
    p_info_list = result_info_list[0].find_all('p')
    for item in p_info_list:
        textStr = textStr + item.get_text().strip()
    return (textStr)

def get_source(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    span_info_list = soup.find_all('span', attrs={'id': 'source'}, limit=1)
    return (span_info_list[0].get_text())

def get_releaseTime(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    span_info_list = soup.find_all('span', attrs={'id': 'showtime'}, limit=1)
    return (span_info_list[0].get_text())

def geocode(address):
    parameters = {'address': address, 'key': 'f6922b393df061ffff5b3c61529ce7d0'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    jwd = (answer['geocodes'][0]['location']).split(',')
    return jwd

# ---------------------------------------------------------------

mysqlCommand = MySQLCommand()

class rainstorm_ZH001(object):

   def rund(self):
       mysqlCommand.connectMysql()
       try:
           url = 'http://www.cibeicn.com/topic/list.aspx?key=%E6%9A%B4%E9%9B%A8&pageIndex=1'
           infos_paser(url)
       except Exception as e:
           print("访问网站失败", str(e))#输出插入失败的报错语句
       mysqlCommand.closeMysql()

       a = rainstorm_ZH001()
       t = Timer(2*60*60,a.rund)#60秒爬取一次
       t.start()


# --------测试代码-----------
#a = rainstorm_ZH001()
#a.rund()


