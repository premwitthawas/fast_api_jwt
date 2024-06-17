from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from models.token_model import Token
from models.user_model import User
from utils.jwt import create_access_token
from datetime import timedelta
from controllers.user_controller import authenticate_user, fake_users_db, get_current_active_user
from config.app_config import JwtConfig
router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(JwtConfig.JWT_ACCESS_EXPIRATION_TIME_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me",response_model=User)
async def get_current_user(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user
