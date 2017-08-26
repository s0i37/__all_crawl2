import scrapy
from urlparse import urlparse
from re import escape, match
import logging
import colorama

logger = logging.getLogger(__name__)

class FilterOutsideLinks:
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_spider_output(self, response, result, spider):
		for result_entry in result:
			if isinstance(result_entry, scrapy.Request):
				path = urlparse(result_entry.url).path
				for allow_path in spider.allow_path:
					if not match( escape(allow_path), path ):
						logger.debug( "outside scope %s" % path )
						continue
				for deny_path in spider.deny_path:
					if match( escape(deny_path), path ):
						continue
				yield result_entry
			else:
				yield result_entry


class LogExternalLinks:
	def __init__(self, is_log_external_links=True ):
		self.is_log_external_links = is_log_external_links

	@classmethod
	def from_crawler(cls, crawler):
		is_log_external_links = crawler.settings.getbool("LOG_EXTERNAL_LINKS")
		return cls(is_log_external_links)

	def process_spider_output(self, response, result, spider):
		redis = spider.crawler.engine.slot.scheduler.queue.server
		for result_entry in result:
			if self.is_log_external_links and isinstance(result_entry, scrapy.Request) and self.__is_external_link( redis, spider.allowed_domains, urlparse(result_entry.url).netloc ):
				redis.sadd( "external:{url}".format( url=urlparse(result_entry.url).netloc ), result_entry.url )
			yield result_entry

	def __is_external_link(self, redis, allowed_domains, url):
		for allowed_domain in allowed_domains:
			if not match( ".*\\." + allowed_domain.replace(".", "\\."), url ) and\
			not url in map( lambda x:x.split(":")[0], redis.keys("*:requests") ):
				return True

class PrintError:
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_spider_exception(self, response, exception, spider):
		logger.debug( exception.message )
		print colorama.Fore.RED + "[!] parse %s : %s" % ( spider.name, exception.message ) + colorama.Fore.RESET