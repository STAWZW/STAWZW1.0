# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:19:41 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import datetime
import time
import json
import re
import hashlib
import random
import requests
import spiderConfig
from threading import Timer

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    return html

def infos_paser(url,delay):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    dataString = soup.get_text()
    dataJson = json.loads(dataString)
    dataList = dataJson['features']
    for item in dataList:
        analyzeInfo(item)

def analyzeInfo(item):
        result = {}
        properties = item['properties']
        geometry = item['geometry']
        result['disasterid'] = '10010'                                          #类别:地震
        result['source'] = '美国地震信息中心'                                     #新闻来源
        result['link'] = properties['url']                                      #新闻链接
        result['releaseTime'] = timeConversion(properties['updated'])           #发布时间
        result['occurTime'] = timeConversion(properties['time'])                #发生时间
        result['latitude'] = str(geometry['coordinates'][1])                    #纬度
        result['longitude'] = str(geometry['coordinates'][0])                   #经度
        result['strength'] = str(properties['mag']) + 'M'                       #灾害强度
        result['place'] = translate(properties['place'])                        #发生地点
        result['title'] = translate(properties['title'])                        #新闻标题
        result['originalText'] = result['title']                                #新闻内容
        result['injured'] = '0'                                                 #受伤人数
        result['death'] = '0'                                                   #死亡人数
        result['loss'] = '0'                                                    #经济损失
        result['pictures'] = ''
        depth = str(geometry['coordinates'][2])
        specialData = '{震源深度: ' + depth + 'km}'                              #震源深度
        result['more'] = specialData
        result['regional'] = '国外'
        result['province'] = ''                                                 #灾害发生的一级行政区划
        result['country'] = ''                                                  #灾害发生国家
        result['current_website'] = '美国地震信息中心'                            #灾害当前网站
        result['isreleasetime'] = '0'                                           #灾害发生时间是否是用发布时间代替
        result['isrellonandlat'] = '1'
        resultSun = {}
        resultSun['title'] = result['title']
        resultSun['originalText'] = result['originalText']
        resultSun['pictures'] = result['pictures']
        try:
            title = 'earthquake_ES001'
            res = postgreCommand.insertData(result,resultSun,title)
            if res == 1:
                print(title,'数据插入成功！')
            elif res == 0:
                print(title,'数据更新成功！')
        except Exception as e:
            print("新闻插入数据失败", str(e))

def timeConversion(timeData):
    timeStamp = timeData/1000
    timePeriod = time.localtime(timeStamp)
    timeLocalStr = time.strftime('%Y%m%d%H%M%S', timePeriod)
    timeLocalDate = datetime.datetime.strptime(timeLocalStr,'%Y%m%d%H%M%S')
    timeLink = time.mktime(timeLocalDate.timetuple())
    timeUTC = datetime.datetime.utcfromtimestamp(timeLink)
    timeUtcStr = re.sub("\D", "", str(timeUTC))
    datetime_struct2 = parser.parse(timeUtcStr)
    printTime = datetime_struct2.strftime('%Y-%m-%d %H:%M:%S')
    return printTime

def translate(content):
    apiurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    appid = '20190730000322586'
    secretKey = 'df2vBgyHUCkAUDP6BDwM'
    salt = str(random.randint(32768, 65536))
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    try:
        paramas = {
            'appid': appid,
            'q': content,
            'from': 'en',
            'to': 'zh',
            'salt': salt,
            'sign': sign
        }
        response = requests.get(apiurl, paramas)
        jsonResponse = response.json()
        if "trans_result" in jsonResponse.keys():
            dst = str(jsonResponse["trans_result"][0]["dst"])
        else:
            dst = content
        return dst
    except Exception as e:
        print(e)
        return content

#-----------------------------------------------------------------------------------------------
def earthquake_ES001():
    result = spiderConfig.spiderConfig('earthquake_ES001')
    if result['status'] == '1':
        frequency = int(result['frequency'])
        delay = int(result['delay'])
        global postgreCommand
        postgreCommand = PostgreCommand()
        postgreCommand.connectPostgre()
        try:
            url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'
            infos_paser(url,delay)
        except Exception as e:
            print("earthquake_ES001访问网站失败", str(e))
        postgreCommand.closePostgre()
        timrFor = Timer(frequency*60*60,earthquake_ES001)
        timrFor.start()
    else:
        print('earthquake_ES001爬虫停止')
        timrFor = Timer(1*60*60,earthquake_ES001)
        timrFor.start()

#--------测试代码-----------
#earthquake_ES001()
