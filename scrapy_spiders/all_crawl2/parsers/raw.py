from subprocess import Popen, PIPE
import colorama

ext = ['.img','.bin']
mimetypes = ['application/octet-stream']

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[raw parser]' + colorama.Fore.RESET, 

	if not 'filetype' in items:
		items['filetype'] = 'raw'
	items['intext'] = items['intext'] if 'intext' in items else ''
	proc = Popen( "strings", stdin=PIPE, stdout=PIPE )
	items['intext'] += proc.communicate( input=content )[0].replace("\n"," ") + ' '

	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
