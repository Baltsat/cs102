from app import app
from starlette.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static", html=True), name="static")
