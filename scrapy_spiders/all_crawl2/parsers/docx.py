from subprocess import Popen, PIPE

ext = ['.doc', '.docx']
mimetypes = []

def extract_text(response, item):
	print '[debug] docx parser'
	if not 'filetype' in item:
		item['filetype'] = 'doc'
	item['intext'] = item['intext'] if 'intext' in item else ''
	proc = Popen( "catdoc", stdin=PIPE, stdout=PIPE )
	item['intext'] += proc.communicate( input=response.body )[0] + ' '
	return item

if __name__ == '__main__':
	from sys import argv
	class Response:
		body = ''
		text = u''
	with open( argv[1], 'rb') as f:
		Response.body = f.read()
		for collector,text in extract_text( Response, {} ).items():
			print "{}: {}".format( collector, text )