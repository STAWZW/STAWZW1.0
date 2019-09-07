# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:18:33 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import datetime

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
   # print(tbody_info_list)
    tr_info_list = tbody_info_list.find_all('tr', limit = 20)
    for item in tr_info_list:
        analyzeInfo(item)

def analyzeInfo(item):
    result = {}
    td_info_list = item.find_all('td')
    dataCount = int(mysqlCommand.getLastId()) + 1
    result['id'] = str(dataCount)
    result['disasterid'] = '0002'     #类别:地震
    result['source'] = '全球地震台网(GSN)'      #新闻来源
    result['link'] = 'http://www.iris.edu'
    time = td_info_list[0].get_text().strip()
    time_format = (datetime.datetime.strptime(time, '%d-%b-%Y %H:%M:%S')).strftime('%Y%m%d%H%M%S')
    result['releaseTime'] = time_format
    result['occurTime'] = result['releaseTime']
    result['latitude'] = td_info_list[1].get_text().strip()
    result['longitude'] = td_info_list[2].get_text().strip()
    result['strength'] = td_info_list[3].get_text().strip()
    result['place'] = td_info_list[5].get_text().strip()
    result['title'] = time + 'A magnitude' +  result['strength'] + 'earthquake occurred in ' + result['place'] 
    result['originalText'] = result['title']
    result['injured'] = '0'         #受伤人数
    result['death'] = '0'         #死亡人数
    result['loss'] = '0'       #经济损失
    result['pictures'] = ''
    depth = td_info_list[4].get_text().strip()
    specialData = '{震源深度: ' + depth + 'km}'
    result['more'] = specialData
    
    try:
        # 插入数据，如果已经存在就不在重复插入
        title = 'earthquake_ES002'
        res = mysqlCommand.insertData(result,title)
        if res:
            dataCount=res
    except Exception as e:
        print("插入数据失败", str(e))#输出插入失败的报错语句

#-----------------------------------------------------------------------------------------------
        
mysqlCommand = MySQLCommand()

class earthquake_ES002(object):

    def rund(self):
        mysqlCommand.connectMysql()
        try:
            url = 'http://ds.iris.edu/seismon/eventlist/index.phtml'
            infos_paser(url)
        except Exception as e:
            print("访问网站失败", str(e))#输出插入失败的报错语句

        mysqlCommand.closeMysql()

        a = earthquake_ES002()
        t = Timer(2*60*60,a.rund)#60秒爬取一次
        t.start()


#--------测试代码-----------
#a = earthquake_ES002()
#a.rund()




