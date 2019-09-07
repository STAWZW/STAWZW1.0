#!/usr/bin/env python 
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import address
import time
import re
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
        try:
            analyzeInfo(item)
            time.sleep(5)
        except:
            continue

def analyzeInfo(item):
    result = {}
    a_title = item.find_all('a')
    result['disasterid'] = '10002'                                              #类别:滑坡
    result['link'] = 'http://www.cibeicn.com' + a_title[0]['href']              #新闻链接
    analyze = analyzeInfoSun(result['link'])
    result['originalText'] = analyze[0]                                         #新闻原文
    result['source'] = analyze[1]                                               #新闻来源
    time_str1 = re.sub("\D", "", analyze[2])
    datetime_struct1 = parser.parse(time_str1)
    releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    result['releaseTime'] = releaseTime                                         #发布时间
    strong_info_list = item.find('strong')
    if strong_info_list == None:
        a_info_list = a_title[0].get_text().strip()
        result['title'] = a_info_list                                           #新闻标题
    else:
        result['title'] = strong_info_list.get_text().strip()
    originalText = result['title'] + '，' + result['originalText']
    latlngadd_tuple = address.placeSingle(originalText)
    result['place'] = latlngadd_tuple[0]                                        #发生地点
    result['longitude'] = str(latlngadd_tuple[1])                               #地点经度
    result['latitude'] = str(latlngadd_tuple[2])                                #地点纬度
    result['strength'] = ''                                                     #灾害强度
    result['occurTime'] = result['releaseTime']                                 #发生时间
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    lossNumber = toYc.loss(originalText)
    result['loss'] = str(lossNumber)                                            #经济损失
    result['injured'] = str(injured)                                            #受伤人数
    result['death'] = str(death)                                                #死亡人数
    result['pictures'] = ''                                                     #多个路径之间用分号隔开
    result['more'] = ''                                                         #特殊字段
    result['regional'] = '国内'
    result['province'] = latlngadd_tuple[3]                                     #灾害发生的一级行政区划
    result['country'] = latlngadd_tuple[4]                                      #灾害发生国家
    result['current_website'] = '防灾网'                                         #灾害当前网站
    result['isreleasetime'] = '1'                                               #灾害发生时间是否是用发布时间代替
    result['isrellonandlat'] = '0'
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    try:
        title = 'landslide_ZH001'
        res = postgreCommand.insertData(result,resultSun,title)
        if res == 1:
            print(title,'数据插入成功！')
        elif res == 0:
            print(title,'数据更新成功！')
    except Exception as e:
        print("插入数据失败", str(e))

def analyzeInfoSun(url):
    textList = []
    textStr = ''
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'id': 'result'}, limit=1)
    p_info_list = div_info_list[0].find_all('p')
    for item in p_info_list:
        textList.append(item.get_text().strip())
    textStr = ''.join(textList)
    span_info_list = soup.find_all('span', attrs={'id': 'source'}, limit=1)
    source = (span_info_list[0].get_text()).replace('来源：', '')
    span_info_list = soup.find_all('span', attrs={'id': 'showtime'}, limit=1)
    releaseTime = span_info_list[0].get_text()
    return textStr,source,releaseTime

# ---------------------------------------------------------------

def landslide_ZH001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://www.cibeicn.com/topic/list.aspx?key=%E6%BB%91%E5%9D%A1'
        infos_paser(url)
    except Exception as e:
        print("landslide_ZH001访问网站失败", str(e))
    postgreCommand.closePostgre()

# --------测试代码-----------
#landslide_ZH001()
