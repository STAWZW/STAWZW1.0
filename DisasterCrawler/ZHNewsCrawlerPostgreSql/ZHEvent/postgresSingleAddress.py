# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:08:42 2019

@author: WZW
"""

import psycopg2
import random
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

    def singleAddressEvent(self,disasterid,eventHead,timeLimit):
            try:
                selectSql = "SELECT id,longitude,latitude,occurtime FROM disasterinfo  WHERE affairid is NULL AND disasterid = '%s'" % (disasterid)
                self.cursor.execute(selectSql)
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)
            selectILLO = self.cursor.fetchall()
            if selectILLO != []:
                for item in selectILLO:
                    try:
                        id = item[0]
                        longitude = item[1]
                        latitude = item[2]
                        occurtime = item[3]
                        if longitude == '' and latitude == '':
                            continue
                        lon = longitude[0:longitude.rfind('.', 1)]
                        lat = latitude[0:latitude.rfind('.', 1)]
                        eventTime = str(occurtime)[0:7].replace('-','')
                        try:
                            selectSqlSun = "SELECT affairid,occurtime from disasterinfo WHERE longitude LIKE '{lon}%' AND latitude LIKE '{lat}%' AND affairid IS NOT NULL AND disasterid = '{disa}'".format(lon = lon, lat = lat, disa = disasterid)
                            self.cursor.execute(selectSqlSun)
                        except psycopg2.Error as error:
                            self.conn.rollback()
                            print(error)
                        selectAO = self.cursor.fetchall()
                        if selectAO != []:
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

    def singleTpythoonEvent(self,disasterid,eventHead,timeLimit):
            try:
                selectSql = "SELECT id,place,longitude,latitude,occurtime FROM disasterinfo  WHERE affairid is NULL AND disasterid = '%s'" % (disasterid)
                self.cursor.execute(selectSql)
            except psycopg2.Error as error:
                self.conn.rollback()
                print(error)
            selectILLO = self.cursor.fetchall()
            if selectILLO != []:
                for item in selectILLO:
                    try:
                        id = item[0]
                        place = item[1]
                        longitude = item[2]
                        latitude = item[3]
                        if longitude == '' and latitude == '':
                            continue
                        lon = longitude[0:longitude.rfind('.', 1)]
                        lat = latitude[0:latitude.rfind('.', 1)]
                        occurtime = item[4]
                        eventTime = str(occurtime)[0:7].replace('-','')
                        delTime = datetime.timedelta(days = timeLimit)
                        lowTime = occurtime - delTime
                        highTime = occurtime + delTime
                        try:
                            selectSqlSun = "SELECT affairid,longitude,latitude from disasterinfo WHERE occurtime >= '%s' AND occurtime <= '%s' AND affairid IS NOT NULL AND disasterid = '%s'" % (lowTime,highTime,disasterid)
                            self.cursor.execute(selectSqlSun)
                        except psycopg2.Error as error:
                            self.conn.rollback()
                            print(error)
                        selectALL = self.cursor.fetchall()
                        if selectALL != []:
                            print("存在相同新闻报道")
                            minLng = 10
                            minLat = 10
                            for item in selectALL:
                                affairidFather = item[0]
                                longitudeFather = float(item[1])
                                latitudeFather = float(item[2])
                                lngDif = longitudeFather - float(longitude)
                                latDif = latitudeFather - float(latitude)
                                if -minLng < lngDif < minLng and -minLat < latDif < minLat:
                                    minLng = lngDif
                                    minLat = latDif
                                    updateSql = "UPDATE disasterinfo SET affairid = '%s' WHERE id = %s" % (affairidFather,id)
                                    try:
                                        self.cursor.execute(updateSql)
                                        self.conn.commit()
                                        print('存在相同新闻报道,且已经更新事件编号')
                                    except psycopg2.Error as error:
                                        self.conn.rollback()
                                        print(error)
                            if minLng == 10 or minLat == 10:
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
            print('创建事件编号，并插入数据库')
        except psycopg2.Error as error:
            self.conn.rollback()
            print(error)

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()
