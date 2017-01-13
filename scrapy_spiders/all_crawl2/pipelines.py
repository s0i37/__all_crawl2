# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
import base64, re

class ElasticsearchPipeline(object):
	def open_spider(self, spider):
		if spider.elastic_uri:
			self.es = Elasticsearch( [spider.elastic_uri] )

	def process_item(self, item, spider):
		if spider.elastic_uri:
			self.es.index( index=spider.elastic_index, doc_type='page', id=re.sub( r'[\n/]', '', base64.encodestring( item["inurl"] ) ), body=dict(item) )
		return item

class AllCrawl2Pipeline(object):
	def process_item(self, item, spider):
		return item
