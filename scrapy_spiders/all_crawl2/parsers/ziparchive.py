from zipfile import ZipFile
from io import BytesIO
from os.path import splitext

from parse import get_content

ext = ['.zip','.7z']
mimetypes = []

def extract_text(response, item):
	print '[debug] zip parser'
	if not 'filetype' in item:
		item['filetype'] = 'zip'
	item['intext'] = item['intext'] if 'intext' in item else ''
	z = ZipFile( BytesIO(response.text) )
	for compressed_filepath in z.namelist():
		item['intext'] += compressed_filepath + ' '
		compressed_filedata = z.read(compressed_filepath)
		item.update( get_content(compressed_filedata, item) )
	return item

if __name__ == '__main__':
	from sys import argv
	with open( argv[1], 'rb ') as f:
		for collector,text in extract_text( f.read(), {} ).items():
			print "{}: {}".format( collector, text )