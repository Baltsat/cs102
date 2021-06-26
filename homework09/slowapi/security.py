# type: ignore
import http
from functools import wraps
import datetime as dt
import jwt

from slowapi import Request, Response


class Security:
    def __init__(self, secret, algorithm, exp):
        self.secret = secret
        self.algorithm = algorithm
        self.exp = exp
        self.users = set()
        status = http.HTTPStatus(401)
        self.error = Response(
            status.value, {}, body="\n".join([str(status.value), status.phrase, status.description])
        )

    def add(self, user):
        self.users.add(user)

    def gen_jwt(self, email):
        payload = {"email": email, "exp": dt.datetime.utcnow() + dt.timedelta(seconds=self.exp)}
        return jwt.encode(payload, self.secret, self.algorithm)

    def check_jwt(self, token):
        try:
            payload = jwt.decode(token, self.secret, self.algorithm)
            email = payload.get("email")
            if email in self.users:
                return True
        except Exception:
            pass
        return False

    def protect(self):
        def wrapper(func):
            @wraps(func)
            def decorated(request: Request, *args, **kwargs):
                bearer = request.headers.get("authorization", "").split(" ")
                if bearer[0] != "Bearer":
                    return self.error
                if not self.check_jwt(bearer[1]):
                    return self.error
                return func(request, *args, **kwargs)

            return decorated

        return wrapper
