# -*- coding: utf-8 -*-
import scrapy
from xici_ip.items import XiciIpItem

class Crawler10Spider(scrapy.Spider):
    name = 'crawler1.0'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn/newsDetail_forward_4531034']

    def parse(self, response):
        item = XiciIpItem()
        title = response.css('h1.news_title::text').extract_first()
        print(title)
