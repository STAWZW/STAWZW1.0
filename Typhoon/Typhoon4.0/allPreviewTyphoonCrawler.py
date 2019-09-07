# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:57:56 2019

@author: 86183
"""

from urllib.parse import urlencode 
import urllib.request
import ssl
from postgres import PostgreCommand
import re
import json
from threading import Timer

def get_url():
    urlheader = "http://123.234.129.238:3989/NmfcDataService.asmx/GetNmfcDataNew"
    paramList = []
    requestUrlList = []
    requestUrlResult = {}
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    paramList = postgreCommand.allHistorySelectData()
    postgreCommand.closePostgre()
    address = ['中国','日本','中国香港','美国','中国台湾','韩国']
    for item in paramList:
        for add in address:
            parameter = {
                'taskFlag': 'TF_07',
                'args': item[0] + ',' + add
            }
            requestParameter = urlencode(parameter)
            requestUrl = urlheader + "?" + requestParameter
            requestUrlResult = {'requestUrl': requestUrl, 'args':item[0], 'address': add}
            requestUrlList.append(requestUrlResult)
    return requestUrlList

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context, timeout=1*24*60*60)
    html = page.read().decode('utf-8')
    dataStr = re.sub('<.*?>', '', html).strip()
    dataJson = json.loads(dataStr)
    dataJsonList = dataJson['data']
    return dataJsonList

def allPreviewTyphoonCrawler():
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    dataResult = {}
    requestUrlList = get_url()
    for item in requestUrlList:
        dataJsonList = get_html(item['requestUrl'])
        if dataJsonList != []:
            postgreCommand.deletPreviewInsertData(item['args'],item['address'])
        for dataItem in dataJsonList:
            dataResult['pid'] = dataItem['PID']
            dataResult['typhoon_id'] = dataItem['TYPHOON_ID']
            dataResult['forcast_country_name'] = dataItem['FORCAST_COUNTRY_NAME']
            dataResult['ybsj'] = dataItem['YBSJ']
            dataResult['rqsj'] = dataItem['RQSJ']
            dataResult['jd'] = dataItem['JD']
            dataResult['wd'] = dataItem['WD']
            dataResult['conter_pa'] = dataItem['CONTER_PA']
            dataResult['center_wind'] = dataItem['CENTER_WIND']
            dataResult['seven_wind'] = dataItem['SEVEN_WIND']
            dataResult['ten_wind'] = dataItem['TEN_WIND']
            dataResult['move_direct'] = dataItem['MOVE_DIRECT']
            dataResult['depict'] = dataItem['DEPICT']
            dataResult['tid'] = dataItem['TID']
            dataResult['line_color'] = dataItem['LINE_COLOR']
            postgreCommand.allPreviewInsertData(dataResult)
    postgreCommand.closePostgre()
 
    timrFor = Timer(1*1*3*60,allPreviewTyphoonCrawler)
    timrFor.start()

# allPreviewTyphoonCrawler()








