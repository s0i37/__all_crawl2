import scrapy
from lxml import etree
from urlparse import urlparse
from re import findall
import logging

logger = logging.getLogger(__name__)

class HrefsFromA:
	def __init__(self, allowed_schemes=["http","https"] ):
		self.allowed_schemes = allowed_schemes

	@classmethod
	def from_crawler(cls, crawler):
		allowed_schemes = crawler.settings.getlist("ALLOWED_SCHEMES")
		return cls(allowed_schemes)

	def process_spider_output(self, response, result, spider):
		if 'xpath' in dir(response):
			for href in response.xpath('//a/@href'):
				uri = response.urljoin( href.extract() )
				if not urlparse(uri).scheme in self.allowed_schemes:
					continue
				logger.debug( u"+ %s" % uri )
				yield scrapy.Request(uri)
		for result_entry in result:
			yield result_entry


class HrefsFromFrame:
	def __init__(self, allowed_schemes=["http","https"] ):
		self.allowed_schemes = allowed_schemes

	@classmethod
	def from_crawler(cls, crawler):
		allowed_schemes = crawler.settings.getlist("ALLOWED_SCHEMES")
		return cls(allowed_schemes)

	def process_spider_output(self, response, result, spider):
		if 'xpath' in dir(response):
			for href in response.xpath('(//iframe | //frame)/@src'):
				uri = response.urljoin( href.extract() )
				if not urlparse(uri).scheme in self.allowed_schemes:
					continue
				logger.debug( u'(i)frame: %s' % uri )
				yield scrapy.Request(uri)
		for result_entry in result:
			yield result_entry


class HrefsFromForm:
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_spider_output(self, response, result, spider):
		if 'xpath' in dir(response):
			for form in response.xpath('//form'):
				logger.debug( '<form> %s' % form.xpath('@action') )
				params = {}
				for _input in form.xpath('input'):
					_input_name = _input.xpath('@name').extract()
					_input_value = _input.xpath('@value').extract()
					_input_name = _input_name[0] if _input_name else ''
					_input_value = _input_value[0] if _input_value else ''
					if _input_name:
						params[ _input_name ] = _input_value
				action = form.xpath('@action').extract()
				url = response.urljoin( action[0] ) if action else response.url
				method = form.xpath('@method').extract()
				method = method[0].lower() if method else 'get'
				if method == 'get':
					yield scrapy.Request( url + '?' + urlencode(params) )
				elif method == 'post':
					yield scrapy.FormRequest( url, formdata=params )
		for result_entry in result:
			yield result_entry


class HrefsFromText:
	def __init__(self, allowed_schemes=["http","https"] ):
		self.allowed_schemes = allowed_schemes

	@classmethod
	def from_crawler(cls, crawler):
		allowed_schemes = crawler.settings.getlist("ALLOWED_SCHEMES")
		return cls(allowed_schemes)

	def process_spider_output(self, response, result, spider):
		links = set()
		for result_entry in result:
			if not isinstance(result_entry, scrapy.Request):
				items = result_entry
				for value_of_item in items.values():
					for word in value_of_item.split(' '):
						for scheme in self.allowed_schemes:
							if not scheme.lower() == 'smb':
								regexp = '({scheme}*://[^\s]*)'.format( scheme=scheme.lower() )
							else:
								regexp = r"(\\\\[^\\\s]*\\[^\s]*)"
							for uri in findall( regexp, word.lower() ):
								if not urlparse(uri).scheme in self.allowed_schemes:
									continue
								links.add( response.urljoin(uri) )
			yield result_entry
		for uri in links:
			logger.debug( u'found in text: %s' % uri )
			yield scrapy.Request(uri)
