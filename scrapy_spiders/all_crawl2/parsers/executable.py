from subprocess import Popen, PIPE
import colorama

ext = ['.exe','.dll', '.msi', 'msu']
mimetypes = ['application/x-executable', 'application/x-dosexec', 'application/x-msi',
	'application/.*']

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[executable parser]' + colorama.Fore.RESET, 

	if not 'filetype' in items:
		items['filetype'] = 'exe'
	items['intext'] = items['intext'] if 'intext' in items else ''
	proc = Popen( "strings", stdin=PIPE, stdout=PIPE )
	items['intext'] += proc.communicate( input=content )[0].replace("\n"," ") + ' '

	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items

