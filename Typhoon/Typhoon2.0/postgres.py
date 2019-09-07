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

    def allTyphoonInsertData(self, my_dict):
        try:
            sqlExit = "SELECT typhoon_id FROM typhooninfo WHERE typhoon_id = '%s'" % (my_dict['typhoon_id'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('allTyphoonInsertData select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO typhooninfo (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('allTyphoonInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allTyphoonInsertData insert error.')
                print(e)
        else:
            sqlupdata = "UPDATE typhooninfo SET typhon_status='%s', update_time='%s' WHERE typhoon_id = '%s'" % (my_dict['typhon_status'], my_dict['update_time'], my_dict['typhoon_id'])
            try:
                self.cursor.execute(sqlupdata)
                self.conn.commit()
                print('allTyphoonInsertData数据更新成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allTyphoonInsertData updata error.')
                print(e)

    def allHistorySelectData(self):
        try:
            #sqlExit = "SELECT typhoon_id FROM typhooninfo WHERE typhoon_year >= '2019'"     #近五年的所有数据id,由于数据过多，现只取19年的
            #sqlExit = "SELECT typhoon_id FROM typhooninfo WHERE typhoon_id >= '201909'"
            sqlExit = "SELECT typhoon_id FROM typhooninfo ORDER BY typhoon_id DESC LIMIT 3"
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('allHistorySelectData select error.')
        selectId = self.cursor.fetchall()
        return selectId

    def allHistoryInsertData_json(self, my_dict):
        try:
            sqlExit = "SELECT id FROM historydatas WHERE pid = '%s'" % (my_dict['pid'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('allHistoryInsertData_json select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO historydatas (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('allHistoryInsertData_json数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allHistoryInsertData_json insert error.')
                print(e)
        else:
           print('allHistoryInsertData数据存在不需要更新.')

    def allHistoryInsertData_str(self, my_dict):
        try:
            sqlExit = "SELECT id FROM historydata WHERE args = '%s'" % (my_dict['args'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('allHistoryInsertData_str select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO historydata (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('allHistoryInsertData_str数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allHistoryInsertData_str insert error.')
                print(e)
        else:
            update_sql = "UPDATE historydata SET typhoon_data='%s', update_time='%s' WHERE args='%s'" % (my_dict['typhoon_data'], my_dict['update_time'], my_dict['args'])
            try:
                self.cursor.execute(update_sql)
                self.conn.commit()
                print('allHistoryInsertData_str数据更新成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allHistoryInsertData_str update error.')
                print(e)

    def allPreviewInsertData(self, my_dict):
        try:
            sqlExit = "SELECT id FROM previewdatas WHERE pid = '%s' AND forcast_country_name = '%s'" % (my_dict['pid'],my_dict['forcast_country_name'])
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()
            print('allPreviewInsertData select error.')
        selectId = self.cursor.fetchall()
        if selectId == []:
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO previewdatas (%s) VALUES (%s)" % (cols, "'" + values + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
                print('allPreviewInsertData数据插入成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allPreviewInsertData insert error.')
                print(e)
        else:
            sqlId = selectId[0][0]
            sql = ''
            colsList = list(my_dict.keys())
            for key in colsList:
                sql =sql + key + "='" + my_dict[key] + "',"
            sql = sql.strip(',')
            update_sql = "UPDATE previewdatas SET %s WHERE id=%s" % (sql,sqlId)
            try:
                self.cursor.execute(update_sql)
                self.conn.commit()
                print('allPreviewInsertData数据更新成功！')
            except psycopg2.Error as e:
                self.conn.rollback()
                print('allPreviewInsertData update error.')
                print(e)

    def deletPreviewInsertData(self, current_time):
        sqlDelet = "DELETE FROM previewdatas WHERE  rqsj > '%s'" % (current_time)
        try:
            self.cursor.execute(sqlDelet)
            self.conn.commit()
            print('deletPreviewInsertData数据删除成功！')
        except psycopg2.Error as e:
            self.conn.rollback()
            print('deletPreviewInsertData insert error.')
            print(e)

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()