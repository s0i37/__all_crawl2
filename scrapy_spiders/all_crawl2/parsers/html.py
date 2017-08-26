from lxml import etree
from io import StringIO
import colorama

ext = ['.htm','.html','.phtml','.php','.asp','.aspx','.jsp','.do']
mimetypes = ['text/html']
ignore_tags = ['script','style']

def extract_text( content, items ):
	print colorama.Fore.LIGHTYELLOW_EX + '[html parser]' + colorama.Fore.RESET, 

	if not 'filetype' in items:
		items['filetype'] = 'html'
	parser = etree.HTMLParser()
	x = etree.parse( StringIO( content.decode('utf-8') ), parser )
	items['intitle'] = items['intitle'] if 'intitle' in items else ''
	items['intext'] = items['intext'] if 'intext' in items else ''
	for tag in x.xpath('//*'):
		tag_name = tag.xpath('name()').lower()
		if not tag_name in ignore_tags:
			text = tag.xpath('text()')
			if tag_name in ['title']:
				items['intitle'] += text[0].strip() + ' ' if text else ''
			else:
				items['intext'] += text[0].strip() + ' ' if text else ''

	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
