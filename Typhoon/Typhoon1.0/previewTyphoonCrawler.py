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

def get_url():
    urlheader = "http://123.234.129.238:3989/NmfcDataService.asmx/GetNmfcDataNew"
    paramList = []
    requestUrlList = []
    lichmaPreview = {'taskFlag':'TF_07','args': '201909'}
    RosaPreview = {'taskFlag':'TF_07','args': '201910'}
    paramList.append(lichmaPreview)
    paramList.append(RosaPreview)
    address = ['中国','日本','中国香港','美国','中国台湾','韩国']
    for item in paramList:
        for add in address:
            parameter = {
                'taskFlag': item['taskFlag'],
                'args': item['args'] + ',' + add
            }
            requestParameter = urlencode(parameter)
            requestUrl = urlheader + "?" + requestParameter
            requestUrlList.append(requestUrl)
    return requestUrlList

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    html = page.read().decode('utf-8')
    dataStr = re.sub('<.*?>', '', html).strip()
    dataJson = json.loads(dataStr)
    dataJsonList = dataJson['data']
    return dataJsonList

def previewTyphoonCrawler_copy():
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    dataResult = {}
    requestUrlList = get_url()
    for item in requestUrlList:
        dataJsonList = get_html(item)
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
            postgreCommand.previewInsertData_copy(dataResult)
    postgreCommand.closePostgre()

#previewTyphoonCrawler_copy()








