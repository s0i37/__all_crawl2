# -*- coding: utf-8 -*-
import scrapy
from all_crawl2.items import AllCrawl2Item
from all_crawl2 import parsers

from urlparse import urlparse
from os.path import splitext, basename

import colorama

class LocalSpider(scrapy.Spider):
	name = "file"
	allowed_domains = []
	start_urls = []

	def __init__(self, uri='', zone='', allow_path='/', deny_path='', elastic_uri='', elastic_index='default', *args, **kwargs):
		super(LocalSpider, self).__init__(*args, **kwargs)
		if uri:
			self.start_urls.extend( uri.split(' ') )
		self.allowed_domains.extend( zone.split(' ') if zone else map(lambda uri: urlparse(uri).netloc.split(':')[0], uri.split(' ')) )
		self.name = '+'.join( zone.split(' ') if zone else map( lambda u:urlparse(u).netloc, uri.split(' ') ) )
		self.allow_path = allow_path.split(' ')
		self.deny_path = deny_path.split(' ') if deny_path else []
		self.elastic_uri = elastic_uri
		self.elastic_index = elastic_index

	def parse(self, response):
		#print "queued %d" % len(self.crawler.engine.slot.scheduler)
		print colorama.Fore.GREEN + "[+] open %s" % (response.url,) + colorama.Fore.RESET,
		item = AllCrawl2Item()
		item['inurl'] = response.url
		item['site'] = 'local'
		item['ext'] = splitext( urlparse( response.url ).path )[1][1:].lower()
		item.update( parsers.get_content( response.body, item ) )
		print ''
		return item
