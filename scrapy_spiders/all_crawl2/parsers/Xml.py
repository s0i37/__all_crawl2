from lxml import etree

ext = ['.xml']
mimetypes = []

def extract_text(response, item):
	print '[debug] xml parser'
	if not 'filetype' in item:
		item['filetype'] = 'xml'
	item['intext'] = item['intext'] if 'intext' in item else ''
	root = etree.fromstring( bytes( response.body ) )
	for element in root.xpath("//*"):
		tag = element.xpath('name()')
		text = element.xpath('text()')
		item['intext'] += "{tag}: {text} ".format( tag=tag, text=text[0].strip() ) if text else ''
	return item

if __name__ == '__main__':
	from sys import argv
	class Response:
		body = ''
		text = u''
	with open( argv[1], 'rb ') as f:
		Response.body = f.read()
		for collector,text in extract_text( Response, {} ).items():
			print "{}: {}".format( collector, text )