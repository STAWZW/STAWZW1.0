# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 21:09:20 2019

@author: 86183
"""

from urllib.parse import urlencode 
import urllib.request
import ssl
from postgres import PostgreCommand
import re
import datetime
import json
import time
from threading import Timer

def get_url():
    urlheader = "http://123.234.129.238:3989/NmfcDataService.asmx/GetNmfcDataNew"
    requestUrlList = []
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    paramList = postgreCommand.allHistorySelectData()
    postgreCommand.closePostgre()
    for item in paramList:
        parameter = {
            'taskFlag': 'TF_08',
            'args': item[0]
        }
        requestParameter = urlencode(parameter)
        requestUrl = urlheader + "?" + requestParameter
        requestUrlList.append({'task_flag':'TF_08', 'args':item[0], 'url':requestUrl})
    return requestUrlList

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context, timeout=1*24*60*60)
    html = page.read().decode('utf-8')
    dataStr = re.sub('<.*?>', '', html).strip()
    return dataStr

def allHistoryTyphoonCrawler_str():
    result = {}
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    requestUrlList = get_url()
    for item in requestUrlList:
        dataStr = get_html(item['url'])
        updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dataJsonList = {'typhoon_data':dataStr, 'task_flag':item['task_flag'], 'args':item['args'], 'update_time':updateTime}
        postgreCommand.allHistoryInsertData_str(dataJsonList)
    postgreCommand.closePostgre()
    
    timrFor = Timer(1*1*3*60,allHistoryTyphoonCrawler_str)
    timrFor.start()

# allHistoryTyphoonCrawler_str()


