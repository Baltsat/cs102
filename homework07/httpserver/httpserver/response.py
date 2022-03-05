import dataclasses
import typing as tp
from http import HTTPStatus

responses = {
    200: ("OK", "Request fulfilled, document follows"),
    400: ("Bad Request", "Bad request syntax or unsupported method"),
    403: ("Forbidden", "Request forbidden -- authorization will not help"),
    404: ("Not Found", "Nothing matches the given URI"),
    405: ("Method Not Allowed", "Specified method is invalid for this resource."),
    500: (
        "Internal Server Error",
        "The server encountered an internal error and was unable to complete your request.",
    ),
}


@dataclasses.dataclass
class HTTPResponse:
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: bytes = b""

    def to_http1(self) -> bytes:
        status_message = HTTPStatus(self.status).phrase
        # status_message, _ = responses[self.status]
        headers_str = "\n".join([str(i) + ": " + str(self.headers[i]) for i in self.headers])
        return (
            f"HTTP/1.1 {self.status} {status_message}\r\n{headers_str}\n\n".encode()
            + self.body
            + "\r\n".encode()
        )
