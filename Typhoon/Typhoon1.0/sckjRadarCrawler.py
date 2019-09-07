# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 17:53:20 2019

@author: 86183
"""

import urllib.request
import ssl
import datetime
from postgres import PostgreCommand
import json
from urllib.request import urlretrieve
import base64
import os

def get_html():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WDW64; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    context = ssl._create_unverified_context()
    url = 'https://tf.istrongcloud.com/data/images/radar/mingle/caiyun_transparent.json'
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req, context=context)
    dataStr = page.read().decode('utf-8')
    dataJson = json.loads(dataStr)
    return dataJson

def sckjRadarCrawler():
    result = {}
    dataJson = get_html()
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    for item in dataJson:
        img_name = item['name'].replace('.PNG', '.png')
        filePath = './radar_img/'
        img_list = os.listdir(filePath)
        if img_name in img_list:
            print('图片数据已存在')
            continue
        urlretrieve(item['url'], './radar_img/' + img_name) 
#        with open('./radar_img/' + item['name'], 'rb') as f:
#            base64_data = base64.b64encode(f.read())
#            r_bs = base64_data.decode()
        update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timeStr = item['name'].replace('.PNG','')
        timeDate = datetime.datetime.strptime(timeStr, '%Y%m%d%H%M')
        release_time = datetime.datetime.strftime(timeDate, "%Y-%m-%d %H:%M:%S")
        result['r_name'] = item['name']
        result['r_url'] = item['url']
        result['r_bs'] = img_name
        result['md5'] = item['md5']
        result['dt'] = item['dt']
        result['update_time'] = update_time
        result['release_time'] = release_time
        postgreCommand.sckjRadarInsertData(result)
    postgreCommand.closePostgre()

#sckjRadarCrawler()
