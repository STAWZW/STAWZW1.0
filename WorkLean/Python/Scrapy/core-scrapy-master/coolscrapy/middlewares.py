#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 中间件集合
Desc : 
"""
import random
from scrapy import signals
from scrapy.http import Request
from coolscrapy.settings import IPPOOL_LIST
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent

# IP代理池
class IPPOOLS(HttpProxyMiddleware):
    def __init__(self, ip=""):
        self.ip = ip

    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL_LIST)
        # print("当前使用的IP为： " + thisip["ipaddr"])
        request.meta["REMOTE_ADDR"] = "http://" + thisip["ipaddr"]

# 用户代理池
class USERAGENTS(UserAgentMiddleware):
    def __init__(self, user_agent=""):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        thisua = UserAgent().random
        # print("当前使用的User-Agent是： " + thisua)
        request.headers.setdefault("User-Agent", thisua)


