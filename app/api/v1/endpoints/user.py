# api_gateway/app/api/v1/endpoints/user.py
from typing import List

from fastapi import APIRouter, HTTPException, Depends
import httpx
from app.core.security import get_current_active_user, TokenData
from app.models.schemas.schemas import UserBase, VehicleBase
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()  # Cargar variables desde .env

USUARIO_SERVICE_URL = os.getenv("USUARIO_SERVICE_URL")
VEHICULO_SERVICE_URL = os.getenv("VEHICULO_SERVICE_URL")


@router.post("/user/", response_model=dict)
async def create_user(
        usuario: UserBase,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "usuario" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        user_dict = usuario.dict()
        response = await client.post(f"{USUARIO_SERVICE_URL}/user/", json=user_dict)
    if response.status_code != 200:
        print(response)
        try:
            detail = response.json()
        except httpx.HTTPStatusError:
            detail = "No JSON response"
        raise HTTPException(status_code=response.status_code, detail=detail)
    return response.json()


@router.get("/user/{usuario_ci}", response_model=dict)
async def read_user(
        usuario_ci: str,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "usuario" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USUARIO_SERVICE_URL}/user/{usuario_ci}")
    if response.status_code != 200:
        try:
            detail = response.json()
        except httpx.HTTPStatusError:
            detail = "No JSON response"
        raise HTTPException(status_code=response.status_code, detail=detail)
    return response.json()


@router.get("/user/auth_token/{user_token}", response_model=dict)
async def read_user(
        user_token: str,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "usuario" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USUARIO_SERVICE_URL}/user/user_token/{user_token}")
    if response.status_code != 200:
        try:
            detail = response.json()
        except httpx.HTTPStatusError:
            detail = "No JSON response"
        raise HTTPException(status_code=response.status_code, detail=detail)
    return response.json()
