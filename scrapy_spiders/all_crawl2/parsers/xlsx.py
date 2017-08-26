# -*- coding: utf-8 -*-
import xlrd
import colorama

ext = ['.xls','.xlsx']
mimetypes = []
CODEPAGE = 'cp1251'

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[xlsx parser]' + colorama.Fore.RESET, 

	if not 'filetype' in items:
		items['filetype'] = 'xls'
	items['intitle'] = items['intitle'] if 'intitle' in items else ''
	items['intext'] = items['intext'] if 'intext' in items else ''
	rb = xlrd.open_workbook( file_contents=content, encoding_override=CODEPAGE )
	for sheet_name in rb.sheet_names():
		items['intitle'] += sheet_name.strip() + ' ' if sheet_name else ''
		sheet = rb.sheet_by_name( sheet_name )
		for row in range(sheet.nrows):
			for col in range(sheet.ncols):
				items['intext'] += sheet.row_values(row)[col].strip() + ' ' if sheet.row_values(row)[col] else ''
	
	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items

