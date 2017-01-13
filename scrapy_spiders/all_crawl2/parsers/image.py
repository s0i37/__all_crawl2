from PIL import Image
import pyocr
from io import BytesIO

ext = ['.jpg', '.jpeg', '.png', '.tiff']
mimetypes = ['image/']


def extract_text(response, item):
	print '[debug] image parser'
	if not 'filetype' in item:
		item['filetype'] = 'image'
	item['intext'] = item['intext'] if 'intext' in item else ''
	tool = pyocr.get_available_tools()[0]
	for lang in ["rus", "eng"]:
		item['intext'] += tool.image_to_string( Image.open( BytesIO(response.body) ), lang=lang, builder=pyocr.builders.TextBuilder() ) + ' '
	return item


if __name__ == '__main__':
	from sys import argv
	class Response:
		body = ''
		text = u''
	with open( argv[1], 'rb ') as f:
		Response.body = f.read()
		for collector,text in extract_text( Response, {} ).items():
			print u"{}: {}".format( collector, text )