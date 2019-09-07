# -*- coding: utf-8 -*-

import pymysql

class MySQLCommand(object):

    def __init__(self):
        self.host = "118.190.202.102"
        self.port = 3306
        self.user = "typhoon"
        self.password = "typhoon123"
        self.db = "spidertyphoon" 
        self.table = "typhoon" 

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def selectData(self):
        sqlExit = "SELECT * FROM typhoon"
        self.cursor.execute(sqlExit)
        sqldata = list(self.cursor.fetchall())
        return sqldata

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例