# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:18:33 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from threading import Timer
import datetime
import address_ES
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
    tbody_info_list = soup.find('tbody')
    tr_info_list = tbody_info_list.find_all('tr', limit = 20)
    for item in tr_info_list:
        analyzeInfo(item)

def analyzeInfo(item):
    result = {}
    td_info_list = item.find_all('td')
    result['disasterid'] = '10010'                                          #类别:地震
    result['source'] = '全球地震台网(GSN)'                                    #新闻来源
    result['link'] = 'http://www.iris.edu'
    time = td_info_list[0].get_text().strip()
    time_format = (datetime.datetime.strptime(time, '%d-%b-%Y %H:%M:%S')).strftime('%Y-%m-%d %H:%M:%S')
    result['releaseTime'] = time_format
    result['occurTime'] = result['releaseTime']
    result['latitude'] = td_info_list[1].get_text().strip()
    result['longitude'] = td_info_list[2].get_text().strip()
    result['strength'] = td_info_list[3].get_text().strip()
    place = td_info_list[5].get_text().strip()
    result['place'] = toYc.translate(place)
    addlatlng = address_ES.placeAdd(result['place'])
    title = time + 'A magnitude' +  result['strength'] + 'earthquake occurred in ' + result['place'] 
    result['title'] = title
    result['originalText'] = title
    result['injured'] = '0'                                                 #受伤人数
    result['death'] = '0'                                                   #死亡人数
    result['loss'] = '0'                                                    #经济损失
    result['pictures'] = ''
    depth = td_info_list[4].get_text().strip()
    specialData = '{震源深度: ' + depth + 'km}'
    result['more'] = specialData
    result['regional'] = '国外'
    result['province'] = addlatlng[2]                                       #灾害发生的一级行政区划
    result['country'] = addlatlng[1]                                        #灾害发生国家
    result['current_website'] = '全球地震台网(GSN)'                           #灾害当前网站
    result['isreleasetime'] = '0'                                           #灾害发生时间是否是用发布时间代替
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    
    try:
        title = 'earthquake_ES002'
        res = postgreCommand.insertData(result,resultSun,title)
        if res == 1:
            print(title,'数据插入成功！')
        elif res == 0:
            print(title,'数据更新成功！')
    except Exception as e:
        print("插入数据失败", str(e))

#-----------------------------------------------------------------------------------------------

def earthquake_ES002():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://ds.iris.edu/seismon/eventlist/index.phtml'
        infos_paser(url)
    except Exception as e:
        print("earthquake_ES002访问网站失败", str(e))
    postgreCommand.closePostgre()
#    timrFor = Timer(2*60*60,earthquake_ES002)
#    timrFor.start()

#--------测试代码-----------
#earthquake_ES002()




