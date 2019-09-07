from my import MySQLCommand
from pg import PostgreCommand
from threading import Timer

def star():
    mysqlCommand = MySQLCommand()
    mysqlCommand.connectMysql()
    sqldata = mysqlCommand.selectData()
    mysqlCommand.closeMysql()
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    postgreCommand.insertData(sqldata)
    postgreCommand.closePostgre()

    print("检测完毕！")
    timrFor = Timer(15*60,star)
    timrFor.start()

star()