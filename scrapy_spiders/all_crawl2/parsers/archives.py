from zipfile import ZipFile
from io import BytesIO
from os.path import splitext
from all_crawl2.items import AllCrawl2Item
import colorama

ext = ['.zip','.7z']
mimetypes = []

get_content = lambda x:x

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[zip parser]' + colorama.Fore.RESET

	items['filetype'] = 'zip'
	items['intext'] = ''
	z = ZipFile( BytesIO( content ) )
	nested_items = []
	for compressed_filepath in z.namelist():
		nested_item = AllCrawl2Item()
		items['intext'] += compressed_filepath + '\n'
		compressed_filedata = z.read(compressed_filepath)
		nested_item['site'] = items['site']
		nested_item['inurl'] = items['inurl'] + '/' + compressed_filepath
		nested_item['ext'] = splitext(compressed_filepath)[1][1:].lower()
		nested_item['filetype'] = ''
		nested_item['intext'] = ''
		print colorama.Fore.LIGHTGREEN_EX + "\t %s/%s" % (items['inurl'],compressed_filepath) + colorama.Fore.RESET, 
		nested_item = get_content(compressed_filedata, nested_item)
		if type(nested_item) == list:
			nested_items.extend( nested_item )
		else:
			nested_items.append( nested_item )
	nested_items.append(items)
	
	return nested_items

