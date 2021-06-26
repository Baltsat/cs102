# type: ignore
import datetime as dt
import typing as tp

from slowapi import JsonResponse, SlowAPI, Request
from slowapi.middlewares import CORSMiddleware
from slowapi.security import Security

application = SlowAPI()
notes: tp.Dict[int, tp.Dict[str, tp.Any]] = {}
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 300
users = Security(JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS)


def dt_json_serializer(o):
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()


@application.post("/api/jwt-auth/")
def login(request: Request) -> JsonResponse:
    user_data = request.json()
    email = user_data["email"]
    users.add(email)
    return JsonResponse(data={"token": users.gen_jwt(email)})


@application.post("/api/notes")
@users.protect()
def add_note(request: Request) -> JsonResponse:
    note = request.json()
    note_id = len(notes) + 1
    note["id"] = note_id
    note["pub_date"] = dt.datetime.now()
    notes[note_id] = note
    return JsonResponse(data=note, serializer=dt_json_serializer)


@application.get("/api/notes")
def get_notes(request: Request) -> JsonResponse:
    notes_list = list(notes.values())
    return JsonResponse(data={"notes": notes_list}, serializer=dt_json_serializer)


@application.get("/api/notes/{id}")
def get_note(request: Request, id: int) -> JsonResponse:
    note_id = int(id)
    return JsonResponse(data=notes[note_id], serializer=dt_json_serializer)


@application.patch("/api/notes/{id}")
def update_note(request: Request, id: int) -> JsonResponse:
    note_id = int(id)
    data = request.json()
    note = notes[note_id]
    note["title"] = data["title"]
    note["body"] = data["body"]
    return JsonResponse(data={})


application.add_middleware(CORSMiddleware)


def main():
    from wsgiserver import WSGIRequestHandler, WSGIServer

    server = WSGIServer(port=8080, request_handler_cls=WSGIRequestHandler)
    server.set_app(application)
    server.serve_forever()
    #
    #
    if __name__ == "__main__":
        main()
