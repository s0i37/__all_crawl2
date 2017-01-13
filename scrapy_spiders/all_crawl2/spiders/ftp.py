# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from all_crawl2.items import AllCrawl2Item
from all_crawl2.parsers import parse

from urlparse import urlparse
import json
from os.path import split


class FtpSpider(scrapy.Spider):
	name = "ftp"
	allowed_domains = []
	custom_settings = {
		'DOWNLOAD_DELAY': 2
	}
	
	def start_requests(self):
		yield Request(
			url = self.uri,
			meta = { 'ftp_user': self.ftp_user, 'ftp_password': self.ftp_password }
		)

	def __init__(self, uri='', zone='', allow_path='/', deny_path='', ftp_user='anonymous', ftp_password='anonymous@mail.com', elastic_uri='', elastic_index='default', *args, **kwargs):
		super(FtpSpider, self).__init__(*args, **kwargs)
		self.uri = uri
		self.allowed_domains.extend( zone.split(' ') if zone else map(lambda uri: urlparse(uri).netloc.split(':')[0], uri.split(' ')) )
		self.name = '+'.join( zone.split(' ') if zone else map( lambda u:urlparse(u).netloc, uri.split(' ') ) )
		self.allow_path = allow_path.split(' ')
		self.deny_path = deny_path.split(' ') if deny_path else []
		self.ftp_user = ftp_user
		self.ftp_password = ftp_password
		self.elastic_uri = elastic_uri
		self.elastic_index = elastic_index


	def parse(self, response):
		#print "queued %d" % len(self.crawler.engine.slot.scheduler)
		print "[*] open %s" % response.url
		if not split(response.url)[1]:	# is dir
			files = json.loads( response.body )
			for _file in files:
				print '[debug] %s' % ( _file['filename'] + '/' if _file['filetype'] == 'd' else _file['filename'] )
				if _file['filetype'] == 'd':
					yield Request( response.urljoin( _file['filename'] + '/' ), meta = { 'ftp_user': self.ftp_user, 'ftp_password': self.ftp_password } )
				if _file['filetype'] == '-':
					yield Request( response.urljoin( _file['filename'] ), meta = { 'ftp_user': self.ftp_user, 'ftp_password': self.ftp_password } )
		else:
			item = AllCrawl2Item()
			item['inurl'] = response.url
			item['site'] = urlparse( response.url ).netloc.lower()
			item['ext'] = splitext( urlparse( response.url ).path )[1][1:].lower()
			yield parse.get_content( response, item )

