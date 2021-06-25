import mimetypes
import os
import pathlib
from email.utils import formatdate
from urllib.parse import unquote, urlparse

from httpserver.httpserver import BaseHTTPRequestHandler, HTTPResponse, HTTPServer


def url_normalize(path: str) -> str:
    if path.startswith("."):
        path = "/" + path
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


class FileProducer(object):
    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path: str = ""

    @staticmethod
    def date_time_string():
        return formatdate(timeval=None, localtime=False, usegmt=True)

    def send_head(self) -> HTTPResponse:
        #     NOTE: https://tools.ietf.org/html/rfc3986
        #     NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
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
                "Server": "My Lab Server",
                "Date": self.date_time_string(),
                "Content-Type": str(content_type),
                "Content-Length": str(content_size),
                "Connection": "Closed",
            },
        )

    def do_GET(self):
        try:
            response = self.send_head()
        except FileNotFoundError:
            return self.response_klass(status=404, headers={})
        except PermissionError:
            return self.response_klass(status=403, headers={})
        except:
            return self.response_klass(status=500, headers={})
        else:
            with open(self.path, "rb") as f:
                producer = FileProducer(f)
                file = bytes()
                while chunk := producer.more():
                    file += chunk
                response.body = file
                return response

    def do_HEAD(self):
        try:
            return self.send_head()
        except FileNotFoundError:
            return self.response_klass(status=404, headers={})
        except PermissionError:
            return self.response_klass(status=403, headers={})
        except:
            return self.response_klass(status=500, headers={})


class StaticServer(HTTPServer):
    """
    Static server
    """

    def __init__(self, d_root: pathlib.Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document_root: pathlib.Path = d_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=3,
        d_root=document_root,
        port=5000,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
