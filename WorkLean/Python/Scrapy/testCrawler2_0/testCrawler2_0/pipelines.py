# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Testcrawler20Pipeline1(object):
    def process_item(self, item, spider):
        print('++++++++++++++++++++==')
        print(item)
        return item

class Testcrawler20Pipeline2(object):
    def process_item(self, item, spider):
        print('++++++++++++++++++++==')
        print(item)
        return item


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if 'image_urls' not in item.keys(): # 判断是否获取到图片链接
            item['image_urls'] = []
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        images = [x['checksum'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        item['images'] = images
        return item
