# -*- coding: utf-8 -*-
"""
Created on Wed May  8 21:08:31 2019

@author: Administrator
"""

import urllib.request
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import json
import time
import re
import ssl
import cpca

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
	dataJson = json.loads(dataString)                                          #字符串转化为JSON
	count = 0
	for item in dataJson:
		count = count + 1
		if count == 200:
			break
		analyzeInfo(item)
		time.sleep(5)
def analyzeInfo(item):
    	result = {}
    	result['disasterid'] = '10010'                                         #类别:地震
    	result['source'] = '中国地震局'                                         #新闻来源
    	result['link'] = 'https://www.cea.gov.cn/eportal/ui?struts.portlet.mode=view&struts.portlet.action=/portlet/expressEarthquake!toNewInfoView.action&pageId=366521&id=' + item['id']       #新闻链接
    	time_str1 = re.sub('\D', "", analyzeInfoSun(result['link'])['time'])
    	datetime_struct1 = parser.parse(time_str1)
    	releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    	time_str2 = re.sub('\D', "", item['orig_time'])[:-1]
    	datetime_struct2 = parser.parse(time_str2)
    	occurTime = datetime_struct2.strftime('%Y-%m-%d %H:%M:%S')
    	result['releaseTime'] = releaseTime                                    #发布时间
    	result['title'] = analyzeInfoSun(result['link'])['title']              #新闻标题
    	result['originalText'] = analyzeInfoSun(result['link'])['text']        #新闻内容
    	result['place'] = item['epicenter']                                    #发生地点
    	result['longitude'] = item['longitudes']                               #地点经度
    	result['latitude'] = item['latitudes']                                 #地点纬度
    	if item['num_mag'] == None:
    		result['strength'] = ''
    	else:
    		result['strength'] = item['num_mag'] + 'M'                         #灾害强度
    	result['occurTime'] = occurTime                                        #发生时间
    	result['injured'] = '0'                                                #受伤人数
    	result['death'] = '0'                                                  #死亡人数
    	result['loss'] = '0'                                                   #经济损失
    	result['pictures'] = ''                                                #多个路径之间用分号隔开
    	if item['depth'] == None:
    		specialData =''
    	else:
    		specialData = '{震源深度: ' + item['depth'] + 'km}'
    	result['more'] = specialData                                           #特殊字段
    	placePC = place(result['place'])
    	result['regional'] = '国内'
    	result['province'] = placePC[0]                                        #灾害发生的一级行政区划
    	result['country'] = placePC[1]                                         #灾害发生国家
    	result['current_website'] = '中国地震局网'                               #灾害当前网站
    	result['isreleasetime'] = '0'                                           #灾害发生时间是否是用发布时间代替

    	resultSun = {}
    	resultSun['title'] = result['title']
    	resultSun['originalText'] = result['originalText']
    	resultSun['pictures'] = result['pictures']
    	try:
    		title = 'earthquake_ZH001'
    		res = postgreCommand.insertData(result,resultSun,title)
    		if res == 1:
    			print(title,'数据插入成功！')
    		elif res == 0:
    			print(title,'数据更新成功！')
    	except Exception as e:
    		print("插入数据失败", str(e))

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

def place(newPlace):
        originalText = [newPlace]
        placeKeyVlue = cpca.transform(originalText, cut=False)
        placeVlue = placeKeyVlue.values
        place = placeVlue[0][0] + placeVlue[0][1] + placeVlue[0][2]
        if place != '':
            province = placeVlue[0][0]
            country = '中国'
        else:
            province = ''
            country = ''
        return province,country

#---------------------------------------------------------------

def earthquake_ZH001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'https://www.cea.gov.cn/eportal/ui?struts.portlet.mode=view&struts.portlet.action=/portlet/expressEarthquake!queryExpressEarthquakeList.action&pageId=363409&moduleId=a852ba487b534470a84a30f00e7d6670'
        infos_paser(url)
    except Exception as e:
        print("earthquake_ZH001访问网站失败", str(e))
    postgreCommand.closePostgre()
#    timrFor = Timer(2*60*60,earthquake_ZH001)
#    timrFor.start()

#--------测试代码-----------
#earthquake_ZH001()

