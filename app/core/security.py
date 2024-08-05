# api_gateway/app/core/security.py

from datetime import datetime, timedelta
from typing import Union
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Configuración de los detalles de seguridad
SECRET_KEY = "ultrasecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Esquema OAuth2 para obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


class TokenData(BaseModel):
    username: str
    scopes: list[str] = []


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, scopes=payload.get("scopes", []))
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


async def get_current_active_user(current_user: TokenData = Depends(get_current_user)):
    if current_user.scopes is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
