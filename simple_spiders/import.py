from sys import argv
import getopt
from os.path import splitext
from elasticsearch import Elasticsearch
from urlparse import urlparse
import base64, re

schema = "http"
opts, args = getopt.getopt( argv[1:], "s:", ["schema="] )
for opt,val in opts:
	if opt == "-s":
		schema = val

if len(args) < 1:
	print "%s [-s|--schema=http|https|ftp] site_file elasticsearch_addr [index]" % argv[0]
	exit()

index_file = args[0]
es = Elasticsearch( args[1] )
index = args[2] if len(args) > 2 else 'default' 
path = ''
data = ''
filetype = ''
with open( index_file, "r" ) as f:
	while True:
		line = f.readline()
		if line.startswith(">>>"):
			if path and data:
				try:
					page = {
						"inurl": "%s://%s" % (schema,path),
						"site": urlparse( "%s://%s" % (schema,path) ).netloc,
						"ext": splitext( urlparse( "%s://%s" % (schema,path) ).path )[1][1:].lower(),
						"intitle": data.split("\n")[0] if filetype == 'html' else path,
						"intext": data,
						"filetype": filetype
					}
					print path
					es.index( index=index, doc_type='page', id=re.sub( r'[\n/]', '', base64.encodestring( page["inurl"] ) ), body=page )
				except:
					pass
			path = line[3:].split("\n")[0]
			data = filetype = ""
		elif line.startswith("<<<"):
			filetype = line[3:].split("\n")[0]
		else:
			data += line
		if not line:
			break

