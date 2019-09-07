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

    def connectPostgre(self):
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def insertData(self):
        textList = []
        try:
            sqlExit = "SELECT originalText FROM disasterinfo"
            self.cursor.execute(sqlExit)
        except:
            self.conn.rollback()                                            #注意回滚
            print('select mysql error.', my_title)
        selectText = self.cursor.fetchall()
        if selectText != []:
            for item in selectText:
                textList.append(item[0])
        return textList

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()