import dataclasses
import io
import json
import typing as tp


@dataclasses.dataclass
class Request:
    path: str
    method: str
    query: tp.Dict[str, tp.Any] = dataclasses.field(default_factory=dict)
    body: io.BytesIO = dataclasses.field(default_factory=io.BytesIO)
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)

    def text(self) -> str:
        text = self.body.read().decode('UTF-8')
        return text

    def json(self) -> tp.Dict[str, tp.Any]:
        return json.load(self.body)
