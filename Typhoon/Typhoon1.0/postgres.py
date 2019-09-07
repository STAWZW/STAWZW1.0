# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:08:42 2019

@author: 86183
"""

import psycopg2

class PostgreCommand(object):

    def __init__(self):
          self.host = "118.190.202.102"
          self.port = 5432
          self.user = "postgres"
          self.password = "postgres"
          self.database = "disasterinfodb"

    def connectPostgre(self):
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            self.cursor = self.conn.cursor()
        except:
            print('connect error.')

    def windFarmInsertData(self, my_dict):
        try:
            sqlExit = "SELECT id FROM realdata WHERE occurtime = '%s'" % (my_dict['occurtime'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('windFarmInsertData select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO realdata (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('windFarmInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('windFarmInsertData insert error.')
                print(e)
        else:
            print("windFarmInsertData数据存在不需要更新")

    def historyInsertData(self, my_dict):
        try:
            sqlExit = "SELECT id FROM historydata WHERE args = '%s'" % (my_dict['args'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('historyInsertData select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO historydata (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('historyInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('historyInsertData insert error.')
                print(e)
        else:
            update_sql = "UPDATE historydata SET typhoon_data='%s', update_time='%s' WHERE args='%s'" % (my_dict['typhoon_data'], my_dict['update_time'], my_dict['args'])
            try:
                self.cursor.execute(update_sql)
                self.conn.commit()
                print('historyInsertData数据更新成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('historyInsertData update error.')
                print(e)
                
    def previewInsertData(self, my_dict):
        try:
            sqlExit = "SELECT id FROM previewdata WHERE typhoon_id = '%s' AND rqsj = '%s'" % (my_dict['typhoon_id'], my_dict['rqsj'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('previewInsertData select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO previewdata (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('previewInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('previewInsertData insert error.')
                print(e)
        else:
            print("previewInsertData数据存在不需要更新")
    def previewInsertData_copy(self, my_dict):
        try:
            sqlExit = "SELECT id FROM previewdatas WHERE pid = '%s' AND forcast_country_name = '%s'" % (my_dict['pid'],my_dict['forcast_country_name'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('previewInsertData_copy select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO previewdatas (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('previewInsertData_copy数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('previewInsertData_copy insert error.')
                print(e)
        else:
            print("previewInsertData_copy数据存在不需要插入")
    
    def previewInsertData_del(self):
        try:
            delExit = "TRUNCATE TABLE previewdatas"
            self.cursor.execute(delExit)
            self.conn.commit()
            print('previewInsertData_copy 数据清空.')
        except:
            self.conn.rollback()
            print('previewInsertData_copy 数据清空失败.')
            
    def sckjCloudInsertData(self, my_dict):
        try:
            sqlExit = "SELECT id FROM cloudchart WHERE c_name = '%s'" % (my_dict['c_name'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('sckjCloudInsertData select error.')
        selectId = self.cursor.fetchall()
        valueList = []
        keyList = []
        if selectId == []:
            values = list(my_dict.values())
            keyss = list(my_dict.keys())
            for itemkeys,itemvalue in zip(keyss,values):
                if itemvalue != None:
                    keyList.append(itemkeys)
                    valueList.append(str(itemvalue))
            cols = ','.join(keyList)
            values = "','".join(valueList)
            sqlInsert = "INSERT INTO cloudchart (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('sckjCloudInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('sckjCloudInsertData insert error.')
                print(e)
        else:
            print("sckjCloudInsertData数据存在不需要插入")
            
    def sckjRadarInsertData(self, my_dict):
        try:
            sqlExit = "SELECT id FROM radarchart WHERE r_name = '%s'" % (my_dict['r_name'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('sckjRadarInsertData select error.')
        selectId = self.cursor.fetchall()
        valueList = []
        keyList = []
        if selectId == []:
            values = list(my_dict.values())
            keyss = list(my_dict.keys())
            for itemkeys,itemvalue in zip(keyss,values):
                if itemvalue != None:
                    keyList.append(itemkeys)
                    valueList.append(str(itemvalue))
            cols = ','.join(keyList)
            values = "','".join(valueList)
            sqlInsert = "INSERT INTO radarchart (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('sckjRadarInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('sckjRadarInsertData insert error.')
                print(e)
        else:
            print("sckjRadarInsertData数据存在不需要插入")

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()