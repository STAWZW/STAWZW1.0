# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:49:30 2019

@author: 86183
"""

import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import cpca
import requests
import toYc
import re

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('gbk')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find('div', attrs={'class': 'list_R pdR26'})
    ul_info_list = div_info_list.find('ul')
    li_info_list = ul_info_list.find_all('li')
    for item in li_info_list:
        analyzeInfo_One(item)

def analyzeInfo_One(item):
    result = {}
    divs = item.find_all('div')
    title = divs[0].find('a').get_text().strip()
    link = 'http://www.qxkp.net' + divs[0].find('a')['href']
    releaseTime = re.sub("\D", "", divs[1].get_text())

    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0006'     #类别:暴雨
    result['link'] = link      # 新闻链接
    resultSun = analyzeInfo_Two(link)
    result['source'] = resultSun['source']      #新闻来源
    result['originalText'] = resultSun['originalText']       # 新闻原文
    result['releaseTime'] = releaseTime          # 发布时间
    result['title'] = title                   # 标题
    title_str = [result['originalText']]
    df = cpca.transform(title_str)
    place = df.values
    result['place'] = place[0][0] + place[0][1] + place[0][2]       #发生地点
    if result['place'] != '':
        llat = geocode(result['place'])
        result['longitude'] = llat[0]     #地点经度
        result['latitude'] = llat[1]      #地点纬度
    else:
        result['longitude'] = '0'
        result['latitude'] = '0'
    result['strength'] = '暴雨'    #灾害强度
    result['occurTime'] = ''     #发生时间
    originalText = result['originalText'] + result['title']
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    result['injured'] = str(injured)         #受伤人数
    result['death'] = str(death)         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = resultSun['pictures']       #多个路径之间用分号隔开
    result['more'] = ''       #特殊字段
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'rainstorm_ZH002'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句

def analyzeInfo_Two(url):
    resultSun = {}
    textStr = ''
    imgLink = ''
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    source = soup.find('div', attrs={'class': 'titleInfo'}).get_text().strip().split()[1].replace('来源：', '')
    div_info_list = soup.find('div', attrs={'id': 'BodyLabel'})       #文本结构不同采用两种标签
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

def geocode(address):
    parameters = {'address': address, 'key': 'f6922b393df061ffff5b3c61529ce7d0'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    jwd = (answer['geocodes'][0]['location']).split(',')
    return jwd

# ---------------------------------------------------------------

mysqlCommand = MySQLCommand()

class rainstorm_ZH002(object):

   def rund(self):
       mysqlCommand.connectMysql()
       try:
           url = 'http://www.qxkp.net/zhfy/byhl/'
           infos_paser(url)
       except Exception as e:
           print("访问网站失败", str(e))#输出插入失败的报错语句
       mysqlCommand.closeMysql()

       a = rainstorm_ZH002()
       t = Timer(2*60*60,a.rund)#60秒爬取一次
       t.start()


# --------测试代码-----------
#a = rainstorm_ZH002()
#a.rund()

#url = 'http://www.qxkp.net/zhfy/byhl/'
#infos_paser(url)
    

