# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:08:42 2019

@author: WZW
"""
import psycopg2
import random
import textMatching
import datetime
import fullPath
import re
import jieba.analyse as anls

class PostgreCommand(object):

    def __init__(self):
        self.host = "192.168.1.171"
        self.port = 5432  # 端口号
        self.user = "postgres"  # 用户名
        self.password = "postgres"  # 密码
        self.database = "disasterinfodb"  # 库
        self.table = "disasterinfo"  # 表

        # self.host = "210.77.79.194"
        # self.port = 5432                                                        # 端口号
        # self.user = "disaster"                                                  # 用户名
        # self.password = "disaster@crensed"                                      # 密码
        # self.database = "disaster"                                              # 库

    def connectPostgre(self):
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')
    def updataLyricalEvent(self):
        try:
            # selectSqlAll = "SELECT affairid from disasterinfo" 
            selectSqlAll = 'SELECT affairid,disasterid FROM disasterinfo ORDER BY id DESC LIMIT 100'
            self.cursor.execute(selectSqlAll)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectAll = self.cursor.fetchall()
        disasteridManyList = ['10112','10107','10110','10110','10111','10105','10101']
        disasteridSingleList = ['10010','10502','10002','10001','1000103','1000104','10003','10306','10205','10102','1000101','10108','10115','10302','10116','10005']
        for item in selectAll:
            if item[0] != None:
                if item[1] in disasteridManyList:
                    self.LyricalEventMany(item[0])
                elif item[1] in disasteridSingleList:
                    self.LyricalEventSingle(item[0])
                else:
                    print('updataLyricalEvent灾害编号未定义')
    def LyricalEventMany(self,affairid):
        idList = []
        releasetimeList = []
        originaltextList = []
        sourceList = []
        placeList = []
        occurtimeList = []
        current_websiteList = []
        longitudeList = []
        latitudeList = []
        strengthList = []
        countryList = []
        porvinceList = []
        injuredList = []
        deathList = []
        lossList = []
        titleList = []
        nameValueList = []
        introductionList = []
        sourceFather = []
        sourceSun = []
        sourceId = []
        provinceList = []
        provinceWList = []
        porvinceStrList = []
        isreleasetimeList = []
        linkList = []
        sourceLink = []
        isrellonandlatList = []
        try:
            selectSqlAll = "SELECT id,disasterid,releasetime,originaltext,source,place,occurtime,current_website,longitude,latitude,strength,country,province,injured,death,loss,title,isreleasetime,link,isrellonandlat from disasterinfo WHERE affairid = '%s'" % (affairid)
            self.cursor.execute(selectSqlAll)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectAll = self.cursor.fetchall()
        for item in selectAll:                                  #获取每个事件的各个字段
            idList.append(str(item[0]))
            disasterid = item[1]
            releasetimeList.append(item[2])
            originaltextList.append(item[3])
            sourceList.append(item[4])
            placeList.append(item[5])
            occurtimeList.append(item[6])
            current_websiteList.append(item[7])
            longitudeList.append(item[8])
            latitudeList.append(item[9])
            strengthList.append(item[10])
            countryList.append(item[11])
            porvinceList.append(item[12])
            injuredList.append(item[13])
            deathList.append(item[14])
            lossList.append(item[15])
            titleList.append(item[16])
            isreleasetimeList.append(item[17])
            linkList.append(item[18])
            isrellonandlatList.append(item[19])
        try:
            selectSqlName = "SELECT name from disastertype WHERE disasterid='%s'" % (disasterid)
            self.cursor.execute(selectSqlName)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectName = (self.cursor.fetchone())[0]
        testTime = occurtimeList
        testTime.sort()
        for item in testTime:
            subscript = occurtimeList.index(item)
            sourceFather.append(sourceList[subscript])
            sourceSun.append(current_websiteList[subscript])
            sourceId.append(idList[subscript])
            sourceLink.append(linkList[subscript])
        currentSubscript = occurtimeList.index(testTime[0])     #获取最早新闻的下标
        disasterinfo_id = (',').join(idList)                    #获取所有新闻的id
        title = titleList[currentSubscript]                     #获取最早新闻的标题
        isreleasetime = isreleasetimeList[currentSubscript]     #获取最早新闻的时间标签
        occurtime = occurtimeList[currentSubscript]             #获取最早新闻的时间
        source = sourceList[currentSubscript]                   #最早新闻报道来源
        place = placeList[currentSubscript]                     #获取最早新闻的地点
        longitude = longitudeList[currentSubscript]             #获取最早新闻的经度
        latitude = latitudeList[currentSubscript]               #获取最早新闻的纬度
        strength = strengthList[currentSubscript]               #获取最早新闻的强度
        country = countryList[currentSubscript]                 #获取最早新闻的国家
        porvince = porvinceList[currentSubscript]               #获取最早新闻的省份
        isrellonandlat = isrellonandlatList[currentSubscript]   #获取最早新闻的经纬度标签
        link = linkList[currentSubscript]                       #获取最早新闻的连接
        injuredList.sort()
        injured = injuredList[-1]                               #获取最新的受伤人数
        deathList.sort()
        death = deathList[-1]                                   #获取最新的死亡人数
        lossList.sort()
        loss = lossList[-1]                                     #获取最新经济损失
        originaltext = ('。').join(originaltextList)             #灾害新闻内容
        for words, weights in anls.extract_tags(originaltext, topK=80, withWeight=True):
            introductionList.append(words)
            weights = round(weights*100000)
            nameValue = "{'name':'" + words + "','value':'" + str(weights) + "'}"
            nameValueList.append(nameValue)
        someKeywords = ('、').join(introductionList[:6])                                  #标题中的6个关键词
        affair_keyword = ('[' + (',').join(nameValueList) + ']').replace("'","''")       #关键词和权重组成JSON格式
        introduction = '本报告围绕关键词“' + someKeywords + '”，对' + str(occurtime) + '在' + place + '发生的' + selectName + '相关的新闻报道信息进行了深入分析。该事件源头于' + str(occurtime) + '发布在' + source + '上，题名为：『' + title + '』。根据后续报道，详细报告如下。'
        porvince_str = porvince.replace(',','')
        if porvince_str != '':
            porvincelist0 = porvince.split(',')
            porvincelist1 = list(filter(None, porvincelist0))
            porvincelist2 = list(set(porvincelist1))
            provinceStr = '、'.join(porvincelist2)
        else:
            provinceStr = place.replace(',','、')
        header = provinceStr + selectName
        affair_transway = fullPath.getPath(header,sourceFather,sourceSun,sourceId,sourceLink) #灾害传播路径
        lyricalAffairid = affairid                                                       #事件编号
        lyricalAffairname = header                                                       #事件分析标题
        lyricalIntroduction = introduction                                               #事件相关简介
        lyricalAffair_keyword = affair_keyword                                           #事件关键词云
        lyricalAffair_transway = affair_transway                                         #事件传播路径
        lyricalDisasterinfo_id = disasterinfo_id                                         #事件相关新闻id
        lyricalDisasterid = disasterid                                                   #事件灾害类型
        lyricalOccurtime = occurtime                                                     #事件发生事件
        lyricalLongitude = longitude                                                     #事件地点经度
        lyricalLatitude = latitude                                                       #事件地点纬度
        lyricalPlace = place                                                             #事件发生地点
        lyricalStrength = strength                                                       #事件灾害强度
        lyricalCountry = country                                                         #事件发生国家
        lyricalProvince = porvince                                                       #事件发生一级行政区划
        lyricalInjured = injured                                                         #事件受伤人数
        lyricalDeath = death                                                             #事件死亡人数
        lyricalLoss = loss                                                               #事件经济损失
        lyricalisreleasetime = isreleasetime
        lyricalisrellonandlat = isrellonandlat                                           #经纬度标签
        lyricalLink = link                                                               #事件新闻连接
        try:
            selectSql = "SELECT * from disasteraffair WHERE affairid = '%s'" % (lyricalAffairid)
            self.cursor.execute(selectSql)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectEvent = self.cursor.fetchone()
        if selectEvent == None:
            insertSql = "INSERT INTO disasteraffair(affairid,affairname,affairintroduction,affair_keyword,affair_transway,disasterinfo_id,disasterid,occurtime,longitude,latitude,place,strength,country,province,injured,death,loss,isreleasetime,isrellonandlat,link) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (lyricalAffairid,lyricalAffairname,lyricalIntroduction,lyricalAffair_keyword,lyricalAffair_transway,lyricalDisasterinfo_id,lyricalDisasterid,lyricalOccurtime,lyricalLongitude,lyricalLatitude,lyricalPlace,lyricalStrength,lyricalCountry,lyricalProvince,lyricalInjured,lyricalDeath,lyricalLoss,lyricalisreleasetime,lyricalisrellonandlat,lyricalLink)
            try:
                self.cursor.execute(insertSql)
                self.conn.commit()
                print('LyricalEvent插入数据成功')
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)
        else:
            updateSql = "UPDATE disasteraffair SET affairintroduction = '%s',affair_keyword = '%s',affair_transway = '%s',disasterinfo_id = '%s',occurtime = '%s',injured = '%s',death = '%s',loss = '%s' WHERE affairid = '%s'" % (lyricalIntroduction,lyricalAffair_keyword,lyricalAffair_transway,lyricalDisasterinfo_id,lyricalOccurtime,lyricalInjured,lyricalDeath,lyricalLoss,lyricalAffairid)
            try:
                self.cursor.execute(updateSql)
                self.conn.commit()
                print('LyricalEvent更新数据成功')
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)

    def LyricalEventSingle(self,affairid):
        idList = []
        releasetimeList = []
        originaltextList = []
        sourceList = []
        placeList = []
        occurtimeList = []
        current_websiteList = []
        longitudeList = []
        latitudeList = []
        strengthList = []
        countryList = []
        porvinceList = []
        injuredList = []
        deathList = []
        lossList = []
        titleList = []
        nameValueList = []
        introductionList = []
        sourceFather = []
        sourceSun = []
        sourceId = []
        isreleasetimeList = []
        linkList = []
        sourceLink = []
        isrellonandlatList = []
        try:
            selectSqlAll = "SELECT id,disasterid,releasetime,originaltext,source,place,occurtime,current_website,longitude,latitude,strength,country,province,injured,death,loss,title,isreleasetime,link,isrellonandlat from disasterinfo WHERE affairid = '%s'" % (affairid)
            self.cursor.execute(selectSqlAll)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectAll = self.cursor.fetchall()
        for item in selectAll:                                  #获取每个事件的各个字段
            idList.append(str(item[0]))
            disasterid = item[1]
            releasetimeList.append(item[2])
            originaltextList.append(item[3])
            sourceList.append(item[4])
            placeList.append(item[5])
            occurtimeList.append(item[6])
            current_websiteList.append(item[7])
            longitudeList.append(item[8])
            latitudeList.append(item[9])
            strengthList.append(item[10])
            countryList.append(item[11])
            porvinceList.append(item[12])
            injuredList.append(item[13])
            deathList.append(item[14])
            lossList.append(item[15])
            titleList.append(item[16])
            isreleasetimeList.append(item[17])
            linkList.append(item[18])
            isrellonandlatList.append(item[19])
        try:
            selectSqlName = "SELECT name from disastertype WHERE disasterid = '%s'" % (disasterid)
            self.cursor.execute(selectSqlName)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectName = (self.cursor.fetchone())[0]
        testTime = occurtimeList
        testTime.sort()
        for item in testTime:
            subscript = occurtimeList.index(item)
            sourceFather.append(sourceList[subscript])
            sourceSun.append(current_websiteList[subscript])
            sourceId.append(idList[subscript])
            sourceLink.append(linkList[subscript])
        currentSubscript = occurtimeList.index(testTime[0])     #获取最早新闻的下标
        disasterinfo_id = (',').join(idList)                    #获取所有新闻的id
        title = titleList[currentSubscript]                     #获取最早新闻的标题
        occurtime = occurtimeList[currentSubscript]             #获取最早新闻的时间
        source = sourceList[currentSubscript]                   #最早新闻报道来源
        place = placeList[currentSubscript]                     #获取最早新闻的地点
        longitude = longitudeList[currentSubscript]             #获取最早新闻的经度
        latitude = latitudeList[currentSubscript]               #获取最早新闻的纬度
        strength = strengthList[currentSubscript]               #获取最早新闻的强度
        country = countryList[currentSubscript]                 #获取最早新闻的国家
        porvince = porvinceList[currentSubscript]               #获取最早新闻的省份
        isreleasetime = isreleasetimeList[currentSubscript]     #获取最早新闻的时间标签
        isrellonandlat = isrellonandlatList[currentSubscript]   #获取最早新闻的经纬度标签
        link = linkList[currentSubscript]                       #获取最早新闻的连接
        injuredList.sort()
        injured = injuredList[-1]                               #获取最新的受伤人数
        deathList.sort()
        death = deathList[-1]                                   #获取最新的死亡人数
        lossList.sort()
        loss = lossList[-1]                                     #获取最新经济损失
        originaltext = ('。').join(originaltextList)             #灾害新闻内容
        for words, weights in anls.extract_tags(originaltext, topK=80, withWeight=True):
            introductionList.append(words)
            weights = round(weights*100000)
            nameValue = "{'name':'" + words + "','value':'" + str(weights) + "'}"
            nameValueList.append(nameValue)
        someKeywords = ('、').join(introductionList[:6])                                  #标题中的6个关键词
        affair_keyword = ('[' + (',').join(nameValueList) + ']').replace("'","''")       #关键词和权重组成JSON格式
        introduction = '本报告围绕关键词“' + someKeywords + '”，对' + str(occurtime) + '在' + place + '发生的' + selectName + '灾害相关的新闻报道信息进行了深入分析。该事件源头于' + str(occurtime) + '发布在' + source + '上，题名为：『' + title + '』。根据后续报道，详细报告如下。'
        header = place + selectName
        affair_transway = fullPath.getPath(header,sourceFather,sourceSun,sourceId,sourceLink) #灾害传播路径
        lyricalAffairid = affairid                                                       #事件编号
        lyricalAffairname = header                                                       #事件分析标题
        lyricalIntroduction = introduction                                               #事件相关简介
        lyricalAffair_keyword = affair_keyword                                           #事件关键词云
        lyricalAffair_transway = affair_transway                                         #事件传播路径
        lyricalDisasterinfo_id = disasterinfo_id                                         #事件相关新闻id
        lyricalDisasterid = disasterid                                                   #事件灾害类型
        lyricalOccurtime = occurtime                                                     #事件发生事件
        lyricalLongitude = longitude                                                     #事件地点经度
        lyricalLatitude = latitude                                                       #事件地点纬度
        lyricalPlace = place                                                             #事件发生地点
        lyricalStrength = strength                                                       #事件灾害强度
        lyricalCountry = country                                                         #事件发生国家
        lyricalProvince = porvince                                                       #事件发生一级行政区划
        lyricalInjured = injured                                                         #事件受伤人数
        lyricalDeath = death                                                             #事件死亡人数
        lyricalLoss = loss                                                               #事件经济损失
        lyricalisreleasetime = isreleasetime                                             #时间标签
        lyricalisrellonandlat = isrellonandlat                                           #经纬度标签
        lyricalLink = link                                                               #事件新闻连接
        try:
            selectSql = "SELECT * from disasteraffair WHERE affairid = '%s'" % (lyricalAffairid)
            self.cursor.execute(selectSql)
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)
        selectEvent = self.cursor.fetchone()
        if selectEvent == None:
            insertSql = "INSERT INTO disasteraffair(affairid,affairname,affairintroduction,affair_keyword,affair_transway,disasterinfo_id,disasterid,occurtime,longitude,latitude,place,strength,country,province,injured,death,loss,isreleasetime,isrellonandlat,link) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (lyricalAffairid,lyricalAffairname,lyricalIntroduction,lyricalAffair_keyword,lyricalAffair_transway,lyricalDisasterinfo_id,lyricalDisasterid,lyricalOccurtime,lyricalLongitude,lyricalLatitude,lyricalPlace,lyricalStrength,lyricalCountry,lyricalProvince,lyricalInjured,lyricalDeath,lyricalLoss,lyricalisreleasetime,lyricalisrellonandlat,lyricalLink)
            try:
                self.cursor.execute(insertSql)
                self.conn.commit()
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)
        else:
            updateSql = "UPDATE disasteraffair SET affairintroduction = '%s',affair_keyword = '%s',affair_transway = '%s',disasterinfo_id = '%s',occurtime = '%s',injured = '%s',death = '%s',loss = '%s' WHERE affairid = '%s'" % (lyricalIntroduction,lyricalAffair_keyword,lyricalAffair_transway,lyricalDisasterinfo_id,lyricalOccurtime,lyricalInjured,lyricalDeath,lyricalLoss,lyricalAffairid)
            try:
                self.cursor.execute(updateSql)
                self.conn.commit()
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()