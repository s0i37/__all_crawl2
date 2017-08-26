# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from all_crawl2.items import AllCrawl2Item
from all_crawl2 import parsers

from urlparse import urlparse
from os.path import splitext, basename
from urllib import unquote
import json
from os.path import split
from time import sleep

import colorama

class SmbSpider(scrapy.Spider):
	name = "smb"
	allowed_domains = []
	start_urls = []

	def __init__(self, uri='', zone='', domain='', user='', password='', allow_path='/', deny_path='', elastic_uri='', elastic_index='default', *args, **kwargs):
		super(SmbSpider, self).__init__(*args, **kwargs)
		if uri:
			self.start_urls.extend( uri.split(' ') )
		self.allowed_domains.extend( zone.split(' ') if zone else map(lambda uri: urlparse(uri).netloc.split(':')[0], uri.split(' ')) )
		self.name = '+'.join( zone.split(' ') if zone else map( lambda u:urlparse(u).netloc, uri.split(' ') ) )
		self.domain = domain
		self.user = user
		self.password = password
		self.allow_path = allow_path.split(' ')
		self.deny_path = deny_path.split(' ') if deny_path else []
		self.elastic_uri = elastic_uri
		self.elastic_index = elastic_index

	def parse(self, response):
		#print "queued %d" % len(self.crawler.engine.slot.scheduler)
		print colorama.Fore.GREEN + "[+] open %s" % (response.url,) + colorama.Fore.RESET ,
		items = AllCrawl2Item()
		items['inurl'] = response.url
		items['site'] = urlparse( response.url ).netloc.lower()
		items['ext'] = splitext( urlparse( response.url ).path )[1][1:].lower()
		if not split(response.url)[1]:	# is dir
			#item["intext"] = ''
			for _file in json.loads( response.body ):
				#item["intext"] += _file + ' '
				yield Request( response.url + _file )
			#for _item in item:
			#	yield _item
		else:	# is file
			for item in parsers.get_content( response.body, items ):
				yield item
		print ''

