# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Crawler10Spider(CrawlSpider):
    name = 'crawler1.0'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn']

    rules = (
        # Rule(LinkExtractor(allow=('/group?f=index_group', ), deny=('deny\.php', ))),
        # Rule(LinkExtractor(allow=('/article/\d+\.html',)), callback='parse_item1'),
        # Rule(LinkExtractor(allow=('/article/\d+\.html',)), callback='parse_item2'),
        Rule(LinkExtractor(allow=['newsDetail_forward_\d+',],restrict_css=['#masonryContent']),
        	callback='parse_item1'),
        # Rule(LinkExtractor(allow=('/channel/\d+\.html',)), callback='parse_item2'),
    )

    def parse_item1(self, response):
        print('++++++++++++++++++++++++')
        title = response.css('h1.news_title::text').extract_first()
        souece = response.css('div.news_about p:nth-child(1)::text').extract_first()
        time = response.css('div.news_about p:nth-child(2)::text').extract_first()
        text = response.css('div.news_txt ::text').extract()
        img_url = response.css('div.news_txt img::attr(src)').extract()
        print(response.url)
        print(img_url)