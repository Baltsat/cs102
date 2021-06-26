import dataclasses
import typing as tp
from http import HTTPStatus


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        status_message = HTTPStatus(self.status).phrase
        headers_str = "\n".join([str(i) + ": " + str(self.headers[i]) for i in self.headers])
        return (
            f"HTTP/1.1 {self.status} {status_message}\r\n{headers_str}\n\n".encode()
            + self.body
            + "\r\n".encode()
        )
