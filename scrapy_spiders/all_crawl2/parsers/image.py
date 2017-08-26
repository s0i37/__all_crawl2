from PIL import Image
import pyocr
from io import BytesIO
import colorama

ext = ['.jpg', '.jpeg', '.png', '.tiff']
mimetypes = ['image/']


def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[image parser]' + colorama.Fore.RESET

	if not 'filetype' in items:
		items['filetype'] = 'image'
	items['intext'] = items['intext'] if 'intext' in items else ''
	tool = pyocr.get_available_tools()[0]
	for lang in ["rus", "eng"]:
		items['intext'] += tool.image_to_string( Image.open( BytesIO(content) ), lang=lang, builder=pyocr.builders.TextBuilder() ) + ' '
	
	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items

