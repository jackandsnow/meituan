# -*- coding: utf-8 -*-
import socket
from datetime import datetime
from urllib.parse import urljoin

import scrapy
from cssselect import Selector
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

from meituan.items import MeituanItem

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Cache-Control": "max-age=0",
    "Host": "gz.meituan.com",
    "RA-Sid": "7C4125DE-20150519-013547-91bdb7-b00401",
    "RA-Ver": "3.0.7",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
}


class FoodSpider(scrapy.Spider):
    name = 'food'
    allowed_domains = ['gz.meituan.com']
    # start_urls = ['https://gz.meituan.com/meishi/']
    start_urls = ['https://gz.meituan.com/meishi/c11/']

    def parse(self, response):
        base_path = '//*[@id="app"]'
        # 所有菜系名称
        # dish_name_list = response.xpath(base_path + '//*[@data-reactid="20"]/li/a/text()').extract()
        # 所有菜系URL
        # dish_url_list = response.xpath(base_path + '//*[@data-reactid="20"]/li/a/@href').extract()

        # print(dish_name_list)
        # print(dish_url_list)

        # uls = response.xpath('//*[@id="app"]/section/div/div[2]/div[2]/div[1]/ul/li[2]/div[2]/a/h4/text()')
        uls = response.xpath('//*[@class="list"]/ul/li//a/h4').extract()
        print('uls is ', uls)

        # for i in range(0, 3):#len(dish_url_list)):
        #     yield Request(dish_url_list[i], callback=self.parse_food)

    def parse_food(self, response):
        print('food beginning ......')
        uls = response.xpath('//*[@id="app"]//*[@class="list-ul"]/li')
        print('uls is ', uls)
        for u in range(0, len(uls)):
            dish_type = response.xpath('//*[@id="app"]//*[@class="hasSelect"]/span[2]/text()').extract()
            restaurant_name = response.xpath('//*[@id="app"]//li[' + str(u) + ']/div[2]/a/h4/text()').extract()
            price = response.xpath('//*[@id="app"]//li[' + str(u) + ']/div[2]/a/p/span/text()').extract()
            print(dish_type, ',', restaurant_name, ',', price, '\n')
            # item装载器工具
            # loader = ItemLoader(item=MeituanItem(), response=response)
            # # str.strip 剔除首尾多余的空白符
            # loader.add_xpath('dish_type', '//*[@id="app"]//*[@class="hasSelect"]/span[2]/text()',
            #                  MapCompose(str.strip))
            # loader.add_xpath('restaurant_name', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/h4/text()',
            #                  MapCompose(str.strip))
            # loader.add_xpath('location', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/p/text()',
            #                  MapCompose(str.strip))
            # # '//*[@id="app"]//li[i]//*[@class="desc"]/span/text()'
            # loader.add_xpath('price', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/p/span/text()',
            #                  MapCompose(int), re='[0-9]+')
            # loader.add_xpath('star', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/div/p/text()',
            #                  MapCompose(float), re='[.0-9]+')
            # loader.add_xpath('img_url', '//*[@id="app"]//li[' + str(u) + ']/div[1]//*[@class="imgbox"]/img/@src',
            #                  MapCompose(str.strip))
            # loader.add_xpath('comment_num', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/div/p/span/text()',
            #                  MapCompose(int), re='[0-9]+')
            #
            # item = loader.load_item()
            # print('\nitem is : ', item)
            # yield item
