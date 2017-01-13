# -*- coding: utf-8 -*-
import xlrd

ext = ['.xls','.xlsx']
mimetypes = []
CODEPAGE = 'cp1251'

def extract_text(response, item):
	print '[debug] xlsx parser'
	if not 'filetype' in item:
		item['filetype'] = 'xls'
	item['intitle'] = item['intitle'] if 'intitle' in item else ''
	item['intext'] = item['intext'] if 'intext' in item else ''
	rb = xlrd.open_workbook( file_contents=response.body, encoding_override=CODEPAGE )
	for sheet_name in rb.sheet_names():
		item['intitle'] += sheet_name.strip() + ' ' if sheet_name else ''
		sheet = rb.sheet_by_name( sheet_name )
		for row in range(sheet.nrows):
			for col in range(sheet.ncols):
				item['intext'] += sheet.row_values(row)[col].strip() + ' ' if sheet.row_values(row)[col] else ''
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