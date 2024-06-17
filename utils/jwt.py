import jwt
from config.app_config import JwtConfig
from datetime import timedelta, datetime, timezone


def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode,
        JwtConfig.JWT_ACESSS_SECRET_KEY,
        algorithm=JwtConfig.JWT_ACESSS_ALGORITHM,
    )
    return encode_jwt


def verify_aceess_token(token: str) -> any:
    return jwt.decode(
        token,
        JwtConfig.JWT_ACESSS_SECRET_KEY,
        algorithms=[JwtConfig.JWT_ACESSS_ALGORITHM],
    )
