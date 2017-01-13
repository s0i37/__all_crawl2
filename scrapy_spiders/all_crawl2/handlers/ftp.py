import json
from os.path import split

from twisted.protocols.ftp import FTPFileListProtocol

from scrapy.http import Response
from scrapy.core.downloader.handlers.ftp import FTPDownloadHandler, ReceivedDataProtocol


class FtpListingHandler(FTPDownloadHandler):
    def gotClient(self, client, request, filepath):
        self.client = client
        if split(filepath)[1]:  # is file
            protocol = ReceivedDataProtocol()
            return client.retrieveFile(filepath, protocol)\
                .addCallbacks(callback=self._build_response,
                        callbackArgs=(request, protocol),
                        errback=self._failed,
                        errbackArgs=(request,))
        else:   # is dir
            protocol = FTPFileListProtocol()
            return client.list(filepath[1:], protocol).addCallbacks(
                callback=self._build_response_dir, callbackArgs=(request, protocol),
                errback=self._failed, errbackArgs=(request,))

    def _build_response_dir(self, result, request, protocol):
        self.result = result
        body = json.dumps(protocol.files)
        return Response(url=request.url, status=200, body=body)