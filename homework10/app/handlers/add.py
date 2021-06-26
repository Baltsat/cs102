from app import app
from app.models import Note, User
from app.services.auth import get_current_user
from fastapi import Depends
from pydantic import BaseModel


class NoteModel(BaseModel):
    text: str


@app.put("/note/")
async def h(note: NoteModel, current_user: User = Depends(get_current_user)):
    return (await Note.create(text=note.text, author=current_user)).to_dict()
