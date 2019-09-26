# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiciIpPipeline(object):
    def process_item(self, item, spider):
        with open('ip_proxy.txt', 'a+') as file: #打开源文件并创建一个新文件
            file.write(item['ip'] + '\n')  #将修改后的内容写入新文件
        return item
