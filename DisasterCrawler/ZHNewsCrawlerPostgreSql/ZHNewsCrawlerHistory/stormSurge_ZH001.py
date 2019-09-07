#!/usr/bin/env python
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import address
import re
import time

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
        try:
            analyzeInfo(item)
            time.sleep(5)
        except:
            continue

def analyzeInfo(item):
        result = {}
        a_title = item.find_all('a')
        result['disasterid'] = '10201'                                          #新闻类别:风暴潮
        result['link'] = 'http://www.oceanguide.org.cn' + a_title[0]['href']    #新闻标题
        result['title'] = a_title[0].get_text().strip()                         #新闻标题
        time_str1 = re.sub("\D", "", item.find('p').get_text().strip())
        datetime_struct1 = parser.parse(time_str1)
        releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
        result['releaseTime'] = releaseTime                                     #发布时间
        result['originalText'] = get_original(result['link'])                   #新闻原文
        result['source'] = get_source(result['link'])                           #新闻来源
        originalText = result['originalText'] + '，' + result['title']
        latlngadd_tuple = address.placeMany(originalText)
        result['place'] = latlngadd_tuple[0]                                    #发生地点
        result['longitude'] = str(latlngadd_tuple[1])                           #地点经度
        result['latitude'] = str(latlngadd_tuple[2])                            #地点纬度
        result['strength'] = ''                                                 #灾害强度
        result['occurTime'] = releaseTime                                       #发生时间
        result['injured'] = '0'                                                 #受伤人数
        result['death'] = '0'                                                   #死亡人数
        result['loss'] = '0'                                                    #经济损失
        result['pictures'] = ''                                                 #多个路径之间用分号隔开
        result['more'] = ''                                                     #特殊字段
        result['regional'] = '国内'
        result['province'] = latlngadd_tuple[3]                                 #灾害发生的一级行政区划
        result['country'] = latlngadd_tuple[4]                                  #灾害发生国家
        result['current_website'] = '中国海洋预报网'                              #灾害当前网站
        result['isreleasetime'] = '0'                                               #灾害发生时间是否是用发布时间代替
        
        resultSun = {}
        resultSun['title'] = result['title']
        resultSun['originalText'] = result['originalText']
        resultSun['pictures'] = result['pictures']
        
        try:
            title = 'stormSurge_ZH001'
            res = postgreCommand.insertData(result,resultSun,title)
            if res == 1:
                print(title,'数据插入成功！')
            elif res == 0:
                print(title,'数据更新成功！')
        except Exception as e:
            print("插入数据失败", str(e))


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

def stormSurge_ZH001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://www.oceanguide.org.cn/hyyj/map/boreList.htm?type=storm'
        infos_paser(url)
    except Exception as e:
        print("stormSurge_ZH001访问网站失败", str(e))
    postgreCommand.closePostgre()

# --------测试代码-----------
#stormSurge_ZH001()


