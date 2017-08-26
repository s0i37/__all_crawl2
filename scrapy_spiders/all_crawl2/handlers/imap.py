from urlparse import urlparse
from scrapy.http import Request, Response
import json
import imaplib

class ImapHandler():
    def __init__(self, settings):
        self.imap = None
        self.folder = None
        self.message_id = None

    def __del__(self):
        self.imap.close()
        self.imap.logout()

    def download_request(self, request, spider):
        netloc = urlparse(request.url).netloc
        path = filter( lambda x:x, urlparse(request.url).path.split('/') )

        if len(path):
            self.folder = path.pop(0)
        if len(path):
            self.message_id = path.pop(0)
        
        if not self.imap:
            self.imap = imaplib.IMAP4_SSL(netloc)
            try:
                self.imap.login( spider.user, spider.password )
            except:
                print "access denied"
                return

        if not self.folder:
            resp, mailboxes = self.imap.list('""', '*')
            folders = map( lambda x:x.split()[2], mailboxes )
        else:
            folders = [self.folder]

        if not self.message_id:
            for folder in folders:
                self.imap.select(folder)
                typ, data = self.imap.search(None, 'ALL')
                messages = []
                for num in data[0].split():
                    messages.append( "%s%s/%s" % (request.url, folder, num) )
                body = json.dumps(messages)
        else:
            self.imap.select(self.folder)
            typ, data = self.imap.fetch(self.message_id, '(RFC822)')
            body = data[0][1]
        return Response( url=request.url, status=200, body=body )
