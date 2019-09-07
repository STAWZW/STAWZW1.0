# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:01:57 2019

@author: 86183
"""
import cpca
import fool
import geocoder
import requests

#------------------------------------------------------------------------------
#----------------------多地址灾害-----------------------------------------------
def placeMany(originalText):
    placeList = []
    domesticList = []
    foreignList = []
    dprovinceList = []
    dcountryList = []
    fprovinceList = []
    fcountryList = []
    words, ners = fool.analysis(originalText)
    for itemSun in ners[0]:
        if itemSun[2] == 'location':
            if itemSun[3] in placeList:
                continue
            else:
                placeList.append(itemSun[3])
    for item in placeList:
        location_str = [item]
        dfList = cpca.transform(location_str, cut=False)
        addList = dfList.values
        addPlace = addList[0][0] + addList[0][1] + addList[0][2]
        if addPlace != '':
            if addList[0][0] == addList[0][1]:
                addPlace = addList[0][1] + addList[0][2]
            dcountryList.append('中国')
            dprovinceList.append(addList[0][0])
            domesticList.append(addPlace)
        else:
            foreignList.append(item)
            fcountryList.append('')
            fprovinceList.append('')
    if domesticList != []:
        setList =  Deduplication(domesticList, dprovinceList, dcountryList)
        setLists = latlngFunction(setList)
    else:
        setList = Deduplication(foreignList, fprovinceList, fcountryList)
        setLists = latlngFunction(setList)
    if setLists[0] == '':
        return placeSingle(originalText)
    else:
        return setLists

def Deduplication(placeList, provinceList, countryList):
    ccountry = []
    cprovince = []
    cplaceList = []
    count = 0
    for item1,item3,item4 in zip(placeList, provinceList, countryList):
        for item2 in placeList:
            if item1 in item2:
                count = count + 1
        if count > 1:
            count = 0
            continue
        ccountry.append(item4)
        cprovince.append(item3)
        cplaceList.append(item1)
    return cplaceList,cprovince,ccountry

def latlngFunction(setList):
    placeList = []
    provinceList = []
    countryList = []
    latList = []
    lngList = []
    for item1,item2,item3 in zip(setList[0], setList[1], setList[2]):
        if item3 == '中国':
            lnglat = geocode(item1)
            placeList.append(item1)
            provinceList.append(item2)
            countryList.append(item3)
            latList.append(str(round(lnglat[1],2)))
            lngList.append(str(round(lnglat[0],2)))
        else:
            addreJson = geocoder.arcgis(item1)
            if addreJson.latlng == None:
                continue
            if ((addreJson.address).split(','))[0] in placeList:
                continue
            placeList.append(((addreJson.address).split(','))[0])
            provinceList.append('')
            countryList.append('')
            latList.append(str(round(addreJson.lat,5)))
            lngList.append(str(round(addreJson.lng,5)))
    place = ','.join(placeList)
    province = ','.join(provinceList)
    country = ','.join(countryList)
    lat = ','.join(latList)
    lng = ','.join(lngList)
    return place,lng,lat,province,country

#------------------------------------------------------------------------------
#----------------------单地址灾害-----------------------------------------------

def placeSingle(text):
    placeList = []
    placeLists = []
    provinceList = []
    longitudeList = []
    latitudeList = []
    words, ners = fool.analysis(text)
    for itemSun in ners[0]:
        if itemSun[2] == 'location':
            title_str = [itemSun[3]]
            df = cpca.transform(title_str, cut=False)
            placenmpy = df.values
            places = placenmpy[0][0] + placenmpy[0][1] + placenmpy[0][2]       #发生地点
            if places != '':
                if placenmpy[0][0] == placenmpy[0][1]:
                    places = placenmpy[0][1] + placenmpy[0][2]
                placeList.append(places)
                provinceList.append(placenmpy[0][0])
            else:
                places = geocoder.arcgis(itemSun[3])
                if places.latlng == None:
                    continue
                placeLists.append(places.address)
                longitudeList.append(str(round(places.lng,2)))
                latitudeList.append(str(round(places.lat,2)))
    if placeList != []:
        place = max(placeList, key=placeList.count)
        llat = geocode(place)
        longitude = llat[0]                                                    #地点经度
        latitude = llat[1]
        indexdata = placeList.index(place)
        country = '中国'
        province = provinceList[indexdata]
        return place,longitude,latitude,province,country
    else:
        place = max(placeLists, key=placeLists.count)
        indexdata = placeLists.index(place)
        country = ''
        province = ''
        longitude = longitudeList[indexdata]
        latitude = latitudeList[indexdata]
        return place,longitude,latitude,province,country

#------------------------------------------------------------------------------
#----------------公共类---------------------------------------------------------

def geocode(address):
    parameters = {'address': address, 'key': '708b95575abc7484f5ced467ddd17574'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    latlng = (answer['geocodes'][0]['location']).split(',')
    lng = float(latlng[0])
    lat = float(latlng[1])
    return lng,lat

