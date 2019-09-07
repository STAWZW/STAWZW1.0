# -*- coding:utf-8 -*-

import time
time1=time.time()
from pgword import PostgreCommand

class node(object):
    def __init__(self):
        self.next = {}
        self.fail = None
        self.isWord = False
        self.word = ""

class ac_automation(object):

    def __init__(self):
        self.root = node()

    def addword(self, word):
        temp_root = self.root
        for char in word:
            if char not in temp_root.next:
                temp_root.next[char] = node()
            temp_root = temp_root.next[char]
        temp_root.isWord = True
        temp_root.word = word

    def make_fail(self):
        temp_que = []
        temp_que.append(self.root)
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            p = None
            for key,value in temp.next.item():
                if temp == self.root:
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:
                        if key in p.next:
                            temp.next[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    def search(self, content):
        p = self.root
        result = []
        currentposition = 0

        while currentposition < len(content):
            word = content[currentposition]
            while word in p.next == False and p != self.root:
                p = p.fail

            if word in p.next:
                p = p.next[word]
            else:
                p = self.root

            if p.isWord:
                result.append(p.word)
                p = self.root
            currentposition += 1
        return result

    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.addword(str(keyword).strip())

    def words_replace(self, text):
        result = list(set(self.search(text)))
        if result != []:
            print(text)
            print('垃圾新闻')
            return True
        else:
            print('非垃圾新闻')
            return False




def ac():
    ah = ac_automation()
    path='D:/GitRepository/STAWZW1.0/ZHNewsCrawlerPostgreSql/ZHNewsCrawler1.1/filter_words.txt'
    ah.parse(path)
    global postgreCommand
    postgreCommand = PostgreCommand()
    postgreCommand.connectPostgre()
    textList = postgreCommand.insertData()
    postgreCommand.closePostgre()
    # print(len(textList))
    for item in textList:
        # print(item)
        ah.words_replace(item)
        # break

ac()
