# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:29:29 2019

@author: Administrator
"""
import threading
import allHistoryTyphoonCrawler_json
import allHistoryTyphoonCrawler_str
import allPreviewTyphoonCrawler
import allTyphoonCrawler

def print_time1():
    allHistoryTyphoonCrawler_json.allHistoryTyphoonCrawler_json()
    allHistoryTyphoonCrawler_str.allHistoryTyphoonCrawler_str()

def print_time2():
    allPreviewTyphoonCrawler.allPreviewTyphoonCrawler()

def print_time3():
    allTyphoonCrawler.allTyphoonCrawler()

def crawleStart():
    b1 = threading.Thread(target=print_time1)
    b1.start()
    b2 = threading.Thread(target=print_time2)
    b2.start()
    b3 = threading.Thread(target=print_time3)
    b3.start()

    threads = []
    threads.append(b1)
    threads.append(b2)
    threads.append(b3)

    for t in threads:
        t.join()
    print('end')

crawleStart()


