import os
import urllib2
from ntlm import HTTPNtlmAuthHandler
from scrapy.http import TextResponse

class NtlmAuthMiddleware(object):

	def process_request(self, request, spider):
		usr = '%s\%s' % (os.environ["USERDOMAIN"], getattr(spider, 'http_user', ''))
		pwd = getattr(spider, 'http_pass', '')
		url = request.url

		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, url, usr, pwd)

		# Create the NTLM authentication handler.
		auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

		# Create and install the opener.
		opener = urllib2.build_opener(auth_NTLM)
		urllib2.install_opener(opener)

		# Retrieve the result.
		resp = urllib2.urlopen(url)
		msg = resp.info()

		return HtmlResponse(url=url, status=resp.getcode(), headers=msg.items(), body=resp.read())
