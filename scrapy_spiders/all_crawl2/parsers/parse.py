import scrapy
from urlparse import urlparse
from urllib import urlencode
import mimetypes, magic
from re import match, escape
from os import listdir
from sys import path

mime = magic.Magic(mime=True)

def get_content(response, item):
	import html, docx, xlsx, pdf, Xml, plaintext, executable, image, ziparchive, raw

	parsers = [html, docx, xlsx, pdf, Xml, plaintext, executable, image, ziparchive, raw]

	found_parser = None
	mimetype = mime.from_buffer( response.body ).lower()
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
		return found_parser.extract_text( response, item )
	else:
		print '[!] mime {mime} not found'.format( mime=mimetype )
		return item
