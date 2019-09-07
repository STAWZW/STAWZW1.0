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
        requestUrlList.append(requestUrl)
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

def allHistoryTyphoonCrawler_json():
    result = {}
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    requestUrlList = get_url()
    for urlItem in requestUrlList:
        time.sleep(0.5)
        dataJsonList = get_html(urlItem)
        for dataItem in dataJsonList:
            result['pid'] = dataItem['PID']
            result['typhoon_id'] = dataItem['TYPHOON_ID']
            result['rqsj'] = dataItem['RQSJ']
            result['jd'] = dataItem['JD']
            result['wd'] = dataItem['WD']
            result['conter_pa'] = dataItem['CONTER_PA']
            result['center_wind'] = dataItem['CENTER_WIND']
            result['seven_wind'] = dataItem['SEVEN_WIND']
            result['ten_wind'] = dataItem['TEN_WIND']
            result['move_speed'] = dataItem['MOVE_SPEED']
            result['move_direct'] = dataItem['MOVE_DIRECT']
            result['depict'] = dataItem['DEPICT']
            result['tid'] = dataItem['TID']
            result['bedit'] = dataItem['BEDIT']
            result['radius7_quad_ne'] = dataItem['RADIUS7_QUAD_NE']
            result['radius7_quad_se'] = dataItem['RADIUS7_QUAD_SE']
            result['radius7_quad_sw'] = dataItem['RADIUS7_QUAD_SW']
            result['radius7_quad_nw'] = dataItem['RADIUS7_QUAD_NW']
            result['radius10_quad_ne'] = dataItem['RADIUS10_QUAD_NE']
            result['radius10_quad_se'] = dataItem['RADIUS10_QUAD_SE']
            result['radius10_quad_sw'] = dataItem['RADIUS10_QUAD_SW']
            result['radius10_quad_nw'] = dataItem['RADIUS10_QUAD_NW']
            result['radius12_quad_ne'] = dataItem['RADIUS12_QUAD_NE']
            result['radius12_quad_se'] = dataItem['RADIUS12_QUAD_SE']
            result['radius12_quad_sw'] = dataItem['RADIUS12_QUAD_SW']
            result['radius12_quad_nw'] = dataItem['RADIUS12_QUAD_NW']
            result['twelve_wind'] = dataItem['TWELVE_WIND']
            result['power'] = dataItem['POWER']
            result['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            postgreCommand.allHistoryInsertData_json(result)
    postgreCommand.closePostgre()

    timrFor = Timer(1*1*3*60,allHistoryTyphoonCrawler_json)
    timrFor.start()

#allHistoryTyphoonCrawler_json()







