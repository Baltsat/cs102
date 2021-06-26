from app import app
from app.models import Note, User
from app.services.auth import get_current_user
from fastapi import Depends


@app.get("/note")
async def h(current_user: User = Depends(get_current_user)):
    return [i.to_dict() for i in await Note.filter(author=current_user)]
