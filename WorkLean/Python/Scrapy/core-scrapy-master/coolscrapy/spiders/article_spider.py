#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from coolscrapy.items import Article, ArticleItemLoader

class ArticleSpider(CrawlSpider):
    name = "article"

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        if rule.selectors == 'xpath':
            if rule.next_page:
                rule_list.append(Rule(LinkExtractor(restrict_xpaths=[rule.next_page])))
            rule_list.append(Rule(LinkExtractor(
                allow=[rule.allow_url],
                restrict_xpaths=[rule.extract_from]),
                callback='parse_item_xpath'))
        else:
            if rule.next_page:
                rule_list.append(Rule(LinkExtractor(restrict_css=[rule.next_page])))
            rule_list.append(Rule(LinkExtractor(
                allow=[rule.allow_url],
                restrict_css=[rule.extract_from]),
                callback='parse_item_css'))
        self.rules = tuple(rule_list)
        super(ArticleSpider, self).__init__()

    def parse_item_xpath(self, response):
        articleItem = ArticleItemLoader(item=Article(), response=response)
        articleItem.add_value('url', response.url)
        articleItem.add_xpath('title', self.rule.title_path)
        articleItem.add_xpath('releaseTime', self.rule.releaseTime_path)
        articleItem.add_xpath('image_urls', self.rule.image_path)
        articleItem.add_xpath('body', self.rule.body_path)
        articleItem.add_xpath('source_site', self.rule.source_site_path)
        articleItemLoader = articleItem.load_item()
        # print(f"articleItemLoader = {articleItemLoader}")
        return articleItemLoader

    def parse_item_css(self, response):
        articleItem = ArticleItemLoader(item=Article(), response=response)
        articleItem.add_value('url', response.url)
        articleItem.add_css('title', self.rule.title_path)
        articleItem.add_css('releaseTime', self.rule.releaseTime_path)
        articleItem.add_css('image_urls', self.rule.image_path)
        articleItem.add_css('body', self.rule.body_path)
        articleItem.add_css('source_site', self.rule.source_site_path)
        articleItemLoader = articleItem.load_item()
        # print(f"articleItemLoader = {articleItemLoader}")
        return articleItemLoader
    