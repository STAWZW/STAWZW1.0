# -*- coding: utf-8 -*-
"""
Created on Thu May 30 18:08:42 2019

@author: 86183
"""

import psycopg2

class PostgreCommand(object):

    def __init__(self):
          self.host = "192.168.1.171"
          self.port = 5432                                                        # 端口号
          self.user = "postgres"                                                  # 用户名
          self.password = "postgres"                                              # 密码
          self.database = "disasterinfodb"                                        # 库
          self.table = "disasterinfo"                                             # 表

#        self.host = "210.77.79.194"
#        self.port = 5432                                                        # 端口号
#        self.user = "disaster"                                                  # 用户名
#        self.password = "disaster@crensed"                                      # 密码
#        self.database = "disaster"                                              # 库

    def connectPostgre(self):
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def insertData(self, my_dict,my_dictSun,my_title):
            try:
                sqlExit = "SELECT id FROM disasterinfo  WHERE title = '%s'" % (my_dict['title'])
                self.cursor.execute(sqlExit)
            except:
                self.conn.rollback()                                            #注意回滚
                print('select mysql error.', my_title)
            selectId = self.cursor.fetchall()
            if selectId != []:
                print("数据已存在,准备更新数据", my_title)
                return 0
                # sqlId = selectId[0][0]
                # sql = ''
                # colsList = list(my_dict.keys())
                # for key in colsList:
                #     if key == 'id' or key == 'title' or key == 'disasterid' or key == 'source':
                #         continue
                #     sql =sql + key + "='" + my_dict[key] + "',"
                # sql = sql.strip(',')
                # update_sql = "UPDATE disasterinfo SET %s WHERE id=%s" % (sql,sqlId)
                # try:
                #     self.cursor.execute(update_sql)
                #     self.conn.commit()
                #     return 0
                # except:
                #     self.conn.rollback()                                        #注意回滚
                #     print('update mysql error.', my_title)
            cols = ','.join(my_dict.keys())
            values = "','".join(my_dict.values())
            sqlInsert = "INSERT INTO disasterinfo (%s) VALUES (%s)" % (cols, "'" + values + "'")
            colsSun = ','.join(my_dictSun.keys())
            valuesSun = "','".join(my_dictSun.values())
            sqlInsertSun = "INSERT INTO disasterdetail (%s) VALUES (%s)" % (colsSun, "'" + valuesSun + "'")
            try:
                self.cursor.execute(sqlInsert)
                self.conn.commit()
            except psycopg2.Error as e:
                self.conn.rollback()                                            #注意回滚
                print('insert mysql error.', my_title)
                print(e)
                return 2
            try:
                self.cursor.execute(sqlInsertSun)
                self.conn.commit()
            except psycopg2.Error as e:
                self.conn.rollback()                                            #注意回滚
                print('insertSun mysql error.', my_title)
                print(e)
                return 2
            return 1


    def closePostgre(self):
        self.cursor.close()
        self.conn.close()