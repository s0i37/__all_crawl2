from lxml import etree
import colorama

ext = ['.xml']
mimetypes = []

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[xml parser]' + colorama.Fore.RESET,

	if not 'filetype' in items:
		items['filetype'] = 'xml'
	items['intext'] = items['intext'] if 'intext' in items else ''
	root = etree.fromstring( bytes(content) )
	for element in root.xpath("//*"):
		tag = element.xpath('name()')
		text = element.xpath('text()')
		items['intext'] += "{tag}: {text} ".format( tag=tag, text=text[0].strip() ) if text else ''
	
	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
