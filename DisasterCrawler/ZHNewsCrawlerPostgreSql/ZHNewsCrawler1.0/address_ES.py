# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:19:44 2019

@author: 86183
""" 
import hashlib
import random
import geocoder
import requests
import langid

def translate(content,language):
    apiurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    appid = '20190730000322586'
    secretKey = 'df2vBgyHUCkAUDP6BDwM'
    if language == 'en':
        content = content.lower()
    salt = str(random.randint(32768, 65536))
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    try:
        paramas = {
            'appid': appid,
            'q': content,
            'from': language,
            'to': 'zh',
            'salt': salt,
            'sign': sign
        }
        response = requests.get(apiurl, paramas)
        jsonResponse = response.json()
        if "trans_result" in jsonResponse.keys():
            dst = str(jsonResponse["trans_result"][0]["dst"])
        else:
            dst = content
        return dst
    except Exception as e:
        print(e)
        return content

def countryJudge(country):
    countryName = ''
    with open('guojia.txt',"r") as f:     #设置文件对象
        lines = f.readlines()
        for line in lines:
            lineList = line.split('\t')
            abbreviationList = lineList[1].split(',')
            for item in abbreviationList:
                if country == item:
                    countryName = lineList[0]
                    continue
    return countryName

def placeAdd(add):
    addreJson = geocoder.arcgis(add)
    lat = addreJson.lat
    lng = addreJson.lng
    if addreJson.latlng != None:
        place = (addreJson.address).replace(',','，')
        language_place = langid.classify(place)[0]
        location = geocoder.arcgis([lat, lng], method='reverse')
        state = location.state
        country = location.country
        language_state = langid.classify(state)[0]
        place_zh = translate(place,language_place)
        country_zh = countryJudge(country)
        state_zh = translate(state,language_state)
    else:
        place_zh = ''
        country_zh = ''
        state_zh = ''
    return place_zh,country_zh,state_zh

def placeLatlng(lat,lng):
    location = geocoder.arcgis([lat, lng], method='reverse')
    if location.state != None:
        state = location.state
        language_state = langid.classify(state)[0]
        state_zh = translate(state,language_state)
    else:
        state_zh = ''
    country = location.country
    country_zh = countryJudge(country)
    return country_zh,state_zh

