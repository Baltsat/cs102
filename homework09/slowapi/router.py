import dataclasses
import http
import typing as tp

from slowapi import Response, Request


@dataclasses.dataclass
class Route:
    path: str
    method: str
    func: tp.Callable

    def matches(self, request):
        path_spl = self.path.split('/')
        req_path_spl = request.path.split('/')
        args = []
        if request.method != self.method:
            return False
        if len(path_spl) == len(req_path_spl):
            for i in range(len(req_path_spl)):
                if path_spl[i].startswith('{') and path_spl[i].endswith('}'):
                    args.append(req_path_spl[i])
                else:
                    if path_spl[i] != req_path_spl[i]:
                        return False
            return True
        return False

    def parse_args(self, request):
        path_spl = self.path.split('/')
        req_path_spl = request.path.split('/')
        args = []
        if len(path_spl) == len(req_path_spl):
            for i in range(len(req_path_spl)):
                if path_spl[i].startswith('{') and path_spl[i].endswith('}'):
                    args.append(req_path_spl[i])
            return args

    def handle(self, request):
        return self.func(request, *self.parse_args(request))


class Router:
    def __init__(self):
        self.routes: tp.List[Route] = []

    def resolve(self, request: Request) -> Response:
        for route in self.routes:
            if route.matches(request):
                return route.handle(request)
        status = http.HTTPStatus(404)
        return Response(status.value, {},
                        body='\n'.join([str(status.value), status.phrase, status.description]))

    def add_route(self, route: Route):
        self.routes.append(route)
