# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 20:14:08 2019

@author: 86183
"""

import urllib.request
import ssl
import datetime
from postgres import PostgreCommand
import json

def get_html():
    result = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    url = 'https://tf.istrongcloud.com/data/gfs/gfs.json'
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    dataStr = page.read().decode('utf-8')
    dataJson = json.loads(dataStr)
    occurtimeStr = ''.join(dataJson.keys())
    occurtimeDate = datetime.datetime.strptime(occurtimeStr, '%Y%m%d%H')
    occurtime = datetime.datetime.strftime(occurtimeDate, "%Y-%m-%d %H:%M:%S")
    result['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result['realtime_data'] = dataStr
    result['occurtime'] = occurtime
    return result

def windFarmCrawler():
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    postgreCommand.windFarmInsertData(get_html())
    postgreCommand.closePostgre()

#windFarmCrawler()