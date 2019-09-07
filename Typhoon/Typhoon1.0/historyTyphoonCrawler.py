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

def get_url():
    urlheader = "http://123.234.129.238:3989/NmfcDataService.asmx/GetNmfcDataNew"
    paramList = []
    requestUrlList = []
    lichmaHistory = {'taskFlag':'TF_08','args': '201909'}
    RosaHistory = {'taskFlag':'TF_08','args': '201910'}
    paramList.append(lichmaHistory)
    paramList.append(RosaHistory)
    for item in paramList:
        parameter = {
            'taskFlag': item['taskFlag'],
            'args': item['args']
        }
        requestParameter = urlencode(parameter)
        requestUrl = urlheader + "?" + requestParameter
        requestUrlList.append({'taskFlag':item['taskFlag'], 'args':item['args'], 'url':requestUrl})
    return requestUrlList

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('utf-8')
    dataStr = re.sub('<.*?>', '', html).strip()
    dataJson = json.loads(dataStr)
    dataJsonList = []
    dataJsonSun = dataJson
    if dataJson['data'][0]['TYPHOON_ID'] != '201909':
        return dataStr
    outTimeList = ['00:00:00','01:00:00','03:00:00','04:00:00','06:00:00','07:00:00','09:00:00','10:00:00','12:00:00','13:00:00','15:00:00','16:00:00','18:00:00','19:00:00','21:00:00','22:00:00']
    for num in range(1,(len(dataJson['data'])-1)):
        dataJsonList.append(dataJson['data'][num])
    for item in dataJsonList:
        if item['RQSJ'].split()[1] in outTimeList:
            dataJsonSun['data'].remove(item)
    dataJsonStr = json.dumps(dataJsonSun, ensure_ascii=False)
    return dataJsonStr

def historyTyphoonCrawler():
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    requestUrlList = get_url()
    for item in requestUrlList:
        dataStr = get_html(item['url'])
        updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dataJsonList = {'typhoon_data':dataStr, 'task_flag':item['taskFlag'], 'args':item['args'], 'update_time':updateTime}
        postgreCommand.historyInsertData(dataJsonList)
    postgreCommand.closePostgre()

historyTyphoonCrawler()

