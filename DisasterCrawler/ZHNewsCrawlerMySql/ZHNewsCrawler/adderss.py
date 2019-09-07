# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:01:57 2019

@author: 86183
"""

import cpca
import fool
import requests
def place():
    title_str = '央视网消息：记者从辽宁省农业农村厅了解到，受降水偏少、气温偏高影响，锦州、阜新、朝阳、葫芦岛等辽西地区土壤湿度偏低，当地正全力抗旱保春播。辽宁省气象局8日测墒结果显示，辽宁西部地区土壤墒情不理想，不利于作物播种。锦州市北镇、凌海、义县，阜新市阜新蒙古族自治县、彰武县，朝阳市建平县、喀左县，葫芦岛兴城地区等地土壤相对湿度为14%—38%。据了解，辽西地区今年春播进度明显偏慢。目前，辽宁省派出农技人员开展指导服务4866人次，指导服务农民37.8万户，推广抗旱播种面积1351.4万亩。同时发挥农机作业优势，全省共指导检修各类农机具50.9万台(套)，完成秋翻整地1909.4万亩、春翻整地1759.8万亩。据辽宁省农业农村厅介绍，全省结合生产实际，已提前筛选发布55个主要作物优良品种和12项春耕生产关键技术。辽西旱情显现后，及时组织各级农业农村部门根据当地实际，制定印发宣传单、明白卡等技术资料，选派农技人员进村入户、蹲点包片开展分类技术指导。据了解，下一步，辽宁省将继续指导各地分析研判干旱趋势，做好耐旱作物、短生育期作物种子调剂和技术指导方案制定，确保土壤墒情好转后能及时播上生育期适宜的作物；结合适播作物生育期，改种杂粮、杂豆等抗旱能力强的作物，或改种青贮玉米、鲜食玉米等生育期短的作物，有效规避春旱影响。据气象部门预计，辽宁全省很快将迎来一次全省性降水，主要出现在12日午后—13日白天，辽西等土壤缺墒地区农户宜根据当地实际情况，适时提前开展抢墒播种。'
    address = ''
    placeList = []
    toplaceList = []
    delplaceList = []
    count = 0
    words, ners = fool.analysis(title_str)
    for itemSun in ners[0]:
        if itemSun[2] == 'location':
            if itemSun[3] in address:
                continue
            else:
                try:
                    geocode(itemSun[3])
                    placeList.append(itemSun[3])
                except:
                    continue

    for item in placeList:
        location_str = [item]
        dfList = cpca.transform(location_str)
        addList = dfList.values
        if addList[0][0] == '':
            toplaceList.append(item)
            continue
        addPlace = addList[0][0] + addList[0][1] + addList[0][2] + addList[0][3]
        toplaceList.append(addPlace)
    for item1 in toplaceList:
        for item2 in toplaceList:
            if item1 in item2:
                count = count + 1
            if count > 1:
                delplaceList.append(item1)
                break
        count = 0
    for item3 in delplaceList:
        toplaceList.remove(item3)
    return toplaceList

def geocode(address):
    parameters = {'address': address, 'key': 'f6922b393df061ffff5b3c61529ce7d0'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    jwd = (answer['geocodes'][0]['location']).split(',')
    return jwd



print(place())





