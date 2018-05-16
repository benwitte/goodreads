# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodreadsItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    avgrating = scrapy.Field()
    five_stars = scrapy.Field()
    four_stars = scrapy.Field()
    three_stars = scrapy.Field()
    two_stars = scrapy.Field()
    one_stars = scrapy.Field()
    totalratings = scrapy.Field()
    totalreviews = scrapy.Field()
    genre = scrapy.Field()
    numpages = scrapy.Field()
    publisher = scrapy.Field()
    pubdate = scrapy.Field()
    origpubdate = scrapy.Field()
    awards = scrapy.Field()