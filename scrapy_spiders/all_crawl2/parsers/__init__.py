import pkgutil
from urlparse import urlparse
from urllib import urlencode
import mimetypes, magic
from re import match, escape

import colorama

def get_content(content, items):
	found_parser = None
	mimetype = mime.from_buffer(content).lower()
	for parser in parsers:
		for ext in parser.ext:
			if mimetype == mimetypes.types_map.get(ext):
				found_parser = parser
				break
	if not found_parser:
		for parser in parsers:
			for _mimetype in parser.mimetypes:
				if match( escape( _mimetype ), mimetype ):
					found_parser = parser
					break
	if found_parser:
		return found_parser.extract_text(content, items)
	else:
		print colorama.Fore.RED + ' mime {mime} not found'.format( mime=mimetype ) + colorama.Fore.RESET
		return items

parsers = []
for loader,module_name,is_package in pkgutil.walk_packages( __path__ ):
	if not is_package:
		print colorama.Fore.YELLOW + "[*] load parser {parser}".format( parser=module_name ) + colorama.Fore.RESET
		parser = loader.find_module(module_name).load_module(module_name)
		parser.get_content = get_content
		parsers.append( parser )

mime = magic.Magic(mime=True)
