from fastapi import Depends, HTTPException, status

from app import app

from pydantic import BaseModel

from app.models import User, Note
from app.services.auth import get_current_user


class NoteModel(BaseModel):
    text: str


@app.patch("/note/{note_id}")
async def h(note_id: int, note: NoteModel, current_user: User = Depends(get_current_user)):
    note_db = await Note.filter(id=note_id, author=current_user).first()
    if not note_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note with that id not found",
        )
    note_db.text = note.text
    await note_db.save()
    return note_db.to_dict()
