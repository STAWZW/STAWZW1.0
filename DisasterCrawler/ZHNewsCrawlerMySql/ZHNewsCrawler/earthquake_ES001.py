# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:19:41 2019

@author: Administrator
"""
#网页地址：https://earthquake.usgs.gov/earthquakes/map/



import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import datetime
import time
import json
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
    dataString = soup.get_text()
    dataJson = json.loads(dataString)
    dataList = dataJson['features']
    #print(dataList[0])
    for item in dataList:
        analyzeInfo(item)

def analyzeInfo(item):
    result = {}
    properties = item['properties']
    geometry = item['geometry']
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0002'     #类别:地震
    result['source'] = '美国地震信息中心'      #新闻来源
    result['link'] = properties['url']      #新闻链接
    result['releaseTime'] = timeConversion(properties['updated'])       #发布时间
    result['occurTime'] = timeConversion(properties['time'])        #发生时间
    result['latitude'] = str(geometry['coordinates'][1])        #纬度
    result['longitude'] = str(geometry['coordinates'][0])       #经度
    result['strength'] = str(properties['mag']) + 'M'       #灾害强度
    result['place'] = properties['place']       #发生地点
    result['title'] = properties['title']       #新闻标题
    result['originalText'] = result['title']        #新闻内容
    result['injured'] = '0'         #受伤人数
    result['death'] = '0'         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = ''
    depth = str(geometry['coordinates'][2])
    specialData = '{震源深度: ' + depth + 'km}'         #震源深度
    result['more'] = specialData
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'earthquake_ES001'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("新闻插入数据失败", str(e))#输出插入失败的报错语句

def timeConversion(timeData):
    timeStamp = timeData/1000
    timePeriod = time.localtime(timeStamp)
    timeLocalStr = time.strftime('%Y%m%d%H%M%S', timePeriod)
    timeLocalDate = datetime.datetime.strptime(timeLocalStr,'%Y%m%d%H%M%S')
    timeLink = time.mktime(timeLocalDate.timetuple())
    timeUTC = datetime.datetime.utcfromtimestamp(timeLink)
    timeUtcStr = re.sub("\D", "", str(timeUTC))
    return timeUtcStr

#-----------------------------------------------------------------------------------------------
        
mysqlCommand = MySQLCommand()

class earthquake_ES001(object):

    def rund(self):
        mysqlCommand.connectMysql()
        try:
            url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'
            infos_paser(url)
        except Exception as e:
           print("访问网站失败", str(e))#输出插入失败的报错语句

        mysqlCommand.closeMysql()

        a = earthquake_ES001()
        t = Timer(2*60*60,a.rund)#60秒爬取一次
        t.start()


##--------测试代码-----------
#a = earthquake_ES001()
#a.rund()


