# -*- coding:utf-8 -*-

import urllib.request
import ssl
from bs4 import BeautifulSoup
from postgres import PostgreCommand
from dateutil import parser
import time
import toYc
import address

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('gbk')
    return html

def get_html1(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('UTF-8')
    return html

def infos_paser(url):
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    ul_info_list = soup.find_all('ul', attrs={'class': 'tag_cont'}, limit=1)
    li_info_list = ul_info_list[0].find_all('li')
    for item in li_info_list:
        try:
            analyzeInfo(item)
            time.sleep(1)
        except:
            continue

def analyzeInfo(item):
    result = {}
    h4_list = item.find_all('h4',limit=1)
    a_list = h4_list[0].find_all('a', limit=1)
    i_list = item.find_all('i',limit=1)
    time_str = (i_list[0].get_text().strip())[3:]
    datetime_struct1 = parser.parse(time_str)
    releaseTime = datetime_struct1.strftime('%Y-%m-%d %H:%M:%S')
    result['link'] = a_list[0]['href']                                          #新闻链接
    result['title'] = a_list[0].get_text().strip()                              #新闻标题
    result['releaseTime'] = releaseTime                                         #发布时间
    originalList = get_original(result['link'])
    result['source'] = originalList[1]                                          #新闻来源
    result['originalText'] = originalList[0]                                    #新闻原文
    originalText = result['title'] + '，' + result['originalText']
    latlngadd_tuple = address.placeMany(originalText)
    result['disasterid'] = '10101'                                              #灾害类型
    result['place'] = latlngadd_tuple[0]                                        #发生地点
    result['longitude'] = str(latlngadd_tuple[1])                               #地点经度
    result['latitude'] = str(latlngadd_tuple[2])                                #地点纬度
    result['strength'] = ''
    result['occurTime'] = result['releaseTime']
    death = toYc.death(originalText)
    injured = toYc.Injured(originalText)
    lossNumber = toYc.loss(originalText)
    result['loss'] = str(lossNumber)                                            #经济损失
    result['injured'] = str(injured)                                            #受伤人数
    result['death'] = str(death)                                                #死亡人数
    result['pictures'] = originalList[2]                                        #多个路径之间用分号隔开
    result['more'] = ''                                                         #特殊字段
    result['regional'] = '国内'                                                 #新闻发布地区
    result['province'] = latlngadd_tuple[3]                                     #灾害发生的一级行政区划
    result['country'] = latlngadd_tuple[4]                                      #灾害发生国家
    result['current_website'] = '天气网'                                        #灾害当前网站
    result['isreleasetime'] = '1'                                               #灾害发生时间是否是用发布时间代替
    result['isrellonandlat'] = '0'
    resultSun = {}
    resultSun['title'] = result['title']
    resultSun['originalText'] = result['originalText']
    resultSun['pictures'] = result['pictures']
    try:
        title = 'tropicalWind_ZH001'
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
    div1_info_list = soup.find_all('div', attrs={'class': 'texts'}, limit=1)
    p_info_list = div1_info_list[0].find_all('p')
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
    div2_info_list = soup.find_all('div', attrs={'class': 'time'}, limit=1)
    sourceStrSun = div2_info_list[0].get_text().strip()
    sourceStr = sourceStrSun.split()
    sourceStr = sourceStr[1].replace('来源：', '')
    imgStr = ';'.join(imgList)
    return textStr,sourceStr,imgStr

# ---------------------------------------------------------------

def tropicalWind_ZH001():
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    try:
        url = 'http://www.tianqi.com/tag/%C8%C8%B4%F8%C6%F8%D0%FD/'
        infos_paser(url)
    except Exception as e:
        print("tropicalWind_ZH001访问网站失败", str(e))
    postgreCommand.closePostgre()

# --------测试代码-----------
tropicalWind_ZH001()


