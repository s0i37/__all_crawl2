ext = ['.txt','.ini','.conf','.cfg','.cnf']
mimetypes = ['text/']

def extract_text(response, item):
	print '[debug] plaintext parser'
	if not 'filetype' in item:
		item['filetype'] = 'text'
	item['intext'] = item['intext'] if 'intext' in item else ''
	item['intext'] += response.body + ' '
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