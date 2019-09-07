# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:11:21 2019

@author: Administrator
"""

import urllib.request
from postgres import PostgreCommand
from threading import Timer
from dateutil import parser
import re
import json

def get_html(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    address = re.findall(r'typhoonList":(.+?)}',html)
    dataJson = json.loads(address[0])
    for item in dataJson:
        analyzeInfo(item)

def analyzeInfo(item):
    linkId = str(item[0])
    link = 'http://typhoon.nmc.cn/weatherservice/typhoon/jsons/view_' + linkId + '?t=155748' + linkId + '&callback=typhoon_jsons_view_' + linkId
    dataTyphoon = get_htmlsun(link)
    dataLen = len(dataTyphoon['typhoon'][8])
    if dataTyphoon['typhoon'][8][dataLen - 1][12] == None:                      #发生时间
        occurTimeSun = (dataTyphoon['typhoon'][8][dataLen - 1])[1]
    else:
        occurTimeSun = dataTyphoon['typhoon'][8][dataLen - 1][12][2]
    longitude = str((dataTyphoon['typhoon'][8][dataLen - 1])[4])                #经度
    latitude = str((dataTyphoon['typhoon'][8][dataLen - 1])[5])                 #纬度
    strength = str((dataTyphoon['typhoon'][8][dataLen - 1])[3])                 #强度
    
    datetime_struct1 = parser.parse(occurTimeSun)
    releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    wind = (dataTyphoon['typhoon'][8][dataLen - 1])[8]                          #风向
    WindSpeed = str((dataTyphoon['typhoon'][8][dataLen - 1])[7])                #风速
    CenterPressure = str((dataTyphoon['typhoon'][8][dataLen - 1])[6])           #中心气压
    movingSpeed = str((dataTyphoon['typhoon'][8][dataLen - 1])[9])              #移动速度
    
    original = json.dumps(dataTyphoon, ensure_ascii=False)
    originalText = original.replace(' ','').replace('\n','').replace('\r', '').replace('"', '’')

    result = {}
    result['disasterid'] = '10102'                                              #类别
    result['title'] = str(item[2]) + '台风'                                      #标题
    result['releaseTime'] = releaseTime                                         #发布时间
    result['originalText'] = originalText                                       #新闻原文
    result['source'] = '中央气象台台风网'                                         #新闻来源
    result['link'] = 'http://typhoon.nmc.cn/web.html'                           #新闻链接
    result['place'] = latitude + 'N/' + longitude + 'E'                         #发生地点
    result['longitude'] = longitude                                             #地点经度
    result['latitude'] = latitude                                               #地点纬度
    result['strength'] = strength                                               #灾害强度
    result['occurTime'] = releaseTime                                           #发生时间
    result['injured'] = '0'                                                     #受伤人数
    result['death'] = '0'                                                       #死亡人数
    result['loss'] = '0'                                                        #经济损失
    result['pictures'] = ''                                                     #多个路径之间用分号隔开
    specialData = '{风向: ' + wind + ', 最大风速: ' + WindSpeed + 'm/s, 中心气压: ' + CenterPressure + '百帕, 移动速度: ' + movingSpeed + 'km/h}'
    result['more'] = specialData                                                #特殊字段
    result['regional'] = '国内'
    result['province'] = ''                                                     #灾害发生的一级行政区划
    result['country'] = ''                                                      #灾害发生国家
    result['current_website'] = '中央气象台台风网'                                #灾害当前网站
    result['isreleasetime'] = '0'                                               #灾害发生时间是否是用发布时间代替
    
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']

    try:
        title = 'typhoon_ZH001'
        res = postgreCommand.insertData(result,resultSun,title)
        if res == 1:
            print(title,'数据插入成功！')
        elif res == 0:
            print(title,'数据更新成功！')
    except Exception as e:
        print("插入数据失败", str(e))

def get_htmlsun(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('utf-8')
    address = re.findall(r'[(](.+?)[)]',html)
    dataJson = json.loads(address[0])
    return dataJson

# ---------------------------------------------------------------

def typhoon_ZH001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://typhoon.nmc.cn/weatherservice/typhoon/jsons/list_2019?t=1557472608958&callback=typhoon_jsons_list_2019'
        get_html(url)
    except Exception as e:
        print("typhoon_ZH001访问网站失败", str(e))
    postgreCommand.closePostgre()
#    timrFor = Timer(2*60*60,typhoon_ZH001)
#    timrFor.start()

# --------测试代码-----------
#typhoon_ZH001()





