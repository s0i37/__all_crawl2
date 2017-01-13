# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTImage, LTFigure
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from PIL import Image
import pyocr

ext = ['.pdf']
mimetypes = []

def __recognize(data):
	text = ''
	tool = pyocr.get_available_tools()[0]
	try:
		for lang in ["rus", "eng"]:
			text += tool.image_to_string( Image.open( BytesIO(data) ), lang=lang, builder=pyocr.builders.TextBuilder() ) + ' '
	except Exception as e:
		print e
	return text

def extract_text(response, item):
	print '[debug] pdf parser'
	if not 'filetype' in item:
		item['filetype'] = 'pdf'
	item['intext'] = item['intext'] if 'intext' in item else ''
	rsrcmgr = PDFResourceManager()
	retstr = BytesIO()
	device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
	inter = PDFPageInterpreter(rsrcmgr, device)
	for page in PDFPage.get_pages( BytesIO(response.body), set(), maxpages=0, password='', caching=True, check_extractable=True ):
		inter.process_page(page)
	text = retstr.getvalue()

	device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
	inter = PDFPageInterpreter(rsrcmgr, device)
	for page in PDFPage.get_pages( BytesIO(response.body), set(), maxpages=0, password='', caching=True, check_extractable=True ):
		inter.process_page(page)
		for layout in device.get_result():
			if isinstance( layout, (LTImage,LTFigure) ):
				for i in layout:
					print '[debug] pdf recognize page'
					print __recognize( i.stream.rawdata )
	
	item['intext'] += text + ' ' if text else ''
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