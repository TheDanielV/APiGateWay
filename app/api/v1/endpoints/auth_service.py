# api_gateway/app/api/v1/endpoints/user.py

from fastapi import APIRouter, HTTPException, Depends
import httpx
from app.core.security import get_current_active_user, TokenData
from app.models.schemas.schemas import *
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()  # Cargar variables desde .env

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")


@router.post("/auth_service/", response_model=dict)
async def create_auth_user(
        usuario: AuthBase,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "auth" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        user_dict = usuario.dict()
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/", json=user_dict)
    if response.status_code != 200:
        try:
            detail = response.json()
        except httpx.HTTPStatusError:
            detail = "No JSON response"
        raise HTTPException(status_code=response.status_code, detail=detail)
    return response.json()


@router.post("/auth_service/authenticate/", response_model=dict)
async def authenticate_auth_user(
        usuario: AuthenticateUser,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "auth" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        user_dict = usuario.dict()
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/authenticate", json=user_dict)
    if response.status_code != 200:
        try:
            detail = response.json()
        except httpx.HTTPStatusError:
            detail = "No JSON response"
        raise HTTPException(status_code=response.status_code, detail=detail)
    return response.json()


