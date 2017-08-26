# -*- coding: utf-8 -*-
import scrapy
from all_crawl2.items import AllCrawl2Item
from all_crawl2 import parsers

from urlparse import urlparse
from os.path import splitext, basename

import colorama

class WebSpider(scrapy.Spider):
	name = "www"
	allowed_domains = []
	start_urls = []

	'''
	def start_requests(self):
		return [scrapy.FormRequest("http://www.example.com/login",
			formdata={'user': 'john', 'pass': 'secret'},
			callback=self.logged_in)]
	'''

	def __init__(self, uri='', zone='', allow_path='/', deny_path='', user='', password='', elastic_uri='', elastic_index='default', *args, **kwargs):
		super(WebSpider, self).__init__(*args, **kwargs)
		if uri:
			self.start_urls.extend( uri.split(' ') )
		self.allowed_domains.extend( zone.split(' ') if zone else map(lambda uri: urlparse(uri).netloc.split(':')[0], uri.split(' ')) )
		self.name = '+'.join( zone.split(' ') if zone else map( lambda u:urlparse(u).netloc, uri.split(' ') ) )
		self.allow_path = allow_path.split(' ')
		self.deny_path = deny_path.split(' ') if deny_path else []
		self.elastic_uri = elastic_uri
		self.elastic_index = elastic_index
		self.http_user = user
		self.http_pass = password

	def parse(self, response):
		#print "queued %d" % len(self.crawler.engine.slot.scheduler)
		print colorama.Fore.GREEN + "[+] open %s" % (response.url,) + colorama.Fore.RESET, 
		items = AllCrawl2Item()
		items['inurl'] = response.url
		items['site'] = urlparse( response.url ).netloc.lower()
		items['ext'] = splitext( urlparse( response.url ).path )[1][1:].lower()
		for item in parsers.get_content( response.body, items ):
			yield item
		print ''
