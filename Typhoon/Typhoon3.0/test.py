import time
import os
import logging

PidPath = r'D:\GitRepository\STAWZW1.0\Typhoon2.0\pidTxt.txt'
with open(PidPath,'w') as f:
    f.write(str(os.getpid()))

# logging.basicConfig(filename='loglogger.log', level=logging.INFO)
# logging.info('运行中')
# time.sleep(60)