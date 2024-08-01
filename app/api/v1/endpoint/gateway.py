# api_gateway/app/api/v1/endpoints/gateway.py

from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

USUARIO_SERVICE_URL = "http://localhost:8001"
VEHICULO_SERVICE_URL = "http://localhost:8002"


@router.post("/user/", response_model=dict)
async def create_user(usuario: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USUARIO_SERVICE_URL}/user/", json=usuario)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.get("/user/{usuario_ci}", response_model=dict)
async def read_user(usuario_ci: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USUARIO_SERVICE_URL}/user/{usuario_ci}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.post("/vehicle/", response_model=dict)
async def create_vehicle(vehicle: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VEHICULO_SERVICE_URL}/vehicle/", json=vehicle)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@router.get("/vehicle/{vehicle_owner}", response_model=dict)
async def read_vehicle(vehicle_owner: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{VEHICULO_SERVICE_URL}/vehicle/{vehicle_owner}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
