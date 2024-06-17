from models.user_model import UserInDB
from models.token_model import TokenData
from utils.passwordLib import verify_password
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from typing import Annotated
from utils.jwt import verify_aceess_token
from jwt.exceptions import InvalidTokenError
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

# secret

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: Annotated[str,Depends(oauth2_schema)]):
    creadentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_aceess_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise creadentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise creadentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise creadentials_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
