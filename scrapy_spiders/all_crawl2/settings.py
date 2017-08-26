# -*- coding: utf-8 -*-

# Scrapy settings for all_crawl2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'all_crawl2'

SPIDER_MODULES = ['all_crawl2.spiders']
NEWSPIDER_MODULE = 'all_crawl2.spiders'

#redis queue implementation
'''
SCHEDULER = "all_crawl2.queue.scheduler.Scheduler"
DUPEFILTER_CLASS = "all_crawl2.queue.dupefilter.RFPDupeFilter"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SCHEDULER_SERIALIZER = "all_crawl2.queue.picklecompat"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'all_crawl2.queue.queue.SpiderPriorityQueue'
SCHEDULER_IDLE_BEFORE_CLOSE = 10
'''

DEPTH_LIMIT = 5
DEPTH_PRIORITY = -1

DOWNLOAD_HANDLERS = {
	#'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
	'file': 'all_crawl2.handlers.file.FileHandler',
	'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
	'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
	#'ftp': 'all_crawl2.handlers.ftp.FtpListingHandler',
	'ftp': 'scrapy.core.downloader.handlers.ftp.FTPDownloadHandler',
	'smb': 'all_crawl2.handlers.samba.SmbHandler',
	'imap': 'all_crawl2.handlers.imap.ImapHandler',
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# append to default SPIDER_MIDDLEWARES
SPIDER_MIDDLEWARES = {
	'all_crawl2.spidermiddlewares.extracts.HrefsFromA': 100,
	'all_crawl2.spidermiddlewares.extracts.HrefsFromText': 200,
	'all_crawl2.spidermiddlewares.filters.FilterOutsideLinks': 900,
	#'all_crawl2.spidermiddlewares.filters.LogExternalLinks': 950,
	'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 1,
	'all_crawl2.spidermiddlewares.filters.PrintError': 2
}
ALLOWED_SCHEMES = ["http", "https", "ftp", "smb", "imap"]
LOG_EXTERNAL_LINKS = False
REFERER_ENABLED = True

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# append to default DOWNLOADER_MIDDLEWARES
DOWNLOADER_MIDDLEWARES = {
	'all_crawl2.downloadmiddlewares.filters.FilterOutsideRequests': 1,
	'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 500,
	#'all_crawl2.downloadmiddlewares.ntlmauth.NtlmAuthMiddleware': 600,
	'all_crawl2.downloadmiddlewares.filters.PrintError': 999
}
DOWNLOAD_MAXSIZE = 1 * 1024 * 1024
REDIRECT_ENABLED = True
RETRY_ENABLED = True
RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 421]

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
	'scrapy.extensions.closespider.CloseSpider': 100
}
CLOSESPIDER_TIMEOUT = 0
CLOSESPIDER_ITEMCOUNT = 0
CLOSESPIDER_PAGECOUNT = 0
CLOSESPIDER_ERRORCOUNT = 0

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'all_crawl2.pipelines.AllCrawl2Pipeline': 300,
    'all_crawl2.pipelines.ElasticsearchPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#LOG_ENABLED = False