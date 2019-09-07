# -*- coding: utf-8 -*-

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
            print('connect mysql error.')

    def insertData(self, my_list):
        result = {}
        for item in my_list:
            itemList = list(item)
            result['id'] = itemList[0]
            result['date_file'] = itemList[1]
            result['time_file'] = itemList[2]
            result['date_now'] = itemList[3]
            result['time_now'] = itemList[4]
            result['organization'] = itemList[5]
            result['name_f'] = itemList[6]
            result['name_e'] = itemList[7]
            result['name_c'] = itemList[8]
            result['number'] = itemList[9]
            result['type'] = itemList[10]
            result['lon_now'] = itemList[11]
            result['lat_now'] = itemList[12]
            result['accuracy'] = itemList[13]
            result['move_d'] = itemList[14]
            result['move_a'] = itemList[15]
            result['move_s'] = itemList[16]
            result['pressure'] = itemList[17]
            result['wind_max'] = itemList[18]
            result['wind_gust'] = itemList[19]
            result['radius_34_ne'] = itemList[20]
            result['radius_34_se'] = itemList[21]
            result['radius_34_sw'] = itemList[22]
            result['radius_34_nw'] = itemList[23]
            result['radius_50_ne'] = itemList[24]
            result['radius_50_se'] = itemList[25]
            result['radius_50_sw'] = itemList[26]
            result['radius_50_nw'] = itemList[27]
            result['radius_64_ne'] = itemList[28]
            result['radius_64_se'] = itemList[29]
            result['radius_64_sw'] = itemList[30]
            result['radius_64_nw'] = itemList[31]
            try:
                sqlExit = "SELECT * FROM typhoon WHERE id = '%s'" % (result['id'])
                self.cursor.execute(sqlExit)
            except:
                self.conn.rollback()
                print('windFarmInsertData select mysql error.')
            sqldata = self.cursor.fetchone()
            valueList = []
            keyList = []
            if sqldata == None:
                values = list(result.values())
                keyss = list(result.keys())
                for itemkeys,itemvalue in zip(keyss,values):
                    if itemvalue != None:
                        keyList.append(itemkeys)
                        valueList.append(str(itemvalue))
                cols = ','.join(keyList)
                values = "','".join(valueList)
                sqlInsert = "INSERT INTO typhoon (%s) VALUES (%s)" % (cols, "'" + values + "'")
                try:
                    self.cursor.execute(sqlInsert)
                    self.conn.commit()
                    print('数据插入成功！')
                except psycopg2.Error as e:
                    self.conn.rollback()
                    print('insert error.')
                    print(e)
            else:
                print("windFarmInsertData数据存在不需要更新")
                continue

    def closePostgre(self):
        self.cursor.close()
        self.conn.close()