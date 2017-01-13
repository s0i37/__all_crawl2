from smb import SMBConnection
from os.path import split
from io import BytesIO
from urlparse import urlparse
from urllib import unquote
import json
from scrapy.http import Response

class SmbHandler():
    def __init__(self, settings):
        self.smb = None

    def download_request(self, request, spider):
        netloc = urlparse(request.url).netloc
        dirs = urlparse(request.url).path.split('/')
        share = dirs.pop(1)
        path = '/'.join(dirs[1:])
        if not self.smb:
            self.smb = SMBConnection.SMBConnection(spider.user, spider.password, spider.domain, spider.domain, use_ntlm_v2=True)
            self.smb.connect( netloc, 139 )
        if not split( request.url )[1]: # is dir
            files = []
            for _file in self.smb.listPath( share, unquote(path) ):
                if not _file.filename in [".", ".."]:
                    files.append( _file.filename + '/' if _file.isDirectory else _file.filename )
            body = json.dumps(files)
        else:   # is file
            buff = BytesIO()
            self.smb.retrieveFile( share, unquote(path) , buff )
            buff.seek(0)
            body = buff.read()

        #respcls = responsetypes.from_args(filename=filepath, body=body)
        return Response( url=request.url, status=200, body=body )