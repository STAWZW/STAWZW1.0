# -*- coding: utf-8 -*-
"""
Created on Wed May  8 21:08:31 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from pcsql import MySQLCommand
from threading import Timer
import json
import re
import ssl

def get_html(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.18 Safari/537.36'}  
	context = ssl._create_unverified_context()
	req = urllib.request.Request(url, headers=headers)
	page = urllib.request.urlopen(req, context=context)
	html = page.read().decode('utf-8')  
	return html

def infos_paser(url):
	htmlCode = get_html(url)
	soup = BeautifulSoup(htmlCode,'html.parser')
	dataString = soup.get_text()
	dataJson = json.loads(dataString)      #字符串转化为JSON
	count = 0
	for item in dataJson:
		count = count + 1
		if count == 20:
			break
		analyzeInfo(item)

def analyzeInfo(item):
	result = {}
	dataCount = int(mysqlCommand.getLastId()) + 1
	result['id'] = str(dataCount)
	result['disasterid'] = '0002'     #类别:地震
	result['source'] = '中国地震局'      #新闻来源
	result['link'] = 'https://www.cea.gov.cn/eportal/ui?struts.portlet.mode=view&struts.portlet.action=/portlet/expressEarthquake!toNewInfoView.action&pageId=366521&id=' + item['id']       #新闻链接
	result['releaseTime'] = re.sub('\D', "", analyzeInfoSun(result['link'])['time'])    #发布时间
	result['title'] = analyzeInfoSun(result['link'])['title']      #新闻标题
	result['originalText'] = analyzeInfoSun(result['link'])['text']        #新闻内容
	result['place'] = item['epicenter']       #发生地点
	result['longitude'] = item['longitudes']        #地点经度
	result['latitude'] = item['latitudes']      #地点纬度
	if item['num_mag'] == None:
		result['strength'] = ''
	else:
		result['strength'] = item['num_mag'] + 'M'     #灾害强度
	result['occurTime'] = re.sub('\D', "", item['orig_time'])[:-1]     #发生时间
	result['injured'] = '0'         #受伤人数
	result['death'] = '0'         #死亡人数
	result['loss'] = '0'       #经济损失
	result['pictures'] = ''       #多个路径之间用分号隔开
	if item['depth'] == None:
		specialData =''
	else:
		specialData = '{震源深度: ' + item['depth'] + 'km}'
	result['more'] = specialData       #特殊字段

	try:
        # 插入数据，如果已经存在就不在重复插入
		title = 'earthquake_ZH'
		res = mysqlCommand.insertData(result,title)
		if res:
			dataCount=res
	except Exception as e:
		print("插入数据失败", str(e))#输出插入失败的报错语句

def analyzeInfoSun(url):
	resultSun = {}
	htmlCode = get_html(url)
	soup = BeautifulSoup(htmlCode,'html.parser')
	div_info_list = soup.find_all('div', attrs={'class': 'new_con'}, limit=1)
	divs_info_list = div_info_list[0].find_all('div', attrs={'class': 'con_top'}, limit=1)
	title_info_list = divs_info_list[0].find_all('div', attrs={'class': 'div_title'}, limit=1)
	resultSun['title'] = title_info_list[0].get_text().strip()
	time_info_list = divs_info_list[0].find_all('div', attrs={'class': 'div_time'}, limit=1)
	resultSun['time'] = time_info_list[0].get_text().strip()
	text_info_list = div_info_list[0].find_all('div', attrs={'class': 'con_bottom'}, limit=1)
	resultSun['text'] = text_info_list[0].get_text().strip()
	return resultSun


#---------------------------------------------------------------

mysqlCommand = MySQLCommand()

class earthquake(object):

    def rund(self):
        mysqlCommand.connectMysql()
        
        url = 'https://www.cea.gov.cn/eportal/ui?struts.portlet.mode=view&struts.portlet.action=/portlet/expressEarthquake!queryExpressEarthquakeList.action&pageId=363409&moduleId=a852ba487b534470a84a30f00e7d6670'
        infos_paser(url)

        mysqlCommand.closeMysql()

        a = earthquake()
        t = Timer(2*60*60,a.rund)#60秒爬取一次
        t.start()


#--------测试代码-----------
#a = earthquake()
#a.rund()


