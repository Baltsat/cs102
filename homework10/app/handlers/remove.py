from fastapi import Depends

from app import app

from pydantic import BaseModel

from app.models import User, Note
from app.services.auth import get_current_user


class NoteModel(BaseModel):
    text: str


@app.delete("/note/{note_id}")
async def h(note_id: int, current_user: User = Depends(get_current_user)):
    await Note.filter(id=note_id, author=current_user).delete()
    return {"success": True}
