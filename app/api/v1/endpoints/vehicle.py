from fastapi import APIRouter, HTTPException, Depends
import httpx
from app.core.security import get_current_active_user, TokenData
from app.models.schemas.schemas import *
import os
from dotenv import load_dotenv

router = APIRouter()
VEHICULO_SERVICE_URL = os.getenv("VEHICULO_SERVICE_URL")


# Vehicle routing section

@router.post("/vehicle/", response_model=dict)
async def create_vehicle(
        vehicle: VehicleBase,
        current_user: TokenData = Depends(get_current_active_user)
):
    print(VEHICULO_SERVICE_URL)
    if "vehiculo" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        vehicle_dict = vehicle.dict()
        response = await client.post(f"{VEHICULO_SERVICE_URL}/vehicle/", json=vehicle_dict)
        if response.status_code != 200:
            try:
                detail = response.json()
            except httpx.HTTPStatusError:
                detail = "No JSON response"
            raise HTTPException(status_code=response.status_code, detail=detail)

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
        raise HTTPException(status_code=response.status_code, detail="Vehiculo no encontrado")
    return response.json()


@router.delete("/vehicle/{vehicle_id}", response_model=dict)
async def delete_vehicle(
        vehicle_id: int,
        current_user: TokenData = Depends(get_current_active_user)
):
    if "vehiculo" not in current_user.scopes:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{VEHICULO_SERVICE_URL}/vehicle/{vehicle_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()
