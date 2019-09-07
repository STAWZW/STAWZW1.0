import os
import time
import psutil
import threading

PidPath = r'D:\GitRepository\STAWZW1.0\Typhoon2.0\pidTxt.txt'

def start():
    with open(PidPath,'r') as f:
        logPid = int(f.read())
    pids = psutil.pids()
    print(type(logPid))
    if logPid not in pids:
        print('脚本停止')
        os.popen('cd D:/GitRepository/STAWZW1.0/Typhoon2.0 && python test.py')
        print('启动成功')
    timer = threading.Timer(10, start)
    timer.start()

start()







