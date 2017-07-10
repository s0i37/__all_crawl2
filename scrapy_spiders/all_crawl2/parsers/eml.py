import email
from parse import get_content

ext = ['.eml']
mimetypes = ['message/rfc822']

class Response:
	def __init__(self, text):
		self.body = text
		self.text = text

def extract_text( response, item ):
	mail = email.message_from_string( response.body )
	item['intitle'] = mail['from']
	item['intitle'] += mail['to']
	item['intitle'] += mail['subject']
	part_num = 0
	while True:
		try:
			part = mail.get_payload(part_num)
		except:
			break
		item['filetype'] = part.get_content_type()
		item.update( get_content( Response(part.get_payload()), item) )
		part_num += 1
	return item

if __name__ == '__main__':
	import sys
	with open( sys.argv[1], 'rb' ) as f:
		response = Response( f.read() )
	print extract_text( response, {} )