from urlparse import urlparse
from re import escape, match
from scrapy.exceptions import IgnoreRequest
import logging

logger = logging.getLogger(__name__)

class FilterOutsideRequests:
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_request(self, request, spider):
		path = urlparse(request.url).path or '/'
		for allow_path in spider.allow_path:
			if not match( escape(allow_path), path ):
				raise IgnoreRequest( "outside scope %s" )
		for deny_path in spider.deny_path:
			if match( escape(deny_path), path ):
				raise IgnoreRequest( "outside scope %s" )

class PrintError:
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_exception(self, request, exception, spider):
		logger.debug( exception.message )
		print "[!] load %s : %s" % ( request.url, exception.message)
