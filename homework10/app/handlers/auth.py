from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import app
from app.models import User
from app.services import config
from app.services.auth import Token, authenticate_user, create_access_token, get_user, \
    get_password_hash


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if await get_user(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with that username already exists',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return (
        await User.create(
            username=form_data.username,
            hashed_password=get_password_hash(form_data.password)
        )
    ).to_dict()
