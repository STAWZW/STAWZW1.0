#!/usr/bin/env python 
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'


import urllib.request
import ssl
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import address
import re
import toYc
import time

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
        try:
            analyzeInfo(item)
            time.sleep(5)
        except:
            continue

def analyzeInfo(item):
    result = {}
    a_list = item.find_all('a', limit=1)
    h3_list = item.find_all('h3',attrs={'class': 'tit'},limit=1)
    span_link_list = h3_list[0].find_all('span', limit=1)
    div_list = item.find_all('div', attrs={'class': 'src-tim'}, limit=1)
    span2_list = div_list[0].find_all('span', attrs={'class': 'tim'}, limit=1)
    time_str = re.sub('\D', "", span2_list[0].get_text().strip())
    datetime_struct = parser.parse(time_str)
    releaseTime = datetime_struct.strftime('%Y-%m-%d %H:%M:%S')
    result['disasterid'] = '10205'                                          #新闻类别
    result['link'] = span_link_list[0]['lanmu1']                            #新闻链接
    result['title'] = a_list[0].get_text().strip()                          #新闻标题
    result['releaseTime'] = releaseTime                                     #发布时间
    analyze = analyzeInfoSun(result['link'])
    result['source'] = analyze[1]                                           #新闻来源
    result['originalText'] = analyze[0]                                     #新闻原文
    originalText = result['title'] + '，' + result['originalText']
    latlngadd_tuple = address.placeSingle(originalText)
    result['place'] = latlngadd_tuple[0]                                    #发生地点
    result['longitude'] = str(latlngadd_tuple[1])                           #地点经度
    result['latitude'] = str(latlngadd_tuple[2])                            #地点纬度
    result['strength'] = ''                                                 #灾害强度
    result['occurTime'] = result['releaseTime']                             #发生时间
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    lossNumber = toYc.loss(originalText)
    result['loss'] = str(lossNumber)                                        #经济损失
    result['injured'] = str(injured)                                        #受伤人数
    result['death'] = str(death)                                            #死亡人数
    result['pictures'] = analyze[2]                                         #多个路径之间用分号隔开
    result['more'] = ''                                                     #特殊字段
    result['regional'] = '国内'
    result['province'] = latlngadd_tuple[3]                                 #灾害发生的一级行政区划
    result['country'] = latlngadd_tuple[4]                                  #灾害发生国家
    result['current_website'] = '央视网'                                     #灾害当前网站
    result['isreleasetime'] = '1'                                           #灾害发生时间是否是用发布时间代替
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    try:
        title = 'tsunami_ZH005'
        res = postgreCommand.insertData(result,resultSun,title)
        if res == 1:
            print(title,'数据插入成功！')
        elif res == 0:
            print(title,'数据更新成功！')
    except Exception as e:
        print("插入数据失败", str(e))

def analyzeInfoSun(url):
    textList = []
    picturesList = []
    picturesStr = ''
    testStr = ''
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'cnt_bd'}, limit=1)
    span_info_list = div_info_list[0].find_all('span', attrs={'class': 'info'}, limit=1)
    i_info_list = span_info_list[0].find('i')
    source = i_info_list.get_text().strip()[3:7]
    p_info_list = div_info_list[0].find_all('p')
    for item in p_info_list:
        if item.find('img') != None:
            picturesList.append(item.find('img')['src'])
        if item.find('script') != None:
            continue
        else:
            textList.append(item.get_text().strip())
    picturesStr = ';'.join(picturesList)
    testStr = ''.join(textList)[4:]
    return testStr,source,picturesStr

# ---------------------------------------------------------------

def tsunami_ZH005():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    for item in range(0, 15):
        try:
            url = 'https://search.cctv.com/search.php?qtext=%E6%B5%B7%E5%95%B8&sort=relevance&type=web&vtime=&datepid=1&channel=&page=' + str(
                item)
            infos_paser(url)
        except Exception as e:
            print("tsunami_ZH005访问网站失败", str(e))
            continue
    postgreCommand.closePostgre()

# --------测试代码-----------
# tsunami_ZH005()
