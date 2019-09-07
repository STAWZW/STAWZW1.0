# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:49:11 2019

@author: Administrator
"""

import jieba
import jieba.posseg as pseg #词性标注
def tihuan_tongyici(string1):
    combine_dict = {}
    for line in open("tongyici_tihuan.txt", "r", encoding='UTF-8'):
        seperate_word = line.strip().split("\t")
        num = len(seperate_word)
        for i in range(1, num):
            combine_dict[seperate_word[i]] = seperate_word[0]
    #jieba.suggest_freq("年假", tune = True)       #提升某些词的词频
    seg_list = jieba.cut(string1, cut_all = False)
    f = "/".join(seg_list)
    final_sentence = ""
    for word in f.split("/"):
        if word in combine_dict:
            word = combine_dict[word]
            final_sentence += word
        else:
            final_sentence += word
    return final_sentence


def death(text):
    try:
        textLine = tihuan_tongyici(text)
        textList = textLine.split('，')
        wordList = []
        flagList = []
        count = []
        indexCount = 1
        for item in textList:
            if '死亡' in item:
                jieba.suggest_freq("死亡", tune = True)       #提升某些词的词频
                words = pseg.cut(item)
                for word, flag in words:
                    wordset = "{0}".format(word)
                    flagset = "{0}".format(flag)
                    wordList.append(wordset)
                    flagList.append(flagset)
                position = wordList.index('死亡')
                while indexCount < position:            #循环遍历获取死亡人数
                    if flagList[position - indexCount] == 'm' or flagList[position - indexCount] == 'x':
                        count.append(wordList[position - indexCount])
                        break
                    elif (position + indexCount) < len(flagList):
                        if flagList[position + indexCount] == 'm' or flagList[position - indexCount] == 'x':
                            count.append(wordList[position + indexCount])
                            break
                    indexCount = indexCount + 1
                wordList.clear()            #清空list数组
                flagList.clear()
        for i, v in enumerate(count):          #转换list数组内容为int类型
            try:
                count [i] = int(v)
            except:
                count [i] = 0
                continue
        if count == []:
            return 0
        else:
            return max(count)
    except:
        return 0


def Injured(text):
    try:
        textLine = tihuan_tongyici(text)
        textList = textLine.split('，')
        wordList = []
        flagList = []
        count = []
        indexCount = 1
        for item in textList:
            if '受伤' in item:
                jieba.suggest_freq("受伤", tune = True)       #提升某些词的词频
                words = pseg.cut(item)
                for word, flag in words:
                    wordset = "{0}".format(word)
                    flagset = "{0}".format(flag)
                    wordList.append(wordset)
                    flagList.append(flagset)
                position = wordList.index("受伤")
                while indexCount < position:            #循环遍历获取死亡人数
                    if flagList[position - indexCount] == 'm' or flagList[position - indexCount] == 'x':
                        count.append(wordList[position - indexCount])
                        break
                    elif (position + indexCount) < len(flagList):
                        if flagList[position + indexCount] == 'm' or flagList[position - indexCount] == 'x':
                            count.append(wordList[position + indexCount])
                            break
                    indexCount = indexCount + 1
                wordList.clear()            #清空list数组
                flagList.clear()
        for i, v in enumerate(count):          #转换list数组内容为int类型
            try:
                count [i] = int(v)
            except:
                count [i] = 0
                continue
        if count == []:
            return 0
        else:
            return max(count)
    except:
        return 0


#test = '原标题：印尼暴雨引发洪水及泥石流 已致17人死亡上万人撤离中新网4月29日电 据“中央社”报道，印度尼西亚当局28日表示，连日来暴雨在苏门答腊岛引发洪水及泥石流，至少造成17人丧命，9人失踪。有关官员表示，严峻的气候影响明古鲁省(Bengkulu)9个乡镇市区，撤离约1.2万人，并有数以百计建物、桥梁及道路遭破坏。官员警告，部分区域积水虽退，但整体受灾情况仍是未知数，且部分地带通讯中断。据报道，印尼国家灾害应变总署发言人苏托波表示：“这场灾害的影响可能增加。”他说，水灾造成多人受伤，若降雨量升高，泥石流及洪水可能再度发生。苏托波表示，卫生条件差外加缺乏干净用水，恐引发皮肤病或严重呼吸道感染等“次级灾害”。当局为约1.3万受灾户设立公共厨房和疏散避难所，搜救团队也试图用橡皮艇进入重灾区。苏托波说：“道路遭洪水及泥石流切断，导致救援物资配给工作受阻。”他透露，正在使用挖土机清除道路。报道称，泥石流及洪水在印度尼西亚很常见，尤其在10月至4月的雨季。首都雅加达上一周有部分区域淹水，造成至少2人死亡，超过2000人撤离家园。'
#test1 = '原标题：印尼苏拉威西岛发生泥石流 至少59人遇难数千人撤离中新网1月25日电 综合报道，印度尼西亚苏拉威西岛(Sulawesi)近日发生山洪及土石流，印尼政府25日表示，事故造成至少59人丧生，数千人撤离家园。印尼抗灾署发言人苏托波表示，暴雨从22日开始袭击苏拉威西岛南部，造成河流水位暴涨，丘陵地区出现泥石流，联合搜救团队已前往受灾地区救援。据报道，约有3400人从家中撤离，并在学校、清真寺和帐篷中避难。苏拉威西岛南部11个地区中数十个小区被水淹没，首府望加锡也受到影响。其中，Gowa地区受灾最严重，有44人被发现死亡。每年11月至来年3月为印度尼西亚雨季，各地经常发生暴雨洪水与泥石流，造成多人伤亡。2018年，在苏门答腊岛的几个地区，山洪暴发和山体滑坡造成至少22人死亡，而在印度尼西亚爪哇岛一处山坡发生泥石流，造成十几人死亡。'
#test2 = '原标题：印尼洪水肆虐造成近40人死亡 至少13人失踪中新网4月29日电 据“中央社”报道，当地时间29日，印度尼西亚官员表示，连日暴雨在各地引发洪水及泥石流，已造成近40人丧命，另有至少13人失踪。报道称，每逢10月至来年4月雨季期间，这个东南亚地区最大的群岛国就经常遭暴雨侵袭，引发洪水及泥石流。印度尼西亚救灾部门29日证实称，苏门答腊岛的明古鲁省(Bengkulu)已有29人死亡，另有至少13人失踪。毗邻的楠榜省(Lampung)27日因大雨引发泥石流，也造成一家6口不幸丧命。据报道，印尼首都雅加达与周围地区也有至少2人因洪水死亡。与此同时，洪水还导致2000多人被迫撤离家园，并使14条宠物蟒蛇逃走。据报道，雅加达卫星城市茂物(Bogor)水位高涨，蟒蛇是从私人宅邸逃出，居民可能还得与蟒蛇周旋。印尼官员表示，这些蟒蛇有的长达4米，其中6条已找回，另有8条仍下落不明。'
#test3 = '狂风暴雨袭徐州致92万余人受灾7死1伤'
#print(death(test1))
#print(Injured(test1))


