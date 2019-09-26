# -*- coding: utf-8 -*-
from testCrawler1_0.items import Testcrawler10Item, Testcrawler10ItemLoader, Testcrawler10ImageItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

class Crawler10Spider(CrawlSpider):
    name = 'crawler1.0'
    # allowed_domains = ['huxiu.com']
    # start_urls = ['http://www.huxiu.com/index.php']
    allowed_domains = ['item.jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=9d869af94b494ed3aec46d22d04b4643']

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for url in self.start_urls:
            yield SplashRequest(url, args=splash_args)

    rules = (
        # Rule(LinkExtractor(allow=('/group?f=index_group', ), deny=('deny\.php', ))),
        # Rule(LinkExtractor(allow=('/article/\d+\.html',)), callback='parse_item1'),
        # Rule(LinkExtractor(allow=('/article/\d+\.html',)), callback='parse_item2'),
        Rule(LinkExtractor(allow=('item.jd.com/\d+\.html',)), callback='parse_item3'),
        # Rule(LinkExtractor(allow=('/channel/\d+\.html',)), callback='parse_item2'),
    )

    def splash_request(self, request):
        return SplashRequest(url=request.url, args={'wait': 0.5})

    def _requests_to_follow(self, response):
        # *************请注意我就是被注释注释掉的类型检查o(TωT)o 
        # if not isinstance(response, HtmlResponse):
        #     return
        # ************************************************
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def _build_request(self, rule, link):
        r = SplashRequest(url=link.url, callback=self._response_downloaded, meta={'rule': rule, 'link_text': link.text}, args={'wait': 0.5, 'url': link.url})
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def parse_item1(self, response):
        self.logger.info('+++++++++++++++++++++++++++++++++Hi, this is an item page! %s', response.url)
        testcrawler10ItemLoader = Testcrawler10ItemLoader(item=Testcrawler10Item(), response=response)
        testcrawler10ItemLoader.add_xpath('title', '//*[@id="top"]/section/div/div[1]/div[1]/h1/text()')
        testcrawler10Info = testcrawler10ItemLoader.load_item()
        print(f"testcrawler10Info = {testcrawler10Info}")
        yield testcrawler10Info

    def parse_item2(self, response):
        imageItem = Testcrawler10ImageItem()
        imageItem['title'] = response.xpath('//*[@id="top"]/section/div/div[1]/div[1]/h1/text()').extract()
        imageItem['image_urls'] = response.xpath('//*[@id="top"]/div/div/div/img/@src').extract()
        yield imageItem

    def parse_item3(self, response):
        # imageItem = Testcrawler10ImageItem()
        print('连接为： ',response.url)
        value = response.xpath('//span[@class="p-price"]//text()').extract()
        print(value)


