# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 19:20:37 2019

@author: 86183
"""

import urllib.request
import ssl
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import time
import toYc
import fool
import geocoder

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('gb18030')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find('div', attrs={'class': 'box1'})
    ul_info_list = div_info_list.find_all('ul')
    for ulitem in ul_info_list:
        li_info_list = ulitem.find_all('li')
        for liitem in li_info_list:
            try:
                analyzeInfo(liitem)
                time.sleep(1)
            except:
                continue

def analyzeInfo(item):
    result = {}
    a_info = item.find('a')
    result['link'] = 'http://japan.people.com.cn' + a_info['href']
    result['title'] = a_info.get_text().strip()
    datetime_struct1 = parser.parse(item.find('span').get_text().strip())
    releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    result['releaseTime'] = releaseTime
    analyze = analyzeInfoSun(result['link'])
    result['source'] = analyze[1]
    result['originalText'] = analyze[0]
    originalText = result['title'] + '，' + result['originalText']
    result['disasterid'] = disasterNB(originalText)                          #新闻类别:崩塌
    if result['disasterid'] != '0':
        latlngadd_tuple = placeSingle(originalText)
        result['place'] = latlngadd_tuple[0]                                    #发生地点
        result['longitude'] = str(latlngadd_tuple[1])                           #地点经度
        result['latitude'] = str(latlngadd_tuple[2])                            #地点纬度
        result['strength'] = ''                                                 #灾害强度
        result['occurTime'] = result['releaseTime']                             #parser.parse('2017-10-01 12:12:12')     #发生时间
        death = toYc.death(originalText)
        injured = toYc.Injured(originalText)
        lossNumber = toYc.loss(originalText)
        result['loss'] = str(lossNumber)                                        #经济损失
        result['injured'] = str(injured)                                        #受伤人数
        result['death'] = str(death)                                            #死亡人数
        result['pictures'] = analyze[2]                                         #多个路径之间用分号隔开
        result['more'] = ''                                                     #特殊字段
        result['regional'] = '国内'                                              #新闻发布地区
        result['province'] = ''                                                 #灾害发生的一级行政区划
        result['country'] = '日本'                                               #灾害发生国家
        result['current_website'] = '人民网'                                     #灾害当前网站
        result['isreleasetime'] = '1'                                           #灾害发生时间是否是用发布时间代替
        result['isrellonandlat'] = '0' 
        resultSun = {}
        resultSun['title'] = result['title']
        resultSun['originalText'] = result['originalText']
        resultSun['pictures'] = result['pictures']
        try:
            title = 'comprehensive_ZH001'
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
    if soup.find('div', attrs={'class': 'box01'}) == None:
        testStr=''
        source=''
        picturesStr=''
        return testStr,source,picturesStr
    source = soup.find('div', attrs={'class': 'box01'}).find('div', attrs={'class': 'fl'}).find('a').get_text().strip()
    p_info_list = soup.find('div', attrs={'class': 'fl text_con_left'}).find_all('p')
    for item in p_info_list:
        textList.append(item.get_text().strip())
        img_info = item.find('img')
        if img_info != None:
            picturesList.append('http://japan.people.com.cn' + img_info['src'])
    testStr = ''.join(textList)
    picturesStr = ';'.join(picturesList)
    return testStr,source,picturesStr

def disasterNB(text):
    disasterResult = {'崩塌': '10001', '干旱': '10112', '暴雨': '10301', '地震': '10010', '山体崩塌': '1000104','风暴潮':'10201','海啸':'10205','泥石流':'10306','森林火灾':'10502','台风':'10102','滑坡':'10002'}
    disasterList = ['崩塌','干旱','暴雨','地震','山体崩塌','风暴潮','海啸','泥石流','森林火灾','台风','滑坡']
    disasterCountList = []
    for  disasteritem in disasterList:
        disasterCountList.append(text.count(disasteritem))
    if max(disasterCountList) == 0:
        disasterid = '0'
    else:
        disaster = disasterList[disasterCountList.index(max(disasterCountList))]
        disasterid = disasterResult[disaster]
    return disasterid

def placeSingle(text):
    placeLists = []
    longitudeList = []
    latitudeList = []
    words, ners = fool.analysis(text)
    for itemSun in ners[0]:
        if itemSun[2] == 'location':
            places = geocoder.arcgis(itemSun[3])
            if places.latlng == None:
                continue
            placeLists.append(((places.address).split(','))[0])
            longitudeList.append(str(round(places.lng,2)))
            latitudeList.append(str(round(places.lat,2)))
    if placeLists == []:
        place = ''
        longitude = ''
        latitude = ''
        return place,longitude,latitude
    place = max(placeLists, key=placeLists.count)
    indexdata = placeLists.index(place)
    longitude = longitudeList[indexdata]
    latitude = latitudeList[indexdata]
    return place,longitude,latitude

# ---------------------------------------------------------------

def comprehensive_ZH001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://japan.people.com.cn/GB/35467/387511/index.html'
        infos_paser(url)
    except Exception as e:
        print("comprehensive_ZH001访问网站失败", str(e))
    postgreCommand.closePostgre()

# --------测试代码-----------
#comprehensive_ZH001()



