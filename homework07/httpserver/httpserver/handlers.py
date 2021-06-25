# type: ignore

from __future__ import annotations

import select
import socket
import typing as tp

from httptools import HttpRequestParser
from request import HTTPRequest
from response import HTTPResponse

if tp.TYPE_CHECKING:
    from .server import TCPServer

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError):
            pass
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_klass = HTTPRequest
    response_klass = HTTPResponse

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        if request:
            try:
                response = self.handle_request(request)
            except Exception:
                # TODO: log exception
                response = self.response_klass(status=500, headers={}, body=b"")
        else:
            response = self.response_klass(status=400, headers={}, body=b"")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[HTTPRequest]:
        data = self.socket.recv(65536)
        while self._data_avaiable():
            data += self.socket.recv(65536)
        self.parser.feed_data(data)
        self.method = self.parser.get_method().decode()
        return self.request_klass(self.method, self._urn, self._headers, "")

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        # TODO: Метод handle_request в базовой реализации может возвращать ответ с 405 ошибкой.
        method_name = "do_" + self.method
        if not hasattr(self, method_name):
            allowed_methods = [s.replace("do_", "") for s in dir(self) if str(s).startswith("do_")]
            response = self.response_klass(
                status=405, headers={"Allow": ", ".join(allowed_methods)}, body=b""
            )
        else:
            handler = getattr(self, method_name)
            response = handler()
        return response

    def handle_response(self, response: HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    def on_url(self, url: bytes) -> None:
        self._url = url.decode()

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name.decode()] = value.decode()

    def on_body(self, body: bytes) -> None:
        self._body = body.decode()

    def on_message_complete(self) -> None:
        self._parsed = True
