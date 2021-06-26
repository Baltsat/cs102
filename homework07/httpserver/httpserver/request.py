import dataclasses
import typing as tp


@dataclasses.dataclass
class HTTPRequest:
    method: str
    url: str
    headers: tp.Dict[str, str]
    body: str
