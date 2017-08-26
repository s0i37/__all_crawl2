from urlparse import urlparse
import json
import os

class FileHandler():
    def __init__(self, settings):
        pass

    def download_request(self, request, spider):
        netloc = urlparse(request.url).netloc
        path = filter( lambda x:x, urlparse(request.url).path.split('/') )
        if os.path.isdir(path):
            for _file in os.listdir(path):
                if not _file in [".", ".."]:
                    files.append( _file.filename + '/' if os.path.isdir(_file) else _file )
            body = json.dumps(files)
        else:
            with open(path, 'rb') as f:
                body = f.read()
        return Response( url=request.url, status=200, body=body )
