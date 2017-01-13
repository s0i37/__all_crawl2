from subprocess import Popen, PIPE

ext = ['.img','.bin']
mimetypes = ['application/octet-stream']

def extract_text(response, item):
	print '[debug] raw parser'
	if not 'filetype' in item:
		item['filetype'] = 'raw'
	item['intext'] = item['intext'] if 'intext' in item else ''
	proc = Popen( "strings", stdin=PIPE, stdout=PIPE )
	item['intext'] += proc.communicate( input=response.body )[0].replace("\n"," ") + ' '
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