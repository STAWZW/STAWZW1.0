# -*- coding: utf-8 -*-
# Define here the models for your scraped items

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, Compose
from coolscrapy.utils import time_format, de_weighting_list, Identity_overload, TakeFirst_overload

class ArticleItemLoader(ItemLoader):
    default_input_processor = Identity_overload()
    default_output_processor = TakeFirst_overload()

class Article(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    releaseTime = scrapy.Field(
        # input_processor = MapCompose(time_format),
    )
    image_urls = scrapy.Field(
    	input_processor = Compose(de_weighting_list),
        output_processor = Identity()
    )
    images = scrapy.Field()
    image_paths = scrapy.Field()
    body = scrapy.Field(
        output_processor = Join()
    )
    source_site = scrapy.Field()
