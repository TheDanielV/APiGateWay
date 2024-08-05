# api_gateway/app/api/v1/endpoints/gateway.py

from fastapi import APIRouter, HTTPException, Depends
import httpx
from app.core.security import get_current_active_user, TokenData

router = APIRouter()

USUARIO_SERVICE_URL = "https://user--zmggq4s.internal.orangecliff-243aedf8.australiaeast.azurecontainerapps.io"
VEHICULO_SERVICE_URL = "https://vehicle--re5k1ap.orangecliff-243aedf8.australiaeast.azurecontainerapps.io"


@router.post("/user/", response_model=dict)
async def create_user(
        usuario: dict,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "usuario" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USUARIO_SERVICE_URL}/user/", json=usuario)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
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
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/vehicle/", response_model=dict)
async def create_vehicle(
        vehicle: dict,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "vehiculo" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VEHICULO_SERVICE_URL}/vehicle/", json=vehicle)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.get("/vehicle/{vehicle_owner}", response_model=dict)
async def read_vehicle(
        vehicle_owner: str,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "vehiculo" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{VEHICULO_SERVICE_URL}/vehicle/{vehicle_owner}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
