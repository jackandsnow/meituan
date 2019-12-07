# -*- coding: utf-8 -*-
import json

import pymysql
import scrapy
from scrapy import Request

from meituan.util import call_interface, get_food_list


# write data into mysql database
def write_to_db(item_list):
    conn = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='jack123456',
        database='meituan',
        charset='utf8')
    cursor = conn.cursor()

    for item in item_list:
        sql = 'INSERT INTO TB_RESTAURANTS(pk_id, dish_type, restaurant_name, location, price, star, img_url,' \
              ' comment_num) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        params = (item.pk_id, item.dish_type, item.restaurant_name, item.location, item.price, item.star, item.img_url,
                  item.comment_num)
        # 执行SQL
        cursor.execute(sql, params)
        # 提交数据
        conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    print('Write data into MySQL database successfully!')


class FoodSpider(scrapy.Spider):
    name = 'food'
    allowed_domains = ['gz.meituan.com']
    start_urls = ['https://gz.meituan.com/meishi/']

    def parse(self, response):
        # 所有菜系URL
        dish_url_list = response.xpath('//*[@id="app"]//*[@data-reactid="20"]/li/a/@href').extract()
        # print(dish_url_list)

        # traverse each dish_url to get food data
        for dish_url in dish_url_list:
            yield Request(dish_url.replace('http', 'https'), callback=self.parse_food)

    def parse_food(self, response):
        origin_url = response.url
        print('crawl food from ' + origin_url)
        dish_type = response.xpath('//*[@id="app"]//*[@class="hasSelect"]/span[2]/text()').extract()[0]
        re_data = call_interface(1, origin_url)
        data_list = get_food_list(dish_type, re_data['poiInfos'])
        # calculate how many pages
        if re_data['totalCounts'] % 15 == 0:
            page_num = re_data['totalCounts'] // 15
        else:
            page_num = re_data['totalCounts'] // 15 + 1

        for page in range(2, page_num + 1):
            re_data = call_interface(page, origin_url)
            data_list.extend(get_food_list(dish_type, re_data['poiInfos']))

        write_to_db(data_list)

        # item装载器工具
        # loader = ItemLoader(item=MeituanItem(), response=response)
        # # str.strip 剔除首尾多余的空白符
        # loader.add_xpath('dish_type', '//*[@id="app"]//*[@class="hasSelect"]/span[2]/text()',
        #                  MapCompose(str.strip))
        # loader.add_xpath('restaurant_name', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/h4/text()',
        #                  MapCompose(str.strip))
        # loader.add_xpath('location', '//*[@id="app"]//li[' + str(u) + ']/div[2]/a/p/text()',
        #                  MapCompose(str.strip))
        # # '//*[@id="app"]//li[page]//*[@class="desc"]/span/text()'
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
