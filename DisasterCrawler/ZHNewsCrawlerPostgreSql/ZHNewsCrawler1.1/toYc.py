# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:49:11 2019

@author: Administrator
"""

import re
import jieba
import jieba.posseg as pseg
import hashlib
import random
import requests
import langid

def tihuan_tongyici(string1):
    combine_dict = {}
    for line in open("tongyici_tihuan.txt", "r", encoding='UTF-8'):
        seperate_word = line.strip().split("\t")
        num = len(seperate_word)
        for i in range(1, num):
            combine_dict[seperate_word[i]] = seperate_word[0]
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
        textList = re.split('。|，|,',textLine)
        wordList = []
        flagList = []
        count = []
        indexCount = 1
        for item in textList:
            if '死亡' in item:
                jieba.suggest_freq("死亡", tune = True)                           #提升某些词的词频
                words = pseg.cut(item)
                for word, flag in words:
                    wordset = "{0}".format(word)
                    flagset = "{0}".format(flag)
                    wordList.append(wordset)
                    flagList.append(flagset)
                position = wordList.index('死亡')
                while indexCount < position:                                    #循环遍历获取死亡人数
                    if flagList[position - indexCount] == 'm' or flagList[position - indexCount] == 'x':
                        count.append(wordList[position - indexCount])
                        break
                    elif (position + indexCount) < len(flagList):
                        if flagList[position + indexCount] == 'm' or flagList[position - indexCount] == 'x':
                            count.append(wordList[position + indexCount])
                            break
                    indexCount = indexCount + 1
                wordList.clear()                                                #清空list数组
                flagList.clear()
        if count == []:
            return 0
        else:
            for i, v in enumerate(count):                                       #转换list数组内容为int类型
                try:
                    count [i] = int(v)
                except:
                    count [i] = 0
            return max(count)
    except:
        return 0

def Injured(text):
    try:
        textLine = tihuan_tongyici(text)
        textList = re.split('。|，|,',textLine)
        wordList = []
        flagList = []
        count = []
        indexCount = 1
        for item in textList:
            if '受伤' in item:
                jieba.suggest_freq("受伤", tune = True)                         #提升某些词的词频
                words = pseg.cut(item)
                for word, flag in words:
                    wordset = "{0}".format(word)
                    flagset = "{0}".format(flag)
                    wordList.append(wordset)
                    flagList.append(flagset)
                position = wordList.index("受伤")
                while indexCount < position:                                    #循环遍历获取受伤人数
                    if flagList[position - indexCount] == 'm' or flagList[position - indexCount] == 'x':
                        count.append(wordList[position - indexCount])
                        break
                    elif (position + indexCount) < len(flagList):
                        if flagList[position + indexCount] == 'm' or flagList[position - indexCount] == 'x':
                            count.append(wordList[position + indexCount])
                            break
                    indexCount = indexCount + 1
                wordList.clear()                                                #清空list数组
                flagList.clear()
        if count == []:
            return 0
        else:
            for i, v in enumerate(count):                                       #转换list数组内容为int类型
                try:
                    count [i] = int(v)
                except:
                    count [i] = 0
            return max(count)
    except:
        return 0

def loss(text):
    try:
        textList = re.split('。|，|,',text)
        wordList = []
        flagList = []
        count = []
        countText = []
        indexCount = 1
        for item in textList:
            if '元' in item:
                words = pseg.cut(item)
                for word, flag in words:
                    wordset = "{0}".format(word)
                    flagset = "{0}".format(flag)
                    wordList.append(wordset)
                    flagList.append(flagset)
                for item in wordList:
                    if '元' in item:
                        position = wordList.index(item)
                        if flagList[position] == 'm':
                            while indexCount < position:                        #循环遍历获取经济损失数值
                                if flagList[position - indexCount] == 'm':
                                    count.append(wordList[position - indexCount])
                                    countText.append(item)
                                    break
                                indexCount = indexCount + 1
                                if indexCount == 4:
                                    break
                wordList.clear()                                                #清空list数组
                flagList.clear()
        if count == []:
            return '0'
        else:
            for i, v in enumerate(count):                                       #转换list数组内容为int类型
                try:
                    count [i] = float(v)
                except:
                    count [i] = 0
            lossNumber = str(max(count)) + countText[count.index(max(count))]
            losses = unitConversion(lossNumber)
            return losses
    except:
        return '0'

def unitConversion(lossNumber):
    try:
        loss = float(re.findall(r"\d+\.?\d*",lossNumber)[0])
        if '万' in lossNumber:
            if '美元' in lossNumber:
                return str(loss)
            else:
                lossDollar = round(loss/6.8707,2)
                return str(lossDollar)
        elif '亿' in lossNumber:
            if '美元' in lossNumber:
                lossDollar = loss*10000
                return str(lossDollar)
            else:
                lossDollar = round(loss*10000/6.8707,2)
                return str(lossDollar)
        else:
            lossDollar = round(loss/6.8707/10000,2)
            return str(lossDollar)
    except:
        return '0'

def translate(content):
    language = langid.classify(content)[0]
    if language == 'en':
        content = content.lower()
    apiurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    appid = '20190730000322586'
    secretKey = 'df2vBgyHUCkAUDP6BDwM'
    salt = str(random.randint(32768, 65536))
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    try:
        paramas = {
            'appid': appid,
            'q': content,
            'from': language,
            'to': 'zh',
            'salt': salt,
            'sign': sign
        }
        response = requests.get(apiurl, paramas)
        jsonResponse = response.json()
        if "trans_result" in jsonResponse.keys():
            dst = str(jsonResponse["trans_result"][0]["dst"])
        else:
            dst = content
        return dst
    except Exception as e:
        print(e)
        return content
