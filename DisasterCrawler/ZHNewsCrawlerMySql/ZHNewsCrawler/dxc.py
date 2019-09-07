# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:29:29 2019

@author: Administrator
"""

import threading
from typhoon import typhoon
from earthquake import earthquake
from earthquake_ES001 import earthquake_ES001
from earthquake_ES002 import earthquake_ES002
from stormSurge import stormSurge
from tsunami import tsunami
from forestFire import forestFire
from rainstorm_ZH001 import rainstorm_ZH001
from rainstorm_ZH002 import rainstorm_ZH002
from rainstorm_ES001 import rainstorm_ES001
from landslide import landslide
from debrisFlow import debrisFlow
from drought_ZH001 import drought_ZH001
from drought_ZH002 import drought_ZH002
from collapse import collapse

def print_time1():
    
    a1_1 = earthquake()
    a1_1.rund()

    a2_1 = earthquake_ES001()
    a2_1.rund()
    a2_2 = earthquake_ES002()
    a2_2.rund()

def print_time2():

    a1_1 = typhoon()
    a1_1.rund()

def print_time3():
    
    a1_1 = stormSurge()
    a1_1.rund()

def print_time4():
    
    a3 = debrisFlow()
    a3.rund()

def print_time5():
    
    a1_1 = drought_ZH001()
    a1_1.rund()
    a1_2 = drought_ZH002()
    a1_2.rund()

def print_time6():
    
    a1_1 = tsunami()
    a1_1.rund()

def print_time7():
    
    a1_1 = forestFire()
    a1_1.rund()

def print_time8():
    
    a1_1 = rainstorm_ZH001()
    a1_1.rund()
    a1_2 = rainstorm_ZH002()
    a1_2.rund()

    a2_1 = rainstorm_ES001()
    a2_1.rund()
    
def print_time9():
    
    a1_1 = landslide()
    a1_1.rund()

def print_time10():

    a1_1 = collapse()
    a1_1.rund()

# 创建新线程
if __name__ == "__main__":
    b1 = threading.Thread(target=print_time1)
    b1.start()
    b2 = threading.Thread(target=print_time2)
    b2.start()
    b3 = threading.Thread(target=print_time3)
    b3.start()
    b4 = threading.Thread(target=print_time4)
    b4.start()
    b5 = threading.Thread(target=print_time5)
    b5.start()
    b6 = threading.Thread(target=print_time6)
    b6.start()
    b7 = threading.Thread(target=print_time7)
    b7.start()
    b8 = threading.Thread(target=print_time8)
    b8.start()
    b9 = threading.Thread(target=print_time9)
    b9.start()
    b10 = threading.Thread(target=print_time10)
    b10.start()

threads = []
threads.append(b1)
threads.append(b2)
threads.append(b3)
threads.append(b4)
threads.append(b5)
threads.append(b6)
threads.append(b7)
threads.append(b8)
threads.append(b9)
threads.append(b10)

for t in threads:
    t.join()
print ('end')