# -*- coding: utf-8 -*-
import scrapy
from testCrawler2_0.items import Testcrawler20Item, Testcrawler20Item1, ArticleItemLoader
from scrapy.loader import ItemLoader

class Crawler10Spider(scrapy.Spider):
    name = 'crawler1.0'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn/newsDetail_forward_4530858']

    def parse(self, response):
        atricleItemLoader = ArticleItemLoader(item = Testcrawler20Item(), response=response)
        atricleItemLoader.add_xpath('title', '//h1[@class="article__title"]/text()')
        atricleItemLoader.add_xpath('image_urls', '//*[@id="article-content"]//img/@_src | //*[@id="article-content"]//img/@src')
        articleInfo = atricleItemLoader.load_item()

        # atricleItemLoader = ItemLoader(item = Testcrawler20Item1(), response=response)
        # atricleItemLoader.add_css('title', 'h1.article__title::text')
        # atricleItemLoader.add_css('image_urls', '#article-content img::attr(href)')
        # articleInfo = atricleItemLoader.load_item()
        # print(f"articleInfo = {articleInfo}")
        # newtxt = response.xpath('//div[@id="article-content"]//text()').extract()
        # print(newtxt)
        # source = response.xpath('//span[@class="author-info__username"]/text()').extract()
        # print(source)
        # releaseTime = response.xpath('//span[@class="article__time"]/text()').extract()
        # print(releaseTime)
        # title = response.xpath('//h1[@class="article__title"]/text()').extract()
        # print(title)
        # return articleInfo
