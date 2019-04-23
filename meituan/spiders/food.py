# -*- coding: utf-8 -*-
import json

import pymysql
import scrapy
from scrapy import Request

from meituan.util import call_interface, get_food_list


def write_json(data, no):
    with open('data' + str(no) + '.json', 'w') as f:
        dic = {'data': data}
        json.dump(dic, f, ensure_ascii=False)
        print('Save data into json file successfully!')
        f.close()


def write_to_db(item_list):
    conn = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        database='meituan',
        charset='utf8')

    cursor = conn.cursor()
    for i in range(0, len(item_list)):
        sql = 'INSERT INTO '
        pass
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    print("Database version : %s " % data)

    conn.close()



class FoodSpider(scrapy.Spider):
    name = 'food'
    allowed_domains = ['gz.meituan.com']
    start_urls = ['https://gz.meituan.com/meishi/']

    def parse(self, response):
        # 所有菜系URL
        dish_url_list = response.xpath('//*[@id="app"]//*[@data-reactid="20"]/li/a/@href').extract()
        # print(dish_url_list)

        for i in range(0, 1):  # len(dish_url_list)):
            yield Request(dish_url_list[i], callback=self.parse_food)

    def parse_food(self, response):
        data_list = []
        originUrl = response.url
        print('crawl food from ' + originUrl)
        dish_type = response.xpath('//*[@id="app"]//*[@class="hasSelect"]/span[2]/text()').extract()[0]
        tdata = call_interface(1, originUrl)
        # data_list.append(tdata)
        # for i in range(0, len(data_list)):
        data_list = get_food_list(dish_type, tdata['poiInfos'])
        # calculate how many pages
        # if tdata['totalCounts'] % 15 == 0:
        #     page_num = tdata['totalCounts'] // 15
        # else:
        #     page_num = tdata['totalCounts'] // 15 + 1
        # print(page_num)
        #
        # for page in range(2, 5):#page_num + 1):
        #     data_list.append(call_interface(page, originUrl))
        write_json(data_list, 1)

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
