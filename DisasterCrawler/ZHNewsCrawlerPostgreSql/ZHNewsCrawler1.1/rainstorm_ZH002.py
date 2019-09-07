# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:49:30 2019

@author: 86183
"""

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import address
import time
import toYc
import re
import spiderConfig
from threading import Timer

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('gbk')
    return html

def infos_paser(url,delay):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find('div', attrs={'class': 'list_R pdR26'})
    ul_info_list = div_info_list.find('ul')
    li_info_list = ul_info_list.find_all('li')
    for item in li_info_list:
        try:
            analyzeInfo_One(item)
            time.sleep(delay)
        except:
            continue

def analyzeInfo_One(item):
    result = {}
    divs = item.find_all('div')
    title = divs[0].find('a').get_text().strip()
    link = 'http://www.qxkp.net' + divs[0].find('a')['href']
    time_str1 = re.sub("\D", "", divs[1].get_text())
    datetime_struct1 = parser.parse(time_str1)
    releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    result['disasterid'] = '10107'                                              #类别:暴雨
    result['link'] = link                                                       # 新闻链接
    resultSun = analyzeInfo_Two(link)
    result['source'] = resultSun['source']                                      #新闻来源
    result['originalText'] = resultSun['originalText']                          # 新闻原文
    result['releaseTime'] = releaseTime                                         # 发布时间
    result['title'] = title                                                     # 标题
    originalText = result['title'] + '，' + result['originalText']
    latlngadd_tuple = address.placeMany(originalText)
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
    result['pictures'] = resultSun['pictures']                                  #多个路径之间用分号隔开
    result['more'] = ''                                                         #特殊字段
    result['regional'] = '国内'
    result['province'] = latlngadd_tuple[3]                                     #灾害发生的一级行政区划
    result['country'] = latlngadd_tuple[4]                                      #灾害发生国家
    result['current_website'] = '气象科普网'                                     #灾害当前网站
    result['isreleasetime'] = '1'                                               #灾害发生时间是否是用发布时间代替
    result['isrellonandlat'] = '0'
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    
    try:
        title = 'rainstorm_ZH002'
        res = postgreCommand.insertData(result,resultSun,title)
        if res == 1:
            print(title,'数据插入成功！')
        elif res == 0:
            print(title,'数据更新成功！')
    except Exception as e:
        print("插入数据失败", str(e))
        
def analyzeInfo_Two(url):
    resultSun = {}
    textStr = ''
    imgLink = ''
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    source = soup.find('div', attrs={'class': 'titleInfo'}).get_text().strip().split()[1].replace('来源：', '')
    div_info_list = soup.find('div', attrs={'id': 'BodyLabel'})                 #文本结构不同采用两种标签
    divs_info_list = div_info_list.find_all('div')
    ps_info_list = div_info_list.find_all('p')
    if divs_info_list != []:
        imgLink = ''
        for item in divs_info_list:
            span_info_list = item.find('span')
            if span_info_list == None:
                continue
            else:
                textStr = textStr + span_info_list.get_text().strip()
    elif ps_info_list != []:
        for item in ps_info_list:
            span_info_list = item.find('span')
            if span_info_list != [] and span_info_list != None:
                img_info_list = span_info_list.find('img')
                if img_info_list == None or img_info_list == []:
                    textStr = textStr + span_info_list.get_text().strip()
                else:
                    imgLink = 'http://www.qxkp.net' + img_info_list['src'] + ';' + imgLink
            else:
                img_info_list = item.find('img')
                imgLink = 'http://www.qxkp.net' + img_info_list['src'] + ';' + imgLink
    else:
        textStr = ''
        imgLink = ''
    resultSun['source'] = source
    resultSun['pictures'] = imgLink[:-1]
    resultSun['originalText'] = textStr
    return (resultSun)

# ---------------------------------------------------------------

def rainstorm_ZH002():
    result = spiderConfig.spiderConfig('rainstorm_ZH002')
    if result['status'] == '1':
        frequency = int(result['frequency'])
        delay = int(result['delay'])
        global postgreCommand
        postgreCommand = PostgreCommand()
        postgreCommand.connectPostgre()
        try:
            url = 'http://www.qxkp.net/zhfy/byhl/'
            infos_paser(url,delay)
        except Exception as e:
            print("rainstorm_ZH002访问网站失败", str(e))
        postgreCommand.closePostgre()
        timrFor = Timer(frequency*60*60,rainstorm_ZH002)
        timrFor.start()
    else:
        print('rainstorm_ZH002爬虫停止')
        timrFor = Timer(1*60*60,rainstorm_ZH002)
        timrFor.start()

# --------测试代码-----------
#rainstorm_ZH002()


