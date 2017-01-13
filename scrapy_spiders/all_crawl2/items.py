# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllCrawl2Item(scrapy.Item):
	inurl = scrapy.Field()
	site = scrapy.Field()
	ext = scrapy.Field()

	filetype = scrapy.Field()

	intitle = scrapy.Field()
	intext = scrapy.Field()
