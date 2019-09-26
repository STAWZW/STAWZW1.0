# -*- coding: utf-8 -*-
# Define your item pipelines here
# pip install MySQL-python

from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from coolscrapy.models import db_connect, create_news_table, Article
from coolscrapy.utils import merge_list, session_scope

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import logging
 
logger = logging.getLogger(__name__)

class ArticleDataBasePipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        insert_data = Article(url=item["url"],
                    title=item["title"].encode("utf-8"),
                    releaseTime=item["releaseTime"].encode("utf-8"),
                    image_urls=item["image_urls"],
                    images=item["images"],
                    image_paths=item["image_paths"],
                    body=item["body"],
                    source_site=item["source_site"])
        with session_scope(self.Session) as session:
            session.add(insert_data)

    def close_spider(self, spider):
        pass

class ArticleDataImagePipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }

    def get_media_requests(self, item, info):
        if 'image_urls' not in item.keys(): # 判断是否获取到图片链接
            item['image_urls'] = []
        for image_url in item['image_urls']:
            self.default_headers['referer'] = image_url
            yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        images = [x['checksum'] for ok, x in results if ok]
        if not image_paths:
            item['image_urls'] = ''
            item['image_paths'] = ''
            item['images'] = ''
            logger.info('<***************该新闻没有图片***************>:' + item['url'])
        else:
            item['image_urls'] = merge_list(item['image_urls'],';')
            item['image_paths'] = merge_list(image_paths,';')
            item['images'] = merge_list(images,';')
        return item

class TestPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item
