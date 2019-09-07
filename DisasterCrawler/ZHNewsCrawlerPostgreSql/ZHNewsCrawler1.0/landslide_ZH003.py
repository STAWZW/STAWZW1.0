#!/usr/bin/env python
# -*- coding:utf-8 -*-
_author_ = 'sunyanan'

import urllib.request
import ssl
from bs4 import BeautifulSoup
from postgres import PostgreCommand
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

def get_html1(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('gbk')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    td_info_list = soup.find_all('td', attrs={'class': 'searchresult'}, limit=1)
    table_info_list = td_info_list[0].find_all('table', attrs={'style': 'line-height:160%;width:100%;color:#339933;'})
    for item in table_info_list:
        try:
            analyzeInfo(item)
            time.sleep(5)
        except:
            continue

def analyzeInfo(item):
    result = {}
    a_list = item.find_all('td',limit=1)
    result['link'] = a_list[0].get_text().strip()                               #新闻链接
    originalList = get_original(result['link'])
    result['title'] = originalList[0]                                           #新闻标题
    result['source'] = originalList[1]                                          #新闻来源
    result['releaseTime'] = originalList[2]                                     #发布时间
    result['originalText'] = originalList[3]                                    #新闻原文
    result['disasterid'] = '10002'                                              #灾害类型
    result['pictures'] = originalList[4]                                        #新闻图片
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
    result['regional'] = '国内'                                                 #新闻发布地区                               #灾害发生国家
    result['current_website'] = '大众网'                                        #灾害当前网站
    result['isreleasetime'] = '1'                                               #灾害发生时间是否是用发布时间代替
    result['isrellonandlat'] = '0'
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    try:
        title = 'landslide_ZH003'
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
    htmlCode = get_html1(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div1_info_list = soup.find_all('div', attrs={'class': 'layout'}, limit=1)
    h2_list = div1_info_list[0].find_all('h2')
    titleStr = h2_list[0].get_text().strip()
    news = div1_info_list[0].find_all('div', attrs={'class': 'left'}, limit=1)
    news_list = news[0].get_text().strip().split()
    sourceStr = news_list[3]
    timeStr = news_list[0] + ' ' + news_list[1]
    div2_info_list = soup.find_all('div', attrs={'class': 'news-con'}, limit=1)
    p_info_list = div2_info_list[0].find_all('p')
    for item in p_info_list:
        if item.find('a') != None:
            break
        elif item.find('img') != None:
            img_list = item.find_all('img')
            img_list_one = img_list[0]['src']
            imgList.append(img_list_one)
            continue
        else:
            textStr = textStr + item.get_text().strip()
    imgStr = ';'.join(imgList)
    return titleStr,sourceStr,timeStr,textStr,imgStr

# ---------------------------------------------------------------
def landslide_ZH003():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://so.dzwww.com/web/search?searchscope=DOCTITLE&timescope=&timescopecolumn=&orderby=LIFO&channelid=205667&andsen=&total=&orsen=&exclude=&searchword=%E5%B1%B1%E4%BD%93%E6%BB%91%E5%9D%A1&perpage=&templet=&token=&timeline='
        infos_paser(url)
    except Exception as e:
        print("landslide_ZH003访问网站失败", str(e))
    postgreCommand.closePostgre()

# --------测试代码-----------
#landslide_ZH003()

