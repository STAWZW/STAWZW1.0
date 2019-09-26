# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Identity

def title_convert(value):
    title = ''.join(re.findall('[\u4e00-\u9fa5]',value))
    return title

class Testcrawler10ItemLoader(ItemLoader):					#对全局字段做过滤处理,自定义类继承ItemLoader,重写内部类
    default_input_processor = MapCompose(title_convert)
    default_output_processor = TakeFirst()

class Testcrawler10Item(scrapy.Item):
    title = scrapy.Field(
        # input_processor = MapCompose(title_convert),		#在Item中可重写input和output,会覆盖掉自定义类中的default_input和default_output
        # output_processor = Identity()
        )
    link = scrapy.Field()
    posttime = scrapy.Field()

class Testcrawler10ImageItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
