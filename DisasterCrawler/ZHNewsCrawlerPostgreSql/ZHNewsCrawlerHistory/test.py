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

def infos_paser(url1):
    htmlCode = get_html1(url1)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'class': 'result'}, limit=1)
    div1_info_list = div_info_list[0].find_all('div', attrs={'class': 'box-result clearfix'})
    for item in div1_info_list:
        try:
            analyzeInfo(item)
            time.sleep(1)
        except:
            continue

def analyzeInfo(item):
    result = {}
    h2_list = item.find_all('h2',limit=1)
    a_list = h2_list[0].find_all('a')
    span_list = h2_list[0].find_all('span')
    span_new = span_list[0].get_text().strip().split()
    result['link'] = a_list[0]['href']                                          #新闻链接
    result['title'] = a_list[0].get_text().strip()                              #新闻标题
    result['releaseTime'] = span_new[1] + ' ' +span_new[2]                      #发布时间
    originalList = get_original(result['link'])
    result['source'] = originalList[0]                                          #新闻来源
    print(result)
    
def get_original(url):
    textStr = ''
    imgList = []
    htmlCode = get_html(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div1_info_list = soup.find_all('div', attrs={'class': 'date-source'}, limit=1)
    if div1_info_list == None:
        sourceStr = '新浪网'
    else:
        news = div1_info_list[0].find_all('a', limit=1)
        sourceStr = news[0].get_text().strip()
    div2_info_list = soup.find_all('div', attrs={'class': 'article'}, limit=1)
    if div2_info_list == None:
        textStr = ''
        imgStr = ''
    else:
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
    return sourceStr,textStr,imgStr

# ---------------------------------------------------------------

def infos_url(url):
    aList = []
    htmlCode = get_html1(url)
    soup = BeautifulSoup(htmlCode, 'html.parser')
    div_info_list = soup.find_all('div', attrs={'id': '_function_code_page'}, limit=1)
    a_info_list = div_info_list[0].find_all('a')
    for item in a_info_list:
        link = 'https://search.sina.com.cn' + item['href']
        aList.append(link)
    return aList
# -------------------测试代码----------------------------------------


#url = 'https://search.sina.com.cn/?q=%BB%AC%C6%C2&range=title&c=news&sort=time'
#infos_paser(url)
#urlList = infos_url(url)
#for item in urlList[0:4]:
#        print(item)
#        # url1 = item
infos_paser('https://search.sina.com.cn/?q=%BB%AC%C6%C2&range=title&c=news&sort=time&col=&source=&from=&country=&size=&time=&a=&page=5&pf=0&ps=0&dpc=1')


# --------测试代码-----------
# url = 'https://search.sina.com.cn/?q=%BB%AC%C6%C2&range=title&c=news&sort=time'
# urlList = infos_url(url)
# print(urlList)