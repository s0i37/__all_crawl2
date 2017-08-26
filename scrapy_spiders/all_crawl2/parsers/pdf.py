# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTImage, LTFigure
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from PIL import Image
import pyocr
import colorama

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

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[pdf parser]' + colorama.Fore.RESET ,

	items['filetype'] = 'pdf'
	items['intext'] = ''
	rsrcmgr = PDFResourceManager()
	retstr = BytesIO()
	device = TextConverter( rsrcmgr, retstr, codec='utf-8', laparams=LAParams() )
	inter = PDFPageInterpreter(rsrcmgr, device)
	for page in PDFPage.get_pages( BytesIO(content), set(), maxpages=0, password='', caching=True, check_extractable=True ):
		inter.process_page(page)
	text = retstr.getvalue()

	# try recognize
	if not text.strip():
		device = PDFPageAggregator( rsrcmgr, laparams=LAParams() )
		inter = PDFPageInterpreter(rsrcmgr, device)
		for page in PDFPage.get_pages( BytesIO(content), set(), maxpages=0, password='', caching=True, check_extractable=True ):
			inter.process_page(page)
			for layout in device.get_result():
				if isinstance( layout, (LTImage,LTFigure) ):
					for i in layout:
						#print '[debug] pdf recognize page'
						text = __recognize( i.stream.rawdata )
	
	items['intext'] += text + ' ' if text else ''
	
	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
