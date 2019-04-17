# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    '''
    This is the information you want from website
    '''
    # define the fields for your item here like:
    dish_type = scrapy.Field()
    restaurant_name = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    star = scrapy.Field()
    img_url = scrapy.Field()
    comment_num = scrapy.Field()

    def to_json(self):
        return {
            'dish_type': self.dish_type,
            'restaurant_name': self.restaurant_name,
            'location': self.location,
            'price': self.price,
            'star': self.star,
            'img_url': self.img_url,
            'comment_num': self.comment_num
        }
