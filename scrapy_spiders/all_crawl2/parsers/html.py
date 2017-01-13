from lxml import etree
from io import StringIO

ext = ['.htm','.html','.phtml','.php','.asp','.aspx','.jsp','.do']
mimetypes = ['text/html']
ignore_tags = ['script','style']

def extract_text( response, item ):
	#print '[debug] html parser'
	if not 'filetype' in item:
		item['filetype'] = 'html'
	parser = etree.HTMLParser()
	x = etree.parse( StringIO( response.text ), parser )
	item['intitle'] = item['intitle'] if 'intitle' in item else ''
	item['intext'] = item['intext'] if 'intext' in item else ''
	for tag in x.xpath('//*'):
		tag_name = tag.xpath('name()').lower()
		if not tag_name in ignore_tags:
			text = tag.xpath('text()')
			if tag_name in ['title']:
				item['intitle'] += text[0].strip() + ' ' if text else ''
			else:
				item['intext'] += text[0].strip() + ' ' if text else ''
	return item

if __name__ == '__main__':
	from sys import argv
	class Response:
		body = ''
		text = u''
	with open( argv[1], 'rb ') as f:
		Response.text = f.read().decode('utf-8')	#!
		for collector,text in extract_text( Response, {} ).items():
			print "{}: {}".format( collector, text )