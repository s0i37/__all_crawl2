import colorama

ext = ['.txt','.ini','.conf','.cfg','.cnf']
mimetypes = ['text/']

def extract_text(content, items):
	print colorama.Fore.LIGHTYELLOW_EX + '[plaintext parser]' + colorama.Fore.RESET ,

	items['filetype'] = 'text'
	items['intext'] = content
	
	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
