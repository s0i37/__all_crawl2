#!/usr/bin/env python
#-*- coding:utf-8 -*-

import imaplib
import getpass
import argparse
from all_crawl2.parsers import parse

class Response:
	def __init__(self, text):
		self.body = text
		self.text = text

argparser = argparse.ArgumentParser(description="Dump a IMAP folder into .eml files")
argparser.add_argument('host', help="IMAP host")
argparser.add_argument('-u', dest='username', help="IMAP username", required=True)
argparser.add_argument('-f', dest='folder', help="Remote folder to download (INBOX)", default='')
args = argparser.parse_args()

imap = imaplib.IMAP4_SSL(args.host)
try:
	imap.login(args.username, getpass.getpass())
except:
	print "access denied"
	exit()
resp, mailboxes = imap.list('""', '*')
for mailbox in mailboxes:
	folder = mailbox.split()[2]
	if args.folder and args.folder.lower() != folder.lower():
		break
	print "[*] %s" % folder
	imap.select(folder)
	typ, data = imap.search(None, 'ALL')
	for num in data[0].split():
		typ, data = imap.fetch(num, '(RFC822)')
		response = Response( data[0][1] )
		item = {}
		item['inurl'] = "%s/%s/%s" % (args.host, args.folder, num)
		item['site'] = args.host.lower()
		item['ext'] = ''
		parse.get_content( response, item )
		print str(item)
imap.close()
imap.logout()