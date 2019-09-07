# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:29:29 2019

@author: Administrator
"""
import threading
from threading import Timer
import windFarmCrawler
import historyTyphoonCrawler
import previewTyphoonCrawler
import sckjCloudCrawler
import sckjRadarCrawler


def print_time1():
    windFarmCrawler.windFarmCrawler()

def print_time2():
    historyTyphoonCrawler.historyTyphoonCrawler()

def print_time3():
    sckjCloudCrawler.sckjCloudCrawler()
    sckjRadarCrawler.sckjRadarCrawler()

def print_time4():
    previewTyphoonCrawler_copy.previewTyphoonCrawler()

def crawleStart():
    b1 = threading.Thread(target=print_time1)
    b1.start()
    b2 = threading.Thread(target=print_time2)
    b2.start()
    b3 = threading.Thread(target=print_time3)
    b3.start()
    b4 = threading.Thread(target=print_time4)
    b4.start()

    threads = []
    threads.append(b1)
    threads.append(b2)
    threads.append(b3)
    threads.append(b4)

    for t in threads:
        t.join()
    print ('end')
    
    timrFor = Timer(2*60,crawleStart)
    timrFor.start()

#crawleStart()



