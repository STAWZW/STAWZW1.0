# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 10:35:08 2019

@author: 86183
"""

import urllib.request
import ssl
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import re
import time
import toYc
import address

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('UTF-8')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'id': 'content_left'}, limit=1)
    divs_info_list = div_info_list[0].find_all('div', attrs={'class': 'result'})
    for item in divs_info_list:
        try:
            analyzeInfo(item)
            time.sleep(5)
        except:
            continue

def analyzeInfo(item):
    result = {}
    h3_list = item.find_all('h3', limit=1)
    a_list = h3_list[0].find_all('a', limit=1)
    div_list = item.find('div',attrs={'class': 'c-summary c-row '})#.find('p').get_text().split()
    p_list = div_list.find('p').get_text().split()
    time_str = re.sub("\D", "", p_list[1] + p_list[2])
    datetime_struct1 = parser.parse(time_str)
    releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    result['link'] = a_list[0]['href']
    result['title'] = a_list[0].get_text().strip()
    result['releaseTime'] = releaseTime
    result['disasterid'] = '10102'
    originalList = get_original(result['link'])
    result['source'] = originalList[0]
    result['originalText'] = originalList[1]
    result['pictures'] = originalList[2]
    originalText = result['title'] + '，' + result['originalText']
    latlngadd_tuple = address.placeSingle(originalText)
    result['place'] = latlngadd_tuple[0]                                        #发生地点
    result['longitude'] = str(latlngadd_tuple[1])                               #地点经度
    result['latitude'] = str(latlngadd_tuple[2])                                #地点纬度
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    lossNumber = toYc.loss(originalText)
    result['loss'] = str(lossNumber)                                            #经济损失
    result['injured'] = str(injured)                                            #受伤人数
    result['death'] = str(death)                                                #死亡人数                                             
    result['province'] = latlngadd_tuple[3]                                     #灾害发生的一级行政区划
    result['country'] = latlngadd_tuple[4]                                      #灾害发生国家                                          
    result['strength'] = ''
    result['occurTime'] = result['releaseTime']                                 #多个路径之间用分号隔开
    result['more'] = ''                                                         #特殊字段
    result['regional'] = '国内'                                                  #新闻发布地区
    result['current_website'] = '百度新闻'                                       #灾害当前网站
    result['isreleasetime'] = '1'                                               #灾害发生时间是否是用发布时间代替
    result['isrellonandlat'] = '0'
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    try:
        title = 'typhoon_ZH005'
        res = postgreCommand.insertData(result,resultSun,title)
        if res == 1:
            print(title,'数据插入成功！')
        elif res == 0:
            print(title,'数据更新成功！')
    except Exception as e:
        print("插入数据失败", str(e))
    
def get_original(url):
    textStr = ''
    imgStr = ''
    imgList = []
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div1_info_list = soup.find_all('div', attrs={'class': 'author-txt'}, limit=1)
    p1_list = div1_info_list[0].find_all('p')
    sourceStr = p1_list[0].get_text().strip()
    div2_info_list = soup.find_all('div', attrs={'class': 'article-content'}, limit=1)
    p_info_list = div2_info_list[0].find_all('p')
    div3_info_list = div2_info_list[0].find_all('div', attrs={'class': 'img-container'})
    for item in p_info_list:
        if item.find('a') != None:
            break
        else:
            textStr = textStr + item.get_text().strip()
    if div3_info_list != None:
        for item in div3_info_list:
            img_list = item.find_all('img')
            img_list_one = img_list[0]['src']
            imgList.append(img_list_one)
    imgStr = ';'.join(imgList)
    return sourceStr, textStr, imgStr

# ---------------------------------------------------------------
def typhoon_ZH005():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=undefined&tn=news&rsv_dl=ns_pc&word=%E5%8F%B0%E9%A3%8E%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF&x_bfe_rqs=03E80&x_bfe_tjscore=0.001476&tngroupname=organic_news&pn=0'
        infos_paser(url)
    except Exception as e:
        print("typhoon_ZH005访问网站失败", str(e))
    postgreCommand.closePostgre()

# --------测试代码-----------
#typhoon_ZH005()
