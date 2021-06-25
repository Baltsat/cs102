import mimetypes
import os
import pathlib
import time
import typing as tp
from urllib.parse import unquote, urlparse

from httpserver import BaseHTTPRequestHandler, HTTPRequest, HTTPResponse, HTTPServer


def url_normalize(path: str) -> str:
    if path.startswith("."):
        path = "/" + path
    # TODO: обработка стандартного порта
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1 + 3 :]
        else:
            path = path.replace("/..", "", 1)
            path = path.replace("/./", "/")
            path = path.replace("/.", "")
    return path


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        _url = urlparse(self._urn)
        self.path, qs = _url.path, _url.query
        self.path = url_normalize(unquote(self.path))
        self.path = self.path.strip("/")

        self.path = os.path.join(self.server.document_root, *os.path.split(self.path))

        if os.path.isdir(self.path):
            self.path += "index.html"
            if not os.path.exists(self.path):
                raise PermissionError

        content_type, _ = mimetypes.guess_type(self.path)
        content_size = os.path.getsize(self.path)

        return self.response_klass(
            status=200,
            headers={
                "Server": "My Server",
                "Date": self.date_time_string(),
                "Content-Type": str(content_type),
                "Content-Length": str(content_size),
                "Connection": "Closed",
            },
        )

    def do_HEAD(self):
        pass
    
    def do_HEAD(self):
        pass






class StaticServer(HTTPServer):
    def __init__(self, d_root: pathlib.Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_root: pathlib.Path = d_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=5,
        document_root=document_root,
        port=5000,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
