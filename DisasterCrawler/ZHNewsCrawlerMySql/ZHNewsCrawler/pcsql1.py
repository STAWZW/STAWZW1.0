# -*- coding: utf-8 -*-

import pymysql
# 用来操作数据库的类
class MySQLCommand(object):
    # 类的初始化
    def __init__(self):
        self.host = "localhost"
        self.port = 3306  # 端口号
        self.user = "root"  # 用户名
        self.password = "root"  # 密码
        self.db = "crebas"  # 库
        self.table = "disasterinfo"  # 表

    # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    # 插入数据，插入之前先查询是否存在，如果存在就更新数据
    def insertData(self, my_dict,my_title):
        # 注意，这里查询的sql语句url=' %s '中%s的前后要有空格
        sqlExit = "SELECT id FROM disasterinfo  WHERE title = '%s'" % (my_dict['title'])
        res = self.cursor.execute(sqlExit)
        if res:  # res为查询到的数据条数如果大于0就代表数据已经存在
            print("数据已存在,准备更新数据", my_title)
            #--------------------------------
            sqlId = self.cursor.fetchall()[0][0]
            sql = ''
            colsList = list(my_dict.keys())
            #valuesList = list(my_dict.values())
            for key in colsList:
                if key == 'id' or key == 'title' or key == 'disasterid' or key == 'source':
                    continue
                sql =sql + key + "='" + my_dict[key] + "',"
            sql = sql.strip(',')
            update_sql = "UPDATE disasterinfo SET %s WHERE id=%s" % (sql,sqlId)
            #print(update_sql)
            result1 = self.cursor.execute(update_sql)
            self.conn.commit()
            if result1:
                print("数据更新成功")
            else:
                print("数据不需要更新")
            return 0
            #-----------------------------------------
        # 数据不存在才执行下面的插入操作
        try:
            cols = ','.join(my_dict.keys())#用，分割
            values = '","'.join(my_dict.values())
            sqlInsert = "INSERT INTO disasterinfo (%s) VALUES (%s)" % (cols, '"' + values + '"')
            #拼装后的sql如下
            # INSERT INTO home_list (id, name, time, lj) VALUES ("https://img.huxiucdn.com.jpg"," https://www.huxiu.com90.html"," 12"," ")
            try:
                result = self.cursor.execute(sqlInsert)
                insert_id = self.conn.insert_id()  # 插入成功后返回的id
                self.conn.commit()
                # 判断是否执行成功
                if result:
                    print("插入成功", insert_id)
                    return insert_id + 1
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据插入数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 查询最后一条数据的id值
    def getLastId(self):
        sql = "SELECT max(id) FROM " + self.table
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例