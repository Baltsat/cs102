from app import app
from app.models import Note, User
from app.services.auth import get_current_user
from fastapi import Depends
from pydantic import BaseModel


class NoteModel(BaseModel):
    text: str


@app.delete("/note/{note_id}")
async def h(note_id: int, current_user: User = Depends(get_current_user)):
    await Note.filter(id=note_id, author=current_user).delete()
    return {"success": True}
