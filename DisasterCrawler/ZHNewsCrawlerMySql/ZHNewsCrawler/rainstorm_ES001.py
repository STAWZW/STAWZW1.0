# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:23:23 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import datetime
import re

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    return html

def infos_paser_One(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    map_info_list = soup.find('map', attrs={'name' : 'map1'})
    area_info_list = map_info_list.find_all('area')
    for item in area_info_list:
        analyze_Info_One(item)

def analyze_Info_One(item):
    linkSegment = item['href'].strip('.')
    linkTitle = (re.findall(r"/(.+?)/index",linkSegment))[0]
    link = 'https://severe.worldweather.wmo.int/thunder' + linkSegment
    infos_paser_Two(link,linkTitle)

def infos_paser_Two(link,linkTitle):
    htmlCode = get_html(link)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    map_info_list = soup.find('map', attrs={'name' : linkTitle})
    area_info_list = map_info_list.find_all('area')
    for item in area_info_list:
        analyze_Info_Two(item, link)

def analyze_Info_Two(item, link):
    linkSegment = item['href']
    linkTitle = (re.findall(r"(.+?)/index",link))[0]
    linkSun = (re.findall(r"'.(.+?)','s",linkSegment))[0]
    link = linkTitle + linkSun
    infos_paser_Three(link)

def infos_paser_Three(link):
    htmlCode = get_html(link)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    table_info_list = soup.find('table')
    tr_info_list = table_info_list.find_all('tr')
    for item in tr_info_list:
        if item == None:
            continue
        analyze_Info_Three(item, link)
def analyze_Info_Three(item, link):
    div_info_list = item.find_all('div', attrs={'class' : 'coordinate'}, limit = 2)
    title = div_info_list[0].get_text()
    newsData = div_info_list[1].get_text().replace('\n','|')
    newsList = newsData.split('|')
    newsDataList = list(filter(None, newsList))
    dataLen = len(newsDataList)
    if dataLen== 3:
        latlonStr = newsDataList[0]
        place = ''
        occurTimeStr = newsDataList[1] + '-'
        strength = newsDataList[2]
    else:
        latlonStr = newsDataList[0]
        place = newsDataList[1]
        occurTimeStr = newsDataList[2] + '-'
        strength = newsDataList[3]
    occurTimeLan = re.findall(r"at (.+?)-",occurTimeStr)[0]
    occurTime = (datetime.datetime.strptime(occurTimeLan, '%H UTC %d %b %Y')).strftime('%Y%m%d%H%M%S')
    latlon = (re.findall(r"[(](.+?)[)]", latlonStr)[0]).split()
    if latlon[0][-1] == 'S':
        latitude = '-' + latlon[0][:-1]
    else:
        latitude = latlon[0][:-1]
    if latlon[1][-1] == 'W':
        longitude = '-' + latlon[1][:-1]
    else:
        longitude = latlon[1][:-1]
    title = title + place + strength     
    
        
    result = {}
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0006'     #类别:雷暴
    result['source'] = '世界天气信息服务'      #新闻来源
    result['link'] = link      #新闻链接
    result['releaseTime'] = occurTime       #发布时间
    result['occurTime'] = occurTime      #发生时间
    result['latitude'] = latitude        #纬度
    result['longitude'] = longitude       #经度
    result['strength'] = strength       #灾害强度
    result['place'] = place       #发生地点
    result['title'] = title       #新闻标题
    result['originalText'] = ''       #新闻内容
    result['injured'] = '0'         #受伤人数
    result['death'] = '0'         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = ''         #特殊字段
    result['more'] = ''
    
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'rainstorm_ES001'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("新闻插入数据失败", str(e))#输出插入失败的报错语句

#-----------------------------------------------------------------------------------------------

mysqlCommand = MySQLCommand()

class rainstorm_ES001(object):

    def rund(self):
        mysqlCommand.connectMysql()
        try:
            url = 'https://severe.worldweather.wmo.int/thunder'
            infos_paser_One(url)
        except Exception as e:
            print("访问网站失败", str(e))#输出插入失败的报错语句

        mysqlCommand.closeMysql()

        a = rainstorm_ES001()
        t = Timer(4*60*60,a.rund)#60秒爬取一次
        t.start()


##--------测试代码-----------
#a = rainstorm_ES001()
#a.rund()

#url = 'https://severe.worldweather.wmo.int/thunder'
#infos_paser_One(url)





