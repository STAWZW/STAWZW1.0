# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:23:23 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
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
    occurTime = (datetime.datetime.strptime(occurTimeLan, '%H UTC %d %b %Y')).strftime('%Y-%m-%d %H:%M:%S')
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
    
    try:
        result = {}
        result['disasterid'] = '10107'                                          #类别:雷暴
        result['source'] = '世界天气信息服务网'                                   #新闻来源
        result['link'] = link                                                   #新闻链接
        result['releaseTime'] = occurTime                                       #发布时间
        result['occurTime'] = occurTime                                         #发生时间
        result['latitude'] = latitude                                           #纬度
        result['longitude'] = longitude                                         #经度
        result['strength'] = strength                                           #灾害强度
        result['place'] = place                                                 #发生地点
        result['title'] = title                                                 #新闻标题
        result['originalText'] = ''                                             #新闻内容
        result['injured'] = '0'                                                 #受伤人数
        result['death'] = '0'                                                   #死亡人数
        result['loss'] = '0'                                                    #经济损失
        result['pictures'] = ''                                                 #特殊字段
        result['more'] = ''
        result['regional'] = '国外'
        result['province'] = ''                                                 #灾害发生的一级行政区划
        result['country'] = ''                                                  #灾害发生国家
        result['current_website'] = '世界天气信息服务网'                           #灾害当前网站
        result['isreleasetime'] = '0'                                               #灾害发生时间是否是用发布时间代替
        
        
        resultSun = {}
        resultSun['title'] = result['title']
        resultSun['originalText'] = result['originalText']
        resultSun['pictures'] = result['pictures']
        
        try:
            title = 'rainstorm_ES001'
            res = postgreCommand.insertData(result,resultSun,title)
            if res == 1:
                print(title,'数据插入成功！')
            elif res == 0:
                print(title,'数据更新成功！')
        except Exception as e:
            print("新闻插入数据失败", str(e))
    except:
        print("rainstorm_ES001:当前数据出错")

#-----------------------------------------------------------------------------------------------

def rainstorm_ES001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'https://severe.worldweather.wmo.int/thunder'
        infos_paser_One(url)
    except Exception as e:
        print("rainstorm_ES001访问网站失败", str(e))
    postgreCommand.closePostgre()
#    timrFor = Timer(2*60*60,rainstorm_ES001)
#    timrFor.start()

##--------测试代码-----------
#rainstorm_ES001()


