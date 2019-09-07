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

    def manyAddressEvent(self,disasterid,eventHead,timeLimit):
            all_originaltext = []
            all_affairidFather = []
            try:
                selectSql = "SELECT id,originaltext,longitude,latitude,occurtime,regional FROM disasterinfo  WHERE affairid is NULL AND disasterid = '%s'" % (disasterid)
                self.cursor.execute(selectSql)
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)
            selectIOLLO = self.cursor.fetchall()                            #获取灾害事件编号为空的新闻
            if selectIOLLO != []:                                           #如果存在灾害事件编号为空的新闻
                print("存在affairid为空的数据")
                for item in selectIOLLO:                                    #遍历新闻列表
                    try:
                        id = item[0]
                        originaltext = item[1]
                        longitude = item[2]
                        latitude = item[3]
                        occurtime = item[4]
                        regional = item[5]
                        if longitude == '' and latitude == '':
                            continue
                        lon = longitude[0:longitude.rfind('.', 1, 4)]
                        lat = latitude[0:latitude.rfind('.', 1, 4)]
                        eventTime = str(occurtime)[0:7].replace('-','')
                        if regional == '国内':                                   #如果为国内新闻利用文本相似匹配来判断
                            try:
                                selectSqlFather = "SELECT affairid,originaltext,occurtime from disasterinfo WHERE affairid IS NOT NULL AND disasterid = '%s'" % (disasterid)
                                self.cursor.execute(selectSqlFather)
                            except psycopg2.Error as error:
                                self.conn.rollback()
                                print(error)
                            selectAOO = self.cursor.fetchall()                   #获取灾害编号不为空的新闻
                            if selectAOO != []:                                  #如果存在灾害编号不为空的新闻
                                for item in selectAOO:                           #遍历新闻列表
                                    affairidFather = item[0]
                                    originaltextFather = item[1]
                                    occurtimeFather = item[2]
                                    timeDifference = abs((occurtime - occurtimeFather).days)
                                    if timeDifference < timeLimit:               #如果时间差小于timeLimit
                                        all_affairidFather.append(affairidFather)
                                        all_originaltext.append(originaltextFather)
                                if all_affairidFather != []:                     #如果存在灾害且时间差小于30天
                                    all_originaltext.append("干扰文本")
                                    similarityRateList = textMatching.textAnalysis(all_originaltext,originaltext)   #文本相似度匹配
                                    if similarityRateList[1] > 0.65:                                                #相似率大于0.65合格
                                        affairid = all_affairidFather[similarityRateList[0]]
                                        updateSql = "UPDATE disasterinfo SET affairid = '%s' WHERE id = %s" % (affairid,id)
                                        try:
                                            self.cursor.execute(updateSql)
                                            self.conn.commit()
                                            print('获取相同新闻时间编号，并更新入数据库')
                                        except psycopg2.Error as error:
                                            self.conn.rollback()
                                            print( error)
                                    else:                                                                           #如果匹配相似度较低则新建事件
                                        self.eventCreate(id,eventHead,eventTime,lon,lat)                            
                                    all_affairidFather.clear()
                                    all_originaltext.clear()
                                else:                                                                               #如果不存在时间差小于30天的相同类型灾害则则新建事件
                                    self.eventCreate(id,eventHead,eventTime,lon,lat)
                            else:                                                                                   #如果不存在灾害事件编号不为空的新闻
                                self.eventCreate(id,eventHead,eventTime,lon,lat)
                        else:                                                                                        #如果为国外新闻利用经纬度和事件发生事件来判断
                            try:
                                selectSqlSun = "SELECT affairid,occurtime from disasterinfo WHERE longitude LIKE '{lon}%' AND latitude LIKE '{lat}%' AND affairid IS NOT NULL AND disasterid = '{disa}'".format(lon = lon, lat = lat, disa = disasterid)
                                self.cursor.execute(selectSqlSun)
                            except psycopg2.Error as error:
                                self.conn.rollback()
                                print(error)
                            selectAO = self.cursor.fetchall()
                            if selectAO != []:
                                print("存在相同新闻报道")
                                minTime = timeLimit
                                for item in selectAO:
                                    affairidSun = item[0]
                                    occurtimeSun = item[1]
                                    timeDifference = abs((occurtime - occurtimeSun).days)
                                    if timeDifference < minTime:
                                        minTime = timeDifference
                                        updateSqlSunSub = "UPDATE disasterinfo SET affairid = '%s' WHERE id = %s" % (affairidSun,id)
                                        try:
                                            self.cursor.execute(updateSqlSunSub)
                                            self.conn.commit()
                                            print('存在相同新闻报道,且已经更新事件编号')
                                        except psycopg2.Error as error:
                                            self.conn.rollback()
                                            print(error)
                                if minTime == timeLimit:
                                    self.eventCreate(id,eventHead,eventTime,lon,lat)
                            else:
                                self.eventCreate(id,eventHead,eventTime,lon,lat)
                    except Exception as error:
                        print(error)
                        continue

    def eventCreate(self,id,eventHead,eventTime,lon,lat):
        print("不存在相同新闻报道,加入灾害事件编号")
        rando = str(int(random.uniform(10, 9999)))
        affairid = eventHead + eventTime + lon + lat + rando
        updateSql = "UPDATE disasterinfo SET affairid = '%s' WHERE id = %s" % (affairid,id)
        try:
            self.cursor.execute(updateSql)
            self.conn.commit()
            print('创建时间编号，并插入数据库')
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()