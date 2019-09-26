# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Identity, Join, Compose
from scrapy.loader import ItemLoader

class Identity_overload(Identity):
    def __call__(self, values):
        if not values:
            values.append('')
        return values

class Identity_overload1(Identity):
    def __call__(self, values):
        return values

class TakeFirst_overload(TakeFirst):
    def __call__(self, values):
        for value in values:
            if value is not None:
                return value

def de_weighting_list(target_list):
    if not target_list:
        # target_list.append('')
        return []
    return list(set(target_list))

class ArticleItemLoader(ItemLoader):
    default_input_processor = Identity_overload()
    default_output_processor = TakeFirst_overload()

class Testcrawler20Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(
    	# input_processor = Identity_overload()
    	)
    image_urls = scrapy.Field(
    	input_processor = Compose(de_weighting_list),
    	output_processor = Identity_overload1()
    	)
    images = scrapy.Field(
    	# input_processor = MapCompose(de_weighting_list)
    	)
    image_paths = scrapy.Field()

class Testcrawler20Item1(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()