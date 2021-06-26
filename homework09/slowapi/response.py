# type: ignore
import dataclasses
import json
import typing as tp


@dataclasses.dataclass
class Response:
    content_type: tp.ClassVar[tp.Optional[str]] = None
    status: int
    headers: tp.Dict[str, str] = dataclasses.field(default_factory=dict)
    body: tp.Optional[tp.Any] = None


@dataclasses.dataclass
class JsonResponse(Response):
    content_type: tp.ClassVar[str] = "application/json"
    data: tp.Dict[str, tp.Any] = dataclasses.field(default_factory=dict)
    status: int = 200

    def __init__(self, data, serializer=None, encoding="utf8", *args, **kwargs):
        class JSONEncoder(json.JSONEncoder):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.func = serializer

            def default(self, o):
                if self.func is not None:
                    r = self.func(o)
                    if r is not None:
                        return r
                return json.JSONEncoder.default(self, o)

        try:
            content = json.dumps(data, ensure_ascii=False, cls=JSONEncoder)
        except Exception as err:
            content = "{0} can't be jsonlized, due to {1}".format(data, err)

        super(JsonResponse, self).__init__(self.status, body=content)
