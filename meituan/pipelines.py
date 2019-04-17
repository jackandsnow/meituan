# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MeituanPipeline(object):
    def process_item(self, item, spider):
        self.print_item(item)
        return item

    def print_item(self, item):
        print(item.to_json())
