# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 09:08:22 2019

@author: 86183
"""

from urllib.parse import urlencode 
import urllib.request
import ssl
from postgres import PostgreCommand
import re
import json
import datetime
from threading import Timer

def get_url(taskFlag):
    urlheader = "http://123.234.129.238:3989/NmfcDataService.asmx/GetNmfcDataNew"
    parameter = {
        'taskFlag': taskFlag,
        'args':''
    }
    requestParameter = urlencode(parameter)
    requestUrl = urlheader + "?" + requestParameter
    return requestUrl

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context, timeout=1*24*60*60)
    html = page.read().decode('utf-8')
    dataStr = re.sub('<.*?>', '', html).strip()
    dataJson = json.loads(dataStr)
    dataList = dataJson['data']
    return dataList

def allTyphoonCrawler():
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    dataResult = {}
    currentList = []
    currentDataList = get_html(get_url('TF_09'))
    for item in currentDataList:
        currentList.append(item['TYPHOON_ID'])
    dataList = get_html(get_url('TF_01'))
    for dataItem in dataList:
        dataResult['typhoon_id'] = dataItem['TYPHOON_ID']
        dataResult['chn_name'] = dataItem['CHN_NAME']
        dataResult['eng_name'] = dataItem['ENG_NAME']
        dataResult['typhoon_year'] = dataItem['TYPHOON_YEAR']
        dataResult['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if dataItem['TYPHOON_ID'] in currentList:
            dataResult['typhon_status'] = '1'
        else:
            dataResult['typhon_status'] = '0'
        postgreCommand.allTyphoonInsertData(dataResult)
    postgreCommand.closePostgre()

    timrFor = Timer(1*1*3*60,allTyphoonCrawler)
    timrFor.start()

# allTyphoonCrawler()













