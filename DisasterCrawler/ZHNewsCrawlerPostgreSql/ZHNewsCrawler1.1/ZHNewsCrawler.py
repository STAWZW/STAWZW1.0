# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:29:29 2019

@author: Administrator
"""
import os
import threading
from threading import Timer
import typhoon_ZH001
import typhoon_ZH002
import typhoon_ZH003
import typhoon_ZH004
import earthquake_ZH001
import earthquake_ES001
import earthquake_ES002
import stormSurge_ZH001
import stormSurge_ZH002
import stormSurge_ZH003
import stormSurge_ZH004
import stormSurge_ZH005
import tsunami_ZH001
import tsunami_ZH002
import tsunami_ZH003
import tsunami_ZH004
import tsunami_ZH005
import forestFire_ZH001
import forestFire_ZH002
import forestFire_ZH003
import forestFire_ZH004
import forestFire_ZH005
import forestFire_ZH006
import rainstorm_ZH001
import rainstorm_ZH002
import rainstorm_ZH003
import rainstorm_ZH004
import rainstorm_ZH005
import rainstorm_ZH006
import rainstorm_ES001
import landslide_ZH001
import landslide_ZH002
import landslide_ZH003
import landslide_ZH004
import landslide_ZH005
import landslide_ZH006
import debrisFlow_ZH001
import debrisFlow_ZH002
import debrisFlow_ZH003
import debrisFlow_ZH004
import drought_ZH001
import drought_ZH002
import drought_ZH003
import drought_ZH004
import drought_ZH005
import drought_ZH006
import collapse_ZH001
import collapse_ZH002
import collapse_ZH003
import collapse_ZH004
import collapse_ZH005
import comprehensive_ZH001
import hail_ZH001
import coldWave_ZH001
import heavyFog_ZH001
import tropicalWind_ZH001
import avalanche_ZH001
import volcanic_ZH001
import thunderstorm_ZH001
import mountainTorrent_ZH001
import frost_ZH001
import snowstorm_ZH001

def print_time1():
    stormSurge_ZH001.stormSurge_ZH001()
    stormSurge_ZH002.stormSurge_ZH002()
    stormSurge_ZH003.stormSurge_ZH003()
    stormSurge_ZH004.stormSurge_ZH004()
    stormSurge_ZH005.stormSurge_ZH005()
    tsunami_ZH001.tsunami_ZH001()
    tsunami_ZH002.tsunami_ZH002()
    tsunami_ZH003.tsunami_ZH003()
    tsunami_ZH004.tsunami_ZH004()
    tsunami_ZH005.tsunami_ZH005()

def print_time2():
    comprehensive_ZH001.comprehensive_ZH001()
    earthquake_ZH001.earthquake_ZH001()
    earthquake_ES001.earthquake_ES001()
    earthquake_ES002.earthquake_ES002()
    forestFire_ZH001.forestFire_ZH001()
    forestFire_ZH002.forestFire_ZH002()
    forestFire_ZH003.forestFire_ZH003()
    forestFire_ZH004.forestFire_ZH004()
    forestFire_ZH005.forestFire_ZH005()
    forestFire_ZH006.forestFire_ZH006()

def print_time3():
    typhoon_ZH001.typhoon_ZH001()
    typhoon_ZH002.typhoon_ZH002()
    typhoon_ZH003.typhoon_ZH003()
    typhoon_ZH004.typhoon_ZH004()
    rainstorm_ZH001.rainstorm_ZH001()
    rainstorm_ZH002.rainstorm_ZH002()
    rainstorm_ZH003.rainstorm_ZH003()
    rainstorm_ZH004.rainstorm_ZH004()
    rainstorm_ZH005.rainstorm_ZH005()
    rainstorm_ZH006.rainstorm_ZH006()

def print_time4():
    landslide_ZH001.landslide_ZH001()
    landslide_ZH002.landslide_ZH002()
    landslide_ZH003.landslide_ZH003()
    landslide_ZH004.landslide_ZH004()
    landslide_ZH005.landslide_ZH005()
    landslide_ZH006.landslide_ZH006()
    debrisFlow_ZH001.debrisFlow_ZH001()
    debrisFlow_ZH002.debrisFlow_ZH002()
    debrisFlow_ZH003.debrisFlow_ZH003()
    debrisFlow_ZH004.debrisFlow_ZH004()
    
def print_time5():
    drought_ZH001.drought_ZH001()
    drought_ZH002.drought_ZH002()
    drought_ZH003.drought_ZH003()
    drought_ZH004.drought_ZH004()
    drought_ZH005.drought_ZH005()
    drought_ZH006.drought_ZH006()
    collapse_ZH001.collapse_ZH001()
    collapse_ZH002.collapse_ZH002()
    collapse_ZH003.collapse_ZH003()
    collapse_ZH004.collapse_ZH004()
    collapse_ZH005.collapse_ZH005()

def print_time6():
    hail_ZH001.hail_ZH001()
    coldWave_ZH001.coldWave_ZH001()
    heavyFog_ZH001.heavyFog_ZH001()
    tropicalWind_ZH001.tropicalWind_ZH001()
    avalanche_ZH001.avalanche_ZH001()
    volcanic_ZH001.volcanic_ZH001()
    thunderstorm_ZH001.thunderstorm_ZH001()
    mountainTorrent_ZH001.mountainTorrent_ZH001()
    frost_ZH001.frost_ZH001()
    snowstorm_ZH001.snowstorm_ZH001()

def crawleStart():
    # PidPath = 'D:/GitRepository/STAWZW1.0/ZHNewsCrawlerPostgreSql/ZHNewsCrawler1.1/pidPath.txt'
    # with open(PidPath,'w') as f:
    #     f.write(str(os.getpid()))
    
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

    threads = []
    threads.append(b1)
    threads.append(b2)
    threads.append(b3)
    threads.append(b4)
    threads.append(b5)
    threads.append(b6)

    for t in threads:
        t.join()
    print ('end')

crawleStart()



