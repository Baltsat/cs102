import typing as tp
import urllib.parse
from wsgiref.simple_server import make_server
from httpserver import BaseHTTPRequestHandler, HTTPServer

from .request import WSGIRequest
from .response import WSGIResponse


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.base_environ: tp.Dict[str, str] = {}
        self.app: tp.Callable = object

    def setup_environ(self):
        self.base_environ["SERVER_NAME"] = "My Server"
        self.base_environ["GATEWAY_INTERFACE"] = "CGI/1.1"
        self.base_environ["SERVER_PORT"] = str(self.port)

    def set_app(self, app: tp.Callable) -> None:
        self.app = app

    def get_app(self) -> tp.Callable:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        self.server: WSGIServer
        app = self.server.get_app()

        env = self.server.base_environ.copy()
        env.update(request.to_environ())
        resp = self.response_klass()
        bdy = app(env, resp.start_response)
        body = b""
        if isinstance(bdy, list):
            for i in bdy:
                body += i
        resp.body = body
        return resp
