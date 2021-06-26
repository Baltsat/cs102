from fastapi import Depends, HTTPException, status

from app import app

from app.models import User, Note
from app.services.auth import get_current_user


@app.get("/note/{note_id}")
async def h(note_id: int, current_user: User = Depends(get_current_user)):
    note = await Note.filter(author=current_user, id=note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note with that id not found",
        )
    return note.to_dict()
