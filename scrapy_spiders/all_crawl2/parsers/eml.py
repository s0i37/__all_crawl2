import email
from all_crawl2.items import AllCrawl2Item
import colorama

ext = ['.eml']
mimetypes = ['message/rfc822']

get_content = lambda x:x

def extract_text( content, items ):
	print colorama.Fore.LIGHTYELLOW_EX + '[eml parser]' + colorama.Fore.RESET, 

	mail = email.message_from_string(content)
	items['intitle'] = mail['from'] + "\n"
	items['intitle'] += mail['to'] + "\n"
	items['intitle'] += mail['subject'] + "\n"
	part_num = 0
	nested_items = []
	while True:
		try:
			part = mail.get_payload(part_num)
		except:
			break
		nested_item = AllCrawl2Item()
		nested_item['site'] = items['site']
		nested_item['inurl'] = items['inurl'] + '/' + part.get_content_name()
		nested_item['filetype'] = part.get_content_type()
		nested_item = get_content( Response( part.get_payload() ), nested_item)
		if type(nested_item) == list:
			nested_items.extend(nested_item)
		else:
			nested_items.append(nested_item)
		part_num += 1
	nested_items.append(items)

	print colorama.Fore.LIGHTGREEN_EX + "(%d words)" % len( items['intext'].split() ) + colorama.Fore.RESET
	return items
