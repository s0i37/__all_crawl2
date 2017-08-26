from subprocess import Popen, PIPE
import colorama

ext = ['.doc', '.docx']
mimetypes = []

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[docx parser]' + colorama.Fore.RESET, 

	if not 'filetype' in items:
		items['filetype'] = 'doc'
	items['intext'] = items['intext'] if 'intext' in items else ''
	proc = Popen( "catdoc", stdin=PIPE, stdout=PIPE )
	items['intext'] += proc.communicate( input=content )[0] + ' '

	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
